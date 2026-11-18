from itertools import product
import unittest
from unittest.mock import patch

from challenge import compile_instance, sample_public
from weighted_difference import decode_instance, syndrome_circuit
from differential_bridge import lift_preimage, verify_witness


class NativeChallengeTests(unittest.TestCase):
    def test_sample_and_both_representations(self):
        # For this tiny fixture the verifier can enumerate every possible response.
        matrix, syndrome, weight = sample_public(2, 4, 2)
        potential, target = compile_instance(matrix, syndrome, weight)
        self.assertEqual(decode_instance(potential, target), (matrix, syndrome, weight))
        circuit = syndrome_circuit(matrix)
        matching = []
        for e in product(range(3), repeat=4):
            actual = tuple(sum(x*y for x, y in zip(row, e)) % 3 for row in matrix)
            if sum(v != 0 for v in e) == weight and actual == syndrome:
                matching.append(e)
                self.assertTrue(verify_witness(potential, target, lift_preimage(circuit, target, e)))
        self.assertTrue(matching)

    def test_documented_example_and_sampler_order(self):
        matrix = ((1, 0, 1, 2), (0, 1, 2, 1))
        with patch('challenge.secrets.SystemRandom') as rng, patch(
                'challenge.secrets.randbelow', side_effect=[0, 1, *matrix[0], *matrix[1]]):
            rng.return_value.sample.return_value = [0, 2]
            self.assertEqual(sample_public(2, 4, 2), (matrix, (0, 1), 2))
        with self.assertRaises(ValueError):
            sample_public(4, 2, 1)


class UniqueWitnessBounds(unittest.TestCase):
    def test_counts_at_registered_matched_dimensions(self):
        from math import comb
        from matched_kem import research_profile
        for target, expected in (
            (128, (12149, 8650276, 8662424)),
            (192, (18872, 19151326, 19170197)),
            (256, (25787, 33828555, 33854341)),
        ):
            layout = research_profile(target)
            weight = layout.source.w
            bits = (comb(layout.common_columns, weight) << weight).bit_length()
            floor = 19 * layout.common_rows // 12
            self.assertEqual((bits, floor + 1 - 2*bits, floor - bits), expected)
        self.assertGreater(3**12, 2**19)
