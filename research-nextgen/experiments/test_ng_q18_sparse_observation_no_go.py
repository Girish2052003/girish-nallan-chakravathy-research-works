import unittest
from fractions import Fraction
from itertools import combinations
from ng_q18_sparse_observation_no_go import (
    isolation_moments,isolation_lower_bound,sample_er_edges,isolated_vertices)


class TestSparseObservationNoGo(unittest.TestCase):
    def test_n2_exact_probability(self):
        for p in (Fraction(0),Fraction(1,10),Fraction(1,2),Fraction(9,10),Fraction(1)):
            mu,var=isolation_moments(2,p)
            # Either zero or exactly two isolated: P[X=2]=1-p.
            self.assertEqual(mu,2*(1-p))
            self.assertEqual(var,4*p*(1-p))

    def test_n3_explicit_all_eight_graphs(self):
        edges=list(combinations(range(3),2))
        p=Fraction(2,5)
        total_mu=total_sq=Fraction(0)
        for mask in range(8):
            E={edges[i] for i in range(3) if mask>>i & 1}
            mass=p**len(E)*(1-p)**(3-len(E))
            count=len(isolated_vertices(3,E))
            total_mu+=mass*count
            total_sq+=mass*count*count
        mu,var=isolation_moments(3,p)
        self.assertEqual(mu,total_mu)
        self.assertEqual(var,total_sq-total_mu*total_mu)

    def test_first_second_moments_exact_bounds(self):
        self.assertEqual(isolation_moments(5,Fraction(0)),(Fraction(5),Fraction(0)))
        self.assertEqual(isolation_moments(5,Fraction(1)),(Fraction(0),Fraction(0)))
        for n in (5,20,100):
            for p in (Fraction(1,100),Fraction(1,10),Fraction(1,2)):
                b=isolation_lower_bound(n,p)
                self.assertTrue(0<=b<=1)

    def test_sparsity_obstruction_high_probability_bound(self):
        self.assertGreater(isolation_lower_bound(200,Fraction(1,100)),Fraction(9,10))
        self.assertGreater(isolation_lower_bound(500,Fraction(1,100)),Fraction(1,2))
        self.assertLess(isolation_lower_bound(500,Fraction(3,100)),Fraction(1,10))

    def test_seeded_isolation_observation(self):
        n=200;p=Fraction(1,100)
        isolation_trials=0
        for seed in range(20):
            edges=sample_er_edges(n,p,76123+seed)
            if isolated_vertices(n,edges):
                isolation_trials+=1
        self.assertGreaterEqual(isolation_trials,18)

    def test_input_checks(self):
        with self.assertRaises(ValueError):isolation_moments(4,0.5)
        with self.assertRaises(ValueError):isolation_moments(1,Fraction(1,3))
        with self.assertRaises(ValueError):isolated_vertices(5,{(0,5)})

if __name__=='__main__':unittest.main(verbosity=2)
