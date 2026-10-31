"""Independently challenge NG-Q8 exact finite census and public recovery."""
import random
import unittest
from fractions import Fraction
from itertools import combinations, product
from math import comb
from ng_q8_recovery import (
    exact_local_census, independent_pair_failure_probability, rank_mod3,
    sample_planted, public_one_pass_recover, public_failure_bound,
    complete_triples_bound, INDEX)


def direct_f(B, Q, A, x):
    u = [sum(row[j]*x[j] for j in range(3))%3 for row in B]
    z,w=u[1:]
    return (A*u[0] + Q[INDEX[((z+1)%3,w)]] - Q[INDEX[(z,w)]])%3


class TestNGQ8(unittest.TestCase):
    def test_exact_624_case_census(self):
        p,cases=exact_local_census()
        self.assertEqual(p, Fraction(15,52))
        self.assertEqual(cases, {
            (1,'0'):48, (1,'1/3'):36, (2,'2/9'):108,
            (2,'4/9'):108, (3,'8/27'):324})

    def test_all_Q_for_five_independent_rank_types(self):
        rng=random.Random(9248)
        seen={}
        while len(seen)<5:
            B=[[rng.randrange(3) for _ in range(3)] for _ in range(3)]
            if rank_mod3(B)!=3: continue
            u=tuple(row[0] for row in B)
            v=tuple(row[2] for row in B)
            expected,rank=independent_pair_failure_probability(u,v)
            seen.setdefault((rank,str(expected)), (B,expected))
        for B,expected in seen.values():
            number=0
            for Q in product(range(3), repeat=9):
                f0=direct_f(B,Q,1,(0,0,0))
                number+=int(all(direct_f(B,Q,1,(1,0,z))!=f0 for z in range(3)))
            self.assertEqual(Fraction(number,3**9),expected)

    def test_direct_monte_carlo(self):
        rng=random.Random(19411)
        rejected=0
        for _ in range(10000):
            while True:
                B=[[rng.randrange(3) for _ in range(3)] for _ in range(3)]
                if rank_mod3(B)==3:break
            Q=[rng.randrange(3) for _ in range(9)]
            A=rng.choice((1,2))
            f0=direct_f(B,Q,A,(0,0,0))
            rejected+=int(all(direct_f(B,Q,A,(1,0,z))!=f0 for z in range(3)))
        self.assertLess(abs(rejected/10000-15/52),.025)

    def test_one_pass_public_correctness_on_planted(self):
        for n,trials in ((4,30),(6,20),(12,10),(20,4),(30,3)):
            for j in range(trials):
                planted,factors,targets=sample_planted(n,23451+100*n+j)
                status,result=public_one_pass_recover(n,factors,targets)
                self.assertIn(status,('inconclusive','recovered'))
                if status=='recovered':
                    self.assertEqual(result,planted)

    def test_covers_any_hypergraph_pair_codegree(self):
        for n,t in ((8,1),(10,3),(15,4)):
            scopes=[scope for scope in combinations(range(n),3)
                    if any(v<t for v in scope)]
            self.assertEqual(len(scopes),comb(n,3)-comb(n-t,3))
            codegrees=[sum(a in scope and b in scope for scope in scopes)
                       for a,b in combinations(range(n),2)]
            self.assertEqual(min(codegrees),t)
            self.assertLessEqual(public_failure_bound(n,scopes),
                                 min(1,8*comb(n,2)*Fraction(37,52)**t))
        for n in (3,4,8,30):
            self.assertEqual(public_failure_bound(n,list(combinations(range(n),3))),
                             complete_triples_bound(n))

    def test_unconstrained_pair_reports_inconclusive(self):
        n=4
        secret, factors, targets=sample_planted(n,415,scopes=[(0,1,2)])
        self.assertEqual(public_one_pass_recover(n,factors,targets)[0],'inconclusive')

if __name__=='__main__': unittest.main(verbosity=2)
