"""Encode a signed-weight ternary syndrome instance as a Round 9 cubic problem.

This proof representation is independent of the compact KEM wire format.
All converters take public parameters or a caller-supplied witness.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round12"))
from differential_bridge import Affine, Multiply, TernaryCircuit, compile_circuit, read_public_tag


def _uint(value, maximum):
    return type(value) is int and 0 <= value <= maximum


def _matrix(matrix):
    rows = tuple(tuple(row) for row in matrix)
    if not rows or not rows[0]:
        raise ValueError("expected a nonempty matrix")
    n = len(rows[0])
    if any(len(row) != n or any(not _uint(v, 2) for v in row) for row in rows):
        raise ValueError("expected equally sized rows of trits")
    return rows, n


def syndrome_circuit(matrix):
    """Map e to the syndrome and little-endian binary Hamming weight."""
    rows, n = _matrix(matrix)
    gates = []

    def append(gate):
        index = n + len(gates)
        gates.append(gate)
        return index

    syndrome = [append(Affine(0, tuple((i, v) for i, v in enumerate(row) if v)))
                for row in rows]
    zero = append(Affine(0, ()))
    counter = [zero] * n.bit_length()
    for i in range(n):
        carry = append(Multiply(i, i))
        for j, bit in enumerate(counter):
            product = append(Multiply(bit, carry))
            counter[j] = append(Affine(0, ((bit, 1), (carry, 1), (product, 1))))
            carry = product
    return TernaryCircuit(n, tuple(gates), tuple(syndrome + counter))


def compile_instance(matrix, syndrome, weight):
    """Return the public potential and challenge. No error vector is needed."""
    rows, n = _matrix(matrix)
    y = tuple(syndrome)
    if len(y) != len(rows) or any(not _uint(v, 2) for v in y) or not _uint(weight, n):
        raise ValueError("invalid syndrome or weight")
    # Canonical decimal dimensions avoid a bound on the mathematical input sizes.
    header = f"{len(rows)}x{n}:".encode("ascii")
    tag = header + b"".join(bytes(row) for row in rows)
    target = y + tuple(weight >> j & 1 for j in range(n.bit_length()))
    return compile_circuit(syndrome_circuit(rows), tag), target


def decode_instance(problem, challenge):
    """Left inverse on the image of compile_instance, for the reduction."""
    header, data = read_public_tag(problem).split(b":", 1)
    heights = header.split(b"x")
    if len(heights) != 2:
        raise ValueError("invalid matrix dimensions")
    rows, n = map(int, heights)
    if (min(rows, n) <= 0 or len(data) != rows*n or
            header != f"{rows}x{n}".encode("ascii") or any(v > 2 for v in data)):
        raise ValueError("invalid matrix tag")
    c = tuple(challenge)
    if (len(c) != rows + n.bit_length() or any(not _uint(v, 2) for v in c[:rows])
            or any(not _uint(v, 1) for v in c[rows:])):
        raise ValueError("invalid challenge")
    weight = sum(v << j for j, v in enumerate(c[rows:]))
    if weight > n:
        raise ValueError("invalid decoded weight")
    matrix = tuple(tuple(data[j:j+n]) for j in range(0, len(data), n))
    return matrix, c[:rows], weight
