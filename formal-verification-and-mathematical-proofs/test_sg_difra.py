#!/usr/bin/env python3
"""Finite-field regressions and toy cryptanalysis only; NOT a security proof."""
import itertools
import random
import unittest

Q=1024
P=(1<<10)|(1<<3)|1

def mul(a,b):
    z=0
    for _ in range(10):
        if b&1: z^=a
        b >>= 1
        a <<= 1
        if a & Q: a ^= P
    return z & (Q-1)

def powfield(a,n):
    z=1
    while n:
        if n&1: z=mul(z,a)
        a=mul(a,a)
        n >>= 1
    return z

def inverse(a):
    assert a
    return powfield(a,Q-2)

def polmul(a,b):
    z=0
    while b:
        if b&1: z ^= a
        a <<= 1; b >>= 1
    return z

def rem(a,b):
    while a and a.bit_length()>=b.bit_length():
        a ^= b << (a.bit_length()-b.bit_length())
    return a

def gcd(a,b):
    while b: a,b=b,rem(a,b)
    return a

def irreducible():
    x=2
    v=x
    for j in range(1,11):
        v=rem(polmul(v,v),P)
        if j in (2,5) and gcd(v^x,P)!=1: return False
    return v==x

def rank(A):
    a=[row[:] for row in A]
    if not a: return 0
    ncol=len(a[0])
    k=0
    for col in range(ncol):
        piv=next((i for i in range(k,len(a)) if a[i][col]),None)
        if piv is None: continue
        a[k],a[piv]=a[piv],a[k]
        scale=inverse(a[k][col])
        for j in range(col,ncol): a[k][j]=mul(a[k][j],scale)
        for i in range(len(a)):
            if i==k or not a[i][col]: continue
            t=a[i][col]
            for j in range(col,ncol): a[i][j]^=mul(t,a[k][j])
        k+=1
        if k==len(a): break
    return k

def solve(A,b):
    n=len(A)
    a=[list(row)+[v] for row,v in zip(A,b)]
    for col in range(n):
        piv=next((i for i in range(col,n) if a[i][col]),None)
        if piv is None: return None
        a[col],a[piv]=a[piv],a[col]
        scale=inverse(a[col][col])
        for j in range(col,n+1): a[col][j]=mul(a[col][j],scale)
        for i in range(n):
            if i==col or not a[i][col]: continue
            t=a[i][col]
            for j in range(col,n+1): a[i][j]^=mul(t,a[col][j])
    return [row[n] for row in a]

def dot(a,b):
    z=0
    for x,y in zip(a,b): z^=mul(x,y)
    return z

def noisy(r):
    if r.randrange(16)<3: return r.randrange(1,Q)
    return 0

def clean_basis_attack(H,y,N,threshold):
    # Exponential exhaustive enumeration, deliberately restricted to *toy* N.
    for idx in itertools.combinations(range(len(H)),N):
        t=solve([H[i] for i in idx],[y[i] for i in idx])
        if t is not None and sum(dot(row,t)==v for row,v in zip(H,y))>=threshold:
            return t
    return None

def clause(a,b,c,y):
    return a^b^c^(a&b)^(a&c)^(b&c)^(a&b&c)^(y&(a^b^c^(a&b)^(a&c)^(b&c)))

class ResearchRegressions(unittest.TestCase):
    def test_gf2_10_irreducible(self):
        self.assertTrue(irreducible())
        for v in range(1,Q): self.assertEqual(mul(v,inverse(v)),1)

    def test_balanced_clause_and_satisfiability(self):
        self.assertEqual(sum(clause(*v) for v in itertools.product((0,1),repeat=4)),8)
        for a,b,c in itertools.product((0,1),repeat=3):
            self.assertEqual(any(clause(a,b,c,y) for y in (0,1)),bool(a or b or c))

    def test_f3_regular_fiber_and_zero_line_sum(self):
        r=random.Random(42)
        tab=[[r.randrange(3) for _ in range(3)] for _ in range(3)]
        counts=[0,0,0]
        for x,j in itertools.product(range(3),repeat=2):
            d=(tab[(x+1)%3][j]-tab[x][j])%3
            for a in range(3): counts[(a+d)%3]+=1
        self.assertEqual(counts,[9,9,9])
        for j in range(3):
            self.assertEqual(sum(tab[(x+1)%3][j]-tab[x][j] for x in range(3))%3,0)

    def test_mds_girth(self):
        G=[[powfield(i,j) for j in range(4)] for i in range(10)]
        for j in range(1,5):
            for idx in itertools.combinations(range(10),j):
                self.assertEqual(rank([G[i] for i in idx]),j)
        for idx in itertools.combinations(range(10),5):
            self.assertEqual(rank([G[i] for i in idx]),4)

    def test_secret_incidence_reparametrization(self):
        r=random.Random(101)
        for _ in range(100):
            s=[r.randrange(3) for _ in range(4)]
            sigma=[r.randrange(3) for _ in range(4)]
            delta=[(v-t)%3 for v,t in zip(sigma,s)]
            self.assertEqual([(v+d)%3 for v,d in zip(s,delta)],sigma)
            self.assertEqual([(0+v)%3 for v in sigma],sigma)

    def test_exhaustive_small_clean_basis_attack(self):
        r=random.Random(20261010)
        N,q,threshold=3,24,12
        for _ in range(12):
            H=[[r.randrange(Q) for _ in range(N)] for _ in range(q)]
            t=[r.randrange(Q) for _ in range(N)]
            zero=[dot(h,t)^noisy(r) for h in H]
            self.assertEqual(clean_basis_attack(H,zero,N,threshold),t)
            one=[r.randrange(Q) for _ in range(q)]
            self.assertIsNone(clean_basis_attack(H,one,N,threshold))

    def test_fixed_field_bound(self):
        self.assertEqual(len(set(range(Q))),Q)
        self.assertTrue(1025>Q)

if __name__=="__main__":
    unittest.main(verbosity=2)
