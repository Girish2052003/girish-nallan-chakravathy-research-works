"""NG-Q20: Hankel-basis reconstruction for matrix-word public evaluators.

f(w)=alpha M_{w[0]}...M_{w[t-1]} beta over F_p. With a PROVIDED
full-rank d x d Hankel subblock, reconstruct an exactly equivalent
weighted automaton from O((|alphabet|+1)d^2+2d) membership calls.
No polynomial guarantee for FINDING an unknown basis with membership only.
Well-known weighted automata/Hankel theory, not a new hard problem or KEM.
"""
from itertools import product
from math import isqrt


def is_prime(p):
    return isinstance(p,int) and p>=2 and all(p%d for d in range(2,isqrt(p)+1))


def mod_matmul(A,B,p):
    if not A or not B or len(A[0]) != len(B):raise ValueError('matrix shape')
    return tuple(tuple(sum(A[i][h]*B[h][j] for h in range(len(B)))%p for j in range(len(B[0]))) for i in range(len(A)))


def rank(A,p):
    if not A:return 0
    m=[list(row) for row in A]
    if any(len(row)!=len(m[0]) for row in m):raise ValueError('matrix shape')
    r=0
    for j in range(len(m[0])):
        k=next((i for i in range(r,len(m)) if m[i][j]%p),None)
        if k is None:continue
        m[k],m[r]=m[r],m[k]
        iv=pow(m[r][j],-1,p)
        m[r]=[(z*iv)%p for z in m[r]]
        for i in range(len(m)):
            if i!=r and m[i][j]:
                c=m[i][j];m[i]=[(x-c*y)%p for x,y in zip(m[i],m[r])]
        r+=1
        if r==len(m):break
    return r


