"""Finite checks for the Round 16 public-evaluation size bound."""
from fractions import Fraction
from itertools import product
import unittest


def features(linear, x):
    return (*linear, *(a * b % 3 for i, a in enumerate(x) for b in x[i:]))


def evaluate(matrix, linear, x):
    vector = features(linear, x)
    return tuple(sum(a * b for a, b in zip(vector, column)) % 3
                 for column in zip(*matrix))


class EvaluationTests(unittest.TestCase):
    def test_exact_minimum_distance_with_linear_and_quadratic_inputs(self):
        # All scalar difference functions for h=1, n=2. Output equality
        # reduces to equality in one scalar coordinate where keys differ.
        inputs = list(product(range(3), repeat=3))
        agreements = []
        for coefficients in product(range(3), repeat=4):
            if any(coefficients):
                matrix = [(v,) for v in coefficients]
                agreements.append(sum(evaluate(matrix, (u,), (x, y)) == (0,)
                                      for u, x, y in inputs))
        self.assertEqual(Fraction(max(agreements), len(inputs)), Fraction(5, 9))

    def test_prescribed_queries_recover_all_multivariate_rows(self):
        # h=2, n=3, arbitrary t=2 recipient check vectors.
        rows = ((1, 1), (2, 0), (0, 2), (2, 1), (1, 0), (1, 2), (0, 1), (2, 2))
        basis = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        squares = [evaluate(rows, (0, 0), x) for x in basis]
        recovered = [evaluate(rows, u, (0, 0, 0)) for u in [(1, 0), (0, 1)]]
        for i in range(3):
            for j in range(i, 3):
                if i == j:
                    recovered.append(squares[i])
                else:
                    x = tuple(a + b for a, b in zip(basis[i], basis[j]))
                    mixture = evaluate(rows, (0, 0), x)
                    recovered.append(tuple((v-a-b) % 3 for v, a, b
                                           in zip(mixture, squares[i], squares[j])))
        self.assertEqual(tuple(recovered), rows)

    def test_threshold_and_exact_byte_floor(self):
        factor = Fraction(99, 100)**16 - Fraction(7, 9)**16 - Fraction(1, 4)
        self.assertGreater(factor, Fraction(1, 2))
        self.assertLess(2**176251, 3**111202)
        self.assertLess(3**190537, 2**301994)
        trits = 12119412 * 5256
        minimum = 12620190503
        self.assertLess(8*(minimum-1), trits * Fraction(176251, 111202) - 1)
        self.assertLess(trits * Fraction(301994, 190537), 8*minimum)
        self.assertEqual(12620284606 - (minimum+32), 94071)
