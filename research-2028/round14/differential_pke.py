"""Reference ternary differential PKE with private disjoint parity checks.

This implements exact honest decryption and the samplers in BASE_PROOF.md. Its
computational security depends on the stated decoding assumptions. The code is
variable time; the large illustrative layouts are arithmetic size estimates.
"""
from dataclasses import dataclass
from functools import cached_property
from math import comb
from pathlib import Path
import secrets
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round12"))
from planar_backend import _pack_dense, _unpack_dense, packed_width
from parameters import mixed_rank_bytes, support_bytes


def _width(count):
    """Bytes for a zero-based rank in a set of cardinality count."""
    return ((count - 1).bit_length() + 7) // 8


@dataclass(frozen=True)
class Params:
    bits: int
    h: int
    n: int
    m: int
    w: int
    z: int
    slack: int = 128
    outer: str = 'repeat'

    def __post_init__(self):
        positive = (self.bits, self.h, self.n, self.m, self.w)
        if any(type(v) is not int or not 0 < v < 2**64 for v in positive):
            raise ValueError("bits, h, n, m, w must be positive uint64 integers")
        if any(type(v) is not int or not 0 <= v < 2**64 for v in (self.z, self.slack)):
            raise ValueError("z and slack must be nonnegative uint64 integers")
        if self.outer not in ('repeat', 'rs'):
            raise ValueError('unknown outer code')
        if self.t * self.w > self.m:
            raise ValueError("not enough base coordinates for the disjoint checks")

    @property
    def t(self):
        if self.outer == "rs":
            from outer_code import rs_shape
            return rs_shape(self.bits, self.z)[3]
        return self.bits * (2 * self.z + 1)

    @property
    def d(self):
        return self.h + self.n * (self.n + 1) // 2

    @property
    def N(self):
        return self.m + self.t

    @property
    def message_bytes(self):
        return (self.bits + 7) // 8

    @cached_property
    def public_bytes(self):
        return packed_width(self.d * self.N)

    @cached_property
    def body_bytes(self):
        return packed_width(self.N)

    @cached_property
    def private_bytes(self):
        return support_bytes(self.m, self.w, self.t)

    @cached_property
    def noise_count(self):
        return comb(self.N, self.z) << self.z

    @cached_property
    def coin_count(self):
        return 3**(self.h + self.n) * self.noise_count

    @cached_property
    def coin_bytes(self):
        return mixed_rank_bytes(self.h + self.n, self.noise_count) + (self.slack + 7) // 8


def _colex_positions(length, weight, rank):
    """Unrank an increasing weight-subset, rank=sum_j C(position_j,j+1)."""
    positions = [0] * weight
    ceiling = length
    for k in range(weight, 0, -1):
        low, high = k - 1, ceiling
        while high - low > 1:
            mid = (low + high) // 2
            if comb(mid, k) <= rank:
                low = mid
            else:
                high = mid
        positions[k - 1] = low
        rank -= comb(low, k)
        ceiling = low
    return positions


def _signed_subset(length, weight, rank):
    subset, signs = divmod(rank, 1 << weight)
    return tuple((index, 1 - 2 * ((signs >> j) & 1))
                 for j, index in enumerate(_colex_positions(length, weight, subset)))


class _UnusedPositions:
    """Order statistics of still unused positions; tree positions are 1-based."""
    def __init__(self, size):
        self.size = size
        self.tree = [i & -i for i in range(size + 1)]

    def select(self, rank):
        position = 0
        step = 1 << (self.size.bit_length() - 1)
        while step:
            probe = position + step
            if probe <= self.size and self.tree[probe] <= rank:
                rank -= self.tree[probe]
                position = probe
            step >>= 1
        return position

    def remove(self, position):
        i = position + 1
        while i <= self.size:
            self.tree[i] -= 1
            i += i & -i


