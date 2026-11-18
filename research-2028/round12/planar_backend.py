"""Masked Coulter–Matthews differential KEM experiment over F3.

Public evaluation needs only a coordinate coefficient string. Inversion
regenerates two affine masks and uses a field root computation. Correctness
and compact ciphertexts do not imply that recovering that root from public
data alone is hard. This reference has no security rating.
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from functools import lru_cache
from hashlib import shake_256
from itertools import combinations_with_replacement
from math import comb
import secrets

from field3 import Field3


def monomial_count(n):
    """Total-degree <= 3 reduced monomials, including the constant."""
    if type(n) is not int or n < 1:
        raise ValueError("positive dimension required")
    return comb(n + 3, 3) - n


def _monomials(n):
    for degree in range(4):
        for term in combinations_with_replacement(range(n), degree):
            # x_i^3 = x_i on F3; store the reduced representative.
            if degree != 3 or term[0] != term[2]:
                yield term


@lru_cache(maxsize=64)
def _power3(n):
    return 3 ** n


@lru_cache(maxsize=128)
def packed_width(n):
    """Exact ceil(log_256(3**n)) without constructing huge ranks for size reports."""
    if type(n) is not int or n < 1:
        raise ValueError("positive coefficient count required")
    if n < 4096:
        return ((_power3(n) - 1).bit_length() + 7) // 8
    with localcontext() as ctx:
        ctx.prec = len(str(n)) + 16
        while True:
            # Decimal.ln is correctly rounded to nearest. Enclose both logs
            # before outward-rounded multiplication and division.
            log3, log256 = Decimal(3).ln(), Decimal(256).ln()
            ctx.rounding = ROUND_FLOOR
            low = int((Decimal(n) * log3.next_minus()) / log256.next_plus())
            ctx.rounding = ROUND_CEILING
            high = int((Decimal(n) * log3.next_plus()) / log256.next_minus())
            if low == high:
                return low + 1  # 3**n cannot be a power of 256.
            ctx.prec += 16


def _pack_dense(trits):
    """Pack first trit most significant, splitting big-integer arithmetic."""
    def collect(start, stop):
        if stop - start <= 64:
            value = 0
            for i in range(start, stop):
                value = 3 * value + trits[i]
            return value
        mid = (start + stop) // 2
        return collect(start, mid) * _power3(stop - mid) + collect(mid, stop)

    return collect(0, len(trits)).to_bytes(packed_width(len(trits)), "big")


def _unpack_dense(encoded, trit_count):
    if type(encoded) is not bytes or len(encoded) != packed_width(trit_count):
        raise ValueError("noncanonical coefficient length")
    rank = int.from_bytes(encoded, "big")
    if rank >= _power3(trit_count):
        raise ValueError("unused coefficient rank")

    trits = bytearray(trit_count)

    def expand(value, start, stop):
        if stop - start <= 64:
            for i in range(stop - 1, start - 1, -1):
                value, trits[i] = divmod(value, 3)
            return
        mid = (start + stop) // 2
        left, right = divmod(value, _power3(stop - mid))
        expand(left, start, mid)
        expand(right, mid, stop)

    expand(rank, 0, trit_count)
    return trits


def _expand_rank(seed, label, n, attempt, limit):
    # Fixed-cost rank sampling with 128 slack bits, no claim of information-
    # theoretic uniformity for masks generated from a short seed and SHAKE.
    version = b"SG-DIFRA/R12/CM14/key-expansion/v1"
    framed = (version + bytes([len(label)]) + label + n.to_bytes(4, "big")
              + attempt.to_bytes(2, "big") + seed)
    width = ((limit - 1).bit_length() + 7) // 8 + 16
    return int.from_bytes(shake_256(framed).digest(width), "big") % limit


def _sample_trits(seed, label, n, attempt, count):
    width = packed_width(count)
    rank = _expand_rank(seed, label, n, attempt, _power3(count))
    return _unpack_dense(rank.to_bytes(width, "big"), count)


def _matrix_inverse(rows):
    n = len(rows)
    work = [list(row) + [int(i == j) for j in range(n)] for i, row in enumerate(rows)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if work[i][col]), None)
        if pivot is None:
            return None
        work[col], work[pivot] = work[pivot], work[col]
        if work[col][col] == 2:
            work[col] = [(2 * x) % 3 for x in work[col]]
        for i in range(n):
            if i != col and work[i][col]:
                factor = work[i][col]
                work[i] = [(x - factor*y) % 3 for x, y in zip(work[i], work[col])]
    return tuple(bytes(row[n:]) for row in work)


def _matvec(rows, x):
    return tuple(sum(a*b for a, b in zip(row, x)) % 3 for row in rows)


@dataclass(frozen=True)
class _Affine:
    rows: tuple
    inverse_rows: tuple
    offset: tuple

    def apply(self, x):
        return tuple((u + v) % 3 for u, v in zip(_matvec(self.rows, x), self.offset))

    def undo(self, y):
        return _matvec(self.inverse_rows, tuple((u-v) % 3 for u,v in zip(y, self.offset)))


def _make_affine(seed, label, n):
    offset = tuple(_sample_trits(seed, label+b"/offset", n, 0, n))
    # Bounded attempts make key generation total for every possible seed.
    for attempt in range(64):
        entries = _sample_trits(seed, label+b"/matrix", n, attempt, n*n)
        rows = tuple(bytes(entries[i:i+n]) for i in range(0, len(entries), n))
        inverse = _matrix_inverse(rows)
        if inverse is not None:
            return _Affine(rows, inverse, offset)
    identity = tuple(bytes(int(i == j) for j in range(n)) for i in range(n))
    return _Affine(identity, identity, offset)


class MaskedPlanarBackend:
    """Round 11 permutation backend. Keys contain coefficients or a private seed.

    Each instance caches at most one decoded public key and one expanded secret.
    Public parsing validates the coefficient encoding; the permutation theorem
    concerns honestly generated keys, not arbitrary strings of coefficients.
    """

    suite = b"SG-DIFRA/R12/masked-CM14/v1"

    def __init__(self, dimension):
        if type(dimension) is not int or dimension < 1 or dimension % 3 == 0:
            raise ValueError("CM14 requires a positive dimension coprime to 3")
        self.field = Field3(dimension)
        self.dimension = dimension
        self.seed_bytes = max(16, packed_width(dimension))
        self._secret = None
        self._public = None

    def generate(self):
        private = secrets.token_bytes(self.seed_bytes)
        return self.public_from_private(private), private

    def _expand_secret(self, private):
        if type(private) is not bytes or len(private) != self.seed_bytes:
            raise ValueError("noncanonical seed")
        if self._secret is None or self._secret[0] != private:
            n = self.dimension
            left = _make_affine(private, b"input", n)
            right = _make_affine(private, b"output", n)
            shift = 1 + _expand_rank(private, b"shift", n, 0, self.field.order - 1)
            self._secret = (private, left, right, shift, None)
        return self._secret

    def _secret_forward(self, data, x):
        _, left, right, shift, _ = data
        element = self.field.from_coeffs(left.apply(x))
        image = self.field.cm_forward(element, shift)
        return right.apply(self.field.coeffs(image))

    def _compile(self, data):
        # Newton interpolation on the lower set alpha_i<=2, sum(alpha)<=3.
        # Each coefficient uses at most eight lower-set evaluations. Convert
        # binom(x,2) to 2*x^2+x to emit ordinary reduced monomials.
        n = self.dimension
        terms = list(_monomials(n))
        index = {term: i for i, term in enumerate(terms)}
        values = []
        coefficients = bytearray(len(terms) * n)
        for i, term in enumerate(terms):
            point = [0] * n
            for variable in term:
                point[variable] += 1
            values.append(bytes(self._secret_forward(data, point)))
            differences = [0] * n
            for mask in range(1 << len(term)):
                subset = tuple(v for j, v in enumerate(term) if mask >> j & 1)
                sign = -1 if (len(term) - len(subset)) % 2 else 1
                probe = values[index[subset]]
                for j, value in enumerate(probe):
                    differences[j] += sign * value
            repeated = next((j for j in range(1,len(term)) if term[j-1] == term[j]), None)
            if repeated is None:
                adjustments = ((i, 1),)
            else:
                lower = term[:repeated] + term[repeated+1:]
                adjustments = ((i, 2), (index[lower], 1))
            for dest, scale in adjustments:
                for j, value in enumerate(differences):
                    k = dest * n + j
                    coefficients[k] = (coefficients[k] + scale*value) % 3
        return _pack_dense(coefficients)

    def public_from_private(self, private):
        data = self._expand_secret(private)
        if data[4] is None:
            data = (*data[:4], self._compile(data))
            self._secret = data
        return data[4]

    def _public_coefficients(self, public):
        if type(public) is not bytes:
            raise ValueError("public key must be bytes")
        if self._public is None or self._public[0] != public:
            count = monomial_count(self.dimension) * self.dimension
            self._public = (public, _unpack_dense(public, count))
        return self._public[1]

    def validate_public(self, encoded):
        self._public_coefficients(encoded)

    def _check_vector(self, vector):
        if len(vector) != self.dimension or any(type(t) is not int or t not in (0,1,2) for t in vector):
            raise ValueError("invalid ternary vector")

    def forward(self, public, x):
        self._check_vector(x)
        coefficients = self._public_coefficients(public)
        n = self.dimension
        output = [0] * n
        for i, term in enumerate(_monomials(n)):
            factor = 1
            for v in term:
                factor *= x[v]
            if factor:
                for j in range(n):
                    output[j] += factor * coefficients[n*i+j]
        return tuple(v % 3 for v in output)

    def inverse(self, private, y):
        self._check_vector(y)
        _, left, right, shift, _ = self._expand_secret(private)
        image = self.field.from_coeffs(right.undo(y))
        original = self.field.cm_inverse(image, shift)
        return left.undo(self.field.coeffs(original))
