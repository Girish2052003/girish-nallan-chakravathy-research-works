import unittest
from itertools import product
from random import Random
from ng_q10_public_star_no_go import solve_star, brute_star_solutions
from ng_q8_recovery import sample_planted


class TestPublicStarComplete(unittest.TestCase):
    def test_planted_one_factor_each_leaf(self):
        for n in (4,8,32,128):
            scopes=[(0,1,j) for j in range(2,n)]
            s,factors,targets=sample_planted(n,38100+n,scopes=scopes)
            status,w=solve_star(n,3,factors,targets)
            self.assertEqual(status,'satisfiable')
            self.assertIsNotNone(w)
            self.assertTrue(all(table[tuple(w[v] for v in scope)]==t
                        for (scope,table),t in zip(factors,targets)))

    def test_random_correlated_tables_with_arbitrary_targets(self):
        for n in (3,4,5,6):
            for seed in range(20):
                rng=Random(50000+n*100+seed)
                factors=[];targets=[]
                for j in range(2,n):
                    for rep in range(rng.randrange(1,4)):
                        tab={x:rng.randrange(3) for x in product(range(3),repeat=3)}
                        factors.append(((0,1,j),tab))
                        targets.append((rng.randrange(3),))
                status,w=solve_star(n,3,factors,targets)
                brute=brute_star_solutions(n,3,factors,targets)
                self.assertEqual(status=='satisfiable',bool(brute))
                if w is not None:self.assertIn(w,brute)

    def test_unsatisfiable_contradictory_tables(self):
        table={x:(0,) for x in product(range(3),repeat=3)}
        factors=[((0,1,2),table),((0,1,2),table)]
        self.assertEqual(solve_star(3,3,factors,[(0,),(1,)]),
                         ('unsatisfiable',None))

    def test_different_alphabet_size_and_missing_leaf(self):
        q=4;n=5
        table={x:(sum(x)%q,) for x in product(range(q),repeat=3)}
        factors=[((0,1,2),table)]
        targets=[(2,)]
        status,w=solve_star(n,q,factors,targets)
        self.assertEqual(status,'satisfiable')
        self.assertIn(w,brute_star_solutions(n,q,factors,targets))

    def test_invalid_scope_rejected(self):
        t={x:(0,) for x in product(range(3),repeat=3)}
        with self.assertRaises(ValueError):
            solve_star(5,3,[((0,2,3),t)],[(0,)])

if __name__=='__main__':unittest.main(verbosity=2)
