"""Exact F3 research code for challenge-coupled differential solvability.

These are public decision algorithms and complexity reductions, not encryption
algorithms, a hardness estimator or a private trapdoor. The mathematical input
lists its variables explicitly; dimension parameters are not a succinct way to
claim exponentially many unlisted variables. Polynomials use their unique
reduced representative (individual exponents at most two) over F3.
"""
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from itertools import product


def _dimension(value):
    if not isinstance(value, int) or value < 0:
        raise ValueError("Dimensions must be nonnegative integers")
    return int(value)


def _coordinates(values, size, field=3):
    values = tuple(values)
    if len(values) != size or any(not isinstance(x, int) or not 0 <= x < field
                                 for x in values):
        raise ValueError("Wrong coordinate count or coordinate outside the field")
    return tuple(int(value) for value in values)


@dataclass(frozen=True, init=False)
class Poly:
    """An immutable sparse polynomial function over F3."""
    terms: tuple

    def __init__(self, terms=None):
        if terms is None:
            terms = {}
        if not isinstance(terms, Mapping):
            raise TypeError("Polynomial terms must be a monomial/coefficient mapping")
        combined = {}
        for monomial, coefficient in terms.items():
            monomial = tuple(monomial)
            if not isinstance(coefficient, int):
                raise ValueError("Coefficients must be integers")
            if any(not isinstance(i, int) or i < 0 for i in monomial):
                raise ValueError("Variable indices must be nonnegative integers")
            counts = Counter(int(i) for i in monomial)
            # x^3=x as functions on F3; positive powers reduce to exponent 1 or 2.
            reduced = tuple(i for i in sorted(counts)
                            for _ in range(1 + (counts[i] - 1) % 2))
            combined[reduced] = (combined.get(reduced, 0) + coefficient) % 3
        object.__setattr__(self, "terms", tuple(sorted(
            ((m, c) for m, c in combined.items() if c), key=lambda item: (len(item[0]), item[0]))))

    @staticmethod
    def variable(index):
        index = _dimension(index)
        return Poly({(index,): 1})

    @staticmethod
    def _coerce(other):
        if isinstance(other, Poly):
            return other
        if isinstance(other, int):
            return Poly({(): other})
        raise TypeError("Polynomial arithmetic requires polynomials or integers")

    @property
    def degree(self):
        return max((len(m) for m, _ in self.terms), default=0)

    def __add__(self, other):
        other = self._coerce(other)
        terms = dict(self.terms)
        for m, c in other.terms:
            terms[m] = terms.get(m, 0) + c
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms})

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __rsub__(self, other):
        return self._coerce(other) - self

    def __mul__(self, other):
        other = self._coerce(other)
        terms = {}
        for m, a in self.terms:
            for n, b in other.terms:
                key = tuple(sorted(m + n))
                terms[key] = terms.get(key, 0) + a * b
        return Poly(terms)

    __rmul__ = __mul__

    def evaluate(self, point):
        point = _coordinates(point, len(point))
        total = 0
        for monomial, coefficient in self.terms:
            value = coefficient
            for index in monomial:
                if index >= len(point):
                    raise ValueError("Point has too few coordinates for the polynomial")
                value *= point[index]
            total += value
        return total % 3


@dataclass(frozen=True)
class Problem:
    """The public map P(s,x,y) and the entire affine challenge family."""
    n_challenges: int
    n_responses: int
    outputs: tuple

    def __post_init__(self):
        object.__setattr__(self, "n_challenges", _dimension(self.n_challenges))
        object.__setattr__(self, "n_responses", _dimension(self.n_responses))
        outputs = tuple(self.outputs)
        if any(not isinstance(p, Poly) for p in outputs):
            raise TypeError("Outputs must be Poly instances")
        for p in outputs:
            if any(i >= self.n_variables for m, _ in p.terms for i in m):
                raise ValueError("Polynomial refers to an undeclared variable")
        object.__setattr__(self, "outputs", outputs)

    @property
    def n_variables(self):
        return 1 + self.n_challenges + self.n_responses

    @property
    def degree(self):
        return max((p.degree for p in self.outputs), default=0)

    def direction(self, challenge):
        c = _coordinates(challenge, self.n_challenges)
        return (1,) + c + (0,) * self.n_responses

    def difference(self, point, challenge):
        w = _coordinates(point, self.n_variables)
        h = self.direction(challenge)
        shifted = tuple((a + b) % 3 for a, b in zip(w, h))
        return tuple((p.evaluate(shifted) - p.evaluate(w)) % 3 for p in self.outputs)

    def is_collision(self, point, challenge):
        return not any(self.difference(point, challenge))

    def public_encoding(self):
        """An explicit-variable, sparse, JSON-compatible mathematical input."""
        return {"field": 3,
                "variables": ["s"] + [f"x{i}" for i in range(self.n_challenges)]
                             + [f"y{i}" for i in range(self.n_responses)],
                "challenge_coordinates": self.n_challenges,
                "response_coordinates": self.n_responses,
                "outputs": [[[list(m), c] for m, c in p.terms] for p in self.outputs]}


