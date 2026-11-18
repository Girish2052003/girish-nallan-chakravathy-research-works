"""Exact finite checks for the separated-input ternary syndrome bounds."""
from fractions import Fraction
from itertools import product
from math import comb
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round16"))
from matched_kem import research_profile


class CommunicationBounds(unittest.TestCase):
    # Every iid ternary 1 by 2 matrix and every signed vector of weight one.
    matrices = tuple(product(range(3), repeat=2))
    errors = ((1, 0), (2, 0), (0, 1), (0, 2))

    def syndrome_list(self, matrix):
        return [sum(x * y for x, y in zip(matrix, error)) % 3 for error in self.errors]

    def test_signed_second_moment(self):
        for first, second in product(range(-2, 3), repeat=2):
            f = (first, second, -first-second)
            conditional = [
                Fraction(sum(f[y] for y in self.syndrome_list(b)), 4)
                for b in self.matrices
            ]
            calculated = sum(value**2 for value in conditional) / 9
            expected = Fraction(sum(f[y]**2 + f[y]*f[-y % 3] for y in range(3)), 12)
            self.assertEqual(calculated, expected)

    def test_every_rectangle_in_tiny_example(self):
        n = len(self.matrices)
        w_count = len(self.errors)
        for subset in range(1 << 3):
            indicators = [int(bool(subset & (1 << y))) for y in range(3)]
            j_size = sum(indicators)
            row_hits = [sum(indicators[y] for y in self.syndrome_list(b))
                        for b in self.matrices]
            for matrix_subset in range(1 << n):
                rows = [i for i in range(n) if matrix_subset & (1 << i)]
                a_size = len(rows)
                hits = sum(row_hits[i] for i in rows)
                difference = 3 * hits - w_count * a_size * j_size
                self.assertLessEqual(difference**2, 2*w_count*a_size*(n-a_size)
                                     * j_size*(3-j_size))

    def test_noncommuting_one_qubit_messages(self):
        # The two entries are rational Bloch coordinates along X and Z.
        encoding = {b: ((1, 0) if b == (0, 0) else
                        (0, 1) if 0 in b else (-1, 0)) for b in self.matrices}
        mean = [Fraction(sum(v[j] for v in encoding.values()), 9) for j in range(2)]
        centered_energy = sum((v[j]-mean[j])**2 for v in encoding.values()
                              for j in range(2)) / 18
        conditional_energy = Fraction(0)
        for target in range(3):
            messages = [encoding[b] for b in self.matrices for y in self.syndrome_list(b)
                        if y == target]
            self.assertEqual(len(messages), 12)
            conditional = [Fraction(sum(v[j] for v in messages), len(messages))
                           for j in range(2)]
            conditional_energy += sum((conditional[j]-mean[j])**2 for j in range(2)) / 6
        self.assertGreater(conditional_energy, 0)
        self.assertLessEqual(conditional_energy, Fraction(2, 4) * centered_energy)
        self.assertLessEqual(centered_energy, Fraction(1, 2))

    def test_registered_communication_budgets(self):
        budgets = [(128, 12148, 11587, 11589), (192, 18871, 18310, 18312),
                   (256, 25786, 25225, 25227)]
        for target, floor_bits, classical_bits, qubits in budgets:
            profile = research_profile(target)
            w = profile.source.w
            count = comb(profile.common_columns, w) << w
            self.assertEqual(count.bit_length()-1, floor_bits)
            self.assertLessEqual(1 << (classical_bits+561), count)
            self.assertGreater(1 << (classical_bits+562), count)
            self.assertLessEqual(((1 << qubits)-1) << 559, count)
            self.assertGreater(((1 << (qubits+1))-1) << 559, count)


if __name__ == "__main__":
    unittest.main()
