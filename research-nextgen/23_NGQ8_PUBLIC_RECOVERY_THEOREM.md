# NG-Q8 — Proved public recovery from independent NCSG source-form ternary constraints

**Date:** 1 November 2026. **Status:** A precise, finite-enumeration-assisted mathematical argument plus direct independent exhaustive checks and public reconstruction tests. **NOT** proof-assistant-checked, externally peer-reviewed, or a universally novel mathematical framework. The theorem applies only to the exact sampler below and **does not describe an existing secure KEM**.

## 1. Exact distribution and attacker interface

Work over F3. For each *fixed, public, ordered* triple scope S=(i,j,k) of distinct global variables, independently sample

- B uniformly from GL(3,F3) by rejection;
- A uniformly from F3 nonzero;
- Q uniformly from the 3^9 scalar tables F3^2 -> F3.

Use fixed right direction a=(1,0), and define the source-form local function f(x)=A u_0+Q(u_R+a)-Q(u_R), where u=Bx and u_R=(u_1,u_2). Every local f is publicly represented by its complete 27-input truth table. Fix a planted s in F3^n **independently** of all factor randomness and publish t_S=f(s restricted to S). Distinct factors, even if they share a scope, have independent random B,A,Q. The attacker sees only public triple scopes, complete tables and t_S; not s or any B,A,Q.

This is the original small scalar NCSG source-form family, not a KEM; no encryption/decapsulation interface is assumed.

## 2. Exact local rejection lemma (NG-Q8.1)

Fix a planted local input x=(x_i,x_j,x_k), and choose any different pair values (v_i,v_j)!=(x_i,x_j). Let R be the target fiber {y in F3^3: f(y)=f(x)} and pi_ij its two-coordinate projection. Then over random B,A,Q,

**Pr[(v_i,v_j) not in pi_ij(R)] = delta = 15/52**,

equivalently the wrong pair survives with probability **p=37/52**. This probability is exact, does not depend on x or the chosen nonzero pair difference, and does not condition on an adversarially selected pair *after seeing f*.

### Detailed finite-field proof

Translation of x can be absorbed into a translated uniform Q, and A into a rescaling of the uniform first row of B. Use planted x=0, A=1. Let h be the fixed nonzero difference supported on the two tested input coordinates and e be the third coordinate's unit direction. They are independent. As B ranges uniformly over GL(3,F3), the images u=Bh and v=Be range uniformly over the **26*24=624 ordered linearly independent vector pairs** in F3^3 (each has exactly 18 completions to a full invertible 3x3 B).

For any ordered independent (u,v), a false pair survives precisely if some z in F3 satisfies f(u+zv)=f(0). For the nine independent uniformly chosen Q entries, the triple of differences

D_z=f(u+zv)-f(0), z=0,1,2

is an **affine linear image** of Q in F3^3. Write its 3x9 coefficient matrix M and affine offset b from the explicit four Q-index coefficients and the linear first-coordinate part. Every element of b+image(M) occurs with equal probability. Thus the probability of rejection is exactly the proportion of this affine image contained in (F3 nonzero)^3 = {1,2}^3.

Exhaustively evaluating the **entire set** of 624 independent (u,v) pairs yields these exact disjoint classes:

| rank(M) | Failure probability for Q | Independent (u,v) pairs |
| ---: | ---: | ---: |
| 1 | 0 | 48 |
| 1 | 1/3 | 36 |
| 2 | 2/9 | 108 |
| 2 | 4/9 | 108 |
| 3 | 8/27 | 324 |

The counts sum to 624. The exact total is

delta = (48*0 + 36*(1/3) + 108*(2/9) + 108*(4/9) + 324*(8/27)) / 624 = 180/624 = **15/52**.

**Enumerative proof boundary:** Every affine image and its probability is derived by a transparent finite-field matrix calculation; the 624-case classification is supplied as executable exhaustive rational arithmetic, **not** a published hand-derived classification table or proof-assistant-checked certificate. Five representative rank/failure classes were independently checked by brute-force enumeration of all 19,683 Q tables each, and 10,000 direct B,A,Q Monte Carlo draws agreed within expected sampling error.

## 3. General hypergraph public-recovery theorem (NG-Q8.2)

Let H be any fixed **3-uniform multihypergraph** on n>=3 public variable indices: each hyperedge corresponds to an independently sampled local source-form factor and may repeat a scope. Let d_ij be the number of factors containing both variables i and j, counting factor multiplicities.

**Public algorithm:** For each factor and its public target, list the accepted local triples; project them onto each of its three coordinate pairs. For each global pair (i,j), intersect all such projected two-coordinate relations; start with the nine F3^2 choices. If **every** global pair has exactly one surviving assignment, combine those pairs into a global candidate and verify *every original factor*. Otherwise report inconclusive, never claim unsatisfiable.

**Theorem:** The algorithm's probability of returning the planted global witness is at least

1 - min(1, 8 * sum_(1<=i<j<=n) (37/52)^(d_ij)).

When d_ij=0 the bound correctly becomes uninformative; it makes no claim of success. The algorithm uses polynomial time in the complete explicit public factor-table encoding length and n.

