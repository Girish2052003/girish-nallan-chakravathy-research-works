"""Exact integer certificates for selected ternary KEM query-budget diagnostics.

These calculations count possibilities and search queries. They do not evaluate
any cryptosystem, estimate gates, or supply a lower bound for cryptanalysis.
"""
from fractions import Fraction


TARGETS = (128, 191, 192, 256)


def _positive(value):
    if type(value) is not int or value < 1:
        raise ValueError("positive integer required")
    return value


def _inverse_sine_squared_bounds(u, v):
    """For 0 < u <= angle <= v < 1, enclose 1 / sin(angle)**2."""
    if not 0 < u <= v < 1:
        raise ValueError("angle bounds must be positive and below one radian")
    return 1 / v**2, 1 / (u - u**3 / 6)**2


def half_recovery_threshold(trials, marked=1):
    """Bound marked / sin(pi/(8*trials-4))**2 by exact rational numbers."""
    _positive(trials)
    _positive(marked)
    denominator = 8 * trials - 4
    u = Fraction(314, 100) / denominator
    v = Fraction(22, 7) / denominator
    low, high = _inverse_sine_squared_bounds(u, v)
    return marked * low, marked * high


def reduction_threshold(hash_queries, phase_queries):
    """Bounds for a one-stage raw IND gap of at most 1/2 via Round 12."""
    _positive(hash_queries)
    if type(phase_queries) is not int or phase_queries < 0:
        raise ValueError("nonnegative phase-query budget required")
    s = Fraction(1, 4 * hash_queries)
    scale = 2 * phase_queries + 1
    # For 0<s<1, s <= asin(s) <= s/(1-s^2), by integrating its derivative.
    return _inverse_sine_squared_bounds(s / scale, s / ((1-s*s) * scale))


def first_power_above(base, threshold):
    if type(base) is not int or base < 2 or threshold < 0:
        raise ValueError("base must be at least two and threshold nonnegative")
    exponent, power = 0, 1
    while power <= threshold:
        power *= base
        exponent += 1
    return exponent


def certified_exponent(base, bounds):
    """Require the full interval to lie strictly between consecutive powers."""
    low, high = bounds
    if not 0 < low <= high:
        raise ValueError("positive, ordered bounds required")
    exponent = first_power_above(base, high)
    if exponent and base**(exponent - 1) >= low:
        raise ArithmeticError("rational enclosure cannot certify this exponent")
    return exponent


def point_bytes(trits):
    _positive(trits)
    return ((3**trits - 1).bit_length() + 7) // 8


def profile_row(bits):
    """Compute the independent size filters specified in PROFILE_BOUNDS.md."""
    budget = 1 << _positive(bits)
    generic = half_recovery_threshold(budget)
    quantum_trits = certified_exponent(3, generic)
    proof_trits = certified_exponent(3, reduction_threshold(budget, budget))
    return {
        "bits": bits,
        "classical_trits": first_power_above(3, 2*budget - 2),
        "quantum_trits": quantum_trits,
        "quantum_bytes": point_bytes(quantum_trits),
        "seed_bits": certified_exponent(2, generic),
        "proof_trits": proof_trits,
        "proof_bytes": point_bytes(proof_trits),
    }


if __name__ == '__main__':
    print('b   classical trits   quantum trits/B   seed bits   reduction trits/B')
    for target in TARGETS:
        print('{bits:3} {classical_trits:15} {quantum_trits:11}/{quantum_bytes:<3} '
              '{seed_bits:10} {proof_trits:16}/{proof_bytes}'.format(**profile_row(target)))
