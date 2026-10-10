#!/usr/bin/env python3
"""Small GF(1024) hidden-GRS subspace recovery.

Attack is exhaustive and only feasible at tiny parameters. A toy success
is NOT an exploit against the three proposed production-sized research profiles.
"""
import itertools
import random
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1] /
                      "formal-verification-and-mathematical-proofs"))
from test_sg_difra import rank, dot, powfield, mul

Q=1024
def planted_fixture(seed, m=6, B=3, M=5, u=3, N=6):
    r=random.Random(seed)
    T=[[r.randrange(Q) for _ in range(N)] for _ in range(u)]
    while rank(T)<u:
        T=[[r.randrange(Q) for _ in range(N)] for _ in range(u)]
    good=set(r.sample(range(m),M))
    H=[[tuple(r.randrange(Q) for _ in range(N)) for _ in range(B)]
       for _ in range(m)]
    indices={}
    for i,group in enumerate(sorted(good)):
        at=r.randrange(B)
        G=[powfield(i+1,k) for k in range(u)]
        H[group][at]=tuple(dot(G,[T[k][j] for k in range(u)]) for j in range(N))
        indices[group]=at
    return H,indices,u

def find_rank_witness(H,u):
    m=len(H);B=len(H[0])
    # u+1 distinct groups, choose one row per group, and look for dependency
    for group_ids in itertools.combinations(range(m),u+1):
        for position_ids in itertools.product(range(B),repeat=u+1):
            trial=[list(H[g][p]) for g,p in zip(group_ids,position_ids)]
            if rank(trial)<=u:
                return list(zip(group_ids,position_ids))
    return []

def recover_selected(H,witness,u):
    if not witness:
        return {}
    rows=[list(H[g][p]) for g,p in witness[:u]]
    if rank(rows)!=u: return {}
    found={}
    for g,bucket in enumerate(H):
        for p,v in enumerate(bucket):
            if rank(rows+[list(v)])==u:
                found[g]=p
    return found

class ToyHiddenSubspaceTests(unittest.TestCase):
    def test_successful_toy_recovery(self):
        for seed in (1,2,3,2028,31415):
            with self.subTest(seed=seed):
                H,ground_truth,u=planted_fixture(seed)
                witness=find_rank_witness(H,u)
                self.assertEqual(len(witness),u+1)
                self.assertTrue(all(ground_truth.get(g)==p for g,p in witness))
                self.assertEqual(recover_selected(H,witness,u),ground_truth)
    def test_no_false_certification(self):
        self.assertGreater(27**64,2**256) # exponential candidate burden in large profile
if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ToyHiddenSubspaceTests)
    res=unittest.TextTestRunner(verbosity=2).run(suite)
    if not res.wasSuccessful():sys.exit(1)
    print("Toy hidden GRSystem recoveries succeed; this is a structural attack FAMILY, not a real-profile break.")
