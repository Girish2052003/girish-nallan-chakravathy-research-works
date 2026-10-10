#!/usr/bin/env python3
"""Adversarial regression: publicly generated bounded-degree NCSG ideal ciphertexts
are efficiently distinguishable by elementary linear algebra over F3.

This is a BREAK of an experimental idea, not an implementation of a secure KEM.
No external crypto algorithms or packages are used.
"""
from itertools import combinations, product
from math import comb
from random import Random
import unittest

P=3
N=3
D=1  # degree bound for public multipliers
TOTAL=3 # upper bound on total degree of sampled output

def exponents(n,t):
    return [v for v in product(range(t+1),repeat=n) if sum(v)<=t]

MON=exponents(N,TOTAL)
MULT=exponents(N,D)
def add(a,b):
    return tuple((x+y) for x,y in zip(a,b))
def monomial_mul(f,e):
    return {add(k,e):v for k,v in f.items() if sum(add(k,e))<=TOTAL}
def add_scaled(target,source,coefficient):
    for k,v in source.items():
        target[k]=(target.get(k,0)+coefficient*v)%P
        if target[k]==0:target.pop(k)
def vector(f):
    return [f.get(k,0) for k in MON]
def rank(rows):
    if not rows:return 0
    a=[list(r) for r in rows]
    k=0
    cols=len(a[0])
    for j in range(cols):
        pivot=next((i for i in range(k,len(a)) if a[i][j]%P),None)
        if pivot is None:continue
        a[k],a[pivot]=a[pivot],a[k]
        inv=pow(a[k][j],-1,P)
        a[k]=[(v*inv)%P for v in a[k]]
        for i in range(len(a)):
            if i==k:continue
            c=a[i][j]
            if c:a[i]=[(x-c*y)%P for x,y in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k
def eval_poly(f,s):
    return sum(v*__import__("functools").reduce(
        lambda acc,term:acc*term,[pow(x,e,P) for x,e in zip(s,mon)],1)
        for mon,v in f.items())%P
def private_witness_relations(s):
    raw=[
      {(1,0,0):1,(0,1,0):1,(0,0,1):1},
      {(1,1,0):1,(0,0,1):1,(0,0,0):1},
      {(0,1,1):1,(1,0,0):1,(0,0,0):2},
    ]
    ans=[]
    for p in raw:
        q=dict(p)
        add_scaled(q,{(0,0,0):1},-eval_poly(p,s))
        ans.append(q)
    return ans
def public_span(relations):
    return [vector(monomial_mul(r,e)) for r in relations for e in MULT]
def encrypt_ideal_zero(relations,rng):
    c={}
    for row in public_span(relations):
        k=rng.randrange(P)
        for ix,v in enumerate(row):
            if v:
                mon=MON[ix]
                c[mon]=(c.get(mon,0)+k*v)%P
                if c[mon]==0:c.pop(mon)
    return vector(c)
def random_one(rng):
    return [rng.randrange(P) for _ in MON]
def distinguisher(relations,sample):
    basis=public_span(relations)
    return 0 if rank(basis+[sample])==rank(basis) else 1

class IdealAttackTest(unittest.TestCase):
    def test_membership_break(self):
        rng=Random(20261010)
        total_zero_correct=0
        false_zero=0
        count=150
        s=(1,2,1)
        r=private_witness_relations(s)
        basis=public_span(r)
        self.assertLess(rank(basis),len(MON))
        for _ in range(count):
            zero=encrypt_ideal_zero(r,rng)
            one=random_one(rng)
            total_zero_correct+=int(distinguisher(r,zero)==0)
            false_zero+=int(distinguisher(r,one)==0)
        self.assertEqual(total_zero_correct,count)
        self.assertLessEqual(false_zero,3)
        print("NCSG ideal-membership distinguisher: bit-0 detected",total_zero_correct,
              "/",count,"; uniform false accepts",false_zero,"/",count)
        print("Ambient coefficient dimension",len(MON),"public multiplication span rank",rank(basis))
    def test_decapsulation_trapdoor_correctness_is_not_secrecy(self):
        rng=Random(23); s=(1,2,1)
        r=private_witness_relations(s)
        for _ in range(30):
            vec=encrypt_ideal_zero(r,rng)
            poly=dict(zip(MON,vec))
            self.assertEqual(eval_poly(poly,s),0)
        # Yet exactly those 30 samples were PUBLICLY recognisable.
    def test_size_polynomial_for_constant_degree(self):
        for n in range(2,20):
            t=3
            self.assertEqual(comb(n+t,t),comb(n+t,n))
            self.assertLess(comb(n+t,t),(n+5)**3)
if __name__=="__main__":
    unittest.main(verbosity=2)