**Proof:** The actual planted pair survives every local projection. For any of the eight different pair assignments, an independent factor containing that pair fails to exclude it with exact probability p=37/52 by NG-Q8.1. Factors are mutually independent conditional on s, so the false pair survives all d_ij factors with probability p^(d_ij). A union bound over eight false pair assignments for every unordered global variable pair gives the displayed probability that **some** incorrect pair remains. On the complementary event, every global pair relation equals the planted pair alone, so the algorithm uniquely reconstructs s and verifies it. Explicit local arity is 3, so each factor costs at most constant-size 27-input enumeration; all intersections and final verification are polynomial. QED.

## 4. Dense complete-triple corollary (NG-Q8.3)

If H contains one independent factor for **every** triple S in C([n],3), then d_ij=n-2 and

P[public one-pass recovery fails] <= min(1,8*C(n,2)*(37/52)^(n-2)),

which tends to zero exponentially in n up to the polynomial n^2 prefactor. Public recovery therefore succeeds with probability 1-o(1) in **polynomial** explicit-input time.

Some strict finite upper bounds (not measured success rates):

| n | Upper failure bound |
| ---: | ---: |
| 20 | 1 (trivial bound) |
| 30 | 0.2530077917056873 |
| 40 | 0.015091174680777 |
| 50 | 0.000788403123930 |
| 100 | 1.29758694745292e-10 |

The bound is deliberately conservative at small n. In a separate small seeded run, the one-pass attacker recovered 0/12 at n=6, 0/10 at n=12, 1/5 at n=20, and 2/3 at n=30. This does not contradict the **previous iterative NG-Q7** attack, which performs additional consistency propagation and often succeeds at much smaller sizes. An inconclusive one-pass run is not evidence of hardness or unsatisfiability.

## 5. Sub-cubic factor-count corollary (NG-Q8.4)

A deterministic example with only O(n^2 log n) distinct public factors still admits a high-probability public attack. Pick an anchor set A of t vertices, with 1<=t<=n-2, and include exactly all triples meeting A. Its number of factors is C(n,3)-C(n-t,3) = O(t*n^2). Any non-anchor pair belongs to exactly t included triples; a pair with an anchor vertex belongs to n-2 included triples. Hence min d_ij=t.

By NG-Q8.2, recovery failure probability is at most min(1,8*C(n,2)*(37/52)^t). For desired error eta in (0,1), choose

t = ceil(ln(8*C(n,2)/eta) / ln(52/37))

when t<=n-2. For eta=n^(-constant), t=O(log n) and factor count O(n^2 log n). All the functions are still independently generated from the identical source-form sampler and publicly enumerable.

**Important:** This is only a counterexample to a claimed *hardness inference* based on dense overlap or unique planted assignments. A fixed different scope distribution, succinct function representations, correlated secret generation, larger local arity or restricted public information requires fresh proof.

## 6. Reproducibility and adversarial checks

Source: `research-nextgen/experiments/ng_q8_recovery.py`; tests: `research-nextgen/experiments/test_ng_q8_recovery.py`.

```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q8_recovery
python ng_q8_recovery.py
```

**Locally executed Python 3.13.5, Linux x86_64; 6/6 tests passed.** The committed GitHub blobs were matched byte-for-byte to the locally executed files. Direct tests cover: all 624 independent (u,v) pairs; full 19,683-table Q enumeration for five distinct affine-rank categories; 10,000 direct random B,A,Q samples; publicly verified recovery on 4/6/12/20/30-variable planted samples; incomplete-coverage inconclusive control; and deterministic anchor hypergraph codegree/size formulas.

No Lean/Rocq/Isabelle proof was executed. No GitHub Actions run was performed. No external experts validated novelty, theorem correctness or cryptographic security.

## 7. Prior art, originality and security boundary

The **algorithmic mechanism** of relational projection and consistency is established CSP mathematics: Alan K. Mackworth, *Consistency in networks of relations*, *Artificial Intelligence* 8(1), pp. 99–118, 1977, DOI 10.1016/0004-3702(77)90007-8. Additional close modern context: Arpon Basu, Jun-Ting Hsieh, Andrew D. Lin and Peter Manohar, *Solving Random Planted CSPs Below the n^(k/2) Threshold*, ICALP 2026, DOI 10.4230/LIPIcs.ICALP.2026.23. That work studies a related Boolean planted-CSP model; **its theorems have not been shown to directly apply to the present ternary finite-difference sampler**.

The exact rational constant 15/52 and codegree recovery bound may be useful *model-specific* mathematical cryptanalysis, but **full novelty has not been established**. This is not a new foundational framework, a proof that every planted CSP is easy, a trapdoor, IND-CPA/IND-CCA/QROM security, a KEM or any certified 128/192/256-bit instantiation.

**Research disposition:** NG-Q8 provides an **asymptotic public-recovery theorem for the explicitly sampled source-form global family**, stronger than prior finite tests. Reject this family as a proposed hard-witness distribution at high pair-codegree; retain negative mathematics and investigate a genuinely independent mathematical foundation.
