"""Standalone SG-DIFRA under one matched ternary syndrome assumption.

At the specified dimensions, the common syndrome experiment supplies the
same number of check rows to both security reductions. See the round note.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round15"))
from projected_kem import Params, ProjectedKEM, concat_shape


_SUITE = b"SG-DIFRA/R16/matched-direct-Golay-RS/v1"


class _DirectParams(Params):
    """The entire coin space uses the transmitted Golay–RS body length."""

    @property
    def t(self):
        return concat_shape(self.bits, self.z)[3]


class MatchedKEM(ProjectedKEM):
    """Key generation, encapsulation and decapsulation for the matched layout."""

    def __init__(self, bits, n, weight, *, slack=128, nonce_bytes=32):
        if any(type(i) is not int or not 0 < i < 2**64 for i in (bits, n, weight)):
            raise ValueError("message bits, quadratic inputs and weight must be positive uint64s")
        t = concat_shape(bits, weight)[3]
        a = n * (n + 1) // 2
        m = 4 * (t - 1) * weight
        m += (m + t - a) % 2
        h = (m + t - a) // 2
        r = m - (t - 1) * weight
        if h <= 0 or h + a >= r:
            raise ValueError("dimensions leave no nondegenerate common syndrome problem")
        params = _DirectParams(bits, h, n, m, weight, weight, slack, outer="rs")
        # The parent computes the physical m by dropping (params.t - t)*w.
        # Here that difference is zero. Thus parent coin sampling is already
        # direct and no error coordinate is discarded.
        super().__init__(params, nonce_bytes)
        self.common_columns = r
        self.common_rows = params.d
        self.suite = _SUITE + len(self.suite).to_bytes(8, "big") + self.suite


def research_profile(target):
    """Describe a full design target without generating its large keys."""
    if type(target) is not int or target not in (128, 192, 256):
        raise ValueError("expected a 128, 192 or 256 research target")
    return MatchedKEM(2*target+128, target, 6*target, slack=target+128,
                      nonce_bytes=(4*target+128)//8)
