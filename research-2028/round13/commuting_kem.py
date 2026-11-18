"""A correctness-only differential KEM. Its public transcript reveals its key.

The fixed potential is an ordered tuple of reduced ternary polynomials. The
only private operations below use the receiver's known shift. The reference
supports the exact coefficient layout specified in TRANSLATION_CLASSES.md.
"""
from hashlib import shake_256
from itertools import combinations_with_replacement
from pathlib import Path
import secrets
import sys

_ROUNDS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROUNDS / 'round9'))
sys.path.insert(0, str(_ROUNDS / 'round12'))
from differential_challenges import Poly
from planar_backend import _pack_dense, _unpack_dense, packed_width


SETUP_TAG = b'SG-DIFRA/R13/commuting/setup/v1'
KEM_TAG = b'SG-DIFRA/R13/commuting/kem/v1'


def _digest(*fields):
    state = shake_256()
    for value in fields:
        state.update(len(value).to_bytes(8, 'big'))
        state.update(value)
    return state.digest(32)


def _monomials(n, degree):
    return tuple(indices for k in range(degree + 1)
                 for indices in combinations_with_replacement(range(n), k)
                 if all(indices[i] != indices[i + 2] for i in range(k - 2)))


def _encode_polys(outputs, monomials):
    digits = bytearray()
    for poly in outputs:
        terms = dict(poly.terms)
        digits.extend(terms.get(monomial, 0) for monomial in monomials)
    return _pack_dense(digits)


def _delta_polys(outputs, shift):
    """Compute the published first difference from its known shift."""
    linear = [Poly.variable(i) + value for i, value in enumerate(shift)]
    translated_terms = {(): Poly({(): 1})}
    result = []
    for poly in outputs:
        shifted = Poly()
        for monomial, coefficient in poly.terms:
            for k in range(1, len(monomial) + 1):
                prefix = monomial[:k]
                if prefix not in translated_terms:
                    translated_terms[prefix] = translated_terms[prefix[:-1]] * linear[prefix[-1]]
            shifted += coefficient * translated_terms[monomial]
        result.append(shifted - poly)
    return tuple(result)


class CommutingKEM:
    """Honest protocol on a fixed public quadratic or cubic potential.

    All keys and ciphertexts are byte strings. The fixed setup is negotiated
    out of band. Fresh instances with the same setup interoperate.
    """

    def __init__(self, n, potential):
        if type(n) is not int or not 1 <= n < 2**64:
            raise ValueError('positive uint64 dimension required')
        outputs = tuple(potential)
        if not 1 <= len(outputs) < 2**64 or any(not isinstance(p, Poly) for p in outputs):
            raise ValueError('a nonempty list of ternary polynomials is required')
        if any(index >= n for p in outputs for term, _ in p.terms for index in term):
            raise ValueError('potential uses an undeclared variable')
        degree = max(p.degree for p in outputs)
        if degree not in (2, 3):
            raise ValueError('the reference handles quadratic and cubic potentials')
        self.n, self.m, self.degree = n, len(outputs), degree
        self.potential = outputs
        self.monomials = _monomials(n, degree - 1)
        self.coefficient_count = self.m * len(self.monomials)
        self.public_bytes = packed_width(self.coefficient_count)
        self.private_bytes = packed_width(n)
        self.ciphertext_bytes = self.public_bytes
        self.setup = _digest(SETUP_TAG, n.to_bytes(8, 'big'), self.m.to_bytes(8, 'big'),
                             bytes([degree]), _encode_polys(outputs, _monomials(n, degree)))

    def _sample(self):
        return tuple(secrets.randbelow(3) for _ in range(self.n))

    def _publish(self, shift):
        return _encode_polys(_delta_polys(self.potential, shift), self.monomials)

    def _shared_difference(self, coefficients, shift):
        # Evaluate Q(shift)-Q(0) directly from its coefficients; the constant
        # monomial contributes zero, so neither side needs its private peer.
        values = [0]
        for term in self.monomials[1:]:
            value = 1
            for i in term:
                value *= shift[i]
            values.append(value % 3)
        width = len(values)
        return tuple(sum(a*b for a, b in zip(coefficients[j*width:(j+1)*width], values)) % 3
                     for j in range(self.m))

    def keygen(self):
        b = self._sample()
        return self._publish(b), _pack_dense(b)

    def encaps(self, public):
        public_coefficients = _unpack_dense(public, self.coefficient_count)
        a = self._sample()
        ciphertext = self._publish(a)
        secret = self._shared_difference(public_coefficients, a)
        return ciphertext, _digest(KEM_TAG, self.setup, public, ciphertext, _pack_dense(secret))

    def decaps(self, private, ciphertext):
        b = _unpack_dense(private, self.n)
        try:
            ct_coefficients = _unpack_dense(ciphertext, self.coefficient_count)
        except ValueError:
            return None
        public = self._publish(b)
        secret = self._shared_difference(ct_coefficients, b)
        return _digest(KEM_TAG, self.setup, public, ciphertext, _pack_dense(secret))
