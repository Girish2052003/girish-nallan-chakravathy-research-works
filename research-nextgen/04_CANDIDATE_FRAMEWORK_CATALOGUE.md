# Candidate framework catalogue — no promoted new mathematical discipline

Baseline: `main@cc8f1831cbd5b21caa236331b40c545b88e3071d`. All candidates evaluated without predetermined mathematical winner. Neither mathematical novelty nor a secure KEM follows from naming a candidate.

## NG-C01 — Additive public quotient search
**Objects:** finite-field map `F: F_3^n -> F_3^R` formed by public overlapping factors; constant-derivative subspace `D`, increment map `Gamma`, quotient `F_3^n / D`.
**Operations:** shift by `D`, form affine fiber orbits, enumerate complement representatives.
**Theorems:** NG-Q1 exact witness recovery and cardinality, NG-Q2 constructed high-width deficient-increment counterexample.
**Model:** precise, nontrivial finite and unbounded examples; finite checks and written proof.
**Originality gate:** **REJECT AS NEW FOUNDATION**. This is additive linear-structure mathematics plus standard quotient/Gaussian elimination. Charpin–Kyureghyan (2009) already formalized linear structures, and the original SG-DIFRA Round 8 already calculated `D`. A scoped attack may remain publishable only after further novelty review. **No secret trapdoor**.

## NG-C02 — Hypergraph shift-survival enumerator
**Objects:** a finite hypergraph `H=(V,E)`, with `|V|=n` and `m` (possibly repeated/multiset) factor scopes. For a subset `S⊆V`, let `hit_H(S)` count edges intersecting `S`, respecting multiplicities. Define the exact polynomial

`P_H(z) = sum_(nonempty S⊆V) 2^|S| z^(hit_H(S))`.

Each exponent counts local factor restrictions that receive a nonzero input shift. Coefficients are nonnegative integers; relabeling vertices leaves the polynomial invariant. For independently randomized r,d source-form factors, NG-Q4 gives `E[|D|-1]=P_H(alpha_(r,d))`, hence `P[dim D>=1]<=min(1,P_H(alpha_(r,d))/2)`.

**Explicit equivalence obstruction:** Let `E[T]` be the multiset of hyperedges fully contained in `T⊆V`. Substitute `T=V\S` to obtain exactly

`P_H(z) = sum_(T⊆V) 2^(n-|T|) z^(m-|E[T]|) - 1.`

Thus `P_H` is an elementary specialization/reindexing of a **standard induced-subhypergraph edge-count enumerator**, not evidence of a new mathematical universe. Its definition and useful interpretation do not establish originality.

**Tiny example:** one 3-variable factor on four global variables has `P_H(z)=2+78z`: the two nonzero shifts of the one isolated variable touch no factor, and the remaining 78 nonzero shifts touch the single factor. At `z=5/39`, `P_H(z)=12`, matching the exact disconnected-scope regression.

**Status:** mathematically well-defined; exact equivalence displayed; **REJECT AS ORIGINAL FOUNDATIONAL FRAMEWORK**. May retain as a convenient attack-screening summary only with attribution to earlier graph-polynomial methods. Not a hardness assumption.

## NG-C03 — Nonlinear overlap obstructions (exploratory, unselected)
**Provisional research question:** Can local-to-global compatibility of nonlinear finite-field constraints yield an invariant **not equivalent** to standard CSP propagation, finite-field cochains, sheaf/cohomology of constraints, group actions, or algebraic elimination?
**Status:** No precise unique new axioms, provably distinctive invariant, nontrivial original theorem, or private trapdoor established. **OPEN RESEARCH QUESTION, NOT AN ACCEPTED CANDIDATE**. Do not invent a brand or claim novelty.

## Actual conclusion
NG-Q4 bounds the survival of **one already-known public structural shortcut** on a specified distribution. Under dense independent source factors its absence is overwhelmingly likely. This does **not** imply the remaining constraint problem is computationally hard.

**Official mathematical migration:** NOT AUTHORIZED BY SCIENTIFIC EVIDENCE. Continue testing genuinely distinct structure candidates, rejecting known reparameterizations and preserving negative results.


## NG-C04 — Dense independently randomized planted NCSG hardness

**Definition:** complete-three-variable public source-form factors with independent uniform GL(3,3) coordinate masks, independent scalar potential tables, and a fixed planted global witness generating all public factor targets.

**Mathematical attributes:** NG-Q4 shows global additive shift shortcuts vanish at high density; NG-Q6 shows the planted solution is likely unique at high density. Both results have conventional proofs.

**Adversarial outcome:** NG-Q7, a public known-CSP consistency method, recovered a complete global witness without secret generation information in every tested n>=6 complete-triple instance. The constructed test cases all had zero nonzero global constant-shift dimension. This demonstrates that absence of these shifts and near-uniqueness do not establish cryptographic hardness.

