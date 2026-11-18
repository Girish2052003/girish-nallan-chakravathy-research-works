from hashlib import shake_256
from itertools import product
import unittest

from binary_bridge import BinarySystematic, read_instance
from differential_bridge import lift_preimage, verify_witness


class BinaryBridgeTests(unittest.TestCase):
    def test_boolean_xor_weight_and_cubic_fibers(self):
        system = BinarySystematic(4, 2, bytes((3,1)))
        circuit = system.circuit()
        potential, _ = system.compile(b'\0', 0)
        self.assertLessEqual(max((len(m) for p in potential.outputs for m,_ in p.terms), default=0), 3)
        for e in product(range(3), repeat=4):
            trace = circuit.trace(e)
            actual = circuit.evaluate(e)
            target = tuple(actual)
            if max(e) > 1:
                self.assertTrue(any(actual[:4]))
                target = (0,)*4 + actual[4:]
                point = (0,)*(1+len(target))+trace
                self.assertFalse(verify_witness(potential, target, point))
                continue
            word = bytes((sum(bit << j for j,bit in enumerate(e)),))
            c = bytes(((e[0]^e[2]^e[3]) + 2*(e[1]^e[2]),))
            self.assertEqual(system.encode(word), c)
            for weight in range(5):
                for syndrome in map(lambda v: bytes([v]), range(4)):
                    target = system.target(syndrome, weight)
                    ok = syndrome == c and weight == sum(e)
                    self.assertEqual(system.accepts(syndrome, weight, word), ok)
                    point = (0,)*(1+len(target))+trace
                    self.assertEqual(verify_witness(potential, target, point), ok)
                    if ok:
                        self.assertEqual(lift_preimage(circuit,target,e),point)
                        decoded, original, w = read_instance(potential,target)
                        self.assertEqual((decoded.public, original, w), (system.public,c,sum(e)))

    def test_real_classic_mceliece_public_encodings(self):
        from classic_kem import ClassicMcEliece
        for target, n, rows, weight in ((128,3488,768,64), (192,4608,1248,96),
                                        (256,6688,1664,128)):
            provider = ClassicMcEliece(target)
            public, secret = provider.keygen()
            # This deliberately public error pattern tests interoperability only.
            positions = [(j*n)//weight for j in range(weight)]
            error = sum(1 << j for j in positions).to_bytes((n+7)//8, 'little')
            system = BinarySystematic(n, rows, public)
            ciphertext = system.encode(error)
            self.assertTrue(system.accepts(ciphertext, weight, error))
            key = shake_256(bytes([1]) + error + ciphertext).digest(32)
            self.assertEqual(provider.decaps(secret, ciphertext), key)

    def test_mod_three_replacement_and_weight_three(self):
        s = BinarySystematic(4,1,b'\x07')
        # Four binary ones in one row give binary parity zero, ternary sum one.
        self.assertEqual(s.encode(b'\x0f'), b'\0')
        self.assertTrue(s.accepts(b'\1', 3, b'\x07'))
        self.assertFalse(s.accepts(b'\1', 0, b'\x07'))

    def test_multi_byte_packing_and_invalid_data(self):
        n, rows = 20,9
        masks = tuple((1 << 10) | (1 << j) for j in range(9))
        s = BinarySystematic(n, rows, b''.join(m.to_bytes(2,'little') for m in masks))
        error = (1 + (1<<19) + (1<<9)).to_bytes(3,'little')
        self.assertTrue(s.accepts(b'\xff\x01', 3, error))
        self.assertFalse(s.accepts(b'\xff\x81', 3, error))
        self.assertFalse(s.accepts(b'\xff\x01', 3, b'\0\0\x80'))
        self.assertFalse(s.accepts(b'\xff\x01', True, error))
        with self.assertRaises(ValueError):
            BinarySystematic(4,2,b'\x80\0')
        with self.assertRaises(ValueError):
            BinarySystematic(4,2,b'')
