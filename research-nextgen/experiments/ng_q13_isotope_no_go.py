"""NG-Q13: explicit public group normalization of abelian-group isotopes.

Not a novel quasigroup structure: classic transport and isotope theory.
Finite truth tables only; complexity measured in the PUBLIC table length.
"""
from itertools import product
from random import Random


def digits(value,m):
    result=[]
    for _ in range(m):
        result.append(value%3);value//=3
    if value:raise ValueError('element out of group range')
    return tuple(result)


def index(coords):
    return sum(v*3**j for j,v in enumerate(coords))


def group_sum(x,y,m):
    return index(tuple((a+b)%3 for a,b in zip(digits(x,m),digits(y,m))))


def group_diff(x,y,m):
    return index(tuple((a-b)%3 for a,b in zip(digits(x,m),digits(y,m))))


def random_isotope(m,seed):
    """T(x,y)=gamma^-1(alpha(x)+beta(y)) over (F3)^m."""
    if not 1<=m<=6:raise ValueError('invalid test size')
    n=3**m
    rng=Random(seed)
    alpha=list(range(n));beta=list(range(n));gamma=list(range(n))
    rng.shuffle(alpha);rng.shuffle(beta);rng.shuffle(gamma)
    inverse_gamma={v:i for i,v in enumerate(gamma)}
    T={(x,y):inverse_gamma[group_sum(alpha[x],beta[y],m)]
       for x in range(n) for y in range(n)}
    return T,alpha,beta,gamma


def validate_latin_square(T,n):
    if n<2 or len(T)!=n*n or any((x,y) not in T for x in range(n) for y in range(n)):
        raise ValueError('incomplete public table')
    if any(T[x,y] not in range(n) for x in range(n) for y in range(n)):
        raise ValueError('invalid public symbol')
    if any(len({T[x,y] for y in range(n)})!=n for x in range(n)):
        raise ValueError('not Latin rows')
    if any(len({T[x,y] for x in range(n)})!=n for y in range(n)):
        raise ValueError('not Latin columns')


def public_principal_group(T,n,x0=0,y0=0):
    """Public normalization P(a,b)=T(R^-1(a), L^-1(b)).

    R(x)=T(x,y0), L(y)=T(x0,y). For an abelian group isotope,
    P is a public abelian group law with identity T(x0,y0).
    """
    validate_latin_square(T,n)
    if not (0<=x0<n and 0<=y0<n):raise ValueError('invalid anchors')
    r_inv={T[x,y0]:x for x in range(n)}
    l_inv={T[x0,y]:y for y in range(n)}
    P={(a,b):T[r_inv[a],l_inv[b]] for a in range(n) for b in range(n)}
    e=T[x0,y0]
    return P,e


def public_group_coordinates(P,n,e):
    """Recover equivalent additive F3 coordinates if P is elementary abelian.

    Generates subgroup by adjoining a new order-3 element repeatedly;
    verifies every Cayley-table equation after reconstruction.
    """
    if n<2 or 3**round(__import__('math').log(n,3))!=n:
        raise ValueError('n must be 3^m')
    if any(P[e,x]!=x or P[x,e]!=x for x in range(n)):
        raise ValueError('not identity')
    coordinate={e:()}
    while len(coordinate)<n:
        old=coordinate
        g=next(x for x in range(n) if x not in old)
        gg=P[g,g]
        if P[g,gg]!=e:raise ValueError('element does not have order three')
        coordinate={}
        for k,t in enumerate((e,g,gg)):
            for x,vec in old.items():
                y=P[x,t]
                if y in coordinate:raise ValueError('coset collision')
                coordinate[y]=vec+(k,)
        if len(coordinate)!=3*len(old):raise ValueError('unexpected subgroup size')
    m=len(next(iter(coordinate.values())))
    if len(coordinate)!=n or m>0 and 3**m!=n:raise ValueError('not 3-elementary')
    for x in range(n):
        for y in range(n):
            if coordinate[P[x,y]] != tuple((u+v)%3 for u,v in zip(coordinate[x],coordinate[y])):
                raise ValueError('not elementary abelian group')
    return coordinate


def recover_equivalent_isotope(T,n,x0=0,y0=0):
    """Extract an equivalent PUBLIC (alpha,beta,gamma) group-isotope secret.

    If the public Latin square is not a principal elementary-abelian-group
    isotope, rejects rather than fabricating group coordinates.
    """
    P,e=public_principal_group(T,n,x0,y0)
    coords=public_group_coordinates(P,n,e)
    m=len(coords[e])
    gamma={x:index(coords[x]) for x in range(n)}
    alpha={x:gamma[T[x,y0]] for x in range(n)}
    beta={y:gamma[T[x0,y]] for y in range(n)}
    inv_gamma={v:k for k,v in gamma.items()}
    if any(T[x,y]!=inv_gamma[group_sum(alpha[x],beta[y],m)]
           for x in range(n) for y in range(n)):
        raise ValueError('isotope representation check failed')
    return alpha,beta,gamma


def fano_steiner_table():
    """Fano-plane Steiner Latin square on the 7 nonzero F2^3 vectors.

    Symbols 0..6 encode vectors 1..7. For distinct x,y use their
    xor as the third point; diagonal entries are idempotent.
    This is not isomorphic or isotopic to the order-seven additive group.
    """
    return {(x,y):(x if x==y else ((x+1)^(y+1))-1)
            for x in range(7) for y in range(7)}


if __name__=='__main__':
    for m in (2,3):
        T,a,b,g=random_isotope(m,20261101+m)
        P,e=public_principal_group(T,3**m,x0=1,y0=2)
        coords=public_group_coordinates(P,3**m,e)
        print('m',m,'table entries',len(T),'recoverable equivalent public group coordinates',len(coords))
