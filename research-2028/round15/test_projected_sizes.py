from itertools import combinations, product
import unittest

from projected_sizes import engineering_example, limits_for_profile, outer_length_floor, rebalanced_example
from projected_kem import research_profile


class ProjectedSizeTests(unittest.TestCase):
    def test_ternary_length_floor_on_small_codes(self):
        for n, bits in ((2, 1), (2, 2), (3, 1), (3, 2)):
            words = list(product(range(3), repeat=n))
            for code in combinations(words, 2**bits):
                distance = min(sum(x != y for x, y in zip(a, b)) for a, b in combinations(code, 2))
                self.assertLessEqual(outer_length_floor(bits, (distance - 1)//2), n)

    def test_three_preserved_layouts_and_floors(self):
        expected = (
            (128, 3564, 3981553087, 80, 2216336, 2540, 2837548254, 2060325),
            (192, 5256, 15022416160, 96, 5482436, 3772, 10780846923, 5143442),
            (256, 6960, 35323168790, 112, 9722492, 5005, 25401132614, 9127173),
        )
        for target, t, pk, sk, ct, t_floor, pk_floor, ct_floor in expected:
            kem = research_profile(target)
            self.assertEqual((kem.t, kem.public_bytes, kem.private_bytes, kem.ciphertext_bytes),
                             (t, pk, sk, ct))
            floor = limits_for_profile(target)
            self.assertEqual((floor['t'], floor['public'], floor['ciphertext']),
                             (t_floor, pk_floor, ct_floor))
            self.assertEqual(floor['r'], kem.m - (kem.t-1)*kem.source.w)
            self.assertLessEqual(floor['public'], kem.public_bytes)
            self.assertLessEqual(floor['ciphertext'], kem.ciphertext_bytes)

    def test_different_source_and_engineering_layouts(self):
        for target, pk, ct in ((128, 1294315463, 1085357), (192, 4222727200, 2400356),
                               (256, 9872992406, 4237558)):
            resized = rebalanced_example(target)
            self.assertEqual((resized.public_bytes, resized.ciphertext_bytes), (pk, ct))
            self.assertEqual(resized.m, 2*resized.t*resized.source.w)
            old = research_profile(target).source
            self.assertNotEqual(resized.source.h, old.h)
            self.assertNotEqual(resized.source.N, old.N)
        example = engineering_example()
        self.assertEqual((example.public_bytes, example.private_bytes, example.ciphertext_bytes),
                         (62573, 64, 1273))
