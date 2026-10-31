"""NG-Q8 public-only one-pass pair projection, and exact GF(3) local census.
Research-only: this is not a KEM and no production security is claimed.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import comb
import random

POINTS = tuple(product(range(3), repeat=2))
INDEX = {p: j for j, p in enumerate(POINTS)}
TRIPLES = tuple(product(range(3), repeat=3))


def rank_mod3(rows):
    if not rows:
        return 0
    a = [list(row) for row in rows]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((j for j in range(rank, len(a)) if a[j][col] % 3), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][col] % 3, -1, 3)
        a[rank] = [(inverse * t) % 3 for t in a[rank]]
        for j in range(len(a)):
            if j != rank and a[j][col] % 3:
                c = a[j][col] % 3
                a[j] = [(t - c * w) % 3 for t, w in zip(a[j], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def potential_difference_row(right):
    z, w = right
    result = [0] * 9
    result[INDEX[((z + 1) % 3, w)]] += 1
    result[INDEX[(z, w)]] -= 1
    return result


def independent_pair_failure_probability(u, v):
    """Exact Pr_Q[no z in F3 makes f(u+z*v)=f(0)], A=1.

    u,v are linearly independent vectors in F3^3. The three differences
    form an affine map of the 9 uniform independent potential entries.
    """
    base = potential_difference_row((0, 0))
    rows, offsets = [], []
    for z in range(3):
        w = tuple((u[j] + z * v[j]) % 3 for j in range(3))
        rows.append(tuple((x - y) % 3 for x, y in
                          zip(potential_difference_row(w[1:]), base)))
        offsets.append(w[0])
    basis = []
    for column in zip(*rows):
        if rank_mod3(basis + [column]) > len(basis):
            basis.append(column)
    failures = 0
    for coeff in product(range(3), repeat=len(basis)):
        differences = [((offsets[j] + sum(a * b[j] for a,b in
                        zip(coeff,basis))) % 3) for j in range(3)]
        failures += int(all(differences))
    return Fraction(failures, 3 ** len(basis)), len(basis)


def exact_local_census():
    """Exhaustive finite proof obligation: 26*24=624 independent pairs."""
    nonzero = [x for x in TRIPLES if any(x)]
    classes = Counter()
    for u in nonzero:
        for v in nonzero:
            if rank_mod3((u, v)) != 2:
                continue
            probability, image_rank = independent_pair_failure_probability(u, v)
            classes[(image_rank, str(probability))] += 1
    assert sum(classes.values()) == 624
    failure = sum((Fraction(key[1]) * count for key,count in classes.items()),
                  Fraction(0)) / 624
    return failure, classes


def public_one_pass_recover(n, factors, targets):
    """Use only PUBLIC scopes, complete tables, targets. No s, B, A, Q."""
    if n < 3 or len(factors) != len(targets):
        raise ValueError('require n>=3 and one target per factor')
    domains = {p: set(product(range(3), repeat=2))
               for p in combinations(range(n), 2)}
    for (scope, table), target in zip(factors, targets):
        scope = tuple(scope)
        if len(scope) != 3 or tuple(sorted(scope)) != scope or any(
                j < 0 or j >= n for j in scope):
            raise ValueError('require sorted public triple scopes')
        if len(table) != 27 or any(point not in table for point in TRIPLES):
            raise ValueError('require complete public ternary table')
        if tuple(target) not in ((0,), (1,), (2,)):
            raise ValueError('require one scalar ternary target')
        fiber = [point for point in TRIPLES if tuple(table[point]) == tuple(target)]
        for a,b in combinations(range(3), 2):
            pair = (scope[a],scope[b])
            domains[pair].intersection_update((point[a], point[b]) for point in fiber)
    if any(len(values) != 1 for values in domains.values()):
        return 'inconclusive', None
    candidate = [None] * n
    for (a,b), values in domains.items():
        va,vb = next(iter(values))
        if (candidate[a] not in (None,va) or candidate[b] not in (None,vb)):
            return 'inconclusive', None
        candidate[a], candidate[b] = va, vb
    candidate = tuple(candidate)
    if any(candidate[j] is None for j in range(n)):
        return 'inconclusive', None
    for (scope, table), target in zip(factors, targets):
        if tuple(table[tuple(candidate[j] for j in scope)]) != tuple(target):
            return 'inconclusive', None
    return 'recovered', candidate


def public_failure_bound(n, scopes, delta=Fraction(15, 52)):
    """Bound when factor randomness is independent and all scopes are fixed."""
    scopes = [tuple(s) for s in scopes]
    if n < 3 or any(len(s) != 3 or len(set(s)) != 3 or
                    any(j < 0 or j >= n for j in s) for s in scopes):
        raise ValueError('invalid hypergraph')
    p = 1 - delta
    value = sum((8 * p ** sum(a in s and b in s for s in scopes)
                 for a,b in combinations(range(n), 2)), Fraction(0))
    return min(Fraction(1), value)


def complete_triples_bound(n):
    return min(Fraction(1), 8 * comb(n,2) * Fraction(37,52) ** (n - 2))


def sample_planted(n, seed, scopes=None):
    rng = random.Random(seed)
    secret = tuple(rng.randrange(3) for _ in range(n))
    if scopes is None:
        scopes = combinations(range(n), 3)
    factors, targets = [], []
    for scope in scopes:
        while True:
            B = [[rng.randrange(3) for _ in range(3)] for _ in range(3)]
            if rank_mod3(B) == 3:
                break
        A = rng.choice((1, 2))
        Q = [rng.randrange(3) for _ in range(9)]
        table = {}
        for x in TRIPLES:
            u = tuple(sum(row[j] * x[j] for j in range(3)) % 3 for row in B)
            z,w = u[1:]
            table[x] = ((A * u[0] + Q[INDEX[((z+1)%3,w)]] - Q[INDEX[(z,w)]]) % 3,)
        factors.append((tuple(scope), table))
        targets.append(table[tuple(secret[j] for j in scope)])
    return secret, factors, targets


if __name__ == '__main__':
    probability, classes = exact_local_census()
    print('local wrong-pair rejection probability:', probability)
    print('finite rank / failure fraction cases:', dict(sorted(classes.items())))
    for n in (6, 12, 20, 30, 40, 50, 100):
        print('n:', n, 'failure upper bound:', float(complete_triples_bound(n)))
    for n, trials in ((6, 12), (12, 10), (20, 5), (30, 3)):
        recovered = 0
        for j in range(trials):
            secret, factors, targets = sample_planted(n, 8132000 + 1000*n + j)
            status, x = public_one_pass_recover(n, factors, targets)
            if status == 'recovered':
                assert x == secret
                recovered += 1
        print('public one-pass recovered', n, recovered, '/', trials)
