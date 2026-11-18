"""Finite checks of planted complete policies and their exact label symmetry."""

from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import sys
import unittest

from planted_policy import PlantedPolicy, adjacency_gate_list, generate_policy, graph_from_coins
from research_kem import pack, unpack

# In the repository the unmodified Round 10 compiler is a sibling directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round10"))
from cubic_compiler import compile_three_colouring
from quadratic_compiler import Circuit


def circuit_trace(circuit, inputs):
    wires = list(inputs)
    for operation, a, *rest in circuit.gates:
        wires.append(1 - wires[a] if operation == "not" else wires[a] * wires[rest[0]])
    return tuple(wires[len(inputs):]), wires[circuit.output]


class PlantedPolicyTests(unittest.TestCase):
    def test_exact_posterior_for_every_supported_graph(self):
        for n in (1, 2, 3):
            weights = defaultdict(Counter)
            posterior = defaultdict(Counter)
            for colors in product(range(3), repeat=n):
                for bits in range(1 << (n * (n - 1) // 2)):
                    graph = graph_from_coins(colors, bits)
                    weights[graph][colors] += 1
                    for vertex, label in enumerate(colors):
                        posterior[graph, vertex][label] += 1
            self.assertEqual(len(weights), 1 << (n * (n - 1) // 2))
            for (graph, vertex), counts in posterior.items():
                total = sum(weights[graph].values())
                self.assertEqual([3 * counts[t] for t in range(3)], [total] * 3)
                self.assertIn(vertex, range(n))
            if n == 3:
                triangle = bytes([7])
                self.assertEqual(len(weights[triangle]), 6)

    def test_canonical_graph_and_circuit(self):
        n = 3
        for bits in range(8):
            public = bytes([bits])
            circuit = Circuit(*adjacency_gate_list(n, public))
            for i in range(4):
                for j in range(4):
                    inputs = (i // 2, i % 2, j // 2, j % 2)
                    _, edge = circuit_trace(circuit, inputs)
                    pairs = tuple(combinations(range(n), 2))
                    expected = any(set(pair) == {i, j} and bits & (1 << k)
                                   for k, pair in enumerate(pairs))
                    self.assertEqual(edge, int(expected))
        for malformed in (b"", b"\x08", b"\x01\x00"):
            with self.assertRaises(ValueError):
                adjacency_gate_list(n, malformed)

    def test_private_table_answers_actual_compiled_polynomial(self):
        for colors, coins in (((0, 0, 0), 7), ((0, 1, 1), 3), ((2, 0, 1), 7)):
            public = graph_from_coins(colors, coins)
            policy = PlantedPolicy(3, pack(colors))
            circuit = Circuit(*adjacency_gate_list(3, public))
            instance = compile_three_colouring(circuit)
            # All pairs of ternary addresses, including invalid binary encodings.
            for a, b in product(product(range(3), repeat=2), repeat=2):
                inputs = a + b
                # Invalid addresses disable the edge guard even on an all-zero trace.
                if 2 in inputs:
                    trace = (0,) * len(circuit.gates)
                else:
                    trace, _ = circuit_trace(circuit, inputs)
                for w in (trace, (2,) * len(trace)):
                    challenge = inputs + w
                    responses = instance.complete(challenge, policy.answer(a), policy.answer(b))
                    moving = (1,) * (1 + len(challenge))
                    after = tuple((u + h) % 3 for u, h in zip(moving, (1,) + challenge))
                    self.assertEqual(instance.potential_values(moving + responses),
                                     instance.potential_values(after + responses))
            if public == bytes([7]):
                inputs = (0, 0, 0, 1)
                trace, _ = circuit_trace(circuit, inputs)
                challenge = inputs + trace
                bad = instance.complete(challenge, 2, 2)
                zero = (0,) * (1 + len(challenge))
                self.assertNotEqual(instance.potential_values(zero + bad),
                                    instance.potential_values((1,) + challenge + bad))

    def test_sampling_and_private_encoding(self):
        for vertices in (1, 3, 9):
            public, private = generate_policy(vertices)
            colors = unpack(private, vertices)
            self.assertEqual(len(public), (vertices * (vertices - 1) // 2 + 7) // 8)
            mask = int.from_bytes(public, "little")
            for i, (u, v) in enumerate(combinations(range(vertices), 2)):
                if mask & (1 << i):
                    self.assertNotEqual(colors[u], colors[v])
        p = PlantedPolicy(3, pack((2, 1, 0)))
        self.assertEqual(p.answer((1, 1)), 0)
        self.assertEqual(p.answer((0, 2)), 0)
        with self.assertRaises(ValueError):
            p.answer((3, 0))
        with self.assertRaises(ValueError):
            PlantedPolicy(3, b"\xff")


if __name__ == "__main__":
    unittest.main()
