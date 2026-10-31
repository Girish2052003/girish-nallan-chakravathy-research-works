"""Finite independent collision checks and exhaustive planted fiber tests."""
import unittest
from itertools import product,combinations
from fractions import Fraction
from random import Random
from planted_witness_uniqueness_bound import (
    nonzero_local_collision_probability,expected_other_witnesses,
    complete_uniform_scope_expected_other,probability_not_unique_upper_bound)
from random_source_shift_codimension_probe import sample


class PlantedCollisionTests(unittest.TestCase):
    def test_exact_mixed_difference_collision_19683_tables(self):
        pts=list(product(range(3),repeat=2)); idx={p:i for i,p in enumerate(pts)}
        def diff(Q,v):
            return tuple((Q[idx[((x[0]+v[0])%3,(x[1]+v[1])%3)]]-Q[idx[x]])%3 for x in pts)
        for v in ((1,0),(0,1),(2,1)):
            hits=0
            for Q in product(range(3),repeat=9):
                g=diff(Q,(1,0))
                hits+=int(diff(g,v)[0]==0)
            self.assertEqual(hits,6561)
        self.assertEqual(nonzero_local_collision_probability(1,2),Fraction(4,13))
        self.assertEqual(nonzero_local_collision_probability(2,3),Fraction(26,242))

    def test_exact_first_moment_weight_enumeration(self):
        for n in (3,4,5):
            scopes=list(combinations(range(n),3))
            self.assertEqual(expected_other_witnesses(scopes,n),
                             complete_uniform_scope_expected_other(n))
        self.assertLess(probability_not_unique_upper_bound(5),Fraction(1,50))
        self.assertLess(probability_not_unique_upper_bound(6),Fraction(1,10000))

    def test_finite_independent_secret_fiber_reproduction(self):
        # Data-only: all candidate solutions independently enumerated.
        for n in (4,5,6):
            m=len(list(combinations(range(n),3)))
            for j in range(12):
                seed=20261110+1000*n+100*m+j
                public=sample(n,m,seed)
                rng=Random(seed+123456)
                secret=tuple(rng.randrange(3) for _ in range(n))
                t=public._evaluate(secret)
                fiber=[x for x in product(range(3),repeat=n) if public._evaluate(x)==t]
                self.assertIn(secret,fiber)
                self.assertGreaterEqual(len(fiber),1)
                if n==6:
                    self.assertEqual(len(fiber),1)

if __name__=='__main__':unittest.main(verbosity=2)
