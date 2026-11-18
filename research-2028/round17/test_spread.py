"""Finite checks of body spread with a fixed public key, message and sender input."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round16"))
from matched_kem import research_profile as matched_profile
from spread import projected_body_spread, quotient_body_spread


def signed_errors(length, weight):
    for support in combinations(range(length), weight):
        for signs in product((1, 2), repeat=weight):
            vector = [0] * length
            for i, sign in zip(support, signs):
                vector[i] = sign
            yield tuple(vector)


class BodySpread(unittest.TestCase):
    def test_projected_atoms_and_certificate(self):
        for length in range(1, 7):
            for w in range(length + 1):
                errors = tuple(signed_errors(length, w))
                for kept in range(length + 1):
                    counts = Counter(e[:kept] for e in errors)
                    for vector, count in counts.items():
                        hidden = w - sum(v != 0 for v in vector)
                        self.assertEqual(count, comb(length-kept, hidden) << hidden)
                    upper = Fraction(9 * max(counts.values()), 8 * len(errors))
                    bits = projected_body_spread(length, kept, w, 3)
                    self.assertLessEqual(min(1, upper), Fraction(1, 1 << bits))
                    self.assertGreater(upper, Fraction(1, 1 << (bits+1)))

    def test_conditional_sampler_with_a_partial_modulo_block(self):
        raw = Counter(divmod(tape % 18, 6) for tape in range(128))
        for sender_inputs in range(3):
            masses = [raw[sender_inputs, error] for error in range(6)]
            for mass in masses:
                self.assertLessEqual(Fraction(mass, sum(masses)), Fraction(1+4, 4*6))

    def test_quotient_fibers_including_deficient_keys(self):
        length, kept, w = 5, 3, 2
        errors = tuple(signed_errors(length, w))
        for row in product(range(3), repeat=kept):
            # A canonical coset label for the span of one row, including rank zero.
            counts = Counter(min(tuple((e[i]+a*row[i]) % 3 for i in range(kept))
                                 for a in range(3)) for e in errors)
            rank = int(any(row))
            k = length - kept + rank
            self.assertLessEqual(max(counts.values()),
                                 sum(comb(k, i) << i for i in range(min(k, w)+1)))
            bits = quotient_body_spread(length, kept, rank, w, 12)
            self.assertLessEqual(Fraction(max(counts.values()), len(errors)),
                                 Fraction(1, 1 << bits))
        self.assertEqual(quotient_body_spread(5, 3, 0, 2, 12),
                         projected_body_spread(5, 3, 2, 12))

    def test_registered_spread_and_minimum_nonce_widths(self):
        expected = {
            128: (1181184, (12467, 5971, 767, 0), (2467, 971, 550, 12)),
            192: (2656512, (19350, 9285, 1150, 0), (3673, 1446, 821, 10)),
            256: (4721664, (26424, 12694, 1534, 0), (4883, 1923, 1092, 8)),
        }
        from concatenated import concat_shape
        for target, (drop, full, short) in expected.items():
            kem = matched_profile(target)
            p = kem.source
            short_t = concat_shape(p.bits, p.w // 2)[3]
            short_n = kem.common_columns + (short_t - 1) * p.w + short_t
            self.assertEqual(p.N-short_n, drop)
            queries = 1 << (target - 1)
            for kept, (spread, exponent, quotient, nonce) in ((p.N, full), (short_n, short)):
                self.assertEqual(projected_body_spread(p.N, kept, p.w, p.slack), spread)
                self.assertEqual(quotient_body_spread(p.N, kept, p.d, p.w, p.slack), quotient)
                square = (240 * queries**2)**2
                self.assertLess(square << (2 * exponent), 1 << spread)
                self.assertGreaterEqual(square << (2 * (exponent+1)), 1 << spread)
                self.assertGreaterEqual(8 * nonce + quotient, 8 * kem.nonce_bytes)
                if nonce:
                    self.assertLess(8 * (nonce-1) + quotient, 8 * kem.nonce_bytes)

    def test_bad_message_blacklisting_count(self):
        for encryptions in product(range(2), repeat=3):
            for decoder in product(range(3), repeat=2):
                bad = sum(decoder[c] != m for m, c in enumerate(encryptions))
                for prior in (set(), {0}, {1}, {0, 1}):
                    self.assertLessEqual(sum(c in prior for c in encryptions), len(prior)+bad)
