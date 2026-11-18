"""Two quadratic triangular layers with real and known-rank middle maps.

This research fixture exposes only canonical quartic coordinate polynomials.
Real keys are permutations with efficient private inversion. The public
algebraic structure also determines the preimage in polynomial time. Use
small dimensions; dense public keys grow as a polynomial of degree five.
"""

from collections import Counter
from dataclasses import dataclass
from itertools import combinations, combinations_with_replacement, product
from math import comb
import secrets

from planar_backend import _matrix_inverse, _matvec, _pack_dense, _unpack_dense


def public_monomials(n):
    """Display order is degree first, then lexicographic repeated indices."""
    if type(n) is not int or n <= 0:
        raise ValueError("dimension must be a positive integer")
    return tuple(term for degree in range(5)
                 for term in combinations_with_replacement(range(n), degree)
                 if all(term[i] != term[i + 2] for i in range(len(term) - 2)))


def _trits(count):
    return tuple(secrets.randbelow(3) for _ in range(count))


def _uniform_invertible(n):
    while True:
        rows = tuple(_trits(n) for _ in range(n))
        if _matrix_inverse(rows) is not None:
            return rows


def _add(left, right, sign=1):
    return tuple((a + sign*b) % 3 for a, b in zip(left, right))


def _quadratic(coefficients, values):
    pairs = combinations_with_replacement(range(len(values)), 2)
    return sum(c * values[i] * values[j] for c, (i, j) in zip(coefficients, pairs)) % 3


def _triangle(layer, x, undo=False):
    result = []
    for j, coefficients in enumerate(layer):
        prefix = result if undo else x[:j]
        offset = _quadratic(coefficients, prefix)
        result.append((x[j] - offset if undo else x[j] + offset) % 3)
    return tuple(result)


@dataclass(frozen=True)
class _Layers:
    A: tuple
    a: tuple
    first: tuple
    M: tuple
    d: tuple
    second: tuple
    B: tuple
    b: tuple

    def forward(self, x):
        z = _add(_matvec(self.A, x), self.a)
        middle = _add(_matvec(self.M, _triangle(self.first, z)), self.d)
        return _add(_matvec(self.B, _triangle(self.second, middle)), self.b)

    def encode(self):
        stream = []
        for matrix, offset, triangle in (
            (self.A, self.a, self.first), (self.M, self.d, self.second), (self.B, self.b, ())
        ):
            stream.extend(t for row in matrix for t in row)
            stream.extend(offset)
            stream.extend(t for row in triangle for t in row)
        return _pack_dense(stream)


