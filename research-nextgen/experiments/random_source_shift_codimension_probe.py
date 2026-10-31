"""Finite adversarial control: public shift codimension of sampled source-form factors.

This is diagnostic only. Fixed small n, independently sampled Q and uniform
invertible 3x3 matrices by rejection. Not security evidence or a proof.
"""
from itertools import combinations, product
from pathlib import Path
import random
import sys
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'research-2028' / 'attacks'))
from public_global_shift_witness_recovery import PublicShiftSystem, _rref


def matvec(B, x):
    return tuple(sum(a*b for a, b in zip(row, x)) % 3 for row in B)


def source_table(rng):
    while True:
        B = [[rng.randrange(3) for _ in range(3)] for _ in range(3)]
        if len(_rref(B, 3)[1]) == 3:
            break
    A = rng.randrange(1, 3)
    Q = {z: rng.randrange(3) for z in product(range(3), repeat=2)}
    table = {}
    for x in product(range(3), repeat=3):
        u = matvec(B, x)
        z = u[1:]
        za = ((z[0]+1) % 3, z[1])
        table[x] = ((A*u[0]+Q[za]-Q[z]) % 3,)
    return table


def sample(n, m, seed):
    rng = random.Random(seed)
    scopes = list(combinations(range(n), 3))
    rng.shuffle(scopes)
    factors = [(scope, source_table(rng)) for scope in scopes[:m]]
    return PublicShiftSystem(n, factors)


if __name__ == '__main__':
    for n in (4, 5, 6):
        for policy in ('n_factors', 'all_triples'):
            m = n if policy == 'n_factors' else len(list(combinations(range(n), 3)))
            rows = []
            for j in range(30):
                seed = 20261031 + 1000*n + 100*(policy == 'all_triples') + j
                s = sample(n, m, seed=seed)
                rows.append((s.shift_dimension, s.increment_rank, n-s.shift_dimension))
            print('n=', n, 'm=', m, 'policy=', policy, 'trials=', len(rows),
                  'D_dim_counts=', dict(sorted(Counter(a for a,b,c in rows).items())),
                  'rank_counts=', dict(sorted(Counter(b for a,b,c in rows).items())),
                  'quotient_dim_counts=', dict(sorted(Counter(c for a,b,c in rows).items())))
