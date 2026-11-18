"""End-to-end FO checks on the sampled ternary differential PKE."""
from hashlib import shake_256
import unittest
from unittest.mock import patch

from differential_kem import DifferentialKEM
from differential_pke import Params


TOY = Params(2, 2, 2, 12, 1, 1, 16)


def suite_encoding(p, nonce_bytes):
    fields = (p.bits, p.h, p.n, p.m, p.w, p.z, p.slack, nonce_bytes, 32)
    outer = p.outer.encode("ascii")
    return (b"SG-DIFRA/R14/differential-code/FO/v1"
            + b"".join(t.to_bytes(8, "big") for t in fields)
            + len(outer).to_bytes(8, "big") + outer)


def oracle(domain, suite, pk, message, length):
    data = b"".join(len(t).to_bytes(8, "big") + t for t in (domain, suite, pk, message))
    return shake_256(data).digest(length)


class KEMTests(unittest.TestCase):
    def test_all_messages_on_a_fresh_key(self):
        receiver, sender = DifferentialKEM(TOY), DifferentialKEM(TOY)
        pk, sk = receiver.keygen()
        self.assertEqual(sk[:TOY.public_bytes], pk)
        self.assertEqual((len(pk), len(sk)), (TOY.public_bytes, TOY.public_bytes + TOY.private_bytes))
        suite = suite_encoding(TOY, 32)
        seen = set()
        for rank in range(4):
            msg = bytes([rank])
            with patch("differential_kem.secrets.randbits", return_value=rank):
                c, key = sender.encaps(pk)
            tape = oracle(b"SG-DIFRA/R14/FO/G/v1", suite, pk, msg, 32 + TOY.coin_bytes)
            self.assertEqual(c[:32], tape[:32])
            self.assertEqual(c[32:], receiver.base.encrypt(pk, msg, tape[32:]))
            self.assertEqual(receiver.base.decrypt(sk[len(pk):], c[32:]), msg)
            self.assertEqual(key, oracle(b"SG-DIFRA/R14/FO/H/v1", suite, pk, msg, 32))
            self.assertEqual(receiver.decaps(sk, c), key)
            self.assertEqual((len(c), len(key)), (32 + TOY.body_bytes, 32))
            seen.add(c)
        self.assertEqual(len(seen), 4)

    def test_full_ciphertext_check_and_canonical_bytes(self):
        kem = DifferentialKEM(TOY, nonce_bytes=16)
        pk, sk = kem.keygen()
        with patch("differential_kem.secrets.randbits", side_effect=(1, 2)):
            c1, _ = kem.encaps(pk)
            c2, _ = kem.encaps(pk)
        self.assertNotEqual(c1[:16], c2[:16])
        self.assertIsNone(kem.decaps(sk, bytes([c1[0] ^ 1]) + c1[1:]))
        self.assertIsNone(kem.decaps(sk, c1[:16] + c2[16:]))
        first_unused_rank = (3**TOY.N).to_bytes(TOY.body_bytes, "big")
        self.assertIsNone(kem.decaps(sk, c1[:16] + first_unused_rank))
        for malformed in (b"", c1 + b"\x00", c1[:-1], bytearray(c1)):
            self.assertIsNone(kem.decaps(sk, malformed))
        for malformed in (b"", pk+b"\x00", bytearray(pk)):
            with self.assertRaises(ValueError):
                kem.encaps(malformed)
        with self.assertRaises(ValueError):
            kem.decaps(sk[:-1], c1)

    def test_outer_code_is_bound_to_the_complete_kem(self):
        p = Params(4, 1, 2, 64, 1, 2, 16, outer="rs")
        sender, receiver = DifferentialKEM(p, 16), DifferentialKEM(p, 16)
        pk, sk = receiver.keygen()
        for rank in range(16):
            with patch("differential_kem.secrets.randbits", return_value=rank):
                c, k = sender.encaps(pk)
            self.assertEqual(receiver.decaps(sk, c), k)
            self.assertEqual(len(c), 16 + p.body_bytes)
        repetition = DifferentialKEM(Params(4, 1, 2, 64, 1, 2, 16, outer="repeat"), 16)
        self.assertNotEqual(repetition.suite, sender.suite)
        self.assertEqual(sender.suite, suite_encoding(p, 16))

    def test_suite_binding_and_toy_known_answer(self):
        # The zero coefficient matrix is an admissible key generation outcome
        # and zero encodes the first private-support rank. Fresh nonzero keys
        # are exercised separately.
        pk = bytes(TOY.public_bytes)
        sk = pk + bytes(TOY.private_bytes)
        kem = DifferentialKEM(TOY)
        with patch("differential_kem.secrets.randbits", return_value=2):
            c, key = kem.encaps(pk)
        self.assertEqual(c.hex(), "582530e81285c4f5e48ba3a0cd6c21bdc20f087e601f6e9b89eaed74776d968d00000252")
        self.assertEqual(key.hex(), "39b33e2061b8d3b287109b8eb3aafb40a1d387f8524b5b4011f9d9099c41e028")
        self.assertEqual(kem.decaps(sk, c), key)
        different = DifferentialKEM(TOY, nonce_bytes=31)
        self.assertNotEqual(different.suite, kem.suite)
        self.assertIsNone(different.decaps(sk, c))
        for bad in (0, -1, False, 1 << 64):
            with self.assertRaises(ValueError):
                DifferentialKEM(TOY, bad)


if __name__ == "__main__":
    unittest.main()
