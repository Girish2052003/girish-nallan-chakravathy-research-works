"""NG-Q18: standard Erdős–Rényi isolation obstruction to full relative recovery.

Exact first/second isolation moments; conservative Chebyshev probability bound.
No claim of novel random-graph theory, cryptographic hardness, or key security.
"""
from fractions import Fraction
from random import Random


def isolation_moments(n, p):
    """Undirected G(n,p): E[isolated vertices], Var[isolated vertices].

    Exact rational arithmetic; works at p=0 and p=1 including endpoints.
    """
    if n < 2 or not isinstance(p, Fraction) or not (0 <= p <= 1):
        raise ValueError('require n>=2 and p as Fraction in [0,1]')
    q = 1 - p
    mu = n * q ** (n - 1)
    pair = n*(n-1)*q**(2*n-3)
    variance = mu + pair - mu*mu
    assert variance >= 0
    return mu, variance


def isolation_lower_bound(n, p):
    """P[at least one isolated vertex] >= 1 - Var(X)/E[X]^2."""
    mu, var = isolation_moments(n,p)
    if mu == 0:
        return Fraction(0)
    return max(Fraction(0), 1 - var / (mu*mu))


def sample_er_edges(n, p, seed):
    if n < 2 or not (0 <= p <= 1):
        raise ValueError('invalid parameters')
    rng = Random(seed)
    edges = set()
    for i in range(n):
        for j in range(i+1,n):
            if rng.random() < float(p):
                edges.add((i,j))
    return edges


def isolated_vertices(n, edges):
    nonisolated = set()
    for a,b in edges:
        if not (0<=a<b<n):
            raise ValueError('invalid edge')
        nonisolated.add(a);nonisolated.add(b)
    return tuple(i for i in range(n) if i not in nonisolated)


if __name__ == '__main__':
    for n,p in ((100,Fraction(1,100)),(200,Fraction(1,100)),
                (500,Fraction(1,100)),(500,Fraction(3,100))):
        mu,var=isolation_moments(n,p)
        print('n',n,'rho',float(p),'expected isolated',float(mu),
              'isolation probability >=',float(isolation_lower_bound(n,p)))
