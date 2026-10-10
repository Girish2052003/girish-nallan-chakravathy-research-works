#!/usr/bin/env python3
"""Round 8: public-only global witness recovery on bounded-treewidth ternary CSPs.

Theorem: for public factor scopes and explicit public relation tables,
variable elimination takes poly(input_size)*3^(w+1) time at induced width w.
It uses no hidden NCSG directions, trapdoor, or private planted witness.
This does NOT break an unspecified general/global NCSG KEM or prove IND-CCA.
"""
from itertools import product
import random
import unittest

P=3

def primal_order(n,factors):
    graph={i:set() for i in range(n)}
    for scope,allowed in factors:
        assert len(set(scope))==len(scope)
        assert all(0<=i<n for i in scope)
        assert all(len(a)==len(scope) and all(0<=x<P for x in a) for a in allowed)
        for i in scope: graph[i].update(set(scope)-{i})
    active=set(range(n));order=[];width=0
    while active:
        def score(v):
            nbr=sorted(graph[v]&active)
            missing=sum(y not in graph[x] for i,x in enumerate(nbr) for y in nbr[i+1:])
            return (missing,len(nbr),v)
        v=min(active,key=score)
        nbr=graph[v]&active
        width=max(width,len(nbr))
        for x in nbr:graph[x].update(nbr-{x})
        active.remove(v)
        order.append(v)
    return order,width

def public_witness(n,factors):
    """Exact bucket elimination and backwards reconstruction, no secret input."""
    original=[(tuple(s),set(a)) for s,a in factors]
    order,width=primal_order(n,original)
    # A false zero-arity or ordinary empty relation is an immediate
    # contradiction; leaving it in a variable-free bucket would be unsound.
    if any(not allowed for _,allowed in original):
        return None,width
    work=list(original);back=[]
    for v in order:
        bucket=[(s,a) for s,a in work if v in s]
        work=[(s,a) for s,a in work if v not in s]
        rem=tuple(sorted(set().union(*(set(s) for s,_ in bucket))-{v})) if bucket else ()
        saved={}
        for row in product(range(P),repeat=len(rem)):
            env=dict(zip(rem,row))
            for z in range(P):
                env[v]=z
                if all(tuple(env[j] for j in s) in a for s,a in bucket):
                    saved[row]=z
                    break
        if not saved:return None,width
        work.append((rem,set(saved)))
        back.append((v,rem,saved))
    assignment={}
    for v,rem,saved in reversed(back):
        assignment[v]=saved[tuple(assignment[j] for j in rem)]
    result=tuple(assignment[j] for j in range(n))
    assert all(tuple(result[j] for j in s) in a for s,a in original)
    return result,width

def rank3(rows):
    a=[list(row) for row in rows]
    if not a:return 0
    k=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(k,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[k],a[pivot]=a[pivot],a[k]
        inv=pow(a[k][j],-1,P)
        a[k]=[z*inv%P for z in a[k]]
        for i in range(len(a)):
            if i!=k and a[i][j]:
                h=a[i][j]
                a[i]=[(z-h*w)%P for z,w in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k

def invertible(n,rng):
    while True:
        a=[[rng.randrange(P) for _ in range(n)] for _ in range(n)]
        if rank3(a)==n:return a

def source_style_public_table(k,d,seed):
    """Generator-only hidden A/B/a/Q; attacker is given only the output table."""
    rng=random.Random(seed);r=k-d
    A=invertible(r,rng);B=invertible(k,rng)
    direction=tuple(rng.randrange(P) for _ in range(d))
    while not any(direction):
        direction=tuple(rng.randrange(P) for _ in range(d))
    Q={z:tuple(rng.randrange(P) for _ in range(r))
       for z in product(range(P),repeat=d)}
    mat=lambda M,v:tuple(sum(x*y for x,y in zip(row,v))%P for row in M)
    F={}
    for x in product(range(P),repeat=k):
        zall=mat(B,x);z=zall[r:]
        za=tuple((p+q)%P for p,q in zip(z,direction))
        left=mat(A,zall[:r])
        F[x]=tuple((left[i]+Q[za][i]-Q[z][i])%P for i in range(r))
    return F

def public_factor(F,scope,target):
    return tuple(scope),{x for x,y in F.items() if y==target}

class Round8Tests(unittest.TestCase):
    def test_contradictory_public_targets(self):
        w,width=public_witness(1,[((0,),{(0,)}),((0,),{(1,)})])
        self.assertIsNone(w)
        self.assertEqual(width,0)

    def test_zero_arity_contradictions_and_empty_instances(self):
        self.assertEqual(public_witness(0,[]),((),0))
        self.assertEqual(public_witness(0,[((),{()})]),((),0))
        self.assertEqual(public_witness(0,[((),set())]),(None,0))
        self.assertEqual(public_witness(2,[((),set()),((0,),{(0,)})])[0],None)

    def test_random_csp_exact_against_exhaustive(self):
        rng=random.Random(20261010)
        for n in range(1,7):
            for _ in range(18):
                factors=[]
                for j in range(5):
                    k=rng.randint(1,min(3,n))
                    s=tuple(sorted(rng.sample(range(n),k)))
                    allowed={a for a in product(range(P),repeat=k)
                             if rng.random()<0.55}
                    factors.append((s,allowed))
                expected=next((x for x in product(range(P),repeat=n)
                      if all(tuple(x[i] for i in s) in a for s,a in factors)),None)
                got,_=public_witness(n,factors)
                self.assertEqual(got is None,expected is None)

    def test_public_witness_from_overlapping_R1_R2_R3_factors(self):
        for label,k,d in (('SGD-R1',5,3),('SGD-R2',7,4),('SGD-R3',9,5)):
            left=source_style_public_table(k,d,1000+k)
            right=source_style_public_table(k,d,2000+k)
            n=2*k-1
            planted=tuple(random.Random(3000+k+j).randrange(P) for j in range(n))
            a=tuple(range(k))
            b=tuple(range(k-1,n))
            t1=left[tuple(planted[j] for j in a)]
            t2=right[tuple(planted[j] for j in b)]
            f=[public_factor(left,a,t1),public_factor(right,b,t2)]
            witness,width=public_witness(n,f)
            self.assertIsNotNone(witness)
            self.assertEqual(left[tuple(witness[j] for j in a)],t1)
            self.assertEqual(right[tuple(witness[j] for j in b)],t2)
            self.assertLessEqual(width,k-1)
            print('Round8 public overlapping-factor witness',label,
                  'n',n,'width',width,'recovered',witness is not None)

    def test_disjoint_factor_product(self):
        w,width=public_witness(6,[((0,1),{(0,1)}),((2,3),{(1,2)}),((4,5),{(2,0)})])
        self.assertEqual(w,(0,1,1,2,2,0))
        self.assertEqual(width,1)

if __name__=='__main__':unittest.main(verbosity=2)
