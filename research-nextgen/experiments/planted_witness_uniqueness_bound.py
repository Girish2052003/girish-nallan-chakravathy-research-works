"""Exact planted-witness collision first moment for independent source-form maps.

For fixed s independent of B_i,Q_i and target t=F(s), gives expected number
of OTHER witnesses. The uniqueness bound says NOTHING about recovery hardness.
"""
from fractions import Fraction
from itertools import product
from math import comb


def nonzero_local_collision_probability(r=1,d=2):
    if not isinstance(r,int) or not isinstance(d,int) or r<1 or d<1:
        raise ValueError('r,d must be positive integers')
    # v=0 implies nonzero left direction and nonzero output difference.
    # v!=0 implies a nonzero mixed-difference linear functional of Q,
    # uniformly distributed over F3^r.
    return Fraction(3**d-1,3**(r+d)-1)


def expected_other_witnesses(scopes,n,r=1,d=2):
    """Exact E[|F^-1(F(s))|-1] for a fixed, independently planted secret s."""
    scopes=tuple(tuple(scope) for scope in scopes)
    if any(len(scope)!=r+d or len(set(scope))!=len(scope) or
           any(j<0 or j>=n for j in scope) for scope in scopes):
        raise ValueError('invalid factor scope')
    beta=nonzero_local_collision_probability(r,d)
    return sum((beta**sum(any(h[j] for j in scope) for scope in scopes)
                for h in product(range(3),repeat=n) if any(h)),Fraction(0))


def complete_uniform_scope_expected_other(n,r=1,d=2):
    k=r+d
    if n<k:raise ValueError('n<k')
    m=comb(n,k)
    beta=nonzero_local_collision_probability(r,d)
    return sum((comb(n,s)*2**s*beta**(m-(comb(n-s,k) if n-s>=k else 0))
                for s in range(1,n+1)),Fraction(0))


def probability_not_unique_upper_bound(n,r=1,d=2):
    return min(Fraction(1),complete_uniform_scope_expected_other(n,r,d))


if __name__=='__main__':
    print('beta d2 r1',nonzero_local_collision_probability())
    for n in range(4,10):
        print('n',n,'m',comb(n,3),'other witness E',float(complete_uniform_scope_expected_other(n)),
              'P(nonunique) upper',float(probability_not_unique_upper_bound(n)))
