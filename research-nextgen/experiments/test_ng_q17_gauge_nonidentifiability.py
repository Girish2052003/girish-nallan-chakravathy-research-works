"""Independent exact enumeration of uniform-gauge posterior and component ambiguity."""
import unittest
from itertools import combinations, permutations
from fractions import Fraction
from ng_q16_robust_relative_sync import multiply, inverse, true_relative_pairs, identity
from ng_q17_gauge_nonidentifiability import (
    components,left_gauge_transform,observed_likelihood,exact_posterior_histogram)


class TestGaugeAmbiguity(unittest.TestCase):
    def test_exact_s3_root_posterior_uniform_under_noise(self):
        G=list(permutations(range(3)))
        obs={(0,1):G[2],(1,2):G[3]}
        probs=exact_posterior_histogram(3,3,obs,[(0,2)],
                   Fraction(3,4),Fraction(1,3),lambda x:x[0])
        self.assertEqual(len(probs),6)
        self.assertEqual(set(probs.values()),{Fraction(1,6)})

    def test_even_clean_complete_ratios_cannot_identify_root(self):
        G=list(permutations(range(3)))
        x=(G[0],G[3],G[5]);obs=true_relative_pairs(x)
        probs=exact_posterior_histogram(3,3,obs,[],Fraction(1),Fraction(0),lambda y:y[0])
        self.assertEqual(set(probs.values()),{Fraction(1,6)})

    def test_disconnected_cross_component_ratio_uniform(self):
        G=list(permutations(range(3)))
        obs={(0,1):G[3],(2,3):G[4]}
        probs=exact_posterior_histogram(4,3,obs,[],Fraction(1),Fraction(0),
                   lambda x:multiply(inverse(x[0]),x[2]))
        self.assertEqual(len(probs),6)
        self.assertEqual(set(probs.values()),{Fraction(1,6)})

    def test_partial_observation_cross_component_still_uniform(self):
        G=list(permutations(range(3)))
        obs={(0,1):G[2],(2,3):G[5]}
        probs=exact_posterior_histogram(4,3,obs,[(0,2),(0,3),(1,2),(1,3)],
                   Fraction(3,4),Fraction(1,4),
                   lambda x:multiply(inverse(x[1]),x[3]))
        self.assertEqual(set(probs.values()),{Fraction(1,6)})

    def test_independent_component_gauge_preserves_likelihood(self):
        G=list(permutations(range(3)))
        comp,nodes=components(5,[(0,1),(1,2),(3,4)])
        self.assertEqual(len(nodes),2)
        original=(G[0],G[1],G[2],G[3],G[4])
        shifted=left_gauge_transform(original,comp,(G[4],G[5]))
        obs={(0,1):G[1],(1,2):G[2],(3,4):G[3]}
        miss=[(i,j) for i,j in combinations(range(5),2) if comp[i]!=comp[j]]
        a=observed_likelihood(original,obs,miss,6,Fraction(4,5),Fraction(1,4))
        b=observed_likelihood(shifted,obs,miss,6,Fraction(4,5),Fraction(1,4))
        self.assertEqual(a,b)

    def test_gauge_ambiguity_can_coexist_with_public_ratio_recovery(self):
        G=list(permutations(range(3)))
        x=(G[3],G[1],G[5],G[2])
        public=true_relative_pairs(x)
        shifted=left_gauge_transform(x,(0,0,0,0),(G[4],))
        self.assertNotEqual(shifted,x)
        self.assertEqual(public,true_relative_pairs(shifted))
        self.assertNotEqual(x[0], identity(3))

    def test_invalid_component_edges_rejected(self):
        with self.assertRaises(ValueError):components(3,[(0,3)])
        with self.assertRaises(ValueError):components(3,[(1,0)])
        with self.assertRaises(ValueError):observed_likelihood((identity(3),)*2,
                                         {(0,1):identity(3)},[(0,1)],6,
                                         Fraction(1,2),Fraction(1,3))

if __name__=='__main__':
    unittest.main(verbosity=2)
