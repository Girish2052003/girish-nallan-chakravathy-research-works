# Initial originality and equivalence gate — candidate NG-Q

**Decision: FAIL as a newly established foundational mathematical framework; retain as a project-specific adversarial extension.**

## Known antecedents
- Constant-derivative/linear structures of finite-field functions are established mathematics. The set `D` is not novel by renaming it a quotient-shift space.
- Direct-sum complements, linear quotients, group-action orbits, rank-nullity, affine cosets, and Gaussian elimination are standard.
- Existing SG-DIFRA Theorem 12.10 already constructs `D`, `Gamma`, and a public shift-only inversion procedure.
- Classical CSP literature contains symmetry-based search reduction and width-based variable elimination. Precise equivalence to published quotient-symmetry algorithms has not been comprehensively checked.

## What this checkpoint actually adds
The scoped contribution is an **explicit complete public quotient search for the exact earlier model**, including a uniform fiber-cardinality formula, plus a constructed family of genuine source-form overlapping factors with: unbounded primal width, non-surjective `Gamma`, and polynomial public recovery. Written proof and bounded tests accompany the claim. These are genuine findings **within the stated model**, but their global mathematical novelty is unknown; a knowledgeable reviewer may regard them as immediate consequences of established group-action symmetry reduction.

## Originality gate
- Precise definitions: YES.
- Nontrivial finite/infinite family: YES.
- Substantial entirely new theory beyond antecedents: **NOT ESTABLISHED**.
- Conventional proof and finite counterexample search: YES for NG-Q1/Q2.
- Lean/Rocq/Isabelle proof: NO.
- Meaningful prior-art comparison: INITIAL ONLY.
- Worldwide novelty certification/external review: NO.

**No mathematical migration is recommended.** Continue independent framework exploration and prior-art review. Even a novel impossibility example would not itself provide a private trapdoor or secure KEM.


## NG-Q4 audit

The source-form probability calculation, exact global first moment, and dense-overlap bound are mathematically justified in their specified distribution. **However, the proof method uses standard linear structures, elementary translation-operator rank, the first-moment method, and a union bound**. Charpin–Kyureghyan (2009), Definition 1 and Proposition 1, explicitly establish the linear-structure concept; random-CSP first moments predate this project (Achlioptas–Moore). The project-specific probability formula is not certified novel. This result **passes a scoped mathematical-consistency and conventional proof test**, but **does not pass M2 originality for a new framework**.

A proposed name such as a new 'NCSG shift-survival geometry' would be cosmetic; none is adopted. Complete prior-art comparison, independent external mathematical review and proof-assistant formalization remain open.


## NG-Q6 / NG-Q7 prior art boundaries

NG-Q6's probability is model-specific, but the global bound is a standard first-moment/union-bound calculation. NG-Q7 is an explicit classical CSP-consistency adversary, with antecedents including Alan K. Mackworth (1977). The NCSG-specific experimental successes are valid findings about a precise distribution, **not** invention of generic pair consistency, or original private-trapdoor mathematics. New foundational originality M2 **still does not pass**.


## NG-Q8 / NG-C05 novelty boundary

The model-specific exact probability **15/52** and pair-codegree recovery bound now have a full transparent finite-enumeration argument and conventional global proof. The generic local consistency/projection method is established CSP mathematics, not new research machinery (Mackworth, *Artificial Intelligence*, 1977, DOI 10.1016/0004-3702(77)90007-8). Modern *planted CSP recovery* literature is also active (Basu, Hsieh, Lin and Manohar, ICALP 2026, DOI 10.4230/LIPIcs.ICALP.2026.23); that work's Boolean planting assumptions have **not** been proved identical to this ternary NCSG sampler.

A proposed new 'nonlinear cohomological compatibility geometry' is **not** foundationally original just by treating overlapping relation-fibers as local sections: Abramsky and Brandenburger (2011) studied global-section obstructions, and Ó Conghaile (MFCS 2022, DOI 10.4230/LIPIcs.MFCS.2022.75) explicitly applied presheaves/cohomology to CSP local-to-global consistency. NG-C05 therefore **fails the novelty gate** without new non-reducible mathematics. M2 remains OPEN / NOT ESTABLISHED.


## NG-Q9 novelty assessment

The general fixed-arity pair-exclusion bound uses standard matrix-rank counts, an elementary constant-derivative subdistribution, known public local relation projections and a union bound. Its formalized model-specific conclusion may be a useful negative cryptanalytic extension of SG-DIFRA, but the **mathematical tools and broad algorithmic approach are not original**. No claim of a wholly new algebra, category, hardness assumption or globally novel theorem without comprehensive literature comparison. M2 remains NOT PASSED.


## NG-Q10 / NG-Q11 originality audit

NG-Q10's sparse-star exact solver is **mathematically redundant** with 1999 and earlier bucket elimination / conditioning methods and bounded-treewidth CSP algorithms. The proposed O(n log n) probabilistic recovery and novelty claim were weaker than a deterministic public linear-time method for fixed alphabet; reject.

NG-Q11's bound on algebraic degree and public Gaussian solver at d=1 are elementary consequences of finite-field interpolation, finite differences and Gaussian elimination. Its degree<=3 scalar distinguisher is a direct generalized Reed–Muller code membership test. The particular source-form application and exact counts are useful technical evidence, but not a new foundational algebra or globally originality-certified cryptanalysis. Formal M2 novelty gate **still NOT PASSED**.
