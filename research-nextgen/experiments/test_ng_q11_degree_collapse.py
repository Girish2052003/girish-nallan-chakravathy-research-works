import unittest
from random import Random
from itertools import product,combinations
from fractions import Fraction
from ng_q11_degree_collapse import (
 interpolate,algebraic_degree,source_d2_identity,
 random_scalar_false_positive_probability,solve_affine_public)
from ng_q8_recovery import sample_planted,rank_mod3


def d1_factor(rng,r):
    k=r+1
    while True:
        B=[[rng.randrange(3) for _ in range(k)] for _ in range(k)]
        if rank_mod3(B)==k:break
    # A = I_r is already invertible.
    Q=[tuple(rng.randrange(3) for _ in range(r)) for _ in range(3)]
    table={}
    for x in product(range(3),repeat=k):
        u=[sum(B[row][j]*x[j] for j in range(k))%3 for row in range(k)]
        z=u[-1]
        table[x]=tuple((u[j]+Q[(z+1)%3][j]-Q[z][j])%3 for j in range(r))
    return table

class TestDegreeCollapse(unittest.TestCase):
 def test_univariate_tensor_interpolation_identity(self):
    for k in (1,2,3,4):
      for seed in range(8):
        rng=Random(seed+k*100)
        table={x:rng.randrange(3) for x in product(range(3),repeat=k)}
        a=interpolate(table,k)
        for x in table:
          got=sum(c*__import__('math').prod(x[j]**e[j] for j in range(k))
                  for e,c in a.items())%3
          self.assertEqual(got,table[x])
 def test_d1_random_source_affine_for_r1_r2(self):
    for r in (1,2):
      rng=Random(1031+r)
      for _ in range(100):
        T=d1_factor(rng,r)
        for t in range(r):
          single={x:y[t] for x,y in T.items()}
          self.assertLessEqual(algebraic_degree(single,r+1),1)
 def test_any_global_scope_planted_d1_public_recovery(self):
    for n,r in ((6,1),(9,1),(6,2),(8,2)):
      rng=Random(1302+n*10+r)
      k=r+1
      scopes=list(combinations(range(n),k))
      rng.shuffle(scopes)
      factors=[(scope,d1_factor(rng,r)) for scope in scopes[:min(len(scopes),n+5)]]
      secret=tuple(rng.randrange(3) for _ in range(n))
      target=[table[tuple(secret[j] for j in scope)] for scope,table in factors]
      status,recovered=solve_affine_public(n,factors,target)
      self.assertEqual(status,'satisfiable')
      self.assertTrue(all(table[tuple(recovered[j] for j in scope)]==tar
                          for (scope,table),tar in zip(factors,target)))
 def test_linear_system_unsat_and_invalid_nonlinearity(self):
    ident={(x,y):(x,) for x,y in product(range(3),repeat=2)}
    self.assertEqual(solve_affine_public(2,[((0,1),ident),((0,1),ident)],[(0,),(1,)])[0],
                     'unsatisfiable')
    nonlinear={(x,y):(x*y%3,) for x,y in product(range(3),repeat=2)}
    with self.assertRaises(ValueError):
      solve_affine_public(2,[((0,1),nonlinear)],[(0,)])
 def test_d2_full_19683_Q_tables_degree_3_exact_count(self):
    count=0
    for Q in product(range(3),repeat=9):
      degree=algebraic_degree(source_d2_identity(1,Q),3)
      self.assertLessEqual(degree,3)
      count+=degree==3
    self.assertEqual(count,13122)
    self.assertEqual(random_scalar_false_positive_probability(3,3),
                     (Fraction(1,59049),17))
 def test_d2_affine_mask_low_degree(self):
    for j in range(200):
      secret,factors,targets=sample_planted(3,808001+j,scopes=[(0,1,2)])
      table=factors[0][1]
      self.assertLessEqual(algebraic_degree({x:y[0] for x,y in table.items()},3),3)
 def test_d2_reed_muller_degree_distinguishing(self):
    # Distinguisher only: no KEM claim. Random-function false-positive exact by dimension.
    rng=Random(93824)
    passes=0
    for _ in range(3000):
      table={x:rng.randrange(3) for x in product(range(3),repeat=3)}
      passes+=algebraic_degree(table,3)<=3
    self.assertLessEqual(passes,3)

if __name__=='__main__':unittest.main(verbosity=2)
