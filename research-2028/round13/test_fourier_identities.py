"""Exact finite identities used by the ternary prediction proof.

These tests check probability identities on small truth tables. They do not
implement a hidden-shift learner or take protocol keys or ciphertexts as input.
"""
from itertools import product
import unittest


class FourierIdentityTests(unittest.TestCase):
    def test_parseval_and_translation_agreement(self):
        for dimension, alphabet in ((1, range(3)), (2, range(2))):
            points = tuple(product(range(3), repeat=dimension))
            size = len(points)
            index = {point: i for i, point in enumerate(points)}
            # The matrix entries are 2 Re(omega^(direction . frequency)).
            character = [
                [2 if sum(x*y for x, y in zip(delta, freq)) % 3 == 0 else -1
                 for freq in points]
                for delta in points
            ]
            translated = [
                [index[tuple((x+d) % 3 for x, d in zip(point, delta))] for point in points]
                for delta in points
            ]
            for values in product(alphabet, repeat=size):
                agreements = [
                    sum(values[i] == values[j] for i, j in enumerate(shift))
                    for shift in translated
                ]
                # Each weight is 2 * size^2 * p_y, computed with integers.
                weights = [
                    sum(count * row[k] for count, row in zip(agreements, character))
                    for k in range(size)
                ]
                self.assertTrue(all(weight >= 0 for weight in weights))
                self.assertEqual(sum(weights), 2 * size**2)
                for count, row in zip(agreements, character):
                    nontrivial_weight = sum(w for w, c in zip(weights, row) if c == -1)
                    self.assertEqual(4 * size * (size-count), 3 * nontrivial_weight)

    def test_excluded_label_residual_on_three_field_elements(self):
        for true_value, candidate, quadratic_value in product(range(3), repeat=3):
            labels = [k for k in range(3) if k != true_value]
            true_residuals = [(true_value**2 + k*true_value + k*k - 1) % 3 for k in labels]
            self.assertEqual(true_residuals, [0, 0])
            if candidate != true_value:
                residuals = [(quadratic_value + k*candidate + k*k - 1) % 3 for k in labels]
                self.assertNotEqual(residuals[0], residuals[1])


if __name__ == '__main__':
    unittest.main()
