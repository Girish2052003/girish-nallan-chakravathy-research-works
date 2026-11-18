from collections import Counter
from itertools import product
import unittest
from unittest.mock import patch

from systematic_kem import SystematicKEM, research_profile
from matched_kem import MatchedKEM
from outer_kem import ProjectedRadiusKEM
from quotient_kem import RowQuotient
from projected_kem import _COINS, _hash, _signed_subset, _unpack_dense


class SystematicTests(unittest.TestCase):
    def test_normalization_and_conditioning_probability(self):
        # Two rows, three columns. Invertible first two columns normalize to I.
        tails = Counter()
        for a, b, c, d, y, z in product(range(3), repeat=6):
            det = (a*d-b*c) % 3
            if det == 0:
                continue
            tail = ((d*y-b*z)*det % 3, (a*z-c*y)*det % 3)
            tails[tail] += 1
            self.assertEqual(((a*tail[0]+b*tail[1]) % 3, (c*tail[0]+d*tail[1]) % 3), (y, z))
        self.assertEqual(set(tails), set(product(range(3), repeat=2)))
        self.assertEqual(set(tails.values()), {48})
        self.assertGreater(sum(tails.values()), 3**6 // 2)

    def test_explicit_rowspace_and_selected_row_encryption(self):
        kem = SystematicKEM(MatchedKEM(5, 1, 1, nonce_bytes=1), nonce_bytes=0)
        public, private = kem.keygen()
        seed = public[:32]
        base = kem.base
        p = base.source
        checks = base._checks(private[32:])
        public_row = kem._public_checks(public)
        rows = []
        for i in range(p.d):
            tail = kem._tail_row(seed, i)
            suffix = public_row(i, tail)
            self.assertEqual(list(suffix), kem._check_row(i, tail, checks))
            pivot = bytearray(p.d)
            pivot[i] = 1
            rows.append(pivot + tail + suffix)
        quotient = RowQuotient(base.N, rows)
        self.assertEqual(len(quotient.basis), p.d)
        for mi in range(8):
            message = bytes([mi])
            tape = _hash(_COINS, base.suite, seed, message, p.coin_bytes)
            joint = int.from_bytes(tape, 'big') % p.coin_count
            error = _signed_subset(p.N, p.z, joint % p.noise_count)
            # Deliberately add a nonzero public linear combination.
            word = bytearray(sum(row[j] for row in rows) % 3 for j in range(base.N))
            for i, v in enumerate(base._outer.encode(mi), start=base.m):
                word[i] = (word[i]+v) % 3
            for i, sign in error:
                word[i] = (word[i]+sign) % 3
            wire = kem._encode(seed, message, public_row)
            self.assertEqual(_unpack_dense(wire, base.N-p.d), quotient.project(word))

    def test_both_layouts_and_private_replay(self):
        for cls, sizes in ((MatchedKEM, (752,33,34)), (ProjectedRadiusKEM, (393,33,25))):
            kem = SystematicKEM(cls(8,1,3,nonce_bytes=8), nonce_bytes=4)
            with patch('secrets.token_bytes', side_effect=lambda n: bytes(range(n))):
                pk, sk = kem.keygen()
            with patch('secrets.randbits', return_value=5), patch.object(
                kem, '_tail_row', wraps=kem._tail_row
            ) as rows:
                ct, key = kem.encaps(pk)
                self.assertLessEqual(rows.call_count, 3)
            with patch.object(kem, '_public', side_effect=AssertionError('full key regenerated')), patch.object(
                kem, '_tail_row', wraps=kem._tail_row
            ) as rows:
                self.assertEqual(kem.decaps(sk, ct), key)
                self.assertLessEqual(rows.call_count, 3)
            self.assertEqual((len(pk), len(sk), len(ct)), sizes)
            self.assertEqual(kem.ciphertext_bytes_for(pk), len(ct))
            self.assertIsNone(kem.decaps(sk, ct[:-1]))
            self.assertIsNone(kem.decaps(sk, bytes([ct[0]^1]) + ct[1:]))
            with self.assertRaises(ValueError):
                kem.encaps(pk[:32]+bytes([255])*(len(pk)-32))

    def test_registered_widths_at_every_key(self):
        for target, perfect, short in ((128, 1083802, 849798), (192, 2397431, 1871132),
                                      (256, 4232857, 3297407)):
            self.assertEqual(research_profile(target, full_radius=True).ciphertext_bytes, perfect)
            self.assertEqual(research_profile(target).ciphertext_bytes, short)


if __name__ == '__main__':
    unittest.main()
