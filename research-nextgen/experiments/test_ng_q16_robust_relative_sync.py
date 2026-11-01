"""Adversarial and independent tests for NG-Q16 public relative synchronization."""
import unittest
from fractions import Fraction
from collections import Counter
from itertools import combinations, permutations
from math import comb, factorial
from random import Random

from ng_q16_robust_relative_sync import (
    identity, inverse, multiply, directed, sample_public, two_hop_votes,
    public_recover, true_relative_pairs, clean_two_hop_counts,
    deterministic_majority_certificate, hoeffding_failure_upper,
    strict_clean_majority_bound)


class TestTwoHopPublicRecovery(unittest.TestCase):
    def test_noncommutative_permutation_composition(self):
        a = (1, 0, 2)
        b = (1, 2, 0)
        self.assertNotEqual(multiply(a, b), multiply(b, a))
        self.assertEqual(multiply(inverse(a), a), identity(3))

    def test_all_S3_ground_truth_clean(self):
        group = list(permutations(range(3)))
        for i in range(6):
            x = (group[i], group[(i+2)%6], group[(i+4)%6], group[(i+3)%6])
            public = true_relative_pairs(x)
            est, margins = two_hop_votes(4, 3, public)
            self.assertEqual(est, public)
            self.assertEqual(public_recover(4,3,public)['status'],'self_consistent')
            self.assertTrue(all(v == (2,0,2) for v in margins.values()))

    def test_adversarial_corruption_per_vertex_bound(self):
        n,k = 32,4
        x, full, bad = sample_public(n,k,1.0,0.0,99811)
        rng=Random(9922)
        # Every vertex has corrupted degree 4: edges of cyclic step 1 or 2.
        bad=set()
        for i,j in combinations(range(n),2):
            diff = (j-i)%n
            if diff in (1,2,n-1,n-2):
                old=full[(i,j)]
                replacement=old
                while replacement==old:
                    replacement=tuple(rng.sample(range(k),k))
                full[(i,j)]=replacement
                bad.add((i,j))
        degrees=Counter()
        for i,j in bad:
            degrees[i]+=1;degrees[j]+=1
        self.assertEqual(set(degrees.values()),{4})
        self.assertLess(2*max(degrees.values()),(n-2)/2)
        self.assertTrue(deterministic_majority_certificate(n,full,bad))
        out=public_recover(n,k,full)
        self.assertEqual(out['status'],'self_consistent')
        self.assertEqual(out['estimated_pairs'],true_relative_pairs(x))

    def test_uniform_noisy_complete_S3(self):
        for seed in range(3):
            x,p,bad=sample_public(90,3,1.0,0.36,81211+seed)
            self.assertEqual(len(p),comb(90,2))
            out=public_recover(90,3,p)
            self.assertEqual(out['status'],'self_consistent')
            self.assertEqual(out['estimated_pairs'],true_relative_pairs(x))
            # Honest-majority sufficient condition need not hold when eps>0.293.

    def test_erasures_and_noise(self):
        for seed in range(3):
            x,p,bad=sample_public(90,4,0.78,0.1,31141+seed)
            self.assertLess(len(p),comb(90,2))
            out=public_recover(90,4,p)
            self.assertEqual(out['status'],'self_consistent')
            self.assertEqual(out['estimated_pairs'],true_relative_pairs(x))

    def test_missing_no_two_hop_paths_is_inconclusive(self):
        x,p,bad=sample_public(5,3,0.0,0.0,11211)
        self.assertFalse(p)
        out=public_recover(5,3,p)
        self.assertEqual(out['status'],'inconclusive')
        self.assertEqual(out['estimated_pairs'],{})

    def test_constant_corrupted_group_does_not_use_hidden_secret(self):
        n=6
        x,p,bad=sample_public(n,3,1.0,0.0,4488)
        # Overwrite public input to be an internally consistent but incorrect
        # all-identity gauge. A public algorithm cannot know this is forged.
        fake={(i,j): identity(3) for i,j in combinations(range(n),2)}
        out=public_recover(n,3,fake)
        self.assertEqual(out['status'],'self_consistent')
        self.assertNotEqual(out['estimated_pairs'],true_relative_pairs(x))
        # This confirms why self_consistent != certified planted truth.

    def test_failure_bounds_and_small_n_are_conservative(self):
        self.assertEqual(hoeffding_failure_upper(3,6,0.0,0.0),1.0)
        self.assertEqual(strict_clean_majority_bound(30,1.0,0.5),1.0)
        self.assertLess(hoeffding_failure_upper(120,6,1.0,0.05),1.0)
        self.assertLess(strict_clean_majority_bound(1200,1.0,0.02),1.0)
        self.assertGreaterEqual(hoeffding_failure_upper(120,6,1.0,0.05),0)

    def test_single_twohop_distribution_exact_over_all_S3_labels(self):
        G=list(permutations(range(3)))
        xi,xh,xj=G[2],G[4],G[5]
        a=multiply(inverse(xi),xh)
        b=multiply(inverse(xh),xj)
        truth=multiply(a,b)
        epsilon=Fraction(1,2)
        rho=Fraction(3,4)
        weights=Counter()
        for u in G:
            for v in G:
                pu=(1-epsilon)*int(u==a)+epsilon/6
                pv=(1-epsilon)*int(v==b)+epsilon/6
                weights[multiply(u,v)]+=rho*rho*pu*pv
        self.assertEqual(weights[truth],Fraction(27,128))
        self.assertEqual({weights[g] for g in G if g!=truth},{Fraction(9,128)})
        self.assertEqual(weights[truth]-weights[G[0] if G[0]!=truth else G[1]],
                         rho*rho*(1-epsilon)**2)
        self.assertEqual(sum(weights.values()),rho*rho)

    def test_nonflat_transport_does_not_satisfy_twohop_identity(self):
        e=identity(3)
        a=(1,0,2); b=(1,2,0)
        # No hidden vertex changes, so B_ij=H_ij. Yet H_01 H_12 != H_02.
        nonflat={(0,1):a,(1,2):b,(0,2):e}
        estimated,_=two_hop_votes(3,3,nonflat)
        self.assertEqual(estimated[(0,2)],multiply(a,b))
        self.assertNotEqual(estimated[(0,2)],nonflat[(0,2)])

    def test_invalid_observations(self):
        with self.assertRaises(ValueError):
            two_hop_votes(4,3,{(0,2):(0,0,1)})
        with self.assertRaises(ValueError):
            two_hop_votes(4,3,{(2,0):(0,1,2)})
        with self.assertRaises(ValueError):
            sample_public(3,3,1.1,0.0,12)

if __name__ == '__main__':
    unittest.main(verbosity=2)
