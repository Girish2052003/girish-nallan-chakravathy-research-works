"""Centered odd-coefficient layout for the publicly invertible research orbit.

The public key contains the input center, its output and the centered cubic
coefficients. Suite parameters are out of band. This is a size experiment.
"""
from itertools import combinations_with_replacement, permutations
from math import comb, prod

from orbit_backend import OrbitBackend, _check_vector
from planar_backend import _matvec, _pack_dense, _unpack_dense
from differential_bridge import Affine, Multiply, TernaryCircuit, Poly, circuit_from_polynomials


def compact_trit_count(n):
    if type(n) is not int or n <= 0:
        raise ValueError('positive dimension required')
    return 2 * n + n * comb(n + 2, 3)


def _odd_terms(n):
    for i in range(n):
        yield (i,)
    for triple in combinations_with_replacement(range(n), 3):
        if triple[0] != triple[2]:
            yield triple


def compact_public_circuit(n, public):
    """Lower the public translations and centered map to ternary circuit gates."""
    data = _unpack_dense(public, compact_trit_count(n))
    center, offset = data[:n], data[n:2*n]
    rows = [{} for _ in range(n)]
    for i, term in enumerate(_odd_terms(n), 2):
        for row, coefficient in zip(rows, data[n*i:n*(i + 1)]):
            if coefficient:
                row[term] = coefficient
    middle = circuit_from_polynomials(n, (Poly(row) for row in rows))
    # After the n mandatory translation gates, every middle wire is shifted
    # by exactly n positions, including a raw input selected as an output.
    gates = [Affine((-c) % 3, ((i, 1),)) for i, c in enumerate(center)]
    for gate in middle.gates:
        if isinstance(gate, Multiply):
            gates.append(Multiply(n + gate.left, n + gate.right))
        else:
            terms = tuple((n + wire, coefficient) for wire, coefficient in gate.terms)
            gates.append(Affine(gate.constant, terms))
    first_output = n + len(gates)
    gates.extend(Affine(v, ((n + wire, 1),)) for v, wire in zip(offset, middle.outputs))
    return TernaryCircuit(n, gates, tuple(range(first_output, first_output + n)))


class CompactOrbitBackend(OrbitBackend):
    """The same sampled masks in a separate KEM suite and public wire format."""
    def __init__(self, n, indices=None):
        super().__init__(n, indices)
        i, j = self.indices
        self.suite = b'SG-DIFRA/R13/centered-affine-power/v1/' + i.to_bytes(4, 'big') + j.to_bytes(4, 'big')

    def _public_coefficients(self, public):
        if type(public) is not bytes:
            raise ValueError('public key must be bytes')
        if self._public_cache is None or self._public_cache[0] != public:
            self._public_cache = (public, _unpack_dense(public, compact_trit_count(self.dimension)))
        return self._public_cache[1]

    def public_from_private(self, private):
        inner, outer = self._masks(private)
        if self._private_cache[2] is not None:
            return self._private_cache[2]
        n, field = self.dimension, self.field
        center = inner.undo((0,) * n)
        data = bytearray((*center, *outer.offset))
        columns = [field.from_coeffs(row[i] for row in inner.rows) for i in range(n)]
        factors = [columns] + [[field.power(column, 3**k) for column in columns] for k in self.indices]
        for term in _odd_terms(n):
            # Reduced linears come from the unreduced pure cubes. Each other
            # monomial receives one product for each distinct slot assignment.
            triple = term * 3 if len(term) == 1 else term
            total = 0
            for i, j, k in set(permutations(triple)):
                term_value = field.mul(field.mul(factors[0][i], factors[1][j]), factors[2][k])
                total = field.add(total, term_value)
            data.extend(_matvec(outer.rows, field.coeffs(total)))
        public = _pack_dense(data)
        self._private_cache = (private, (inner, outer), public)
        return public

    def forward(self, public, x):
        n = self.dimension
        _check_vector(x, n)
        data = self._public_coefficients(public)
        centered = tuple((t - c) % 3 for t, c in zip(x, data[:n]))
        result = list(data[n:2*n])
        for i, term in enumerate(_odd_terms(n), 2):
            weight = prod(centered[j] for j in term) % 3
            if weight:
                for j, coefficient in enumerate(data[n*i:n*(i + 1)]):
                    result[j] += weight * coefficient
        return tuple(t % 3 for t in result)
