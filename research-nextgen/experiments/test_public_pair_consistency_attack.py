"""Public-only pair projection filtering: exhaustive and planted-source checks."""
from itertools import combinations, product
from random import Random
import unittest
from public_pair_consistency_attack import solve_pair_consistency
from random_source_shift_codimension_probe import sample


class PairConsistencyTests(unittest.TestCase):
    def test_constructed_consistent_and_contradictory(self):
        for n in (3,4):
            factors=[]
            for scope in combinations(range(n),3):
                table={x:(sum(x)%3,) for x in product(range(3),repeat=3)}
                factors.append((scope,table))
            target=[(0,)]*len(factors)
            result=solve_pair_consistency(n,factors,target)
            if result.witness is not None:
                self.assertTrue(all(table[tuple(result.witness[j] for j in scope)]==(0,)
                                    for scope,table in factors))
        contradictory=[((0,1,2),{x:(sum(x)%3,) for x in product(range(3),repeat=3)})]
        contradictory.append(((0,1,2),{x:(sum(x)%3,) for x in product(range(3),repeat=3)}))
        self.assertEqual(solve_pair_consistency(3,contradictory,[(0,),(1,)]).status,'inconclusive')

    def test_random_planted_small_instances_never_false_positive(self):
        for n in (4,5,6):
            for j in range(20):
                m=min(n+2, len(list(combinations(range(n),3))))
                seed=20261112+n*100+j
                system=sample(n,m,seed)
                rng=Random(seed+501)
                secret=tuple(rng.randrange(3) for _ in range(n))
                targets=[table[tuple(secret[k] for k in scope)] for scope,table in system.factors]
                res=solve_pair_consistency(n,system.factors,targets)
                self.assertIn(res.status,('recovered','inconclusive'))
                if res.witness is not None:
                    self.assertEqual(system._evaluate(res.witness), system._evaluate(secret))

    def test_dense_independent_random_source_recovery(self):
        for n in (5,6,7,8,9):
            m=len(list(combinations(range(n),3)))
            for j in range(15):
                seed=20261110+1000*n+100*m+j
                system=sample(n,m,seed)
                rng=Random(seed+123456)
                secret=tuple(rng.randrange(3) for _ in range(n))
                targets=[table[tuple(secret[k] for k in scope)] for scope,table in system.factors]
                res=solve_pair_consistency(n,system.factors,targets)
                if n>=6:
                    self.assertEqual(res.status,'recovered')
                if res.witness is not None:
                    self.assertEqual(system._evaluate(res.witness), system._evaluate(secret))

    def test_malformed_input_rejected(self):
        table={x:(sum(x)%3,) for x in product(range(3),repeat=3)}
        for factors,targets in [([((0,1,2),table)],[]),
                                ([((0,0,1),table)],[(0,)]),
                                ([((0,1,2),{(0,0,0):(0,)})],[(0,)])]:
            with self.assertRaises(ValueError):
                solve_pair_consistency(3,factors,targets)

if __name__=='__main__':unittest.main(verbosity=2)
