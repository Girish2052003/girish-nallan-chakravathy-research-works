#!/usr/bin/env python3
"""Round 6: exact, PUBLIC-ONLY affine-linearity subspace recovery.

The complete public truth table f:F_3^k -> F_3^r of the original ternary
MaxEnt NCSG construction reveals B^{-1}(F_3^r x <a>) with explicitly bounded
failure probability. The algorithm never accesses secret A, B, a or Q.

It requires a public complete table or exhaustively evaluable f, with cost
polynomial in the EXPLICIT table size 3^k, NOT polynomial in compact k.
This is NOT an IND-CPA/CCA ciphertext break of archived GF(1024) labels.
"""
from itertools import product
from fractions import Fraction
import random
import unittest

def mm(M,v):
    return tuple(sum(a*b for a,b in zip(row,v))%3 for row in M)
def rank(M):
    if not M:return 0
    A=[list(x) for x in M]; piv=0
    for col in range(len(A[0])):
        ix=next((i for i in range(piv,len(A)) if A[i][col]),None)
        if ix is None:continue
        A[piv],A[ix]=A[ix],A[piv]
        inv=pow(A[piv][col],-1,3)
        A[piv]=[(v*inv)%3 for v in A[piv]]
        for j in range(len(A)):
            if j!=piv and A[j][col]:
                c=A[j][col]
                A[j]=[(u-c*v)%3 for u,v in zip(A[j],A[piv])]
        piv+=1
        if piv==len(A):break
    return piv
def inv_random(n,rng):
    while True:
        M=[[rng.randrange(3) for _ in range(n)] for j in range(n)]
        if rank(M)==n:return M
def add(a,b):return tuple((x+y)%3 for x,y in zip(a,b))
def sub(a,b):return tuple((x-y)%3 for x,y in zip(a,b))
def neg(a):return tuple((-x)%3 for x in a)

def original_source_fixture(k,d,seed):
    r=k-d; rng=random.Random(seed)
    A=inv_random(r,rng); B=inv_random(k,rng)
    a=tuple(rng.randrange(3) for _ in range(d))
    while not any(a):a=tuple(rng.randrange(3) for _ in range(d))
    Q={z:tuple(rng.randrange(3) for _ in range(r))
       for z in product(range(3),repeat=d)}
    F={}
    for x in product(range(3),repeat=k):
        ulz=mm(B,x); ul,z=ulz[:r],ulz[r:]
        F[x]=add(mm(A,ul),sub(Q[add(z,a)],Q[z]))
    # This witness is used ONLY in testing, never by attacker.
    a_sub={tuple((t*v)%3 for v in a) for t in range(3)}
    expected={h for h in F if mm(B,h)[r:] in a_sub}
    return F,expected

def projective(h):
    ix=next((i for i,v in enumerate(h) if v),None)
    if ix is None:return None
    return h if h[ix]==1 else neg(h)

def zero_second_difference(F,h,x):
    return all((u+v+w)%3==0 for u,v,w in zip(
        F[x],F[add(x,h)],F[sub(x,h)]))

def public_recover_direction_subspace(F,k):
    """Only F and k as input: full deterministic validation follows screening.

    O(k*r*3^(2k)) worst case: polynomial in explicit public-table length,
    exponential in succinct bit/circuit representation of k.
    """
    D=list(F); rng=random.Random(2029)
    probes=rng.sample(D,min(32,len(D)))
    valid=[]
    # A complete public table need not put the origin first. Projective
    # normalization already rejects zero; skipping a key loses directions.
    for h in D:
        if projective(h)!=h:continue
        if all(zero_second_difference(F,h,x) for x in probes):
            if all(zero_second_difference(F,h,x) for x in D):
                valid.append(h)
    recovered={(0,)*k}
    for h in valid:recovered.add(h);recovered.add(neg(h))
    return recovered

def exact_operator_rank(d):
    """GF(3) matrix rank of (T_a-1)(T_b-1)^2 on F_3^d."""
    Z=list(product(range(3),repeat=d))
    ids={z:i for i,z in enumerate(Z)}
    a=(1,)+(0,)*(d-1)
    b=(0,1)+(0,)*(d-2)
    H=[[0]*len(Z) for _ in Z]
    for z in Z:
        for t in range(3):
            off=tuple((t*v)%3 for v in b)
            pos=ids[add(add(z,a),off)]
            negpos=ids[add(z,off)]
            H[ids[z]][pos]=(H[ids[z]][pos]+1)%3
            H[ids[z]][negpos]=(H[ids[z]][negpos]-1)%3
    return rank(H)

def failure_upper_bound(k,d):
    r=k-d
    return Fraction(3**k-3**(r+1),3**(2*r*3**(d-2)))

class PublicStructuralAttackTests(unittest.TestCase):
    def test_reordered_public_table_preserves_recovered_subspace(self):
        F, expected = original_source_fixture(5, 3, 12)
        first = (1, 1, 1, 0, 0)
        self.assertIn(first, expected)
        reordered = {first: F[first]}
        reordered.update(F)
        self.assertEqual(public_recover_direction_subspace(reordered, 5), expected)

    def test_exact_difference_operator_rank(self):
        for d in (2,3,4,5):
            self.assertEqual(exact_operator_rank(d),2*3**(d-2))
            print("Round6 exact derivative rank",d,2*3**(d-2))
    def test_exhaustive_GF3_potential_19683(self):
        Z=list(product(range(3),repeat=2))
        hits=0; a=(1,0)
        for code in range(3**9):
            Q={}; n=code
            for z in Z:Q[z]=n%3;n//=3
            if all(sum(Q[add(add(z,a),(0,t))]-Q[add(z,(0,t))]
                       for t in range(3))%3==0 for z in Z):
                hits+=1
        self.assertEqual(hits,3**7)
        self.assertEqual(Fraction(hits,3**9),Fraction(1,9))
        print("Round6 exact 3^9 potential tables:",hits,"/",3**9)
    def test_public_only_recovery_R1_R2_R3(self):
        for k,d in ((5,3),(7,4),(9,5)):
            for seed in ((12,27) if k<9 else (12,)):
                with self.subTest(k=k,d=d,seed=seed):
                    F,hidden=original_source_fixture(k,d,seed)
                    result=public_recover_direction_subspace(F,k)
                    self.assertEqual(result,hidden)
                    self.assertEqual(len(result),3**(k-d+1))
                    self.assertEqual(rank(list(result)),k-d+1)
                    print("Round6 recover from PUBLIC map",k,d,seed,
                          "dim",rank(list(result)),"elements",len(result))
    def test_exact_source_profile_bounds(self):
        for k,d in ((5,3),(7,4),(9,5)):
            b=failure_upper_bound(k,d)
            self.assertLess(b,Fraction(1,2000))
            print("Round6 source failure probability bound",k,d,
                  str(b),float(b))

if __name__=="__main__":unittest.main(verbosity=2)
