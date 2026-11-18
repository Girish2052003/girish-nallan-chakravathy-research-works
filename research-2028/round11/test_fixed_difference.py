"""Finite-field identities used in the sparse-cubic fixed-challenge bound."""

from itertools import product
import unittest


FIELD = range(3)


def difference(polynomial, base, shift):
    moved = tuple((a + h) % 3 for a, h in zip(base, shift))
    return (polynomial(*moved) - polynomial(*base)) % 3


class FixedDifferenceTests(unittest.TestCase):
    def test_reduced_cubic_types_after_pinning(self):
        # With the first two coordinates fixed, xyz is affine in z.
        # With the squared coordinate fixed, x²y is affine in y.
        for poly, width in ((lambda x, y, z: x*y*z, 3),
                             (lambda x, y: x*x*y, 2)):
            for shift in product(FIELD, repeat=width):
                for prefix in product(FIELD, repeat=width-1):
                    values = [difference(poly, prefix + (t,), shift) for t in FIELD]
                    self.assertEqual((values[0] - 2*values[1] + values[2]) % 3, 0)

    def test_compiler_exception_restricts_to_affine_fibres(self):
        poly = lambda s, m, n: -s*m*n
        for s, m, n in product(FIELD, repeat=3):
            delta = difference(poly, (s, m, n), (1, 0, 0))
            self.assertEqual(delta, (-m*n) % 3)
        for target in FIELD:
            direct = {(s, m, n) for s, m, n in product(FIELD, repeat=3)
                      if difference(poly, (s, m, n), (1, 0, 0)) == target}
            restricted = set()
            for m in FIELD:
                valid_n = [n for n in FIELD if (m*n + target) % 3 == 0]
                restricted.update((s, m, n) for s in FIELD for n in valid_n)
            self.assertEqual(direct, restricted)


if __name__ == "__main__":
    unittest.main()
