"""Finite counting checks for the promised worst-case reduction."""
from collections import Counter
from itertools import permutations, product
import unittest


def field9_power_five(x):
    # Coordinates a+b*t with t^2=-1.  x^5=x*Norm(x) over F9.
    a, b = divmod(x, 3)
    norm = (a*a + b*b) % 3
    return 3*((a*norm) % 3) + (b*norm) % 3


def affine_plane_group():
    points = tuple(product(range(3), repeat=2))
    for a, b, c, d in product(range(3), repeat=4):
        if (a*d - b*c) % 3:
            for u, v in points:
                yield tuple(3*((a*x + b*y + u) % 3) + (c*x + d*y + v) % 3
                            for x, y in points)


def compare_distributions(central, masks):
    # For each public presentation, count its image at one regular point,
    # and at all regular points. A pointwise comparison checks the joint law.
    result_fixed, result_uniform = Counter(), Counter()
    for inner in masks:
        masked = tuple(central[x] for x in inner)
        for outer in masks:
            public = bytes(outer[z] for z in masked)
            result_fixed[public, outer[1]] += 1
            for y in outer[1:]:
                result_uniform[public, y] += 1
    return {key: value*(len(central)-1) for key, value in result_fixed.items()} == result_uniform


class OrbitLawTests(unittest.TestCase):
    def test_regular_pairs_in_a_nonlinear_field_example(self):
        masks = tuple(affine_plane_group())
        self.assertEqual(len(set(masks)), 432)
        central = tuple(map(field9_power_five, range(9)))
        self.assertEqual(len(set(central)), 9)
        self.assertNotIn(central, masks)
        self.assertTrue(compare_distributions(central, masks))

    def test_ambiguous_center_in_presentations(self):
        # Even the identity can be represented with any of the three centers.
        ident = (0, 1, 2)
        masks = tuple(permutations(ident))
        centers = {outer[0] for inner in masks for outer in masks
                   if tuple(outer[t] for t in inner) == ident}
        self.assertEqual(centers, set(ident))
        self.assertTrue(compare_distributions(ident, masks))
