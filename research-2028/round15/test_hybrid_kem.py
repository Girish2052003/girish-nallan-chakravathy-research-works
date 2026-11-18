"""Wire parsing, transcript independence, component agreement and combiner checks."""
from hashlib import sha3_384
import unittest

from hybrid_kem import HybridKEM, ParallelKEM, _OUTPUT, _hash


def independent_digest(fields):
    transcript = b"".join(len(field).to_bytes(8, "big") + field for field in fields)
    return sha3_384(transcript).digest()[:32]


class HybridTests(unittest.TestCase):
    def test_transcript_known_answer(self):
        fields = (bytes(range(32)), bytes(range(32, 64)), b"first-c", b"second-c",
                  b"first-pk", b"second-pk", b"example suite")
        expected = bytes.fromhex("e31034d2c741151939d9de4660ece8ebfa5b54056b880ca765554958a617c7c9")
        self.assertEqual(_hash(_OUTPUT, *fields), expected)
        self.assertEqual(expected, independent_digest((_OUTPUT, *fields)))
        self.assertNotEqual(_hash(_OUTPUT, b"a", b"bc"), _hash(_OUTPUT, b"ab", b"c"))

    def test_profiles_and_independent_matched_transcripts(self):
        for profile, public_width, ct_width in ((512, 1332, 963), (768, 1716, 1283),
                                               (1024, 2100, 1763)):
            with self.subTest(profile=profile):
                kem = HybridKEM(profile)
                public, private = kem.keygen()
                ct, shared = kem.encaps(public)
                self.assertEqual((len(public), len(private), len(ct), len(shared)),
                                 (public_width, 128, ct_width, 32))
                self.assertEqual(kem.decaps(private, ct), shared)
                anchor = kem.anchor
                c1, c2 = ct[:anchor.ciphertext_bytes], ct[anchor.ciphertext_bytes:]
                p1, p2 = public[:anchor.public_bytes], public[anchor.public_bytes:]
                k1 = anchor.decaps(private[:anchor.private_bytes], c1)
                k2 = kem.native.decaps(private[anchor.private_bytes:], c2)
                self.assertEqual(shared, independent_digest((_OUTPUT, k1, k2, c1, c2, p1, p2, kem.suite)))
                self.assertIsNone(kem.decaps(private, ct[:-1]))
                self.assertIsNone(kem.decaps(private, ct + b"\x00"))
                changed = c1 + bytes([c2[0] ^ 1]) + c2[1:]
                self.assertIsNone(kem.decaps(private, changed))

    def test_component_mix_and_cache_mode(self):
        kem = HybridKEM(512)
        public, private = kem.keygen()
        a = kem.anchor
        c1, k1 = a.encaps(public[:a.public_bytes])
        c2, k2 = kem.native.encaps(public[a.public_bytes:])
        ct = c1 + c2
        direct = kem.decaps(private, ct)
        self.assertEqual(direct, independent_digest(
            (_OUTPUT, k1, k2, c1, c2, public[:a.public_bytes], public[a.public_bytes:], kem.suite)))
        cached = ParallelKEM(a)
        pk2, sk2 = cached.keygen()
        ct2, shared2 = cached.encaps(pk2)
        self.assertEqual(cached.decaps(sk2, ct2), shared2)
        self.assertEqual(cached.private_bytes, kem.private_bytes + 32)
        binding = independent_digest((b"SG-DIFRA/R15/parallel/public-bound/v1",
                                      public[:a.public_bytes], public[a.public_bytes:], cached.suite))
        result = cached.decaps(private + binding, ct)
        self.assertEqual(result, independent_digest((_OUTPUT, k1, k2, c1, c2, binding, cached.suite)))
        self.assertNotEqual(direct, result)
        with self.assertRaises(ValueError):
            kem.decaps(private + binding, ct)
        with self.assertRaises(ValueError):
            kem.encaps(public[:-1])
