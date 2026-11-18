"""Native research KEM with canonical ternary cosets on the ciphertext wire."""
from copy import copy
from hmac import compare_digest
from pathlib import Path
import secrets
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round16"))
from matched_kem import MatchedKEM
from projected_kem import (_COINS, _KEY, _SEED_BYTES, _hash, _pack_dense,
                           _signed_subset, _unpack_dense, packed_width)


def _eliminate(word, pivot, row):
    multiplier = word[pivot]
    if multiplier:
        for i in range(pivot, len(word)):
            word[i] = (word[i] - multiplier * row[i]) % 3


class RowQuotient:
    """Represent a coset by zeroing pivot coordinates of a public echelon basis."""

    def __init__(self, width, rows):
        basis = {}
        for row in rows:
            word = bytearray(row)
            if len(word) != width or any(v >= 3 for v in word):
                raise ValueError("expected a ternary matrix with the indicated width")
            for pivot in sorted(basis):
                _eliminate(word, pivot, basis[pivot])
            lead = next((i for i, entry in enumerate(word) if entry), None)
            if lead is not None:
                if word[lead] == 2:
                    word = bytearray((2 * v) % 3 for v in word)
                basis[lead] = word
        self.width = width
        self.basis = sorted(basis.items())
        self.free = [i for i in range(width) if i not in basis]

    def project(self, word):
        if len(word) != self.width:
            raise ValueError("wrong coset input width")
        representative = bytearray(word)
        for pivot, row in self.basis:
            _eliminate(representative, pivot, row)
        return bytearray(representative[i] for i in self.free)

    def lift(self, remainder):
        if len(remainder) != len(self.free):
            raise ValueError("wrong coset coordinate count")
        word = bytearray(self.width)
        for i, value in zip(self.free, remainder):
            word[i] = value
        return word


class QuotientKEM:
    """Wrap a matched full- or reduced-radius layout in a distinct hash suite."""

    def __init__(self, base, *, nonce_bytes=None):
        if not isinstance(base, MatchedKEM):
            raise TypeError("expected a matched SG-DIFRA layout")
        if nonce_bytes is None:
            nonce_bytes = base.nonce_bytes
        if type(nonce_bytes) is not int or not 0 <= nonce_bytes < 2**64:
            raise ValueError("nonce width must fit an unsigned 64-bit integer")
        self.nonce_bytes = nonce_bytes
        self.base = copy(base)
        self.base.suite = (b"SG-DIFRA/R17/row-quotient/v1"
                           + nonce_bytes.to_bytes(8, "big") + base.suite)
        self.public_bytes = base.public_bytes
        self.private_bytes = base.private_bytes
        self.key_bytes = base.key_bytes
        self.full_rank_ciphertext_bytes = self.nonce_bytes + packed_width(base.N - base.source.d)

    def keygen(self):
        return self.base.keygen()

    def _space(self, public):
        base = self.base
        if type(public) is not bytes or len(public) != self.public_bytes:
            raise ValueError("invalid public key")
        seed = public[:_SEED_BYTES]

        def rows():
            offset = _SEED_BYTES
            for first, count in base._blocks():
                end = offset + packed_width(count * base.t)
                suffix = _unpack_dense(public[offset:end], count * base.t)
                for j in range(count):
                    yield base._row(seed, first + j) + suffix[j * base.t:(j + 1) * base.t]
                offset = end

        return RowQuotient(base.N, rows())

    def ciphertext_bytes_for(self, public):
        return self.nonce_bytes + packed_width(len(self._space(public).free))

    def _ciphertext(self, public, space, message):
        base = self.base
        params = base.source
        tape = _hash(_COINS, base.suite, public, message, self.nonce_bytes + params.coin_bytes)
        joint_rank = int.from_bytes(tape[self.nonce_bytes:], "big") % params.coin_count
        error = _signed_subset(params.N, params.z, joint_rank % params.noise_count)
        word = bytearray(base.m)
        word.extend(base._outer.encode(int.from_bytes(message, "big")))
        for i, sign in error:
            if i < base.N:
                word[i] = (word[i] + sign) % 3
        return tape[:self.nonce_bytes] + _pack_dense(space.project(word))

    def encaps(self, public):
        space = self._space(public)
        p = self.base.source
        message = secrets.randbits(p.bits).to_bytes(p.message_bytes, "big")
        ciphertext = self._ciphertext(public, space, message)
        return ciphertext, _hash(_KEY, self.base.suite, public, message, self.key_bytes)

    def decaps(self, private, ciphertext):
        base = self.base
        if type(private) is not bytes or len(private) != self.private_bytes:
            raise ValueError("invalid private key")
        if type(ciphertext) is not bytes or not (
            self.full_rank_ciphertext_bytes <= len(ciphertext) <= self.nonce_bytes + base.body_bytes
        ):
            return None
        checks = base._checks(private[_SEED_BYTES:])
        public = base._public(private[:_SEED_BYTES], checks)
        space = self._space(public)
        try:
            remainder = _unpack_dense(ciphertext[self.nonce_bytes:], len(space.free))
        except ValueError:
            return None
        word = space.lift(remainder)
        residual = [(word[base.m + j] - sum(sign * word[i] for i, sign in check)) % 3
                    for j, check in enumerate(checks)]
        integer = base._outer.decode(residual)
        if integer is None:
            return None
        message = integer.to_bytes(base.source.message_bytes, "big")
        if not compare_digest(ciphertext, self._ciphertext(public, space, message)):
            return None
        return _hash(_KEY, base.suite, public, message, self.key_bytes)


def registered_options(target, full_radius):
    """Select an underlying layout and enough nonce bits for its spread target."""
    from spread import quotient_body_spread
    from matched_kem import research_profile as full
    from outer_kem import research_profile as shortened

    base = full(target) if full_radius else shortened(target)
    p = base.source
    body_bits = quotient_body_spread(p.N, base.N, p.d, p.w, p.slack)
    nonce_bytes = max(0, (8 * base.nonce_bytes - body_bits + 7) // 8)
    return base, nonce_bytes


def research_profile(target, *, full_radius=False):
    """Quotient profile using enough nonce bits to retain the old spread bound."""
    base, nonce_bytes = registered_options(target, full_radius)
    return QuotientKEM(base, nonce_bytes=nonce_bytes)
