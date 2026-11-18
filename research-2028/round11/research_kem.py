"""Research harness for a hashed permutation on fixed-width ternary vectors.

The only bundled backend is an intentionally public-invertible correctness
control. It provides no confidentiality. There is no default backend. The ROM
proof assumes a one-way permutation backend and an ideal hash. This Python
implementation uses SHAKE256 for reproducible evaluation, not for a proof
that SHAKE256 is an ideal oracle.
"""

from dataclasses import dataclass, field
from hashlib import shake_256
import secrets
from typing import Protocol


Trits = tuple[int, ...]
SHARED_KEY_BYTES = 32
KDF_DOMAIN = b"SG-DIFRA/R11/hashed-permutation-kem/v1"


def _domain_size(dimension: int) -> int:
    if type(dimension) is not int or dimension < 1:
        raise ValueError("dimension must be a positive integer")
    return 3 ** dimension


def ternary_bytes(dimension: int) -> int:
    """Shortest fixed byte length sufficient for every vector of this dimension."""
    return ((_domain_size(dimension) - 1).bit_length() + 7) // 8


def _validate_vector(trits: Trits, dimension: int) -> None:
    if len(trits) != dimension or any(type(t) is not int or t not in (0, 1, 2) for t in trits):
        raise ValueError("invalid ternary vector")


def pack(trits: Trits) -> bytes:
    """Encode the first trit as the most significant base-three digit."""
    width = ternary_bytes(len(trits))
    _validate_vector(trits, len(trits))
    rank = 0
    for digit in trits:
        rank = 3 * rank + digit
    return rank.to_bytes(width, "big")


def _digits(rank: int, dimension: int) -> Trits:
    result = [0] * dimension
    for index in range(dimension - 1, -1, -1):
        rank, result[index] = divmod(rank, 3)
    return tuple(result)


def unpack(encoded: bytes, dimension: int) -> Trits:
    """Reject aliases, including leading extension bytes and unused ranks."""
    if type(encoded) is not bytes or len(encoded) != ternary_bytes(dimension):
        raise ValueError("wrong ternary encoding type or length")
    rank = int.from_bytes(encoded, "big")
    if rank >= _domain_size(dimension):
        raise ValueError("rank outside ternary domain")
    return _digits(rank, dimension)


def _sample_vector(dimension: int) -> Trits:
    # A uniform rank induces independent uniform trits; randbelow uses rejection.
    size = _domain_size(dimension)
    return _digits(secrets.randbelow(size), dimension)


@dataclass(frozen=True)
class PublicKey:
    suite: bytes
    dimension: int
    encoded: bytes


@dataclass(frozen=True)
class PrivateKey:
    suite: bytes
    dimension: int
    encoded: bytes = field(repr=False)


class PermutationBackend(Protocol):
    """Contract for an explicitly selected backend.

    generate emits canonical binary encodings of matching keys. A valid public
    key defines a bijection of the whole ternary domain, not just a typical
    subset. public_from_private must recover the exact public encoding. Key
    validation, including canonical parsing, belongs to the backend. A security
    argument must establish average-case one-wayness separately.
    """

    @property
    def dimension(self) -> int: ...

    @property
    def suite(self) -> bytes: ...

    def generate(self) -> tuple[bytes, bytes]: ...
    def validate_public(self, encoded: bytes) -> None: ...
    def public_from_private(self, encoded: bytes) -> bytes: ...
    def forward(self, public: bytes, x: Trits) -> Trits: ...
    def inverse(self, private: bytes, y: Trits) -> Trits: ...


def _derive_key(suite: bytes, dimension: int, public: bytes, x: Trits) -> bytes:
    kdf = shake_256()
    for item in (KDF_DOMAIN, suite, dimension.to_bytes(8, "big"), public, pack(x)):
        kdf.update(len(item).to_bytes(8, "big"))
        kdf.update(item)
    return kdf.digest(SHARED_KEY_BYTES)


class ResearchKEM:
    """KeyGen, Encaps and Decaps for research; suite and dimension are out-of-band."""

    def __init__(self, backend: PermutationBackend):
        if type(backend.suite) is not bytes or not backend.suite:
            raise ValueError("a nonempty byte suite identifier is required")
        if type(backend.dimension) is not int or not 1 <= backend.dimension < 2**64:
            raise ValueError("dimension must fit as a positive uint64")
        self.backend = backend

    def keygen(self) -> tuple[PublicKey, PrivateKey]:
        b = self.backend
        public, private = b.generate()
        b.validate_public(public)
        if b.public_from_private(private) != public:
            raise ValueError("backend generated mismatched keys")
        return PublicKey(b.suite, b.dimension, public), PrivateKey(b.suite, b.dimension, private)

    def encaps(self, key: PublicKey) -> tuple[bytes, bytes]:
        b = self.backend
        if not isinstance(key, PublicKey) or (key.suite, key.dimension) != (b.suite, b.dimension):
            raise ValueError("public key type, suite or dimension mismatch")
        b.validate_public(key.encoded)
        x = _sample_vector(b.dimension)
        y = b.forward(key.encoded, x)
        if len(y) != b.dimension:
            raise ValueError("backend returned wrong output dimension")
        return pack(y), _derive_key(b.suite, b.dimension, key.encoded, x)

    def decaps(self, key: PrivateKey, ciphertext: bytes) -> bytes | None:
        b = self.backend
        if not isinstance(key, PrivateKey) or (key.suite, key.dimension) != (b.suite, b.dimension):
            raise ValueError("private key type, suite or dimension mismatch")
        public = b.public_from_private(key.encoded)
        try:
            y = unpack(ciphertext, b.dimension)
        except ValueError:
            return None
        x = b.inverse(key.encoded, y)
        if len(x) != b.dimension:
            raise ValueError("backend returned wrong preimage dimension")
        return _derive_key(b.suite, b.dimension, public, x)


@dataclass(frozen=True)
class PublicShearControl:
    """Negative control with one cubic term in a finite-difference potential.

    At zero-based index 2, F(x) adds x[0]*x[1] to x[2], and then every
    coordinate is translated by its public trit b[i]. The inverse translation
    -b is just as public as b. A receiver holding -b therefore illustrates a
    fast decoder, but the receiver has no computational advantage.
    """

    dimension: int

    @property
    def suite(self) -> bytes:
        return b"SG-DIFRA/R11/public-shear-control/v1"

    def __post_init__(self):
        if type(self.dimension) is not int or self.dimension < 3:
            raise ValueError("the control needs at least three coordinates")

    def generate(self) -> tuple[bytes, bytes]:
        b = _sample_vector(self.dimension)
        return pack(b), pack(tuple(-t % 3 for t in b))

    def validate_public(self, encoded: bytes) -> None:
        unpack(encoded, self.dimension)

    def public_from_private(self, encoded: bytes) -> bytes:
        minus_b = unpack(encoded, self.dimension)
        return pack(tuple(-t % 3 for t in minus_b))

    def forward(self, public: bytes, x: Trits) -> Trits:
        b = unpack(public, self.dimension)
        _validate_vector(x, self.dimension)
        y = [(xi + bi) % 3 for xi, bi in zip(x, b)]
        y[2] = (y[2] + x[0] * x[1]) % 3
        return tuple(y)

    def inverse(self, private: bytes, y: Trits) -> Trits:
        minus_b = unpack(private, self.dimension)
        _validate_vector(y, self.dimension)
        x = [(yi + di) % 3 for yi, di in zip(y, minus_b)]
        x[2] = (x[2] - x[0] * x[1]) % 3
        return tuple(x)