**Decision:** REJECT **as a positively justified KEM hardness foundation** at this checkpoint. A universal asymptotic public-recovery theorem has not been proved, and other sampling variants remain open. This candidate is not genuinely new mathematical structure.


## NG-C05 — cohomological local-to-global constraint framework (equivalence gate)

Natural objects are public local solution relations R_S on overlapping scopes S; restrictions map assignments on larger scopes to smaller scopes. Compatible global witnesses are precisely **global sections** of the resulting presheaf of local assignments. This is **not a novel foundational definition** merely because the underlying local predicates are nonlinear finite-field differences. Closely matching established work includes Abramsky–Brandenburger's sheaf-theoretic local/global contextuality treatment (2011), and Adam Ó Conghaile, *Cohomology in Constraint Satisfaction and Structure Isomorphism*, MFCS 2022, DOI 10.4230/LIPIcs.MFCS.2022.75, which explicitly represents CSPs through presheaf global sections and develops cohomological refinements of k-consistency.

**Gate decision:** **REJECT the basic local-section/sheaf/cohomology rebranding as a new mathematical framework.** Genuine novelty would require a distinct invariant/theorem beyond those established constructions, with fully evaluated counterexamples and prior-art comparisons. No cryptographic trapdoor was found by simply using this representation.

## NG-C06 — dense/high-codegree NCSG-source planted hardness

NG-Q8 supplies a mathematically scoped **polynomial-time public recovery theorem** under exactly the independently random r=1,d=2 source-form sampler. Public pair constraints with codegrees at least logarithmic in n admit a vanishing recovery failure bound. This rejects the proposed dense and anchor-source planting distributions as defensible **asymptotically hard planted-witness problems**. It is neither a proof that every alternative NCSG family is easy nor a new algebraic foundation.


## NG-C07 — enlarged uniform-source local arity as a hardness repair

NG-Q9 gives an explicit **positive** public pair-exclusion probability for any fixed r,d>=1 in the independent uniform source-form family over F3. For sufficiently large pair codegrees, this alone yields polynomial public planted-witness recovery with high probability. Thus changing local dimension from (1,2) to another **fixed** pair (r,d) is not, by itself, a justified repair for the same high-overlap secret-witness hardness model. The probability constant may become astronomically weak and does not refute concrete finite profiles or distributions with correlated/hidden representations. **Decision:** reject fixed-dimension increase alone as a proven cryptographic security foundation; no new mathematical framework selected.


## NG-C08 — sparse star with shared public anchors — REJECTED

The proposed O(n log n) planted NCSG sparse construction on repeated scopes (0,1,j) has constant separator size **two** and primal graph treewidth <=2. A complete deterministic public solver enumerates 3^2=9 anchor assignments then solves every leaf independently, even with **one** constraint per leaf, arbitrary nonlinear factor tables or arbitrary target values. No random planting, collision probability or private information is needed. This is standard bounded-treewidth CSP mathematics (Dechter 1999); **reject as original foundation or hard-witness distribution**. The failed preliminary anchor-only-sufficiency test and corrected complete solver are preserved in NG-Q10.

## NG-C09 — finite-difference degree collapse — mathematically valid, not new foundational algebra

All ternary source-form factors `f(x)=A uL+Delta_a Q(uR)` have algebraic degree <=max(1,2d-1), for any B invertible. If d=1 they are affine, so every public global factor system is solved by Gaussian elimination, independent of graph width. If r=1,d=2 they are local degree<=3 functions; a uniform random F3^3 scalar function has this degree with probability exactly 1/59049, yielding a public distinguisher but no d=2 KEM break. This is a direct use of **known affine-invariant finite-field polynomial/Reed–Muller theory**, not a novel mathematical foundation. **Reject d=1 as proposed hard-witness family; retain d>=2 distinguishability as scoped structural evidence.**


## NG-C10 — hidden NCSG local generator coordinates (REJECT as private local secret)

When local r=1,d=2 scalar factors and all 27 values are public, NG-Q12 recovers an equivalent (B,A,Q) representation by 11232 finite matrix candidates, verifying all 27 inputs. The finite difference has image dimension 6/kernel dimension 3 for fixed B,A. **No secret generator advantage** can be assumed from the mere obfuscation of a fixed-size local B or Q. Asymptotic public-key secrecy and global KEM keys were not modeled, so do not extrapolate beyond this exact local attack.

## NG-C11 — hidden abelian group by secret quasigroup isotopy (REJECT as new foundation)

