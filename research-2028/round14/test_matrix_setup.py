import unittest
from unittest.mock import patch

from differential_kem import DifferentialKEM
from differential_pke import Params, _pack_dense
from matrix_setup import SharedMatrixKEM, generate_setup


class SharedMatrixTests(unittest.TestCase):
    def test_exhaustive_small_key_distributions(self):
        # d=2, m=t=w=1. Exercise all nine matrices and both signed supports.
        p = Params(1, 1, 1, 1, 1, 0)
        for rank in range(9):
            with patch("matrix_setup.secrets.randbelow", return_value=rank):
                setup = generate_setup(p)
            adapter = SharedMatrixKEM(p, setup)
            for support_rank, sign in enumerate((1, -1)):
                with patch("differential_pke.secrets.randbelow", return_value=support_rank):
                    pub, secret = adapter.keygen()
                rows = divmod(rank, 3)
                expected = [v*sign % 3 for v in rows]
                self.assertEqual(pub, _pack_dense(expected))
                self.assertEqual(secret, bytes((support_rank,)))
                self.assertEqual(adapter.expand_public(pub),
                                 _pack_dense([rows[0], expected[0], rows[1], expected[1]]))

    def test_receiver_and_full_key_interoperate(self):
        for outer in ("rs", "repeat"):
            p = Params(3, 2, 2, 40, 2, 1, outer=outer)
            adapter = SharedMatrixKEM(p, generate_setup(p), nonce_bytes=8)
            full = DifferentialKEM(p, nonce_bytes=8)
            pub, sk = adapter.keygen()
            pk = adapter.expand_public(pub)
            self.assertEqual(len(pub), adapter.public_bytes)
            self.assertEqual(len(sk), adapter.private_bytes)
            for message in range(8):
                with patch("differential_kem.secrets.randbits", return_value=message):
                    c, k = adapter.encaps(pub)
                    self.assertEqual((c, k), full.encaps(pk))
                self.assertEqual(adapter.decaps(sk, c), k)
                self.assertEqual(full.decaps(pk+sk, c), k)
                self.assertIsNone(adapter.decaps(sk, bytes([c[0]^1]) + c[1:]))

    def test_noncanonical_inputs(self):
        p = Params(1, 1, 1, 1, 1, 0)
        with self.assertRaises(ValueError):
            SharedMatrixKEM(p, b'\xff')
        adapter = SharedMatrixKEM(p, b'\x01')
        for invalid in (b'', b'\xff'):
            with self.assertRaises(ValueError):
                adapter.encaps(invalid)
        self.assertIsNone(adapter.decaps(b'\x00', b''))


if __name__ == '__main__':
    unittest.main()
