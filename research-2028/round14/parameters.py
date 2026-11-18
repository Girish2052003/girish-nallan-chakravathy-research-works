"""Wire-size arithmetic for the repetition and Reed-Solomon research layouts.

This module allocates neither the public matrix nor vectors proportional to its
entry count. A byte count is not an estimate of cryptographic strength.
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from functools import lru_cache
from math import comb


def rank_bytes(count):
    """Shortest fixed byte width for ranks 0 through count-1."""
    if type(count) is not int or count < 1:
        raise ValueError("positive integer count required")
    return ((count - 1).bit_length() + 7) // 8


def mixed_rank_bytes(trits, multiplier=1):
    """Exact width of 3**trits * multiplier, even for enormous trit counts."""
    if type(trits) is not int or trits < 0 or type(multiplier) is not int or multiplier < 1:
        raise ValueError("invalid rank count")
    if trits == 0:
        return rank_bytes(multiplier)
    with localcontext() as ctx:
        ctx.prec = 40
        while True:
            a, b, c = Decimal(3).ln(), Decimal(multiplier).ln(), Decimal(256).ln()
            # Decimal.ln rounds to nearest. Bound each logarithm outward;
            # monotone operands and directed division give certified intervals.
            ctx.rounding = ROUND_FLOOR
            lo = (Decimal(trits)*a.next_minus() + b.next_minus()) / c.next_plus()
            ctx.rounding = ROUND_CEILING
            hi = (Decimal(trits)*a.next_plus() + b.next_plus()) / c.next_minus()
            if int(lo) == int(hi):
                return int(lo) + 1  # 3 divides the rank count, excluding an exact power of 256.
            ctx.prec *= 2


def signed_error_count(length, weight):
    return comb(length, weight) << weight


def support_bytes(m, w, t):
    """Sum the byte widths of independently ranked signed-support slots."""
    if min(w, t) < 1 or m < t*w:
        raise ValueError("supports must fit and have positive weight")
    @lru_cache(maxsize=None)
    def slot(j):
        return rank_bytes(signed_error_count(m - j*w, w))

    # Slot widths decrease monotonically. Find entire equal-width runs at
    # once, avoiding millions of huge binomial calculations for repetition.
    total = 0
    start = 0
    while start < t:
        width = slot(start)
        low, high = start + 1, t
        while low < high:
            mid = (low + high) // 2
            if slot(mid) == width:
                low = mid + 1
            else:
                high = mid
        total += (low - start) * width
        start = low
    return total


@dataclass(frozen=True)
class Layout:
    bits: int
    h: int
    n: int
    m: int
    w: int
    z: int
    t: int
    slack: int
    nonce_bytes: int

    def __post_init__(self):
        positive = (self.bits, self.h, self.n, self.m, self.w, self.t, self.nonce_bytes)
        if (any(type(v) is not int or v < 1 for v in positive)
                or any(type(v) is not int or v < 0 for v in (self.z, self.slack))
                or self.t*self.w > self.m or self.z > self.m+self.t):
            raise ValueError("invalid layout")

    def sizes(self):
        N = self.m + self.t
        d = self.h + self.n*(self.n + 1)//2
        pk = mixed_rank_bytes(d*N)
        priv = support_bytes(self.m, self.w, self.t)
        body = mixed_rank_bytes(N)
        coins = mixed_rank_bytes(self.h + self.n, signed_error_count(N, self.z))
        coins += (self.slack + 7)//8
        key_payload = mixed_rank_bytes(d*self.t)
        return dict(d=d, N=N, key_dsd_length=self.m-(self.t-1)*self.w,
                    noise_dsd_rows=N-self.h, pk=pk, supports=priv, sk=pk+priv,
                    body=body, ct=body+self.nonce_bytes, coins=coins, shared=32,
                    crs=mixed_rank_bytes(d*self.m), with_crs_pk=key_payload,
                    seeded_pk=32+key_payload, seeded_sk=32+priv)


def outer_shape(bits, z):
    """Independent integer evaluation of the minimal extension-field width."""
    if type(bits) is not int or bits < 1 or type(z) is not int or z < 0:
        raise ValueError("positive message and nonnegative radius required")
    s, q = 1, 3
    while True:
        k, capacity = 0, 1
        while capacity < 1 << bits:
            capacity *= q
            k += 1
        ell = k + 2*z
        if ell <= q:
            return s, k, ell, s*ell
        s += 1
        q *= 3


def illustration(b, outer="rs"):
    """An analytical scaling experiment; the rows are unrated."""
    if type(b) is not int or b < 1 or outer not in ("rs", "repeat"):
        raise ValueError("invalid target or outer code")
    bits, w, z = 2*b + 128, 6*b, 6*b
    t = outer_shape(bits, z)[3] if outer == "rs" else bits*(2*z + 1)
    m = 2*t*w
    return Layout(bits, m//3, b, m, w, z, t, b+128, (4*b+128+7)//8)


if __name__ == "__main__":
    for target in (128, 192, 256):
        row = illustration(target)
        sizes = row.sizes()
        baseline = illustration(target, "repeat")
        # Only the comparison public key is needed for the repetition table.
        plain_d = baseline.h + baseline.n*(baseline.n+1)//2
        plain_pk = mixed_rank_bytes(plain_d*(baseline.m + baseline.t))
        print(target, outer_shape(row.bits, row.z), row, sizes, 'repeat_pk', plain_pk)
