#!/usr/bin/env python3
"""Round 7: exact public inversion of the 2026 ternary MaxEnt NCSG map.

The publicly available local map f(x) = A u_L + (T_a-I)Q(u_R),
(u_L,u_R)=Bx, has PUBLIC additive shift directions. One can construct a
linear right inverse from a COMPLETE public truth table without A,B,a,Q,
without any hardness assumption, and for EVERY table Q (probability one).

This is a local predicate inversion, NOT global NCSG-DS solution,
NOT recovered original secret B or global witness, and NOT a direct
attack on the old independent GF(1024) labels. Running time is
polynomial in the EXPLICIT truth-table size 3^k, not in a succinct k.
"""
from itertools import product
from fractions import Fraction
import random
import unittest
from public_second_difference_subspace_recovery import (
    mm,rank,inv_random,add,sub,original_source_fixture
)

def delta(F,h,x):
    return sub(F[add(x,h)],F[x])

def all_constant_shifts(F,probes=32):
    """Enumerate every constant derivative direction from PUBLIC F only."""
    D=list(F)
    rng=random.Random(7007)
    sample=rng.sample(D,min(probes,len(D)))
    result={}
    for h in D:
        d=delta(F,h,D[0])
        if all(delta(F,h,x)==d for x in sample):
            if all(delta(F,h,x)==d for x in D):
                result[h]=d
    return result

def public_shift_basis(F,probes=32):
    """Extract r public shifts with independent output increments.

    Never samples any secret A,B,a,Q. Probe filtering never accepts
    a candidate without a full exhaustive all-input check.
    """
    D=list(F)
    r=len(F[D[0]])
    rng=random.Random(2028)
    sample=rng.sample(D,min(probes,len(D)))
    shifts=[];increments=[]
    for h in D[1:]:
        d=delta(F,h,D[0])
        if rank(increments+[d])==len(increments):
            continue
        if not all(delta(F,h,x)==d for x in sample):
            continue
        if not all(delta(F,h,x)==d for x in D):
            continue
        shifts.append(h)
        increments.append(d)
        if len(increments)==r:
            return shifts,increments
    raise AssertionError("No public affine right inverse: model violation")

def solve_target(increments,rhs):
    """Solve columns (increments) times coeff = rhs over GF(3)."""
    n=len(rhs)
    A=[[increments[j][i] for j in range(n)]+[rhs[i]] for i in range(n)]
    for col in range(n):
        i=next((j for j in range(col,n) if A[j][col]),None)
        if i is None:raise ValueError("Not a basis")
        A[col],A[i]=A[i],A[col]
        inv=pow(A[col][col],-1,3)
        A[col]=[(x*inv)%3 for x in A[col]]
        for j in range(n):
            if j!=col and A[j][col]:
                c=A[j][col]
                A[j]=[(x-c*y)%3 for x,y in zip(A[j],A[col])]
    return tuple(row[-1] for row in A)

def public_invert(F,target,basis=None):
    """Return x satisfying F[x]==target, with no hidden witness."""
    k=len(next(iter(F)))
    if basis is None:
        basis=public_shift_basis(F)
    shifts,increments=basis
    x0=(0,)*k
    coeff=solve_target(increments,sub(target,F[x0]))
    out=x0
    for c,h in zip(coeff,shifts):
        out=add(out,tuple((c*z)%3 for z in h))
    assert F[out]==target
    return out

def source_extra_shift_bound(k,d):
    """Finite union bound for C(f)!=B^-1(F3^r x {0})."""
    r=k-d
    return (Fraction(2*3**r,3**(r*(3**(d-1)-1)))+
            Fraction((3**d-3)*3**r,3**(r*(4*3**(d-2)-1))))

def op(F,a,b,z):
    # Mixed finite difference (T_b-I)(T_a-I)F.
    return (F[add(add(z,a),b)]-F[add(z,a)]-F[add(z,b)]+F[z])%3

def is_constant_mixed(F,a,b):
    Z=list(F)
    y=op(F,a,b,Z[0])
    return all(op(F,a,b,z)==y for z in Z)

