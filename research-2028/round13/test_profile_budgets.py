"""Checks of the query-budget arithmetic. No oracle or target is evaluated."""
from fractions import Fraction
from math import asin, ceil, pi, sin, sqrt
import unittest

from profile_budgets import (
    certified_exponent, first_power_above, half_recovery_threshold,
    point_bytes, profile_row, reduction_threshold,
)


class ProfileBudgetTests(unittest.TestCase):
    def test_exact_integer_profiles_and_minimal_encodings(self):
        expected = {
            128: (82, 164, 33, 259, 327, 65),
            191: (122, 243, 49, 385, 486, 97),
            192: (122, 244, 49, 387, 489, 97),
            256: (163, 325, 65, 515, 650, 129),
        }
        for bits, values in expected.items():
            with self.subTest(bits=bits):
                row = profile_row(bits)
                self.assertEqual(tuple(row[k] for k in (
                    'classical_trits', 'quantum_trits', 'quantum_bytes',
                    'seed_bits', 'proof_trits', 'proof_bytes')), values)
                B = 1 << bits
                n = row['classical_trits']
                self.assertLess((3**(n-1) + 1)//2, B)
                self.assertGreaterEqual((3**n + 1)//2, B)
                for name, base, bounds in (
                    ('quantum_trits', 3, half_recovery_threshold(B)),
                    ('seed_bits', 2, half_recovery_threshold(B)),
                    ('proof_trits', 3, reduction_threshold(B, B))):
                    n = row[name]
                    self.assertLess(base**(n-1), bounds[0])
                    self.assertLess(bounds[1], base**n)
                for n, width in ((row['quantum_trits'], row['quantum_bytes']),
                                 (row['proof_trits'], row['proof_bytes'])):
                    self.assertLess(256**(width-1), 3**n)
                    self.assertGreaterEqual(256**width, 3**n)

    def test_small_query_thresholds_against_direct_trigonometry(self):
        for budget in range(1, 8):
            for marked in (1, 2, 5):
                low, high = half_recovery_threshold(budget, marked)
                cutoff = marked / sin(pi/(8*budget - 4))**2
                self.assertLess(float(low), cutoff)
                self.assertGreater(float(high), cutoff)
                for domain in range(marked, 150):
                    theta = asin(sqrt(marked/domain))
                    # Use direct probabilities rather than the first-passage formula.
                    best = max(sin((2*j+1)*theta)**2 for j in range(budget))
                    if abs(best - 0.5) > 1e-11:
                        self.assertEqual(best < 0.5, domain > cutoff)

    def test_proof_method_boundary_for_small_unequal_budgets(self):
        for h in (1, 2, 4):
            for q in (0, 1, 3):
                low, high = reduction_threshold(h, q)
                cutoff = 1 / sin(asin(1/(4*h))/(2*q+1))**2
                self.assertLessEqual(float(low), cutoff)
                self.assertGreaterEqual(float(high), cutoff)
                for n in (int(cutoff)-1, ceil(cutoff)+1):
                    angle = asin(1/sqrt(n))
                    best = max(sin((2*j+1)*angle)**2 for j in range(q+1))
                    self.assertEqual(2*h*sqrt(best) <= 0.5, n >= cutoff)
        self.assertEqual(half_recovery_threshold(8, 3),
                         tuple(3*x for x in half_recovery_threshold(8)))

    def test_input_errors_and_unresolved_enclosures(self):
        self.assertEqual(first_power_above(3, 9), 3)
        self.assertEqual(certified_exponent(3, (Fraction(10), Fraction(17))), 3)
        with self.assertRaises(ArithmeticError):
            certified_exponent(3, (Fraction(9), Fraction(17)))
        for action in (lambda: first_power_above(1, 1), lambda: point_bytes(True),
                       lambda: half_recovery_threshold(-1), lambda: half_recovery_threshold(2, 0),
                       lambda: reduction_threshold(0, 2), lambda: reduction_threshold(1, -1)):
            with self.assertRaises(ValueError):
                action()


if __name__ == '__main__':
    unittest.main()
