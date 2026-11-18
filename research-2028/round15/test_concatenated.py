import random
import unittest
from collections import Counter
from itertools import combinations, product

from concatenated import (ConcatenatedOuter, _EvaluationField, _field,
                          _inner_words, _leaders, _nearest, concat_shape)


class ConcatenatedTests(unittest.TestCase):
    def test_golay_weight_distribution_and_coset_leaders(self):
        words = _inner_words()
        self.assertEqual(len(set(words)), 729)
        self.assertEqual(Counter(sum(x != 0 for x in w) for w in words),
                         {0: 1, 6: 264, 9: 440, 12: 24})
        self.assertEqual(len(_leaders()), 729)
        for syndrome, (distance, _) in _leaders().items():
            sample = (0,)*6 + syndrome
            nearest, cost = _nearest(sample)
            self.assertEqual(cost, distance)
            self.assertEqual(sum(x != y for x,y in zip(words[nearest], sample)), cost)
        self.assertEqual(max(v[0] for v in _leaders().values()), 3)

    def test_tiny_code_all_messages_all_error_patterns(self):
        code = ConcatenatedOuter(2, 2)
        for message in range(4):
            clean = code.encode(message)
            for weight in (0, 1, 2):
                for indices in combinations(range(code.t), weight):
                    for errors in product((1, 2), repeat=weight):
                        word = list(clean)
                        for i, e in zip(indices, errors):
                            word[i] = (word[i] + e) % 3
                        self.assertEqual(code.decode(word), message)

    def test_less_reliable_blocks_need_erasure(self):
        for z, taken in ((8, 4), (11, 5)):
            code = ConcatenatedOuter(1, z)
            clean = list(code.encode(0))
            one_block = _inner_words()[1]
            indices = [i for i,v in enumerate(one_block) if v][:taken]
            for i in indices:
                clean[i] = clean[i+12] = one_block[i]
            self.assertEqual(_nearest(clean[:12]), (1, 6-taken))
            self.assertEqual(code.decode(clean), 0)

    def test_random_multisymbol_outer_messages(self):
        rng = random.Random(6097)
        code = ConcatenatedOuter(37, 18)
        for _ in range(12):
            msg = rng.getrandbits(37)
            clean = list(code.encode(msg))
            for i in rng.sample(range(code.t), code.z):
                clean[i] = (clean[i]+rng.choice((1,2))) % 3
            self.assertEqual(code.decode(clean), msg)
        smaller = ConcatenatedOuter(3, 1)
        self.assertIsNone(smaller.decode(_inner_words()[8]))
        for bad in (None, [3]*code.t, [True]*code.t, [], [0]*(code.t+1)):
            self.assertIsNone(code.decode(bad))
        with self.assertRaises(ValueError):
            code.encode(1 << code.bits)

    def test_full_target_outer_codes_at_requested_radius(self):
        for target in (128, 192, 256):
            rng = random.Random(1008 + target)
            code = ConcatenatedOuter(2*target + 128, 6*target)
            message = rng.getrandbits(code.bits)
            received = list(code.encode(message))
            for i in rng.sample(range(len(received)), code.z):
                received[i] = (received[i] + 1 + rng.randrange(2)) % 3
            self.assertEqual(code.decode(received), message)

    def test_field_acceleration_and_shapes(self):
        generic = _EvaluationField(6)
        fast = _field(6)
        for a in range(729):
            for b in (0, 1, 2, 5, 27, 121, 631, 728):
                self.assertEqual(fast.add(a,b), generic.add(a,b))
                self.assertEqual(fast.mul(a,b), generic.mul(a,b))
            if a:
                self.assertEqual(fast.mul(a, fast.inverse(a)), 1)
        for bits,z,expected in ((384,768,(6,41,297,3564)),
                                (512,1152,(6,54,438,5256)),
                                (640,1536,(6,68,580,6960)),
                                (1,2187,(12,1,730,17520))):
            self.assertEqual(concat_shape(bits,z), expected)
        # A larger extension groups multiple inner words for one field symbol.
        wider = ConcatenatedOuter(1, 2187)
        self.assertEqual(wider.encode(1)[:24], _inner_words()[1] + _inner_words()[0])
