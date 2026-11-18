"""Parallel KEM composition with ciphertext binding and a compact SG-DIFRA component.

Each profile fixes component widths and either regenerates both public
keys or stores one public-context digest in the private key.
"""
from hashlib import sha3_384
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round14"))
from differential_pke import Params, _pack_dense
from private_seed import PrivateSeedKEM


_SUITE = b"SG-DIFRA/R15/anchor+R14-small/parallel/SHA3-384-256/v1"
_PUBLIC = b"SG-DIFRA/R15/parallel/public-bound/v1"
_OUTPUT = b"SG-DIFRA/R15/parallel/output/v1"


def _hash(tag, *fields):
    """Injective framing, followed by a 32-byte truncation of SHA3-384."""
    digest = sha3_384()
    for field in (tag, *fields):
        digest.update(len(field).to_bytes(8, "big"))
        digest.update(field)
    return digest.digest()[:32]


class ParallelKEM:
    """Single-recipient fixed-width research profile. See COMBINER.md."""
    key_bytes = 32

    def __init__(self, anchor, cache_public=True):
        if type(cache_public) is not bool or type(anchor.suite) is not bytes or not anchor.suite:
            raise ValueError("expected a named anchor suite and a boolean cache choice")
        if not cache_public and not callable(getattr(anchor, "public_from_private", None)):
            raise ValueError("the full-public mode requires public-key regeneration")
        if anchor.key_bytes != 32:
            raise ValueError("anchor must produce 32-byte shared secrets")
        self.anchor = anchor
        self.cache_public = cache_public
        params = Params(bits=256, h=8, n=3, m=640, w=3, z=2, slack=128, outer="rs")
        self.native = PrivateSeedKEM(params, nonce_bytes=32)
        mode = b"public-digest" if cache_public else b"full-public"
        self.suite = b"".join(len(field).to_bytes(8, "big") + field for field in
                              (_SUITE, anchor.suite, self.native.profile, mode))
        self.public_bytes = self.anchor.public_bytes + self.native.public_bytes
        self.private_bytes = self.anchor.private_bytes + self.native.private_bytes + (32 if cache_public else 0)
        self.ciphertext_bytes = self.anchor.ciphertext_bytes + self.native.ciphertext_bytes

    def _combine(self, first_secret, second_secret, first_ct, second_ct,
                 public_fields):
        return _hash(_OUTPUT, first_secret, second_secret, first_ct, second_ct,
                     *public_fields, self.suite)

    def _public_fields(self, first_public, second_public):
        if self.cache_public:
            return (_hash(_PUBLIC, first_public, second_public, self.suite),)
        return (first_public, second_public)

    def _native_public(self, private):
        # Round 14's public wire is the matrix seed followed by its check columns.
        seed = private[:32]
        adapter = self.native.seeded._adapter(seed)
        checks = self.native._supports(private[32:])
        return seed + _pack_dense(adapter._public_trits(checks))

    def keygen(self):
        first_public, first_private = self.anchor.keygen()
        second_public, second_private = self.native.keygen()
        private = first_private + second_private
        if self.cache_public:
            private += self._public_fields(first_public, second_public)[0]
        return first_public + second_public, private

    def encaps(self, public):
        if type(public) is not bytes or len(public) != self.public_bytes:
            raise ValueError("invalid composite encapsulation key")
        first_public = public[:self.anchor.public_bytes]
        second_public = public[self.anchor.public_bytes:]
        first_ct, first_secret = self.anchor.encaps(first_public)
        second_ct, second_secret = self.native.encaps(second_public)
        shared = self._combine(first_secret, second_secret, first_ct, second_ct,
                               self._public_fields(first_public, second_public))
        return first_ct + second_ct, shared

    def decaps(self, private, ciphertext):
        if type(private) is not bytes or len(private) != self.private_bytes:
            raise ValueError("invalid composite decapsulation key")
        if type(ciphertext) is not bytes or len(ciphertext) != self.ciphertext_bytes:
            return None
        first_ct = ciphertext[:self.anchor.ciphertext_bytes]
        second_ct = ciphertext[self.anchor.ciphertext_bytes:]
        first_private = private[:self.anchor.private_bytes]
        end = self.anchor.private_bytes + self.native.private_bytes
        second_private = private[self.anchor.private_bytes:end]
        first_secret = self.anchor.decaps(first_private, first_ct)
        second_secret = self.native.decaps(second_private, second_ct)
        if first_secret is None or second_secret is None:
            return None
        if self.cache_public:
            public_fields = (private[end:],)
        else:
            public_fields = (self.anchor.public_from_private(first_private),
                             self._native_public(second_private))
        return self._combine(first_secret, second_secret, first_ct, second_ct, public_fields)


class HybridKEM(ParallelKEM):
    """Compact ML-KEM-backed suite; uses the full public-key transcript."""

    def __init__(self, profile):
        from reviewed_kem import MLKEM
        super().__init__(MLKEM(profile), cache_public=False)
