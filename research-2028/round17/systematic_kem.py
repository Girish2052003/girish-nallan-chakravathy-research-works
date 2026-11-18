"""Standalone ternary quotient KEM with an explicit identity pivot block."""
from functools import cached_property
from hmac import compare_digest
from pathlib import Path
import secrets
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round16"))
from quotient_kem import QuotientKEM
from projected_kem import (_COINS, _KEY, _MATRIX, _ROWS_PER_BLOCK, _SEED_BYTES,
                           _hash, _pack_dense, _signed_subset, _unpack_dense,
                           packed_width)


class SystematicKEM(QuotientKEM):
    """Send one fixed-width coset representative; expand only needed mask rows."""

    def __init__(self, base, *, nonce_bytes=None):
        super().__init__(base, nonce_bytes=nonce_bytes)
        self.base.suite = b"SG-DIFRA/R17/systematic-quotient-seed-context/v1" + self.base.suite
        self.tail = base.m - base.source.d
        self.ciphertext_bytes = self.full_rank_ciphertext_bytes
        self._row_width = packed_width(self.tail)
        self._block_width = packed_width(_ROWS_PER_BLOCK * base.t)

    @cached_property
    def _tail_count(self):
        return 3**self.tail

    def _tail_row(self, seed, i):
        raw = _hash(_MATRIX, self.base.suite, seed, i.to_bytes(8, "big"),
                    self._row_width + self.base.slack_bytes)
        rank = int.from_bytes(raw, "big") % self._tail_count
        return _unpack_dense(rank.to_bytes(self._row_width, "big"), self.tail)

    def _check_row(self, i, tail, checks):
        d = self.base.source.d
        # A_i has a single 1 at i among the first d entries, then the public tail.
        result = []
        for check in checks:
            value = 0
            for pos, sign in check:
                if pos == i:
                    value += sign
                elif pos >= d:
                    value += sign * tail[pos - d]
            result.append(value % 3)
        return result

    def _public(self, seed, checks):
        output = bytearray(seed)
        for first, count in self.base._blocks():
            block = bytearray()
            for i in range(first, first + count):
                block.extend(self._check_row(i, self._tail_row(seed, i), checks))
            output.extend(_pack_dense(block))
        return bytes(output)

    def keygen(self):
        seed = secrets.token_bytes(_SEED_BYTES)
        private_seed = secrets.token_bytes(self.base.seed_bytes)
        checks = self.base._checks(private_seed)
        return self._public(seed, checks), seed + private_seed

    def _public_checks(self, public):
        if type(public) is not bytes or len(public) != self.public_bytes:
            raise ValueError("invalid public key")
        # For one honest recipient the public key has canonical blocks. On input
        # from a caller validate even blocks the current sender would skip.
        t = self.base.t
        modulus = {}
        for first, count in self.base._blocks():
            width = self._block_width if count == _ROWS_PER_BLOCK else packed_width(count*t)
            start = _SEED_BYTES + (first // _ROWS_PER_BLOCK) * self._block_width
            if count not in modulus:
                modulus[count] = 3**(count*t)
            if int.from_bytes(public[start:start + width], "big") >= modulus[count]:
                raise ValueError("unused public-key block rank")

        last_block = None
        data = None

        def row(i, tail):
            nonlocal last_block, data
            block, offset = divmod(i, _ROWS_PER_BLOCK)
            if block != last_block:
                count = min(_ROWS_PER_BLOCK, self.base.source.d - block * _ROWS_PER_BLOCK)
                width = self._block_width if count == _ROWS_PER_BLOCK else packed_width(count*t)
                start = _SEED_BYTES + block * self._block_width
                data = _unpack_dense(public[start:start + width], count*t)
                last_block = block
            return data[offset*t:(offset+1)*t]

        return row

    def ciphertext_bytes_for(self, public):
        self._public_checks(public)
        return self.ciphertext_bytes

    def _encode(self, seed, message, check_row):
        base = self.base
        p = base.source
        tape = _hash(_COINS, base.suite, seed, message, self.nonce_bytes + p.coin_bytes)
        rank = int.from_bytes(tape[self.nonce_bytes:], "big") % p.coin_count
        error = _signed_subset(p.N, p.z, rank % p.noise_count)
        remainder = bytearray(self.tail)
        remainder.extend(base._outer.encode(int.from_bytes(message, "big")))
        for i, sign in error:
            if i < p.d:
                row = self._tail_row(seed, i)
                for j, a in enumerate(row):
                    remainder[j] = (remainder[j] - sign*a) % 3
                for j, a in enumerate(check_row(i, row)):
                    pos = self.tail + j
                    remainder[pos] = (remainder[pos] - sign*a) % 3
            elif i < base.N:
                remainder[i - p.d] = (remainder[i - p.d] + sign) % 3
        return tape[:self.nonce_bytes] + _pack_dense(remainder)

    def encaps(self, public):
        base = self.base
        check_row = self._public_checks(public)
        message = secrets.randbits(base.source.bits).to_bytes(base.source.message_bytes, "big")
        seed = public[:_SEED_BYTES]
        return self._encode(seed, message, check_row), _hash(_KEY, base.suite, seed, message, self.key_bytes)

    def decaps(self, private, ciphertext):
        base = self.base
        if type(private) is not bytes or len(private) != self.private_bytes:
            raise ValueError("invalid private key")
        if type(ciphertext) is not bytes or len(ciphertext) != self.ciphertext_bytes:
            return None
        d = base.source.d
        try:
            remainder = _unpack_dense(ciphertext[self.nonce_bytes:], self.tail + base.t)
        except ValueError:
            return None
        seed = private[:_SEED_BYTES]
        checks = base._checks(private[_SEED_BYTES:])
        # The canonical lift is zero throughout its first d coordinates.
        residual = [(remainder[self.tail+j] - sum(sign*remainder[pos-d]
                     for pos, sign in check if pos >= d)) % 3 for j, check in enumerate(checks)]
        integer = base._outer.decode(residual)
        if integer is None:
            return None
        message = integer.to_bytes(base.source.message_bytes, "big")
        replay = self._encode(seed, message, lambda i, row: self._check_row(i, row, checks))
        if not compare_digest(ciphertext, replay):
            return None
        return _hash(_KEY, base.suite, seed, message, self.key_bytes)


def research_profile(target, *, full_radius=False):
    """Primary registered layout with the previous spread target and fixed widths."""
    from quotient_kem import registered_options
    base, nonce_bytes = registered_options(target, full_radius)
    return SystematicKEM(base, nonce_bytes=nonce_bytes)
