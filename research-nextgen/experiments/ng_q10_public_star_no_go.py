"""NG-Q10 negative control: complete public solver on a 2-anchor star CSP.

Not cryptography. Any field size q and any arbitrary local factor tables,
including fully nonlinear correlated functions. No planted witness required.
"""
from itertools import product


def solve_star(n, q, factors, targets):
    """Return ('satisfiable', verified witness) or ('unsatisfiable', None).

    Every local scope must be (0,1,j) for j in [2,n), and every table must
    be complete over F_q^3 (this is a plain finite alphabet, no field ops).
    All factors are public. Missing leaf factors are allowed: free choices.
    """
    if n < 3 or q < 2 or len(factors) != len(targets):
        raise ValueError('invalid input')
    groups = {j: [] for j in range(2, n)}
    local = tuple(product(range(q), repeat=3))
    for (scope, table), target in zip(factors, targets):
        scope = tuple(scope)
        if len(scope) != 3 or tuple(scope[:2]) != (0,1) or not (2 <= scope[2] < n):
            raise ValueError('not a 2-anchor star scope')
        if len(table) != q**3 or any(x not in table for x in local):
            raise ValueError('incomplete local table')
        groups[scope[2]].append((table, target))
    for a,b in product(range(q), repeat=2):
        witness = [a,b]
        possible = True
        for j in range(2,n):
            choices = [x for x in range(q) if all(table[(a,b,x)] == target
                       for table,target in groups[j])]
            if not choices:
                possible = False
                break
            witness.append(choices[0])
        if not possible:
            continue
        witness = tuple(witness)
        assert all(table[tuple(witness[v] for v in scope)] == target
                   for (scope,table),target in zip(factors,targets))
        return 'satisfiable', witness
    return 'unsatisfiable',None


def brute_star_solutions(n,q,factors,targets):
    return [x for x in product(range(q), repeat=n) if all(
        table[tuple(x[v] for v in scope)]==target
        for (scope,table),target in zip(factors,targets))]


if __name__ == '__main__':
    from ng_q8_recovery import sample_planted
    for n in (8,32,128):
        scopes=[(0,1,2)] + [(0,1,j) for j in range(3,n)]
        s,factors,targets=sample_planted(n,805510+n,scopes=scopes)
        result,w=solve_star(n,3,factors,targets)
        print('n=',n,'factors=',len(factors),'result=',result,
              'witness_verified=',w is not None and all(
                  table[tuple(w[v] for v in scope)]==t
                  for (scope,table),t in zip(factors,targets)))
