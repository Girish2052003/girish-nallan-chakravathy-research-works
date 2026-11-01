"""Complete small-group and high-degree controls for public symmetric transport."""
from itertools import permutations
from random import Random
import unittest
from ng_q14_nonabelian_transport import (
    edge_from_hidden, identity, inverse, multiply, recover_public_vertices)
from ng_q15_symmetric_transport import (
    simultaneous_permutation_conjugator,recover_twisted_symmetric_vertices)

class TestPolynomialSymmetricRecovery(unittest.TestCase):
    def test_all_S3_pairs_conjugacy_decision(self):
        G=list(permutations(range(3)))
        for a in G:
            for b in G:
                t=simultaneous_permutation_conjugator(3,(a,),(b,))
                brute=[p for p in G if multiply(multiply(inverse(p),a),p)==b]
                self.assertEqual(t is not None,bool(brute))
                if t is not None:self.assertIn(t,brute)

    def test_all_S3_two_tuple_samples(self):
        G=list(permutations(range(3)))
        r=Random(10014)
        for _ in range(300):
            A=(r.choice(G),r.choice(G));B=(r.choice(G),r.choice(G))
            t=simultaneous_permutation_conjugator(3,A,B)
            brute=[p for p in G if all(multiply(multiply(inverse(p),a),p)==b
                                     for a,b in zip(A,B))]
            self.assertEqual(t is not None,bool(brute))
            if t is not None:self.assertIn(t,brute)

    def test_nontransitive_actions_and_empty_tuple(self):
        self.assertEqual(simultaneous_permutation_conjugator(9,(),()),identity(9))
        A=((1,0,2,4,3,5,7,6,8),)
        B=((0,2,1,3,5,4,8,7,6),)
        t=simultaneous_permutation_conjugator(9,A,B)
        self.assertIsNotNone(t)
        self.assertEqual(multiply(multiply(inverse(t),A[0]),t),B[0])
        A=((1,2,0,3,4,5),)
        B=((1,0,2,3,4,5),)
        self.assertIsNone(simultaneous_permutation_conjugator(6,A,B))

    def test_exact_solver_agreement_on_random_S3_S4_graphs(self):
        rng=Random(271828)
        for k in (3,4):
            G=list(permutations(range(k)))
            for n in (3,5,8):
                for j in range(20):
                    x=tuple(rng.choice(G) for _ in range(n))
                    spec=[(u,u+1,rng.choice(G)) for u in range(n-1)]
                    spec.extend((u,v,rng.choice(G)) for u in range(n)
                                for v in range(u+2,n) if rng.random()<0.5)
                    E=[edge_from_hidden(u,v,h,x) for u,v,h in spec]
                    old=recover_public_vertices(n,k,E)
                    fast=recover_twisted_symmetric_vertices(n,k,E)
                    self.assertEqual(fast['status'],old['status'])
                    self.assertEqual(fast['status'],'satisfiable')
                    self.assertTrue(all(multiply(multiply(inverse(fast['witness'][u]),h),
                                                      fast['witness'][v])==b for u,v,h,b in E))

    def test_large_symmetric_group_degree_100(self):
        rng=Random(12713)
        for k in (8,16,40,100):
            n=12
            x=tuple(tuple(rng.sample(range(k),k)) for _ in range(n))
            spec=[(u,u+1,tuple(rng.sample(range(k),k))) for u in range(n-1)]
            spec.extend((u,v,tuple(rng.sample(range(k),k))) for u in range(n)
                        for v in range(u+2,n) if rng.random()<0.2)
            E=[edge_from_hidden(u,v,h,x) for u,v,h in spec]
            out=recover_twisted_symmetric_vertices(n,k,E)
            self.assertEqual(out['status'],'satisfiable')
            self.assertEqual(out['witness'],x)

    def test_inconsistent_cycle_conjugacy(self):
        e=identity(3);a=(1,0,2);b=(1,2,0)
        edges=[(0,1,e,e),(1,2,e,e),(0,2,a,b)]
        self.assertEqual(recover_twisted_symmetric_vertices(3,3,edges)['status'],'unsatisfiable')

    def test_disconnected_and_tree(self):
        e=identity(4); a=(1,2,3,0)
        E=[(0,1,e,a),(2,3,e,a)]
        out=recover_twisted_symmetric_vertices(5,4,E)
        self.assertEqual(out['status'],'satisfiable')
        self.assertEqual(out['components'],3)
        self.assertTrue(all(multiply(multiply(inverse(out['witness'][u]),h),out['witness'][v])==b
                            for u,v,h,b in E))

    def test_invalid_tuples_rejected(self):
        with self.assertRaises(ValueError):simultaneous_permutation_conjugator(4,[identity(4)],[])
        with self.assertRaises(ValueError):simultaneous_permutation_conjugator(4,[(0,0,1,2)],[(0,1,2,3)])

if __name__=='__main__':unittest.main(verbosity=2)