class DifferentialPKE:
    def __init__(self, params):
        if not isinstance(params, Params):
            raise TypeError("expected Params")
        self.params = params

    @cached_property
    def _rs(self):
        from outer_code import RSOuter
        return RSOuter(self.params.bits, self.params.z)

    def _encode_message(self, message):
        p = self.params
        if p.outer == "rs":
            return self._rs.encode(message)
        word = []
        for j in reversed(range(p.bits)):
            word.extend([(message >> j) & 1] * (2*p.z + 1))
        return word

    def _decode_message(self, residuals):
        p = self.params
        if p.outer == "rs":
            return self._rs.decode(residuals)
        repeats = 2*p.z + 1
        message = 0
        for start in range(0, p.t, repeats):
            block = residuals[start:start + repeats]
            if block.count(0) > p.z:
                bit = 0
            elif block.count(1) > p.z:
                bit = 1
            else:
                return None
            message = 2*message + bit
        return message

    def _private_checks(self, encoded):
        p = self.params
        if type(encoded) is not bytes or len(encoded) != p.private_bytes:
            raise ValueError("invalid private key width")
        available = _UnusedPositions(p.m)
        checks = []
        offset = 0
        for j in range(p.t):
            length = p.m - j * p.w
            count = comb(length, p.w) << p.w
            width = _width(count)
            rank = int.from_bytes(encoded[offset:offset + width], "big")
            offset += width
            if rank >= count:
                raise ValueError("unused private key rank")
            check = tuple((available.select(pos), sign)
                          for pos, sign in _signed_subset(length, p.w, rank))
            for index, _ in check:
                available.remove(index)
            checks.append(check)
        return tuple(checks)

    def validate_private(self, encoded):
        self._private_checks(encoded)

    def validate_public(self, encoded):
        _unpack_dense(encoded, self.params.d * self.params.N)

    def sample_private(self):
        """Sample exact, uniformly signed disjoint supports in canonical wire form."""
        p = self.params
        private = bytearray()
        for j in range(p.t):
            count = comb(p.m - j * p.w, p.w) << p.w
            private.extend(secrets.randbelow(count).to_bytes(_width(count), "big"))
        return bytes(private)

    def keygen(self):
        p = self.params
        sk = self.sample_private()
        checks = self._private_checks(sk)
        public = bytearray()
        row_count = 3**p.m
        for _ in range(p.d):
            rank = secrets.randbelow(row_count)
            row = _unpack_dense(rank.to_bytes(packed_width(p.m), "big"), p.m)
            public.extend(row)
            public.extend(sum(row[i] * sign for i, sign in support) % 3
                          for support in checks)
        return _pack_dense(public), sk

    def encrypt(self, pk, msg, coin_bytes):
        p = self.params
        if type(msg) is not bytes or len(msg) != p.message_bytes:
            raise ValueError("invalid message length")
        message = int.from_bytes(msg, "big")
        if message >= 1 << p.bits:
            raise ValueError("unused high message bits")
        if type(coin_bytes) is not bytes or len(coin_bytes) != p.coin_bytes:
            raise ValueError("invalid coin tape")
        matrix = _unpack_dense(pk, p.d * p.N)
        rank = int.from_bytes(coin_bytes, "big") % p.coin_count
        input_rank, noise_rank = divmod(rank, p.noise_count)
        trits = _unpack_dense(input_rank.to_bytes(packed_width(p.h+p.n), "big"), p.h+p.n)
        x = trits[p.h:]
        features = list(trits[:p.h])
        features.extend((a*x[j]) % 3 for i, a in enumerate(x) for j in range(i, p.n))
        target = [0] * p.m + list(self._encode_message(message))
        for i, feature in enumerate(features):
            if feature:
                offset = i * p.N
                for j in range(p.N):
                    target[j] += feature * matrix[offset + j]
        for index, sign in _signed_subset(p.N, p.z, noise_rank):
            target[index] += sign
        return _pack_dense([value % 3 for value in target])

    def decrypt(self, sk, body):
        p = self.params
        checks = self._private_checks(sk)
        try:
            word = _unpack_dense(body, p.N)
        except ValueError:
            return None
        residuals = tuple((word[p.m + j] - sum(sign * word[i] for i, sign in check)) % 3
                          for j, check in enumerate(checks))
        message = self._decode_message(residuals)
        if message is None or not 0 <= message < 1 << p.bits:
            return None
        return message.to_bytes(p.message_bytes, "big")
