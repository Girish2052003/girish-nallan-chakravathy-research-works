"""Independent full-domain oracle plus high-width, shift-rank-deficient fixtures."""
from itertools import combinations, product
import random
import unittest
from public_global_quotient_witness_recovery import PublicQuotientSystem
from public_global_shift_witness_recovery import PublicShiftSystem


def dense_edge_fixture(q):
    # Variables: z (index 0), vertices 1..q. Each local scope is (z,i,j).
    # One non-linear f_ij=xi+xj+z^2, all other f_ij=xi+xj.
    # Each factor is a source-form NCSG function: uL=xi+xj,
    # uR=(z,xj), a=(0,1), Q=b*z^2*xj, A=1, B invertible.
    factors=[]
    for idx,(i,j) in enumerate(combinations(range(1,q+1),2)):
        b=int(idx==0)
        table={(z,x,y): ((x+y+b*z*z)%3,) for z,x,y in product(range(3),repeat=3)}
        factors.append(((0,i,j),table))
    return q+1,factors


class QuotientTests(unittest.TestCase):
    def test_rank_deficient_but_recoverable(self):
        for q in (4,5,8):
            n,factors=dense_edge_fixture(q)
            a=PublicQuotientSystem(n,factors)
            self.assertEqual((a.shift_dimension,a.quotient_dimension),(q,1))
            self.assertEqual(a.increment_rank,q)
            self.assertLess(a.increment_rank,a.output_dimension)
            # Witness x=(1,0,...,0) yields one hot edge target.
            target=[(int(i==0),) for i in range(len(factors))]
            self.assertEqual(PublicShiftSystem(n,factors).solve(target).status,"inconclusive")
            result=a.solve(target)
            self.assertEqual(result.status,"recovered")
            self.assertEqual(a._evaluate(result.witness),tuple(t[0] for t in target))
            self.assertLessEqual(result.cosets_examined,3)
            print("q",q,"primal_width",q,"rank",a.increment_rank,
                  "output_dim",a.output_dimension,"cosets",result.cosets_examined)

    def test_random_small_factors_exactly_match_bruteforce(self):
        rng=random.Random(20261031)
        for n in (1,2,3,4):
            for _ in range(12):
                factors=[]
                for _ in range(2):
                    scope=tuple(rng.sample(range(n),min(2,n)))
                    table={v:(rng.randrange(3),) for v in product(range(3),repeat=len(scope))}
                    factors.append((scope,table))
                system=PublicQuotientSystem(n,factors)
                ground={system._evaluate(x) for x in product(range(3),repeat=n)}
                for t in product(range(3),repeat=2):
                    outcome=system.solve([(t[0],),(t[1],)])
                    self.assertEqual(outcome.status=="recovered",t in ground)
                    exact=sum(system._evaluate(x)==t for x in product(range(3),repeat=n))
                    self.assertEqual(system.count_solutions([(t[0],),(t[1],)]),exact)
                    if outcome.witness is not None:
                        self.assertEqual(system._evaluate(outcome.witness),t)

    def test_no_factor_and_constant_unsat(self):
        self.assertEqual(PublicQuotientSystem(3,[]).solve([]).witness,(0,0,0))
        system=PublicQuotientSystem(0,[((),{(): (2,)})])
        self.assertEqual(system.solve([(1,)]).status,"unsatisfiable")
        self.assertEqual(system.solve([(2,)]).status,"recovered")


if __name__ == '__main__':
    unittest.main(verbosity=2)
