"""Fixed-seed public witness attack on independent source-form planted systems.

No secret is passed to the attacker. Trials measure this exact distribution only.
"""
from itertools import combinations,product
from math import comb
from random import Random
from public_pair_consistency_attack import solve_pair_consistency
from random_source_shift_codimension_probe import sample


def run_campaign():
    rows=[]
    for n,trials in ((4,30),(5,30),(6,30),(7,30),(8,30),(9,10),(10,10),(12,10)):
        m=comb(n,3)
        recovered=zero_shift=both=0
        unique=0
        for j in range(trials):
            seed=20261110+1000*n+100*m+j
            public=sample(n,m,seed)
            rng=Random(seed+123456)
            secret=tuple(rng.randrange(3) for _ in range(n))
            targets=[table[tuple(secret[k] for k in scope)] for scope,table in public.factors]
            outcome=solve_pair_consistency(n,public.factors,targets)
            good=outcome.status=='recovered'
            if good:
                assert public._evaluate(outcome.witness)==public._evaluate(secret)
            no=public.shift_dimension==0
            recovered+=good
            zero_shift+=no
            both+=good and no
            if n<=6:
                target=public._evaluate(secret)
                count=sum(public._evaluate(x)==target for x in product(range(3),repeat=n))
                unique+=count==1
        row=(n,m,trials,recovered,zero_shift,both,unique if n<=6 else None)
        rows.append(row)
        print('n m trials recovered no_nonzero_shift both unique_bruteforce',*row)
    return rows


if __name__=='__main__':run_campaign()
