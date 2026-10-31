"""Independent tests for exact probability formulas; no security claims."""
from itertools import combinations,product
from fractions import Fraction
import unittest
from public_global_shift_survival_bound import (
  local_survival_probability, expected_nonzero_shifts,
  complete_uniform_scope_expected, complete_uniform_scope_probability_bound,
  mixed_difference_rank)

class SourceSurvivalTests(unittest.TestCase):
    def test_local_operator_rank_independently(self):
        for d in (2,3):
            a = (1,) + (0,)*(d-1)
            for v in product(range(3),repeat=d):
                if not any(v):continue
                expected=3**(d-1) if v[1:]==(0,)*(d-1) else 4*3**(d-2)
                self.assertEqual(mixed_difference_rank(d,a,v),expected,(d,a,v))

    def test_exhaustive_19683_potential_tables(self):
        points=list(product(range(3),repeat=2)); loc={x:i for i,x in enumerate(points)}
        def diff(Q,v):
            return tuple((Q[loc[((x[0]+v[0])%3,(x[1]+v[1])%3)]]-Q[loc[x]])%3 for x in points)
        counts={(1,0):0,(0,1):0}
        for Q in product(range(3),repeat=9):
            g=diff(Q,(1,0))
            for v in counts:
                counts[v]+=int(len(set(diff(g,v)))==1)
        self.assertEqual(counts,{(1,0):2187,(0,1):729})
        self.assertEqual(local_survival_probability(1,2),Fraction(5,39))

    def test_exact_first_moment_matches_scope_enumeration(self):
        for n in (3,4,5):
            scopes=list(combinations(range(n),3))
            self.assertEqual(expected_nonzero_shifts(scopes,n),
                             complete_uniform_scope_expected(n))
        self.assertEqual(complete_uniform_scope_probability_bound(4),
                         Fraction(14000,771147))
        self.assertLess(complete_uniform_scope_probability_bound(5),Fraction(1,10000))
        self.assertLess(complete_uniform_scope_probability_bound(6),Fraction(1,100000000))

    def test_disconnected_and_empty_scope_bounds(self):
        # An unused variable always supplies a nonzero global shift.
        self.assertEqual(expected_nonzero_shifts([(0,1,2)],4), Fraction(12))
        self.assertEqual(expected_nonzero_shifts([],2), Fraction(8))

if __name__ == '__main__':unittest.main(verbosity=2)
