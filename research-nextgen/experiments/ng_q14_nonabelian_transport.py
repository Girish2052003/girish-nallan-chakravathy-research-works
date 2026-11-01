"""NG-Q14: public recovery for finite nonabelian edge transports.

A directed edge u->v carries PUBLIC H_e and B_e, with B_e = x_u^-1 H_e x_v.
For a connected component the full problem reduces to simultaneous conjugacy of
fundamental cycle gains. The finite S_k implementation enumerates k! elements;
it is NOT polynomial in the succinct permutation degree k.
"""
from collections import deque
from itertools import permutations
from math import factorial


def identity(k):
    return tuple(range(k))


def multiply(p, q):
    """Permutation multiplication p o q (apply q, then p)."""
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p):
    result = [0]*len(p)
    for i,j in enumerate(p):
        result[j] = i
    return tuple(result)


def validate_perm(p,k):
    if len(p)!=k or set(p)!=set(range(k)):
        raise ValueError('invalid finite permutation')


def edge_from_hidden(u,v,h,x):
    """Construct B=x[u]^-1 * h * x[v] for experimental planted labels."""
    return (u,v,h,multiply(multiply(inverse(x[u]),h),x[v]))


def cycle_conjugacy_constraints(n,k,edges):
    """Return component-local fundamental cycle pairs (H_cycle,B_cycle).

    Public paths are built via any BFS forest, preserving orientation inverses.
    Every edge constraint is included, including tree edges (identities).
    """
    if n<1 or not (2<=k<=6):
        raise ValueError('n>=1 and 2<=permutation degree<=6')
    adj = [[] for _ in range(n)]
    for u,v,h,b in edges:
        if not (0<=u<n and 0<=v<n) or u==v:
            raise ValueError('vertices must be distinct and in range')
        validate_perm(h,k);validate_perm(b,k)
        adj[u].append((v,h,b))
        adj[v].append((u,inverse(h),inverse(b)))
    ih = [None]*n; ib=[None]*n; comp=[None]*n; members=[]
    for root in range(n):
        if ih[root] is not None: continue
        idx=len(members); members.append([])
        ih[root]=identity(k); ib[root]=identity(k)
        comp[root]=idx
        q=deque([root])
        while q:
            u=q.popleft(); members[idx].append(u)
            for v,h,b in adj[u]:
                if ih[v] is None:
                    ih[v]=multiply(ih[u],h)
                    ib[v]=multiply(ib[u],b)
                    comp[v]=idx; q.append(v)
    constraints=[[] for _ in members]
    for u,v,h,b in edges:
        hh=multiply(multiply(ih[u],h),inverse(ih[v]))
        bb=multiply(multiply(ib[u],b),inverse(ib[v]))
        constraints[comp[u]].append((hh,bb))
    return tuple(comp),tuple(tuple(m) for m in members),tuple(ih),tuple(ib),tuple(tuple(c) for c in constraints)


def recover_public_vertices(n,k,edges):
    """Exact decision/count/witness for S_k with small explicit enumerable k.

    A successful witness is directly verified against every supplied edge.
    """
    comp,members,hpath,bpath,constraints=cycle_conjugacy_constraints(n,k,edges)
    candidate_roots=[]
    for cc in constraints:
        roots=[]
        for t in permutations(range(k)):
            if all(multiply(multiply(inverse(t),h),t)==b for h,b in cc):
                roots.append(t)
        candidate_roots.append(roots)
        if not roots:
            return {'status':'unsatisfiable','witness':None,'solution_count':0,
                    'component_root_counts':tuple(len(a) for a in candidate_roots),
                    'cycle_constraint_count':tuple(len(x) for x in constraints)}
    x=[None]*n
    for i,vs in enumerate(members):
        t=candidate_roots[i][0]
        for v in vs:
            x[v]=multiply(multiply(inverse(hpath[v]),t),bpath[v])
    x=tuple(x)
    if not all(multiply(multiply(inverse(x[u]),h),x[v])==b
               for u,v,h,b in edges):
        raise AssertionError('public witness failed validation')
    counts=tuple(len(ts) for ts in candidate_roots)
    return {'status':'satisfiable','witness':x,
            'solution_count':__import__('math').prod(counts),
            'component_root_counts':counts,
            'cycle_constraint_count':tuple(len(c) for c in constraints)}


def simultaneous_centralizer_size(k,h_cycle_values):
    """Exact finite centralizer of a tuple of S_k elements (small k only)."""
    for h in h_cycle_values: validate_perm(h,k)
    return sum(all(multiply(t,h)==multiply(h,t) for h in h_cycle_values)
               for t in permutations(range(k)))


if __name__ == '__main__':
    e=identity(3); a=(1,0,2); c=(1,2,0)
    x=((1,2,0),(2,1,0),(1,0,2),(0,2,1))
    hs=[(0,1,e),(0,2,e),(0,3,e),(1,2,a),(2,3,c)]
    edges=[edge_from_hidden(u,v,h,x) for u,v,h in hs]
    ans=recover_public_vertices(4,3,edges)
    print('S3 twisted cycle example: recovered',ans['status'],
          'count',ans['solution_count'],'equals planted',ans['witness']==x)
    print('S3 common centralizer size',simultaneous_centralizer_size(3,(a,c)))
