"""Public affine-shift recovery for overlapping finite-field constraints.

Input: n, public scopes, COMPLETE public ternary function tables, targets.
No local coordinate transforms, potentials or planted witness are inputs.

The algorithm computes the full constant-shift space D of the joint map
F(x)=(f_i(x|S_i)) and its linear increment map Gamma. Targets in
F(0)+im(Gamma) have a public witness; a target outside this affine image is
INCONCLUSIVE, since nonlinear quotient variables may still solve it.

Preprocessing is polynomial in explicit local table size and global dimensions,
independently of primal graph width. This is a structural attack criterion,
not a general NCSG solver, KEM, or cryptographic security result.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ShiftResult:
    status: str
    witness: tuple | None


def _rref(rows, ncols):
    """Reduce over GF(3), pivoting only the first ncols columns."""
    matrix = [list(row) for row in rows]
    pivots = []
    for col in range(ncols):
        pivot = next((i for i in range(len(pivots), len(matrix))
                      if matrix[i][col] % 3), None)
        if pivot is None:
            continue
        index = len(pivots)
        matrix[index], matrix[pivot] = matrix[pivot], matrix[index]
        inv = pow(matrix[index][col] % 3, -1, 3)
        matrix[index] = [x * inv % 3 for x in matrix[index]]
        for i in range(len(matrix)):
            if i != index and matrix[i][col] % 3:
                coefficient = matrix[i][col] % 3
                matrix[i] = [(x - coefficient*y) % 3
                             for x, y in zip(matrix[i], matrix[index])]
        pivots.append(col)
    return matrix, pivots


def _nullspace(rows, ncols):
    matrix, pivots = _rref(rows, ncols)
    basis = []
    for free in range(ncols):
        if free in pivots:
            continue
        vector = [0] * ncols
        vector[free] = 1
        for row, pivot in zip(matrix, pivots):
            vector[pivot] = -row[free] % 3
        basis.append(tuple(vector))
    return basis


def _constant_shifts(table):
    """Enumerate and fully validate every constant derivative from the table."""
    points = tuple(table)
    k = len(points[0])
    origin = (0,) * k
    offset = table[origin]
    probes = points[::max(1, len(points)//16)][:16]
    shifts = {}
    for h in points:
        increment = tuple((a - b) % 3 for a, b in zip(table[h], offset))

        def matches(x):
            translated = tuple((a + b) % 3 for a, b in zip(x, h))
            return all((a-b) % 3 == c for a, b, c in
                       zip(table[translated], table[x], increment))

        if all(matches(x) for x in probes) and all(matches(x) for x in points):
            shifts[h] = increment
    return shifts


class PublicShiftSystem:
    def __init__(self, n, factors):
        if not isinstance(n, int) or n < 0:
            raise ValueError("n must be a nonnegative integer")
        self.n = n
        self.factors = [(tuple(scope), dict(table)) for scope, table in factors]
        self.output_lengths = []
        local_shifts = []
        restrictions = []
        for scope, table in self.factors:
            k = len(scope)
            if len(set(scope)) != k or any(not isinstance(j, int) or
                                          not 0 <= j < n for j in scope):
                raise ValueError("scope must contain distinct valid variables")
            if len(table) != 3**k or any(len(x) != k or
                    any(a not in (0, 1, 2) for a in x) for x in table):
                raise ValueError("a complete public ternary table is required")
            r = len(next(iter(table.values())))
            if any(len(y) != r or any(a not in (0, 1, 2) for a in y)
                   for y in table.values()):
                raise ValueError("table outputs must have a fixed ternary length")
            self.output_lengths.append(r)
            shifts = _constant_shifts(table)
            local_shifts.append(shifts)
            # Annihilator vectors impose P_i h in C(f_i).
            for annihilator in _nullspace(list(shifts), k):
                row = [0] * n
                for j, coefficient in zip(scope, annihilator):
                    row[j] = coefficient
                restrictions.append(tuple(row))
        self.shift_basis = _nullspace(restrictions, n)
        self.shift_dimension = len(self.shift_basis)
        self.output_dimension = sum(self.output_lengths)
        self.increments = [tuple(c for (scope, _), shifts in
                                 zip(self.factors, local_shifts)
                                 for c in shifts[tuple(h[j] for j in scope)])
                           for h in self.shift_basis]
        self.increment_rank = len(_rref(self.increments, self.output_dimension)[1])
        self.offset = self._evaluate((0,) * n)

    def _evaluate(self, x):
        return tuple(c for scope, table in self.factors
                     for c in table[tuple(x[j] for j in scope)])

    def solve(self, targets):
        targets = [tuple(target) for target in targets]
        if len(targets) != len(self.factors) or any(len(target) != r or
                any(a not in (0, 1, 2) for a in target)
                for target, r in zip(targets, self.output_lengths)):
            raise ValueError("one ternary target per public factor is required")
        target = tuple(a for value in targets for a in value)
        rhs = tuple((a-b) % 3 for a, b in zip(target, self.offset))
        rows = [[column[i] for column in self.increments] + [rhs[i]]
                for i in range(self.output_dimension)]
        reduced, pivots = _rref(rows, self.shift_dimension)
        if any(not any(row[:-1]) and row[-1] for row in reduced):
            return ShiftResult("inconclusive", None)
        coefficients = [0] * self.shift_dimension
        for row, pivot in zip(reduced, pivots):
            coefficients[pivot] = row[-1]
        witness = tuple(sum(c * h[j] for c, h in
                            zip(coefficients, self.shift_basis)) % 3
                        for j in range(self.n))
        if self._evaluate(witness) != target:
            raise AssertionError("public shift witness failed verification")
        return ShiftResult("recovered", witness)