def inverse(A,p):
    n=len(A)
    if n<1 or any(len(row)!=n for row in A):raise ValueError('square matrix required')
    aug=[list(row)+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        k=next((i for i in range(j,n) if aug[i][j]%p),None)
        if k is None:raise ValueError('singular Hankel block')
        aug[k],aug[j]=aug[j],aug[k]
        iv=pow(aug[j][j],-1,p);aug[j]=[(z*iv)%p for z in aug[j]]
        for i in range(n):
            if i!=j and aug[i][j]:
                c=aug[i][j];aug[i]=[(x-c*y)%p for x,y in zip(aug[i],aug[j])]
    return tuple(tuple(row[n:]) for row in aug)


def validate_wfa(alpha,transitions,beta,p):
    if not is_prime(p) or not transitions or not alpha or len(beta)!=len(alpha):
        raise ValueError('prime field, nonempty alphabet and dimension required')
    d=len(alpha)
    if any(not isinstance(x,int) or not 0<=x<p for x in alpha+beta):
        raise ValueError('noncanonical vector')
    for a,M in transitions.items():
        if not isinstance(a,str) or not a or len(M)!=d or any(len(row)!=d for row in M):
            raise ValueError('invalid transition')
        if any(not isinstance(x,int) or not 0<=x<p for row in M for x in row):
            raise ValueError('noncanonical transition')


def evaluate(alpha,transitions,beta,p,word):
    row=tuple(alpha)
    for a in word:
        if a not in transitions:raise ValueError('symbol outside public alphabet')
        M=transitions[a]
        row=tuple(sum(row[j]*M[j][k] for j in range(len(row)))%p for k in range(len(row)))
    return sum(x*y for x,y in zip(row,beta))%p


def reconstruct(f,alphabet,p,prefixes,suffixes):
    """Exactly reconstruct realization, assuming full Hankel rank d and invertible H.

    f: publicly evaluable oracle (tuple of symbols -> field element).
    alphabet: explicit finite tuple of symbols.
    prefixes,suffixes: PUBLIC/PROVIDED word tuples forming full rank d basis.
    If Hankel rank is larger than d, matching finite values is not a global proof;
    global equality follows only from the stated rank-d assumption.
    """
    if not is_prime(p):raise ValueError('p must be prime')
    if not alphabet or len(set(alphabet))!=len(alphabet):raise ValueError('invalid alphabet')
    P=tuple(tuple(w) for w in prefixes);S=tuple(tuple(w) for w in suffixes)
    d=len(P)
    if d<1 or d!=len(S) or len(set(P))!=d or len(set(S))!=d:
        raise ValueError('need equally sized unique word bases')
    if any(a not in alphabet for w in P+S for a in w):raise ValueError('invalid word')
    cache={}
    def query(w):
        w=tuple(w)
        if w not in cache:
            x=f(w)
            if not isinstance(x,int) or not 0<=x<p:raise ValueError('oracle out of field')
            cache[w]=x
        return cache[w]
    H=tuple(tuple(query(u+v) for v in S) for u in P)
    Hinv=inverse(H,p)
    H_a={a:tuple(tuple(query(u+(a,)+v) for v in S) for u in P) for a in alphabet}
    # H=R C, H_a=R M_a C so H^-1 H_a=C^-1 M_a C.
    M={a:mod_matmul(Hinv,H_a[a],p) for a in alphabet}
    alpha=tuple(query(s) for s in S)  # alpha C
    hP=tuple(tuple((query(u),)) for u in P)  # R beta
    beta=tuple(row[0] for row in mod_matmul(Hinv,hP,p)) # C^-1 beta
    validate_wfa(alpha,M,beta,p)
    return {'alpha':alpha,'M':M,'beta':beta,'p':p,'dimension':d,
            'oracle_calls':len(cache),'queried_words':tuple(cache)}


def all_words(alphabet,max_len):
    return tuple(w for length in range(max_len+1) for w in product(alphabet,repeat=length))


def exploratory_hankel_basis(f,alphabet,p,d):
    """EXPONENTIAL search diagnostic. NOT a poly(d) general basis finder."""
    W=all_words(alphabet,d-1)
    matrix=tuple(tuple(f(u+v)%p for v in W) for u in W)
    if rank(matrix,p)<d:raise ValueError('given realization is not minimal dimension d')
    row_idx=[]
    for i,row in enumerate(matrix):
        if rank([matrix[t] for t in row_idx]+[row],p)>len(row_idx):row_idx.append(i)
        if len(row_idx)==d:break
    col_idx=[]
    for j in range(len(W)):
        cand=col_idx+[j]
        if rank([[matrix[i][t] for t in cand] for i in row_idx],p)>len(col_idx):col_idx.append(j)
        if len(col_idx)==d:break
    return tuple(W[i] for i in row_idx),tuple(W[j] for j in col_idx)


def needle(word,p,alphabet=None):
    """Rank |word|+1 weighted automaton over Fp with a single nonzero word."""
    u=tuple(word);L=len(u)
    d=L+1
    if alphabet is None:alphabet=tuple(sorted(set(u)))
    if not alphabet or any(a not in alphabet for a in u):raise ValueError('invalid needle alphabet')
    A={a:tuple(tuple(1 if i<L and j==i+1 and u[i]==a else 0 for j in range(d)) for i in range(d))
       for a in alphabet}
    alpha=(1,)+tuple(0 for _ in range(L))
    beta=tuple(int(i==L) for i in range(d))
    return alpha,A,beta


def needle_word_reconstruction_success_limit(alphabet_size,L,q):
    """Upper bound (q+1)/alphabet_size**L, q<alphabet_size**L.
    Uniform hidden needle, membership-only queries and one final guess.
    Other lengths give no information; adaptivity cannot improve this.
    """
    N=alphabet_size**L
    if alphabet_size<2 or L<1 or q<0 or q>=N:raise ValueError('parameters')
    from fractions import Fraction
    return Fraction(q+1,N)

if __name__=='__main__':
    from random import Random
    rng=Random(20261102)
    p=7;alphabet=('a','b');d=3
    while True:
        alpha=tuple(rng.randrange(p) for _ in range(d))
        beta=tuple(rng.randrange(p) for _ in range(d))
        matrices={a:tuple(tuple(rng.randrange(p) for _ in range(d)) for _ in range(d)) for a in alphabet}
        try:
            P,S=exploratory_hankel_basis(lambda w:evaluate(alpha,matrices,beta,p,w),alphabet,p,d)
            break
        except ValueError:pass
    rec=reconstruct(lambda w:evaluate(alpha,matrices,beta,p,w),alphabet,p,P,S)
    print('Hankel dimension',d,'basis',P,S,'public oracle evaluations',rec['oracle_calls'])
    print('same on all words length <=8:',all(evaluate(alpha,matrices,beta,p,w)==evaluate(rec['alpha'],rec['M'],rec['beta'],p,w) for w in all_words(alphabet,8)))
    for L in (8,16):print('needle length',L,'possibilities',2**L,'membership-only success bound 20 queries',needle_word_reconstruction_success_limit(2,L,20))
