"""Public concatenated evaluation/Golay encoder and guaranteed-radius GMD decoder."""
from functools import cache
from itertools import combinations, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'round14'))
from outer_code import _EvaluationField, _divmod, _eval, _sub, _times, _trim


# Paley conference matrix of order six over F3. The generator is [I | PARITY].
PARITY = ((0, 1, 1, 1, 1, 1), (1, 0, 1, 2, 2, 1), (1, 1, 0, 1, 2, 2),
          (1, 2, 1, 0, 1, 2), (1, 2, 2, 1, 0, 1), (1, 1, 2, 2, 1, 0))


def _digits(x, count):
    trits = []
    for _ in range(count):
        x, rem = divmod(x, 3)
        trits.append(rem)
    return tuple(trits)


def _rank(trits):
    rank = 0
    for t in reversed(trits):
        rank = 3*rank + t
    return rank


def _parity(data):
    return tuple(sum(x*a[j] for x, a in zip(data, PARITY)) % 3 for j in range(6))


@cache
def _inner_words():
    return tuple(data + _parity(data) for data in (_digits(i, 6) for i in range(729)))


@cache
def _leaders():
    """Store one minimum-weight error per syndrome, by increasing weight."""
    entries = {}
    for weight in range(13):
        for support in combinations(range(12), weight):
            for values in product((1, 2), repeat=weight):
                error = [0] * 12
                for j, value in zip(support, values):
                    error[j] = value
                syndrome = tuple((y-p) % 3 for y, p in zip(error[6:], _parity(error[:6])))
                entries.setdefault(syndrome, (weight, tuple(error[:6])))
        if len(entries) == 729:
            return entries
    raise ArithmeticError('incomplete syndrome table')


def _nearest(word):
    syndrome = tuple((y-p) % 3 for y, p in zip(word[6:], _parity(word[:6])))
    distance, error = _leaders()[syndrome]
    return _rank(tuple((x-e) % 3 for x, e in zip(word, error))), distance


def concat_shape(bits, z):
    """Return field degree, message symbols, outer symbols, transmitted trits."""
    if type(bits) is not int or bits < 1 or type(z) is not int or z < 0:
        raise ValueError('expected a positive message width and a nonnegative error bound')
    # ceil(log_3(2**bits)), using exact integer comparisons.
    low, high = 0, bits
    while high - low > 1:
        middle = (low + high) // 2
        if (3**middle).bit_length() > bits:
            high = middle
        else:
            low = middle
    g = 1
    while True:
        degree = 6*g
        k = (high + degree - 1) // degree
        length = k + z//3
        if length <= 729**g:
            return degree, k, length, 12*g*length
        g += 1


def _small_add(a, b):
    return _rank(tuple((x+y) % 3 for x,y in zip(_digits(a, 3), _digits(b, 3))))


class _Field729(_EvaluationField):
    """Table-based arithmetic in the same polynomial basis for the target profiles."""
    def __init__(self):
        super().__init__(6)
        self._sum = tuple(tuple(_small_add(a,b) for b in range(27)) for a in range(27))
        self._negative = tuple(_rank(tuple((-c) % 3 for c in _digits(a, 6))) for a in range(729))
        # 728 = 2^3 * 7 * 13. Use the generic field only to construct the tables.
        generic = _EvaluationField(6)
        primitive = next(a for a in range(2, 729)
                         if all(generic.power(a, 728//p) != 1 for p in (2, 7, 13)))
        powers = [1]
        for _ in range(727):
            powers.append(generic.mul(powers[-1], primitive))
        self._power = tuple(powers + powers)
        self._log = [0] * 729
        for j, a in enumerate(powers):
            self._log[a] = j

    def add(self, a, b):
        return self._sum[a//27][b//27]*27 + self._sum[a%27][b%27]

    def neg(self, a):
        return self._negative[a]

    def sub(self, a, b):
        return self.add(a, self._negative[b])

    def mul(self, a, b):
        return self._power[self._log[a]+self._log[b]] if a and b else 0

    def inverse(self, a):
        if not a:
            raise ZeroDivisionError('zero has no multiplicative inverse')
        return self._power[728-self._log[a]]


@cache
def _field(degree):
    return _Field729() if degree == 6 else _EvaluationField(degree)


def _recover(F, k, observations):
    """Gao decoding after puncturing erased coordinates. Return message coefficients."""
    retained = len(observations)
    if retained < k:
        return None
    if (retained - k) % 2:
        observations = observations[:-1]
    radius = (len(observations) - k) // 2
    vanishing = [1]
    for a, _ in observations:
        vanishing = _times(F, vanishing, [F.neg(a), 1])
    values = [0] * len(observations)
    for a, y in observations:
        if y:
            quotient, _ = _divmod(F, vanishing, [F.neg(a), 1])
            scale = F.mul(y, F.inverse(_eval(F, quotient, a)))
            for j, coeff in enumerate(quotient):
                values[j] = F.add(values[j], F.mul(coeff, scale))
    previous, remainder = vanishing, _trim(values)
    v_prev, v = [], [1]
    while len(remainder) > k + radius:
        quotient, next_rem = _divmod(F, previous, remainder)
        v_prev, v = v, _sub(F, v_prev, _times(F, quotient, v))
        previous, remainder = remainder, next_rem
    if not v:
        return None
    poly, rem = _divmod(F, remainder, v)
    return None if rem or len(poly) > k else poly


class ConcatenatedOuter:
    def __init__(self, bits, z):
        self.bits = bits
        self.z = z
        self.b, self.k, self.length, self.t = concat_shape(bits, z)
        self.groups = self.b // 6
        self.field = _field(self.b)

    def encode(self, message):
        if type(message) is not int or message < 0 or message.bit_length() > self.bits:
            raise ValueError('message outside the fixed bit width')
        poly = []
        while message:
            message, digit = divmod(message, self.field.order)
            poly.append(digit)
        inner = _inner_words()
        result = []
        for a in range(self.length):
            symbol = _eval(self.field, poly, a)
            for _ in range(self.groups):
                symbol, part = divmod(symbol, 729)
                result.extend(inner[part])
        return tuple(result)

    def decode(self, trits):
        try:
            word = tuple(trits)
        except TypeError:
            return None
        if len(word) != self.t or any(type(x) is not int or not 0 <= x < 3 for x in word):
            return None
        symbols = []
        stride = 12*self.groups
        for start in range(0, len(word), stride):
            distance = symbol = 0
            place = 1
            for j in range(start, start+stride, 12):
                part, cost = _nearest(word[j:j+12])
                symbol += place*part
                place *= 729
                distance += cost
            symbols.append((symbol, distance))

        # Forney thresholds: a block at nearest distance 0/1/2 is retained
        # in respectively 3/2/1 trials. Other blocks are always erased.
        previous_count = None
        for threshold in (3, 2, 1):
            retained = [(a, symbol) for a,(symbol,cost) in enumerate(symbols)
                        if cost < threshold]
            if len(retained) < self.k:
                break
            if len(retained) == previous_count:
                continue
            previous_count = len(retained)
            poly = _recover(self.field, self.k, retained)
            if poly is None:
                continue
            message = 0
            for coeff in reversed(poly):
                message = message*self.field.order + coeff
            if message.bit_length() <= self.bits:
                candidate = self.encode(message)
                if sum(x != y for x, y in zip(word, candidate)) <= self.z:
                    return message
        return None
