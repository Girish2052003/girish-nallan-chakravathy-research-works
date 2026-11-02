"""Independent test controls for public matrix-intertwiner graph reconstruction."""
from itertools import product
from random import Random
from fractions import Fraction
import unittest
from ng_q19_matrix_transport import (eye,mul,inv,nullspace,random_gl,
    conjugator,simultaneous_space,edge_from_secret,recover_graph,rank_and_rref)

class TestMatrixTransport(unittest.TestCase):
    def test_matrix_noncommutativity_and_inverse(self):
        p=7;a=((1,1),(0,1));b=((1,0),(1,1))
        self.assertNotEqual(mul(a,b,p),mul(b,a,p))
        self.assertEqual(mul(a,inv(a,p),p),eye(2))
        with self.assertRaises(ValueError):inv(((1,2),(2,4)),7)

    def test_nullspace_all_binary_two_dimensional_equations(self):
        # Independent explicit row dot-product verification for all 2^4 rows.
        p=2;d=4
        rows=[(1,1,0,1),(1,0,1,1),(0,0,1,1)]
        b=nullspace(rows,p,d)
        produced={tuple(sum(c*v[j] for c,v in zip(coeff,b))%p for j in range(d))
                  for coeff in product(range(p),repeat=len(b))}
        direct={vec for vec in product(range(p),repeat=d)
                if all(sum(a*v for a,v in zip(row,vec))%p==0 for row in rows)}
        self.assertEqual(produced,direct)

    def test_all_gl2_f2_tuple_pair_decisions_independent_brute(self):
        p=2;k=2
        matrices=[((a,b),(c,d)) for a,b,c,d in product(range(p),repeat=4)]
        group=[]
        for m in matrices:
            try:inv(m,p);group.append(m)
            except ValueError:pass
        self.assertEqual(len(group),6)
        for A in group:
            for B in group:
                valid=[T for T in group if mul(A,T,p)==mul(T,B,p)]
                candidate=conjugator((A,),(B,),p,k,32,seed=17)
                if candidate['status']=='witness':self.assertIn(candidate['T'],valid)
                if candidate['status']=='proven_unsatisfiable':self.assertEqual(valid,[])
                if valid:
                    self.assertGreaterEqual(len(simultaneous_space((A,),(B,),p)),1)

    def test_exact_invertible_count_and_schwartz_zippel_lower_bound(self):
        p=5;k=2
        all_m=[((a,b),(c,d)) for a,b,c,d in product(range(p),repeat=4)]
        invertible=sum(1 for M in all_m if (M[0][0]*M[1][1]-M[0][1]*M[1][0])%p)
        self.assertEqual(invertible,(p*p-1)*(p*p-p))
        actual=Fraction(invertible,p**(k*k))
        self.assertGreaterEqual(actual,1-Fraction(k,p))
        self.assertEqual(actual,Fraction(96,125))

    def test_plant_simultaneous_intertwiner(self):
        r=Random(106)
        for k,p in [(2,5),(3,11),(4,17),(6,31)]:
            T=random_gl(k,p,r);Tin=inv(T,p)
            A=tuple(random_gl(k,p,r) for _ in range(4))
            B=tuple(mul(mul(Tin,a,p),T,p) for a in A)
            ans=conjugator(A,B,p,k,48,seed=k*101+p)
            self.assertEqual(ans['status'],'witness')
            self.assertTrue(all(mul(a,ans['T'],p)==mul(ans['T'],b,p) for a,b in zip(A,B)))

    def test_singular_intertwiners_are_inconclusive_not_unsat(self):
        p=11;e=eye(2);j=((1,1),(0,1))
        ans=conjugator((e,),(j,),p,2,24,seed=22)
        self.assertEqual(ans['status'],'inconclusive')
        self.assertGreater(ans['space_dimension'],0)
        self.assertLess(ans['failure_upper_if_planted'],1)
        # Public certificate cannot assert no solution merely from randomness.
        self.assertIsNone(ans['T'])

    def test_zero_kernel_proves_unsatisfiable(self):
        p=5;e=eye(2);two=((2,0),(0,2))
        ans=conjugator((e,),(two,),p,2,4,seed=3)
        self.assertEqual(ans['status'],'proven_unsatisfiable')
        self.assertEqual(ans['space_dimension'],0)

    def test_connected_graph_reconstruction(self):
        r=Random(1091)
        for k,p,n in [(2,5,4),(3,11,7),(5,17,9),(7,101,8)]:
            secret=tuple(random_gl(k,p,r) for _ in range(n))
            spec=[(i,i+1,random_gl(k,p,r)) for i in range(n-1)]
            spec += [(i,j,random_gl(k,p,r)) for i in range(n) for j in range(i+2,n)
                     if r.random()<0.6]
            public=[edge_from_secret(i,j,h,secret,p) for i,j,h in spec]
            ans=recover_graph(n,k,p,public,trials=64,seed=1823)
            self.assertEqual(ans['status'],'witness')
            x=ans['witness']
            self.assertTrue(all(mul(mul(inv(x[i],p),h,p),x[j],p)==b for i,j,h,b in public))

    def test_disconnected_graph_and_isolated_vertex(self):
        p=11;k=2;n=5;e=eye(k)
        spec=[(0,1,e,e),(2,3,e,e)]
        ans=recover_graph(n,k,p,spec)
        self.assertEqual(ans['status'],'witness')
        self.assertEqual(ans['components'],3)
        self.assertEqual(len(ans['witness']),5)

    def test_inconsistent_graph_zero_kernel(self):
        p=5;k=2;e=eye(k);two=((2,0),(0,2))
        public=[(0,1,e,e),(1,2,e,e),(0,2,e,two)]
        result=recover_graph(3,k,p,public)
        self.assertEqual(result['status'],'proven_unsatisfiable')

    def test_empty_group_conjugacy(self):
        self.assertEqual(conjugator((),(),11,3)['T'],eye(3))
        self.assertEqual(recover_graph(1,3,11,[])['witness'],(eye(3),))

    def test_bad_field_and_invalid_edge(self):
        with self.assertRaises(ValueError):recover_graph(3,2,9,[])
        with self.assertRaises(ValueError):recover_graph(3,2,7,[(0,3,eye(2),eye(2))])
        with self.assertRaises(ValueError):recover_graph(3,2,7,[(0,1,eye(2),((1,0),(0,0)))])
        with self.assertRaises(ValueError):conjugator((eye(2),),(),7,2)

if __name__=='__main__':unittest.main(verbosity=2)
