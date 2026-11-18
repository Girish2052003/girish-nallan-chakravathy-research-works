"""Public binary Niederreiter syndrome relation in ternary cubic coordinates.

The executable wire check takes a supplied binary vector. The expanded
potential is a proof representation; full-size KEM exchanges use native bytes.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'round12'))
from differential_bridge import Affine, Multiply, TernaryCircuit, compile_circuit, read_public_tag


def _binary_integer(wire, bits):
    if type(wire) is not bytes or len(wire) != (bits+7)//8:
        raise ValueError('incorrect binary vector width')
    value = int.from_bytes(wire, 'little')
    if value.bit_length() > bits:
        raise ValueError('nonzero vector padding')
    return value


class BinarySystematic:
    """H = [I | T], with row-packed T in the Classic McEliece ENCODE format."""
    def __init__(self, n, rows, public):
        if type(n) is not int or type(rows) is not int or not 0 < rows < n:
            raise ValueError('invalid systematic parity-check dimensions')
        self.n, self.rows, self.public = n, rows, public
        width = (n-rows+7)//8
        if type(public) is not bytes or len(public) != rows*width:
            raise ValueError('incorrect public matrix width')
        self.masks = tuple(_binary_integer(public[j:j+width], n-rows)
                           for j in range(0, len(public), width))

    def encode(self, error):
        """Compute the standard binary syndrome of a caller-supplied vector."""
        e = _binary_integer(error, self.n)
        tail = e >> self.rows
        result = e & ((1 << self.rows)-1)
        for i, row in enumerate(self.masks):
            result ^= ((row & tail).bit_count() & 1) << i
        return result.to_bytes((self.rows+7)//8, 'little')

    def accepts(self, ciphertext, weight, error):
        """Check exact integer weight, canonical byte strings and the syndrome."""
        if type(weight) is not int or not 0 <= weight <= self.n:
            return False
        try:
            _binary_integer(ciphertext, self.rows)
            return _binary_integer(error, self.n).bit_count() == weight and self.encode(error) == ciphertext
        except ValueError:
            return False

    def circuit(self):
        n = self.n
        gates = []

        def append(gate):
            gates.append(gate)
            return n + len(gates)-1

        def half_add(a, b):
            carry = append(Multiply(a,b))
            bit = append(Affine(0, ((a,1),(b,1),(carry,1))))
            return bit, carry

        checks = []
        for i in range(n):
            square = append(Multiply(i,i))
            checks.append(append(Affine(0, ((square,1),(i,2)))))

        syndrome = []
        for i, row in enumerate(self.masks):
            bit = i
            while row:
                lowest = row & -row
                j = lowest.bit_length()-1
                bit, _ = half_add(bit, self.rows+j)
                row ^= lowest
            syndrome.append(bit)

        zero = append(Affine(0, ()))
        count = [zero] * n.bit_length()
        for i in range(n):
            carry = i
            for j, old in enumerate(count):
                count[j], carry = half_add(old, carry)
        return TernaryCircuit(n, tuple(gates), tuple(checks + syndrome + count))

    def target(self, ciphertext, weight):
        if type(weight) is not int or not 0 <= weight <= self.n:
            raise ValueError('invalid Hamming weight')
        syndrome = _binary_integer(ciphertext, self.rows)
        return ((0,)*self.n + tuple(syndrome >> j & 1 for j in range(self.rows))
                + tuple(weight >> j & 1 for j in range(self.n.bit_length())))

    def compile(self, ciphertext, weight):
        target = self.target(ciphertext, weight)
        tag = f'{self.n}/{self.rows}:'.encode('ascii') + self.public
        return compile_circuit(self.circuit(), tag), target


def read_instance(problem, target):
    """Recover the original syndrome instance on the image of the compiler."""
    header, public = read_public_tag(problem).split(b':', 1)
    n, rows = (int(field) for field in header.split(b'/'))
    system = BinarySystematic(n, rows, public)
    if header != f'{n}/{rows}'.encode('ascii'):
        raise ValueError('noncanonical public header')
    target = tuple(target)
    if (len(target) != n+rows+n.bit_length() or any(type(v) is not int or v not in (0,1) for v in target)
            or any(target[:n])):
        raise ValueError('invalid binary-system target')
    pos = n+rows
    c = sum(v << j for j,v in enumerate(target[n:pos]))
    weight = sum(v << j for j,v in enumerate(target[pos:]))
    if weight > n:
        raise ValueError('impossible encoded weight')
    return system, c.to_bytes((rows+7)//8, 'little'), weight
