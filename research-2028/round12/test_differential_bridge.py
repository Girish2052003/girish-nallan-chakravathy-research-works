"""Independent finite checks of the public circuit-to-difference compiler."""
from itertools import product
from pathlib import Path
from random import Random
import sys
import unittest
from unittest.mock import patch

from differential_bridge import (
    Affine, Multiply, Poly, Problem, TernaryCircuit, circuit_from_polynomials,
    cm14_public_circuit, compile_circuit, lift_preimage, read_public_tag,
    two_layer_public_circuit, verify_witness,
)
from planar_backend import MaskedPlanarBackend
from two_layer import TwoLayerBackend

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round11"))
from research_kem import PublicKey, PrivateKey, ResearchKEM, unpack


def full_collision_sets(problem):
    """Test-only oracle: compare both output vectors using sparse encoded terms."""
    encoding = problem.public_encoding()

    def value(point):
        output = []
        for component in encoding["outputs"]:
            result = 0
            for monomial, coefficient in component:
                term = coefficient
                for i in monomial:
                    term *= point[i]
                result += term
            output.append(result % 3)
        return tuple(output)

    space = tuple(product(range(3), repeat=len(encoding["variables"])))
    images = {point: value(point) for point in space}
    fibers = {}
    for c in product(range(3), repeat=encoding["challenge_coordinates"]):
        direction = (1,) + c + (0,) * encoding["response_coordinates"]
        fibers[c] = {
            p for p in space
            if images[p] == images[tuple((a+b) % 3 for a,b in zip(p, direction))]
        }
    return fibers


