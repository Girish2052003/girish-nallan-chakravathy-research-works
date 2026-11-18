"""Exact reduced-cubic compilation, serialization and KEM integration checks."""
from hashlib import sha256
from itertools import product
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round11"))
from research_kem import PublicKey, PrivateKey, ResearchKEM
from planar_backend import MaskedPlanarBackend, monomial_count, packed_width


class PlanarBackendTests(unittest.TestCase):
    def test_compiled_maps_match_and_invert_everywhere(self):
        for n, seeds in ((2, (2, 7)), (4, (3,))):
            for first in seeds:
                receiver = MaskedPlanarBackend(n)
                private = bytes([first]) + bytes(receiver.seed_bytes - 1)
                public = receiver.public_from_private(private)
                sender = MaskedPlanarBackend(n)  # never receives the seed
                maps = receiver._expand_secret(private)
                outputs = set()
                for x in product(range(3), repeat=n):
                    y = sender.forward(public, x)
                    self.assertEqual(y, receiver._secret_forward(maps, x))
                    self.assertEqual(receiver.inverse(private, y), x)
                    outputs.add(y)
                self.assertEqual(len(outputs), 3**n)
                self.assertIsNone(sender._secret)
                self.assertEqual(len(public), packed_width(n * monomial_count(n)))
                self.assertEqual(MaskedPlanarBackend(n).public_from_private(private), public)

    def test_canonical_formats_and_alternative_public_maps(self):
        n = 4
        backend = MaskedPlanarBackend(n)
        total = n * monomial_count(n)
        width = packed_width(total)
        # Rank zero is the constant-zero polynomial; syntax alone cannot
        # certify that an arbitrary external coefficient string is a permutation.
        self.assertEqual(backend.forward(bytes(width), (1, 2, 0, 1)), (0, 0, 0, 0))
        with self.assertRaises(ValueError):
            backend.validate_public((3**total).to_bytes(width, "big"))
        with self.assertRaises(ValueError):
            backend.validate_public(bytes(width + 1))
        with self.assertRaises(ValueError):
            backend.public_from_private(bytes(backend.seed_bytes - 1))
        with self.assertRaises(ValueError):
            MaskedPlanarBackend(3)
        with self.assertRaises(ValueError):
            backend.forward(bytes(width), (0, 1, 2, 3))

    def test_exact_profile_widths(self):
        # Cross the fast width path and verify it directly on manageable cases.
        for count in (1, 31, 4095, 4096, 4097, 8001, 100_003):
            self.assertEqual(packed_width(count), ((3**count - 1).bit_length() + 7)//8)
        for n, expected in ((82, 1_603_272), (122, 7_677_285), (163, 24_171_671)):
            self.assertEqual(packed_width(n * monomial_count(n)), expected)

    def test_known_answer(self):
        backend = MaskedPlanarBackend(4)
        kem = ResearchKEM(backend)
        with patch("planar_backend.secrets.token_bytes", return_value=bytes(range(16))):
            public, private = kem.keygen()
        with patch("research_kem.secrets.randbelow", return_value=4):
            ciphertext, shared = kem.encaps(public)
        self.assertEqual(sha256(public.encoded).hexdigest(),
                         "9b33e5757ea27cb95432e5c6514da04a602c52dcf922371fe753dae2c9f92a3b")
        self.assertEqual(ciphertext.hex(), "4c")
        self.assertEqual(shared.hex(),
                         "fbfc817ec81fc0f715d3bb2c5c8f6785497e92608f1e559e70b545d980bd8a34")
        self.assertEqual(kem.decaps(private, ciphertext), shared)

    def test_private_cache_switches_without_stale_public(self):
        backend = MaskedPlanarBackend(4)
        seeds = [bytes([i]) * backend.seed_bytes for i in (7, 11)]
        public_a = backend.public_from_private(seeds[0])
        public_b = backend.public_from_private(seeds[1])
        self.assertNotEqual(public_a, public_b)
        self.assertEqual(backend.public_from_private(seeds[0]), public_a)
        x = (0, 0, 2, 1)
        for pk, sk in zip((public_a, public_b), seeds):
            self.assertEqual(backend.inverse(sk, backend.forward(pk, x)), x)

    def test_kem_across_serialized_keys_and_public_only_sender(self):
        receiver = ResearchKEM(MaskedPlanarBackend(5))
        sender = ResearchKEM(MaskedPlanarBackend(5))
        public, private = receiver.keygen()
        public = PublicKey(public.suite, public.dimension, bytes(public.encoded))
        private = PrivateKey(private.suite, private.dimension, bytes(private.encoded))
        for _ in range(5):
            ct, shared = sender.encaps(public)
            self.assertEqual(receiver.decaps(private, ct), shared)
            self.assertEqual(len(shared), 32)
        self.assertIsNone(sender.backend._secret)
        self.assertIsNone(receiver.decaps(private, b""))
        self.assertIsNone(receiver.decaps(private, bytes([255])))


if __name__ == "__main__":
    unittest.main()
