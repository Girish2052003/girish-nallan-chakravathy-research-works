"""Finite checks of the single-cubic-monomial graph colouring reduction."""

from dataclasses import replace
from itertools import product
import unittest

from cubic_compiler import compile_three_colouring
from quadratic_compiler import Circuit


TRITS = (0, 1, 2)
BITS = (0, 1)


def transcript(circuit, left, right):
    wires = list(left + right)
    for gate in circuit.gates:
        if gate[0] == "not":
            wires.append(1 - wires[gate[1]])
        else:
            wires.append(wires[gate[1]] & wires[gate[2]])
    return tuple(wires)


def collision(instance, challenge, responses, start=None):
    """Direct comparison of two raw polynomial outputs at translated points."""
    if start is None:
        # Deliberately use a nonzero start for the publicly shifted coordinates.
        start = tuple((2 + i) % 3 for i in range(1 + len(challenge)))
    shifted = tuple((z + h) % 3 for z, h in zip(start, (1,) + challenge))
    return instance.potential_values(start + responses) == instance.potential_values(shifted + responses)


def permitted_colors(instance, c):
    return {
        (a, b) for a, b in product(TRITS, repeat=2)
        if collision(instance, c, instance.complete(c, a, b))
    }


def four_vertex_circuit(complete):
    # K4 tests (u0 != v0) OR (u1 != v1); K2,2 tests only u0 != v0.
    gates = []

    def gate(op, *inputs):
        gates.append((op,) + inputs)
        return 3 + len(gates)

    def either(a, b):
        return gate("not", gate("and", gate("not", a), gate("not", b)))

    def different(a, b):
        return gate("and", either(a, b), gate("not", gate("and", a, b)))

    edge = different(0, 2)
    if complete:
        edge = either(edge, different(1, 3))
    return Circuit(2, tuple(gates), edge)


class CubicCompilerTests(unittest.TestCase):
    def test_all_trits_transcripts_and_both_independent_local_tables(self):
        # The only Boolean edge is 1 -> 0. Extra challenge trits range over
        # all 9 candidate transcripts, including every false/nonbinary one.
        graph = Circuit(1, (("not", 1), ("and", 0, 2)), 3)
        instance = compile_three_colouring(graph)
        all_pairs = set(product(TRITS, repeat=2))
        by_address = {(u, v): all_pairs.copy() for u, v in product(TRITS, repeat=2)}
        for c in product(TRITS, repeat=graph.challenge_size):
            u, v, neg_v, edge = c
            good_edge = (u, v, neg_v, edge) == (1, 0, 1, 1)
            same = u == v and u in BITS
            expected = {(a, b) for a, b in all_pairs
                        if (not same or a == b) and (not good_edge or a != b)}
            actual = permitted_colors(instance, c)
            self.assertEqual(actual, expected, c)
            by_address[u, v].intersection_update(actual)

        tables = tuple(product(TRITS, repeat=3))
        winning = 0
        for left, right in product(tables, repeat=2):
            passes = all((left[u], right[v]) in permitted
                         for (u, v), permitted in by_address.items())
            expected = left[0] == right[0] and left[1] == right[1] and left[1] != right[0]
            self.assertEqual(passes, expected)
            winning += passes
        # 3*2 proper colorings; the two nonbinary-address entries are free.
        self.assertEqual(winning, 54)

    def test_all_colorings_on_four_vertices(self):
        vertices = tuple(product(BITS, repeat=2))
        for complete, expected_count in ((True, 0), (False, 18)):
            graph = four_vertex_circuit(complete)
            instance = compile_three_colouring(graph)
            constraints = {}
            for i, u in enumerate(vertices):
                for j, v in enumerate(vertices):
                    c = transcript(graph, u, v)
                    constraints[i, j] = permitted_colors(instance, c)
                    adjacent = u != v if complete else u[0] != v[0]
                    self.assertEqual(c[graph.output], int(adjacent))
                    self.assertEqual(constraints[i, j], {
                        (a, b) for a, b in product(TRITS, repeat=2)
                        if (i != j or a == b) and (not adjacent or a != b)
                    })
            # Diagonal constraints identify the two Boolean-address tables.
            count = sum(all((labels[i], labels[j]) in allowed
                            for (i, j), allowed in constraints.items())
                        for labels in product(TRITS, repeat=4))
            self.assertEqual(count, expected_count)

    def test_term_counts_and_each_single_deletion(self):
        graph = four_vertex_circuit(True)
        original = compile_three_colouring(graph)
        first_stationary = 1 + original.challenge_size
        for row in original.potentials:
            self.assertLessEqual(len(row), 5)
            for _, factors in row:
                self.assertEqual(len(set(factors)), len(factors))
                self.assertEqual(sum(i < first_stationary for i in factors), 1)
                if len(factors) != 2:
                    self.assertIn(0, factors)
        exceptions = [(i, term) for i, row in enumerate(original.potentials)
                      for term in row if len(term[1]) != 2]
        self.assertEqual([len(term[1]) for _, term in exceptions], [1, 3])
        self.assertEqual([term[0] for _, term in exceptions], [2, 2])
        vertices = tuple(product(BITS, repeat=2))
        for row_idx, term in exceptions:
            rows = list(original.potentials)
            rows[row_idx] = tuple(x for x in rows[row_idx] if x != term)
            edited = replace(original, potentials=tuple(rows))
            for u, v in product(vertices, repeat=2):
                c = transcript(graph, u, v)
                if len(term[1]) == 1:
                    responses = (0,) * (2 + len(edited.assignments))
                else:
                    # With -s*M*N removed, the row forces Q=0. Other
                    # assignments retain their triangular definitions.
                    values = [0, 0]
                    for i, expr in enumerate(edited.assignments):
                        values.append(0 if i == row_idx else expr.evaluate(c, values))
                    responses = tuple(values)
                self.assertTrue(collision(edited, c, responses))

    def test_helper_tampering_breaks_a_collision(self):
        graph = Circuit(1, (("not", 1), ("and", 0, 2)), 3)
        instance = compile_three_colouring(graph)
        c = (1, 0, 1, 1)
        genuine = instance.complete(c, 2, 0)
        self.assertTrue(collision(instance, c, genuine))
        for i in range(2, len(genuine)):
            values = list(genuine)
            values[i] = (values[i] + 1) % 3
            self.assertFalse(collision(instance, c, tuple(values)), i)


if __name__ == "__main__":
    unittest.main()
