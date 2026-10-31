"""Exact public witness recovery by quotienting all global constant shifts.

Extends Round-8 PublicShiftSystem. The algorithm is polynomial in explicit
factor-table length when the *publicly computed* shift codimension is O(log L),
even with high primal width or deficient shift-increment rank. Otherwise it is
an exponential but complete finite search. It is not a KEM or a hardness proof.
"""
from dataclasses import dataclass
from itertools import product

from public_global_shift_witness_recovery import PublicShiftSystem, _rref


@dataclass(frozen=True)
class QuotientResult:
    status: str  # "recovered" or "unsatisfiable" (for fully valid inputs)
    witness: tuple | None
    cosets_examined: int


class PublicQuotientSystem(PublicShiftSystem):
    def __init__(self, n, factors):
        super().__init__(n, factors)
        span = list(self.shift_basis)
        complement = []
        rank = len(span)
        for j in range(n):
            e = tuple(int(i == j) for i in range(n))
            if len(_rref(span + [e], n)[1]) > rank:
                complement.append(e)
                span.append(e)
                rank += 1
        assert rank == n
        self.complement = tuple(complement)
        self.quotient_dimension = len(self.complement)

    def _shift_coefficients(self, rhs):
        # Gamma has columns self.increments. Solve Gamma a = rhs.
        k = self.shift_dimension
        rows = [[col[i] for col in self.increments] + [rhs[i]]
                for i in range(self.output_dimension)]
        reduced, pivots = _rref(rows, k)
        if any(not any(row[:k]) and row[k] for row in reduced):
            return None
        result = [0] * k
        for row, pivot in zip(reduced, pivots):
            result[pivot] = row[k]
        return tuple(result)

    def count_solutions(self, targets):
        """Exact global fiber cardinality; exponential in quotient codimension."""
        targets = [tuple(t) for t in targets]
        if len(targets) != len(self.factors) or any(
            len(t) != length or any(x not in (0, 1, 2) for x in t)
            for t, length in zip(targets, self.output_lengths)
        ):
            raise ValueError("one valid ternary target per factor required")
        target = tuple(x for t in targets for x in t)
        orbit_count = 0
        for a in product(range(3), repeat=self.quotient_dimension):
            z = tuple(sum(c * h[j] for c, h in zip(a, self.complement)) % 3
                      for j in range(self.n))
            fz = self._evaluate(z)
            rhs = tuple((u - v) % 3 for u, v in zip(target, fz))
            if self._shift_coefficients(rhs) is not None:
                orbit_count += 1
        return orbit_count * 3 ** (self.shift_dimension - self.increment_rank)

    def solve(self, targets):
        targets = [tuple(t) for t in targets]
        if len(targets) != len(self.factors) or any(
            len(t) != length or any(x not in (0, 1, 2) for x in t)
            for t, length in zip(targets, self.output_lengths)
        ):
            raise ValueError("one valid ternary target per factor required")
        target = tuple(x for t in targets for x in t)
        examined = 0
        for a in product(range(3), repeat=self.quotient_dimension):
            examined += 1
            z = tuple(sum(c * h[j] for c, h in zip(a, self.complement)) % 3
                      for j in range(self.n))
            fz = self._evaluate(z)
            rhs = tuple((u - v) % 3 for u, v in zip(target, fz))
            coeffs = self._shift_coefficients(rhs)
            if coeffs is None:
                continue
            witness = tuple((z[j] + sum(c * h[j] for c, h in
                             zip(coeffs, self.shift_basis))) % 3
                            for j in range(self.n))
            if self._evaluate(witness) != target:
                raise AssertionError("public witness did not verify")
            return QuotientResult("recovered", witness, examined)
        return QuotientResult("unsatisfiable", None, examined)
