"""Compile a public ternary circuit into the Round 9 zero-difference relation.

For challenge c the full basepoints are exactly (0, 0^m, x, gates(x)) for
C(x)=c. The suffix of constant outputs carries an optional public byte label.
All functions except the supplied-input lift and point check are compilers or
parsers. The compiler does not need a secret key.
"""
from dataclasses import dataclass
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round9"))
from differential_challenges import Poly, Problem


def _trit(value):
    return type(value) is int and 0 <= value < 3


def _index(value, limit):
    return type(value) is int and 0 <= value < limit


@dataclass(frozen=True)
class Affine:
    """A gate computing constant + sum(coefficient * wires[index])."""
    constant: int
    terms: tuple

    def __post_init__(self):
        terms = tuple(tuple(pair) for pair in self.terms)
        if not _trit(self.constant) or any(
            len(pair) != 2 or type(pair[0]) is not int or pair[0] < 0
            or not _trit(pair[1]) for pair in terms
        ):
            raise ValueError("affine gates require a trit and (index, trit) terms")
        object.__setattr__(self, "terms", terms)


@dataclass(frozen=True)
class Multiply:
    left: int
    right: int


@dataclass(frozen=True)
class TernaryCircuit:
    """Input wires first, followed by one wire per gate in topological order."""
    n_inputs: int
    gates: tuple
    outputs: tuple

    def __post_init__(self):
        if type(self.n_inputs) is not int or self.n_inputs < 0:
            raise ValueError("invalid input dimension")
        gates = tuple(self.gates)
        outputs = tuple(self.outputs)
        for i, gate in enumerate(gates, self.n_inputs):
            if isinstance(gate, Multiply):
                indices = (gate.left, gate.right)
            elif isinstance(gate, Affine):
                indices = (wire for wire, _ in gate.terms)
            else:
                raise ValueError("unknown gate")
            if any(not _index(wire, i) for wire in indices):
                raise ValueError("gate references an unavailable wire")
        if any(not _index(wire, self.n_inputs + len(gates)) for wire in outputs):
            raise ValueError("invalid output wire")
        object.__setattr__(self, "gates", gates)
        object.__setattr__(self, "outputs", outputs)

    def trace(self, x):
        """Evaluate the supplied input and return all input and gate wires."""
        wires = list(x)
        if len(wires) != self.n_inputs or not all(_trit(value) for value in wires):
            raise ValueError("invalid input vector")
        for gate in self.gates:
            if isinstance(gate, Multiply):
                value = wires[gate.left] * wires[gate.right]
            else:
                value = gate.constant + sum(a*wires[i] for i, a in gate.terms)
            wires.append(value % 3)
        return tuple(wires)

    def evaluate(self, x):
        wires = self.trace(x)
        return tuple(wires[i] for i in self.outputs)


def circuit_from_polynomials(n_inputs, outputs):
    """Build a common-product circuit from reduced Round 9 scalar polynomials."""
    if type(n_inputs) is not int or n_inputs < 0:
        raise ValueError("invalid input dimension")
    gates, output_wires = [], []
    wire_for_term = {(i,): i for i in range(n_inputs)}

    def append(gate):
        wire = n_inputs + len(gates)
        gates.append(gate)
        return wire

    for polynomial in outputs:
        if not isinstance(polynomial, Poly):
            raise TypeError("expected a Round 9 Poly")
        constant, terms = 0, []
        for term, coefficient in polynomial.terms:
            if not term:
                constant = coefficient
                continue
            if term[-1] >= n_inputs:
                raise ValueError("polynomial uses an undeclared input")
            for size in range(2, len(term) + 1):
                prefix = term[:size]
                if prefix not in wire_for_term:
                    wire_for_term[prefix] = append(Multiply(wire_for_term[prefix[:-1]], prefix[-1]))
            terms.append((wire_for_term[term], coefficient))
        if constant == 0 and len(terms) == 1 and terms[0][1] == 1:
            output_wires.append(terms[0][0])
        else:
            output_wires.append(append(Affine(constant, tuple(terms))))
    return TernaryCircuit(n_inputs, gates, output_wires)


