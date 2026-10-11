"""Independent behavioral checks, written before the proposed attacker.

These tests fail if valid public shift witnesses are missed, if a target outside
the shift image is falsely declared unsatisfiable, or if the global shift
space/rank disagrees with exhaustive public ground truth.
"""
from itertools import combinations, product
import random
import unittest

from public_global_shift_witness_recovery import PublicShiftSystem


def eval_global(factors, x):
    return tuple(c for scope, table in factors
                 for c in table[tuple(x[j] for j in scope)])


def brute_shift_statistics(n, factors):
    points = list(product(range(3), repeat=n))
    zero_value = eval_global(factors, (0,) * n)
    shifts = []
    increments = set()
    for h in points:
        delta = tuple((a - b) % 3 for a, b in
                      zip(eval_global(factors, h), zero_value))
        if all(tuple((a - b) % 3 for a, b in zip(
                eval_global(factors, tuple((u + v) % 3
                                          for u, v in zip(x, h))),
                eval_global(factors, x))) == delta for x in points):
            shifts.append(h)
            increments.add(delta)
    dim = lambda size: next(i for i in range(n + 1) if 3**i == size)
    return dim(len(shifts)), dim(len(increments))


def private_first_induced_width(n, factors, q):
    """Independent graph check of the explicitly provided elimination order."""
    graph = [set() for _ in range(n)]
    for scope, _ in factors:
        for i in scope:
            graph[i].update(set(scope) - {i})
    if any(j not in graph[i] for i in range(q) for j in range(i+1, q)):
        raise AssertionError("shared variables do not form the claimed clique")
    active = set(range(n))
    width = 0
    for v in tuple(range(q, n)) + tuple(range(q)):
        neighbors = graph[v] & active
        width = max(width, len(neighbors))
        for i in neighbors:
            graph[i].update(neighbors - {i})
        active.remove(v)
    return width


def source_private_left_fixture(q, d, r, seed):
    """Source-form restricted distribution; secrets stay inside generator.

    Every d-subset of the q shared right variables gets r private left
    variables. Each B is block upper triangular (not uniform in GL_k).
    A and both diagonal blocks are invertible upper triangular matrices.
    """
    rng = random.Random(seed)
    factors = []
    n = q

    def triangular(size):
        return [[(rng.randrange(1, 3) if i == j else rng.randrange(3))
                 if j >= i else 0 for j in range(size)]
                for i in range(size)]

    def mv(matrix, vector):
        return tuple(sum(a * b for a, b in zip(row, vector)) % 3
                     for row in matrix)

    for shared in combinations(range(q), d):
        private = tuple(range(n, n + r))
        n += r
        scope = private + shared
        A, left, right = triangular(r), triangular(r), triangular(d)
        mixing = [[rng.randrange(3) for _ in range(d)] for _ in range(r)]
        B = [left[i] + mixing[i] for i in range(r)]
        B += [[0] * r + right[i] for i in range(d)]
        direction = (1,) + tuple(rng.randrange(3) for _ in range(d - 1))
        potential = {z: tuple(rng.randrange(3) for _ in range(r))
                     for z in product(range(3), repeat=d)}
        table = {}
        for x in product(range(3), repeat=r + d):
            transformed = mv(B, x)
            u, z = transformed[:r], transformed[r:]
            za = tuple((a + b) % 3 for a, b in zip(z, direction))
            linear = mv(A, u)
            table[x] = tuple((linear[j] + potential[za][j]
                              - potential[z][j]) % 3 for j in range(r))
        # Deliberately reorder a complete table to prohibit zero-first reliance.
        table = dict(reversed(list(table.items())))
        factors.append((scope, table))
    return n, factors


