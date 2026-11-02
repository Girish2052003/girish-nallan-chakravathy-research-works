"""NG-Q19: public randomized recovery for GL(k,F_p) twisted graph transport.

Research-only. For prime p>k, random intertwiners from a PUBLIC linear
space recover invertible conjugators with per-trial success >=1-k/p when
one exists. This is standard module-isomorphism/Schwartz-Zippel mathematics,
NOT a new trapdoor, universal finite-field algorithm, or secure KEM.
"""
from collections import deque
from random import Random


def is_prime(p):
    if not isinstance(p,int) or p<2:return False
    return all(p%d for d in range(2,__import__('math').isqrt(p)+1))


def validate(A,p,k):
    if len(A)!=k or any(len(row)!=k for row in A):raise ValueError('bad matrix shape')
    if any(not isinstance(t,int) or t<0 or t>=p for row in A for t in row):
        raise ValueError('noncanonical field element')


def eye(k):return tuple(tuple(int(i==j) for j in range(k)) for i in range(k))


def mul(A,B,p):
    n=len(A)
    return tuple(tuple(sum(A[i][r]*B[r][j] for r in range(n))%p
                       for j in range(n)) for i in range(n))


def rank_and_rref(rows,p,d):
    A=[list(x) for x in rows]
    if any(len(a)!=d for a in A):raise ValueError('bad equation dimensions')
    piv=[];r=0
    for col in range(d):
        t=next((i for i in range(r,len(A)) if A[i][col]%p),None)
        if t is None:continue
        A[r],A[t]=A[t],A[r]
        z=pow(A[r][col],-1,p)
        A[r]=[(v*z)%p for v in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][col]:
                v=A[i][col]
                A[i]=[(x-v*y)%p for x,y in zip(A[i],A[r])]
        piv.append(col);r+=1
        if r==len(A):break
    return tuple(tuple(row) for row in A),tuple(piv)


def inv(A,p):
    k=len(A);validate(A,p,k)
    aug=[list(row)+list(eye(k)[i]) for i,row in enumerate(A)]
    for j in range(k):
        r=next((i for i in range(j,k) if aug[i][j]%p),None)
        if r is None:raise ValueError('singular matrix')
        aug[j],aug[r]=aug[r],aug[j]
        invpivot=pow(aug[j][j],-1,p)
        aug[j]=[(x*invpivot)%p for x in aug[j]]
        for i in range(k):
            if i!=j and aug[i][j]:
                c=aug[i][j]
                aug[i]=[(a-c*b)%p for a,b in zip(aug[i],aug[j])]
    return tuple(tuple(row[k:]) for row in aug)


def nullspace(rows,p,d):
    A,piv=rank_and_rref(rows,p,d)
    free=[c for c in range(d) if c not in piv]
    basis=[]
    for col in free:
        v=[0]*d;v[col]=1
        for row,pc in enumerate(piv):v[pc]=(-A[row][col])%p
        basis.append(tuple(v))
    return tuple(basis)


def simultaneous_space(A,B,p):
    """Public basis of T with A_i*T=T*B_i; no secret is an argument."""
    if not is_prime(p) or len(A)!=len(B):raise ValueError('prime p and matching tuples required')
    if A:k=len(A[0])
    elif B:k=len(B[0])
    else:raise ValueError('dimension required for empty tuples')
    if k<1:raise ValueError('positive k required')
    rows=[]
    for a,b in zip(A,B):
        validate(a,p,k);validate(b,p,k)
        for i in range(k):
            for j in range(k):
                eq=[0]*(k*k)
                for u in range(k):
                    eq[u*k+j]+=a[i][u]
                    eq[i*k+u]-=b[u][j]
                rows.append(tuple(x%p for x in eq))
    return nullspace(rows,p,k*k)


