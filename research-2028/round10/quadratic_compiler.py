"""A quadratic differential reduction from succinct graph nonconnectivity.

Public coordinates are (s, x), with shift (1, c). Stationary coordinates
are (A, B, helpers), where A sees the left address, B the right address,
and every helper sees the whole challenge. The code emits actual sparse
potentials. All field operations use F3. No third-party modules are needed.
"""

from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Circuit:
    """Inputs are left bits, then right bits. New wires follow gate order.

    A gate is ("not", i) or ("and", i, j), using zero-based wire numbers.
    The same input may appear twice in an AND gate. An output may also
    be a primary input. A graph has 2**width vertices.
    """

    width: int
    gates: tuple
    output: int

    def __post_init__(self):
        if type(self.width) is not int or self.width < 1:
            raise ValueError("Address width must be a positive integer")
        wire_count = 2 * self.width
        for gate in self.gates:
            if not gate or gate[0] not in ("not", "and"):
                raise ValueError("Unknown gate")
            arity = 1 if gate[0] == "not" else 2
            if len(gate) != arity + 1 or any(
                type(i) is not int or not 0 <= i < wire_count for i in gate[1:]
            ):
                raise ValueError("Invalid gate arity or wire index")
            wire_count += 1
        if type(self.output) is not int or not 0 <= self.output < wire_count:
            raise ValueError("Invalid output wire")

    @property
    def challenge_size(self):
        return 2 * self.width + len(self.gates)


def _checked_vector(values, size, alphabet, name):
    values = tuple(values)
    if len(values) != size or any(type(x) is not int or x not in alphabet for x in values):
        raise ValueError(f"Invalid {name}")
    return values


@dataclass(frozen=True)
class _Expression:
    # Represents constant + sum(coefficient * optional challenge trit * response).
    constant: int
    terms: tuple

    def evaluate(self, challenge, responses):
        value = self.constant
        for coefficient, trit, response in self.terms:
            factor = 1 if trit is None else challenge[trit]
            value += coefficient * factor * responses[response]
        return value % 3


def _linear(*terms, constant=0):
    return _Expression(constant, tuple((coef, None, index) for coef, index in terms))


@dataclass(frozen=True)
class DifferentialInstance:
    challenge_size: int
    assignments: tuple
    potentials: tuple

    def complete(self, challenge, left, right):
        """Return the unique helper completion satisfying all assignment rows."""
        c = _checked_vector(challenge, self.challenge_size, range(3), "challenge")
        values = list(_checked_vector((left, right), 2, range(3), "local responses"))
        for expr in self.assignments:
            values.append(expr.evaluate(c, values))
        return tuple(values)

    def potential_values(self, point):
        """Evaluate the emitted sparse monomials directly at an entire input."""
        n = 1 + self.challenge_size + 2 + len(self.assignments)
        point = _checked_vector(point, n, range(3), "potential input")
        result = []
        for polynomial in self.potentials:
            value = 0
            for coefficient, factors in polynomial:
                term = coefficient
                for coordinate in factors:
                    term *= point[coordinate]
                value += term
            result.append(value % 3)
        return tuple(result)


class _Builder:
    def __init__(self, size):
        self.size = size
        self.assignments = []
        self.rows = []

    def assign(self, expr):
        new_index = 2 + len(self.assignments)
        self.assignments.append(expr)
        self.rows.append(_Expression(expr.constant, expr.terms + ((-1, None, new_index),)))
        return new_index

    def guard(self, payload, positions, accepted):
        """Multiply a response by the indicator of a constant-arity predicate.

        The indicator of c=d is 1-(c-d)^2. Each intermediate c*response
        is expressible by a quadratic monomial in the potential.
        """
        branches = []
        for pattern in accepted:
            value = payload
            for position, digit in zip(positions, pattern):
                first = self.assign(_Expression(0, ((1, position, value),)))
                # (1-d^2)*value + 2*d*c*value - c*(c*value)
                value = self.assign(_Expression(0, (
                    (1 - digit * digit, None, value),
                    (2 * digit, None, first),
                    (-1, position, first),
                )))
            branches.append((1, value))
        return self.assign(_linear(*branches))

    def zero(self, response):
        self.rows.append(_linear((1, response)))

    def finish(self):
        polys = []
        offset = 1 + self.size
        for row in self.rows:
            # Delta(beta*s) = beta. Delta(x_i*y_j) = c_i*y_j.
            # Index 0 instead of x_i gives Delta(s*y_j) = y_j.
            coef = {(0,): row.constant}
            for weight, trit, response in row.terms:
                key = (0 if trit is None else 1 + trit, offset + response)
                coef[key] = coef.get(key, 0) + weight
            polys.append(tuple(
                (weight % 3, factors) for factors, weight in sorted(coef.items()) if weight % 3
            ))
        return DifferentialInstance(self.size, tuple(self.assignments), tuple(polys))


def _equality_and_edge(builder, circuit, equality_payload, edge_payload):
    width = circuit.width
    same = equality_payload
    for i in range(width):
        same = builder.guard(same, (i, width + i), ((0, 0), (1, 1)))
    builder.zero(same)

    edge = edge_payload
    for i in range(2 * width):
        edge = builder.guard(edge, (i,), ((0,), (1,)))
    for i, gate in enumerate(circuit.gates, start=2 * width):
        inputs = gate[1:]
        # If input wires coincide, inconsistent patterns have zero product.
        # Each valid transcript still matches exactly one pattern.
        patterns = []
        for bits in product((0, 1), repeat=len(inputs)):
            result = 1 - bits[0] if gate[0] == "not" else bits[0] * bits[1]
            patterns.append(bits + (result,))
        edge = builder.guard(edge, inputs + (i,), patterns)
    edge = builder.guard(edge, (circuit.output,), ((1,),))
    builder.zero(edge)


def compile_nonconnectivity(circuit, start, target):
    """Compile weak nonconnectivity of two vertices specified by bit tuples.

    Challenge slots hold two addresses followed by the claimed gate values.
    The equality and anchor rows apply independently of the wire transcript.
    Each address bit and bounded-fan-in gate adds O(1) helpers and rows.
    Writing variable indices in binary adds a logarithmic factor in bits.
    """
    width = circuit.width
    start = _checked_vector(start, width, (0, 1), "start address")
    target = _checked_vector(target, width, (0, 1), "target address")
    builder = _Builder(circuit.challenge_size)
    difference = builder.assign(_linear((1, 0), (-1, 1)))

    _equality_and_edge(builder, circuit, difference, difference)

    start_value = 0  # index of A
    target_value = builder.assign(_linear((1, 1), constant=-1))  # B-1
    for i in range(width):
        start_value = builder.guard(start_value, (i,), ((start[i],),))
        target_value = builder.guard(target_value, (width + i,), ((target[i],),))
    builder.zero(start_value)
    builder.zero(target_value)
    return builder.finish()
