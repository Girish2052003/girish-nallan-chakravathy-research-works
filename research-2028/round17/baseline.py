"""Resource arithmetic for the fixed-weight public distributions; takes only dimensions."""
from decimal import Decimal, localcontext
from fractions import Fraction
from math import comb, prod


def containment(rows, columns, weight):
    if not (0 < weight <= rows <= columns):
        raise ValueError("expected 0 < weight <= rows <= columns")
    return Fraction(comb(rows, weight), comb(columns, weight))


def rank_interval(rows, terms=48):
    """Rigorous bounds on the nonsingularity probability of a ternary square."""
    if rows <= 0 or terms <= 0:
        raise ValueError("positive dimensions and truncation length required")
    last = min(terms, rows)
    partial = prod(1 - Fraction(1, 3**j) for j in range(1, last + 1))
    tail = Fraction(1, 2 * 3**last) if last < rows else Fraction(0)
    return partial * (1 - tail), partial


def table_row(rows, columns, weight):
    support = containment(rows, columns, weight)
    rank_low, rank_high = rank_interval(rows)
    with localcontext() as ctx:
        ctx.prec = 55
        log_two = Decimal(2).ln()

        def exponent(fraction):
            return (Decimal(fraction.denominator) / Decimal(fraction.numerator)).ln() / log_two

        low, high = exponent(support * rank_high), exponent(support * rank_low)
        midpoint = (low + high) / 2
        ideal_tb = Decimal(rows * columns) * Decimal(3).ln() / (log_two * 8 * 10**12)
        return exponent(support), low, high, midpoint / 2, ideal_tb


if __name__ == '__main__':
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'round16'))
    from matched_kem import research_profile

    for target in (128, 192, 256):
        kem = research_profile(target)
        result = table_row(kem.common_rows, kem.common_columns, kem.source.w)
        print(target, *(f'{field:.6f}' for field in result))
