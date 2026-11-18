"""Research permutation with uniform affine masks on a ternary field power.

The public key contains only the coefficients of the resulting cubic, in the
monomial-major layout used in Round 12. No security level is assigned.
"""
from itertools import product
from math import gcd
from pathlib import Path
import secrets
import sys

_PREVIOUS = Path(__file__).resolve().parents[1] / 'round12'
sys.path.insert(0, str(_PREVIOUS))
from field3 import Field3, MODULI, _check_modulus
from planar_backend import (_Affine, _matrix_inverse, _matvec, _monomials, _pack_dense,
                            _unpack_dense, monomial_count)


PROFILE_POWERS = {
    4: (1, 3), 5: (1, 3), 7: (1, 5), 8: (1, 5),
    82: (22, 53), 122: (33, 78), 163: (44, 104),
    164: (45, 105), 244: (66, 157), 325: (87, 208),
}

EXTRA_MODULI = {
    164: ((0, 2), (15, 1)),
    244: ((0, 2), (31, 1)),
    325: ((0, 1), (157, 2)),
}


class _OrbitField(Field3):
    """The same polynomial basis and arithmetic with extra checked moduli."""
    def __init__(self, n):
        terms = EXTRA_MODULI.get(n, MODULI.get(n))
        if terms is None or not _check_modulus(n, terms):
            raise ValueError('no verified modulus for this dimension')
        self.n, self.terms, self.order = n, terms, 3**n


def power_exponent(n, i, j):
    if type(n) is not int or not 3 <= n < 2**32:
        raise ValueError('dimension must be at least three and fit in uint32')
    if type(i) is not int or type(j) is not int or not 0 < i < j < n:
        raise ValueError('expected distinct ordered positive Frobenius indices')
    d = 1 + 3**i + 3**j
    if gcd(d, 3**n-1) != 1:
        raise ValueError('central exponent does not permute this field')
    return d


def _random_mask(n, fixed_column=False):
    # The normalized inner mask fixes the basis element 1. Its first matrix
    # column occupies no secret-key bytes. Condition independent free trits
    # on invertibility to give the uniform distribution on this subgroup.
    while True:
        width = n-1 if fixed_column else n
        encoded_rows = tuple(bytes(secrets.randbelow(3) for _ in range(width)) for _ in range(n))
        rows = tuple(bytes([int(i == 0)]) + row for i, row in enumerate(encoded_rows)) if fixed_column else encoded_rows
        if _matrix_inverse(rows) is not None:
            return b''.join(encoded_rows) + bytes(secrets.randbelow(3) for _ in range(n))


def _check_vector(x, n):
    if len(x) != n or any(type(t) is not int or not 0 <= t < 3 for t in x):
        raise ValueError('invalid ternary vector')


class OrbitBackend:
    """Implements the Round 11 backend contract for each implemented field."""
    def __init__(self, n, indices=None):
        if type(n) is not int or n not in PROFILE_POWERS:
            raise ValueError('unsupported orbit dimension')
        i, j = PROFILE_POWERS[n] if indices is None else indices
        self.dimension = n
        self.indices = i, j
        self.exponent = power_exponent(n, i, j)
        self.field = _OrbitField(n)
        self.inverse_exponent = pow(self.exponent, -1, self.field.order - 1)
        self.suite = b'SG-DIFRA/R13/affine-power/v1/' + i.to_bytes(4, 'big') + j.to_bytes(4, 'big')
        self._public_cache = self._private_cache = None

    def generate(self):
        private = _pack_dense(_random_mask(self.dimension, fixed_column=True) + _random_mask(self.dimension))
        return self.public_from_private(private), private

    def _masks(self, private):
        if type(private) is not bytes:
            raise ValueError('private key must be bytes')
        if self._private_cache is None or self._private_cache[0] != private:
            n = self.dimension
            digits = _unpack_dense(private, 2*n*n + n)
            masks = []
            for start, width in ((0, n-1), (n*n, n)):
                rows = tuple(bytes(digits[start+j*width:start+(j+1)*width]) for j in range(n))
                if width == n-1:
                    rows = tuple(bytes([int(j == 0)]) + row for j, row in enumerate(rows))
                inverse_rows = _matrix_inverse(rows)
                if inverse_rows is None:
                    raise ValueError('private affine mask is singular')
                offset_start = start + n*width
                masks.append(_Affine(rows, inverse_rows, tuple(digits[offset_start:offset_start+n])))
            self._private_cache = (private, tuple(masks), None)
        return self._private_cache[1]

    def _public_coefficients(self, public):
        if type(public) is not bytes:
            raise ValueError('public key must be bytes')
        if self._public_cache is None or self._public_cache[0] != public:
            n = self.dimension
            self._public_cache = (public, _unpack_dense(public, n*monomial_count(n)))
        return self._public_cache[1]

    def validate_public(self, public):
        self._public_coefficients(public)

    def public_from_private(self, private):
        left, right = self._masks(private)
        if self._private_cache[2] is not None:
            return self._private_cache[2]
        n, f = self.dimension, self.field
        # L(z)=offset + sum_i column_i*z_i. Frobenius fixes each input trit.
        linear = {(): f.from_coeffs(left.offset)}
        linear.update({(k,): f.from_coeffs(row[k] for row in left.rows) for k in range(n)})
        coefficients = {(): 1}
        for exponent in (0,) + self.indices:
            factor = {term: f.power(c, 3**exponent) for term, c in linear.items() if c}
            updated = {}
            for (t, c), (s, h) in product(coefficients.items(), factor.items()):
                term = tuple(sorted(t+s))
                if len(term) == 3 and term[0] == term[2]:
                    term = term[:1]  # z_i^3=z_i over the ternary field
                updated[term] = f.add(updated.get(term, 0), f.mul(c, h))
            coefficients = updated
        trits = bytearray()
        for term in _monomials(n):
            value = f.coeffs(coefficients.get(term, 0))
            trits.extend(_matvec(right.rows, value) if term else right.apply(value))
        public = _pack_dense(trits)
        self._private_cache = (private, (left, right), public)
        return public

    def forward(self, public, x):
        n = self.dimension
        _check_vector(x, n)
        coefficients = self._public_coefficients(public)
        output = [0] * n
        for index, term in enumerate(_monomials(n)):
            weight = 1
            for k in term:
                weight *= x[k]
            if weight:
                for j, value in enumerate(coefficients[index*n:(index+1)*n]):
                    output[j] += weight * value
        return tuple(value % 3 for value in output)

    def inverse(self, private, y):
        _check_vector(y, self.dimension)
        left, right = self._masks(private)
        f = self.field
        t = f.power(f.from_coeffs(right.undo(y)), self.inverse_exponent)
        return left.undo(f.coeffs(t))
