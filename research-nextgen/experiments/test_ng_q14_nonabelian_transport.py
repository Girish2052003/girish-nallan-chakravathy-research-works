"""Independent exact checks of NG-Q14 using full assignment enumeration at small sizes."""
from itertools import permutations,product
from random import Random
import unittest

from ng_q14_nonabelian_transport import (
    identity,multiply,inverse,edge_from_hidden,
    recover_public_vertices,cycle_conjugacy_constraints,
    simultaneous_centralizer_size)


def brute_solutions(n,k,edges):
    group=list(permutations(range(k)))
    return [xx for xx in product(group,repeat=n) if all(
        multiply(multiply(inverse(xx[u]),h),xx[v]) == b
        for u,v,h,b in edges)]


class TestNonabelianTransport(unittest.TestCase):
    def test_noncommutative_s3(self):
        a=(1,0,2); c=(1,2,0)
        self.assertNotEqual(multiply(a,c),multiply(c,a))
        self.assertEqual(simultaneous_centralizer_size(3,(a,c)),1)
        self.assertEqual(simultaneous_centralizer_size(3,(a,)),2)
        self.assertEqual(simultaneous_centralizer_size(3,()),6)

    def test_flat_transport_has_exact_global_gauge(self):
        r=Random(9182)
        e=identity(3)
        for n in (2,3,4):
            xx=tuple(r.choice(list(permutations(range(3)))) for _ in range(n))
            E=[edge_from_hidden(j,j+1,e,xx) for j in range(n-1)]
            E += [edge_from_hidden(0,n-1,e,xx)] if n>=3 else []
            rec=recover_public_vertices(n,3,E)
            self.assertEqual(rec['status'],'satisfiable')
            self.assertEqual(rec['solution_count'],6)
            self.assertEqual(len(brute_solutions(n,3,E)),6)

    def test_noncommuting_chords_force_unique_root(self):
        e=identity(3); a=(1,0,2); c=(1,2,0)
        xx=((1,2,0),(2,1,0),(1,0,2),(0,2,1))
        spec=[(0,1,e),(0,2,e),(0,3,e),(1,2,a),(2,3,c)]
        E=[edge_from_hidden(u,v,h,xx) for u,v,h in spec]
        rec=recover_public_vertices(4,3,E)
        self.assertEqual(rec['status'],'satisfiable')
        self.assertEqual(rec['solution_count'],1)
        self.assertEqual(rec['witness'],xx)
        self.assertEqual(brute_solutions(4,3,E),[xx])

    def test_one_chord_leaves_two_roots(self):
        e=identity(3); a=(1,0,2)
        xx=(e,(1,2,0),(2,1,0))
        E=[edge_from_hidden(u,v,h,xx) for u,v,h in
           [(0,1,e),(0,2,e),(1,2,a)]]
        r=recover_public_vertices(3,3,E)
        self.assertEqual(r['solution_count'],2)
        self.assertEqual(len(brute_solutions(3,3,E)),2)

    def test_inconsistent_cycle_detected(self):
        e=identity(3); a=(1,0,2); c=(1,2,0)
        E=[(0,1,e,e),(1,2,e,e),(0,2,a,c)]
        r=recover_public_vertices(3,3,E)
        self.assertEqual(r['status'],'unsatisfiable')
        self.assertEqual(r['solution_count'],0)
        self.assertEqual(brute_solutions(3,3,E),[])

    def test_noisy_flat_label_rejected(self):
        e=identity(3); a=(1,0,2)
        E=[(0,1,e,e),(1,2,e,e),(0,2,e,a)]
        self.assertEqual(recover_public_vertices(3,3,E)['status'],'unsatisfiable')

    def test_disconnected_components_gauge_product(self):
        e=identity(3); c=(1,2,0)
        E=[(0,1,e,c),(2,3,e,c)]
        r=recover_public_vertices(4,3,E)
        self.assertEqual(r['component_root_counts'],(6,6))
        self.assertEqual(r['solution_count'],36)
        self.assertEqual(len(brute_solutions(4,3,E)),36)

    def test_random_planted_s3_vs_bruteforce(self):
        rng=Random(33111); group=list(permutations(range(3)))
        for n in (3,4):
            for j in range(20):
                xx=tuple(rng.choice(group) for _ in range(n))
                spec=[(u,v,rng.choice(group)) for u in range(n)
                      for v in range(u+1,n) if rng.random()<0.7]
                E=[edge_from_hidden(u,v,h,xx) for u,v,h in spec]
                r=recover_public_vertices(n,3,E)
                brute=brute_solutions(n,3,E)
                self.assertEqual(r['status'],'satisfiable')
                self.assertEqual(r['solution_count'],len(brute))
                self.assertIn(r['witness'],brute)

    def test_random_s4_plant_verified(self):
        rng=Random(39813);group=list(permutations(range(4)))
        for n in (3,5,9):
            xx=tuple(rng.choice(group) for _ in range(n))
            spec=[(u,u+1,rng.choice(group)) for u in range(n-1)]
            spec.extend((0,v,rng.choice(group)) for v in range(2,n))
            E=[edge_from_hidden(u,v,h,xx) for u,v,h in spec]
            r=recover_public_vertices(n,4,E)
            self.assertEqual(r['status'],'satisfiable')
            self.assertTrue(all(multiply(multiply(inverse(r['witness'][u]),h),r['witness'][v])==b
                                for u,v,h,b in E))

    def test_invalid_edge_rejected(self):
        e=identity(3)
        with self.assertRaises(ValueError): recover_public_vertices(2,3,[(0,1,e,(0,0,1))])
        with self.assertRaises(ValueError): recover_public_vertices(2,3,[(0,2,e,e)])
        with self.assertRaises(ValueError): recover_public_vertices(2,3,[(0,0,e,e)])

if __name__=='__main__': unittest.main(verbosity=2)
