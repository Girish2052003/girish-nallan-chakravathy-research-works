"""Exact finite checks of the ternary Fourier identity in WITNESS_PROOF.md."""

from fractions import Fraction
from itertools import product
import unittest


ROWS = tuple(product(range(3), repeat=2))
SECRETS = tuple(row for row in ROWS if sum(value != 0 for value in row) == 1)


def dot(row, secret):
    return sum(value * coordinate for value, coordinate in zip(row, secret)) % 3


def in_coordinate_image(row, target):
    return target in {row[0], -row[0] % 3, row[1], -row[1] % 3}


def first_coordinate_equals_target(row, target):
    return row[0] == target


def amplitude(row, secret, accepts):
    # Count signed paths by exponent of omega, where 1+omega+omega^2=0.
    buckets = [0, 0, 0]
    syndrome = dot(row, secret)
    for r, b, c in product(ROWS, range(3), range(3)):
        updated_row = tuple((a + b * x) % 3 for a, x in zip(row, r))
        updated_target = (syndrome + c * b) % 3
        sign = 1 - 2 * int(accepts(updated_row, updated_target))
        buckets[(c - dot(r, secret)) % 3] += sign
    n = len(ROWS) * 9
    return (Fraction(buckets[0] - buckets[2], n),
            Fraction(buckets[1] - buckets[2], n))


class FourierWitnessTests(unittest.TestCase):
    def test_exact_averages_and_norms(self):
        for accepts in (in_coordinate_image, first_coordinate_equals_target):
            with self.subTest(predicate=accepts.__name__):
                p_real = Fraction(sum(accepts(row, dot(row, secret))
                                      for row, secret in product(ROWS, SECRETS)),
                                  len(ROWS) * len(SECRETS))
                p_uniform = Fraction(sum(accepts(row, y)
                                         for row, y in product(ROWS, range(3))),
                                     len(ROWS) * 3)
                gap = p_real - p_uniform
                self.assertNotEqual(gap, 0)
                values = [amplitude(row, secret, accepts)
                          for row, secret in product(ROWS, SECRETS)]
                self.assertEqual(sum(a for a, _ in values) / len(values), -2 * gap / 3)
                self.assertEqual(sum(b for _, b in values), 0)
                average_norm = sum(a * a - a * b + b * b for a, b in values) / len(values)
                self.assertGreaterEqual(average_norm, 4 * gap * gap / 9)


if __name__ == "__main__":
    unittest.main()
