"""Compile succinct graph 3-colouring to a ternary differential strategy.

Only the two color coordinates have restricted observation. A polynomial-
size Boolean circuit on vertex addresses specifies the edges. Each public
challenge also contains a candidate transcript for the circuit. See
quadratic_compiler.py for the monomial encoding and the two public guards.
"""

from dataclasses import dataclass, replace

from quadratic_compiler import _Builder, _equality_and_edge, _linear


@dataclass(frozen=True)
class _Product:
    left: int
    right: int

    def evaluate(self, challenge, responses):
        return responses[self.left] * responses[self.right] % 3


def compile_three_colouring(circuit):
    """Return the sparse potential and a constructive helper completion.

    Every monomial is quadratic except one linear and one square-free
    cubic monomial. The degree includes the public clock coordinate s.
    """
    builder = _Builder(circuit.challenge_size)
    # Responses 0 and 1 are the local colors A and B. All later coordinates
    # are stationary helpers with full observation of the public challenge.
    unit = builder.assign(_linear(constant=1))
    difference = builder.assign(_linear((1, 0), (-1, 1)))
    minus = builder.assign(_linear((1, difference), (-1, unit)))
    plus = builder.assign(_linear((1, difference), (1, unit)))

    # Reserve the product output in the triangular assignment list. The
    # generic builder emits quadratic rows; install this row explicitly below.
    product_row = len(builder.rows)
    edge_value = builder.assign(_linear())
    _equality_and_edge(builder, circuit, difference, edge_value)
    base = builder.finish()
    offset = 1 + base.challenge_size  # first stationary coordinate in P
    rows = list(base.potentials)
    rows[0] = ((2, (0,)), (1, (0, offset + unit)))  # s(T-1)
    rows[product_row] = (
        (1, (0, offset + edge_value)),
        (2, (0, offset + minus, offset + plus)),
    )  # s(Q-M*N)
    assignments = list(base.assignments)
    assignments[edge_value - 2] = _Product(minus, plus)
    return replace(base, assignments=tuple(assignments), potentials=tuple(rows))