def linear_coverage(problem):
    """Decide universal coverage for degree-at-most-one potentials."""
    if problem.degree > 1:
        raise ValueError("The linear criterion requires degree at most one")
    return not any(len(m) == 1 and m[0] <= problem.n_challenges
                   for p in problem.outputs for m, _ in p.terms)


def solve_linear(rows, rhs, n_variables):
    """Gaussian elimination over F3; free variables are set to zero."""
    _dimension(n_variables)
    rows, rhs = [tuple(row) for row in rows], tuple(rhs)
    if len(rows) != len(rhs) or any(len(row) != n_variables for row in rows):
        raise ValueError("Inconsistent matrix dimensions")
    if any(not isinstance(x, int) for row in rows for x in row) or any(
            not isinstance(x, int) for x in rhs):
        raise ValueError("Matrix entries must be integers")
    a = [[x % 3 for x in row] + [b % 3] for row, b in zip(rows, rhs)]
    pivot_row, pivots = 0, []
    for column in range(n_variables):
        selected = next((i for i in range(pivot_row, len(a)) if a[i][column]), None)
        if selected is None:
            continue
        a[pivot_row], a[selected] = a[selected], a[pivot_row]
        inverse = pow(a[pivot_row][column], -1, 3)
        a[pivot_row] = [(inverse * value) % 3 for value in a[pivot_row]]
        for i in range(len(a)):
            if i != pivot_row and a[i][column]:
                factor = a[i][column]
                a[i] = [(x - factor * y) % 3 for x, y in zip(a[i], a[pivot_row])]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(a):
            break
    if any(not any(row[:-1]) and row[-1] for row in a):
        return None
    result = [0] * n_variables
    for row, column in enumerate(pivots):
        result[column] = a[row][-1]
    return tuple(result)


def solve_quadratic_challenge(problem, challenge):
    """Find a public collision for one quadratic challenge, or certify none exists.

    The affine system is reconstructed by evaluations at 0 and standard basis
    vectors. No planted response, generator state or secret data is an input.
    """
    if problem.degree > 2:
        raise ValueError("Quadratic solver requires degree at most two")
    challenge = _coordinates(challenge, problem.n_challenges)
    n = problem.n_variables
    zero = (0,) * n
    constant = problem.difference(zero, challenge)
    columns = []
    for j in range(n):
        e = tuple(int(i == j) for i in range(n))
        columns.append(tuple((v - b) % 3 for v, b in zip(problem.difference(e, challenge), constant)))
    rows = [tuple(columns[j][i] for j in range(n)) for i in range(len(problem.outputs))]
    answer = solve_linear(rows, [(-b) % 3 for b in constant], n)
    if answer is not None and not problem.is_collision(answer, challenge):
        raise AssertionError("Affine solver returned an invalid collision")
    return answer


def _quadratic_parts(problem):
    """Return polar Hessians H and linear rows L for P=Q+L+b."""
    if problem.degree > 2:
        raise ValueError("Quadratic certificates require degree at most two")
    n = problem.n_variables
    matrices, linear = [], []
    for p in problem.outputs:
        h, ell = [[0] * n for _ in range(n)], [0] * n
        for term, coefficient in p.terms:
            if len(term) == 1:
                ell[term[0]] = coefficient
            elif len(term) == 2:
                i, j = term
                h[i][j] = (h[i][j] + coefficient) % 3
                h[j][i] = (h[j][i] + coefficient) % 3
        matrices.append(h)
        linear.append(ell)
    return matrices, linear


