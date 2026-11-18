from fractions import Fraction
from itertools import combinations
from math import comb
import unittest
from unittest.mock import patch

from outer_kem import MatchedKEM, ProjectedRadiusKEM, research_profile


class ShortenedKEMTests(unittest.TestCase):
    def test_profiles_and_certificates(self):
        for target, (checks, public, private, ciphertext, exponent) in {
            128: (2028, 2201315732, 80, 1935303, 399),
            192: (2952, 7088151760, 96, 4272336, 607),
            256: (3888, 16482794077, 112, 7536917, 813),
        }.items():
            kem = research_profile(target)
            self.assertEqual((kem.t, kem.public_bytes, kem.private_bytes, kem.ciphertext_bytes),
                             (checks, public, private, ciphertext))
            self.assertEqual(kem.common_columns, kem.m - (checks - 1) * kem.source.w)
            self.assertLess(kem.N, kem.source.N)
            bound = kem.failure_bound()
            self.assertLess(bound, Fraction(1, 1 << exponent))
            self.assertGreater(bound, Fraction(1, 1 << (exponent + 1)))
            q = 1 << (target - 1)
            self.assertLess(20 * (3 * q + 1)**2 * bound, Fraction(1, 1 << target))

    def test_sampling_moment_against_exact_law(self):
        for n in range(3, 10):
            for w in range(1, n):
                for relevant in range(1, n):
                    hits = [sum(j < relevant for j in support)
                            for support in combinations(range(n), w)]
                    self.assertEqual(len(hits), comb(n, w))
                    moment = Fraction(sum(6**count for count in hits), len(hits))
                    bound = Fraction(n + 5 * relevant, n)**w
                    self.assertLessEqual(moment, bound)
                    for radius in range(w):
                        tail = Fraction(sum(count > radius for count in hits), len(hits))
                        self.assertLessEqual(tail, moment / 6**(radius + 1))

    def test_wire_exchange_and_suite(self):
        kem = ProjectedRadiusKEM(4, 1, 5, slack=32, nonce_bytes=8)
        other = MatchedKEM(4, 1, 5, slack=32, nonce_bytes=8)
        self.assertNotEqual(kem.suite, other.suite)
        with patch('projected_kem.secrets.token_bytes', side_effect=lambda size: bytes(range(size))), \
             patch('projected_kem.secrets.randbits', return_value=3):
            pk, sk = kem.keygen()
            ct, shared = kem.encaps(pk)
        self.assertEqual((len(pk), len(sk), len(ct), len(shared)), (613, 33, 90, 32))
        self.assertEqual(kem.decaps(sk, ct), shared)
        self.assertIsNone(kem.decaps(sk, ct[:-1]))
        self.assertIsNone(kem.decaps(sk, bytes([ct[0] ^ 1]) + ct[1:]))

    def test_full_radius_and_invalid_radii(self):
        full = ProjectedRadiusKEM(4, 1, 5, radius=5)
        self.assertEqual(full.N, full.source.N)
        self.assertEqual(full.failure_bound(), 0)
        for radius in (True, -1, 6):
            with self.assertRaises(ValueError):
                ProjectedRadiusKEM(4, 1, 5, radius=radius)
