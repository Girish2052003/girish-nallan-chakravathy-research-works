"""Exact finite checks for centered orbit keys, the differential bridge and KEM."""
from itertools import product
from pathlib import Path
from random import Random
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'round11'))
from research_kem import ResearchKEM
from compact_orbit import CompactOrbitBackend, compact_public_circuit, compact_trit_count
from orbit_backend import OrbitBackend
from planar_backend import _pack_dense, _unpack_dense, monomial_count, packed_width
from differential_bridge import compile_circuit, lift_preimage, verify_witness


class CompactOrbitTests(unittest.TestCase):
    def test_all_inputs_dense_centered_and_bridge(self):
        n = 4
        receiver, sender, dense = CompactOrbitBackend(n), CompactOrbitBackend(n), OrbitBackend(n)
        with patch('orbit_backend.secrets.randbelow', side_effect=Random(811).randrange):
            public, private = receiver.generate()
        original = dense.public_from_private(private)
        circuit = compact_public_circuit(n, public)
        potential = compile_circuit(circuit, public_tag=public)
        inner, outer = receiver._masks(private)
        center, offset = inner.undo((0,) * n), outer.offset
        self.assertNotEqual(center, (0,) * n)
        digits = _unpack_dense(public, compact_trit_count(n))
        self.assertEqual(tuple(digits[:2*n]), center + offset)
        self.assertEqual(sender.forward(public, center), offset)
        self.assertEqual((len(original), len(public)), (25, 18))
        for x in product(range(3), repeat=n):
            y = dense.forward(original, x)
            self.assertEqual(sender.forward(public, x), y)
            self.assertEqual(circuit.evaluate(x), y)
            self.assertEqual(receiver.inverse(private, y), x)
            self.assertTrue(verify_witness(potential, y, lift_preimage(circuit, y, x)))
        self.assertIsNone(sender._private_cache)

    def test_two_distinct_private_presentations_have_identical_public_bytes(self):
        n = 4
        backend = CompactOrbitBackend(n)
        with patch('orbit_backend.secrets.randbelow', side_effect=Random(719).randrange):
            public, private = backend.generate()
        inner, outer = backend._masks(private)
        field = backend.field
        def frobenius(vector, power):
            return field.coeffs(field.power(field.from_coeffs(vector), power))
        def matrix_from_function(function, skip_first):
            offset = function((0,) * n)
            columns = [function(tuple(int(i == j) for i in range(n))) for j in range(n)]
            return tuple((columns[j][i] - offset[i]) % 3 for i in range(n)
                         for j in range(int(skip_first), n)) + offset
        # Frobenius fixes 1, preserves normalization and commutes with the
        # central monomial. Move it from the outer mask to the inner one.
        block1 = matrix_from_function(lambda x: frobenius(inner.apply(x), 3), True)
        block2 = matrix_from_function(lambda x: outer.apply(frobenius(x, 3**(n - 1))), False)
        alternate = _pack_dense(block1 + block2)
        self.assertNotEqual(private, alternate)
        self.assertEqual(backend.public_from_private(alternate), public)

    def test_wire_sizes_and_invalid_keys(self):
        for n, expected, saved in ((82, 1_548_004, 55_268), (122, 7_495_956, 181_329),
                                   (163, 23_740_067, 431_604), (164, 24_325_325, 439_581),
                                   (244, 118_483_795, 1_444_874), (325, 371_800_509, 3_410_948)):
            self.assertEqual(packed_width(compact_trit_count(n)), expected)
            self.assertEqual(packed_width(n * monomial_count(n)) - expected, saved)
        backend = CompactOrbitBackend(4)
        count = compact_trit_count(4)
        width = packed_width(count)
        for malformed in (b'', b'\x00' * (width + 1), (3**count).to_bytes(width, 'big'),
                          bytearray(width)):
            with self.assertRaises(ValueError):
                backend.validate_public(malformed)
            with self.assertRaises(ValueError):
                compact_public_circuit(4, malformed)
        with self.assertRaises(ValueError):
            backend.forward(bytes(width), (0, 1, 2, 3))

    def test_kem_interoperation_and_suite_separation(self):
        sender = ResearchKEM(CompactOrbitBackend(4))
        receiver = ResearchKEM(CompactOrbitBackend(4))
        with patch('orbit_backend.secrets.randbelow', side_effect=Random(721).randrange):
            public, private = receiver.keygen()
        for rank in range(81):
            with patch('research_kem.secrets.randbelow', return_value=rank):
                ct, key = sender.encaps(public)
            self.assertEqual(receiver.decaps(private, ct), key)
        for invalid in (b'', bytes([81]), b'\x00\x00'):
            self.assertIsNone(receiver.decaps(private, invalid))
        with self.assertRaises(ValueError):
            ResearchKEM(OrbitBackend(4)).encaps(public)
        self.assertIsNone(sender.backend._private_cache)


if __name__ == '__main__':
    unittest.main()
