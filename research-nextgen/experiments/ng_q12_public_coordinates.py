"""NG-Q12: Recover equivalent coordinates of explicit F3 local source forms.

Research-only deterministic exhaustive finite algorithm. A recovered triple
(B,A,Q) is an equivalent PUBLIC GENERATING REPRESENTATION, not a KEM secret.
"""
from itertools import product
from fractions import Fraction

F3 = range(3)
POINTS2 = tuple(product(F3, repeat=2))
POINTS3 = tuple(product(F3, repeat=3))


def matvec(M, v):
    return tuple(sum(x*y for x,y in zip(row,v))%3 for row in M)


def rank(M):
    m=[list(row) for row in M]
    pivots=0
    for col in range(len(m[0])):
        j=next((j for j in range(pivots,len(m)) if m[j][col]),None)
        if j is None:continue
        m[pivots],m[j]=m[j],m[pivots]
        k=pow(m[pivots][col],-1,3)
        m[pivots]=[(k*v)%3 for v in m[pivots]]
        for t in range(len(m)):
            if t!=pivots and m[t][col]:
                c=m[t][col]
                m[t]=[(a-c*b)%3 for a,b in zip(m[t],m[pivots])]
        pivots+=1
        if pivots==len(m):break
    return pivots


def invert(M):
    a=[list(row)+[int(i==j) for j in range(3)] for i,row in enumerate(M)]
    for col in range(3):
        j=next((i for i in range(col,3) if a[i][col]),None)
        if j is None:raise ValueError('singular')
        a[col],a[j]=a[j],a[col]
        inv=pow(a[col][col],-1,3)
        a[col]=[(inv*v)%3 for v in a[col]]
        for i in range(3):
            if i!=col and a[i][col]:
                v=a[i][col]
                a[i]=[(u-v*w)%3 for u,w in zip(a[i],a[col])]
    return tuple(tuple(row[3:]) for row in a)


def all_invertible_matrices():
    """Unbiased enumeration of all |GL(3,3)|=11232 invertible matrices."""
    nonzero=tuple(x for x in POINTS3 if any(x))
    for r0 in nonzero:
        for r1 in nonzero:
            if any(r1==tuple(c*v%3 for v in r0) for c in (0,1,2)):
                continue
            for r2 in POINTS3:
                M=(r0,r1,r2)
                if rank(M)==3:
                    yield M


def generate(B,A,Q):
    """Explicit public 27-entry f(x) for B in GL3, A in F3*, Q nine entries."""
    if A not in (1,2) or rank(B)!=3 or set(Q)!=set(POINTS2):
        raise ValueError('invalid generation parameters')
    result={}
    for x in POINTS3:
        u=matvec(B,x)
        z,w=u[1:]
        result[x]=(A*u[0]+Q[((z+1)%3,w)]-Q[(z,w)])%3
    return result


def validate_public(f):
    if len(f)!=27 or set(f)!=set(POINTS3) or any(x not in F3 for x in f.values()):
        raise ValueError('require complete scalar ternary truth table')


def recover_equivalent(f):
    """Find an equivalent (B,A,Q), or prove NONE exists in the fixed model.

    Enumerate the inverse B coordinate map C; verify all 27 table values.
    Never needs original secret inputs and does not branch on planted witnesses.
    """
    validate_public(f)
    for C in all_invertible_matrices():
        g={}
        A=None
        plausible=True
        for z,w in POINTS2:
            x0=matvec(C,(0,z,w))
            x1=matvec(C,(1,z,w))
            x2=matvec(C,(2,z,w))
            v0,v1,v2=f[x0],f[x1],f[x2]
            this_A=(v1-v0)%3
            if this_A not in (1,2) or v2!=(v0+2*this_A)%3:
                plausible=False;break
            if A is not None and A!=this_A:
                plausible=False;break
            A=this_A
            g[(z,w)]=v0
        if not plausible:continue
        if any(sum(g[(z,w)] for z in F3)%3 for w in F3):continue
        Q={}
        for w in F3:
            Q[(0,w)]=0
            Q[(1,w)]=g[(0,w)]
            Q[(2,w)]=(g[(0,w)]+g[(1,w)])%3
        B=invert(C)
        if generate(B,A,Q)==f:
            return B,A,Q
        raise AssertionError('representation failed direct verification')
    return None


def membership_false_positive_upper_bound():
    """Union bound for uniform independent 27-entry random function table."""
    matrices=(27-1)*(27-3)*(27-9)
    return Fraction(matrices*2*3**6,3**27)


def fixed_basis_source_count():
    """Fixed known basis B and nonzero A: image Q has dimension 6, ker dimension 3."""
    return 3**6,3**3

if __name__=='__main__':
    print('GL3 count:',sum(1 for _ in all_invertible_matrices()))
    print('fixed (B,A): source image count, Q fiber count=',fixed_basis_source_count())
    print('uniform random table membership upper bound=',membership_false_positive_upper_bound(),
          'approx',float(membership_false_positive_upper_bound()))
