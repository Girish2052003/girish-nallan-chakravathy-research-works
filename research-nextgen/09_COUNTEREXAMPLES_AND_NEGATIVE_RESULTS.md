# NG-Q2 — High-width, rank-deficient, publicly recoverable family

**Status:** Explicit mathematical counterexample with proof, reproducible constructed fixtures. This is not a claim about uniform-random NCSG factors or finite-profile KEM security.

## Construction

For any integer `q>=4`, use global ternary variables `z,x_1,...,x_q`; let every edge `{i,j}` of the complete graph on `1,...,q` define a public scalar factor on scope `(z,x_i,x_j)`:

`f_ij(z,x_i,x_j)=x_i+x_j+b_ij*z^2 (mod 3)`,

where exactly one fixed edge `{1,2}` has `b_12=1`, and all other `b_ij=0`. Every local factor has 27 explicitly enumerable inputs, and there are `m=q(q-1)/2` factors.

**Relation to the SG-DIFRA source form:** In each local factor choose hidden-coordinate map
`(u_L,u_R1,u_R2)=(x_i+x_j,z,x_j)`, which is invertible. Set `A=1`, `a=(0,1)` and `Q(u_R1,u_R2)=b_ij*(u_R1)^2*u_R2`. Then `Delta_a Q=b_ij*z^2`, so the factors really are of the original `A u_L + Delta_a Q(u_R)` type, albeit **not** a draw from the original uniform potential distribution.

## Claims and proof

1. **Primal width `q`:** each factor links `z,i,j`. The union of all scopes makes all `q+1` variables mutually adjacent; the primal graph is `K_(q+1)`, treewidth exactly `q`.
2. **Global constant shift space has dimension `q`:** any shift with `h_z=0` changes each factor by the constant `h_i+h_j`. Any `h_z!=0` produces, on the exceptional edge, derivative `2*h_z*z+h_z^2+h_i+h_j`, which depends on `z` in `F_3`. Thus `D={h:h_z=0}`, of dimension `q`; quotient dimension `c=1`.
3. **Increment map is deficient:** `Gamma(h)_(ij)=h_i+h_j`. Its edge-sum matrix for complete `K_q` has rank `q` over `F_3`: if all pair sums vanish, a triangle implies every coordinate zero (as `2!=0` in `F_3`). Since `m>q`, `Gamma` is not surjective.
4. **A satisfiable target fails the old shift criterion:** let `t_(12)=1` and every other edge target be zero. The assignment `z=1,x_i=0` satisfies it. But `t-F(0)=t` is **not** in `im Gamma`: equations from edges `13,14,34` force `h_1=h_3=h_4=0`; edge `23` then forces `h_2=0`, contradicting `h_1+h_2=1`. Consequently existing Round-8 shift-only recovery reports inconclusive.
5. **The new quotient attack succeeds:** `E` can be spanned by the unit vector in the `z` coordinate. It checks at most three quotient representatives, including `z=1`, whose public evaluation already equals `t`. It recovers a valid witness and can count all witnesses exactly. For fixed local arity, the cost is polynomial in `q` despite unbounded width and deficient `Gamma`.

## Executed checks (Python 3.13.5; 31 October 2026)

`python -m unittest -v test_public_global_quotient_witness_recovery` executed three methods successfully in a local workspace.

| q | n | m | primal width | dim D | rank Gamma | c | cosets examined to witness |
| ---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 5 | 6 | 4 | 4 | 4 | 1 | 2 |
| 5 | 6 | 10 | 5 | 5 | 5 | 1 | 2 |
| 8 | 9 | 28 | 8 | 8 | 8 | 1 | 2 |
| 12 | 13 | 66 | 12 | 12 | 12 | 1 | 2 |

