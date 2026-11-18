"""Shorter standalone differential KEM under the Round 16 source distribution."""
from fractions import Fraction
from functools import cached_property
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'round16'))
from matched_kem import MatchedKEM
from concatenated import ConcatenatedOuter, concat_shape
from projected_kem import _ROWS_PER_BLOCK, _SEED_BYTES, packed_width


class ProjectedRadiusKEM(MatchedKEM):
    """Project the original error and decode to a smaller certified radius."""

    def __init__(self, bits, n, weight, *, radius=None, slack=128, nonce_bytes=32):
        super().__init__(bits, n, weight, slack=slack, nonce_bytes=nonce_bytes)
        if radius is None:
            radius = weight // 2
        if type(radius) is not int or not 0 <= radius <= weight:
            raise ValueError('radius must be an integer between zero and the error weight')
        self.radius = radius
        self.t = concat_shape(bits, radius)[3]
        self.m = self.common_columns + (self.t - 1) * weight
        self.N = self.m + self.t
        if self.N > self.source.N:
            raise ValueError('outer code must fit in the original body')
        blocks, tail = divmod(self.source.d, _ROWS_PER_BLOCK)
        check_bytes = blocks * packed_width(_ROWS_PER_BLOCK * self.t)
        if tail:
            check_bytes += packed_width(tail * self.t)
        self.public_bytes = _SEED_BYTES + check_bytes
        self.body_bytes = packed_width(self.N)
        self.ciphertext_bytes = self.nonce_bytes + self.body_bytes
        self.suite = b'SG-DIFRA/R17/projected-radius/v1' + radius.to_bytes(8, 'big') + self.suite

    @cached_property
    def _outer(self):
        return ConcatenatedOuter(self.source.bits, self.radius)

    def failure_bound(self):
        """Per-key, per-message upper bound for the finite random-tape sampler."""
        w = self.source.w
        relevant = self.t * (w + 1)
        if self.radius >= min(w, relevant):
            return Fraction(0)
        # Tilt 6 is close to optimal for the three registered half-radius suites.
        moment = Fraction(self.source.N + 5 * relevant, self.source.N) ** w
        relative_inflation = 1 + Fraction(1, 1 << self.source.slack)
        return min(Fraction(1), relative_inflation * moment / 6**(self.radius + 1))


def research_profile(target):
    if type(target) is not int or target not in (128, 192, 256):
        raise ValueError('expected a 128, 192 or 256 research target')
    return ProjectedRadiusKEM(2 * target + 128, target, 6 * target,
                              slack=target + 128, nonce_bytes=(4 * target + 128) // 8)
