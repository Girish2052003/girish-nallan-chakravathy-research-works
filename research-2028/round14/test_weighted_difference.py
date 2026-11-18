from itertools import product
import unittest

from weighted_difference import syndrome_circuit, compile_instance, decode_instance
from differential_bridge import lift_preimage, verify_witness


class WeightedDifferenceTests(unittest.TestCase):
    def test_all_fixed_weight_fibers(self):
        matrix = ((1, 2, 1), (2, 0, 1))
        circuit = syndrome_circuit(matrix)
        points = list(product(range(3), repeat=3))
        for weight in range(4):
            for y in product(range(3), repeat=2):
                potential, target = compile_instance(matrix, y, weight)
                self.assertEqual(decode_instance(potential, target), (matrix, y, weight))
                for e in points:
                    trace = circuit.trace(e)
                    point = (0,) * (len(target) + 1) + trace
                    expected = (tuple(sum(a*b for a,b in zip(row,e)) % 3 for row in matrix) == y
                                and sum(v != 0 for v in e) == weight)
                    self.assertEqual(verify_witness(potential, target, point), expected)
                    if expected:
                        self.assertEqual(lift_preimage(circuit, target, e), point)
                        self.assertEqual(point[1+len(target):1+len(target)+len(e)], e)

    def test_weight_three_is_distinct_from_zero(self):
        c = syndrome_circuit(((0, 0, 0),))
        self.assertEqual(c.evaluate((1, 2, 1)), (0, 1, 1))
        self.assertEqual(c.evaluate((0, 0, 0)), (0, 0, 0))

    def test_invalid_public_parameters(self):
        for args in [(((1,),), (3,), 1), (((1,),), (2,), 2), (((1,4),), (0,), 0)]:
            with self.assertRaises(ValueError):
                compile_instance(*args)
