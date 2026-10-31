"""NG-Q9: elementary general-arity lower bound on local pair exclusion.
Uniform B in GL(k,3), A invertible, uniform vector potential Q over F3^d.
Proof uses constant finite-difference event and full-rank linear-map counting.
"""
from fractions import Fraction
from itertools import product
from math import prod

def gaussian_rank_count(q,rows,cols,t):
    if t<0 or t>min(rows,cols):return 0
    num=prod((q**rows-q**i)*(q**cols-q**i) for i in range(t))
    den=prod(q**t-q**i for i in range(t))
    assert num%den==0
    return num//den

def full_row_rank_count(q,r,k):
    assert k>=r>=1
    return prod(q**k-q**i for i in range(r))

def gamma_uniform_surjective_map(r,d):
    """P[L h notin L(T)] for uniform full row rank r x (r+d).
    T is a coordinate subspace of dimension k-2; h is outside T.
    """
    if r<1 or d<1:raise ValueError('require positive r,d')
    q=3;k=r+d; s=k-2
    counts=0
    t=r-1
    if 0<=t<=min(r,s):
        counts+=gaussian_rank_count(q,r,s,t)*(q**r-q**t)*q**r
    t=r-2
    if 0<=t<=min(r,s):
        counts+=gaussian_rank_count(q,r,s,t)*(q**r-q**t)*(q**r-q**(t+1))
    return Fraction(counts,full_row_rank_count(q,r,k))

def local_projection_rejection_lower_bound(r,d):
    # Pr[Delta_a Q is globally constant] = 3^(-r*(2*3^(d-1)-1))
    gamma=gamma_uniform_surjective_map(r,d)
    return gamma*Fraction(1,3**(r*(2*3**(d-1)-1)))


def general_projection_failure_upper_bound(n,scopes,r,d):
    """NG-Q9 rigorous upper bound for fixed k-ary independent source factors."""
    from itertools import combinations
    if n<2 or any(len(scope)!=r+d or len(set(scope))!=r+d or
                   any(v<0 or v>=n for v in scope) for scope in scopes):
        raise ValueError('invalid fixed-arity scopes')
    epsilon=local_projection_rejection_lower_bound(r,d)
    return min(Fraction(1),sum(
        (8*(1-epsilon)**sum(i in scope and j in scope for scope in scopes)
         for i,j in combinations(range(n),2)),Fraction(0)))

if __name__=='__main__':
    for r,d in ((1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2)):
        print('r,d',r,d,'gamma',gamma_uniform_surjective_map(r,d),
              'epsilon',local_projection_rejection_lower_bound(r,d),
              'approx',float(local_projection_rejection_lower_bound(r,d)))
