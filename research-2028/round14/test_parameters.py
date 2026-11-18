"""Independent tiny-instance checks for arithmetic-only size budgeting."""
import unittest
from fractions import Fraction
from math import comb

from differential_pke import Params
from differential_kem import DifferentialKEM
from outer_code import rs_shape
from parameters import Layout, illustration, mixed_rank_bytes, outer_shape, support_bytes
from seeded_matrix import SeededMatrixKEM


def integer_width(count):
    return ((count - 1).bit_length() + 7) // 8


class SizeTests(unittest.TestCase):
    def test_certified_width_matches_exact_rank_count(self):
        for trits in (0, 1, 2, 5, 13, 63, 128, 1024):
            for m in (1, 2, 255, 256, 257, 65536, 2**83 + 1):
                self.assertEqual(mixed_rank_bytes(trits, m), integer_width(3**trits*m))

    def test_support_slot_aggregation(self):
        for m, w, t in ((1, 1, 1), (70, 1, 70), (400, 3, 100), (900, 11, 70)):
            expected = sum(integer_width(comb(m-i*w, w)*2**w) for i in range(t))
            self.assertEqual(support_bytes(m, w, t), expected)

    def test_shapes_and_wire_lengths_against_protocol(self):
        for bits, z in ((1, 0), (3, 1), (6, 3), (8, 2)):
            self.assertEqual(outer_shape(bits, z), rs_shape(bits, z))
            for outer in ('repeat', 'rs'):
                p = Params(bits, 3, 2, 200, 2, z, 5, outer)
                u = 3
                kem = DifferentialKEM(p, u)
                sizes = Layout(bits, p.h, p.n, p.m, p.w, z, p.t, p.slack, u).sizes()
                self.assertEqual((sizes['pk'], sizes['sk'], sizes['ct'], sizes['shared']),
                                 (kem.public_bytes, kem.private_bytes, kem.ciphertext_bytes, kem.key_bytes))
                self.assertEqual((sizes['coins'], sizes['body'], sizes['supports']),
                                 (p.coin_bytes, p.body_bytes, p.private_bytes))

    def test_published_row_totals(self):
        rows = {
            128: (18882418835572, 18882436172546, 3348787),
            192: (123590462639307, 123590509085920, 8567191),
            256: (389648968566839, 389649053026405, 15210996),
        }
        for b, expected in rows.items():
            layout = illustration(b)
            self.assertEqual(outer_shape(layout.bits, layout.z), rs_shape(layout.bits, layout.z))
            data = layout.sizes()
            self.assertEqual((data['pk'], data['sk'], data['ct']), expected)
            self.assertLess(data['d'], data['key_dsd_length'])
            self.assertLess(layout.h, data['N'])
            self.assertEqual(data['seeded_pk'], 32 + data['with_crs_pk'])
            self.assertEqual(data['seeded_sk'], 32 + data['supports'])

    def test_192_conditional_guessing_bounds(self):
        layout = illustration(192)
        rows = layout.h + layout.n * (layout.n + 1) // 2
        queries = 2**191
        seed_slack = layout.bits + 64

        def inverse_power(bits):
            return Fraction(1, 2**bits)

        half_message = inverse_power(layout.bits // 2)
        half_nonce = inverse_power(4 * layout.nonce_bytes)
        tail = (16 * (2*queries) * half_message
                + 48 * queries * (5*queries) * half_nonce
                + 2 * queries * inverse_power(layout.bits)
                + 4 * queries * half_message
                + 2 * layout.t * inverse_power(seed_slack))
        self.assertLess(tail, inverse_power(57))

        for assumed_bits, base_bits, leading_bits, guessing_limit in (
            (224, 208, 5, Fraction(516, 1000)),
            (280, 264, 33, Fraction(1, 2) + inverse_power(33)),
        ):
            base_gap = ((2*layout.t + 2) * inverse_power(assumed_bits)
                        + 2 * inverse_power(layout.slack)
                        + 2 * rows * inverse_power(seed_slack))
            self.assertLess(base_gap, inverse_power(base_bits))
            self.assertLess(64 * (2*queries) * base_gap, inverse_power(2*leading_bits))
            guessing_bound = (1 + inverse_power(leading_bits) + tail) / 2
            self.assertLess(guessing_bound, guessing_limit)

    def test_small_documented_wire_sizes(self):
        p = Params(8, 3, 2, 80, 2, 2, 32, 'rs')
        kem = DifferentialKEM(p, nonce_bytes=8)
        public, private = kem.keygen()
        ct, shared = kem.encaps(public)
        self.assertEqual((len(public), len(private), len(ct), p.coin_bytes), (112, 140, 27, 7))
        self.assertEqual(kem.decaps(private, ct), shared)
        seeded = SeededMatrixKEM(p, nonce_bytes=8)
        public, private = seeded.keygen()
        ct, shared = seeded.encaps(public)
        self.assertEqual((len(public), len(private), len(ct)), (49, 60, 27))
        self.assertEqual(seeded.decaps(private, ct), shared)


if __name__ == '__main__':
    unittest.main()
