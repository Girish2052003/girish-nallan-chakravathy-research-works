"""Public-only 2-coordinate projection consistency for explicit ternary factors.

Works for factors of arbitrary arity >=2 with tuple outputs. Reveals no
original generator secret; returns recovered only after verifying all factors.
If constraints are consistent but pair projections fail to imply a full
witness, reports 'inconclusive'. No unsatisfiability certificate is attempted.
"""
from itertools import combinations,product
from dataclasses import dataclass


@dataclass(frozen=True)
class PairResult:
    status: str
    witness: tuple | None
    iterations: int
    removed_tuples: int
    pair_domain_counts: tuple


def solve_pair_consistency(n, factors, targets):
    if len(factors)!=len(targets): raise ValueError('targets length')
    relations=[]
    for (scope,table),target in zip(factors, targets):
        scope=tuple(scope);target=tuple(target)
        if len(scope)<2 or len(set(scope))!=len(scope) or any(j<0 or j>=n for j in scope):
            raise ValueError('invalid scope')
        if len(table)!=3**len(scope):raise ValueError('incomplete table')
        rel={x for x,y in table.items() if tuple(y)==target}
        relations.append([scope,rel])
    pairs=set()
    for scope,_ in relations:
        pairs.update(combinations(sorted(scope),2))
    all_pairs=list(sorted(pairs))
    domains={p:set(product(range(3),repeat=2)) for p in all_pairs}
    removed=0; iterations=0
    while True:
        iterations+=1
        changed=False
        for scope, rel in relations:
            loc={j:i for i,j in enumerate(scope)}
            allowed=set(x for x in rel if all(
                (x[loc[a]],x[loc[b]]) in domains[(a,b)]
                for a,b in combinations(sorted(scope),2)))
            if allowed != rel:
                removed+=len(rel)-len(allowed)
                rel.clear();rel.update(allowed);changed=True
        for p in all_pairs:
            possible=domains[p]
            for scope,rel in relations:
                if p[0] in scope and p[1] in scope:
                    ia,ib=scope.index(p[0]),scope.index(p[1])
                    possible=possible.intersection((x[ia],x[ib]) for x in rel)
            if possible != domains[p]:
                domains[p]=possible;changed=True
        if not changed:break
    if any(not rel for _,rel in relations) or any(not d for d in domains.values()):
        return PairResult('inconclusive',None,iterations,removed,tuple(len(x) for x in domains.values()))
    unary=[set(range(3)) for _ in range(n)]
    for (a,b),values in domains.items():
        unary[a]&={x for x,y in values}
        unary[b]&={y for x,y in values}
    if any(not x for x in unary):
        return PairResult('inconclusive',None,iterations,removed,tuple(len(x) for x in domains.values()))
    if not all(len(x)==1 for x in unary):
        return PairResult('inconclusive',None,iterations,removed,tuple(len(x) for x in domains.values()))
    witness=tuple(next(iter(x)) for x in unary)
    if any(tuple(table[tuple(witness[j] for j in scope)])!=tuple(target)
           for (scope,table),target in zip(factors,targets)):
        return PairResult('inconclusive',None,iterations,removed,tuple(len(x) for x in domains.values()))
    return PairResult('recovered',witness,iterations,removed,tuple(len(x) for x in domains.values()))