def conjugator(A,B,p,k,trials=32,seed=1):
    """Randomized public witness or inconclusive. NEVER calls failure UNSAT.

    If A,B admit invertible T and p>k, each independent random trial
    succeeds with probability at least 1-k/p by determinant polynomial SZ.
    For p<=k there is no useful stated lower bound, but successes are valid.
    """
    if not is_prime(p) or k<1 or trials<1:raise ValueError('bad parameters')
    for a,b in zip(A,B):validate(a,p,k);validate(b,p,k)
    if len(A)!=len(B):raise ValueError('tuple mismatch')
    if not A: return {'status':'witness','T':eye(k),'space_dimension':k*k,
                      'failure_upper_if_planted':0.0}
    basis=simultaneous_space(A,B,p)
    if not basis:return {'status':'proven_unsatisfiable','T':None,'space_dimension':0,
                         'failure_upper_if_planted':0.0}
    rng=Random(seed)
    for _ in range(trials):
        co=[rng.randrange(p) for _ in basis]
        flat=[sum(c*v[j] for c,v in zip(co,basis))%p for j in range(k*k)]
        T=tuple(tuple(flat[i*k+j] for j in range(k)) for i in range(k))
        try:inv(T,p)
        except ValueError:continue
        if any(mul(a,T,p)!=mul(T,b,p) for a,b in zip(A,B)):
            raise AssertionError('public linearization yielded invalid conjugator')
        return {'status':'witness','T':T,'space_dimension':len(basis),
                'failure_upper_if_planted':0.0}
    bound=(k/p)**trials if p>k else None
    return {'status':'inconclusive','T':None,'space_dimension':len(basis),
            'failure_upper_if_planted':bound}


def edge_from_secret(u,v,H,X,p):
    return (u,v,H,mul(mul(inv(X[u],p),H,p),X[v],p))


def recover_graph(n,k,p,edges,trials=32,seed=1):
    """Public-only graph witness/ambiguous decision over GL(k,F_p).

    Does not expose original secret. Return 'inconclusive' after random failure.
    No universal polynomial decision guarantee claimed for p<=k.
    """
    if n<1 or k<1 or not is_prime(p):raise ValueError('invalid graph parameters')
    adj=[[] for _ in range(n)]
    for u,v,h,b in edges:
        if not(0<=u<n and 0<=v<n) or u==v:raise ValueError('invalid vertices')
        validate(h,p,k);validate(b,p,k)
        inv(h,p);inv(b,p)
        adj[u].append((v,h,b));adj[v].append((u,inv(h,p),inv(b,p)))
    hp=[None]*n;bp=[None]*n; comp=[None]*n;vertices=[]
    for root in range(n):
        if comp[root] is not None:continue
        ci=len(vertices);vertices.append([]);comp[root]=ci;hp[root]=eye(k);bp[root]=eye(k)
        queue=deque([root])
        while queue:
            u=queue.popleft();vertices[ci].append(u)
            for v,h,b in adj[u]:
                if comp[v] is None:
                    comp[v]=ci;hp[v]=mul(hp[u],h,p);bp[v]=mul(bp[u],b,p);queue.append(v)
    As=[[] for _ in vertices];Bs=[[] for _ in vertices]
    for u,v,h,b in edges:
        As[comp[u]].append(mul(mul(hp[u],h,p),inv(hp[v],p),p))
        Bs[comp[u]].append(mul(mul(bp[u],b,p),inv(bp[v],p),p))
    result=[None]*n;bounds=[]
    for ci,vs in enumerate(vertices):
        ans=conjugator(As[ci],Bs[ci],p,k,trials,seed+ci)
        if ans['status']!='witness':
            return {'status':ans['status'],'witness':None,
                    'components':len(vertices),'failure_bound':ans['failure_upper_if_planted']}
        t=ans['T'];bounds.append(ans['failure_upper_if_planted'])
        for v in vs:result[v]=mul(mul(inv(hp[v],p),t,p),bp[v],p)
    if any(mul(mul(inv(result[u],p),h,p),result[v],p)!=b for u,v,h,b in edges):
        raise AssertionError('graph witness failed full public verification')
    return {'status':'witness','witness':tuple(result),
            'components':len(vertices),'failure_bound':0.0}


def random_gl(k,p,rng):
    if not is_prime(p):raise ValueError('field prime required')
    for _ in range(100000):
        M=tuple(tuple(rng.randrange(p) for _ in range(k)) for _ in range(k))
        try:inv(M,p);return M
        except ValueError:pass
    raise RuntimeError('random GL generator exceeded trials')

if __name__=='__main__':
    r=Random(119)
    for k,p,n in [(2,5,5),(3,11,7),(5,17,9),(7,101,8)]:
        secret=tuple(random_gl(k,p,r) for _ in range(n))
        spec=[(i,i+1,random_gl(k,p,r)) for i in range(n-1)]
        spec += [(0,j,random_gl(k,p,r)) for j in range(2,n)]
        pub=[edge_from_secret(i,j,h,secret,p) for i,j,h in spec]
        found=recover_graph(n,k,p,pub,trials=64,seed=91)
        print('GL',k,p,'vertices',n,'public witness?',found['status'],
              'original_equal?',found['witness']==secret)
