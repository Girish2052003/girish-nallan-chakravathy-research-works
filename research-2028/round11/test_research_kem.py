"""Correctness and serialization tests only; the bundled backend is public-invertible."""

import itertools
import unittest
from unittest.mock import patch

from research_kem import (
    PrivateKey, PublicKey, PublicShearControl, ResearchKEM, pack, ternary_bytes, unpack,
)


class TernaryCodecTests(unittest.TestCase):
    def test_exhaustive_small_domain_and_all_one_byte_codes(self):
        for n in range(1, 7):
            digits = itertools.product(range(3), repeat=n)
            for rank, x in enumerate(digits):
                expected = rank.to_bytes(ternary_bytes(n), "big")
                self.assertEqual(pack(x), expected)
                self.assertEqual(unpack(expected, n), x)
            if ternary_bytes(n) == 1:
                for rank in range(3**n, 256):
                    with self.assertRaises(ValueError):
                        unpack(bytes([rank]), n)

    def test_minimal_width_and_invalid_vectors(self):
        for n in (1, 3, 5, 6, 80, 81, 121, 122, 161, 162, 255):
            width = ternary_bytes(n)
            self.assertLess(256 ** (width - 1), 3**n)
            self.assertLessEqual(3**n, 256**width)
            self.assertEqual(unpack(pack((2,)*n), n), (2,)*n)
        for trits in ((), (3,), (-1, 0), (True,), (1.0,)):
            with self.assertRaises(ValueError):
                pack(trits)
        for n in (0, -1, True):
            with self.assertRaises(ValueError):
                ternary_bytes(n)
        with self.assertRaises(ValueError):
            unpack(b"\x00\x01", 3)


class KEMTests(unittest.TestCase):
    def setUp(self):
        self.control = PublicShearControl(3)
        self.kem = ResearchKEM(self.control)

    def test_exhaustive_keys_inputs_and_literal_differences(self):
        vectors = tuple(itertools.product(range(3), repeat=3))
        for key_rank, b in enumerate(vectors):
            with patch("research_kem.secrets.randbelow", return_value=key_rank) as rng:
                pk, sk = self.kem.keygen()
                rng.assert_called_once_with(27)
            self.assertEqual(pk.encoded, pack(b))
            outputs = set()
            for rank, x in enumerate(vectors):
                with patch("research_kem.secrets.randbelow", return_value=rank) as rng:
                    ct, key = self.kem.encaps(pk)
                    rng.assert_called_once_with(27)
                outputs.add(ct)
                self.assertEqual(len(key), 32)
                self.assertEqual(self.kem.decaps(sk, ct), key)
                # Independent pointwise evaluation of P(s+1,x)-P(s,x).
                def potential(s):
                    return tuple((s*xi + s*bi + (s*x[0]*x[1] if i == 2 else 0)) % 3
                                 for i, (xi, bi) in enumerate(zip(x, b)))

                y = unpack(ct, 3)
                for s in range(3):
                    self.assertEqual(tuple((j-i) % 3 for i, j in zip(potential(s), potential((s+1)%3))), y)
            self.assertEqual(len(outputs), 27)

    def test_known_answer(self):
        with patch("research_kem.secrets.randbelow", side_effect=(21, 16)):
            pk, sk = self.kem.keygen()
            ct, key = self.kem.encaps(pk)
        self.assertEqual((pk.encoded.hex(), sk.encoded.hex(), ct.hex()), ("15", "0f", "00"))
        self.assertEqual(key.hex(), "f1e92c2a0982b717244afda29ab9b571239c738ab9bb9f1cb1a5b37faea733f1")
        self.assertEqual(self.kem.decaps(sk, ct), key)

    def test_invalid_inputs_and_canonical_ciphertexts(self):
        pk, sk = self.kem.keygen()
        for rank in range(256):
            key = self.kem.decaps(sk, bytes([rank]))
            self.assertEqual(key is None, rank >= 27)
        for invalid in (b"", b"\x00\x01", bytearray([0]), "00", None):
            self.assertIsNone(self.kem.decaps(sk, invalid))
        for malformed in (PublicKey(pk.suite, 4, pk.encoded),
                          PublicKey(b"else", 3, pk.encoded),
                          PublicKey(pk.suite, 3, b"\x1b"), sk):
            with self.assertRaises(ValueError):
                self.kem.encaps(malformed)
        for malformed in (PrivateKey(sk.suite, 2, sk.encoded), PrivateKey(sk.suite, 3, b"\xff"), pk):
            with self.assertRaises(ValueError):
                self.kem.decaps(malformed, b"\x00")
        with self.assertRaises(TypeError):
            ResearchKEM()
        with self.assertRaises(ValueError):
            PublicShearControl(2)
        with self.assertRaises(ValueError):
            self.control.forward(pk.encoded, (3, 0, 0))
        with self.assertRaises(ValueError):
            self.control.inverse(sk.encoded, (0,))

    def test_hash_binds_full_context_and_input(self):
        class AnotherSuite(PublicShearControl):
            @property
            def suite(self):
                return b"negative-control/context-test"

        def one_session(control, key_rank, x_rank):
            kem = ResearchKEM(control)
            with patch("research_kem.secrets.randbelow", side_effect=(key_rank, x_rank)):
                pk, sk = kem.keygen()
                ct, key = kem.encaps(pk)
            self.assertEqual(kem.decaps(sk, ct), key)
            return key

        # 3 and 4 trits both encode in one byte: only the dimension changes.
        values = [one_session(self.control, 0, 0),
                  one_session(PublicShearControl(4), 0, 0),
                  one_session(AnotherSuite(3), 0, 0),
                  one_session(self.control, 1, 0),
                  one_session(self.control, 0, 1)]
        self.assertEqual(len(set(values)), len(values))

    def test_serialized_key_roundtrips_and_real_sampler(self):
        for dimension, width in ((81, 17), (122, 25), (162, 33)):
            control = PublicShearControl(dimension)
            kem = ResearchKEM(control)
            pk, sk = kem.keygen()
            local_pk = PublicKey(control.suite, dimension, bytes(pk.encoded))
            local_sk = PrivateKey(control.suite, dimension, bytes(sk.encoded))
            ct, shared = kem.encaps(local_pk)
            self.assertEqual(kem.decaps(local_sk, ct), shared)
            self.assertEqual(tuple(map(len, (pk.encoded, sk.encoded, ct, shared))),
                             (width, width, width, 32))


if __name__ == "__main__":
    unittest.main()
