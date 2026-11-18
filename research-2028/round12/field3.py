"""Arithmetic for the research map (x+a)^14 - x^14 on fixed ternary fields.

A field element is the integer sum(d[i]*3**i), with coefficient d[0] first.
Integer addition and multiplication are NOT field operations on these ranks.
The implementation uses variable-time Python integers and Euclidean algorithms.
"""

from functools import cache
from math import comb
from struct import unpack


# Non-leading terms (exponent, coefficient) of each monic defining polynomial.
# These choices are checked by the finite-field irreducibility test below.
MODULI = {
    1: ((0, 1),),
    2: ((0, 2), (1, 1)),
    4: ((0, 2), (1, 1)),
    5: ((0, 1), (1, 2)),
    7: ((0, 1), (2, 2)),
    8: ((0, 2), (2, 1)),
    82: ((0, 1), (2, 2)),
    122: ((0, 1), (14, 2)),
    163: ((0, 1), (59, 2)),
}


def _trim(poly):
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def _prime_gcd_degree(a, b):
    a, b = _trim(list(a)), _trim(list(b))
    while b:
        while len(a) >= len(b):
            offset = len(a) - len(b)
            scale = a[-1] * b[-1] % 3  # each nonzero trit is self-inverse
            for i, coeff in enumerate(b):
                a[offset + i] = (a[offset + i] - scale * coeff) % 3
            _trim(a)
        a, b = b, a
    return len(a) - 1


def _reduce(values, n, terms):
    for i in range(len(values) - 1, n - 1, -1):
        lead = values[i] % 3
        if lead:
            for j, coeff in terms:
                values[i - n + j] -= lead * coeff
    return [c % 3 for c in values[:n]]


def _cube_coeffs(coeffs, n, terms):
    result = [0] * (3*n)
    result[::3] = coeffs  # coefficient cubing on the prime field is identity
    return _reduce(result, n, terms)


@cache
def _check_modulus(n, terms):
    """Rabin test: X^(3^n)=X and no roots from a proper prime-index subfield."""
    if n == 1:
        return True
    modulus = [0] * n + [1]
    for degree, coeff in terms:
        modulus[degree] = coeff
    indices = {n//p for p in range(2, n+1) if n % p == 0
               and all(p % j != 0 for j in range(2, int(p**0.5)+1))}
    x = [0] * n
    x[1] = 1
    value = x
    for i in range(1, n+1):
        value = _cube_coeffs(value, n, terms)
        if i in indices:
            diff = list(value)
            diff[1] = (diff[1] - 1) % 3
            if _prime_gcd_degree(modulus, diff) != 0:
                return False
    return value == x


def _rank(coeffs):
    result = 0
    for coeff in reversed(coeffs):
        result = result * 3 + coeff
    return result


def _chunk(x):
    digits = []
    for _ in range(5):
        x, digit = divmod(x, 3)
        digits.append(digit)
    return tuple(digits)


_CHUNKS = tuple(_chunk(i) for i in range(243))


