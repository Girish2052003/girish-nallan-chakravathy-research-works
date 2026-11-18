"""Independent small-domain checks of the positive PKE construction."""
from collections import Counter
from itertools import combinations, product
from math import comb
import unittest
from unittest.mock import patch

from differential_pke import DifferentialPKE, Params


def pack(trits):
    rank = 0
    for trit in trits:
        rank = 3*rank + trit
    return rank.to_bytes(((3**len(trits)-1).bit_length()+7)//8, "big")


def unpack(encoded, length):
    rank = int.from_bytes(encoded, "big")
    digits = []
    for _ in range(length):
        rank, digit = divmod(rank, 3)
        digits.append(digit)
    assert rank == 0
    return digits[::-1]


class PKEChecks(unittest.TestCase):
    def test_all_coins_and_messages(self):
        p = Params(1, 1, 1, 3, 1, 1)
        pke = DifferentialPKE(p)
        # Five independent uniform draws produce the three disjoint singleton
        # checks (three ranks) and the two base matrix rows (two ranks).
        with patch('differential_pke.secrets.randbelow', side_effect=(3, 2, 1, 7, 17)):
            pk, sk = pke.keygen()
        actual = Counter()
        for rank in range(p.coin_count):
            tape = rank.to_bytes(p.coin_bytes, "big")
            for bit in (0, 1):
                msg = bytes([bit])
                body = pke.encrypt(pk, msg, tape)
                self.assertEqual(pke.decrypt(sk, body), msg)
                actual[bit, body] += 1
        self.assertEqual(p.coin_count, 108)
        self.assertEqual(sum(actual.values()), 216)
        for bit in (0, 1):
            self.assertEqual(pke.encrypt(pk, bytes([bit]), bytes(p.coin_bytes)),
                             pke.encrypt(pk, bytes([bit]), p.coin_count.to_bytes(p.coin_bytes, "big")))

    def test_ordered_disjoint_secret_law(self):
        p = Params(2, 1, 1, 4, 2, 0)
        kem = DifferentialPKE(p)
        all_checks = set()
        for j, k in product(range(comb(4, 2)*4), range(4)):
            all_checks.add(kem._private_checks(bytes([j, k])))
        expected = set()
        for support in combinations(range(4), 2):
            remaining = sorted(set(range(4)) - set(support))
            for signs in product((1, -1), repeat=4):
                expected.add((tuple(zip(support, signs[:2])), tuple(zip(remaining, signs[2:]))))
        self.assertEqual(all_checks, expected)
        self.assertEqual(len(expected), 96)

    def test_known_body_against_clock_difference(self):
        p = Params(2, 1, 2, 8, 1, 1, 16)
        pke = DifferentialPKE(p)
        with patch('differential_pke.secrets.randbelow', side_effect=(0, 3, 5, 1, 2, 5,
                                                                     1, 550, 942, 6000)):
            pk, sk = pke.keygen()
        matrix = unpack(pk, p.d*p.N)
        # Independent signed supports decoded by hand from the sequential ranks.
        checks = (((0, 1),), ((2, -1),), ((4, -1),), ((1, -1),), ((5, 1),), ((7, -1),))
        self.assertEqual(pke._private_checks(sk), checks)
        rows = [matrix[i*p.N:(i+1)*p.N] for i in range(p.d)]
        for a in rows:
            self.assertEqual(a[p.m:], [sum(sign*a[j] for j, sign in C) % 3 for C in checks])
        def potential(s, u, x, y):
            return [(s*(u*rows[0][j] + x*x*rows[1][j] + x*y*rows[2][j] +
                        y*y*rows[3][j])) % 3 for j in range(p.N)]
        for u, x, y in product(range(3), repeat=3):
            phi_rank = 9*u+3*x+y
            for pos, sign in product(range(p.N), (1, -1)):
                rank = phi_rank * (2*p.N) + 2*pos + int(sign < 0)
                ciphertext = pke.encrypt(pk, b'\x02', rank.to_bytes(p.coin_bytes, "big"))
                expected = [(v-w) % 3 for v, w in zip(potential(2,u,x,y), potential(1,u,x,y))]
                expected[p.m:p.m+3] = [(v+1) % 3 for v in expected[p.m:p.m+3]]
                expected[pos] = (expected[pos]+sign) % 3
                self.assertEqual(pack(expected), ciphertext)
                self.assertEqual(pke.decrypt(sk, ciphertext), b'\x02')

    def test_validation_and_impossible_majority(self):
        for args in ((2,1,1,5,1,1), (0,1,1,6,1,1), (True,1,1,6,1,1),
                     (2,1,1,6,1,-1), (2,1,1,6,1,1,-1)):
            with self.assertRaises(ValueError):
                Params(*args)
        p = Params(2,1,1,6,1,1)
        pke = DifferentialPKE(p)
        pk, sk = pke.keygen()
        self.assertEqual(len(pk), p.public_bytes)
        self.assertEqual(len(sk), p.private_bytes)
        pke.validate_public(pk)
        pke.validate_private(sk)
        with self.assertRaises(ValueError):
            pke.validate_public((3**(p.N*p.d)).to_bytes(p.public_bytes, 'big'))
        with self.assertRaises(ValueError):
            pke.validate_private(bytes([255]) + sk[1:])
        with self.assertRaises(ValueError):
            pke.encrypt(pk, b'\x04', bytes(p.coin_bytes))
        with self.assertRaises(ValueError):
            pke.encrypt(pk, b'\x00', bytes(p.coin_bytes+1))
        for body in (b'', (3**p.N).to_bytes(p.body_bytes, 'big'), pack([0]*p.m+[2]*p.t)):
            self.assertIsNone(pke.decrypt(sk, body))

    def test_exhaustive_two_errors_with_overlapping_residual_damage(self):
        # Two errors in the same block, or two errors meeting different blocks,
        # must never prevent decoding all bits.
        p = Params(2, 1, 1, 10, 1, 2, 8)
        pke = DifferentialPKE(p)
        pk, sk = pke.keygen()
        for k in range(p.noise_count):
            body = pke.encrypt(pk, b'\x01', k.to_bytes(p.coin_bytes, 'big'))
            self.assertEqual(pke.decrypt(sk, body), b'\x01')

    def test_reed_solomon_body_all_single_errors(self):
        p = Params(2, 1, 1, 12, 2, 1, 8, 'rs')
        pke = DifferentialPKE(p)
        with patch('differential_pke.secrets.randbelow', side_effect=lambda bound: bound // 3):
            pk, sk = pke.keygen()
        for value, error_rank in product(range(4), range(p.noise_count)):
            msg = bytes([value])
            rank = 5 * p.noise_count + error_rank
            body = pke.encrypt(pk, msg, rank.to_bytes(p.coin_bytes, 'big'))
            self.assertEqual(pke.decrypt(sk, body), msg)


if __name__ == '__main__':
    unittest.main()
