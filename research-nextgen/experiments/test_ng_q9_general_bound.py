import unittest
from itertools import product
from fractions import Fraction
from math import prod
from ng_q9_general_bound import gamma_uniform_surjective_map, local_projection_rejection_lower_bound, gaussian_rank_count

def rk(X):
    if not X:return 0
    a=[list(row) for row in X];rank=0
    for j in range(len(a[0])):
        k=next((i for i in range(rank,len(a)) if a[i][j]%3),None)
        if k is None:continue
        a[rank],a[k]=a[k],a[rank]
        f=pow(a[rank][j]%3,-1,3)
        a[rank]=[f*x%3 for x in a[rank]]
        for i in range(len(a)):
            if i!=rank and a[i][j]:
                f=a[i][j];a[i]=[(x-f*y)%3 for x,y in zip(a[i],a[rank])]
        rank+=1
        if rank==len(a):break
    return rank

class GeneralProjectionTest(unittest.TestCase):
 def test_gamma_exact_linear_maps(self):
    for r,d in ((1,1),(1,2),(1,3),(2,1),(2,2),(2,3)):
      k=r+d;s=k-2
      den=num=0
      for flat in product(range(3),repeat=r*k):
        M=[flat[i*k:(i+1)*k] for i in range(r)]
        if rk(M)!=r:continue
        den+=1
        sub=[[row[j] for j in range(2,k)] for row in M]
        # rank of free coordinates, plus first chosen pair coordinate.
        free=[[row[j] for j in range(2,k)] for row in M]
        rankfree=rk(free) if s else 0
        withh=[[row[0]]+list(row[2:]) for row in M]
        if rk(withh)>rankfree:num+=1
      self.assertEqual(Fraction(num,den),gamma_uniform_surjective_map(r,d), (r,d))
 def test_potential_constant_difference_probability(self):
    # Exhaust all ternary Q when d=1,2; check Delta_(1,0,..) Q constant.
    for d in (1,2):
      points=list(product(range(3),repeat=d))
      where={p:i for i,p in enumerate(points)}
      count=0
      for Q in product(range(3),repeat=3**d):
        diffs=[(Q[where[((x[0]+1)%3,)+x[1:]]]-Q[where[x]])%3 for x in points]
        count+=int(len(set(diffs))==1)
      expected=Fraction(1,3**(2*3**(d-1)-1))
      self.assertEqual(Fraction(count,3**(3**d)),expected)
 def test_boundary(self):
    self.assertEqual(gamma_uniform_surjective_map(1,2),Fraction(3,13))
    self.assertEqual(local_projection_rejection_lower_bound(1,2),Fraction(1,1053))
    self.assertEqual(gamma_uniform_surjective_map(2,2),Fraction(37,130))
if __name__=='__main__':unittest.main(verbosity=2)
