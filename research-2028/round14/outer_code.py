"""Public evaluation Reed–Solomon outer code for correcting ternary residuals.

Symbols and polynomial coefficients use least significant coordinates first.
The modulus and all evaluation points are public. See OUTER_CODE.md.
"""
from functools import cache, cached_property, lru_cache
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round12"))
from field3 import Field3, MODULI, _check_modulus


@lru_cache(maxsize=128, typed=True)
def rs_shape(bits, z):
    """Return extension degree, message symbols, code symbols and trit length."""
    if type(bits) is not int or bits < 1 or type(z) is not int or z < 0:
        raise ValueError("expected a positive bit length and a nonnegative error bound")
    low, high = 0, bits
    while high - low > 1:
        power = (low + high) // 2
        if (3**power).bit_length() > bits:
            high = power
        else:
            low = power
    b = 1
    while True:
        k = (high + b - 1) // b
        length = k + 2*z
        if length <= 3**b:
            return b, k, length, b*length
        b += 1


class _EvaluationField(Field3):
    """Only field arithmetic is used; the CM-specific degree condition is irrelevant."""
    def __init__(self, b):
        if b >= 16384:
            raise ValueError("extension degree exceeds the field arithmetic limit")
        self.n = b
        self.order = 3**b
        self.terms = _modulus(b)


@cache
def _modulus(b):
    if b in MODULI and _check_modulus(b, MODULI[b]):
        return MODULI[b]
    for rank in range(1, 3**b):
        if rank % 3:
            terms = []
            i = 0
            while rank:
                rank, coeff = divmod(rank, 3)
                if coeff:
                    terms.append((i, coeff))
                i += 1
            candidate = tuple(terms)
            if _check_modulus(b, candidate):
                return candidate
    raise ArithmeticError("irreducible polynomial search failed")


def _trim(p):
    while p and not p[-1]:
        p.pop()
    return p


def _eval(F, p, point):
    value = 0
    for coefficient in reversed(p):
        value = F.add(F.mul(value, point), coefficient)
    return value


def _times(F, p, q):
    if not p or not q:
        return []
    result = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                result[i+j] = F.add(result[i+j], F.mul(a,b))
    return _trim(result)


def _sub(F, p, q):
    result = list(p) + [0]*max(0, len(q)-len(p))
    for j, b in enumerate(q):
        result[j] = F.sub(result[j], b)
    return _trim(result)


def _divmod(F, p, q):
    if not q:
        raise ZeroDivisionError("zero polynomial divisor")
    r = list(p)
    result = [0] * max(0, len(r)-len(q)+1)
    inv = F.inverse(q[-1])
    while len(r) >= len(q):
        j = len(r)-len(q)
        c = F.mul(r[-1], inv)
        result[j] = c
        for i, a in enumerate(q):
            r[i+j] = F.sub(r[i+j], F.mul(c,a))
        _trim(r)
    return _trim(result), r


class RSOuter:
    def __init__(self, bits, z):
        self.bits, self.z = bits, z
        self.b, self.k, self.length, self.t = rs_shape(bits, z)
        self.field = _EvaluationField(self.b)

    def encode(self, message):
        if type(message) is not int or message < 0 or message.bit_length() > self.bits:
            raise ValueError("message outside the fixed bit width")
        coeffs = []
        while message:
            message, c = divmod(message, self.field.order)
            coeffs.append(c)
        return tuple(trit for a in range(self.length)
                     for trit in self.field.coeffs(_eval(self.field, coeffs, a)))

    @cached_property
    def _vanishing(self):
        F = self.field
        poly = [1]
        for a in range(self.length):
            poly = _times(F, poly, [F.neg(a), 1])
        return poly

    def _interpolate(self, received):
        F = self.field
        # Running sum of y_i G(X)/((X-a_i) G'(a_i)).
        result = [0] * self.length
        for a, y in enumerate(received):
            if y:
                quotient, _ = _divmod(F, self._vanishing, [F.neg(a), 1])
                scale = F.mul(y, F.inverse(_eval(F, quotient, a)))
                for j, c in enumerate(quotient):
                    result[j] = F.add(result[j], F.mul(scale, c))
        return _trim(result)

    def decode(self, trits):
        try:
            word = tuple(trits)
            if len(word) != self.t:
                return None
            F = self.field
            received = [F.from_coeffs(word[j:j+self.b]) for j in range(0, self.t, self.b)]
        except (ValueError, TypeError):
            return None

        # Partial extended Euclidean algorithm (Gao decoding).
        previous, remainder = self._vanishing, self._interpolate(received)
        previous_v, v = [], [1]
        while len(remainder) > self.k + self.z:
            quotient, new_remainder = _divmod(F, previous, remainder)
            previous, remainder = remainder, new_remainder
            previous_v, v = v, _sub(F, previous_v, _times(F, quotient, v))
        if not v:
            return None
        message_poly, rem = _divmod(F, remainder, v)
        if rem or len(message_poly) > self.k:
            return None
        if sum(_eval(F, message_poly, a) != y for a, y in enumerate(received)) > self.z:
            return None
        message = 0
        for c in reversed(message_poly):
            message = message*F.order + c
        return message if message.bit_length() <= self.bits else None
