import unittest

from classic_kem import ClassicMcEliece, code_based_hybrid


class ClassicCompositionTests(unittest.TestCase):
    def test_library_and_parallel_wire_all_profiles(self):
        for target, sizes in ((128, (261652, 6588, 291)),
                              (192, (524692, 13704, 351)),
                              (256, (1045524, 14028, 403))):
            with self.subTest(target=target):
                kem = code_based_hybrid(target)
                pk, sk = kem.keygen()
                ct, sender = kem.encaps(pk)
                self.assertEqual((len(pk), len(sk), len(ct)), sizes)
                self.assertEqual(len(sender), 32)
                self.assertEqual(kem.decaps(sk, ct), sender)
                self.assertIsNone(kem.decaps(sk, ct[:-1]))
                # A fresh standard encapsulation under the same recipient's anchor key.
                standard = ClassicMcEliece(target)
                raw_ct, raw_key = standard.encaps(pk[:standard.public_bytes])
                self.assertEqual(standard.decaps(sk[:standard.private_bytes], raw_ct), raw_key)
                self.assertIsNone(standard.decaps(sk[:standard.private_bytes], b""))

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            ClassicMcEliece(0)
        from hybrid_kem import ParallelKEM
        simple = ClassicMcEliece(128)
        with self.assertRaises(ValueError):
            ParallelKEM(simple, cache_public=False)
        with self.assertRaises(ValueError):
            simple.encaps(b"")
        with self.assertRaises(ValueError):
            simple.decaps(b"", bytes(simple.ciphertext_bytes))
