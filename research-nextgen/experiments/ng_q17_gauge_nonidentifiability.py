"""NG-Q17: absolute gauge and disconnected-component ambiguity.

A distributional NO-IDENTIFIABILITY theorem under independently uniform
finite-group vertex secrets and observation kernels depending only on ratios.
Not cryptographic confidentiality, because ratios can be publicly recovered.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import permutations, product
from ng_q16_robust_relative_sync import multiply, inverse, validate_perm


def components(n, edges):
    if n < 1:
        raise ValueError('n must be positive')
    adj = [[] for _ in range(n)]
    for i,j in edges:
        if not (0 <= i < j < n):
            raise ValueError('invalid edge')
        adj[i].append(j);adj[j].append(i)
    comp = [None] * n
    nodes = []
    for start in range(n):
        if comp[start] is not None:
            continue
        ci=len(nodes); nodes.append([])
        stack=[start];comp[start]=ci
        while stack:
            u=stack.pop();nodes[ci].append(u)
            for v in adj[u]:
                if comp[v] is None:
                    comp[v]=ci;stack.append(v)
    return tuple(comp),tuple(tuple(sorted(x)) for x in nodes)


def left_gauge_transform(secrets, comp, gauge):
    """Independently left-multiply all vertices in a component by g_c."""
    if len(comp)!=len(secrets) or max(comp,default=-1)>=len(gauge):
        raise ValueError('invalid gauge map')
    return tuple(multiply(gauge[comp[i]],secrets[i]) for i in range(len(secrets)))


def observed_likelihood(secrets, observed, erasures, group_size, rho, eps):
    """Likelihood of exact data, given fixed secret x and a chosen edge set.

    Each potential edge independently present with probability rho; when present,
    label is true ratio w.p.1-eps, otherwise uniformly sampled from G.
    Exact fractions; prior over x is handled separately by caller.
    """
    if len(observed)+len(erasures)==0:
        raise ValueError('provide observation/erasure pattern')
    if not (Fraction(0)<=rho<=Fraction(1) and Fraction(0)<=eps<=Fraction(1)):
        raise ValueError('invalid noise probabilities')
    seen=set(observed)
    if seen & set(erasures):
        raise ValueError('edge both observed and missing')
    weight=Fraction(1)
    for (i,j),label in observed.items():
        if not (0<=i<j<len(secrets)):
            raise ValueError('bad edge')
        truth=multiply(inverse(secrets[i]),secrets[j])
        weight *= rho * ((1-eps)*int(label==truth)+eps/Fraction(group_size))
    for i,j in erasures:
        if not (0<=i<j<len(secrets)):
            raise ValueError('bad erased edge')
        weight *= (1-rho)
    return weight


def exact_posterior_histogram(n,k,observed,erasures,rho,eps,readout):
    """Exhaustively calculate unnormalized posterior readout histogram.

    Uniform independent S_k hidden vertices. Work only for toy k,n:
    exhaustive cost is (k!)^n. This is a finite proof check, not an attack.
    """
    if k>4 or n>5:
        raise ValueError('toy exhaustive control only')
    group=list(permutations(range(k)))
    for x in observed.values():
        validate_perm(x,k)
    counts=defaultdict(Fraction)
    for x in product(group,repeat=n):
        counts[readout(x)] += observed_likelihood(x,observed,erasures,
                                                 len(group),rho,eps)
    total=sum(counts.values(),Fraction(0))
    if total==0:
        raise ValueError('impossible observation')
    return {k:w/total for k,w in counts.items()}


if __name__ == '__main__':
    group=list(permutations(range(3)))
    obs={(0,1):group[2],(1,2):group[3]}
    posterior=exact_posterior_histogram(3,3,obs,[(0,2)],
                                        Fraction(3,4),Fraction(1,3),lambda x:x[0])
    print('posterior root marginal:',{str(k):str(v) for k,v in posterior.items()})
