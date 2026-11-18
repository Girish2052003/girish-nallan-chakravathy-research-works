"""Planted complete policies for small explicit graphs in the Round 10 model.

A generated policy answers all collision challenges. It has no encapsulation
operation. Vertex count is a separate public parameter. The public graph
contains only the upper-triangular adjacency bits of a simple undirected graph.
"""

from itertools import combinations
import secrets

from research_kem import pack, unpack


def _edge_slots(vertices):
    if type(vertices) is not int or vertices < 1:
        raise ValueError("vertex count must be a positive integer")
    return vertices * (vertices - 1) // 2


def _decode_graph(vertices, public):
    slots = _edge_slots(vertices)
    if type(public) is not bytes or len(public) != (slots + 7) // 8:
        raise ValueError("wrong graph length or type")
    mask = int.from_bytes(public, "little")
    if mask >= 1 << slots:
        raise ValueError("nonzero unused graph bits")
    return mask


def graph_from_coins(colors, coins):
    """Use one coin for each unordered pair, discarding it for equal colors."""
    vertices = len(colors)
    slots = _edge_slots(vertices)
    if any(type(t) is not int or t not in (0, 1, 2) for t in colors):
        raise ValueError("colors must be trits")
    if type(coins) is not int or not 0 <= coins < 1 << slots:
        raise ValueError("coin mask outside its domain")
    mask = 0
    for bit, (i, j) in enumerate(combinations(range(vertices), 2)):
        if colors[i] != colors[j]:
            mask |= coins & (1 << bit)
    return mask.to_bytes((slots + 7) // 8, "little")


def generate_policy(vertices):
    """Return the canonical public adjacency and the packed private color table."""
    slots = _edge_slots(vertices)
    colors = tuple(secrets.randbelow(3) for _ in range(vertices))
    return graph_from_coins(colors, secrets.randbits(slots)), pack(colors)


class PlantedPolicy:
    """Decode once. Nonbinary and padded vertex addresses use the value zero."""

    def __init__(self, vertices, private):
        _edge_slots(vertices)
        self.width = max(1, (vertices - 1).bit_length())
        self.colors = unpack(private, vertices)

    def answer(self, address):
        if len(address) != self.width or any(type(x) is not int or x not in (0, 1, 2)
                                              for x in address):
            raise ValueError("invalid ternary address")
        if 2 in address:
            return 0
        index = 0
        for bit in address:
            index = (index << 1) | bit
        return self.colors[index] if index < len(self.colors) else 0


def adjacency_gate_list(vertices, public):
    """Return (width, gates, output), the inputs to the Round 10 Circuit type."""
    mask = _decode_graph(vertices, public)
    width = max(1, (vertices - 1).bit_length())
    gates = []

    def gate(op, *inputs):
        gates.append((op, *inputs))
        return 2 * width + len(gates) - 1

    def either(x, y):
        return gate("not", gate("and", gate("not", x), gate("not", y)))

    flipped = [gate("not", i) for i in range(2 * width)]

    def address_word(start, vertex):
        digits = [(vertex >> i) & 1 for i in reversed(range(width))]
        literals = [start + i if digit else flipped[start + i] for i, digit in enumerate(digits)]
        wire = literals[0]
        for literal in literals[1:]:
            wire = gate("and", wire, literal)
        return wire

    left = [address_word(0, v) for v in range(vertices)]
    right = [address_word(width, v) for v in range(vertices)]
    output = gate("and", 0, flipped[0])  # constant false
    for bit, (i, j) in enumerate(combinations(range(vertices), 2)):
        if mask & (1 << bit):
            endpoint_order = gate("and", left[i], right[j])
            reverse_order = gate("and", left[j], right[i])
            output = either(output, either(endpoint_order, reverse_order))
    return width, tuple(gates), output
