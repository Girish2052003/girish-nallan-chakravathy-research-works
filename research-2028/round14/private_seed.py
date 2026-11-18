"""Optional seed-only storage for the private disjoint checks.

The public wire and FO suite interoperate with SeededMatrixKEM. Replacing
exact random support generation introduces the assumption in PRIVATE_SEED.md.
"""
from math import comb
import secrets

from differential_kem import _hash
from differential_pke import _pack_dense, _width
from seeded_matrix import SeededMatrixKEM, _SEED_BYTES

_PRIVATE_DOMAIN = b"SG-DIFRA/R14/private-checks/hidden-seed/v1"


class PrivateSeedKEM:
    def __init__(self, params, nonce_bytes=32, matrix_slack=None,
                 private_seed_bytes=None, check_slack=None):
        self.seeded = SeededMatrixKEM(params, nonce_bytes, matrix_slack)
        if private_seed_bytes is None:
            private_seed_bytes = (params.bits + 7) // 8
        if check_slack is None:
            check_slack = params.bits + 64
        if type(private_seed_bytes) is not int or not 0 < private_seed_bytes < 2**64:
            raise ValueError("private seed width must be a positive uint64")
        if type(check_slack) is not int or not 0 <= check_slack < 2**64:
            raise ValueError("invalid check-sampling slack")
        self.private_seed_bytes = private_seed_bytes
        self.check_slack_bytes = (check_slack + 7) // 8
        self.profile = (self.seeded.suite + private_seed_bytes.to_bytes(8, "big")
                        + check_slack.to_bytes(8, "big"))
        self.tape_bytes = params.private_bytes + params.t * self.check_slack_bytes
        self.public_bytes = self.seeded.public_bytes
        self.private_bytes = _SEED_BYTES + private_seed_bytes
        self.ciphertext_bytes = self.seeded.ciphertext_bytes
        self.key_bytes = self.seeded.key_bytes

    def _rank_tape(self, tape):
        """Convert disjoint blocks into canonical ranks for the remaining positions."""
        if type(tape) is not bytes or len(tape) != self.tape_bytes:
            raise ValueError("invalid support randomness tape")
        p = self.seeded.params
        result = bytearray()
        cursor = 0
        for j in range(p.t):
            count = comb(p.m - j*p.w, p.w) << p.w
            width = _width(count)
            end = cursor + width + self.check_slack_bytes
            rank = int.from_bytes(tape[cursor:end], "big") % count
            result.extend(rank.to_bytes(width, "big"))
            cursor = end
        return bytes(result)

    def _supports(self, private_seed):
        tape = _hash(_PRIVATE_DOMAIN, self.profile, b"", private_seed, self.tape_bytes)
        return self._rank_tape(tape)

    def keygen(self):
        matrix_seed = secrets.token_bytes(_SEED_BYTES)
        private_seed = secrets.token_bytes(self.private_seed_bytes)
        adapter = self.seeded._adapter(matrix_seed)
        public = _pack_dense(adapter._public_trits(self._supports(private_seed)))
        return matrix_seed + public, matrix_seed + private_seed

    def encaps(self, public):
        return self.seeded.encaps(public)

    def decaps(self, private, ciphertext):
        if type(private) is not bytes or len(private) != self.private_bytes:
            raise ValueError("invalid seed-only decapsulation key")
        if type(ciphertext) is not bytes or len(ciphertext) != self.ciphertext_bytes:
            return None
        supports = self._supports(private[_SEED_BYTES:])
        return self.seeded.decaps(private[:_SEED_BYTES] + supports, ciphertext)


def research_profile(target):
    """Construct a measured-layout descriptor; the target is an unrated design label."""
    from differential_pke import Params
    from parameters import illustration

    if type(target) is not int or target not in (128, 192, 256):
        raise ValueError("choose the 128, 192 or 256 research target")
    layout = illustration(target)
    params = Params(layout.bits, layout.h, layout.n, layout.m, layout.w,
                    layout.z, layout.slack, outer="rs")
    return PrivateSeedKEM(params, nonce_bytes=layout.nonce_bytes)
