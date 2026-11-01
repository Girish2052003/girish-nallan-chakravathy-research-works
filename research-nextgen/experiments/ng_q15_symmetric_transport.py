"""NG-Q15: polynomial-time simultaneous conjugacy in the full symmetric group.

Public permutation tuples A_i,B_i satisfy t^-1 A_i t = B_i when a conjugator
exists. Determine it by matching orbits of the two coloured permutation actions.
Use it to recover hidden twisted-transport vertices over S_k without listing k!.
Prior art: simultaneous conjugacy algorithms and finite permutation actions.
"""
from collections import deque
from ng_q14_nonabelian_transport import (
    identity, inverse, multiply, validate_perm)


def _orbits(k, generators):
    moves=list(generators)+[inverse(p) for p in generators]
    unseen=set(range(k))
    result=[]
    while unseen:
        root=min(unseen)
        seen={root};q=deque([root])
        while q:
            x=q.popleft()
            for p in moves:
                y=p[x]
                if y not in seen:
                    seen.add(y);q.append(y)
        unseen-=seen
        result.append(tuple(sorted(seen)))
    return result


def _pointed_map(k, A, B, source, dest):
    """Test one possible source->dest image and return orbit map or None."""
    A_moves = list(A)+[inverse(p) for p in A]
    B_moves = list(B)+[inverse(p) for p in B]
    mapping={source: dest}
    inverse_mapping={dest: source}
    q=deque([source])
    while q:
        x=q.popleft()
        for a,b in zip(A_moves,B_moves):
            xb=b[x];ya=a[mapping[x]]
            if xb in mapping:
                if mapping[xb]!=ya:return None
            else:
                if ya in inverse_mapping:return None
                mapping[xb]=ya;inverse_mapping[ya]=xb;q.append(xb)
    return mapping


def simultaneous_permutation_conjugator(k,A,B):
    """Find t in S_k such that t^-1 A_i t=B_i for every pair, or None.

    Polynomial in explicit degree k and number of permutation generators.
    No group enumeration. Works with nontransitive tuples / empty constraints.
    """
    if k<1 or len(A)!=len(B):raise ValueError('invalid tuple length or degree')
    for p in tuple(A)+tuple(B):validate_perm(p,k)
    orbit_a=_orbits(k,A)
    orbit_b=_orbits(k,B)
    used=set();global_map={}
    for ob in orbit_b:
        source=ob[0]
        choice=None;choice_orbit=None
        for oa_id,oa in enumerate(orbit_a):
            if oa_id in used or len(oa)!=len(ob):continue
            for dest in oa:
                candidate=_pointed_map(k,A,B,source,dest)
                if candidate is not None and len(candidate)==len(ob) and set(candidate.values())==set(oa):
                    choice=candidate;choice_orbit=oa_id;break
            if choice is not None:break
        if choice is None:return None
        used.add(choice_orbit)
        global_map.update(choice)
    if len(global_map)!=k:return None
    t=tuple(global_map[i] for i in range(k))
    validate_perm(t,k)
    if any(multiply(multiply(inverse(t),a),t)!=b for a,b in zip(A,B)):
        raise AssertionError('simultaneous conjugacy witness verification failed')
    return t


def recover_twisted_symmetric_vertices(n,k,edges):
    """Solve arbitrary public twisted transport over S_k in polynomial time.

    For each graph component, a spanning tree gives path H,B; each chord
    yields t^-1 H_cycle t=B_cycle. Recover t by orbit propagation, then
    compute every secret-equivalent vertex value and verify all edges.
    """
    if k<2:raise ValueError('degree must be at least two')
    # The shared finite-group helper is only bounded by k<=6; here reproduce
    # its tree traversal with no factorial size dependency.
    from collections import deque
    if n<1:raise ValueError('n must be positive')
    adj=[[] for _ in range(n)]
    for u,v,h,b in edges:
        if not(0<=u<n and 0<=v<n) or u==v:raise ValueError('invalid edge')
        validate_perm(h,k);validate_perm(b,k)
        adj[u].append((v,h,b))
        adj[v].append((u,inverse(h),inverse(b)))
    comp=[None]*n; hpath=[None]*n; bpath=[None]*n; members=[]
    for root in range(n):
        if comp[root] is not None:continue
        ci=len(members);members.append([]);comp[root]=ci
        hpath[root]=identity(k);bpath[root]=identity(k)
        q=deque([root])
        while q:
            u=q.popleft();members[ci].append(u)
            for v,h,b in adj[u]:
                if comp[v] is None:
                    comp[v]=ci;hpath[v]=multiply(hpath[u],h)
                    bpath[v]=multiply(bpath[u],b);q.append(v)
    ca=[[] for _ in members]; cb=[[] for _ in members]
    for u,v,h,b in edges:
        ca[comp[u]].append(multiply(multiply(hpath[u],h),inverse(hpath[v])))
        cb[comp[u]].append(multiply(multiply(bpath[u],b),inverse(bpath[v])))
    output=[None]*n
    for ci,vs in enumerate(members):
        root_t=simultaneous_permutation_conjugator(k,ca[ci],cb[ci])
        if root_t is None:return {'status':'unsatisfiable','witness':None,'components':len(members)}
        for v in vs:
            output[v]=multiply(multiply(inverse(hpath[v]),root_t),bpath[v])
    output=tuple(output)
    if not all(multiply(multiply(inverse(output[u]),h),output[v])==b
               for u,v,h,b in edges):raise AssertionError('bad public graph witness')
    return {'status':'satisfiable','witness':output,'components':len(members)}


if __name__=='__main__':
    from random import Random
    from ng_q14_nonabelian_transport import edge_from_hidden
    rng=Random(1415)
    for k in (3,7,20,100):
        n=7
        x=tuple(tuple(rng.sample(range(k),k)) for _ in range(n))
        spec=[(u,u+1,tuple(rng.sample(range(k),k))) for u in range(n-1)]
        spec += [(0,v,tuple(rng.sample(range(k),k))) for v in range(2,n)]
        edges=[edge_from_hidden(u,v,h,x) for u,v,h in spec]
        recovered=recover_twisted_symmetric_vertices(n,k,edges)
        print('degree',k,'n',n,'status',recovered['status'],
              'witness matches planted',recovered['witness']==x)
