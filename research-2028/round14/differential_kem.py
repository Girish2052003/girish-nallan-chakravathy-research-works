"""Positive FO KEM construction with explicit rejection over DifferentialPKE.

Research reference. Parameters and acceptance rules are part of the protocol.
The accompanying theorem models G and H as independent random oracles.
"""
from hashlib import shake_256
from hmac import compare_digest
import secrets

from differential_pke import DifferentialPKE


_SUITE = b"SG-DIFRA/R14/differential-code/FO/v1"
_COINS = b"SG-DIFRA/R14/FO/G/v1"
_KEY = b"SG-DIFRA/R14/FO/H/v1"


def _hash(domain, suite, public, message, size):
    """Hash four independently length-delimited byte fields."""
    state = shake_256()
    for field in (domain, suite, public, message):
        state.update(len(field).to_bytes(8, "big"))
        state.update(field)
    return state.digest(size)


class DifferentialKEM:
    """Keygen returns (encapsulation key, standalone decapsulation key).

    The public key uses the underlying PKE format. A decapsulation key stores
    the public key immediately followed by the PKE private payload. Fixed
    widths come from the out-of-band suite. Ordinary operation needs only one
    call to keygen, encaps, or decaps; decaps returns None on rejection.
    """

    key_bytes = 32

    def __init__(self, params, nonce_bytes=32):
        if type(nonce_bytes) is not int or not 1 <= nonce_bytes < 2**64:
            raise ValueError("nonce width must be a positive uint64")
        self.base = DifferentialPKE(params)
        self.params = params
        self.nonce_bytes = nonce_bytes
        config = (params.bits, params.h, params.n, params.m, params.w,
                  params.z, params.slack, nonce_bytes, self.key_bytes)
        if any(type(x) is not int or not 0 <= x < 2**64 for x in config):
            raise ValueError("KEM suite dimensions must fit uint64")
        outer = params.outer.encode("ascii")
        self.suite = (_SUITE + b"".join(x.to_bytes(8, "big") for x in config)
                      + len(outer).to_bytes(8, "big") + outer)
        self.public_bytes = params.public_bytes
        self.private_bytes = params.public_bytes + params.private_bytes
        self.ciphertext_bytes = nonce_bytes + params.body_bytes

    def keygen(self):
        public, secret = self.base.keygen()
        return public, public + secret

    def _ciphertext(self, public, message):
        tape = _hash(_COINS, self.suite, public, message,
                     self.nonce_bytes + self.params.coin_bytes)
        nonce, coins = tape[:self.nonce_bytes], tape[self.nonce_bytes:]
        return nonce + self.base.encrypt(public, message, coins)

    def encaps(self, public):
        """Return an honest ciphertext and the sender's 32-byte shared key."""
        if type(public) is not bytes or len(public) != self.public_bytes:
            raise ValueError("invalid encapsulation-key length or type")
        rank = secrets.randbits(self.params.bits)
        message = rank.to_bytes(self.params.message_bytes, "big")
        ciphertext = self._ciphertext(public, message)
        return ciphertext, _hash(_KEY, self.suite, public, message, self.key_bytes)

    def decaps(self, private, ciphertext):
        """Return the verified shared key or None for a malformed/mismatched ciphertext."""
        if type(private) is not bytes or len(private) != self.private_bytes:
            raise ValueError("invalid decapsulation-key length or type")
        if type(ciphertext) is not bytes or len(ciphertext) != self.ciphertext_bytes:
            return None
        public = private[:self.public_bytes]
        secret = private[self.public_bytes:]
        self.base.validate_public(public)
        message = self.base.decrypt(secret, ciphertext[self.nonce_bytes:])
        if message is None:
            return None
        expected = self._ciphertext(public, message)
        if not compare_digest(ciphertext, expected):
            return None
        return _hash(_KEY, self.suite, public, message, self.key_bytes)
