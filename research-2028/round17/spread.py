"""Exact sufficient spread certificates for punctured and quotient ciphertext bodies."""
from math import comb


def _certified_bits(full_length, weight, slack, fiber_size):
    atom_denominator = (comb(full_length, weight) << weight) << slack
    atom_numerator = ((1 << slack) + 1) * fiber_size
    if atom_numerator >= atom_denominator:
        return 0
    bits = atom_denominator.bit_length() - atom_numerator.bit_length()
    return bits - ((atom_numerator << bits) > atom_denominator)


def _validate(full_length, transmitted_length, weight, slack):
    values = (full_length, transmitted_length, weight, slack)
    if any(type(value) is not int for value in values):
        raise ValueError("coordinate lengths, weight and slack must be integers")
    if not (0 <= transmitted_length <= full_length and 0 <= weight <= full_length and slack >= 0):
        raise ValueError("invalid spread dimensions or slack")


def projected_body_spread(full_length, transmitted_length, weight, slack):
    """Guaranteed whole bits of min-entropy from the projected error alone."""
    _validate(full_length, transmitted_length, weight, slack)
    dropped = full_length - transmitted_length
    # An atom with k hidden nonzeros has 2^k binom(dropped,k) completions.
    # This sequence is unimodal and its modes include floor(2*(dropped+1)/3).
    first = max(0, weight - transmitted_length)
    last = min(weight, dropped)
    mode = min(last, max(first, 2 * (dropped + 1) // 3))
    fiber_size = comb(dropped, mode) << mode
    return _certified_bits(full_length, weight, slack, fiber_size)


def quotient_body_spread(full_length, transmitted_length, max_rank, weight, slack):
    """Guaranteed per-key spread for a quotient by a space of rank at most max_rank."""
    _validate(full_length, transmitted_length, weight, slack)
    if type(max_rank) is not int or max_rank < 0:
        raise ValueError("maximum rank must be a nonnegative integer")
    if max_rank == 0:
        return projected_body_spread(full_length, transmitted_length, weight, slack)
    kernel_dimension = full_length - transmitted_length + min(max_rank, transmitted_length)
    highest = min(weight, kernel_dimension)
    term = comb(kernel_dimension, highest) << highest
    fiber_size = term
    # Count restrictions of weight at most w to an information set.
    for i in range(highest, 0, -1):
        term = term * i // (2 * (kernel_dimension - i + 1))
        fiber_size += term
    return _certified_bits(full_length, weight, slack, fiber_size)