For T(x,y)=gamma^-1(alpha(x)+beta(y)) over F3^m with publicly complete Latin-square table, NG-Q13 reconstructs an equivalent group law, group coordinates, and full equivalent (alpha',beta',gamma') from public data. Hidden permutations and apparent nonassociativity add **no novel algebraic structure**; group isotopy is established prior art. A legitimate non-group-isotopic control (seven-element Fano Steiner quasigroup) was constructed and proven non-isotopic to Z7, but its public quasigroup divisions are still trivial. Thus **non-isotopy is only a classification boundary, not a cryptographic hardness proof.**

**Selection verdict:** Neither candidate becomes the SG-DIFRA NEXT GENERATION mathematical foundation. Continue searching structures with independently stated, non-reducible invariants and computational questions. Prioritize mathematical counterexamples over new branding.

## NG-C12 — public nonabelian graph transport — REJECTED

Proposed asymptotic objects: a public graph with secret group vertices x_v and PUBLIC exact relations B_uv = x_u^-1 H_uv x_v. NG-Q14 proves all vertex secrets on one component reduce to a single public simultaneous conjugator t for cycle gains, with solution count given by the common centralizer. A planted hidden assignment can be unique while still publicly recoverable.

For explicit full symmetric groups S_k, NG-Q15 proves complete polynomial public decision and witness construction using colored permutation-action orbit propagation, independent of k! group enumeration. This includes high-degree S100 test instances. No claim about arbitrary succinct groups or noisy-edge hardness follows.

This proposal is an instance of classical gain-graph switching and simultaneous permutation conjugacy, not a novel mathematical framework or private trapdoor. Reject and preserve full proofs and tests.


## NG-C13 — independent noisy/erased public flat group ratios (REJECT as a novel private inversion engine)

Proposed alteration of NG-Q14: reveal `Y_ij` as independently observed (probability rho) and independently uniformly corrupted (probability epsilon) versions of relative group ratios `R_ij=x_i^-1 x_j`. **This is a standard group synchronization statistical model**, not a new mathematical framework. NG-Q16 demonstrates an explicit public polynomial-time two-hop recovery algorithm and sound deterministic/independent-noise sufficient conditions: `Pr[any wrong/tied pair] <= C(n,2)(|G|-1)e^{-(n-2)rho^4(1-epsilon)^4/2}`, clipped to one. In full observed graphs, less than (n-2)/4 adversarial corrupted-edge degree per vertex is sufficient for honest two-hop majority. The probabilistic theorem is not automatically a useful finite-size guarantee at every rho/epsilon/n.

**NG-C14 — hidden absolute group gauge (REJECT as computational cryptographic security).** NG-Q17 proves exact posterior uniformity of the absolute X_0 under independent uniformly random group secrets and ratio-only observations. This is an unavoidable global symmetry (or per-component symmetry if disconnected), not an actual *secret-only computational trapdoor*. A public adversary can simultaneously learn all relative ratios while the arbitrary original gauge remains information-theoretically unidentifiable. Neither side gets key agreement for free merely by naming the gauge 'secret'.

**NG-C15 — sparse observation graph (REJECT absent-information-as-hardness claim).** If public observation graph G(n,p) has isolated vertices or multiple connected components, many intercomponent relative ratios are inherently unidentifiable for uniform independent secrets. NG-Q18 gives exact mean/variance and isolation lower bound: n=200, p=.01 implies isolation probability at least .9580. Sparse absence of information is **not** a new NP-hard inversion problem or valid KEM security assumption.

These are three distinct scientifically tested outcomes of the same known group-synchronization family, not a genuinely new foundational mathematical proposal. No KEM accepted.


## NG-C16 — hidden general-linear-group graph transports — REJECTED

Candidate objects: arbitrary graphs, secret vertex X_v in GL(k,F_p), public invertible labels H_e and B_e=X_u^(-1)H_e X_v. Fundamental cycle equations A_e T=T D_e are **linear** in the k² unknown entries of one root T. A publicly computed intertwiner space contains a valid planted root. For p>k, uniformly random public linear-combination matrices are invertible with probability >=1-k/p, producing a full valid public vertex assignment with per-component failure <=(k/p)^N after N independent samples.

Source/proof/tests: [37_NGQ19_MATRIX_TRANSPORT_LINEARIZATION.md](37_NGQ19_MATRIX_TRANSPORT_LINEARIZATION.md), [implementation](experiments/ng_q19_matrix_transport.py), [12 independent passing tests](experiments/test_ng_q19_matrix_transport.py). Published 1997 module-isomorphism methods are direct prior art. For p<=k, this bounded-sampling code DOES NOT prove an efficient solver; inconclusive does not mean unsatisfiable.

**Reject as original foundation M2 and private inversion C3**, preserve negative mathematics. No surviving new framework, no new original KEM and no gate transition.
