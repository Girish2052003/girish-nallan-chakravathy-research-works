"""Independent finite checks for the Round-9 reductions, not security proofs."""
import itertools
import random
import unittest
from collections import Counter
from math import prod

try:
    import differential_challenges as dc
except ModuleNotFoundError as exc:
    if exc.name != "differential_challenges":
        raise
    dc = None


COUNTS = Counter()


def points(n):
    return itertools.product(range(3), repeat=n)


def raw_value(poly, point):
    """Direct monomial arithmetic independent of the implementation evaluator."""
    return sum(coefficient * prod(point[i] for i in monomial)
               for monomial, coefficient in poly.terms) % 3


def raw_collisions(problem, challenge):
    h = (1,) + tuple(challenge) + (0,) * problem.n_responses
    found = []
    for w in points(problem.n_variables):
        shifted = tuple((a + b) % 3 for a, b in zip(w, h))
        if all(raw_value(p, shifted) == raw_value(p, w)
               for p in problem.outputs):
            found.append(w)
    return found


def monomials(n, degree):
    return [m for d in range(degree + 1)
            for m in itertools.combinations_with_replacement(range(n), d)
            if all(m.count(i) <= 2 for i in set(m))]


def random_problem(rng, challenges, responses, outputs, degree):
    n = 1 + challenges + responses
    return dc.Problem(challenges, responses, tuple(
        dc.Poly({term: rng.randrange(3) for term in monomials(n, degree)})
        for _ in range(outputs)))


def cnf_true(bits, clauses):
    return all(any(bool(bits[abs(literal) - 1]) == (literal > 0)
                   for literal in clause) for clause in clauses)


class DifferentialChallengesTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(dc, "Round-9 implementation has not been created")

    def test_pin_polynomial_has_exact_ternary_difference(self):
        s = dc.Poly.variable(0)
        pin = 2 * s * (s - 1)
        self.assertEqual([pin.evaluate((v,)) for v in range(3)], [0, 0, 1])
        p = dc.Problem(0, 0, (pin,))
        self.assertEqual([p.difference((v,), ()) for v in range(3)],
                         [(0,), (1,), (2,)])

    def test_reduced_polynomial_arithmetic_preserves_field_function(self):
        x, y = dc.Poly.variable(0), dc.Poly.variable(1)
        self.assertEqual((x * x * x).terms, x.terms)
        p = (x + y + 2) * (x - y)
        for a, b in points(2):
            self.assertEqual(p.evaluate((a, b)), ((a + b + 2) * (a - b)) % 3)
        self.assertEqual((3 * p).terms, ())
        self.assertEqual((p - p).terms, ())

    def test_one_shot_monomial_input_is_not_consumed_during_validation(self):
        p = dc.Poly({iter((1, 1)): 1})
        self.assertEqual(p.evaluate((0, 0)), 0)
        self.assertEqual(p.evaluate((0, 2)), 1)

    def test_one_shot_challenge_can_be_reused_for_all_affine_probes(self):
        x = dc.Poly.variable(1)
        p = dc.Problem(1, 0, (x * x,))
        try:
            witness = dc.solve_quadratic_challenge(p, iter((1,)))
        except ValueError as exc:
            self.fail(f"A valid one-shot challenge was consumed too early: {exc}")
        self.assertEqual(witness, (0, 1))

    def test_public_encoding_uses_integers_even_for_python_boolean_inputs(self):
        p = dc.Problem(True, False, (dc.Poly.variable(True),))
        encoding = p.public_encoding()
        self.assertIs(type(encoding["challenge_coordinates"]), int)
        self.assertIs(type(encoding["response_coordinates"]), int)
        self.assertIs(type(encoding["outputs"][0][0][0][0]), int)
        self.assertIs(type(p.direction((True,))[1]), int)
        circuit = dc.BooleanCircuit(True, False, (("const", True),), True)
        self.assertIs(type(circuit.evaluate((False,), ())), int)

    def test_bad_dimensions_and_out_of_domain_coordinates_are_rejected(self):
        with self.assertRaises(ValueError):
            dc.Problem(-1, 0, ())
        with self.assertRaises(ValueError):
            dc.Problem(0, 0, (dc.Poly.variable(1),))
        with self.assertRaises(ValueError):
            dc.Poly.variable(-1)
        p = dc.Problem(1, 0, ())
        for challenge in [(), (3,), (-1,), (0, 1)]:
            with self.assertRaises(ValueError):
                p.direction(challenge)
        with self.assertRaises(ValueError):
            p.difference((0,), (0,))

    def test_affine_coverage_matches_all_scalar_affine_maps(self):
        terms = monomials(3, 1)
        for coefficients in points(len(terms)):
            p = dc.Problem(1, 1, (dc.Poly(dict(zip(terms, coefficients))),))
            expected = all(raw_collisions(p, c) for c in points(1))
            self.assertEqual(dc.linear_coverage(p), expected)
            COUNTS["scalar_affine_maps_exhausted"] += 1
        self.assertTrue(dc.linear_coverage(dc.Problem(0, 0, (dc.Poly({(): 2}),))))

    def test_gaussian_solver_handles_nonunit_pivots_and_inconsistency(self):
        self.assertEqual(dc.solve_linear([(2, 1), (1, 2)], [1, 2], 2), (2, 0))
        self.assertIsNone(dc.solve_linear([(2, 1), (1, 2)], [1, 1], 2))
        self.assertEqual(dc.solve_linear([], [], 3), (0, 0, 0))
        self.assertEqual(dc.solve_linear([()], [0], 0), ())
        self.assertIsNone(dc.solve_linear([()], [1], 0))
        with self.assertRaises(ValueError):
            dc.solve_linear([(1,)], [0], 2)

    def test_all_729_scalar_quadratic_maps_against_exhaustive_search(self):
        terms = monomials(2, 2)
        self.assertEqual(len(terms), 6)
        for coefficients in points(len(terms)):
            p = dc.Problem(1, 0, (dc.Poly(dict(zip(terms, coefficients))),))
            covered = True
            for c in points(1):
                actual = dc.solve_quadratic_challenge(p, c)
                expected = raw_collisions(p, c)
                self.assertEqual(actual is not None, bool(expected))
                if actual is not None:
                    self.assertIn(actual, expected)
                covered = covered and bool(expected)
                COUNTS["scalar_quadratic_challenges_checked"] += 1
            cert = dc.quadratic_no_certificate(p)
            self.assertEqual(cert is None, covered)
            if cert is not None:
                self.assertTrue(dc.check_quadratic_certificate(p, cert))
                self.assertFalse(raw_collisions(p, cert["challenge"]))
            COUNTS["scalar_quadratic_maps_exhausted"] += 1

    def test_seeded_vector_quadratics_dual_and_primal_match_ground_truth(self):
        rng = random.Random(20261118)
        for _ in range(36):
            r, t, m = rng.choice([(1, 1, 2), (2, 0, 2), (0, 2, 3)])
            p = random_problem(rng, r, t, m, 2)
            expected = all(raw_collisions(p, c) for c in points(r))
            for strategy in ("challenges", "outputs", "auto"):
                self.assertEqual(dc.quadratic_coverage(p, strategy), expected)
            cert = dc.quadratic_no_certificate(p)
            if cert is not None:
                self.assertTrue(dc.check_quadratic_certificate(p, cert))
                self.assertFalse(raw_collisions(p, cert["challenge"]))
            COUNTS["vector_quadratic_maps_checked"] += 1

    def test_homogeneous_quadratic_maps_have_public_midpoint_witness(self):
        rng = random.Random(602)
        for _ in range(12):
            terms = [()] + list(itertools.combinations_with_replacement(range(5), 2))
            p = dc.Problem(2, 2, tuple(dc.Poly({term: rng.randrange(3)
                                               for term in terms}) for _ in range(3)))
            for c in points(2):
                self.assertTrue(p.is_collision(p.direction(c), c))
                COUNTS["homogeneous_midpoint_witnesses_checked"] += 1
            self.assertIsNone(dc.quadratic_no_certificate(p))

    def test_dual_certificate_rejects_wrong_challenge_and_multiplier(self):
        s, x, y = [dc.Poly.variable(i) for i in range(3)]
        p = dc.Problem(1, 1, (x * y, s))
        cert = dc.quadratic_no_certificate(p)
        self.assertIsNotNone(cert)
        self.assertTrue(dc.check_quadratic_certificate(p, cert))
        for bad in [None, {}, {"challenge": (), "multiplier": (0, 1)},
                    {"challenge": (0,), "multiplier": (0, 0)},
                    {"challenge": (0,), "multiplier": (0, 2)},
                    {"challenge": (3,), "multiplier": (0, 1)}]:
            self.assertFalse(dc.check_quadratic_certificate(p, bad))

    def test_empty_outputs_and_no_challenge_coordinates_are_well_defined(self):
        empty = dc.Problem(2, 0, ())
        self.assertTrue(dc.quadratic_coverage(empty))
        self.assertIsNone(dc.quadratic_no_certificate(empty))
        no = dc.Problem(0, 0, (dc.Poly.variable(0),))
        self.assertFalse(dc.quadratic_coverage(no))
        self.assertTrue(dc.check_quadratic_certificate(no, dc.quadratic_no_certificate(no)))

    def test_algorithms_do_not_silently_treat_cubics_as_quadratics(self):
        s, x = dc.Poly.variable(0), dc.Poly.variable(1)
        p = dc.Problem(1, 0, (s * s * x,))
        for call in [lambda: dc.linear_coverage(p),
                     lambda: dc.solve_quadratic_challenge(p, (0,)),
                     lambda: dc.quadratic_no_certificate(p)]:
            with self.assertRaises(ValueError):
                call()

    def test_quadratic_unsat_reduction_matches_boolean_truth(self):
        rng = random.Random(903)
        fixtures = [((1, 1, 1),), ((1, 1, 1), (-1, -1, -1)),
                    ((1, -1, 2),), (), ((1, 2, 2), (-1, -2, -2))]
        fixtures += [tuple(tuple(rng.choice((-2, -1, 1, 2)) for _ in range(3))
                           for _ in range(rng.randrange(1, 5))) for _ in range(15)]
        for clauses in fixtures:
            p = dc.quadratic_unsat_problem(2, clauses)
            self.assertLessEqual(p.degree, 2)
            self.assertEqual(len(p.outputs), 9 * len(clauses) + 1)
            self.assertEqual(p.n_responses, 10 * len(clauses))
            for c in points(2):
                bits = tuple(a * a % 3 for a in c)
                found = dc.solve_quadratic_challenge(p, c)
                self.assertEqual(found is not None, not cnf_true(bits, clauses))
                if found is not None:
                    self.assertTrue(p.is_collision(found, c))
                COUNTS["unsat_reduction_challenges_checked"] += 1
            expected = not any(cnf_true(bits, clauses)
                               for bits in itertools.product((0, 1), repeat=2))
            self.assertEqual(dc.quadratic_coverage(p, "challenges"), expected)
            COUNTS["cnf_instances_checked"] += 1
        self.assertFalse(dc.quadratic_coverage(dc.quadratic_unsat_problem(0, ())))

    def test_unsat_reduction_rejects_malformed_clauses(self):
        for clauses in [((1, 1),), ((0, 1, 1),), ((2, 1, 1),)]:
            with self.assertRaises(ValueError):
                dc.quadratic_unsat_problem(1, clauses)

    def test_boolean_gate_evaluator_uses_boolean_not_ternary_arithmetic(self):
        for operation, wanted in [("and", [0, 0, 0, 1]),
                                  ("or", [0, 1, 1, 1]),
                                  ("xor", [0, 1, 1, 0])]:
            circuit = dc.BooleanCircuit(1, 1, ((operation, 0, 1),), 2)
            self.assertEqual([circuit.evaluate((a,), (b,))
                              for a, b in itertools.product((0, 1), repeat=2)], wanted)
        circuit = dc.BooleanCircuit(1, 0, (("not", 0),), 1)
        self.assertEqual([circuit.evaluate((a,), ()) for a in (0, 1)], [1, 0])

    def test_cubic_circuit_reduction_has_exact_fiber_bijection(self):
        circuits = [dc.BooleanCircuit(1, 1, ((op, 0, 1),), 2)
                    for op in ("and", "or", "xor")]
        circuits += [dc.BooleanCircuit(1, 1, (("xor", 0, 1), ("not", 2)), 3),
                     dc.BooleanCircuit(1, 1, (), 1),
                     dc.BooleanCircuit(1, 0, (), 0),
                     dc.BooleanCircuit(0, 0, (("const", 1),), 0),
                     dc.BooleanCircuit(0, 0, (("const", 0),), 0)]
        truth_tables = [[0, 0, 0, 1], [0, 1, 1, 1], [0, 1, 1, 0],
                        [1, 0, 0, 1], [0, 1, 0, 1], [0, 1], [1], [0]]
        for circuit, table in zip(circuits, truth_tables):
            p = dc.cubic_circuit_problem(circuit)
            self.assertLessEqual(p.degree, 3)
            for c in points(circuit.n_universal):
                u = tuple(a * a % 3 for a in c)
                expected = set()
                for v in itertools.product((0, 1), repeat=circuit.n_existential):
                    index = sum(bit << (len(u + v) - 1 - i)
                                for i, bit in enumerate(u + v))
                    if table[index]:
                        expected.add(dc.lift_circuit_witness(circuit, c, v))
                    else:
                        with self.assertRaises(ValueError):
                            dc.lift_circuit_witness(circuit, c, v)
                actual = set(raw_collisions(p, c))
                self.assertEqual(actual, expected)
                for w in actual:
                    self.assertEqual(w[:1 + circuit.n_universal],
                                     (0,) * (1 + circuit.n_universal))
                COUNTS["cubic_fibers_exhausted"] += 1
                COUNTS["cubic_points_enumerated"] += 3 ** p.n_variables
            COUNTS["cubic_circuit_instances_checked"] += 1

    def test_response_may_depend_on_challenge_and_order_cannot_be_swapped(self):
        equal = dc.BooleanCircuit(1, 1, (("xor", 0, 1), ("not", 2)), 3)
        p = dc.cubic_circuit_problem(equal)
        response_sets = []
        for c in points(1):
            witnesses = raw_collisions(p, c)
            self.assertEqual(len(witnesses), 1)
            response_sets.append({w[2] for w in witnesses})
        self.assertEqual(response_sets, [{0}, {1}, {1}])
        self.assertFalse(set.intersection(*response_sets))

    def test_literal_ternary_cubic_example_and_fixed_direction_np_slice(self):
        and_circuit = dc.BooleanCircuit(1, 1, (("and", 0, 1),), 2)
        p = dc.cubic_circuit_problem(and_circuit)
        self.assertTrue(p.is_collision((0, 0, 1, 1, 1), (2,)))
        self.assertEqual(dc.lift_circuit_witness(and_circuit, (2,), (1,)),
                         (0, 0, 1, 1, 1))
        # The challenge is present but ignored: this reduces ordinary SAT.
        positive = dc.BooleanCircuit(1, 1, (), 1)
        contradiction = dc.BooleanCircuit(1, 1, (("not", 1), ("and", 1, 2)), 3)
        self.assertTrue(raw_collisions(dc.cubic_circuit_problem(positive), (0,)))
        self.assertFalse(raw_collisions(dc.cubic_circuit_problem(contradiction), (0,)))

    def test_circuit_validation_rejects_cycles_and_nonboolean_inputs(self):
        for gates, output in [((("not", 1),), 1), ((("unknown", 0),), 1),
                              ((("and", 0),), 1), ((("const", 2),), 1),
                              ((), 1)]:
            with self.assertRaises(ValueError):
                dc.BooleanCircuit(1, 0, gates, output)
        circuit = dc.BooleanCircuit(1, 1, (), 1)
        with self.assertRaises(ValueError):
            circuit.evaluate((2,), (1,))
        with self.assertRaises(ValueError):
            dc.lift_circuit_witness(circuit, (0,), (2,))


if __name__ == "__main__":
    unittest.main(verbosity=2)