class PublicGlobalShiftTests(unittest.TestCase):
    def test_every_target_recovered_with_shared_nonlinear_right_input(self):
        # Two source maps: x + Delta_(1,0)(z0^2*z1), sharing both z's.
        table = {(x, a, b): ((x + ((a + 1)**2 - a*a)*b) % 3,)
                 for x, a, b in product(range(3), repeat=3)}
        factors = [((0, 2, 3), table), ((1, 2, 3), dict(reversed(list(table.items()))))]
        attack = PublicShiftSystem(4, factors)
        self.assertEqual(attack.increment_rank, 2)
        self.assertEqual(attack.output_dimension, 2)
        for target in product(range(3), repeat=2):
            result = attack.solve([(target[0],), (target[1],)])
            self.assertEqual(result.status, "recovered")
            self.assertEqual(eval_global(factors, result.witness), target)

    def test_rank_deficient_target_is_inconclusive_even_when_satisfiable(self):
        square = {(x,): (x*x % 3,) for x in range(3)}
        factors = [((0,), square)]
        attack = PublicShiftSystem(1, factors)
        self.assertEqual(attack.increment_rank, 0)
        result = attack.solve([(1,)])
        self.assertEqual(result.status, "inconclusive")
        self.assertIsNone(result.witness)
        self.assertTrue(any(eval_global(factors, (x,)) == (1,) for x in range(3)))

    def test_rank_deficient_map_still_recovers_target_in_its_image(self):
        square = {(x,): (x*x % 3,) for x in range(3)}
        result = PublicShiftSystem(1, [((0,), square)]).solve([(0,)])
        self.assertEqual(result.status, "recovered")
        self.assertEqual(result.witness, (0,))

    def test_source_form_overlap_can_have_no_useful_global_shift(self):
        # Both are source-form local maps: x+y*z and y+x*z.
        # For g(y,z)=y*z use Q(y,z)=(2*y*y+y)*z and direction (1,0).
        # Their constant-shift lines are different, so the global intersection
        # is zero even though each map separately has a public right inverse.
        first = {(x, y, z): ((x+y*z) % 3,)
                 for x, y, z in product(range(3), repeat=3)}
        second = {(x, y, z): ((y+x*z) % 3,)
                  for x, y, z in product(range(3), repeat=3)}
        factors = [((0, 1, 2), first), ((0, 1, 2), second)]
        attack = PublicShiftSystem(3, factors)
        self.assertEqual((attack.shift_dimension, attack.increment_rank), (0, 0))
        result = attack.solve([(1,), (1,)])
        self.assertEqual(result.status, "inconclusive")
        self.assertEqual(eval_global(factors, (1, 1, 0)), (1, 1))

    def test_random_small_maps_match_exhaustive_global_shift_statistics(self):
        rng = random.Random(9182)
        for n in (1, 2, 3, 4):
            for _ in range(8):
                factors = []
                for _ in range(2):
                    scope = tuple(rng.sample(range(n), min(n, 2)))
                    table = {x: (rng.randrange(3),)
                             for x in product(range(3), repeat=len(scope))}
                    factors.append((scope, table))
                attack = PublicShiftSystem(n, factors)
                self.assertEqual((attack.shift_dimension, attack.increment_rank),
                                 brute_shift_statistics(n, factors))
                all_points = list(product(range(3), repeat=n))
                for target in product(range(3), repeat=2):
                    result = attack.solve([(target[0],), (target[1],)])
                    if result.witness is not None:
                        self.assertEqual(eval_global(factors, result.witness), target)
                    if not any(eval_global(factors, x) == target for x in all_points):
                        self.assertEqual(result.status, "inconclusive")

    def test_high_primal_width_fixed_local_geometry_is_publicly_invertible(self):
        for q in (4, 8, 12):
            n, factors = source_private_left_fixture(q, d=2, r=1, seed=9100+q)
            attack = PublicShiftSystem(n, factors)
            self.assertEqual(private_first_induced_width(n, factors, q), q-1)
            self.assertEqual(attack.increment_rank, len(factors))
            for seed in (1, 2, 3):
                rng = random.Random(seed)
                targets = [(rng.randrange(3),) for _ in factors]
                result = attack.solve(targets)
                self.assertEqual(result.status, "recovered")
                self.assertEqual(eval_global(factors, result.witness),
                                 tuple(t[0] for t in targets))
            print("global-shift high-width fixture", "q", q, "n", n,
                  "m", len(factors), "primal_width", q-1,
                  "increment_rank", attack.increment_rank)

    def test_original_r1_local_geometry_in_high_width_family(self):
        n, factors = source_private_left_fixture(q=7, d=3, r=2, seed=9128)
        attack = PublicShiftSystem(n, factors)
        self.assertEqual(private_first_induced_width(n, factors, 7), 6)
        self.assertEqual(attack.increment_rank, 2 * len(factors))
        targets = [(i % 3, (i+1) % 3) for i in range(len(factors))]
        result = attack.solve(targets)
        self.assertEqual(result.status, "recovered")
        self.assertEqual(eval_global(factors, result.witness),
                         tuple(x for target in targets for x in target))

    def test_empty_system_and_nonzero_constant_offsets(self):
        result = PublicShiftSystem(3, []).solve([])
        self.assertEqual(result.status, "recovered")
        self.assertEqual(result.witness, (0, 0, 0))
        table = {(x,): ((2*x+1) % 3,) for x in range(3)}
        attack = PublicShiftSystem(1, [((0,), table)])
        for target in range(3):
            result = attack.solve([(target,)])
            self.assertEqual(result.status, "recovered")
            self.assertEqual(table[result.witness], (target,))

    def test_zero_dimensions_and_zero_arity_constants(self):
        empty = PublicShiftSystem(0, [])
        self.assertEqual(empty.solve([]).witness, ())
        constant = PublicShiftSystem(0, [((), {(): (2,)})])
        self.assertEqual((constant.shift_dimension, constant.increment_rank), (0, 0))
        self.assertEqual(constant.solve([(2,)]).witness, ())
        self.assertEqual(constant.solve([(1,)]).status, "inconclusive")
        no_output = PublicShiftSystem(1, [((0,), {(x,): () for x in range(3)})])
        self.assertEqual((no_output.shift_dimension, no_output.increment_rank), (1, 0))
        self.assertEqual(no_output.solve([()]).witness, (0,))

    def test_incomplete_or_malformed_public_inputs_are_rejected(self):
        valid = {(x,): (x,) for x in range(3)}
        invalid_factors = [
            [((0,), {(0,): (0,), (1,): (1,)})],
            [((0,), {(0,): (0,), (1,): (1,), (3,): (2,)})],
            [((0,), {(0,): (0,), (1,): (1, 2), (2,): (2,)})],
            [((0,), {(0,): (0,), (1,): (1,), (2,): (3,)})],
            [((0, 0), valid)],
            [((1,), valid)],
            [((-1,), valid)],
            [((), {})],
        ]
        for factors in invalid_factors:
            with self.subTest(factors=factors):
                with self.assertRaises(ValueError):
                    PublicShiftSystem(1, factors)
        with self.assertRaises(ValueError):
            PublicShiftSystem(-1, [])

    def test_malformed_target_shapes_and_values_are_rejected(self):
        attack = PublicShiftSystem(1, [((0,), {(x,): (x,) for x in range(3)})])
        for targets in ([], [(0,), (0,)], [()], [(0, 1)], [(3,)]):
            with self.subTest(targets=targets):
                with self.assertRaises(ValueError):
                    attack.solve(targets)


if __name__ == "__main__":
    unittest.main(verbosity=2)
