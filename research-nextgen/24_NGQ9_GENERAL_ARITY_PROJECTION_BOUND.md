# NG-Q9 — General fixed-local-arity public projection obstruction

**Status:** Detailed finite-field counting proof + finite independent tests; not proof-assistant-checked, externally reviewed, or a new mathematical framework. **This is a nonsecurity result about specified public constraint distributions, not an original KEM.** Complements the sharper r=1,d=2 exact NG-Q8 theorem.

## Exact research model

Let r,d>=1 be **fixed integers**, k=r+d. Each local public factor on a k-element scope independently chooses B uniform invertible over F3^k, A arbitrary fixed invertible r-by-r or independent invertible, and Q a uniform r-vector table F3^d -> F3^r. Fix any a!=0 in F3^d. The public function is

f(x) = A u_L + Q(u_R+a)-Q(u_R), where (u_L,u_R)=Bx.

Every public factor table is complete and explicit (3^k inputs). A global planted s is fixed independently of all factor samplers; public targets are f_i(s restricted to S_i). An attacker needs only public factors, scopes and targets, **not** the matrices, potentials or s.

## Lemma NG-Q9.1 — constant-potential derivative probability

For uniform independent Q, the event `Delta_a Q(z) = c` for **one fixed output vector c** at all z is not the relevant event; rather allow any c. Translation by a partitions F3^d into 3^(d-1) disjoint 3-cycles. One common output increment c has 3^r choices; on each cycle choose an arbitrary initial r-vector (3^r choices), and the other two values are uniquely determined. Therefore

`P[Delta_a Q is globally constant] = 3^(-r*(2*3^(d-1)-1)).`

Conditional on this event, `f` is affine, namely `f(x)=Lx+c`, with `L=A*pr_L*B` uniform among **all full-row-rank r-by-k matrices**. The sampling of L and the event on Q are independent.

## Lemma NG-Q9.2 — exact affine-map exclusion probability

Fix any two distinct input coordinate indices, a nonzero wrong pair difference h supported on these coordinates, and let T be the (k-2)-dimensional subspace of freely variable other coordinates. Under uniformly random full-row-rank `L:F3^k -> F3^r`, let

`gamma_(r,d) = P[Lh not in L(T)]`.

This has a strictly positive and exact finite formula. Put q=3, k=r+d, s=k-2, and let `N(r,s,t)` count rank-t r-by-s matrices over Fq:

`N(r,s,t) = prod_(i=0..t-1) ((q^r-q^i)*(q^s-q^i))/(q^t-q^i)`,

with N=0 outside 0<=t<=min(r,s). Let `F(r,k)=prod_(i=0..r-1)(q^k-q^i)` be the number of full-row-rank maps. Then

`gamma_(r,d) = [N(r,s,r-1)*(q^r-q^(r-1))*q^r + N(r,s,r-2)*(q^r-q^(r-2))*(q^r-q^(r-1))] / F(r,k)`.

**Proof:** Choose input coordinates `(h,e,T)`, so the two fixed-pair directions are h and a second vector e, followed by a basis for T. Write the random surjective L as columns `[u,v,C]`, C having s columns and rank t. As L is full row rank, t can only be r, r-1, or r-2. The desired exclusion is `u not in columnspace(C)`. For t=r, exclusion is impossible. If t=r-1, choose any u outside the rank-(r-1) span and any v; then L is surjective. If t=r-2, choose u outside rank t and v outside span(C,u); then L is surjective. Count C of each rank using standard rank-matrix counts and divide by total surjective L. This gives the formula and positivity (rank-(r-1) choices are feasible when d>=1). Uniform B and invertible A make L uniformly full row rank, so no orientation assumption is hidden. QED.

## Theorem NG-Q9.3 — all fixed-dimensional independently random source forms have a public high-codegree shortcut

Define the explicit positive constant

`epsilon_(r,d) = gamma_(r,d) * 3^(-r*(2*3^(d-1)-1)) > 0.`

For any fixed **k-uniform public factor multihypergraph H** of independent source-form factors, let d_ij count how many local factor scopes contain a global pair (i,j). The same one-pass projection algorithm, now projecting each local accepted k-tuple to all pairs of its coordinates, recovers the planted global s with failure probability at most

`min(1, 8 * sum_(i<j)(1-epsilon_(r,d))^d_ij)`.

**Proof:** Conditional on Q's constant-derivative event (NG-Q9.1), f is a random surjective affine L and a false pair cannot extend to a valid full local tuple if Lh is outside L(T) (NG-Q9.2). These independent events yield a **lower bound** epsilon on local false-pair rejection, hence local false-pair survival at most 1-epsilon. For different local factors, B,Q sampling is independent conditional on planted s. A fixed wrong pair survives all d_ij incident factors with probability at most (1-epsilon)^d_ij. There are exactly eight wrong F3^2 pair assignments; union bound over all pairs proves the stated failure bound. If every public pair relation is the singleton planted pair, independently reconstruct and publicly verify the global s. Full local tables have fixed constant 3^k entries, so the procedure runs in polynomial public-input time. QED.

**Complete k-uniform corollary (k>=3 only):** With one factor for every k-element global scope, `d_ij=C(n-2,k-2)`. For fixed r,d with **k=r+d>=3**, the recovery failure bound `8*C(n,2)*(1-epsilon_(r,d))^(C(n-2,k-2))` tends to zero as n grows. **Exception k=2:** One factor per pair gives `d_ij=1`, so the bound is trivial and *no high-probability recovery conclusion follows*. With k=2, a multihypergraph containing independently generated repeated constraints on every pair with multiplicity Omega(log n) can instead meet the high-codegree condition. Under these exact assumptions only, the theorem refutes planted-witness one-wayness in the high-overlap public-table ensemble; no general quantum or KEM claim follows.

## Verified finite outputs

| r | d | gamma (exact) | Lower bound epsilon (exact) |
| ---: | ---: | ---: | ---: |
| 1 | 1 | 3/4 | 1/4 |
| 1 | 2 | 3/13 | 1/1053 |
| 2 | 1 | 10/13 | 10/117 |
| 2 | 2 | 37/130 | 37/7676370 |
| 3 | 1 | 31/40 | 31/1080 |
| 1 | 3 | 3/40 | 1/1721868840 |

For (r,d)=(1,2), epsilon=1/1053 is merely a **weak universal lower bound** on rejection; NG-Q8 independently gives the **exact** and vastly stronger 15/52 for the same local sampler.

Reproducible source: `experiments/ng_q9_general_bound.py`; independent tests: `experiments/test_ng_q9_general_bound.py`. Locally executed Python 3.13.5. Three tests passed after correcting an initial list/tuple concatenation error in the test harness, with no change to the theorem or computed counts. Tests include exhaustive full-row-rank r-by-(r+d) matrices for (r,d)=(1,1),(1,2),(1,3),(2,1),(2,2),(2,3) and exhaustive scalar Q tables for d=1,2; exact rational boundary checks.

```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q9_general_bound
python ng_q9_general_bound.py
```

**Limits and status:** Numerical epsilon can be astronomically small as d grows; this does not promise practical recovery at finite parameters. It assumes independent uniform Q and B, fixed r,d, full explicit public functions, and pair codegrees scaling sufficiently fast. Correlated secret generation, succinct local maps, different arity scaling, other fields, or a future KEM need independent evaluation. The mathematics uses existing rank-counting and CSP-projection techniques; its **global originality is unresolved**. No proof assistant, external peer review, or active KEM security theorem.
