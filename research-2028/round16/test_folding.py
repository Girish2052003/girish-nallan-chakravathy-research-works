"""Finite algebra checks for folding supplied signed witnesses and padding their systems."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round14"))
from parameters import illustration


def signed_vectors(length, weight):
    for support in combinations(range(length), weight):
        for signs in product((1, 2), repeat=weight):
            vector = [0] * length
            for index, sign in zip(support, signs):
                vector[index] = sign
            yield tuple(vector)


def no_collision_probability(singles, doubles, weight):
    """Exact support count from coefficients of (1+X)^singles (1+2X)^doubles."""
    first = max(0, weight - singles)
    last = min(weight, doubles)
    if first > last:
        return Fraction(0)
    term = 2**first * comb(doubles, first) * comb(singles, weight-first)
    ways = term
    for i in range(first, last):
        term, remainder = divmod(term * 2 * (doubles-i) * (weight-i),
                                 (i+1) * (singles-weight+i+1))
        if remainder:
            raise ArithmeticError("support-count recurrence was not integral")
        ways += term
    return Fraction(ways, comb(singles + 2*doubles, weight))


class FoldingTests(unittest.TestCase):
    def test_exact_folded_law_and_lifting_given_witness(self):
        # H has three columns: the first member of a pair, a singleton, and
        # the second member of the pair. C contains the first two columns.
        for weight in (1, 2):
            frequencies = Counter()
            rank_failures = 0
            for entries in product(range(3), repeat=6):
                c0, c1, right = (entries[i:i+2] for i in (0, 2, 4))
                diff = tuple((y-x) % 3 for x, y in zip(c0, right))
                if diff == (0, 0):
                    rank_failures += 1
                    continue
                q = (-diff[1], diff[0])
                small_row = tuple(sum(a*b for a,b in zip(q, col)) % 3 for col in (c0,c1))
                for e in signed_vectors(3, weight):
                    if e[0] and e[2]:
                        continue
                    y = tuple((c0[i]*e[0] + c1[i]*e[1] + right[i]*e[2]) % 3
                              for i in range(2))
                    folded = ((e[0] + e[2]) % 3, e[1])
                    target = sum(a*b for a,b in zip(q, y)) % 3
                    # Lift the supplied folded witness through the retained full system.
                    pivot = 0 if diff[0] else 1
                    delta = y[pivot] - c0[pivot]*folded[0] - c1[pivot]*folded[1]
                    second = delta * pow(diff[pivot], -1, 3) % 3
                    self.assertEqual(((folded[0]-second) % 3, folded[1], second), e)
                    for order in ((0,1),(1,0)):
                        row = tuple(small_row[j] for j in order)
                        planted = tuple(folded[j] for j in order)
                        self.assertEqual(target, sum(a*b for a,b in zip(row, planted)) % 3)
                        frequencies[row, planted] += 1
            expected = {(row, e) for row in product(range(3), repeat=2)
                        for e in signed_vectors(2, weight)}
            self.assertEqual(set(frequencies), expected)
            self.assertEqual(len(set(frequencies.values())), 1)
            self.assertEqual(Fraction(rank_failures, 3**6), Fraction(1, 9))
            self.assertLess(Fraction(rank_failures, 3**6), Fraction(1, 2*3))

    def test_padding_preserves_the_entire_planted_law(self):
        counts = Counter()
        for row in product(range(3), repeat=2):
            for e in signed_vectors(2, 1):
                y = sum(a*b for a,b in zip(row, e)) % 3
                for extra in range(3):
                    for order in permutations(range(3)):
                        padded_row = tuple((row+(extra,))[i] for i in order)
                        padded_e = tuple((e+(0,))[i] for i in order)
                        self.assertEqual(sum(a*b for a,b in zip(padded_row,padded_e)) % 3, y)
                        counts[padded_row, padded_e] += 1
        self.assertEqual(len(counts), 3**3 * 6)
        self.assertEqual(len(set(counts.values())), 1)

    def test_collision_counts_against_enumeration(self):
        for singles in range(4):
            for doubles in range(1, 4):
                n = singles + 2*doubles
                for weight in range(n+1):
                    good = sum(all(not ({singles+2*i, singles+2*i+1} <= set(support))
                                   for i in range(doubles))
                               for support in combinations(range(n), weight))
                    self.assertEqual(no_collision_probability(singles, doubles, weight),
                                     Fraction(good, comb(n, weight)))

    def test_source_dimensions_and_profile_probabilities(self):
        expected = {128: (11271925, 14079669, 983399),
                    192: (28834120, 36020584, 985383),
                    256: (51192216, 63952664, 985364)}
        for b, (rows, length, millionths) in expected.items():
            source = illustration(b)
            d = source.h + source.n*(source.n+1)//2
            r = source.m - (source.t - 1)*source.w
            N = source.m + source.t
            self.assertEqual(rows, N-source.h)
            doubles = rows-d
            singles = r-doubles
            self.assertEqual(length, singles + 2*doubles)
            self.assertTrue(0 < rows < length < N)
            p = no_collision_probability(singles, doubles, source.w)
            self.assertEqual((10**6 * p.numerator) // p.denominator, millionths)
            union = Fraction(doubles*source.w*(source.w-1), length*(length-1))
            self.assertGreaterEqual(p, 1-union)
            # A square full-rank subset can contain the whole planted support.
            # Check the honest support mass exactly; no inversion routine is used.
            exponent_ceiling = {128: 247, 192: 370, 256: 494}[b]
            contained = comb(rows, source.w)
            all_supports = comb(length, source.w)
            self.assertGreater(contained << exponent_ceiling, all_supports)
            self.assertLess(contained << (exponent_ceiling - 1), all_supports)


if __name__ == "__main__":
    unittest.main()
