"""Exact finite checks for the classical ROM specialization."""
from fractions import Fraction
from itertools import product
import unittest


class ClassicalReductionTests(unittest.TestCase):
    def test_middle_sufficient_gaps_with_prechallenge_and_decoding_error(self):
        queries = 1 << 191
        inverse = lambda bits: Fraction(1, 1 << bits)
        failure = inverse(607)
        remainder = (inverse(316) + queries * inverse(512)
                     + 2 * queries * inverse(896) + 2 * queries * failure
                     + 2 * queries * inverse(512) + 2 * 5256 * inverse(576)
                     + 2 * queries * inverse(512) + 2 * failure)
        for gap, ceiling in ((inverse(20), Fraction(508, 1000)),
                             (inverse(47), Fraction(1, 2) + inverse(34))):
            raw_gap = 11816 * gap + remainder
            self.assertLess((1 + raw_gap) / 2, ceiling)

    def test_middle_systematic_quantum_bound_with_decoding_failures(self):
        queries = 1 << 191
        inverse = lambda bits: Fraction(1, 1 << bits)
        rank_defect = inverse(1000)
        # Both old rectangular generator and parity-check rank defects are tiny.
        # The systematic square is full rank with probability greater than 1/2.
        self.assertLess(4 * (2952 + 1 / (1 - rank_defect)), 11816)
        additive_base = (4 * rank_defect + 4 * inverse(320)
                         + 2 * 12_119_412 * inverse(576))
        self.assertLess(additive_base, inverse(316))
        tail = (32 * queries * inverse(256) + 240 * queries**2 * inverse(448)
                + 2 * queries * inverse(512) + 4 * queries * inverse(256)
                + 2 * 2952 * inverse(576)
                + (20 * (3 * queries + 1)**2 + 2) * inverse(607))
        for eta, ceiling in ((inverse(224), Fraction(508, 1000)),
                             (inverse(280), Fraction(1, 2) + inverse(34))):
            base = 11816 * eta + inverse(316)
            margin = 2 * ceiling - 1 - tail
            self.assertGreater(margin, 0)
            self.assertLess(64 * 2 * queries * base, margin**2)

    def test_good_message_preimage_count_including_decoding_failures(self):
        # All one-bit ciphertext maps on three messages and all decoders.
        for encoding in product(range(2), repeat=3):
            for decoding in product(range(3), repeat=2):
                bad = sum(decoding[c] != m for m, c in enumerate(encoding))
                for queried_ciphertext in range(2):
                    hits = sum(c == queried_ciphertext for c in encoding)
                    self.assertLessEqual(hits, 1 + bad)
