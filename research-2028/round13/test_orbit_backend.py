"""Known-structure arithmetic checks for the masked cubic orbit experiment."""
from hashlib import sha256
from itertools import product
from math import gcd
from pathlib import Path
from random import Random
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'round11'))
from research_kem import PrivateKey, PublicKey, ResearchKEM
from orbit_backend import OrbitBackend, power_exponent
from planar_backend import _pack_dense, monomial_count, packed_width
from differential_bridge import cm14_public_circuit, compile_circuit, lift_preimage, verify_witness


def identity_private(n):
    block = tuple(int(i == j) for i in range(n) for j in range(n)) + (0,)*n
    inner = tuple(int(i == j) for i in range(n) for j in range(1, n)) + (0,)*n
    return _pack_dense(inner + block)


class OrbitBackendTests(unittest.TestCase):
    def test_every_point_after_independent_masks_and_bridge(self):
        rng = Random(90133)
        recv, send = OrbitBackend(4), OrbitBackend(4)
        with patch('orbit_backend.secrets.randbelow', side_effect=rng.randrange):
            pk, sk = recv.generate()
        self.assertEqual((len(pk), len(sk)), (25, 8))
        inner, outer = recv._masks(sk)
        circuit = cm14_public_circuit(4, pk)  # identical monomial-major cubic layout
        potential = compile_circuit(circuit, public_tag=pk)
        seen = set()
        field = recv.field
        for x in product(range(3), repeat=4):
            y = send.forward(pk, x)
            t = field.from_coeffs(inner.apply(x))
            expected = outer.apply(field.coeffs(field.power(t, 1+3+27)))
            self.assertEqual(y, expected)
            self.assertEqual(recv.inverse(sk, y), x)
            self.assertEqual(circuit.evaluate(x), y)
            self.assertTrue(verify_witness(potential, y, lift_preimage(circuit, y, x)))
            seen.add(y)
        self.assertEqual(len(seen), 81)
        self.assertIsNone(send._private_cache)
        self.assertEqual(OrbitBackend(4).public_from_private(sk), pk)

    def test_reapplying_independent_affines_reproduces_composed_map(self):
        rng = Random(7250)
        base, changed = OrbitBackend(4), OrbitBackend(4)
        with patch('orbit_backend.secrets.randbelow', side_effect=rng.randrange):
            pk, sk = base.generate()
            _, masks = changed.generate()
        inner, outer = base._masks(sk)
        input_mask, output_mask = changed._masks(masks)
        n = 4
        def encode_composition(left, right, omit_first_column=False):
            # Evaluate an affine composition on the origin and basis points.
            def act(x):
                return left.apply(right.apply(x))
            origin = act((0,)*n)
            cols = [act(tuple(int(i == j) for j in range(n))) for i in range(n)]
            if omit_first_column:
                self.assertEqual(tuple((a-b) % 3 for a,b in zip(cols[0], origin)), (1,0,0,0))
            return tuple((cols[j][i]-origin[i]) % 3 for i in range(n)
                         for j in range(int(omit_first_column), n)) + origin
        combined = _pack_dense(encode_composition(inner, input_mask, True) +
                               encode_composition(output_mask, outer))
        remasked = changed.public_from_private(combined)
        for x in product(range(3), repeat=n):
            self.assertEqual(changed.forward(remasked, x), output_mask.apply(base.forward(pk, input_mask.apply(x))))

    def test_scalar_normalization_preserves_public_function(self):
        # Start with an unrestricted mask pair, normalize its first input
        # column, and compare the complete canonical-key map to the original.
        rng = Random(4121)
        backend = OrbitBackend(4)
        n, f = backend.dimension, backend.field
        from orbit_backend import _random_mask
        with patch('orbit_backend.secrets.randbelow', side_effect=rng.randrange):
            raw_s, raw_t = _random_mask(n), _random_mask(n)
        def apply(mask, v):
            return tuple((mask[n*n+i] + sum(mask[i*n+j]*v[j] for j in range(n))) % 3
                         for i in range(n))
        scalar = f.from_coeffs(raw_s[i*n] for i in range(n))
        self.assertNotEqual(scalar, 1)
        def normalized_input(v):
            return f.coeffs(f.mul(f.inverse(scalar), f.from_coeffs(apply(raw_s, v))))
        def normalized_output(v):
            return apply(raw_t, f.coeffs(f.mul(f.power(scalar, backend.exponent), f.from_coeffs(v))))
        def encode(act, omit):
            origin = act((0,)*n)
            cols = [act(tuple(int(i == j) for j in range(n))) for i in range(n)]
            if omit:
                self.assertEqual(tuple((a-b) % 3 for a,b in zip(cols[0], origin)), (1,0,0,0))
            return tuple((cols[j][i]-origin[i]) % 3 for i in range(n) for j in range(int(omit),n)) + origin
        sk = _pack_dense(encode(normalized_input, True) + encode(normalized_output, False))
        pk = backend.public_from_private(sk)
        for x in product(range(3), repeat=n):
            y = apply(raw_t, f.coeffs(f.power(f.from_coeffs(apply(raw_s,x)), backend.exponent)))
            self.assertEqual(backend.forward(pk,x), y)

    def test_all_encapsulation_coins_and_codec(self):
        sender, receiver = ResearchKEM(OrbitBackend(4)), ResearchKEM(OrbitBackend(4))
        sk = identity_private(4)
        payload = receiver.backend.public_from_private(sk)
        key = PublicKey(sender.backend.suite, 4, payload)
        private = PrivateKey(receiver.backend.suite, 4, sk)
        self.assertEqual(sha256(payload).hexdigest(),
                         '1ad07db26f64f05683149b6d555a5374a3d7ffd26fa84baf3fb5e68d9dd1454d')
        for rank in range(81):
            with patch('research_kem.secrets.randbelow', return_value=rank):
                ct, ss = sender.encaps(key)
            self.assertEqual(receiver.decaps(private, ct), ss)
            self.assertEqual((len(ct), len(ss)), (1, 32))
            if rank == 17:
                self.assertEqual(ct.hex(), '16')
                self.assertEqual(ss.hex(),
                                 '550bfd67c49e9684a3c2040937bb7c90d61a9105e290bc9aa292e1a72c21c06c')
        for invalid in (b'', b'\x00\x00', bytes([81])):
            self.assertIsNone(receiver.decaps(private, invalid))
        foreign = OrbitBackend(4, (1, 2))
        self.assertNotEqual(foreign.suite, sender.backend.suite)
        with self.assertRaises(ValueError):
            ResearchKEM(foreign).encaps(key)
        for malformed in (payload + b'\0', bytes([255])*len(payload)):
            with self.assertRaises(ValueError):
                receiver.backend.validate_public(malformed)
        for malformed in (sk[:-1], bytes(len(sk))):
            with self.assertRaises(ValueError):
                receiver.backend.public_from_private(malformed)

    def test_actual_field_inverses_at_every_profile_without_large_public_keys(self):
        profile_data = (
            (82, 1_603_272, 2_681, 17), (122, 7_677_285, 5_922, 25),
            (163, 24_171_671, 10_561, 33), (164, 24_764_906, 10_690, 33),
            (244, 119_928_669, 23_639, 49), (325, 375_211_457, 41_918, 65),
        )
        for n, pk, sk, ct in profile_data:
            backend = OrbitBackend(n)
            i, j = backend.indices
            self.assertEqual(gcd(n, i, j), 1)
            self.assertTrue(all(t % n for t in (i+j, 2*i-j, 2*j-i)))
            self.assertEqual((packed_width(n*monomial_count(n)), packed_width(2*n*n+n), packed_width(n)),
                             (pk, sk, ct))
            f = backend.field
            y = f.from_coeffs((k*k+2) % 3 for k in range(n))
            x = f.power(y, backend.inverse_exponent)
            self.assertEqual(f.power(x, backend.exponent), y)
        with self.assertRaises(ValueError):
            power_exponent(3, 1, 2)
        with self.assertRaises(ValueError):
            OrbitBackend(4, (2, 2))


if __name__ == '__main__':
    unittest.main()
