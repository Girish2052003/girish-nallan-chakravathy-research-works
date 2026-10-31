"""NG-Q11: ternary source-form algebraic-degree leakage and d=1 linear solve.

All mathematical operations over F3, all local tables explicitly public.
Based on standard polynomial interpolation / Reed-Muller mathematics.
"""
from itertools import product
from fractions import Fraction


def interpolate(table, k):
    """Unique reduced F3 polynomial coefficients indexed by exponent tuples.

    Three-point transform coefficients: [f(0), f(2)-f(1), -f(0)-f(1)-f(2)].
    """
    pts = list(product(range(3),repeat=k))
    if len(table) != 3**k or any(x not in table for x in pts):
        raise ValueError('incomplete table')
    a = {x:int(table[x])%3 for x in pts}
    for axis in range(k):
        b = {}
        for fixed in product(range(3), repeat=k-1):
            def point(j):
                z=list(fixed);z.insert(axis,j)
                return tuple(z)
            v0,v1,v2 = (a[point(j)] for j in range(3))
            for j,coeff in enumerate((v0,(v2-v1)%3,(-v0-v1-v2)%3)):
                b[point(j)] = coeff
        a = b
    return a


def algebraic_degree(table, k):
    coeff = interpolate(table,k)
    return max((sum(exp) for exp,c in coeff.items() if c%3), default=-1)


def source_d2_identity(A, Q):
    """r=1,d=2, B=I; Q is an F3^2 -> F3 explicit table."""
    if len(Q)!=9:raise ValueError('Q table length must be nine')
    assert A in (1,2)
    points=list(product(range(3),repeat=2))
    index={z:i for i,z in enumerate(points)}
    table={}
    for x in product(range(3),repeat=3):
        z,w=x[1:]
        table[x]=(A*x[0]+Q[index[((z+1)%3,w)]]-Q[index[(z,w)]])%3
    return table


def random_scalar_false_positive_probability(k, threshold):
    if not (0<=threshold<=2*k):raise ValueError('threshold')
    monomials=sum(sum(e)<=threshold for e in product(range(3),repeat=k))
    return Fraction(1,3**(3**k-monomials)),monomials


def _solve_mod3(rows, rhs, n):
    a=[[int(y)%3 for y in row]+[int(b)%3] for row,b in zip(rows,rhs)]
    rank=0;pivots=[]
    for col in range(n):
        pivot=next((j for j in range(rank,len(a)) if a[j][col]),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank]
        inverse=pow(a[rank][col],-1,3)
        a[rank]=[inverse*x%3 for x in a[rank]]
        for j in range(len(a)):
            if j!=rank and a[j][col]:
                scale=a[j][col]
                a[j]=[(x-scale*y)%3 for x,y in zip(a[j],a[rank])]
        pivots.append(col);rank+=1
        if rank==len(a):break
    if any(not any(row[:n]) and row[n] for row in a):
        return None
    sol=[0]*n
    for idx,col in enumerate(pivots):sol[col]=a[idx][-1]
    return tuple(sol)


def solve_affine_public(n, factors, targets):
    """Exact public Gaussian elimination for arbitrary affine F3 factor maps.

    Returns satisfiable with a verified witness, or unsatisfiable.
    Throws if any table is non-affine or not complete. No secret input.
    """
    if n<1 or len(factors)!=len(targets):raise ValueError('invalid input')
    rows=[];rhs=[]
    for (scope,table),target in zip(factors,targets):
        scope=tuple(scope);k=len(scope)
        if not k or len(set(scope))!=k or any(j<0 or j>=n for j in scope):
            raise ValueError('invalid scope')
        pts=list(product(range(3),repeat=k))
        if len(table)!=3**k or any(p not in table for p in pts):
            raise ValueError('incomplete table')
        baseline=tuple(table[(0,)*k]); outdim=len(baseline)
        target=tuple(target)
        if not outdim or len(target)!=outdim:raise ValueError('dimension mismatch')
        coeff=[]
        for j in range(k):
            unit=tuple(int(i==j) for i in range(k))
            value=tuple(table[unit])
            coeff.append(tuple((value[t]-baseline[t])%3 for t in range(outdim)))
        for x in pts:
            expected=tuple((baseline[t]+sum(x[j]*coeff[j][t] for j in range(k)))%3
                           for t in range(outdim))
            if tuple(table[x])!=expected:
                raise ValueError('factor function is not affine')
        for t in range(outdim):
            row=[0]*n
            for j,var in enumerate(scope):row[var]=coeff[j][t]
            rows.append(row)
            rhs.append((target[t]-baseline[t])%3)
    witness=_solve_mod3(rows,rhs,n)
    if witness is None:return 'unsatisfiable',None
    assert all(tuple(table[tuple(witness[i] for i in scope)])==tuple(t)
               for (scope,table),t in zip(factors,targets))
    return 'satisfiable',witness


if __name__=='__main__':
    from random import Random
    rng=Random(730251)
    rows=[]
    for _ in range(300):
        Q=[rng.randrange(3) for _ in range(9)]
        rows.append(algebraic_degree(source_d2_identity(1,Q),3))
    print('degree histogram of 300 r1d2 source forms with identity B:',
          {v:rows.count(v) for v in set(rows)})
    print('random arbitrary function P[degree<=3]:',random_scalar_false_positive_probability(3,3))
