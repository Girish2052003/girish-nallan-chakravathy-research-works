"""Generate small public examples of the single-distribution search problem.

A public instance is (B, y, w). The generator retains no answer in its output.
The explicit iid matrix costs rows*columns trits, even before cubic compilation.
"""
import argparse
import json
from pathlib import Path
import secrets
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "round14"))
from weighted_difference import compile_instance


def sample_public(rows, columns, weight):
    if any(type(v) is not int for v in (rows, columns, weight)):
        raise ValueError("dimensions and weight must be integers")
    if not 0 < rows < columns or not 0 < weight <= columns:
        raise ValueError("expected 0 < rows < columns and 0 < weight <= columns")
    support = secrets.SystemRandom().sample(range(columns), weight)
    signed = [(i, 1 + secrets.randbelow(2)) for i in support]
    matrix = [tuple(secrets.randbelow(3) for _ in range(columns)) for _ in range(rows)]
    syndrome = [sum(row[i]*v for i, v in signed) % 3 for row in matrix]
    return tuple(matrix), tuple(syndrome), weight


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cubic", action="store_true", help="emit the explicit cubic representation")
    args = parser.parse_args()
    # Small fixed dimensions keep the human-readable example usable.
    matrix, syndrome, weight = sample_public(3, 6, 2)
    if args.cubic:
        potential, target = compile_instance(matrix, syndrome, weight)
        output = {"potential": potential.public_encoding(), "challenge": target}
    else:
        output = {"field": 3, "matrix": matrix, "syndrome": syndrome, "weight": weight}
    print(json.dumps(output))


if __name__ == "__main__":
    main()
