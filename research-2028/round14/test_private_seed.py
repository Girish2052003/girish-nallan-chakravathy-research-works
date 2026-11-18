"""Checks for the optional secret seed wire format and bounded rank sampler."""
from collections import Counter
import unittest

from differential_pke import Params
from private_seed import PrivateSeedKEM, research_profile
from seeded_matrix import SeededMatrixKEM


class PrivateSeedTests(unittest.TestCase):
    def test_interoperability_both_outer_codes(self):
        for outer in ('repeat', 'rs'):
            p = Params(4, 4, 2, 80, 2, 1, 9, outer)
            kem = PrivateSeedKEM(p, nonce_bytes=5)
            public, private = kem.keygen()
            exact = SeededMatrixKEM(p, nonce_bytes=5)
            self.assertEqual((len(public), len(private)), (exact.public_bytes, 33))
            ct, key = exact.encaps(public)
            self.assertEqual(kem.decaps(private, ct), key)
            ct, key = kem.encaps(public)
            expanded = private[:32] + kem._supports(private[32:])
            self.assertEqual(exact.decaps(expanded, ct), key)
            self.assertEqual(kem.decaps(private, ct), key)
            self.assertIsNone(kem.decaps(private, bytes([ct[0] ^ 1]) + ct[1:]))
            self.assertIsNone(kem.decaps(private, ct[:-1]))
            with self.assertRaises(ValueError):
                kem.decaps(private[:-1], ct)

    def test_slot_counts_independent_enumeration(self):
        p = Params(2, 1, 1, 3, 1, 0, 0)
        kem = PrivateSeedKEM(p, check_slack=0)
        self.assertEqual(kem.tape_bytes, 2)
        counts = Counter(kem._rank_tape(i.to_bytes(2, 'big')) for i in range(65536))
        self.assertEqual(len(counts), 6 * 4)
        for a in range(6):
            for b in range(4):
                self.assertEqual(counts[bytes((a, b))], (43 if a < 4 else 42)*64)

    def test_named_research_profiles(self):
        for target, expected in (
            (128, (12285243257, 80, 3348787)),
            (192, (53618422002, 96, 8567191)),
            (256, (126797581733, 112, 15210996)),
        ):
            kem = research_profile(target)
            self.assertEqual((kem.public_bytes, kem.private_bytes, kem.ciphertext_bytes), expected)
        with self.assertRaises(ValueError):
            research_profile(0)

    def test_seed_width_and_rejection(self):
        p = Params(3, 1, 1, 9, 1, 0, 5)
        for width, vector in ((48, '0c070b'), (64, '080b0d'), (80, '0c0503')):
            kem = PrivateSeedKEM(p, private_seed_bytes=width)
            _, private = kem.keygen()
            self.assertEqual(len(private), 32 + width)
            self.assertEqual(kem._supports(bytes(width)), bytes.fromhex(vector))
        with self.assertRaises(ValueError):
            PrivateSeedKEM(p, private_seed_bytes=0)
        with self.assertRaises(ValueError):
            PrivateSeedKEM(p, check_slack=-1)
        with self.assertRaises(ValueError):
            kem._rank_tape(bytes(kem.tape_bytes + 1))


if __name__ == '__main__':
    unittest.main()