class Field3:
    """A specified polynomial-basis F_(3^n), with an admissible CM degree n."""

    def __init__(self, n):
        if type(n) is not int or n not in MODULI or n % 3 == 0:
            raise ValueError("unsupported ternary extension degree")
        self.n = n
        self.terms = MODULI[n]
        if not _check_modulus(n, self.terms):
            raise ValueError("defining polynomial is reducible")
        self.order = 3**n

    def _check(self, a):
        if type(a) is not int or not 0 <= a < self.order:
            raise ValueError("field element outside the canonical range")

    def coeffs(self, a):
        self._check(a)
        digits = []
        while a:
            a, part = divmod(a, 243)
            digits.extend(_CHUNKS[part])
        digits.extend([0] * max(0, self.n - len(digits)))
        return tuple(digits[:self.n])

    def from_coeffs(self, trits):
        digits = tuple(trits)
        if len(digits) != self.n or any(type(t) is not int or t not in (0, 1, 2) for t in digits):
            raise ValueError("expected one trit for each basis coordinate")
        return _rank(digits)

    def add(self, a, b):
        self._check(a)
        self._check(b)
        if not a or not b:
            return a or b
        return _rank([(x+y) % 3 for x, y in zip(self.coeffs(a), self.coeffs(b))])

    def neg(self, a):
        return _rank([(-x) % 3 for x in self.coeffs(a)])

    def sub(self, a, b):
        self._check(a)
        self._check(b)
        if not b or a == b:
            return a if not b else 0
        return _rank([(x-y) % 3 for x, y in zip(self.coeffs(a), self.coeffs(b))])

    def mul(self, a, b):
        self._check(a)
        self._check(b)
        if a < 3 or b < 3:
            scalar, other = (a, b) if a < 3 else (b, a)
            if scalar == 2:
                return self.neg(other)
            return scalar * other
        # Kronecker substitution. Each integer convolution coefficient is
        # <= 4*n < 65536 for every supported n, so 16-bit lanes do not carry.
        def lanes(rank):
            data = bytearray(2*self.n)
            data[::2] = bytes(self.coeffs(rank))
            return int.from_bytes(data, "little")

        size = 2*self.n - 1
        product = (lanes(a) * lanes(b)).to_bytes(2*size, "little")
        coeffs = list(unpack(f"<{size}H", product))
        return _rank(_reduce(coeffs, self.n, self.terms))

    def cube(self, a):
        coeffs = self.coeffs(a)
        return _rank(_cube_coeffs(coeffs, self.n, self.terms))

    def power(self, a, exponent):
        self._check(a)
        if type(exponent) is not int or exponent < 0:
            raise ValueError("expected a nonnegative integer exponent")
        result = 1
        while exponent:
            if exponent & 1:
                result = self.mul(result, a)
            exponent >>= 1
            if exponent:
                a = self.mul(a, a)
        return result

    def inverse(self, a):
        self._check(a)
        if not a:
            raise ZeroDivisionError("zero field element has no inverse")
        return self.power(a, self.order - 2)

    def cm_forward(self, x, a=1):
        self._check(a)
        if a == 0:
            raise ValueError("nonzero shift required")
        return self.sub(self.power(self.add(x, a), 14), self.power(x, 14))

    def _remainder(self, dividend, divisor):
        """Remainder in K[T], including nonmonic divisors."""
        values = _trim(list(dividend))
        if not divisor or not divisor[-1]:
            raise ValueError("expected a nonzero polynomial without trailing zeros")
        inverse_lead = 1 if divisor[-1] == 1 else self.inverse(divisor[-1])
        while len(values) >= len(divisor):
            start = len(values) - len(divisor)
            scale = self.mul(values[-1], inverse_lead)
            for i, coeff in enumerate(divisor[:-1]):
                if coeff:
                    values[start+i] = self.sub(values[start+i], self.mul(scale, coeff))
            values.pop()
            _trim(values)
        return values

    def dickson(self, z, degree):
        """Evaluate D_degree(z,1) by the binary Dickson recurrences."""
        self._check(z)
        if type(degree) is not int or degree < 0:
            raise ValueError("expected a nonnegative Dickson degree")
        low, high = 2, z  # successive degrees 0 and 1
        for bit in bin(degree)[2:]:
            odd = self.sub(self.mul(low, high), z)
            if bit == "0":
                low, high = self.sub(self.mul(low, low), 2), odd
            else:
                low, high = odd, self.sub(self.mul(high, high), 2)
        return low

    def cm_inverse(self, y, a=1):
        """Invert the centered derivative using its known Dickson expression."""
        self._check(y)
        self._check(a)
        if a == 0:
            raise ValueError("nonzero shift required")
        target = y if a == 1 else self.mul(y, self.inverse(self.power(a, 14)))
        # Delta_1(x) = -D_13(x-1,1). The permutation inverse of D_13
        # is D_d for d = 13^{-1} mod (q^2-1), where q=3^n.
        degree = pow(13, -1, self.order*self.order - 1)
        centered = self.dickson(self.neg(target), degree)
        return self.mul(a, self.add(1, centered))

    def cm_inverse_gcd(self, y, a=1):
        """Independent root check using gcd(g(T),T^(3^n)-T), without search."""
        self._check(y)
        self._check(a)
        if a == 0:
            raise ValueError("nonzero shift required")
        # Write x=a*u and (x+a)^14-x^14 = a^14 ((u+1)^14-u^14).
        target = y if a == 1 else self.mul(y, self.inverse(self.power(a, 14)))
        # g(T) = 2*((T+1)^14 - T^14 - target) is monic of degree 13.
        g = [(2 * comb(14, i)) % 3 for i in range(14)]
        g[0] = self.mul(2, self.sub(1, target))
        r = [0, 1]
        for _ in range(self.n):
            cubed = [0] * (3*len(r))
            cubed[::3] = [self.cube(c) for c in r]
            r = self._remainder(cubed, g)
        r += [0] * max(0, 2-len(r))
        r[1] = self.sub(r[1], 1)
        r = _trim(r)
        while r:
            g, r = r, self._remainder(g, r)
        if len(g) != 2:
            raise ArithmeticError("expected a linear gcd for a planar derivative")
        root = self.mul(self.neg(g[0]), self.inverse(g[1]))
        return self.mul(a, root)
