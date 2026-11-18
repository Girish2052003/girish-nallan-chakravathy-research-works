from itertools import product
import unittest
from unittest.mock import patch

from quotient_kem import QuotientKEM, RowQuotient, _COINS, _hash, _unpack_dense
from matched_kem import MatchedKEM
from outer_kem import ProjectedRadiusKEM


class RowQuotientTests(unittest.TestCase):
    def test_all_cosets_in_small_spaces(self):
        words = list(product(range(3), repeat=3))
        for rows in (((0, 1, 2), (1, 1, 2)), ((0, 2, 1), (0, 1, 2)),
                     ((0, 0, 0), (0, 0, 0))):
            space = RowQuotient(3, rows)
            span = {tuple((a*x + b*y) % 3 for x, y in zip(*rows))
                    for a, b in product(range(3), repeat=2)}
            classes = {}
            for v in words:
                canonical = bytes(space.project(v))
                classes.setdefault(canonical, set()).add(v)
                lift = space.lift(canonical)
                self.assertIn(tuple((x-y) % 3 for x, y in zip(v, lift)), span)
            self.assertEqual(set(map(len, classes.values())), {len(span)})
            self.assertEqual(len(classes) * len(span), len(words))

    def test_projection_matches_encryption_including_finite_tape(self):
        for base in (MatchedKEM(4, 1, 2, nonce_bytes=4),
                     ProjectedRadiusKEM(4, 1, 2, radius=1, nonce_bytes=4)):
            for nonce in (0, 4):
                kem = QuotientKEM(base, nonce_bytes=nonce)
                self.assertNotEqual(base.suite, kem.base.suite)
                pk, _ = kem.keygen()
                space = kem._space(pk)
                p = base.source
                for m in (0, 2, 7, 15):
                    message = m.to_bytes(p.message_bytes, 'big')
                    tape = _hash(_COINS, kem.base.suite, pk, message, nonce+p.coin_bytes)
                    full_body = kem.base._body(pk, message, tape[nonce:])
                    projected = space.project(_unpack_dense(full_body, base.N))
                    ct = kem._ciphertext(pk, space, message)
                    self.assertEqual(ct[:nonce], tape[:nonce])
                    self.assertEqual(_unpack_dense(ct[nonce:], len(space.free)), projected)

    def test_exchange_rejection_and_deficient_keys(self):
        kem = QuotientKEM(MatchedKEM(8, 1, 1, nonce_bytes=4))
        for deficient in (False, True):
            row_fn = (lambda seed, i: bytearray(kem.base.m)) if deficient else kem.base._row
            with patch.object(kem.base, '_row', row_fn):
                public, private = kem.keygen()
                ct, k = kem.encaps(public)
                self.assertEqual(kem.decaps(private, ct), k)
                self.assertEqual(len(ct), kem.ciphertext_bytes_for(public))
                if deficient:
                    self.assertGreater(len(ct), kem.full_rank_ciphertext_bytes)
                self.assertIsNone(kem.decaps(private, ct[:-1]))
                self.assertIsNone(kem.decaps(private, bytes([ct[0] ^ 1])+ct[1:]))
                invalid_rank = ct[:4] + b'\xff' * (len(ct)-4)
                self.assertIsNone(kem.decaps(private, invalid_rank))

    def test_short_radius_exchange_and_nonce_framing(self):
        base = ProjectedRadiusKEM(8, 1, 3, nonce_bytes=8)
        kem = QuotientKEM(base, nonce_bytes=4)
        other = QuotientKEM(base, nonce_bytes=0)
        self.assertNotEqual(kem.base.suite, other.base.suite)
        with patch("secrets.token_bytes", side_effect=lambda n: bytes(range(n))), patch(
            "secrets.randbits", return_value=5
        ):
            pk, sk = kem.keygen()
            ct, key = kem.encaps(pk)
        self.assertEqual(kem.decaps(sk, ct), key)
        self.assertEqual((len(pk), len(sk), len(ct), len(key)), (393, 33, 25, 32))

    def test_profile_widths(self):
        from quotient_kem import research_profile
        from projected_kem import packed_width
        previous = ((1083882, 849866), (2397543, 1871234), (4233001, 3297543))
        nonces = {128: 12, 192: 10, 256: 8}
        for target, (big, small) in zip((128, 192, 256), previous):
            for full_radius, old_width in ((True, big), (False, small)):
                kem = research_profile(target, full_radius=full_radius)
                base = kem.base
                body_width = packed_width(base.N-base.source.d)
                self.assertEqual(body_width + base.nonce_bytes, old_width)
                self.assertEqual(body_width + kem.nonce_bytes, kem.full_rank_ciphertext_bytes)
                self.assertEqual(kem.nonce_bytes, 0 if full_radius else nonces[target])


if __name__ == "__main__":
    unittest.main()
