"""Check actual before/after values against a separate graph specification."""

import unittest
from dataclasses import replace
from itertools import product

from quadratic_compiler import Circuit, compile_nonconnectivity


FIXTURES = (
    (Circuit(1, (("and", 0, 1),), 2), (0,), (1,)),  # only a loop
    (Circuit(1, (), 0), (0,), (1,)),  # reverse edge 1 -> 0
    (Circuit(1, (("not", 0), ("and", 2, 1)), 3), (0,), (1,)),  # 0 -> 1
    (Circuit(1, (("and", 0, 0),), 2), (1,), (1,)),  # identical anchors
)


def direct_wires(circuit, a, b):
    wires = list(a + b)
    for gate in circuit.gates:
        if gate[0] == "and":
            value = wires[gate[1]] & wires[gate[2]]
        else:
            value = int(not wires[gate[1]])
        wires.append(value)
    return tuple(wires)


def local_conditions(circuit, start, target, c, left, right):
    w = circuit.width
    a, b = c[:w], c[w:2*w]
    if a == start and left != 0 or b == target and right != 1:
        return False
    if 2 in a + b:
        return True
    wires = direct_wires(circuit, a, b)
    if a == b or (wires == c and wires[circuit.output]):
        return left == right
    return True


def collides(instance, challenge, responses):
    # Nonzero, varying base coordinates independently exercise cancellation.
    moving = tuple((i + sum(challenge)) % 3 for i in range(1 + len(challenge)))
    translated = tuple((x + h) % 3 for x, h in zip(moving, (1,) + challenge))
    return (instance.potential_values(moving + responses)
            == instance.potential_values(translated + responses))


def weakly_connected(edges, start, target):
    reached = {start}
    while True:
        new = {x for edge in edges if reached.intersection(edge) for x in edge}
        if new <= reached:
            return target in reached
        reached.update(new)


class QuadraticReductionTests(unittest.TestCase):
    def test_all_challenges_local_values_and_strategies(self):
        for circuit, start, target in FIXTURES:
            instance = compile_nonconnectivity(circuit, start, target)
            permitted = {ab: set(product(range(3), repeat=2))
                         for ab in product(range(3), repeat=2)}
            for c in product(range(3), repeat=circuit.challenge_size):
                for left, right in product(range(3), repeat=2):
                    responses = instance.complete(c, left, right)
                    passes = collides(instance, c, responses)
                    expected = local_conditions(circuit, start, target, c, left, right)
                    self.assertEqual(passes, expected, (circuit, c, left, right))
                    if not passes:
                        permitted[c[:2]].discard((left, right))

            edges = {(a, b) for a, b in product(range(2), repeat=2)
                     if direct_wires(circuit, (a,), (b,))[circuit.output]}
            found = False
            for entries in product(range(3), repeat=6):
                left, right = entries[:3], entries[3:]
                usable = all((left[a], right[b]) in pairs
                             for (a, b), pairs in permitted.items())
                expected = (left[start[0]] == 0 and right[target[0]] == 1
                            and all(left[x] == right[x] for x in (0, 1))
                            and all(left[a] == right[b] for a, b in edges))
                self.assertEqual(usable, expected)
                found |= usable
            self.assertEqual(found, not weakly_connected(edges, start[0], target[0]))

    def test_every_single_helper_change_breaks_a_collision(self):
        circuit, start, target = FIXTURES[0]
        instance = compile_nonconnectivity(circuit, start, target)
        c = (0, 1, 0)
        responses = list(instance.complete(c, 0, 1))
        self.assertTrue(collides(instance, c, tuple(responses)))
        for index in range(2, len(responses)):
            original = responses[index]
            for delta in (1, 2):
                responses[index] = (original + delta) % 3
                self.assertFalse(collides(instance, c, tuple(responses)))
            responses[index] = original

    def test_deleting_the_only_linear_monomial_gives_zero_response(self):
        for circuit, start, target in FIXTURES:
            instance = compile_nonconnectivity(circuit, start, target)
            linear = [term for row in instance.potentials for term in row
                      if len(term[1]) == 1]
            self.assertEqual(linear, [(2, (0,))])
            self.assertTrue(all(len(row) <= 5 for row in instance.potentials))
            stationary_start = 1 + circuit.challenge_size
            for row in instance.potentials:
                for _, factors in row:
                    if factors != (0,):
                        self.assertEqual(len(factors), 2)
                        self.assertLess(factors[0], stationary_start)
                        self.assertGreaterEqual(factors[1], stationary_start)
            homogeneous = replace(instance, potentials=tuple(
                tuple(term for term in row if len(term[1]) == 2)
                for row in instance.potentials
            ))
            zero = (0,) * (2 + len(instance.assignments))
            for c in product(range(3), repeat=circuit.challenge_size):
                self.assertTrue(collides(homogeneous, c, zero))

    def test_two_bit_addresses_valid_and_invalid_wires(self):
        circuit = Circuit(2, (("not", 0), ("and", 4, 3)), 5)
        start, target = (0, 0), (1, 1)
        instance = compile_nonconnectivity(circuit, start, target)
        samples = (
            (0, 1, 1, 1, 1, 1), (0, 1, 1, 1, 2, 1),
            (2, 1, 0, 1, 1, 1), (1, 0, 1, 0, 2, 2),
            (0, 0, 2, 2, 2, 2), (2, 2, 1, 1, 2, 2),
        )
        for c in samples:
            for left, right in product(range(3), repeat=2):
                expected = local_conditions(circuit, start, target, c, left, right)
                self.assertEqual(collides(instance, c, instance.complete(c, left, right)), expected)

    def test_rejects_malformed_inputs(self):
        for circuit_args in ((0, (), 0), (1, (), 2), (1, (("and", 0, 2),), 0)):
            with self.assertRaises(ValueError):
                Circuit(*circuit_args)
        circuit, start, target = FIXTURES[0]
        with self.assertRaises(ValueError):
            compile_nonconnectivity(circuit, (2,), target)
        instance = compile_nonconnectivity(circuit, start, target)
        with self.assertRaises(ValueError):
            instance.complete((0, 0, 3), 0, 1)
        with self.assertRaises(ValueError):
            instance.potential_values(())


if __name__ == "__main__":
    unittest.main()
