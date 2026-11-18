from fractions import Fraction
import unittest

from matched_kem import research_profile


def inverse_power(exponent):
    return Fraction(1, 1 << exponent)


class MatchedSecurityArithmetic(unittest.TestCase):
    def test_middle_target_reduction_inequalities(self):
        kem = research_profile(192)
        p = kem.source
        queries = 1 << 191
        queries_and_depth = 2 * queries
        self.assertGreater(min(kem.N - p.h, kem.N - p.d), 1000)
        rank_defect = inverse_power(1000)  # upper bound for both rank defects
        coefficient = 2 * (kem.t + 1 / (1 - rank_defect))
        sampling_error = (2 * rank_defect + 2 * inverse_power(p.slack)
                          + 2 * p.d * inverse_power(8 * kem.slack_bytes))
        tail = (32 * queries * inverse_power(p.bits // 2)
                + 240 * queries**2 * inverse_power(4 * kem.nonce_bytes)
                + 2 * queries * inverse_power(p.bits)
                + 4 * queries * inverse_power(4 * kem.seed_bytes)
                + 2 * kem.t * inverse_power(8 * kem.slack_bytes))
        self.assertLess(coefficient, 10516)
        self.assertLess(sampling_error, inverse_power(318))
        self.assertLess(tail, inverse_power(57))

        for gap_bits, guess_ceiling in ((224, Fraction(508, 1000)),
                                        (280, Fraction(1, 2) + inverse_power(34))):
            base_gap = coefficient * inverse_power(gap_bits) + sampling_error
            residual = 2 * guess_ceiling - 1 - tail
            self.assertGreater(residual, 0)
            # Compare squared positive quantities to avoid floating point.
            self.assertLess(64 * queries_and_depth * base_gap, residual**2)

        base_floor = (Fraction(1, 8) - tail)**2 / (64 * queries_and_depth)
        decision_floor = (base_floor - sampling_error) / coefficient
        self.assertGreater(decision_floor, inverse_power(221))
        self.assertGreater(Fraction(4, 9) * decision_floor**2, inverse_power(444))