def exact_rank_mixed(d,parallel):
    Z=list(product(range(3),repeat=d))
    a=(1,)+(0,)*(d-1)
    b=a if parallel else (0,1)+(0,)*(d-2)
    M=[[0]*len(Z) for _ in Z]
    for i,z in enumerate(Z):
        for zz,c in ((add(add(z,a),b),1),(add(z,a),-1),
                     (add(z,b),-1),(z,1)):
            M[i][Z.index(zz)]=(M[i][Z.index(zz)]+c)%3
    return rank(M)

class PublicInversionTests(unittest.TestCase):
    def test_r1_r2_r3_every_target_using_public_data(self):
        for k,d in ((5,3),(7,4),(9,5)):
            F,_=original_source_fixture(k,d,2000+k)
            basis=public_shift_basis(F)
            self.assertEqual(rank(basis[1]),k-d)
            for target in product(range(3),repeat=k-d):
                x=public_invert(F,target,basis)
                self.assertEqual(F[x],target)
            self.assertEqual(len(basis[0]),k-d)
            print("R7 ALL public local targets inverted",k,d,
                  "targets",3**(k-d),"basis size",len(basis[0]))


    def test_public_translations_biject_every_local_fiber(self):
        # One public shift maps the ENTIRE preimage of target t to that of
        # another target tprime. This test never accesses A,B,a or Q.
        for k,d in ((5,3),(7,4),(9,5)):
            F,_=original_source_fixture(k,d,2100+k)
            basis=public_shift_basis(F)
            r=k-d
            alltargets=list(product(range(3),repeat=r))
            baseline=alltargets[0]
            preimage0={x for x,y in F.items() if y==baseline}
            self.assertEqual(len(preimage0),3**d)
            for target in alltargets:
                h=public_invert(F,target,basis)
                translated={add(x,h) for x in preimage0}
                expected={x for x,y in F.items() if y==target}
                self.assertEqual(translated,expected)
            print("R7 ALL local fibers publicly translation equivalent",
                  k,d,"targets",len(alltargets),"per fiber",len(preimage0))

    def test_constant_direction_subspace_and_linearity(self):
        # Independently reconstruct the FULL constant-derivative space on
        # R1/R2. Every locally linear mask is public and its increment
        # map is additive; secret A,B are never inputs.
        for k,d in ((5,3),(7,4)):
            F,V=original_source_fixture(k,d,2030+k)
            C=all_constant_shifts(F)
            self.assertTrue(set(C).issubset(V))
            self.assertEqual(len(C),3**(k-d))
            H=list(C)
            rng=random.Random(2030)
            for i in range(100):
                h,h2=rng.choice(H),rng.choice(H)
                self.assertEqual(C[add(h,h2)],add(C[h],C[h2]))
            self.assertEqual(rank(list(C.values())),k-d)
            print("R7 public constant shift subspace",k,d,
                  "dimension",rank(list(C)),"size",len(C))

    def test_exact_mixed_operator_ranks(self):
        for d in (2,3,4):
            self.assertEqual(exact_rank_mixed(d,True),3**(d-1))
            self.assertEqual(exact_rank_mixed(d,False),4*3**(d-2))
            print("R7 exact mixed shift rank",d,
                  "parallel",3**(d-1),"independent",4*3**(d-2))

    def test_exhaustive_19683_tables_local_false_shift(self):
        Z=list(product(range(3),repeat=2))
        a=(1,0); b=(0,1); par=ind=0
        for code in range(3**9):
            Q={};n=code
            for z in Z:
                Q[z]=n%3;n//=3
            par+=int(is_constant_mixed(Q,a,a))
            ind+=int(is_constant_mixed(Q,a,b))
        self.assertEqual(par,3**7)
        self.assertEqual(ind,3**6)
        print("R7 19,683 scalar potentials: extra parallel",par,
              "extra independent",ind)

    def test_explicit_probability_bounds(self):
        for k,d in ((5,3),(7,4),(9,5)):
            p=source_extra_shift_bound(k,d)
            self.assertLess(p,Fraction(1,1000000))
            print("R7 exact extra-shift failure bound",k,d,
                  p,float(p))
if __name__=="__main__":
    unittest.main(verbosity=2)
