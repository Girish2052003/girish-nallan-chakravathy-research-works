"""Independent fixtures: sampled coordinates never enter attacker arguments."""
from itertools import product
from collections import Counter
import math
import random
import unittest

from public_oracle_local_inversion import (
    recover_public_right_inverse, invert_target, project_to_target_fiber,
    sample_target_fiber,
)


def _rank(rows):
    a = [list(row) for row in rows]
    p = 0
    for c in range(len(a[0]) if a else 0):
        j = next((i for i in range(p, len(a)) if a[i][c]), None)
        if j is None:
            continue
        a[p], a[j] = a[j], a[p]
        inv = pow(a[p][c], -1, 3)
        a[p] = [(v * inv) % 3 for v in a[p]]
        for i in range(p + 1, len(a)):
            v = a[i][c]
            a[i] = [(x - v * y) % 3 for x, y in zip(a[i], a[p])]
        p += 1
        if p == len(a):
            break
    return p


def source_oracle(k, d, seed, constant_potential=False):
    """Create f(x) through evaluation; never materialize its 3^k table."""
    rng = random.Random(seed)
    r = k - d

    def matrix(n):
        while True:
            m = [[rng.randrange(3) for _ in range(n)] for _ in range(n)]
            if _rank(m) == n:
                return m

    a_matrix, b_matrix = matrix(r), matrix(k)
    direction = (0,) * d
    while not any(direction):
        direction = tuple(rng.randrange(3) for _ in range(d))
    q_table = {
        z: tuple(0 if constant_potential else rng.randrange(3) for _ in range(r))
        for z in product(range(3), repeat=d)
    }
    calls = [0]

    def evaluate(x):
        calls[0] += 1
        u = tuple(sum(a * b for a, b in zip(row, x)) % 3 for row in b_matrix)
        left, right = u[:r], u[r:]
        shifted = tuple((x + a) % 3 for x, a in zip(right, direction))
        linear = tuple(sum(a * b for a, b in zip(row, left)) % 3 for row in a_matrix)
        return tuple((v + qp - q) % 3 for v, qp, q in zip(linear, q_table[shifted], q_table[right]))

    return evaluate, calls


class OracleAttackTests(unittest.TestCase):
    def test_tiny_failure_budget_does_not_overflow(self):
        public_eval = lambda x: ((x[0] + x[1]) % 3,)
        basis = recover_public_right_inverse(public_eval, 2, 1, 1e-320, random.Random(710))
        self.assertIsNotNone(basis)
        self.assertLessEqual(basis["failure_bound"], 1e-320)
        self.assertEqual(public_eval(invert_target(public_eval, basis, (2,))), (2,))

    def test_all_source_profile_targets_without_public_truth_table(self):
        for k, d in ((5, 3), (7, 4), (9, 5)):
            for seed in (11, 29):
                with self.subTest(k=k, d=d, seed=seed):
                    public_eval, calls = source_oracle(k, d, seed)
                    basis = recover_public_right_inverse(public_eval, k, d, 1e-6, random.Random(seed + 700))
                    self.assertIsNotNone(basis, "Public-evaluation attack must recover an inverse")
                    self.assertEqual(_rank(basis["increments"]), k - d)
                    self.assertLessEqual(calls[0], basis["query_bound"])
                    self.assertLessEqual(basis["failure_bound"], 1e-6)
                    for target in product(range(3), repeat=k - d):
                        x = invert_target(public_eval, basis, target)
                        self.assertIsNotNone(x)
                        self.assertEqual(public_eval(x), target)
                    print("public oracle source fixture", k, d, seed,
                          "queries", calls[0], "budget", basis["query_bound"])

    def test_growing_dimension_without_exponential_full_table(self):
        k, d = 24, 3
        public_eval, calls = source_oracle(k, d, 41)
        basis = recover_public_right_inverse(public_eval, k, d, 1e-6, random.Random(701))
        self.assertIsNotNone(basis)
        self.assertLess(calls[0], 100000)
        rng = random.Random(81)
        for _ in range(20):
            target = tuple(rng.randrange(3) for _ in range(k - d))
            x = invert_target(public_eval, basis, target)
            self.assertIsNotNone(x)
            self.assertEqual(public_eval(x), target)
        print("succinct dimension fixture", k, d, "3^k", 3**k, "queries", calls[0])

    def test_constant_potential_extra_directions_do_not_prevent_inversion(self):
        public_eval, _ = source_oracle(7, 3, 31, constant_potential=True)
        basis = recover_public_right_inverse(public_eval, 7, 3, 1e-6, random.Random(709))
        self.assertIsNotNone(basis)
        for target in product(range(3), repeat=4):
            x = invert_target(public_eval, basis, target)
            self.assertEqual(public_eval(x), target)

    def test_target_verification_rejects_forged_nonconstant_shift(self):
        def public_eval(x):
            return ((x[0] * x[0]) % 3,)
        forged = {"k": 2, "r": 1, "f0": (0,),
                  "shifts": [(1, 0)], "increments": [(1,)]}
        self.assertIsNone(invert_target(public_eval, forged, (2,)))
        self.assertEqual(invert_target(public_eval, forged, (1,)), (1, 0))

    def test_wrong_model_inconclusive_does_not_claim_security(self):
        basis = recover_public_right_inverse(lambda x: (0,), 2, 1, 0.1, random.Random(733))
        self.assertIsNone(basis)

    def test_exhaustive_projection_has_equal_preimage_multiplicity(self):
        k, d = 4, 2
        for seed in (19, 43):
            public_eval, _ = source_oracle(k, d, seed)
            basis = recover_public_right_inverse(public_eval, k, d, 1e-6, random.Random(seed + 911))
            self.assertIsNotNone(basis)
            domain = list(product(range(3), repeat=k))
            for target in product(range(3), repeat=k - d):
                expected_fiber = {x for x in domain if public_eval(x) == target}
                counts = Counter(project_to_target_fiber(public_eval, basis, target, z)
                                 for z in domain)
                self.assertEqual(set(counts), expected_fiber)
                self.assertEqual(set(counts.values()), {3**(k - d)})
            print("uniform fiber exhaustive", k, d, seed,
                  "targets", 3**(k - d), "inputs", len(domain),
                  "multiplicity", 3**(k - d))

    def test_sampler_returns_verified_public_preimages(self):
        public_eval, _ = source_oracle(7, 4, 31)
        basis = recover_public_right_inverse(public_eval, 7, 4, 1e-6, random.Random(919))
        self.assertIsNotNone(basis)
        rng = random.Random(941)
        for target in product(range(3), repeat=3):
            for _ in range(3):
                x = sample_target_fiber(public_eval, basis, target, rng)
                self.assertIsNotNone(x)
                self.assertEqual(public_eval(x), target)

    def test_fiber_projection_verifies_result_with_forged_basis(self):
        def public_eval(x):
            return ((x[0] * x[0]) % 3,)
        forged = {"k": 2, "r": 1, "f0": (0,),
                  "shifts": [(1, 0)], "increments": [(1,)]}
        self.assertIsNone(project_to_target_fiber(public_eval, forged, (2,), (0, 0)))
        self.assertEqual(project_to_target_fiber(public_eval, forged, (1,), (0, 0)), (1, 0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
