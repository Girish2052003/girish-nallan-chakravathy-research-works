"""Single-user seeded public matrix encoding in a separate ideal-oracle domain."""
import secrets

from differential_kem import DifferentialKEM, _hash
from differential_pke import _pack_dense, _unpack_dense, packed_width
from matrix_setup import SharedMatrixKEM


_PROFILE = b"SG-DIFRA/R14/seeded-matrix/v1"
_MATRIX = b"SG-DIFRA/R14/seeded-matrix/row/v1"
_SEED_BYTES = 32


class SeededMatrixKEM:
    """Publish seed || syndromes and retain seed || signed supports.

    This is a distinct cryptographic suite. The logical full public matrix and
    the seed both enter FO hashing. Expansion uses one tagged SHAKE256 call per
    row. The single-user proof models that role by a third independent oracle.
    """
    key_bytes = DifferentialKEM.key_bytes

    def __init__(self, params, nonce_bytes=32, matrix_slack=None):
        if matrix_slack is None:
            matrix_slack = params.bits + 64
        if type(matrix_slack) is not int or not 0 <= matrix_slack < 2**64:
            raise ValueError("invalid matrix sampling slack")
        template = DifferentialKEM(params, nonce_bytes)
        self.params = params
        self.nonce_bytes = nonce_bytes
        self.matrix_slack = matrix_slack
        self.suite = (_PROFILE + len(template.suite).to_bytes(8, "big") + template.suite
                      + matrix_slack.to_bytes(8, "big"))
        self.public_bytes = _SEED_BYTES + packed_width(params.d * params.t)
        self.private_bytes = _SEED_BYTES + params.private_bytes
        self.ciphertext_bytes = template.ciphertext_bytes

    def _setup(self, seed):
        if type(seed) is not bytes or len(seed) != _SEED_BYTES:
            raise ValueError("expected a 32-byte matrix seed")
        p = self.params
        width = packed_width(p.m)
        row_bytes = width + (self.matrix_slack + 7)//8
        row_id_bytes = max(1, ((p.d-1).bit_length() + 7)//8)
        cardinality = 3**p.m
        trits = bytearray()
        for j in range(p.d):
            raw = _hash(_MATRIX, self.suite, seed, j.to_bytes(row_id_bytes, "big"), row_bytes)
            rank = int.from_bytes(raw, "big") % cardinality
            trits.extend(_unpack_dense(rank.to_bytes(width, "big"), p.m))
        return _pack_dense(trits)

    def _adapter(self, seed):
        adapter = SharedMatrixKEM(self.params, self._setup(seed), self.nonce_bytes)
        # Fixed-length seed follows an unambiguously framed profile and configuration.
        adapter.full.suite = self.suite + seed
        return adapter

    def keygen(self):
        seed = secrets.token_bytes(_SEED_BYTES)
        syndromes, supports = self._adapter(seed).keygen()
        return seed + syndromes, seed + supports

    def encaps(self, public):
        if type(public) is not bytes or len(public) != self.public_bytes:
            raise ValueError("invalid seeded encapsulation key")
        return self._adapter(public[:_SEED_BYTES]).encaps(public[_SEED_BYTES:])

    def decaps(self, private, ciphertext):
        if type(private) is not bytes or len(private) != self.private_bytes:
            raise ValueError("invalid seeded decapsulation key")
        if type(ciphertext) is not bytes or len(ciphertext) != self.ciphertext_bytes:
            return None
        return self._adapter(private[:_SEED_BYTES]).decaps(private[_SEED_BYTES:], ciphertext)
