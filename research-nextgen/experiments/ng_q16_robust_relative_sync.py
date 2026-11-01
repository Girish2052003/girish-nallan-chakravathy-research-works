"""NG-Q16: two-hop public recovery in noisy/erased finite-group synchronization.

No cryptography or secret-only trapdoor is claimed. The observations are public
relative group elements Y_ij = x_i^-1 * x_j, independently erased/corrupted.
For explicit permutations, the algorithm is polynomial in n and degree k.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb, exp
from random import Random


def identity(k):
    return tuple(range(k))


def multiply(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p):
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def validate_perm(p, k):
    if len(p) != k or set(p) != set(range(k)):
        raise ValueError("invalid permutation")


def sample_public(n, k, rho, eps, seed, planted=None):
    """Public sample: per edge observe w.p. rho, then true w.p. 1-eps,
    otherwise uniformly random S_k, including possible accidental truth.
    Returns (planted, public_pairs, actual_corrupted_edges).
    """
    if n < 3 or k < 2 or not (0 <= rho <= 1 and 0 <= eps <= 1):
        raise ValueError('invalid parameters')
    rng = Random(seed)
    x = tuple(tuple(rng.sample(range(k), k)) for _ in range(n)) if planted is None else tuple(planted)
    if len(x) != n:
        raise ValueError('wrong secret count')
    for v in x:
        validate_perm(v, k)
    public = {}
    bad = set()
    for i, j in combinations(range(n), 2):
        if rng.random() >= rho:
            continue
        truth = multiply(inverse(x[i]), x[j])
        if rng.random() < eps:
            public[(i, j)] = tuple(rng.sample(range(k), k))
            if public[(i, j)] != truth:
                bad.add((i, j))
        else:
            public[(i, j)] = truth
    return x, public, bad


def directed(public, a, b):
    if a == b:
        raise ValueError('self-edges absent')
    key = (min(a, b), max(a, b))
    if key not in public:
        return None
    return public[key] if a < b else inverse(public[key])


def two_hop_votes(n, k, public):
    """Public-only plurality per pair; ties and zero observations are unresolved.

    Returns (estimates, margin_metadata); a pair's candidate is derived only
    from observed paths i->h->j and never from the direct edge i->j.
    """
    if n < 3 or k < 2:
        raise ValueError('need n>=3, k>=2')
    for (i, j), p in public.items():
        if not (0 <= i < j < n):
            raise ValueError('require ordered public edge keys')
        validate_perm(p, k)
    estimates = {}
    margins = {}
    for i, j in combinations(range(n), 2):
        counts = Counter()
        for h in range(n):
            if h in (i, j):
                continue
            ih = directed(public, i, h)
            hj = directed(public, h, j)
            if ih is not None and hj is not None:
                counts[multiply(ih, hj)] += 1
        if not counts:
            margins[(i, j)] = (0, 0, 0)
            continue
        order = counts.most_common()
        best, first = order[0]
        second = order[1][1] if len(order) > 1 else 0
        margins[(i, j)] = (first, second, sum(counts.values()))
        if first > second:
            estimates[(i, j)] = best
    return estimates, margins


def public_recover(n, k, public):
    """Return canonical gauge candidate iff pair plurality is global-cocycle consistent.

    A consistent candidate is verified against *estimated pair ratios*, not the
    unavailable planted secret. A wrong-but-consistent answer is logically
    possible outside the stated recovery theorem; never label it verified secret.
    """
    estimates, margins = two_hop_votes(n, k, public)
    if len(estimates) != comb(n, 2):
        return {'status': 'inconclusive', 'gauge_witness': None,
                'estimated_pairs': estimates, 'votes': margins}
    x = [identity(k)]
    for j in range(1, n):
        x.append(estimates[(0, j)])
    for i, j in combinations(range(n), 2):
        if multiply(inverse(x[i]), x[j]) != estimates[(i, j)]:
            return {'status': 'inconclusive', 'gauge_witness': None,
                    'estimated_pairs': estimates, 'votes': margins}
    return {'status': 'self_consistent', 'gauge_witness': tuple(x),
            'estimated_pairs': estimates, 'votes': margins}


def true_relative_pairs(x):
    return {(i, j): multiply(inverse(x[i]), x[j])
            for i, j in combinations(range(len(x)), 2)}


def clean_two_hop_counts(n, public, bad):
    """Diagnostic uses hidden corruption positions; NEVER passed to attacker."""
    counts = {}
    for i, j in combinations(range(n), 2):
        counts[(i, j)] = sum(
            (min(i, h), max(i, h)) in public and
            (min(h, j), max(h, j)) in public and
            (min(i, h), max(i, h)) not in bad and
            (min(h, j), max(h, j)) not in bad
            for h in range(n) if h not in (i, j))
    return counts


def deterministic_majority_certificate(n, public, bad):
    """Hidden diagnostic: >half observed 2-hop routes are genuinely clean.
    This condition is SUFFICIENT, not required for success.
    """
    good = clean_two_hop_counts(n, public, bad)
    observed = {p: sum((min(i, h), max(i, h)) in public and
                       (min(h, j), max(h, j)) in public
                       for h in range(n) if h not in (i, j))
                for p in combinations(range(n), 2)
                for i, j in (p,)}
    return all(observed[p] > 0 and 2 * good[p] > observed[p] for p in good)


def hoeffding_failure_upper(n, group_size, rho, eps):
    """Pr[ANY incorrect pair plurality] bound with independent noise/erasures.

    Each incorrect label comparison uses n-2 independent Z_h in [-1,1],
    with mean rho^2*(1-eps)^2; Hoeffding then a union bound.
    Caller supplies finite |G| as an integer; this is NOT an empirical rate.
    """
    if n < 3 or group_size < 2 or not (0 <= rho <= 1 and 0 <= eps <= 1):
        raise ValueError('invalid parameters')
    delta = rho * rho * (1 - eps) ** 2
    return min(1.0, comb(n, 2) * (group_size - 1) *
               exp(-(n - 2) * delta ** 2 / 2))


def strict_clean_majority_bound(n, rho, eps):
    """Group-size-independent bound from strict honest two-hop majority.

    For rho=1: clean-route probability q=(1-eps)^2. With missing edges,
    count absent routes as non-clean: q=rho^2*(1-eps)^2 and compare to
    n-2 potential routes. Thus this bound is deliberately conservative.
    """
    if n < 3 or not (0 <= rho <= 1 and 0 <= eps <= 1):
        raise ValueError('invalid parameters')
    q = (rho * (1 - eps)) ** 2
    if q <= 0.5:
        return 1.0
    return min(1.0, comb(n, 2) * exp(-2 * (n - 2) * (q - 0.5) ** 2))


if __name__ == '__main__':
    for k in (3, 5):
        x, public, bad = sample_public(100, k, 0.95, 0.1, 20261102 + k)
        result = public_recover(100, k, public)
        correct = result['estimated_pairs'] == true_relative_pairs(x)
        print('S_'+str(k), 'edges', len(public), 'corrupted', len(bad),
              'status', result['status'], 'all_relative_labels_correct', correct)