def quadratic_no_certificate(problem):
    """Find a missing direction in O(3^m poly(input)), or return None.

    A returned (c,lambda) satisfies (sum lambda_i H_i)h(c)=0 and
    (sum lambda_i L_i)h(c)=1. These identities are a public NO certificate.
    Returning None is conclusive only because every output multiplier is
    enumerated; this is not a random heuristic.
    """
    matrices, linear = _quadratic_parts(problem)
    n, r, m = problem.n_variables, problem.n_challenges, len(problem.outputs)
    for weights in product(range(3), repeat=m):
        if not any(weights):
            continue
        h = [[sum(weights[k] * matrices[k][i][j] for k in range(m)) % 3
              for j in range(n)] for i in range(n)]
        ell = [sum(weights[k] * linear[k][i] for k in range(m)) % 3 for i in range(n)]
        rows = [tuple(row[1:1+r]) for row in h] + [tuple(ell[1:1+r])]
        rhs = [(-row[0]) % 3 for row in h] + [(1 - ell[0]) % 3]
        challenge = solve_linear(rows, rhs, r)
        if challenge is not None:
            return {"challenge": challenge, "multiplier": weights}
    return None


def check_quadratic_certificate(problem, certificate):
    """Check a normalized NO certificate by polynomial-time field arithmetic."""
    matrices, linear = _quadratic_parts(problem)
    if not isinstance(certificate, Mapping):
        return False
    try:
        challenge = _coordinates(certificate["challenge"], problem.n_challenges)
        weights = _coordinates(certificate["multiplier"], len(problem.outputs))
    except (KeyError, TypeError, ValueError):
        return False
    a = problem.direction(challenge)
    n = problem.n_variables
    if any(sum(weights[k] * matrices[k][i][j] * a[j]
               for k in range(len(weights)) for j in range(n)) % 3 for i in range(n)):
        return False
    return sum(weights[k] * linear[k][j] * a[j]
               for k in range(len(weights)) for j in range(n)) % 3 == 1


def quadratic_coverage(problem, strategy="auto"):
    """Exact public decision by the smaller enumeration, never a hardness estimate."""
    if problem.degree > 2:
        raise ValueError("Quadratic coverage requires degree at most two")
    if strategy not in ("auto", "challenges", "outputs"):
        raise ValueError("Unknown enumeration strategy")
    if strategy == "auto":
        strategy = "challenges" if problem.n_challenges <= len(problem.outputs) else "outputs"
    if strategy == "outputs":
        return quadratic_no_certificate(problem) is None
    return all(solve_quadratic_challenge(problem, c) is not None
               for c in product(range(3), repeat=problem.n_challenges))


def quadratic_unsat_problem(n_boolean_variables, clauses):
    """Reduce 3-CNF UNSAT to universal quadratic differential coverage.

    For each challenge c, a collision exists iff the Boolean assignment c^2
    falsifies at least one clause. The implementation uses 10 response wires
    and 9 equations per clause, plus one final equation. No truth table is built.
    """
    r = _dimension(n_boolean_variables)
    clauses = tuple(tuple(clause) for clause in clauses)
    if any(len(clause) != 3 or any(not isinstance(a, int) or a == 0 or abs(a) > r
                                 for a in clause) for clause in clauses):
        raise ValueError("Require clauses of exactly three valid signed literals")
    s = Poly.variable(0)
    x = [Poly.variable(1+i) for i in range(r)]
    next_index = 1 + r
    outputs, ends = [], []

    def fresh():
        nonlocal next_index
        result = Poly.variable(next_index)
        next_index += 1
        return result

    for clause in clauses:
        previous = fresh()  # A free multiplier, not a secret trapdoor.
        for literal in clause:
            first, square, following = fresh(), fresh(), fresh()
            axis = x[abs(literal)-1]
            outputs.extend((s * first - axis * previous, s * square - axis * first))
            failure = previous - square if literal > 0 else square
            outputs.append(s * (following - failure))
            previous = following
        ends.append(previous)
    outputs.append(s * (sum(ends, Poly()) - 1))
    return Problem(r, next_index - (1+r), tuple(outputs))