class DifferentialBridgeTests(unittest.TestCase):
    def test_rectangular_square_after_affine_complete_collision_sets(self):
        circuit = TernaryCircuit(2, (Affine(2, ((0, 1), (1, 2))), Multiply(2, 2)), (3,))
        problem = compile_circuit(circuit, b"\x00\xff\x80")
        self.assertEqual((problem.degree, problem.n_variables), (3, 6))
        self.assertEqual(len(problem.outputs), 2+2+2+24)
        actual = full_collision_sets(problem)
        expected = {(i,): set() for i in range(3)}
        for x0, x1 in product(range(3), repeat=2):
            a = (2+x0+2*x1) % 3
            c = (a*a % 3,)
            witness = (0, 0, x0, x1, a, c[0])
            self.assertEqual(lift_preimage(circuit, c, (x0,x1)), witness)
            self.assertTrue(verify_witness(problem, c, witness))
            expected[c].add(witness)
        self.assertEqual(actual, expected)
        self.assertEqual([len(actual[(i,)]) for i in range(3)], [3, 6, 0])

    def test_repeated_selected_output_and_unused_input(self):
        circuit = TernaryCircuit(2, (), (1,1))
        problem = compile_circuit(circuit)
        self.assertEqual(problem.degree, 2)
        actual = full_collision_sets(problem)
        for (a,b), points in actual.items():
            expected = {(0,0,0,x,a) for x in range(3)} if a == b else set()
            self.assertEqual(points, expected)

    def test_tags_preserve_both_fibers_and_public_bytes(self):
        circuit = TernaryCircuit(1, (Multiply(0,0),), (1,))
        empty = compile_circuit(circuit)
        tagged = compile_circuit(circuit, b"\x00\x81\xff")
        self.assertEqual(read_public_tag(empty), b"")
        self.assertEqual(read_public_tag(tagged), b"\x00\x81\xff")
        self.assertEqual(full_collision_sets(empty), full_collision_sets(tagged))
        # Decode after a fresh reconstruction from the JSON-compatible output.
        outputs = tuple(Poly({tuple(m): v for m,v in terms})
                        for terms in tagged.public_encoding()["outputs"])
        self.assertEqual(read_public_tag(Problem(1, 2, outputs)), b"\x00\x81\xff")
        for invalid in ((), (Poly.variable(0),), (Poly(), Poly({(): 1})),
                        (Poly({(): 1}),)*8):
            with self.assertRaises(ValueError):
                read_public_tag(Problem(1, 2, invalid))

    def test_shared_polynomial_products_and_cubic_degree_bound(self):
        x, y = Poly.variable(0), Poly.variable(1)
        square = x*x
        quartic = square*y*y
        polys = (quartic + square + 2, 2*quartic + square + y, Poly(), x)
        circuit = circuit_from_polynomials(2, polys)
        problem = compile_circuit(circuit)
        self.assertEqual(sum(isinstance(gate, Multiply) for gate in circuit.gates), 3)
        self.assertEqual(problem.degree, 3)
        for point in product(range(3), repeat=2):
            c = tuple(poly.evaluate(point) for poly in polys)
            self.assertEqual(circuit.evaluate(point), c)
            self.assertTrue(verify_witness(problem, c, lift_preimage(circuit, c, point)))

    def test_generated_cm14_complete_fibers_and_kem_ciphertext(self):
        backend = MaskedPlanarBackend(1)
        sk = bytes(range(backend.seed_bytes))
        pk = backend.public_from_private(sk)
        circuit = cm14_public_circuit(1, pk)
        problem = compile_circuit(circuit, pk)
        self.assertEqual(read_public_tag(problem), pk)
        actual = full_collision_sets(problem)
        for x in range(3):
            c = backend.forward(pk, (x,))
            expected = lift_preimage(circuit, c, (x,))
            self.assertEqual(actual[c], {expected})
            self.assertEqual(expected[2:3], (x,))
        receiver = ResearchKEM(backend)
        # The only supplied preimage is the input already known to encapsulation.
        with patch("research_kem.secrets.randbelow", return_value=2):
            ciphertext, key = receiver.encaps(PublicKey(backend.suite, 1, pk))
        c = unpack(ciphertext, 1)
        self.assertTrue(verify_witness(problem, c, lift_preimage(circuit, c, (2,))))
        self.assertEqual(receiver.decaps(PrivateKey(backend.suite, 1, sk), ciphertext), key)

    def test_both_generated_public_coefficient_layouts(self):
        cm = MaskedPlanarBackend(2)
        cm_pk = cm.public_from_private(bytes(range(cm.seed_bytes)))
        triangular = TwoLayerBackend(2)
        with patch("two_layer.secrets.randbelow", side_effect=Random(221).randrange):
            tri_pk, _ = triangular.generate()
        for backend, pk, builder in ((cm, cm_pk, cm14_public_circuit),
                                     (triangular, tri_pk, two_layer_public_circuit)):
            circuit = builder(2, pk)
            problem = compile_circuit(circuit, pk)
            self.assertEqual(read_public_tag(problem), pk)
            for x in product(range(3), repeat=2):
                c = backend.forward(pk, x)
                self.assertEqual(circuit.evaluate(x), c)
                self.assertTrue(verify_witness(problem, c, lift_preimage(circuit, c, x)))
            with self.assertRaises(ValueError):
                builder(2, pk + b"\x00")

    def test_empty_transcript_and_invalid_wires(self):
        circuit = TernaryCircuit(0, (), ())
        self.assertEqual(full_collision_sets(compile_circuit(circuit)), {(): {(0,)}})
        constant = TernaryCircuit(0, (Affine(2, ()),), (0,))
        self.assertEqual(lift_preimage(constant, (2,), ()), (0,0,2))
        with self.assertRaises(ValueError):
            lift_preimage(constant, (0,), ())
        with self.assertRaises(ValueError):
            TernaryCircuit(1, (Multiply(0,1),), (0,))
        with self.assertRaises(ValueError):
            TernaryCircuit(0, (), (0,))
        with self.assertRaises(ValueError):
            circuit_from_polynomials(1, (Poly.variable(1),))
        with self.assertRaises(ValueError):
            Affine(0, ((0,3),))
        with self.assertRaises(TypeError):
            compile_circuit(constant, "tag")


if __name__ == "__main__":
    unittest.main()
