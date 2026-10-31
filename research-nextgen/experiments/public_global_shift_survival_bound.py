"""Exact first-moment/union bound for public global NCSG shift survival.

Model: independent source-form local factors on fixed scopes of arity k=r+d:
 f_i(x)=A_i u_L + (Q_i(u_R+a)-Q_i(u_R)), u=B_i x,
 B_i uniform invertible over F3, Q_i independent uniform r-vector tables,
 A_i arbitrary invertible and nonzero a fixed, d>=2. All factor functions
 and scopes are explicit and public. This is NOT a security theorem.
"""
from fractions import Fraction
from itertools import combinations, product
from math import comb


def local_survival_probability(r=1, d=2):
    if not isinstance(r, int) or not isinstance(d, int) or r < 1 or d < 2:
        raise ValueError('require integer r>=1,d>=2')
    parallel_rank = 3 ** (d - 1)
    independent_rank = 4 * 3 ** (d - 2)
    p_parallel = Fraction(1, 3 ** (r * (parallel_rank - 1)))
    p_independent = Fraction(1, 3 ** (r * (independent_rank - 1)))
    alpha = (3 ** r - 1 + 3 ** r * (2 * p_parallel +
             (3 ** d - 3) * p_independent)) / (3 ** (r + d) - 1)
    return alpha


def expected_nonzero_shifts(scopes, n, r=1, d=2):
    """E[|D|-1], exactly, for fixed scopes with independent local factors."""
    scopes = tuple(tuple(s) for s in scopes)
    if any(len(s) != r+d or len(set(s)) != len(s) or
           any(j < 0 or j >= n for j in s) for s in scopes):
        raise ValueError('every scope must have r+d distinct valid coordinates')
    alpha = local_survival_probability(r, d)
    return sum((alpha ** sum(any(h[j] for j in scope) for scope in scopes)
               for h in product(range(3), repeat=n) if any(h)), Fraction(0))


def complete_uniform_scope_expected(n, r=1, d=2):
    """Exact E[|D|-1], if all subsets of arity r+d are independent factors."""
    k = r+d
    if n < k: raise ValueError('n must be at least local arity')
    m = comb(n, k)
    alpha = local_survival_probability(r, d)
    result = Fraction(0)
    for weight in range(1, n+1):
        missed = comb(n-weight, k) if n-weight >= k else 0
        result += comb(n, weight) * (2 ** weight) * alpha ** (m - missed)
    return result


def complete_uniform_scope_probability_bound(n, r=1, d=2):
    # Nontrivial D over GF(3) has >=2 nonzero members (h and 2h).
    return min(Fraction(1), complete_uniform_scope_expected(n, r, d) / 2)


def brute_rank_mod3(matrix):
    a = [[int(v)%3 for v in row] for row in matrix]
    if not a: return 0
    rank=0
    for col in range(len(a[0])):
        ix=next((i for i in range(rank,len(a)) if a[i][col]), None)
        if ix is None: continue
        a[rank],a[ix]=a[ix],a[rank]
        mult=pow(a[rank][col],-1,3)
        a[rank]=[x*mult%3 for x in a[rank]]
        for j in range(len(a)):
            if j!=rank and a[j][col]:
                t=a[j][col]
                a[j]=[(x-t*y)%3 for x,y in zip(a[j],a[rank])]
        rank+=1
        if rank==len(a):break
    return rank


def mixed_difference_rank(d, a, v):
    """Direct linear-operator rank check, independent of the formula."""
    points = list(product(range(3),repeat=d))
    index = {x:i for i,x in enumerate(points)}
    result=[]
    for x in points:
        va = tuple((x[j]+v[j]+a[j])%3 for j in range(d))
        xxv = tuple((x[j]+v[j])%3 for j in range(d))
        xxa = tuple((x[j]+a[j])%3 for j in range(d))
        row=[0]*len(points)
        for y,c in ((va,1),(xxv,-1),(xxa,-1),(x,1)):
            row[index[y]]=(row[index[y]]+c)%3
        result.append(row)
    return brute_rank_mod3(result)


if __name__ == '__main__':
    print('alpha d=2,r=1',local_survival_probability())
    for n in (4,5,6,7,8):
        print('n',n,'factors',comb(n,3),
              'expected_nonzero',float(complete_uniform_scope_expected(n)),
              'P(D != {0}) upper',float(complete_uniform_scope_probability_bound(n)))
