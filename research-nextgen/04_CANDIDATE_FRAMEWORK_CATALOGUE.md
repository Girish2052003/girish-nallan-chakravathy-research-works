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