@dataclass(frozen=True)
class BooleanCircuit:
    """A topologically ordered Boolean circuit; inputs are universal then existential."""
    n_universal: int
    n_existential: int
    gates: tuple
    output: int

    def __post_init__(self):
        object.__setattr__(self, "n_universal", _dimension(self.n_universal))
        object.__setattr__(self, "n_existential", _dimension(self.n_existential))
        gates = tuple(tuple(g) for g in self.gates)
        arities = {"and": 2, "or": 2, "xor": 2, "not": 1, "const": 1}
        inputs = self.n_universal + self.n_existential
        for number, gate in enumerate(gates):
            if not gate or gate[0] not in arities or len(gate) != 1 + arities[gate[0]]:
                raise ValueError("Malformed Boolean gate")
            if gate[0] == "const":
                _coordinates(gate[1:], 1, 2)
            elif any(not isinstance(i, int) or not 0 <= i < inputs + number for i in gate[1:]):
                raise ValueError("Gate references an unavailable wire")
        if not isinstance(self.output, int) or not 0 <= self.output < inputs + len(gates):
            raise ValueError("Invalid output wire")
        object.__setattr__(self, "gates", tuple((gate[0], *(int(i) for i in gate[1:])) for gate in gates))
        object.__setattr__(self, "output", int(self.output))

    def _wires(self, universal, existential):
        u = _coordinates(universal, self.n_universal, 2)
        v = _coordinates(existential, self.n_existential, 2)
        wires = list(u + v)
        for gate in self.gates:
            operation, args = gate[0], gate[1:]
            if operation == "const":
                value = args[0]
            elif operation == "not":
                value = 1 - wires[args[0]]
            else:
                a, b = (wires[i] for i in args)
                value = {"and": a*b, "or": a+b-a*b, "xor": (a+b) % 2}[operation]
            wires.append(value)
        return tuple(wires)

    def evaluate(self, universal, existential):
        return self._wires(universal, existential)[self.output]


def cubic_circuit_problem(circuit):
    """Reduce forall u exists v C(u,v)=1 to ternary cubic differential coverage."""
    r, v_count = circuit.n_universal, circuit.n_existential
    s = Poly.variable(0)
    x = [Poly.variable(1+i) for i in range(r)]
    v = [Poly.variable(1+r+i) for i in range(v_count)]
    u = [Poly.variable(1+r+v_count+i) for i in range(r)]
    gate_vars = [Poly.variable(1+2*r+v_count+i) for i in range(len(circuit.gates))]
    wires = u + v + gate_vars
    residuals = [u[i] - x[i]*x[i] for i in range(r)]
    residuals += [bit*(bit-1) for bit in v]
    for number, gate in enumerate(circuit.gates):
        operation, args = gate[0], gate[1:]
        out = gate_vars[number]
        if operation == "const":
            residual = out - args[0]
        elif operation == "not":
            residual = out + wires[args[0]] - 1
        else:
            a, b = (wires[i] for i in args)
            if operation == "and":
                residual = out - a*b
            elif operation == "or":
                residual = out - a - b + a*b
            else:  # XOR on Boolean inputs: a+b-2ab.
                residual = out - a - b + 2*a*b
        residuals.append(residual)
    residuals.append(wires[circuit.output] - 1)
    outputs = [2*s*(s-1)] + [(s-1)*axis for axis in x]
    outputs += [s * residual for residual in residuals]
    return Problem(r, v_count + r + len(circuit.gates), tuple(outputs))


def lift_circuit_witness(circuit, challenge, response):
    """Encode a supplied accepting response; this is not a response-finding algorithm."""
    c = _coordinates(challenge, circuit.n_universal)
    v = _coordinates(response, circuit.n_existential, 2)
    u = tuple(value*value % 3 for value in c)
    wires = circuit._wires(u, v)
    if wires[circuit.output] != 1:
        raise ValueError("The Boolean response does not satisfy the circuit")
    gates = wires[circuit.n_universal + circuit.n_existential:]
    return (0,) + (0,) * circuit.n_universal + v + u + gates
