import unittest

from profile_sizes import CAPACITY_TARGETS, profile_size


class ProfileSizeTests(unittest.TestCase):
    def test_three_profiles_at_exact_byte_boundaries(self):
        expected = ((81, 17), (122, 25), (162, 33))
        for bits, (trits, width) in zip(CAPACITY_TARGETS, expected, strict=True):
            with self.subTest(bits=bits):
                profile = profile_size(bits)
                self.assertEqual((profile.trits, profile.packed_vector_bytes), (trits, width))
                self.assertEqual(profile.domain_size, 3 ** trits)
                self.assertLess(3 ** (trits - 1), 2 ** bits)
                self.assertGreaterEqual(profile.domain_size, 2 ** bits)
                self.assertLess(256 ** (width - 1), profile.domain_size)
                self.assertGreaterEqual(256 ** width, profile.domain_size)
                record = profile.as_record()
                self.assertEqual(record["control_public_key_bytes"], width)
                self.assertEqual(record["control_private_key_bytes"], width)
                self.assertEqual(record["control_ciphertext_bytes"], width)
                self.assertEqual(record["shared_key_bytes"], 32)
                self.assertTrue(record["control_has_public_inverse"])

    def test_byte_transition_and_mean_rank(self):
        for bits, n, width in [(7, 5, 1), (8, 6, 2)]:
            with self.subTest(bits=bits):
                profile = profile_size(bits)
                self.assertEqual((profile.trits, profile.packed_vector_bytes), (n, width))
                size = 3 ** n
                self.assertEqual(profile.mean_blind_guesses * size, sum(range(1, size + 1)))

    def test_rejects_nonpositive_or_nonnumeric_target(self):
        for target in (0, -1, 128.5, True, "192"):
            with self.subTest(target=target), self.assertRaises(ValueError):
                profile_size(target)


if __name__ == "__main__":
    unittest.main()