def cm14_public_circuit(n, public):
    """Read the masked CM14 monomial-major packed coefficient payload."""
    from planar_backend import _monomials, _unpack_dense, monomial_count

    coefficients = _unpack_dense(public, n * monomial_count(n))
    rows = [{} for _ in range(n)]
    for i, term in enumerate(_monomials(n)):
        for j, value in enumerate(coefficients[n*i:n*(i+1)]):
            if value:
                rows[j][term] = value
    return circuit_from_polynomials(n, (Poly(row) for row in rows))


def two_layer_public_circuit(n, public):
    """Read the triangular backend's output-major packed coefficient payload."""
    from planar_backend import _unpack_dense
    from two_layer import public_monomials

    terms = public_monomials(n)
    width = len(terms)
    coefficients = _unpack_dense(public, n * width)
    return circuit_from_polynomials(n, (
        Poly({term: value for term, value in zip(terms, coefficients[j*width:(j+1)*width])
              if value}) for j in range(n)
    ))


def compile_circuit(circuit, public_tag=b""):
    """Return a native Round 9 Problem. public_tag carries transparent bytes."""
    if type(public_tag) is not bytes:
        raise TypeError("public tag must be bytes")
    m = len(circuit.outputs)
    clock = Poly.variable(0)
    targets = [Poly.variable(1+j) for j in range(m)]
    offset = 1 + m
    active = [2*clock*(clock-1)] + [(clock-1)*target for target in targets]
    for i, gate in enumerate(circuit.gates, circuit.n_inputs):
        # Construct the sparse residual in one pass, including repeated affine
        # terms. Every input/gate wire is in the unshifted coordinate block.
        terms = {(offset+i,): 1}
        if isinstance(gate, Multiply):
            terms[(offset+gate.left, offset+gate.right)] = -1
        else:
            terms[()] = -gate.constant
            for j, coefficient in gate.terms:
                index = (offset+j,)
                terms[index] = terms.get(index, 0) - coefficient
        active.append(clock * Poly(terms))
    for target, wire in zip(targets, circuit.outputs):
        active.append(clock * (Poly.variable(offset+wire) - target))

    active.append(Poly())
    constants = (Poly({(): 1}), Poly({(): 2}))
    for byte in public_tag:
        active.extend(constants[(byte >> shift) & 1] for shift in range(7, -1, -1))
    return Problem(m, circuit.n_inputs + len(circuit.gates), active)


def read_public_tag(problem):
    """Decode the suffix of the ordered sparse Round 9 output list."""
    end = len(problem.outputs)
    start = end
    while start and problem.outputs[start-1].terms:
        terms = problem.outputs[start-1].terms
        if terms not in ((((), 1),), (((), 2),)):
            raise ValueError("missing zero separator in tag suffix")
        start -= 1
    if start == 0 or (end-start) % 8:
        raise ValueError("invalid tag separator or bit length")
    payload = bytearray()
    for i in range(start, end, 8):
        byte = 0
        for poly in problem.outputs[i:i+8]:
            byte = (byte << 1) | (poly.terms[0][1]-1)
        payload.append(byte)
    return bytes(payload)


def lift_preimage(circuit, challenge, x):
    """Lift a known preimage to its unique collision basepoint."""
    c = tuple(challenge)
    wires = circuit.trace(x)
    if not all(_trit(t) for t in c) or c != tuple(wires[i] for i in circuit.outputs):
        raise ValueError("supplied input does not map to the challenge")
    return (0,) * (1 + len(c)) + wires


def verify_witness(problem, challenge, point):
    """Check a supplied full basepoint against the actual differential map."""
    return problem.is_collision(point, challenge)
