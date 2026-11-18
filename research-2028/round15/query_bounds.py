"""Unconditional coordinate-query certificates for two ternary distributions.

The bounds concern reading classical field elements in superposition. They are
not computational security estimates for a public key or ciphertext.
"""
from math import comb


def coordinate_queries(length, log2_denominator_lower, gap_bits, *, square_root):
    """Certify a query count via M(n,D) <= (6n/D)^D with D=2q."""
    if length <= 0 or gap_bits <= 0 or log2_denominator_lower < 0:
        raise ValueError("invalid bound parameters")
    budget = (log2_denominator_lower - 2*gap_bits + 2 if square_root else
              log2_denominator_lower - gap_bits)
    best = 0
    # Check every candidate k giving 6n/D <= 2^k. Within that range, the
    # largest even D with kD <= budget is sufficient and the easiest to certify.
    for k in range(1, (6*length).bit_length() + 1):
        degree = 2 * (min(length, budget // k) // 2)
        if degree > 0 and (degree << k) >= 6*length:
            best = max(best, degree // 2)
    return best


def classical_column_queries(length, weight, gap_bits):
    """Maximum q whose support-containment probability is at most 2^-gap_bits."""
    if not 1 <= weight <= length or gap_bits <= 0:
        raise ValueError("invalid support size or gap")
    denom = comb(length, weight)
    low, high = 0, length
    while high - low > 1:
        mid = (low + high) // 2
        if (comb(mid, weight) << gap_bits) <= denom:
            low = mid
        else:
            high = mid
    return low


def certificates(d, r, weight, N, h, gap_bits=280):
    if not 1 <= weight <= r or not 1 <= h <= N:
        raise ValueError("invalid matrix or weight")
    key_entropy = (comb(r, weight) << weight).bit_length() - 1
    # 3^12 > 2^19, so the following lower bound has no rounding ambiguity.
    payload_entropy = (19*h) // 12
    return (coordinate_queries(d, key_entropy, gap_bits, square_root=True),
            coordinate_queries(N, payload_entropy, gap_bits, square_root=False),
            classical_column_queries(r, weight, gap_bits))


if __name__ == "__main__":
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round14"))
    from parameters import illustration

    for target in (128, 192, 256):
        p = illustration(target)
        d = p.h + p.n*(p.n+1)//2
        r = p.m - (p.t-1)*p.w
        print(target, *certificates(d, r, p.w, p.m+p.t, p.h))
