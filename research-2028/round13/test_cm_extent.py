"""Finite checks for the changing-exponent planar map and dense-key counts."""
from itertools import product
from math import comb, gcd
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'round12'))
from field3 import Field3
from planar_backend import packed_width


def dense_count(n, e):
    return sum((-1)**j * comb(n, j) * comb(n+e-3*j, e-3*j) for j in range(e//3+1))


def difference(field, x, k, a):
    exponent = (3**k+1)//2
    return field.sub(field.power(field.add(x, a), exponent), field.power(x, exponent))


def private_inverse(field, y, k, a):
    r = k % (2*field.n)
    exponent = (3**r+1)//2
    b = pow(exponent-1, -1, field.order**2-1)
    scaled = field.mul(y, field.inverse(field.power(a, exponent)))
    return field.mul(a, field.add(1, field.dickson(field.neg(scaled), b)))


class VariablePlanarTests(unittest.TestCase):
    def test_private_formula_for_all_small_targets(self):
        for n in (1, 2, 4):
            field = Field3(n)
            for k in range(1, 2*n+3):
                if gcd(k, 2*n) != 1:
                    continue
                for a in (1, field.order-1):
                    for y in range(field.order):
                        x = private_inverse(field, y, k, a)
                        self.assertEqual(difference(field, x, k, a), y)

    def test_frobenius_normalization(self):
        for n in (1, 2, 4, 5):
            field = Field3(n)
            for e in range(1, n+1):
                if gcd(e, 2*n) != 1:
                    continue
                a = field.order-1
                for x in range(min(field.order, 29)):
                    reference = difference(field, x, e, a)
                    opposite = difference(field, x, 2*n-e, a)
                    self.assertEqual(field.power(opposite, 3**e), reference)
                    self.assertEqual(difference(field, x, 2*n+e, a), reference)

    def test_true_function_degree_by_coordinate_interpolation(self):
        # Apply the inverse three-point Vandermonde transform on each axis.
        # The list then contains field-valued coefficients in the reduced basis.
        for n, k in ((2, 3), (4, 3), (4, 5)):
            f = Field3(n)
            data = [difference(f, x, k, f.order-1) for x in range(f.order)]
            for j in range(n):
                step = 3**j
                for start in range(0, f.order, 3*step):
                    for i in range(start, start+step):
                        u, v, w = data[i], data[i+step], data[i+2*step]
                        # If y(t)=u+b*t+c*t² then b=w−v, c=−u−v−w.
                        data[i+step] = f.sub(w, v)
                        data[i+2*step] = f.neg(f.add(u, f.add(v, w)))
            max_degree = max(sum(f.coeffs(i)) for i, value in enumerate(data) if value)
            self.assertEqual(max_degree, min(k, 2*n-k))

    def test_dense_counts_and_uniform_dimension_bound(self):
        for n in range(1, 7):
            for e in range(1, n+1):
                mons = tuple(product(range(3), repeat=n))
                count = sum(sum(m) <= e for m in mons)
                self.assertEqual(dense_count(n, e), count)
                self.assertLessEqual(sum(sum(m) <= 6*e for m in mons), count**6)
        for n, trits, pk, ct in ((81, 2_798_603_379, 554_460_177, 17),
                                  (122, 30_902_771_166, 6_122_466_684, 25),
                                  (162, 164_721_340_962, 32_634_643_562, 33)):
            self.assertEqual(n*dense_count(n, 5), trits)
            self.assertEqual((packed_width(trits), packed_width(n)), (pk, ct))


if __name__ == '__main__':
    unittest.main()
