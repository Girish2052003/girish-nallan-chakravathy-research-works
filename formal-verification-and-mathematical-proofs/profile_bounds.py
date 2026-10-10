#!/usr/bin/env python3
"""Exact finite profile arithmetic; named attacks are NOT security lower bounds."""
import math
Q=1024
NU=3/16
PROFILES=[
 ("SGD-R1",128,64,5,3,2,1024,256,64,640,320,384),
 ("SGD-R2",192,96,7,4,3,1536,384,96,960,448,576),
 ("SGD-R3",256,128,9,5,4,2048,512,128,1280,640,768)
]
EXPECTED={
 "SGD-R1":(27648,191.72,156.91,-148.32),
 "SGD-R2":(124416,287.58,310.65,-219.82),
 "SGD-R3":(497664,383.44,515.11,-290.98)
}
def logsumexp(xs):
    z=max(xs)
    return z+math.log(sum(math.exp(x-z) for x in xs))
def logbinom(n,k):
    return math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)
def base_logerror(M,u):
    t=(M-u)//2
    logp0=logsumexp([logbinom(M,j)+j*math.log(NU)+(M-j)*math.log1p(-NU) for j in range(t+1,M+1)])
    logp1=(u-M)*math.log(Q)+logsumexp([logbinom(M,j)+j*math.log(Q-1) for j in range(t+1)])
    return max(logp0,logp1)
def majority_logerror(lp,rep=7):
    p=math.exp(lp)
    return logsumexp([logbinom(rep,j)+j*lp+(rep-j)*math.log1p(-p) for j in range(rep//2+1,rep+1)])
def report():
    for name,lam,n,k,d,r,m,M,u,N,l,fb in PROFILES:
        assert r==k-d and M<=Q and u<M<=m and u<=N
        q=m*(3**d)
        t=(M-u)//2
        clean=-N*math.log2(1-NU)
        relation=math.ceil((u+1)/2)*d*math.log2(3)
        fail=(math.log(l)+majority_logerror(base_logerror(M,u)))/math.log(2)
        e=EXPECTED[name]
        assert q==e[0] and abs(clean-e[1])<0.02 and abs(relation-e[2])<0.02 and abs(fail-e[3])<0.02
        print(f"{name}: q={q:,}, tdec={t}, first planted relation={u+1}; "+
              f"log2(random-clean-basis work)={clean:.2f}; "+
              f"log2(source-specific relation heuristic)={relation:.2f}; "+
              f"log2(whole-message error upper bound)={fail:.2f}")
        print("  These values are NOT a certification of IND-CPA, IND-CCA, or quantum security.")
if __name__=="__main__":
    report()
