"""Shared, uniformly random matrix encoding for the single-user Round 14 game."""
import secrets

from differential_kem import DifferentialKEM
from differential_pke import _pack_dense, _unpack_dense, packed_width


def generate_setup(params):
    """Generate one canonical, uniformly random public matrix for this suite."""
    trits = params.d * params.m
    rank = secrets.randbelow(3**trits)
    return rank.to_bytes(packed_width(trits), "big")


class SharedMatrixKEM:
    """Use a separately authenticated matrix and transmit only syndrome columns.

    Ciphertexts bind the reconstructed canonical full public key, interoperating
    with DifferentialKEM. A receiver stores its support ranks and the setup.
    """

    def __init__(self, params, setup, nonce_bytes=32):
        self.full = DifferentialKEM(params, nonce_bytes)
        self.params = params
        self._a = bytes(_unpack_dense(setup, params.d * params.m))
        self.public_bytes = packed_width(params.d * params.t)
        self.private_bytes = params.private_bytes
        self.ciphertext_bytes = self.full.ciphertext_bytes
        self.key_bytes = self.full.key_bytes

    def _public_trits(self, secret):
        p = self.params
        checks = self.full.base._private_checks(secret)
        result = bytearray()
        for row in range(p.d):
            start = row * p.m
            result.extend(sum(self._a[start + i] * sign for i, sign in support) % 3
                          for support in checks)
        return result

    def _full_public(self, syndromes):
        p = self.params
        matrix = bytearray()
        for i in range(p.d):
            matrix.extend(self._a[i*p.m:(i+1)*p.m])
            matrix.extend(syndromes[i*p.t:(i+1)*p.t])
        return _pack_dense(matrix)

    def expand_public(self, compact_public):
        p = self.params
        return self._full_public(_unpack_dense(compact_public, p.d * p.t))

    def keygen(self):
        secret = self.full.base.sample_private()
        return _pack_dense(self._public_trits(secret)), secret

    def encaps(self, compact_public):
        return self.full.encaps(self.expand_public(compact_public))

    def decaps(self, secret, ciphertext):
        if type(ciphertext) is not bytes or len(ciphertext) != self.ciphertext_bytes:
            return None
        public = self._full_public(self._public_trits(secret))
        return self.full.decaps(public + secret, ciphertext)
