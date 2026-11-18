from fractions import Fraction
from itertools import combinations, product
from math import comb, prod
import unittest

from baseline import containment, rank_interval, table_row


class DistributionBaseline(unittest.TestCase):
    def test_profile_numbers_and_overlap_tail(self):
        for d, r, w, expected in ((5478678, 8209152, 768, ('448.917', '224.459', '8.911')),
                                  (12119412, 18161280, 1152, ('673.108', '336.554', '43.607')),
                                  (21397976, 32067072, 1536, ('897.300', '448.650', '135.944'))):
            _, low, high, half, tb = table_row(d, r, w)
            self.assertEqual(tuple(f'{v:.3f}' for v in (low, half, tb)), expected)
            self.assertLess(high-low, 10**-20)
            self.assertGreater((r-w)**2, 2*(d-w)**2)
            self.assertLess(r, 1<<25)
            self.assertGreater((d-w)//2 - 7 - 25*254, 1_000_000)
        self.assertLess(Fraction(256, 3**128)+Fraction(256, 1<<1_000_000), Fraction(1, 1<<194))

    def test_second_moment_by_enumerating_small_matrices(self):
        # The planted support is position zero; each containing pair has two columns.
        subsets = tuple(s for s in combinations(range(3), 2) if 0 in s)
        first, second = 0, 0
        for matrix in product(range(3), repeat=6):
            good = sum((matrix[a]*matrix[3+b]-matrix[b]*matrix[3+a]) % 3 != 0
                       for a,b in subsets)
            x = Fraction(good, len(subsets))
            first += x
            second += x*x
        alpha, _ = rank_interval(2)
        self.assertEqual(first / 3**6, alpha)
        shared = [len(set(s) & set(t)) for s in subsets for t in subsets]
        predicted = sum(alpha**2 / prod(1-Fraction(3**i, 3**2) for i in range(j))
                        for j in shared) / len(shared)
        self.assertEqual(second / 3**6, predicted)

    def test_middle_search_certificate_constants(self):
        d, r, w = 12119412, 18161280, 1152
        self.assertGreater(containment(d, r, w), Fraction(1, 1<<673))
        lo, _ = rank_interval(d)
        self.assertGreater(lo, Fraction(11,20))
        self.assertLess(containment(d, r, w), Fraction(1, 1<<672))
        self.assertLess((1<<113)*128*(d+1)**3 + d*r + d+r, 1<<191)
        self.assertGreater(Fraction(15,16)**3 * Fraction(11,20), Fraction(4,9))
