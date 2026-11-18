"""Independent small-codeword and bounded-distance checks for the public outer code."""
from itertools import product
from random import Random
import unittest

from outer_code import RSOuter, rs_shape


def f9_add(a, b):
    return (a % 3 + b % 3) % 3 + 3*((a // 3 + b // 3) % 3)


def f9_mul(a, b):
    # Independent schoolbook multiplication with X^2 = 1+2X.
    a0, a1 = a % 3, a // 3
    b0, b1 = b % 3, b // 3
    return (a0*b0 + a1*b1) % 3 + 3*((a0*b1 + a1*b0 + 2*a1*b1) % 3)


class TestOuterCode(unittest.TestCase):
    def test_shape_is_minimal(self):
        for bits, z in product(range(1, 45), range(6)):
            b, k, n, t = rs_shape(bits, z)
            self.assertTrue((3**b)**(k-1) < 2**bits <= (3**b)**k)
            self.assertEqual(n, k+2*z)
            self.assertEqual(t, b*n)
            self.assertLessEqual(n, 3**b)
            if b > 1:
                smaller = 3**(b-1)
                self.assertTrue(smaller < 2*z or smaller**(smaller-2*z) < 2**bits)

    def test_every_received_word_against_distance_oracle(self):
        code = RSOuter(2, 1)
        self.assertEqual(rs_shape(2, 1), (2, 1, 3, 6))
        for symbols in product(range(9), repeat=3):
            expected = next((m for m in range(4) if symbols.count(m) >= 2), None)
            trits = tuple(x for a in symbols for x in (a % 3, a // 3))
            self.assertEqual(code.decode(trits), expected)

    def test_nonconstant_code_and_every_single_symbol_error(self):
        code = RSOuter(7, 1)
        self.assertEqual((code.b, code.k), (2, 3))
        for m in (0, 1, 8, 9, 48, 80, 81, 127):
            a0, a1, a2 = m % 9, (m // 9) % 9, m // 81
            symbols = [f9_add(a0, f9_mul(x, f9_add(a1, f9_mul(x, a2))))
                       for x in range(code.length)]
            word = tuple(t for v in symbols for t in (v % 3, v // 3))
            self.assertEqual(code.encode(m), word)
            self.assertEqual(code.decode(word), m)
            for i, value in product(range(code.length), range(9)):
                noisy = list(word)
                noisy[2*i:2*i+2] = [value % 3, value // 3]
                self.assertEqual(code.decode(noisy), m)

    def test_extension_degree_three_all_error_counts(self):
        code = RSOuter(8, 5)
        self.assertEqual(rs_shape(8, 5), (3, 2, 12, 36))
        rng = Random(104729)
        for m, errors in product((0, 29, 193, 255), range(6)):
            noisy = list(code.encode(m))
            for i in rng.sample(range(code.length), errors):
                j = 3*i + rng.randrange(3)
                noisy[j] = (noisy[j]+1+rng.randrange(2)) % 3
            self.assertEqual(code.decode(noisy), m)

    def test_zero_radius_and_malformed_input(self):
        code = RSOuter(4, 0)
        for m in range(16):
            self.assertEqual(code.decode(code.encode(m)), m)
        for word in (None, (), (0, 0, 3), (0, 0, True)):
            self.assertIsNone(code.decode(word))
        for m in (-1, True, 16):
            with self.assertRaises(ValueError):
                code.encode(m)
        for bits, z in ((0, 0), (1, -1), (1.0, 0)):
            with self.assertRaises(ValueError):
                rs_shape(bits, z)


if __name__ == '__main__':
    unittest.main()
