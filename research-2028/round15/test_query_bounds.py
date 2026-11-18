import unittest
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb

from query_bounds import certificates, classical_column_queries, coordinate_queries


def squared_character_mean(values):
    counts = Counter(values)
    a, b, c = (counts[i] for i in range(3))
    return Fraction(a*a + b*b + c*c - a*b - b*c - c*a, (a+b+c)**2)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b)) % 3


class QueryBoundsTests(unittest.TestCase):
    def test_key_second_moment(self):
        rows = list(product(range(3), repeat=3))
        supports = [x for x in rows if sum(v != 0 for v in x) == 2]
        for frequency in ((0, 1), (1, 1), (1, 2)):
            total = Fraction()
            for B in product(rows, repeat=2):
                total += squared_character_mean(
                    dot(frequency, tuple(dot(row, s) for row in B)) for s in supports
                )
            self.assertEqual(total / (len(rows)**2), Fraction(1, len(supports)))

    def test_payload_character_cancelation(self):
        rows = list(product(range(3), repeat=3))
        words = list(product(range(3), repeat=2))
        for frequency in ((1, 0, 0), (2, 1, 0), (2, 1, 2)):
            exceptions = 0
            for G in product(rows, repeat=2):
                projected = tuple(dot(row, frequency) for row in G)
                exceptional = projected == (0, 0)
                exceptions += exceptional
                # A fixed added noise vector contributes only a fixed phase.
                for phase in range(3):
                    self.assertEqual(squared_character_mean(
                        (dot(projected, u) + phase) % 3 for u in words
                    ), int(exceptional))
            self.assertEqual(Fraction(exceptions, len(rows)**2), Fraction(1,9))

    def test_partial_column_law(self):
        # The signed support is fixed and conditioned on a one-trit syndrome.
        # Enumerate each prescribed non-covering choice of two visible columns.
        for y in range(3):
            signed = (1, 2, 1, 0)
            matrices = [row for row in product(range(3), repeat=4) if dot(row, signed) == y]
            for i, j in ((0, 1), (1, 2), (0, 3)):
                observed = Counter((m[i], m[j]) for m in matrices)
                self.assertEqual(set(observed.values()), {3})
                self.assertEqual(len(observed), 9)

    def test_certificate_logic_against_exact_character_counts(self):
        for n in (10, 31, 130):
            for log_denominator in (7, 30, 81):
                for bits in (1, 8):
                    for sqrt in (False, True):
                        q = coordinate_queries(n, log_denominator, bits, square_root=sqrt)
                        number = sum(comb(n,j) * 2**j for j in range(1, 2*q+1))
                        if sqrt:
                            self.assertLessEqual(number << (2*bits), 4 << log_denominator)
                        else:
                            self.assertLessEqual(number << bits, 1 << log_denominator)
        for r, w, bits in ((16, 4, 5), (14, 2, 30), (10, 9, 1)):
            q = classical_column_queries(r, w, bits)
            self.assertLessEqual(comb(q, w) << bits, comb(r, w))
            self.assertGreater(comb(q+1, w) << bits, comb(r, w))

    def test_published_profiles(self):
        for dimensions, expected in (
            ((5638720, 8446464, 768, 16902389, 5630464), (363, 636758, 6560396)),
            ((14426208, 21612672, 1152, 43241800, 14407680), (547, 1629420, 18261799)),
            ((25616512, 38376960, 1536, 76775832, 25583616), (753, 2893365, 33821781)),
        ):
            self.assertEqual(certificates(*dimensions), expected)


if __name__ == '__main__':
    unittest.main()