def _random_layer(n):
    return tuple(_trits(j*(j+1)//2) for j in range(n))


def _sample_layers(n, rank):
    if rank == n:
        middle = _uniform_invertible(n)
    else:
        left, right = _uniform_invertible(n), _uniform_invertible(n)
        # U diag(I_rank,0) V is uniform on all exact-rank matrices.
        middle = tuple(tuple(sum(left[i][k] * right[k][j] for k in range(rank)) % 3
                             for j in range(n)) for i in range(n))
    return _Layers(_uniform_invertible(n), _trits(n), _random_layer(n), middle, _trits(n),
                   _random_layer(n), _uniform_invertible(n), _trits(n))


def _read_layers(n, private):
    size = 3*n*n + 3*n + 2*comb(n+1, 3)
    stream = iter(_unpack_dense(private, size))
    def take(count):
        return tuple(next(stream) for _ in range(count))
    def matrix():
        return tuple(take(n) for _ in range(n))
    def triangle():
        return tuple(take(j*(j+1)//2) for j in range(n))
    return _Layers(matrix(), take(n), triangle(), matrix(), take(n), triangle(), matrix(), take(n))


def _inverse_matrices(layers):
    matrices = tuple(_matrix_inverse(M) for M in (layers.A, layers.M, layers.B))
    if any(M is None for M in matrices):
        raise ValueError("invalid private permutation key: singular matrix")
    return matrices


def _function_coefficients(layers, n):
    """Exact degree-four interpolation on lower-set points in F3^n.

    For exponent alpha_i<=2, Delta^alpha f(0) multiplies the Newton basis
    product of binomial(X_i,alpha_i). Expanding binomial(X,2)=X+2X² on F3
    returns ordinary reduced monomial coefficients in the published order.
    """
    terms = public_monomials(n)
    index = {term: i for i, term in enumerate(terms)}
    rows = [bytearray(len(terms)) for _ in range(n)]
    samples = {}
    for term in terms:
        point = [0] * n
        for i in term:
            point[i] += 1
        samples[term] = layers.forward(tuple(point))
        difference = [0] * n
        for size in range(len(term) + 1):
            sign = (-1)**(len(term)-size)
            for subset in combinations(term, size):
                for j, value in enumerate(samples[subset]):
                    difference[j] += sign * value
        # Each repeated digit contributes either X or 2X². Single
        # occurrences contribute only X. The empty term contributes one.
        factors = [((i,), (i, i)) if count == 2 else ((i,),)
                   for i, count in Counter(term).items()]
        for choice in product(*factors):
            monomial = tuple(i for factor in choice for i in factor)
            scale = 2**sum(len(factor) == 2 for factor in choice)
            column = index[monomial]
            for row, value in zip(rows, difference):
                row[column] = (row[column] + scale*value) % 3
    return _pack_dense(b"".join(rows))


@dataclass(frozen=True)
class TwoLayerBackend:
    """Round 11-compatible real-key backend and experimental lossy-key sampler.

    The real public key, as well as every lossy public key, contains only
    coefficient data. The separate suite does not carry a mode flag.
    """
    dimension: int
    suite = b"SG-DIFRA/R12/two-triangular-layers/v1"

    def __post_init__(self):
        if type(self.dimension) is not int or not 1 <= self.dimension < 2**64:
            raise ValueError("dimension must fit a positive uint64")

    @property
    def public_coefficient_count(self):
        n = self.dimension
        return n*(comb(n+4, 4) - n*(n+1))

    def generate(self):
        layers = _sample_layers(self.dimension, self.dimension)
        return _function_coefficients(layers, self.dimension), layers.encode()

    def sample_lossy(self, rank):
        if type(rank) is not int or not 0 <= rank < self.dimension:
            raise ValueError("lossy rank must be nonnegative and below dimension")
        return _function_coefficients(_sample_layers(self.dimension, rank), self.dimension)

    def public_from_private(self, private):
        layers = _read_layers(self.dimension, private)
        _inverse_matrices(layers)
        return _function_coefficients(layers, self.dimension)

    def validate_public(self, public):
        # Canonical syntax only. Validly encoded lossy maps must also parse.
        _unpack_dense(public, self.public_coefficient_count)

    def forward(self, public, x):
        n = self.dimension
        if len(x) != n or any(type(t) is not int or not 0 <= t < 3 for t in x):
            raise ValueError("invalid ternary vector")
        coefficients = _unpack_dense(public, self.public_coefficient_count)
        values = []
        for term in public_monomials(n):
            value = 1
            for i in term:
                value *= x[i]
            values.append(value % 3)
        width = len(values)
        return tuple(sum(a*b for a,b in zip(coefficients[j*width:(j+1)*width], values)) % 3
                     for j in range(n))

    def inverse(self, private, y):
        n = self.dimension
        if len(y) != n or any(type(t) is not int or not 0 <= t < 3 for t in y):
            raise ValueError("invalid ternary vector")
        layers = _read_layers(n, private)
        ai, mi, bi = _inverse_matrices(layers)
        t = _matvec(bi, _add(y, layers.b, -1))
        t = _triangle(layers.second, t, undo=True)
        t = _matvec(mi, _add(t, layers.d, -1))
        t = _triangle(layers.first, t, undo=True)
        return _matvec(ai, _add(t, layers.a, -1))
