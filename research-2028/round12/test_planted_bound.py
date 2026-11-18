"""Fixed-pair probability checks on small generated graphs; no key-recovery tool."""

from fractions import Fraction
from itertools import combinations, product
from math import comb
import unittest


def pair_miss(m):
    """Exact conditional probability eta_m, with powers of two cleared."""
    max_product = m * m // 4
    numerator = sum(
        comb(m, r) * (10 * (1 << r) + 1) ** (m - r)
        * (1 << (max_product - r * (m - r)))
        for r in range(m + 1)
    )
    return Fraction(numerator, 12**m * (1 << max_product))


class PlantedBoundTests(unittest.TestCase):
    def test_fixed_pair_on_every_small_label_and_coin_assignment(self):
        # The endpoints have prescribed equal or different labels. Give each
        # unordered pair a fair coin even when its equal-color edge is suppressed.
        for v in range(2, 6):
            pairs = list(combinations(range(v), 2))
            for second in (0, 1):
                missing = total = 0
                for other in product(range(3), repeat=v - 2):
                    colors = (0, second) + other
                    for mask in range(1 << len(pairs)):
                        edges = {pair for bit, pair in enumerate(pairs)
                                 if mask & (1 << bit) and colors[pair[0]] != colors[pair[1]]}
                        common = [w for w in range(2, v) if (0, w) in edges and (1, w) in edges]
                        missing += not any(pair in edges for pair in combinations(common, 2))
                        total += 1
                self.assertEqual(Fraction(missing, total), pair_miss(v - 2) if second == 0 else 1)

    def test_certified_finite_bounds(self):
        for vertices, upper in ((122, '0.151376'), (162, '0.007899'), (256, '0.000005489')):
            estimate = comb(vertices, 2) * pair_miss(vertices - 2) / 3
            limit = Fraction(upper)
            unit = Fraction(1, 10**len(upper.split('.')[1]))
            self.assertLessEqual(estimate, limit)
            self.assertGreater(estimate, limit - unit)
        self.assertGreater(comb(81, 2) * pair_miss(79) / 3, 1)

    def test_disjoint_pair_asymptotic_bound(self):
        for m in range(20):
            self.assertLessEqual(pair_miss(m), Fraction(143, 144) ** (m // 2))


if __name__ == '__main__':
    unittest.main()
