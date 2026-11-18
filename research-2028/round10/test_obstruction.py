"""Independent finite checks of the cardinality proposition in OBSTRUCTION.md."""

from collections import defaultdict, deque
from itertools import product
import unittest

from quadratic_compiler import Circuit, compile_nonconnectivity


def bits(value, width):
    """Return least-significant bit first, as used by the ripple-carry circuit."""
    return tuple((value >> i) & 1 for i in range(width))


def path_circuit(width):
    gates = []

    def gate(*definition):
        gates.append(definition)
        return 2 * width + len(gates) - 1

    def inv(wire):
        return gate("not", wire)

    def both(left, right):
        return gate("and", left, right)

    def either(left, right):
        return inv(both(inv(left), inv(right)))

    def xor(left, right):
        return both(either(left, right), inv(both(left, right)))

    one = either(0, inv(0))

    def successor(left, right):
        carry = one
        equal = one
        for old_bit, new_bit in zip(left, right):
            expected = xor(old_bit, carry)
            equal = both(equal, inv(xor(expected, new_bit)))
            carry = both(old_bit, carry)
        return both(equal, inv(carry))

    left = range(width)
    right = range(width, 2 * width)
    output = either(successor(left, right), successor(right, left))
    return Circuit(width, tuple(gates), output)


def trace(circuit, left, right):
    wires = list(left + right)
    for gate in circuit.gates:
        if gate[0] == "not":
            value = 1 - wires[gate[1]]
        else:
            value = wires[gate[1]] * wires[gate[2]]
        wires.append(value)
    return tuple(wires), wires[circuit.output]


def distances(edges, start):
    graph = defaultdict(set)
    for left, right in edges:
        graph[left].add(right)
        graph[right].add(left)
    pending = deque([start])
    length = {start: 0}
    while pending:
        vertex = pending.popleft()
        for neighbor in graph[vertex]:
            if neighbor not in length:
                length[neighbor] = length[vertex] + 1
                pending.append(neighbor)
    return length


class ObstructionTests(unittest.TestCase):
    def test_exact_sizes_and_deletions(self):
        for width in (2, 3, 4):
            with self.subTest(width=width):
                count = 2**width
                circuit = path_circuit(width)
                edges = set()
                for a, b in product(range(count), repeat=2):
                    _, adjacent = trace(circuit, bits(a, width), bits(b, width))
                    self.assertEqual(bool(adjacent), abs(a - b) == 1)
                    if a == b or adjacent:
                        edges.add((("A", a), ("B", b)))
                start, target = ("A", 0), ("B", count - 1)
                self.assertEqual(distances(edges, start)[target], count - 1)
                chain = [(("A", a), ("B", a + 1)) if a % 2 == 0
                         else (("A", a + 1), ("B", a)) for a in range(count - 1)]
                self.assertTrue(set(chain).issubset(edges))
                self.assertIn(target, distances(chain, start))
                for omitted in chain:
                    self.assertNotIn(target, distances(set(chain) - {omitted}, start))

    def test_two_bit_case_by_exhaustive_ternary_table_search(self):
        # Enumerate actual policies independently of the distance argument.
        # Nonbinary addresses never link, and only a binary endpoint is pinned.
        width = 2
        alphabet = tuple(product(range(3), repeat=width))
        id_for = {bits(v, width): v for v in range(4)}
        start, target = bits(0, width), bits(3, width)
        effects = set()
        for a, b in product(alphabet, repeat=2):
            i, j = id_for.get(a), id_for.get(b)
            for transcript_correct in (False, True):
                linked = i is not None and j is not None and (
                    i == j or (transcript_correct and abs(i - j) == 1)
                )
                effects.add((a == start, b == target, (i, j) if linked else None))

        policies = tuple(product(range(3), repeat=8))
        masks = {}
        for effect in effects:
            pin_a, pin_b, equality = effect
            feasible = 0
            for index, policy in enumerate(policies):
                if pin_a and policy[0] != 0:
                    continue
                if pin_b and policy[7] != 1:
                    continue
                if equality is None or policy[equality[0]] == policy[4 + equality[1]]:
                    feasible |= 1 << index
            masks[effect] = feasible

        self.assertTrue(all(first & second for first, second in product(masks.values(), repeat=2)))
        self.assertFalse(masks[(True, False, (0, 1))]
                         & masks[(False, False, (2, 1))]
                         & masks[(False, True, (2, 3))])

    def test_even_distance_equal_endpoints_and_disconnected(self):
        circuit = path_circuit(2)
        edges = []
        for a, b in product(range(4), repeat=2):
            _, adjacent = trace(circuit, bits(a, 2), bits(b, 2))
            if a == b or adjacent:
                edges.append((("A", a), ("B", b)))
        length = distances(edges, ("A", 0))
        self.assertEqual(length[("B", 2)], 3)
        self.assertEqual(length[("B", 0)], 1)
        edges = [(a, b) for a, b in edges if a[1] == b[1] or 3 not in (a[1], b[1])]
        self.assertNotIn(("B", 3), distances(edges, ("A", 0)))

    def test_projected_guards_against_compiled_polynomial_differences(self):
        width = 2
        circuit = path_circuit(width)
        start, target = bits(0, width), bits(3, width)
        instance = compile_nonconnectivity(circuit, start, target)
        zeros = (0,) * (1 + circuit.challenge_size)

        # Expected flags are pins A=0, B=1, and equality A=B, in that order.
        cases = []
        for a, b, flags in [
            (0, 1, (True, False, True)),
            (2, 1, (False, False, True)),
            (2, 3, (False, True, True)),
            (0, 3, (True, True, False)),
        ]:
            challenge, _ = trace(circuit, bits(a, width), bits(b, width))
            cases.append((challenge, flags))
        # A trit-2 gate transcript is invalid; edge vanishes while pins/diagonal survive.
        bad_trace = (2,) * len(circuit.gates)
        cases.extend([
            (start + bits(1, width) + bad_trace, (True, False, False)),
            (target + target + bad_trace, (False, True, True)),
            ((2, 0) + target + bad_trace, (False, True, False)),
            (start + (2, 0) + bad_trace, (True, False, False)),
        ])
        for challenge, (pin_left, pin_right, equality) in cases:
            for left, right in product(range(3), repeat=2):
                completion = instance.complete(challenge, left, right)
                before = instance.potential_values(zeros + completion)
                after = instance.potential_values((1,) + challenge + completion)
                expected = ((not pin_left or left == 0)
                            and (not pin_right or right == 1)
                            and (not equality or left == right))
                self.assertEqual(before == after, expected)


if __name__ == "__main__":
    unittest.main()
