from math import comb
import unittest

from matched_kem import MatchedKEM, ProjectedKEM, research_profile


def unpack_trits(data, count):
    rank = int.from_bytes(data, "big")
    out = [0] * count
    for pos in reversed(range(count)):
        rank, out[pos] = divmod(rank, 3)
    if rank:
        raise ValueError("noncanonical trits")
    return out


class MatchedKEMTests(unittest.TestCase):
    def test_exact_widths_and_matching(self):
        # d, r, N and the three serialized sizes from independent arithmetic.
        table = {
            128: (5478678, 8209152, 10949100, 3868545931, 80, 2169320),
            192: (12119412, 18161280, 24220296, 12620284606, 96, 4798645),
            256: (21397976, 32067072, 42763056, 29506137220, 112, 8472375),
        }
        for target, expected in table.items():
            kem = research_profile(target)
            p = kem.source
            self.assertEqual((kem.common_rows, kem.common_columns, kem.N,
                              kem.public_bytes, kem.private_bytes, kem.ciphertext_bytes),
                             expected)
            self.assertEqual(kem.N-p.h, p.d)
            self.assertEqual(p.N, kem.N)
            self.assertEqual(p.t, kem.t)
            self.assertEqual(p.m, kem.m)
            self.assertEqual(kem.common_columns, kem.m-(kem.t-1)*p.w)
            self.assertLess(kem.common_rows, kem.common_columns)
            self.assertEqual(p.z, p.w)

    def test_direct_noise_including_last_position(self):
        kem = MatchedKEM(4, 1, 1, slack=24, nonce_bytes=8)
        p = kem.source
        self.assertEqual(p.noise_count, 2*comb(kem.N, 1))
        public, _ = kem.keygen()
        # Set all feature inputs zero and enumerate every signed error.
        clean = [0]*kem.m + list(kem._outer.encode(7))
        for position in range(kem.N):
            for sign_bit in (0, 1):
                noise_rank = 2*position + sign_bit
                coins = noise_rank.to_bytes(p.coin_bytes, "big")
                body = unpack_trits(kem._body(public, b"\x07", coins), kem.N)
                expected = clean[:]
                expected[position] = (expected[position]+1-2*sign_bit) % 3
                self.assertEqual(body, expected)

    def test_key_agreement_and_suite_binding(self):
        for bits, n, w in ((4, 1, 1), (8, 2, 2), (12, 3, 3)):
            kem = MatchedKEM(bits, n, w, nonce_bytes=8)
            other_suite = ProjectedKEM(kem.source, nonce_bytes=8)
            self.assertNotEqual(kem.suite, other_suite.suite)
            pk, sk = kem.keygen()
            ct, key = kem.encaps(pk)
            self.assertEqual(len(key), 32)
            self.assertEqual(kem.decaps(sk, ct), key)
            self.assertIsNone(kem.decaps(sk, ct[:-1]))
            self.assertIsNone(kem.decaps(sk, bytes([ct[0] ^ 1])+ct[1:]))
            self.assertIsNone(other_suite.decaps(sk, ct))

    def test_invalid_parameter_geometries(self):
        for args in ((1, 20, 1), (0, 1, 1), (4, 0, 1), (4, 1, 0), (True, 1, 1)):
            with self.assertRaises(ValueError):
                MatchedKEM(*args)
        with self.assertRaises(ValueError):
            research_profile(64)


if __name__ == "__main__":
    unittest.main()
