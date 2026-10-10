#!/usr/bin/env python3
"""Exact public three-term-line attack on SG-DIFRA's F3 MaxEnt fibers.

Tests use the ORIGINAL frozen k,d values and independently sampled invertible
left/right changes of basis. Detects guaranteed assignment-space relations.
It does NOT break the archived K=GF(1024) independently random dense labels.
No external libraries or crypto primitives.
"""
from itertools import product
from fractions import Fraction
import random
import unittest

P=3

def rank(M):
    a=[list(row) for row in M]
    r=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][j]%P),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r]
        inv=pow(a[r][j],-1,P)
        a[r]=[(q*inv)%P for q in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][j]:
                mult=a[i][j]
                a[i]=[(q-mult*v)%P for q,v in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def invert(M):
    n=len(M)
    a=[list(row)+[int(i==j) for j in range(n)] for i,row in enumerate(M)]
    for col in range(n):
        pivot=next(i for i in range(col,n) if a[i][col])
        a[col],a[pivot]=a[pivot],a[col]
        inv=pow(a[col][col],-1,P)
        a[col]=[(x*inv)%P for x in a[col]]
        for i in range(n):
            if i!=col and a[i][col]:
                c=a[i][col]
                a[i]=[(x-c*y)%P for x,y in zip(a[i],a[col])]
    return [row[n:] for row in a]

def mm(M,x):
    return tuple(sum(a*b for a,b in zip(row,x))%3 for row in M)

def random_invertible(n,rng):
    while True:
        M=[[rng.randrange(3) for _ in range(n)] for __ in range(n)]
        if rank(M)==n:return M

def fixture(k,d,seed):
    r=k-d
    rng=random.Random(seed)
    A=random_invertible(r,rng)
    B=random_invertible(k,rng)
    Ai,Bi=invert(A),invert(B)
    Q={u:tuple(rng.randrange(3) for _ in range(r))
       for u in product(range(3),repeat=d)}
    def derivative(u):
        nxt=((u[0]+1)%3,)+u[1:]
        return tuple((a-b)%3 for a,b in zip(Q[nxt],Q[u]))
    target=tuple(rng.randrange(3) for _ in range(r))
    fiber=set()
    partition=[]
    for tail in product(range(3),repeat=d-1):
        line=[]
        for j in range(3):
            ur=(j,)+tail
            g=derivative(ur)
            ul=mm(Ai,tuple((a-b)%3 for a,b in zip(target,g)))
            point=mm(Bi,ul+ur)
            line.append(point)
            fiber.add(point)
        partition.append(tuple(line))
    return fiber,partition

def pub_zero_sum_triple_count(fiber):
    S=set(fiber)
    hits=set()
    for a in S:
        for b in S:
            if a==b:continue
            c=tuple((-x-y)%3 for x,y in zip(a,b))
            if c in S and c!=a and c!=b:
                hits.add(tuple(sorted((a,b,c))))
    return len(hits)

class AffineFiberTests(unittest.TestCase):
    def test_all_original_profile_geometries(self):
        for name,k,d in (("SGD-R1",5,3),("SGD-R2",7,4),("SGD-R3",9,5)):
            for seed in (1,7,2028):
                with self.subTest(profile=name,seed=seed):
                    fiber,partition=fixture(k,d,seed)
                    self.assertEqual(len(fiber),3**d)
                    self.assertEqual(len(partition),3**(d-1))
                    self.assertEqual({x for L in partition for x in L},fiber)
                    self.assertEqual(len({x for L in partition for x in L}),len(fiber))
                    for line in partition:
                        self.assertEqual(len(set(line)),3)
                        self.assertEqual(tuple(sum(v[j] for v in line)%3
                                               for j in range(k)),(0,)*k)
                    hits=pub_zero_sum_triple_count(fiber)
                    self.assertGreaterEqual(hits,3**(d-1))
                    print(name,"seed",seed,"public fiber",len(fiber),
                          "certified disjoint triples",len(partition),
                          "public triples",hits)

    def test_conditional_ternary_affine_label_distinguisher(self):
        nu=Fraction(3,16)
        alpha=1-Fraction(3,2)*nu
        p0=(1+2*alpha**3)/3
        p1=Fraction(1,3)
        self.assertGreater(p0-p1,Fraction(1,5))
        self.assertEqual(p0-p1,Fraction(2,3)*alpha**3)
        print("Affine ternary label triple parity advantage/event-gap",float(p0-p1))

if __name__=="__main__":
    unittest.main(verbosity=2)