For these targets the quotient cardinality formula gives exactly **two** solutions, corresponding to \`z=1\` and \`z=2\`; separate brute-force checks confirm this at q=4,5,8. The q=12 case was also executed locally in a separate exact-count check. The regression additionally checks 48 randomized small public factor systems (`n=1,...,4`, 12 each), all nine scalar-pair targets per system, matching independent brute-force existence and exact solution counts. Tests include empty and unsatisfiable constant-factor cases. Randomness seed: `20261031`.

**Caveats:** Local tests used a lightweight reproduction of the existing Round-8 support module in the test directory; the committed new script imports the canonical Round-8 module. The new version on GitHub has not yet been separately run by CI. The family is deliberately constructed and NOT a break of real-size NCSG cryptography; it rebuts only the inference that high width plus a non-surjective shift map makes a problem hard.


## NG-Q3 — Random-source adversarial control (added 31 October 2026)

To test whether the one-dimensional quotient in NG-Q2 is representative, 180 small independent source-form ensembles were sampled. Every local scalar factor has the original form `f(x)=A*u_L+Delta_(1,0)Q(u_R)` on a three-input scope, with an independent uniformly sampled 3-by-3 invertible ternary `B`, uniform nonzero `A`, and independent nine-entry uniform `Q`. Scopes were either a random `n`-subset of 3-variable scopes or all 3-subsets. This is a toy diagnostic, not a calibrated instance generator for any new KEM.

| Global n | Factor count | Trials | dim D = 0 | dim D = 1 |
| ---: | ---: | ---: | ---: | ---: |
| 4 | 4 (n-factor policy) | 30 | 30 | 0 |
| 4 | 4 (all triples) | 30 | 28 | 2 |
| 5 | 5 | 30 | 27 | 3 |
| 5 | 10 (all triples) | 30 | 30 | 0 |
| 6 | 6 | 30 | 27 | 3 |
| 6 | 20 (all triples) | 30 | 30 | 0 |

**172/180** sampled systems had `D={0}`, hence quotient codimension `c=n` and **no saving** over full-space enumeration using this algorithm. Among the eight with one-dimensional `D`, two had zero increment rank. Therefore the high-width easy family NG-Q2 must **not** be generalized to the natural randomly sampled source-form ensembles without evidence. A large quotient codimension is not itself proof of hardness: other algorithms may still be efficient.

Reproduce: `python research-nextgen/experiments/random_source_shift_codimension_probe.py`. Seeds generated by `20261031 + 1000*n + 100*(policy=='all_triples') + j` with `j=0,...,29`. All sample scopes are complete public local function tables. This is computational evidence only; no asymptotic conclusion or real KEM security result follows.


## NG-Q4 — Exact random-source negative control and strengthened bound

The proof in `08_THEOREMS_AND_PROOFS.md` establishes exact local survival probability `alpha_(1,2)=5/39` for a **fixed nonzero local direction**, under uniform independent invertible coordinate masks and uniform local potential tables. For complete three-variable scopes (one independent source-form factor per triple), the exact expected number of nonzero **global** constant shifts is

`sum_(s=1)^n C(n,s)*2^s*(5/39)^(C(n,3)-C(n-s,3))`.

Because any nontrivial ternary shift subspace contains a line with **two** nonzero points, its nontriviality probability is at most **half** that expectation.

| n | m=C(n,3) | Tightened proved P(dim D>=1) upper |
| --: | --: | --: |
| 4 | 4 | 0.0181547746408921 |
| 5 | 10 | 0.0000225048374378105 |
| 6 | 20 | 0.00000000719805136645552 |
| 7 | 35 | 0.000000000000290856653378637 |
| 8 | 56 | 0.00000000000000000147605768584661 |

**Independent finite validations:** full enumeration of all `3^9=19683` scalar `Q` tables yields 2187 constant mixed derivatives parallel to `a` and 729 along an independent direction, matching `1/9` and `1/27`; independently computed operator ranks match for every nonzero direction in `d=2,3`. Exact rational first-moment calculations agree between direct global shift enumeration and closed-form weight classes for n=3,4,5. The first disconnected-scope test wrongly expected 26/3; the correct value 12 was established and the test fixed before acceptance. All 7 mathematical unit tests pass after this correction.

**Additional random controls:** new distinct deterministic seeds `20261101 + 10000*n + j`, 0<=j<trials, using the previous uniform source generator:

| n | complete triple factors | independent trials | dim D=0 | dim D>0 |
| --: | --: | --: | --: | --: |
| 4 | 4 | 500 | 491 | 9 |
| 5 | 10 | 120 | 120 | 0 |
| 6 | 20 | 60 | 60 | 0 |

All empirical observations are consistent with the **proved probability bounds**. The theorem does not prove hardness of witness recovery; it can instead indicate that **this particular shift-based shortcut disappears** under densely overlapping independent factors. Other algebraic, statistical, or general CSP solvers may still be effective. NG-Q4 does not show cryptographic security, trapdoor one-wayness or entirely new mathematical axioms.


## NG-Q6 — uniqueness does not imply private inversion

An independently planted `s` with independently sampled local B and Q has exact local nonzero-input collision probability `beta=(3^d-1)/(3^(r+d)-1)`, for r=1,d=2 exactly **4/13**. The expected additional global witnesses are the same support-hit polynomial as NG-Q4 evaluated at beta rather than alpha. For full independent three-variable scopes, the non-uniqueness probabilities are at most 0.0109351263878 at n=5 and 0.0000917201689783 at n=6. This does not prove inversion hardness.

For 30 exactly reconstructed planted samples each, brute-force enumeration found **12/30 unique** at n=4, **29/30 unique** at n=5, **30/30 unique** at n=6. Independent exact scalar-Q enumeration over 19,683 tables gave 6,561 hits for each tested nonzero mixed derivative at one point, matching exact output-uniform probability 1/3. See `experiments/planted_witness_uniqueness_bound.py` and its tests.

## NG-Q7 — public pair projection defeats dense-overlap hardness intuition

A standard polynomial-time public consistency-filtering attack, using only complete local factor tables, scopes and public targets, recovered witnesses in **29/30** complete-triple samples n=5 and **all tested** complete-triple samples n=6 through n=12. For n=6,7,8: 30/30 each; n=9,10,12: 10/10 each. Every returned witness verified. The same instances had `dim D=0` for every trial. For n=4, only 12/30 were publicly recovered by this no-branching filter, which matches the 12/30 unique fibers in this seed set.

**Critical research finding:** The disappearance of constant shifts at high overlap does **not** imply hardness, and neither does a planted unique witness. Although no generic asymptotic recovery theorem has been established, the empirical public reconstruction is a serious negative design gate for the tested distribution. Generic consistency filtering is classical prior art, not original mathematics. See `experiments/public_pair_consistency_attack.py` and `experiments/run_public_pair_consistency_campaign.py`.
