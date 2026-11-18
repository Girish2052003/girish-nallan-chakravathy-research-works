"""Independent finite checks for the two-layer ternary research fixture."""
from collections import Counter
from itertools import combinations_with_replacement, product
from math import comb
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'round11'))
from research_kem import ResearchKEM, pack, unpack, ternary_bytes
from two_layer import TwoLayerBackend, public_monomials


def make_private(A, a, first, M, d, second, B, b):
    digits = []
    for matrix, translation, coefficients in ((A, a, first), (M, d, second), (B, b, ())):
        digits.extend(x for row in matrix for x in row)
        digits.extend(translation)
        digits.extend(coefficients)
    return pack(tuple(digits))


class TwoLayerTests(unittest.TestCase):
    def test_all_scalar_permutation_private_keys(self):
        backend = TwoLayerBackend(1)
        for A, M, B in product((1, 2), repeat=3):
            for a, d, b in product(range(3), repeat=3):
                secret = make_private(((A,),), (a,), (), ((M,),), (d,), (), ((B,),), (b,))
                public = backend.public_from_private(secret)
                self.assertEqual(unpack(public, 3), ((B*(M*a+d)+b) % 3, B*M*A % 3, 0))
                for x in range(3):
                    expected = ((B*(M*(A*x+a)+d)+b) % 3,)
                    self.assertEqual(backend.forward(public, (x,)), expected)
                    self.assertEqual(backend.inverse(secret, expected), (x,))

    def test_all_two_coordinate_swaps_and_shears(self):
        backend = TwoLayerBackend(2)
        identity = ((1, 0), (0, 1))
        swap = ((0, 1), (1, 0))
        a, d, b = (0, 2), (1, 0), (2, 1)
        for A, M, B in product((identity, swap), repeat=3):
            for p, q in product(range(3), repeat=2):
                secret = make_private(A, a, (p,), M, d, (q,), B, b)
                public = backend.public_from_private(secret)
                for x in product(range(3), repeat=2):
                    u, v = x if A == identity else x[::-1]
                    u, v = (u+a[0]) % 3, (v+a[1]) % 3
                    v = (v+p*u*u) % 3
                    if M == swap:
                        u, v = v, u
                    u, v = (u+d[0]) % 3, (v+d[1]) % 3
                    v = (v+q*u*u) % 3
                    if B == swap:
                        u, v = v, u
                    expected = ((u+b[0]) % 3, (v+b[1]) % 3)
                    self.assertEqual(backend.forward(public, x), expected)
                    self.assertEqual(backend.inverse(secret, expected), x)

    def test_canonical_reduction_of_cubes_and_true_quartics(self):
        for n in (3, 4):
            ident = tuple(tuple(int(i == j) for j in range(n)) for i in range(n))
            zero = (0,) * n
            if n == 3:
                # (x0)(x1+x0²) contributes x0 after reducing x0³.
                first = (1, 0, 0, 0)
                second = (0, 0, 1, 0)
                expected = {(2,): 1, (0, 1): 1, (0,): 1}
            else:
                # (x2+x0*x1)² contributes a genuine reduced degree-four term.
                first = (0, 0, 1, 0, 0, 0, 0, 0, 0, 0)
                second = (0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
                expected = {(3,): 1, (2, 2): 1, (0, 1, 2): 2, (0, 0, 1, 1): 1}
            secret = make_private(ident, zero, first, ident, zero, second, ident, zero)
            backend = TwoLayerBackend(n)
            public = backend.public_from_private(secret)
            terms = tuple(t for degree in range(5) for t in combinations_with_replacement(range(n), degree)
                          if all(t.count(i) <= 2 for i in range(n)))
            self.assertEqual(public_monomials(n), terms)
            self.assertEqual(len(terms), comb(n+4, 4) - n*(n+1))
            coefficients = unpack(public, n*len(terms))[-len(terms):]
            self.assertEqual({m: c for m, c in zip(terms, coefficients) if c}, expected)
            for x in product(range(3), repeat=n):
                if n == 3:
                    u, v, w = x
                    target = (u, (v+u*u) % 3, (w+u*(v+u*u)) % 3)
                else:
                    u, v, w, t = x
                    target = (u, v, (w+u*v) % 3, (t+(w+u*v)**2) % 3)
                self.assertEqual(backend.forward(public, x), target)
                self.assertEqual(backend.inverse(secret, target), x)

    def test_image_size_and_all_fibers(self):
        backend = TwoLayerBackend(3)
        for rank in range(4):
            secret = None
            if rank == 3:
                public, secret = backend.generate()
                self.assertEqual(backend.public_from_private(secret), public)
            else:
                public = backend.sample_lossy(rank)
            backend.validate_public(public)
            fibers = Counter()
            for x in product(range(3), repeat=3):
                y = backend.forward(public, x)
                fibers[y] += 1
                if secret is not None:
                    self.assertEqual(backend.inverse(secret, y), x)
            self.assertEqual(len(fibers), 3**rank)
            self.assertEqual(set(fibers.values()), {3**(3-rank)})

    def test_malformed_keys_vectors_and_ranks(self):
        for n in (0, True, 1 << 64):
            with self.assertRaises(ValueError):
                TwoLayerBackend(n)
        backend = TwoLayerBackend(2)
        for rank in (-1, 2, True):
            with self.assertRaises(ValueError):
                backend.sample_lossy(rank)
        public, secret = backend.generate()
        for operand, count, decode in ((public, 18, backend.validate_public),
                                       (secret, 20, backend.public_from_private)):
            self.assertEqual(len(operand), ternary_bytes(count))
            for invalid in (operand + b'\x00', (3**count).to_bytes(len(operand), 'big')):
                with self.assertRaises(ValueError):
                    decode(invalid)
        for invalid in ((0,), (0, 3), (False, 1)):
            with self.assertRaises(ValueError):
                backend.forward(public, invalid)
            with self.assertRaises(ValueError):
                backend.inverse(secret, invalid)
        # A canonical zero public map parses. Private inversion requires nonsingular matrices.
        self.assertEqual(backend.forward(bytes(len(public)), (1, 2)), (0, 0))
        with self.assertRaises(ValueError):
            backend.public_from_private(bytes(len(secret)))
        with self.assertRaises(ValueError):
            backend.inverse(bytes(len(secret)), (0, 0))

    def test_kem_round_trip_all_coins_and_rejection(self):
        receiver = ResearchKEM(TwoLayerBackend(3))
        sender = ResearchKEM(TwoLayerBackend(3))
        public, private = receiver.keygen()
        ciphertexts = set()
        for rank in range(27):
            with patch('research_kem.secrets.randbelow', return_value=rank):
                ciphertext, key = sender.encaps(public)
            ciphertexts.add(ciphertext)
            self.assertEqual(len(key), 32)
            self.assertEqual(receiver.decaps(private, ciphertext), key)
        self.assertEqual(len(ciphertexts), 27)
        for invalid in (b'', bytes([27]), bytes([255]), b'\x00\x00'):
            self.assertIsNone(receiver.decaps(private, invalid))


if __name__ == '__main__':
    unittest.main()
