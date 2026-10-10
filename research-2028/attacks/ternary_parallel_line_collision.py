#!/usr/bin/env python3
"""Round 4: exact three-parallel-line public-fiber distinguisher.

SOURCE: ternary NCSG max-entropy fibers from the original 26-page SG-DIFRA.
NULL: independent uniform same-size subsets of F_3^k.
NOT a KEM ciphertext/IND-CPA break of archived GF(1024) dense labels.

Correct probability bounds are proved in active manuscript Sec. 4.2.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb, factorial, perm
import random
import unittest

from ternary_affine_line_leakage import fixture


def lines_by_direction(points):
    S=set(points)
    arr=sorted(S)
    out=Counter()
    for i,x in enumerate(arr):
        for y in arr[i+1:]:
            z=tuple((-a-b)%3 for a,b in zip(x,y))
            if y<z and z in S:
                direction=tuple((a-b)%3 for a,b in zip(x,y))
                first=next(a for a in direction if a)
                if first==2:
                    direction=tuple((2*a)%3 for a in direction)
                out[direction]+=1
    return out


def detect_three_parallel_lines(S):
    return max(lines_by_direction(S).values(),default=0)>=3


def source_lower_bound(k,d):
    # Each of the 3^(d-1) forced lines has an independent direction,
    # uniform among exactly 3^(k-d) possibilities. A triple occupancy
    # therefore guarantees three distinct parallel public affine lines.
    r=k-d
    m=3**r
    L=3**(d-1)
    favourable=0
    for b in range(L//2+1):
        a=L-2*b
        c=m-a-b
        if c<0:continue
        bins=factorial(m)//(factorial(a)*factorial(b)*factorial(c))
        mappings=bins*factorial(L)//2**b
        favourable+=mappings
    return Fraction(m**L-favourable,m**L)


def null_upper_bound(k,d):
    # Uniform size-s subset of F_3^k contains any specified nine
    # distinct points with probability (s)_9/(n)_9.
    # Parallel lines of one direction are disjoint, and there are
    # D=(n-1)/2 directions with n/3 affine lines each.
    n=3**k
    s=3**d
    return Fraction(n-1,2)*comb(n//3,3)*Fraction(perm(s,9),perm(n,9))


class DirectionCollisionTests(unittest.TestCase):
    def test_exact_three_finite_profiles(self):
        expected=((5,3,.5547368172363233,.006904384909547739),
                  (7,4,.9470512035086418,.005910145914401244),
                  (9,5,.9999123630476998,.0026602673524172248))
        for k,d,src_expect,null_expect in expected:
            src=source_lower_bound(k,d)
            null=null_upper_bound(k,d)
            self.assertAlmostEqual(float(src),src_expect,places=14)
            self.assertAlmostEqual(float(null),null_expect,places=14)
            self.assertGreater(src-null,Fraction(1,2))
            print("R4 certified fiber distinguishing gap:",k,d,
                  float(src-null),"source >=",float(src),
                  "uniform <=",float(null))

    def test_exhaustive_GF3_potential_table_19683(self):
        # d=2,r=1,a=e_1: exactly three right-direction cosets.
        # Exhaust ALL 3^9 scalar potential tables, not random samples.
        hits=0
        for code in range(3**9):
            n=code
            Q=[]
            for _ in range(9):
                Q.append(n%3)
                n//=3
            sums=[sum(Q[3*i:3*i+3])%3 for i in range(3)]
            hits+=len(set(sums))==1
        self.assertEqual(hits,3**7)
        self.assertEqual(Fraction(hits,3**9),Fraction(1,9))
        self.assertEqual(source_lower_bound(3,2),Fraction(1,9))
        print("R4 exhaustive potential certificate:",hits,"/",3**9,
              "three forced parallel lines (exact 1/9)")

    def test_public_only_source_vs_uniform_fiber(self):
        rng=random.Random(2045)
        for k,d in ((5,3),(7,4),(9,5)):
            src_hits=null_hits=0
            universe=list(product(range(3),repeat=k))
            for i in range(24):
                S,partition=fixture(k,d,1000+i*31)
                counts=lines_by_direction(S)
                src_hits+=max(counts.values(),default=0)>=3
                self.assertGreaterEqual(sum(counts.values()),3**(d-1))
                U=set(rng.sample(universe,3**d))
                null_hits+=detect_three_parallel_lines(U)
            # Exact symbolic inequalities above provide the theorem;
            # these broad finite checks catch broken implementations.
            self.assertGreaterEqual(src_hits,9)
            self.assertLessEqual(null_hits,4)
            print("R4 public-only detector",k,d,
                  "source",src_hits,"/24","uniform false positives",
                  null_hits,"/24")


if __name__=="__main__":
    unittest.main(verbosity=2)
