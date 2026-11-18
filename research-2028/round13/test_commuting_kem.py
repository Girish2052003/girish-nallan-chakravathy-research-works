"""Finite checks of honest differential agreement from the four public values."""
from hashlib import shake_256
from itertools import product
from unittest.mock import patch
import unittest

from commuting_kem import CommutingKEM, Poly


def rank_bytes(values):
    value = 0
    for t in values:
        value = 3*value + t
    width = ((3**len(values) - 1).bit_length() + 7) // 8
    return value.to_bytes(width, 'big')


def digest(*fields):
    framed = b''.join(len(x).to_bytes(8, 'big') + x for x in fields)
    return shake_256(framed).digest(32)


def evaluate_wire(blob, n, degree, m, input_point):
    # Independent lexicographic monomial layout, constructed from exponent
    # vectors rather than from combinations of repeated variable indices.
    exponents = [v for v in product(range(3), repeat=n) if sum(v) <= degree]
    exponents.sort(key=lambda v: (sum(v), tuple(j for j in range(n) for _ in range(v[j]))))
    rank = int.from_bytes(blob, 'big')
    coefficients = [0] * (m*len(exponents))
    for i in reversed(range(len(coefficients))):
        rank, coefficients[i] = divmod(rank, 3)
    assert rank == 0
    values = []
    for v in exponents:
        t = 1
        for x, power in zip(input_point, v):
            t *= x**power
        values.append(t)
    width = len(values)
    return tuple(sum(a*b for a,b in zip(coefficients[i:i+width], values)) % 3
                 for i in range(0,len(coefficients),width))


class CommutingTests(unittest.TestCase):
    def test_all_two_variable_shifts_and_canonical_coefficients(self):
        x, y = Poly.variable(0), Poly.variable(1)
        params = (x*x*y+2*y*y+1, x*y+y)
        sender, receiver = CommutingKEM(2, params), CommutingKEM(2, params)

        def expected(t):
            u, v = t
            return ((u*u*v+2*v*v+1)%3, (u*v+v)%3)

        points = list(product(range(3), repeat=2))
        for b in points:
            with patch('commuting_kem.secrets.randbelow', side_effect=b):
                pk, sk = receiver.keygen()
            self.assertEqual(sk, rank_bytes(b))
            for t in points:
                end = expected(tuple((u+v)%3 for u,v in zip(t,b)))
                self.assertEqual(evaluate_wire(pk,2,2,2,t), tuple((v-u)%3 for u,v in zip(expected(t),end)))
            for a in points:
                with patch('commuting_kem.secrets.randbelow', side_effect=a):
                    ct, key = sender.encaps(pk)
                combined = expected(tuple((u+v)%3 for u,v in zip(a,b)))
                four_points = tuple((z-u-v+w)%3 for z,u,v,w in
                                    zip(combined,expected(a),expected(b),expected((0,0))))
                self.assertEqual(key, digest(b'SG-DIFRA/R13/commuting/kem/v1', sender.setup,
                                             pk, ct, rank_bytes(four_points)))
                self.assertEqual(key, receiver.decaps(sk, ct))
                self.assertEqual((len(pk),len(sk),len(ct),len(key)), (3,1,3,32))

    def test_all_univariate_quadratics_and_their_shifts(self):
        x = Poly.variable(0)
        for h, j, k in product((1,2), range(3), range(3)):
            kem = CommutingKEM(1, (h*x*x+j*x+k,))
            for b, a in product(range(3), repeat=2):
                with patch('commuting_kem.secrets.randbelow', side_effect=(b,a)):
                    pk, sk = kem.keygen()
                    ct, key = kem.encaps(pk)
                self.assertEqual(pk, rank_bytes(((h*b*b+j*b)%3, (2*h*b)%3)))
                self.assertEqual(ct, rank_bytes(((h*a*a+j*a)%3, (2*h*a)%3)))
                self.assertEqual(key, kem.decaps(sk, ct))

    def test_period_representatives_and_setup_binding(self):
        x = Poly.variable(0)
        p = x*x
        kem = CommutingKEM(2, (p,))
        with patch('commuting_kem.secrets.randbelow', side_effect=(1,0,1,2,2,1)):
            pk, sk1 = kem.keygen()
            pk2, sk2 = kem.keygen()
            ct, key = kem.encaps(pk)
        self.assertEqual(pk,pk2)
        self.assertNotEqual(sk1,sk2)
        self.assertEqual(kem.decaps(sk1,ct), key)
        self.assertEqual(kem.decaps(sk2,ct), key)
        shifted_constant = CommutingKEM(2,(p+1,))
        self.assertNotEqual(kem.setup,shifted_constant.setup)
        self.assertNotEqual(key,shifted_constant.decaps(sk2,ct))

    def test_layout_known_answer_and_malformed_bytes(self):
        x = Poly.variable(0)
        kem = CommutingKEM(1, (2*x*x+x+1,))
        with patch('commuting_kem.secrets.randbelow', side_effect=(2,1)):
            pk, sk = kem.keygen()
            ct, key = kem.encaps(pk)
        setup = digest(b'SG-DIFRA/R13/commuting/setup/v1', (1).to_bytes(8,'big'),
                       (1).to_bytes(8,'big'), b'\x02', b'\x0e')
        self.assertEqual(kem.setup, setup)
        self.assertEqual((pk, sk, ct), (b'\x05',b'\x02',b'\x01'))
        self.assertEqual(key, digest(b'SG-DIFRA/R13/commuting/kem/v1',setup,pk,ct,b'\x02'))
        self.assertEqual(kem.decaps(sk,ct), key)
        for invalid in (b'', b'\x00\x01', b'\x09', bytearray(ct)):
            with self.assertRaises(ValueError):
                kem.encaps(invalid)
            self.assertIsNone(kem.decaps(sk, invalid))
        with self.assertRaises(ValueError):
            kem.decaps(b'\x03', ct)
        for n, params in ((0,(x*x,)),(1,()),
                          (1,(x,)),(1,(Poly.variable(1)*x,))):
            with self.assertRaises(ValueError):
                CommutingKEM(n,params)


if __name__ == '__main__':
    unittest.main()
