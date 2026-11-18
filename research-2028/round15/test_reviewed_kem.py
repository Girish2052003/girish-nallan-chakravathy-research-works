"""External ML-KEM known answers and agreement through the public interface."""
from base64 import b64decode
import hashlib
import json
from pathlib import Path
import unittest

from reviewed_kem import MLKEM


class StandardKEMTests(unittest.TestCase):
    def test_external_known_answers(self):
        vectors = json.loads(Path(__file__).with_name("reviewed_vectors.json").read_text())
        for name, vector in vectors.items():
            with self.subTest(profile=name):
                kem = MLKEM(int(name))
                pk = kem.public_from_private(bytes.fromhex(vector["acvp_seed"]))
                self.assertEqual(hashlib.sha256(pk).hexdigest(), vector["acvp_ek_sha256"])
                recovered = kem.decaps(bytes.fromhex(vector["decaps_seed"]),
                                       b64decode(vector["ct_base64"], validate=True))
                self.assertEqual(recovered, bytes.fromhex(vector["shared"]))

    def test_full_parameter_sets(self):
        for n, pk_len, ct_len in ((512,800,768), (768,1184,1088), (1024,1568,1568)):
            with self.subTest(profile=n):
                kem = MLKEM(n)
                public, seed = kem.keygen()
                ciphertext, secret = kem.encaps(public)
                self.assertEqual((len(public), len(seed), len(ciphertext), len(secret)),
                                 (pk_len, 64, ct_len, 32))
                self.assertEqual(kem.public_from_private(seed), public)
                self.assertEqual(kem.decaps(seed, ciphertext), secret)
                # FIPS 203's implicit rejection under the all-zero test ciphertext.
                empty_body = bytes(ct_len)
                expected = hashlib.shake_256(seed[32:] + empty_body).digest(32)
                self.assertEqual(kem.decaps(seed, empty_body), expected)
                self.assertIsNone(kem.decaps(seed, ciphertext[:-1]))

    def test_encoding_errors(self):
        with self.assertRaises(ValueError):
            MLKEM(192)
        kem = MLKEM(768)
        with self.assertRaises(ValueError):
            kem.public_from_private(bytes(63))
        with self.assertRaises(ValueError):
            kem.encaps(bytes(1183))
        with self.assertRaises(ValueError):
            kem.encaps(bytes([255])*1184)


if __name__ == "__main__":
    unittest.main()
