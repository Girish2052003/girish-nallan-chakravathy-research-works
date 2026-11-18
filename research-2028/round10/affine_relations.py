"""Explicit finite verifier for the quadratic two-table upper bound over F3.

Each constraint is a relation between one left and one right table entry.
The algorithm materializes the graph, so it is an oracle for small examples.
The proof in the research note gives the polynomial-space implicit version.
"""

from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass


FIELD = (0, 1, 2)
Pair = tuple[int, int]


@dataclass(frozen=True)
class AffineRelation:
    """Pins fix individual coordinates; a transport means right = scale*left + offset."""

    feasible: bool = True
    left_pin: int | None = None
    right_pin: int | None = None
    transport: Pair | None = None


def classify_relation(pairs: Iterable[Pair]) -> AffineRelation:
    """Classify an empty or affine subset of F3²; reject every other subset."""
    points = frozenset(pairs)
    if any(x not in FIELD or y not in FIELD for x, y in points):
        raise ValueError("a relation contains a value outside F3")
    if not points:
        return AffineRelation(feasible=False)
    if len(points) == 9:
        return AffineRelation()
    if len(points) == 1:
        left, right = next(iter(points))
        return AffineRelation(left_pin=left, right_pin=right)
    if len(points) == 3:
        left_values = {x for x, _ in points}
        right_values = {y for _, y in points}
        if len(left_values) == 1:
            return AffineRelation(left_pin=next(iter(left_values)))
        if len(right_values) == 1:
            return AffineRelation(right_pin=next(iter(right_values)))
        if len(left_values) == len(right_values) == 3:
            graph = dict(points)
            offset = graph[0]
            scale = (graph[1] - offset) % 3
            if graph[2] == (2 * scale + offset) % 3:
                return AffineRelation(transport=(scale, offset))
    raise ValueError("the relation is neither empty nor affine over F3")


def _propagate(root, initial, adjacency, allowed):
    """Try one root value, following every bijection in its component."""
    colors = {root: initial}
    pending = deque([root])
    while pending:
        vertex = pending.popleft()
        color = colors[vertex]
        if color not in allowed[vertex]:
            return None
        for neighbor, scale, offset in adjacency[vertex]:
            required = (scale * color + offset) % 3
            if neighbor in colors:
                if colors[neighbor] != required:
                    return None
            else:
                colors[neighbor] = required
                pending.append(neighbor)
    return colors


def affine_network_witness(
    left_size: int,
    right_size: int,
    constraints: Iterable[tuple[int, int, Iterable[Pair]]],
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    """Return satisfying left and right color tables, or None if inconsistent.

    Endpoints are numbered separately on each side, starting at zero. A
    repeated endpoint pair contributes another simultaneous constraint.
    """
    if left_size < 0 or right_size < 0:
        raise ValueError("table sizes must be nonnegative")
    num_vertices = left_size + right_size
    adjacency = [[] for _ in range(num_vertices)]
    allowed = [set(FIELD) for _ in range(num_vertices)]
    feasible = True
    for left, right_index, pairs in constraints:
        if not 0 <= left < left_size or not 0 <= right_index < right_size:
            raise ValueError("constraint endpoint outside the declared tables")
        right = left_size + right_index
        relation = classify_relation(pairs)
        if not relation.feasible:
            feasible = False
        if relation.left_pin is not None:
            allowed[left].intersection_update([relation.left_pin])
        if relation.right_pin is not None:
            allowed[right].intersection_update([relation.right_pin])
        if relation.transport is not None:
            scale, offset = relation.transport
            inverse = pow(scale, -1, 3)
            adjacency[left].append((right, scale, offset))
            adjacency[right].append((left, inverse, (-inverse * offset) % 3))
    if not feasible or any(not colors for colors in allowed):
        return None

    chosen = {}
    for root in range(num_vertices):
        if root in chosen:
            continue
        for initial in FIELD:
            extension = _propagate(root, initial, adjacency, allowed)
            if extension is not None:
                chosen.update(extension)
                break
        else:
            return None
    return (
        tuple(chosen[i] for i in range(left_size)),
        tuple(chosen[left_size + i] for i in range(right_size)),
    )
