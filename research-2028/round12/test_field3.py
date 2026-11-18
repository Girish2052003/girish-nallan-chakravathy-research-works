"""Independent arithmetic and permutation tests for the CM central maps."""

import unittest

from field3 import Field3, MODULI, _check_modulus


def slow_product(f, x, y):
    """Coefficient convolution using elementary long division."""
    a, b = f.coeffs(x), f.coeffs(y)
    poly = [0] * (2*f.n - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            poly[i+j] += u*v
    for i in range(len(poly)-1, f.n-1, -1):
        for degree, coeff in f.terms:
            poly[i-f.n+degree] -= poly[i]*coeff
    return f.from_coeffs(z % 3 for z in poly[:f.n])


class FieldArithmeticTests(unittest.TestCase):
    def test_moduli_have_verified_degree(self):
        for n, terms in MODULI.items():
            self.assertTrue(_check_modulus(n, terms))
            self.assertIn(n % 3, (1, 2))
        # (T^2+1)^2 = T^4+2T^2+1 over F3 is reducible.
        self.assertFalse(_check_modulus(4, ((0, 1), (2, 2))))
        for n in (0, 3, 81, True, -1):
            with self.assertRaises(ValueError):
                Field3(n)

    def test_naive_product_and_field_identities(self):
        for n in (1, 2, 4):
            f = Field3(n)
            for x in range(f.order):
                self.assertEqual(x, f.from_coeffs(f.coeffs(x)))
                self.assertEqual(f.cube(x), f.power(x, 3))
                self.assertEqual(f.power(x, f.order), x)
                if x:
                    self.assertEqual(f.mul(x, f.inverse(x)), 1)
                for y in range(f.order):
                    self.assertEqual(f.mul(x, y), slow_product(f, x, y))
                    self.assertEqual(f.sub(f.add(x, y), y), x)

    def test_dickson_ladder_against_three_term_recurrence(self):
        f = Field3(4)
        for z in range(f.order):
            prev, value = 2, z
            self.assertEqual(f.dickson(z, 0), 2)
            for j in range(1, 28):
                self.assertEqual(f.dickson(z, j), value)
                prev, value = value, f.sub(f.mul(z, value), prev)

    def test_permutation_all_shifts_small_fields(self):
        for n in (1, 2):
            f = Field3(n)
            for a in range(1, f.order):
                image = set()
                for x in range(f.order):
                    y = f.cm_forward(x, a)
                    image.add(y)
                    self.assertEqual(f.cm_inverse(y, a), x)
                    self.assertEqual(f.cm_inverse_gcd(y, a), x)
                self.assertEqual(len(image), f.order)
        f = Field3(4)
        for x in range(f.order):
            self.assertEqual(f.cm_forward(x), f.neg(f.dickson(f.sub(x, 1), 13)))
            self.assertEqual(f.cm_inverse(f.cm_forward(x)), x)

    def test_large_field_roots_by_two_methods(self):
        for n in (82, 122, 163):
            f = Field3(n)
            # A fixed reproducible full-size target; start from y, not a known x.
            y = f.from_coeffs(tuple((i*i+2*i+1) % 3 for i in range(n)))
            a = f.from_coeffs(tuple((i+1) % 3 for i in range(n)))
            x = f.cm_inverse(y, a)
            self.assertEqual(f.cm_inverse_gcd(y, a), x)
            self.assertEqual(f.cm_forward(x, a), y)

    def test_input_errors(self):
        f = Field3(2)
        for fn in (f.cm_forward, f.cm_inverse, f.cm_inverse_gcd):
            with self.assertRaises(ValueError):
                fn(2, 0)
            with self.assertRaises(ValueError):
                fn(f.order, 1)
        for bad in ((0,), (0, 1, 2), (True, 1), (1, -1)):
            with self.assertRaises(ValueError):
                f.from_coeffs(bad)
        with self.assertRaises(ZeroDivisionError):
            f.inverse(0)


if __name__ == "__main__":
    unittest.main()
