"""Check expansion, binding, decoding and the finite-row lift on small examples."""
from fractions import Fraction
from hashlib import shake_256
import unittest
from unittest.mock import patch

from differential_kem import DifferentialKEM
from differential_pke import Params, _pack_dense
from seeded_matrix import SeededMatrixKEM


class SeededMatrixTests(unittest.TestCase):
    def test_seed_expansion_against_independent_ternary_decoder(self):
        p = Params(3, 3, 2, 5, 1, 0)
        profile = SeededMatrixKEM(p, 10, 10)
        seed = bytes(range(32))
        # 3^5=243 (one packed byte) plus two sampling-slack bytes.
        trits = []
        for j in range(p.d):
            fields = (b'SG-DIFRA/R14/seeded-matrix/row/v1', profile.suite, seed, bytes([j]))
            transcript = b''.join(len(s).to_bytes(8, 'big') + s for s in fields)
            rank = int.from_bytes(shake_256(transcript).digest(3), 'big') % 243
            trits.extend((rank // 3**i) % 3 for i in reversed(range(5)))
        self.assertEqual(profile._setup(seed), _pack_dense(trits))

    def test_sender_receiver_and_profile_binding(self):
        for outer in ('repeat', 'rs'):
            p = Params(2, 3, 2, 16, 1, 1, outer=outer)
            seeded = SeededMatrixKEM(p, nonce_bytes=8)
            seed = bytes(range(32))
            with patch('seeded_matrix.secrets.token_bytes', return_value=seed):
                public, private = seeded.keygen()
            self.assertEqual((public[:32], private[:32]), (seed, seed))
            self.assertEqual((len(public), len(private)), (seeded.public_bytes, seeded.private_bytes))
            adapter = seeded._adapter(seed)
            full_public = adapter.expand_public(public[32:])
            dense = DifferentialKEM(p, nonce_bytes=8)
            for m in range(4):
                with patch('differential_kem.secrets.randbits', return_value=m):
                    ciphertext, key = seeded.encaps(public)
                    self.assertEqual(adapter.full.encaps(full_public), (ciphertext, key))
                    self.assertNotEqual(dense.encaps(full_public), (ciphertext, key))
                self.assertEqual(seeded.decaps(private, ciphertext), key)
                self.assertIsNone(seeded.decaps(private, bytes([ciphertext[0]^1]) + ciphertext[1:]))
                self.assertIsNone(seeded.decaps(bytes([private[0]^1]) + private[1:], ciphertext))
                self.assertIsNone(SeededMatrixKEM(p, 8, 17).decaps(private, ciphertext))

    def test_same_expanded_matrix_different_public_seed(self):
        p = Params(1, 1, 1, 2, 1, 0)
        profile = SeededMatrixKEM(p, 8)
        with patch.object(profile, '_setup', return_value=_pack_dense([1, 2, 0, 1])):
            with patch('seeded_matrix.secrets.token_bytes', return_value=bytes(32)):
                public, private = profile.keygen()
            alt_public = b'x'*32 + public[32:]
            alt_private = b'x'*32 + private[32:]
            with patch('differential_kem.secrets.randbits', return_value=1):
                ct, key = profile.encaps(public)
                alt_ct, alt_key = profile.encaps(alt_public)
            self.assertNotEqual((ct, key), (alt_ct, alt_key))
            self.assertEqual(profile.decaps(alt_private, alt_ct), alt_key)
            self.assertIsNone(profile.decaps(alt_private, ct))

    def test_invalid_wire(self):
        profile = SeededMatrixKEM(Params(1, 1, 1, 1, 1, 0), 8)
        for invalid in (b'', bytes(34), bytes(32)+b'\xff'):
            with self.assertRaises(ValueError):
                profile.encaps(invalid)
        with self.assertRaises(ValueError):
            profile.decaps(b'', b'')
        self.assertIsNone(profile.decaps(bytes(profile.private_bytes), b''))
        with self.assertRaises(ValueError):
            SeededMatrixKEM(profile.params, matrix_slack=-1)

    def test_lift_exact_variation(self):
        for bound in (3, 9, 27, 81, 243):
            Q = 256
            sizes = [len(range(a, Q, bound)) for a in range(bound)]
            distance = sum(abs(Fraction(1,Q)-Fraction(1,bound*sizes[x % bound]))
                           for x in range(Q))/2
            remainder = Q % bound
            self.assertEqual(distance, Fraction(remainder*(bound-remainder), Q*bound))


if __name__ == '__main__':
    unittest.main()
