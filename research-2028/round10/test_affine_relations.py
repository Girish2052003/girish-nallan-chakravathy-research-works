"""Independent finite checks for projected affine relations and propagation."""

import itertools
import random
import unittest

from affine_relations import FIELD, affine_network_witness, classify_relation


PLANE = tuple(itertools.product(FIELD, repeat=2))


def subsets():
    for mask in range(1 << len(PLANE)):
        yield frozenset(point for i, point in enumerate(PLANE) if mask & (1 << i))


def is_affine(points):
    """Check closure of a translated set under addition in F3²."""
    if not points:
        return True
    a, b = next(iter(points))
    differences = {((x - a) % 3, (y - b) % 3) for x, y in points}
    return all(
        ((x + u) % 3, (y + v) % 3) in differences
        for x, y in differences
        for u, v in differences
    )


def brute_force(left_size, right_size, constraints):
    for colors in itertools.product(FIELD, repeat=left_size + right_size):
        if all((colors[i], colors[left_size + j]) in pairs for i, j, pairs in constraints):
            return True
    return False


def line(scale, offset):
    return frozenset((x, (scale * x + offset) % 3) for x in FIELD)


class AffineRelationTests(unittest.TestCase):
    def assert_matches_brute_force(self, left_size, right_size, constraints):
        witness = affine_network_witness(left_size, right_size, iter(constraints))
        self.assertEqual(witness is not None, brute_force(left_size, right_size, constraints))
        if witness is not None:
            left, right = witness
            self.assertEqual((len(left), len(right)), (left_size, right_size))
            self.assertTrue(all(color in FIELD for color in left + right))
            self.assertTrue(all((left[i], right[j]) in pairs for i, j, pairs in constraints))

    def test_all_512_subsets_against_affine_closure(self):
        accepted = 0
        for points in subsets():
            if not is_affine(points):
                with self.assertRaises(ValueError):
                    classify_relation(iter(points))
                continue
            relation = classify_relation(iter(points))
            described = set()
            for x, y in PLANE:
                if not relation.feasible:
                    continue
                if relation.left_pin is not None and x != relation.left_pin:
                    continue
                if relation.right_pin is not None and y != relation.right_pin:
                    continue
                if relation.transport is not None:
                    a, b = relation.transport
                    if y != (a * x + b) % 3:
                        continue
                described.add((x, y))
            self.assertSetEqual(described, set(points))
            accepted += 1
        # Empty set, nine points, twelve lines, full plane.
        self.assertEqual(accepted, 23)

    def test_parallel_edge_constraints_exhaustively(self):
        relations = [points for points in subsets() if is_affine(points)]
        for first, second in itertools.product(relations, repeat=2):
            self.assert_matches_brute_force(1, 1, [(0, 0, first), (0, 0, second)])

    def test_all_transport_rectangles(self):
        bijections = [line(a, b) for a in (1, 2) for b in FIELD]
        for maps in itertools.product(bijections, repeat=4):
            constraints = [
                (0, 0, maps[0]), (0, 1, maps[1]),
                (1, 0, maps[2]), (1, 1, maps[3]),
            ]
            self.assert_matches_brute_force(2, 2, constraints)

    def test_cycle_without_fixed_point_and_cycle_with_one_fixed_point(self):
        common = [(0, 0, line(1, 0)), (0, 1, line(1, 0)), (1, 0, line(1, 0))]
        self.assertIsNone(affine_network_witness(2, 2, common + [(1, 1, line(1, 1))]))
        # x = -x+1 mod 3 forces x=2; root trials 0 and 1 both fail.
        self.assertEqual(affine_network_witness(2, 2, common + [(1, 1, line(2, 1))]),
                         ((2, 2), (2, 2)))

    def test_isolated_pins_empty_tables_and_invalid_inputs(self):
        left_two = {(2, y) for y in FIELD}
        right_one = {(x, 1) for x in FIELD}
        self.assertEqual(affine_network_witness(2, 2, [(1, 0, left_two), (0, 1, right_one)]),
                         ((0, 2), (0, 1)))
        self.assertEqual(affine_network_witness(0, 0, []), ((), ()))
        self.assertIsNone(affine_network_witness(1, 1, [(0, 0, set())]))
        with self.assertRaises(ValueError):
            affine_network_witness(1, 1, [(1, 0, PLANE)])
        with self.assertRaises(ValueError):
            affine_network_witness(-1, 0, [])
        with self.assertRaises(ValueError):
            classify_relation([(0, 3)])

    def test_seeded_mixed_networks(self):
        relations = [points for points in subsets() if is_affine(points)]
        rng = random.Random(3049)
        for _ in range(240):
            left_size, right_size = rng.randrange(1, 4), rng.randrange(1, 4)
            constraints = [
                (rng.randrange(left_size), rng.randrange(right_size), rng.choice(relations))
                for _ in range(rng.randrange(9))
            ]
            self.assert_matches_brute_force(left_size, right_size, constraints)


if __name__ == "__main__":
    unittest.main()
