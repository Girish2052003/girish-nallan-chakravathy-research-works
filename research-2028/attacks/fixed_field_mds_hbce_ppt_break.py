#!/usr/bin/env python3
"""Round 3: exact fixed-field planted-frame distinguisher.

SG-DIFRA 2026 MDS-HBCE samples an M-row GRS frame over FIXED K=GF(2^10)
and hides it among q rows of K^N. Any (u+1) planted rows have rank u.
With K fixed, M<=1024 and 1<=u<M<=1024, so exhaustive subset enumeration
of at most 1024 rows costs O(q^1024 poly(N)): an asymptotic polynomial-time
PUBLIC KEY DISTINGUISHER (not a claimed practical finite-profile attack).

Null rows are independent uniform nonzero in K^N. For j<=N, probability
j rows are dependent is exactly
  1 - product_{i=1}^{j-1} (K^N-K^i)/(K^N-1).
Therefore the null false-positive bound is binom(q,u+1) * p_dep.
If N=Omega(lambda), q=poly(lambda), the false-positive probability
is negligible. A PPT adversary distinguishes Plant from Null with high
probability. This refutes the uniform asymptotic MDS-HBCE assumption
WITH THE ORIGINAL FIXED-FIELD GRS SAMPLER, not the finite IND-CCA claim.
"""
import itertools
import math
import random
import unittest
from fractions import Fraction

Q=1024
MOD=(1<<10)|(1<<3)|1

def gf_mul(a,b):
    res=0
    while b:
        if b&1: res^=a
        a<<=1
        if a&Q:a^=MOD
        b>>=1
    return res&(Q-1)

def gf_pow(a,exp):
    res=1
    while exp:
        if exp&1:res=gf_mul(res,a)
        a=gf_mul(a,a)
        exp>>=1
    return res

def gf_rank(rows):
    if not rows:return 0
    A=[list(row) for row in rows]
    n=len(A[0])
    k=0
    for j in range(n):
        pivot=next((i for i in range(k,len(A)) if A[i][j]),None)
        if pivot is None:continue
        A[k],A[pivot]=A[pivot],A[k]
        inv=gf_pow(A[k][j],Q-2)
        A[k]=[gf_mul(x,inv) for x in A[k]]
        for i in range(len(A)):
            if i!=k and A[i][j]:
                c=A[i][j]
                A[i]=[a^gf_mul(c,b) for a,b in zip(A[i],A[k])]
        k+=1
        if k==len(A):break
    return k

def random_nonzero_vec(N,rng):
    while True:
        v=tuple(rng.randrange(Q) for _ in range(N))
        if any(v):return v

def gframe(M,u):
    # Original public source's ordinary GRS rows, multiplier v_i=1.
    assert 1<=u<M<=Q
    return [tuple(gf_pow(i,j) for j in range(u)) for i in range(M)]

def make_plant(q,N,M,u,seed):
    rng=random.Random(seed)
    assert q>=M and N>=u
    while True:
        T=[random_nonzero_vec(N,rng) for _ in range(u)]
        if gf_rank(T)==u:break
    G=gframe(M,u)
    planted=[tuple(
       _xor_all(gf_mul(a,b) for a,b in zip(g,Tcol))
       for Tcol in zip(*T)
    ) for g in G]
    assert all(any(row) for row in planted)
    positions=rng.sample(range(q),M)
    result=[random_nonzero_vec(N,rng) for _ in range(q)]
    for p,row in zip(positions,planted):result[p]=row
    return result,tuple(positions)

def _xor_all(vals):
    out=0
    for x in vals:out^=x
    return out

def make_null(q,N,seed):
    rng=random.Random(seed)
    return [random_nonzero_vec(N,rng) for _ in range(q)]

def find_low_rank_subset(H,u):
    assert u+1<=len(H)
    for idx in itertools.combinations(range(len(H)),u+1):
        if gf_rank([H[j] for j in idx])<=u:
            return idx
    return None

def null_subset_dep_probability(K,N,j):
    assert 1<=j<=N
    independent=Fraction(1)
    KN=K**N
    for i in range(1,j):
        independent*=Fraction(KN-K**i,KN-1)
    return 1-independent

def false_positive_bound(K,N,q,u):
    return math.comb(q,u+1)*null_subset_dep_probability(K,N,u+1)

class FrameDistinguishingTests(unittest.TestCase):
    def test_all_small_planted_games(self):
        # q=14, M=5, u=2, N=5; every plant contains 3-row dependence.
        q,N,M,u=14,5,5,2
        positive=0;false_positive=0
        trials=30
        for seed in range(trials):
            plant,positions=make_plant(q,N,M,u,seed+100)
            subset=find_low_rank_subset(plant,u)
            positive+=int(subset is not None)
            self.assertTrue(set(subset).issubset(set(positions)))
            null=make_null(q,N,seed+99999)
            false_positive+=int(find_low_rank_subset(null,u) is not None)
        self.assertEqual(positive,trials)
        self.assertEqual(false_positive,0)
        bound=false_positive_bound(Q,N,q,u)
        self.assertLess(bound,Fraction(1,100000))
        print("MDS-HBCE toy public-rank attack:",positive,"/",trials,
              "planted; false positives",false_positive,"/",trials,
              "null analytic false positive bound",float(bound))

    def test_null_dependency_exact_formula(self):
        # Exact sanity check over small K and N: enumerate ALL ordered nonzero
        # 3-row tuples to check formula independently of GF(1024).
        K,N,j=3,3,3
        vectors=[v for v in itertools.product(range(K),repeat=N) if any(v)]
        def rank3(rows):
            A=[list(r) for r in rows];rank=0
            for col in range(N):
                idx=next((i for i in range(rank,len(A)) if A[i][col]),None)
                if idx is None:continue
                A[rank],A[idx]=A[idx],A[rank]
                iv=pow(A[rank][col],-1,K)
                A[rank]=[(x*iv)%K for x in A[rank]]
                for i in range(len(A)):
                    if i!=rank and A[i][col]:
                        c=A[i][col]
                        A[i]=[(x-c*y)%K for x,y in zip(A[i],A[rank])]
                rank+=1
                if rank==len(A):break
            return rank
        dependent=sum(rank3(rows)<j for rows in itertools.product(vectors,repeat=j))
        exact=Fraction(dependent,len(vectors)**j)
        formula=null_subset_dep_probability(K,N,j)
        self.assertEqual(exact,formula)

    def test_fixed_field_is_polynomial_exponent_not_practical(self):
        # A uniform asymptotic family has M<=K=1024, u+1<=1024.
        # If q(lambda) is polynomial, q(lambda)^1024 is polynomial;
        # degree 1024 is NOT a feasible concrete attack claim.
        for M,u in ((256,64),(384,96),(512,128),(1024,1023)):
            self.assertLessEqual(u+1,Q)
            self.assertLessEqual(M,Q)
        for name,q,u in (("R1",27648,64),("R2",124416,96),("R3",497664,128)):
            upper_bits=(u+1)*math.log2(q)
            self.assertGreater(upper_bits,900)
            print(name,"naive public-subset enumeration log2 upper work",
                  round(upper_bits,2),"(UNFEASIBLE at finite profiles)")
if __name__=="__main__":unittest.main(verbosity=2)
