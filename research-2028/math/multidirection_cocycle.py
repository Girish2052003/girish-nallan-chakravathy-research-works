#!/usr/bin/env python3
"""Two-direction ternary finite-difference cocycle identity and constructive integration.
Demonstrates mathematical structure, NOT cryptographic one-wayness.
"""
import itertools,random,unittest
P=3
GRID=list(itertools.product(range(P),repeat=2))
A=(1,0)
B=(0,1)
def step(x,e):
    return ((x[0]+e[0])%P,(x[1]+e[1])%P)
def derivative(Q,e):
    return {x:(Q[step(x,e)]-Q[x])%P for x in GRID}
def curl(g,h):
    return {x:(g[step(x,B)]-g[x]-h[step(x,A)]+h[x])%P for x in GRID}
def periodic_sums(g,e):
    return {x:sum(g[(x[0]+j*e[0])%P,(x[1]+j*e[1])%P]
                 for j in range(P))%P for x in GRID}
def integrate(g,h):
    # Solve potential increments from public derivative tables.
    Q={(0,0):0}
    frontier=[(0,0)]
    while frontier:
        x=frontier.pop()
        for e,table in ((A,g),(B,h)):
            y=step(x,e);candidate=(Q[x]+table[x])%P
            if y not in Q:Q[y]=candidate;frontier.append(y)
            elif Q[y]!=candidate:return None
    if len(Q)!=len(GRID):return None
    if derivative(Q,A)!=g or derivative(Q,B)!=h:return None
    return Q
class CocycleTests(unittest.TestCase):
    def test_exact_integrability(self):
        r=random.Random(78010)
        for _ in range(100):
            Q={x:r.randrange(P) for x in GRID}
            g=derivative(Q,A);h=derivative(Q,B)
            self.assertEqual(set(curl(g,h).values()),{0})
            self.assertEqual(set(periodic_sums(g,A).values()),{0})
            self.assertEqual(set(periodic_sums(h,B).values()),{0})
            recovered=integrate(g,h)
            self.assertIsNotNone(recovered)
            self.assertEqual(len({(recovered[x]-Q[x])%P for x in GRID}),1)
    def test_corruption_detected(self):
        r=random.Random(987)
        for _ in range(40):
            Q={x:r.randrange(P) for x in GRID}
            g=derivative(Q,A);h=derivative(Q,B)
            g[(0,0)]=(g[(0,0)]+1)%P
            self.assertIsNone(integrate(g,h))
            self.assertTrue(any(v for v in curl(g,h).values()) or
                            any(v for v in periodic_sums(g,A).values()))
    def test_kernel_dimension(self):
        # 9-element torus: gradient of scalar table has rank 8,
        # since simultaneous directional differences have constant functions as kernel.
        rows=[]
        for x in GRID:
            Q={y:0 for y in GRID};Q[x]=1
            pair=derivative(Q,A),derivative(Q,B)
            rows.append([pair[0][y] for y in GRID]+[pair[1][y] for y in GRID])
        def rank3(A):
            A=[a[:] for a in A];k=0
            for j in range(len(A[0])):
                pivot=next((i for i in range(k,len(A)) if A[i][j]),None)
                if pivot is None:continue
                A[k],A[pivot]=A[pivot],A[k]
                q=pow(A[k][j],-1,3)
                A[k]=[q*z%3 for z in A[k]]
                for i in range(len(A)):
                    if i!=k and A[i][j]:
                        z=A[i][j];A[i]=[(v-z*w)%3 for v,w in zip(A[i],A[k])]
                k+=1
                if k==len(A):break
            return k
        self.assertEqual(rank3(rows),len(GRID)-1)
if __name__=="__main__": unittest.main(verbosity=2)
