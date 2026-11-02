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


## NG-Q10 — sparse-star collapse / failed preliminary test

A proposed sparse public NCSG planted-witness family uses repeated local scopes (0,1,j). A preliminary probability-based solver was *incomplete*: a unit test found a globally unique witness although the anchor-only relation was ambiguous. Adversarial analysis found the stronger conclusion: the complete problem has primal graph width<=2 and is **deterministically publicly solvable** by enumerating all q² shared-anchor values. With q=3 it needs only nine hub guesses even for m=Theta(n) and arbitrary nonlinear/correlated public factors. No hardness or foundational originality survives. Five accepted regression tests, exhaustive brute-force cross-checks and the negative test decision in [NG-Q10](25_NGQ10_REJECTED_SPARSE_STAR.md).

## NG-Q11 — entire d=1 source family is affine; d=2 local polynomial distinguisher

For any F3 source form with d=1, `Delta_aQ` is affine (Q univariate degree<=2), hence all global factors are publicly linear equations regardless of graph width; a classical Gaussian solver returns a valid witness or correct UNSAT. Separately, with r=1,d=2 all source-form scalar factors are degree<=3; a uniform random scalar function F3^3->F3 passes this test with exact probability 1/59049. Exhaustive 19,683 potential tables found precisely 13,122 degree-3 source forms. This is **not** a complete cryptosystem distinguishing or IND-CCA attack. Seven locally passing tests are in [NG-Q11](26_NGQ11_ALGEBRAIC_DEGREE_NO_GO.md).


## NG-Q12 / NG-Q13 — new negative controls

**NG-Q12:** The allegedly private local B and Q in a complete explicit 27-entry ternary r=1,d=2 source table do not form a private coordinate representation under the exact model: an equivalent B',A',Q' is publicly reconstructible by enumerating 11232 matrices. Exactly 729 public output functions exist at fixed B,A and exactly 27 Q potentials represent each one. The uniform random membership probability has rigorous upper bound 832/387420489. **NOT** a proof of global KEM-key compromise, original IP theory or practical general-dimension polynomial-time recovery.

**NG-Q13:** Secret permutations alpha,beta,gamma in the simple abelian-group-isotope quasigroup `T=gamma^-1(alpha(x)+beta(y))` do not hide an equivalent decomposition when T's complete operation table is public. The recovered equivalent permutations publicly reproduce every entry. The non-group-isotopic Fano Steiner control shows this is **not** a tautological assertion about every Latin square: none of 49 anchor normalizations is associative. But Fano's public left/right division is still trivial. This rejects naive 'nonassociative = private trapdoor' reasoning in two complementary ways.

The new 6+6 unit tests passed; rejected candidates and failed novelty gates remain recorded for future experiments.

## NG-Q14 — noncommutativity/uniqueness do not hide group transport secrets

For public group graph labels B_uv=x_u^-1 H_uv x_v, a spanning tree reduces all vertex assignments to a public simultaneous-conjugacy constraint on one root per component. The exact number of solutions in a satisfiable connected component is its public cycle gains' common centralizer size. In S3, one transposition chord leaves 2 solutions; two noncommuting chord gains (transposition plus 3-cycle) give a **unique** planted secret, recovered **publicly**; a contradictory transposition-versus-3-cycle gives zero; flat trees leave all six gauge choices. Ten independent finite tests pass; this is known gain graph/switching mathematics.

## NG-Q15 — full symmetric groups S_k admit polynomial public recovery

For explicit permutations, simultaneous conjugacy of colored permutation actions is solved by matching action orbits and propagating generator equations, avoiding k! group enumeration. Combine with NG-Q14 spanning-tree reduction for a complete public graph witness/UNSAT algorithm polynomial in k,n,m. Tested on planted S3/S4/S8/S16/S40/S100 and inconsistent edges; 8 tests pass, including exact small-group comparisons. This does not extend to arbitrary succinct groups, noisy labels or non-symmetric-group representations. It is a **negative** result for a proposed trapdoor, not a novel universal group algorithm.


## NG-Q16 public recovery despite adversarial or random corruption

For flat public group ratios with independent erasure/replacement noise, public two-hop plurality can reconstruct all pair ratios without secret inputs. Exact sufficient adversarial condition: for every pair strictly > half of *observed* two-hop routes contain two uncorrupted edges. Full complete graph corollary: max corrupted-edge degree < (n-2)/4 per vertex. Independent noise bound `C(n,2)(|G|-1)*exp(-(n-2)*rho^4*(1-eps)^4/2)`. Complete S4 n=32 with 4 corrupted edges per vertex tested; S3 n=90 rho=1 epsilon=.36 and S4 n=90 rho=.78 epsilon=.1 were recovered in a few reproducible seeds; their finite Hoeffding bounds may still be trivial. This shows adding public noise alone does not reliably create private inversion.

**Adversarial failure control:** If an attacker forges ALL public labels to form a different perfect consistent set, a public estimator may return a self-consistent yet **false** secret-equivalent output. No algorithm can verify unknown original truth from only that fully forged data. The reference code says `self_consistent`, not `verified_planted`.

## NG-Q17 global gauge and component ambiguity

For independent uniform vertex secrets, published relative ratios `x_i^-1 x_j` are invariant under global left multiplication. The original absolute x_0 is exactly independent of any ratio-only public channel, even when every relative label can be recovered. With disconnected observation components, cross-component ratios remain uniform and unidentifiable. These facts **cannot** be advertised as quantum-hard secrecy: they are elementary model symmetry and absence of identifying data.

## NG-Q18 sparse Erdos–Rényi observation no-go

When a public graph is disconnected, relative labels across its components cannot be learned from ratio-only observations under independent uniform secrets. In G(n,p), E[#isolated]=n(1-p)^(n-1), variance from pair nonadjacency `(1-p)^(2n-3)`. Chebyshev yields a finite isolation probability lower bound; at n=200,p=.01 it is >=.95800359. This is a textbook information-theoretic obstruction at sparse densities, not a newly hard problem. 6 exact/seeded tests passed.


## NG-Q19 — noncommutative hidden matrix graph transport is publicly linearizable

Exact GL(k,F_p) vertex-transport graph equations reduce to public simultaneous matrix-intertwiner linear equations, and for p>k a publicly sampled intertwiner is invertible with high probability under the stated bound. Rejected as private trapdoor premise. A nonzero vector space of intertwiners need not contain any invertible matrix: the deliberately singular-only A=I, D=[[1,1],[0,1]] negative control must return INCONCLUSIVE, not an unsupported unsatisfiability certificate. The contradictory scalar A=I,D=2I over F5 forces T=0 and correctly certifies UNSAT. All 36 GL(2,F2) pairs were independently brute-enumerated; 12/12 local tests passed. No proof of universal small-p randomized recovery or KEM private-key extraction.
