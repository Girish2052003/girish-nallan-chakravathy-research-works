# Research decision and rejection ledger

2026-10-31 baseline: default main `cc8f1831cbd5b21caa236331b40c545b88e3071d`. Existing research documents a broken local trapdoor (Theorems 4.6/4.8) and public global low-width/shift attacks (12.9/12.10). Main remains unchanged.

**Decision NG-D01:** Reject interpreting constant derivative directions or their linear quotients as a newly invented mathematical structure. Prior art exists; no worldwide novelty validation. Status: **REJECTED AS FOUNDATIONAL NOVELTY**.

**Decision NG-D02:** Retain a *new scoped analytic extension* NG-Q1, exact quotient witness recovery and solution counting. Conventional proof provided. Finite checks conducted. Status: **PROVED WITHIN STATED MODEL** (written proof; unreviewed externally); formalization **OPEN**.

**Decision NG-D03:** Reject inference `large primal width + deficient global increment rank => hardness`. Constructed source-form family NG-Q2 disproves the inference; prior shift-only method returns inconclusive on a satisfiable target and quotient method recovers publicly. Status: **REFUTED as a hardness heuristic** in the stated explicit-table model.

**Decision NG-D04:** Do not promote q=4,5,8,12 toy fixtures into a real-size NCSG distribution break. Status: **EXPERIMENTALLY SUPPORTED restricted fixtures; full distribution OPEN**.

**Decision NG-D05:** Do not claim a new KEM, private trapdoor, or 128/192/256-bit security. No active candidate has met these gates. Status: **OPEN**.

**Next steps:** rigorous literature equivalence audit; test shift codimension for actual randomly sampled source-form overlaps; examine structures beyond differential CSP; prove/scope further results and introduce proof-assistant artifacts when feasible. Never discard prior attacks or change main without a defensible scientific reason.


**Decision NG-D06 (adversarial sampling control):** In 180 small sampled source-form global systems, 172 had zero nontrivial global constant-shift dimension. Consequently reject any inference that `n-dim D=O(log n)` is a generic property of uniform-source global NCSG constraints. Status: **EXPERIMENTALLY REFUTED as a universal small-sample heuristic; asymptotic random-distribution behavior OPEN**. Preserve negative result and pivot toward independent mathematical mechanisms rather than relying on quotient shifts.


**Decision NG-D07 (31 October 2026):** Retain proven model-specific result NG-Q4: a uniform source-form nonzero local shift survives with exact probability 5/39 for r=1,d=2; global independently sampled factors have an exact first moment, and dense complete triple scopes obey exponentially small (in n^2) probability upper bounds for any nontrivial global constant shift. Status: **written proof, exact finite checks; not machine-checked or independently reviewed**.

**Decision NG-D08:** Reject the proposition that rare global additive shifts establishes average-case NCSG witness hardness, quantum security or any private trapdoor. It only limits one public recovery method. Status: **UNSUPPORTED cryptographic inference**.

**Decision NG-D09:** The equivalence analysis identified already published linear-structure theorems (Charpin–Kyureghyan 2009, earlier Lai) and established first-moment methods (Achlioptas–Moore). NG-Q4 is a scoped result, **NOT** a newly established mathematical field; M2 remains open.

**Decision NG-D10:** Initial unit assertion for the disconnected-scope example expected 26/3 but the correct exact expected nonzero shift count is 12. Corrected and independently rerun before committing test. Preserve this correction as part of the proof-audit trail.


**Decision NG-D11:** NG-Q5 support-hit polynomial is a standard induced-subhypergraph edge-count enumerator after a complement reindexing. Reject as a purportedly new foundational algebra or geometry. Retain it only as a useful, explicitly reduced calculation device. Status: **MATHEMATICALLY EQUIVALENT / FOUNDATIONAL NOVELTY REJECTED**.

**Decision NG-D12:** NG-C03 nonlinear-overlap obstruction candidate is too indefinite to establish new mathematical structure. Status: **OPEN, UNSELECTED**. Do not promote or fabricate lemmas.


**NG-D13:** Retain NG-Q6 as a scoped mathematically proved planted-collision and uniqueness bound, supported by exhaustive 19,683-table local checks and finite global brute force. **Do not infer hardness or cryptographic security** from uniqueness.

**NG-D14:** NG-Q7 recovered public planted witnesses on complete-triple source-form instances despite zero nontrivial global constant shifts. **REJECT the tested dense random-overlap scheme as a currently credible private-trapdoor/hardness foundation.** This is a finite empirical attack result, not a theorem of universal polynomial recovery.

**NG-D15:** The public pair-filtering algorithm belongs to prior CSP consistency theory (Mackworth 1977); do not claim newly invented generic CSP techniques. Strong model-specific attack effectiveness may warrant publication only after rigorous prior-art comparison, reproducibility and review.

**NG-D16:** No active NCSG-only KeyGen/Encaps/Decaps, IND-CCA/QROM argument or accepted new mathematical framework exists. Retain independent mathematical discoveries and negative controls with correct attribution and leave cryptographic gates OPEN.


**NG-D17 (2026-11-01):** Accept **within model** NG-Q8 exact local projection rejection `15/52` and generic independently sampled hypergraph public one-pass recovery bound, subject to exhaustive finite-census correctness and explicit model assumptions. 624 finite direction pairs + five full potential-table checks + six local unit tests. Status: **written + computer-assisted finite enumeration; proof assistant/external peer review NOT DONE**.

**NG-D18:** Reject dense complete-triples **and** O(n^2 log n) distinct-scope anchor constructions of the independently randomized r=1,d=2 source-form model as credible hard planted-witness distributions: NG-Q8 gives polynomial-time public recovery with overwhelming probability in the specified scaling. **DO NOT** generalize to unrelated NCSG schemes, quantum models or nonexistent active KEM security.

**NG-D19:** Reject 'cohomological sheaf of overlapping NCSG fibers' as a wholly new mathematical framework absent a new invariant/theorem: published CSP presheaf/cohomological local-to-global constructions already exist (Ó Conghaile, MFCS 2022; Abramsky and Brandenburger 2011). Retain an explicit originality-equivalence record.

**NG-D20:** Earlier NG-Q7 iterative attack succeeded on small n=6/12. A new simple **one-pass** attacker may remain inconclusive on those small n despite an asymptotic recovery theorem. Preserve both data sets without falsely treating them as the same algorithm. No custom KEM, trapdoor, IND-CCA or QROM security statement is accepted.


**NG-D21 (1 November 2026):** Retain NG-Q9 as a **written, tested, scoped general fixed-arity negative theorem**: a positive local pair-exclusion lower bound exists for any fixed r,d source-form sampler with independent uniform B,Q, so sufficiently high public pair codegree yields high-probability polynomial-time witness recovery. It does **not** provide calibrated finite security estimates and does not describe all possible NCSG samplers.

**NG-D22:** Correct complete-scope corollary: k=r+d>=3 required for one *distinct* factor on every k-subset to give growing pair codegree; for k=2 one distinct factor per pair has codegree one, and repeated independent factors are needed. Preserve the negative test and correction.

**NG-D23:** Two NG-Q9 test-development defects (tuple/list concatenation and incorrectly expecting a nontrivial small-n conservative union bound) were corrected before accepting four passing tests. No false mathematical conclusion is retained. M2 novelty and C1-C7 cryptographic goals remain open.


**NG-D24 (2026-11-01):** REJECT O(n log n) repeated sparse-star NCSG as an original mathematical construction or credible hard planted-witness distribution. A preliminary test asserted recovered iff globally unique; failed because ambiguous anchor-only constraints need not imply multiple global solutions. A complete deterministic public q²-anchor conditioning solver replaces it, solving all such CSPs even with one factor per leaf and arbitrary factor tables. Novelty blocked by known bounded-treewidth algorithms (Dechter 1999). Record the failed assertion, not a retrospective clean success.

**NG-D25:** Accept the **scoped deterministic** NG-Q11 result: over F3, nonlinear-right dimension d=1 forces every source-form factor to be affine, regardless of Q,B,A; all public global instances are solvable by Gaussian elimination in polynomial time regardless of primal treewidth. **Reject d=1 as a hard witness-inversion engine.** Do not assert the recovered witness must equal the planted witness.

**NG-D26:** Retain NG-Q11 local algebraic-degree ceiling and exact r=1,d=2 local uniform-vs-source degree distinguisher (false positive 1/59049). This is an exact public local statistical distinguishability observation **only**; no IND-CCA/QROM or general d=2 inversion theorem. Origin lies in established finite-field/Reed–Muller code ideas, so **M2 still fails**.

**NG-D27:** The NG-Q10 correct solver and NG-Q11 interpolation tests added 12 local tests to the 10 previously executed tests; **22/22 combined passed** with exact GitHub source-byte identity. NG-Q11 initially used a floating point approximation in an exact rational helper, caught by a unit test and corrected; preserve as evidence of adversarial checking.


**NG-D28 (2026-11-01):** Retain exact NG-Q12 local finite-difference image/kernel counts, complete equivalent local generator scan and uniform random table union bound, with all 6 tests passed. **Reject** relying on original fixed-size 3-input hidden B,A,Q coordinates as a private local representation when the complete truth table is public. Do not infer global active KEM compromise or general polynomial-time attack in growing dimensions.

**NG-D29:** Reject NG-C11 naïve three-permutation hidden-abelian-group isotopy as a wholly new nonassociative mathematics or secret-only division trapdoor. The public Latin square yields a public normalized group law and fully equivalent α',β',γ'. Established quasigroup isotopy prior art applies.

**NG-D30:** Demand a non-group-isotopic adversarial control: the classical seven-element Fano Steiner quasigroup provably is **not** a group isotope, but public table division remains trivial. Thus non-isotopy alone is not a security proof. All 49 principal normalizations are nonassociative, independently checked.

**NG-D31:** Exact local scripts and tests have GitHub-matching source blob SHAs; 12 new tests pass. Continue searching truly new mathematical structures **without** automatically promoting familiar IP or isotopy problems into new KEM hardness assumptions. M2 and C1..C7 remain NOT ESTABLISHED.

**NG-D32 (2026-11-01):** REJECT secret-vertex nonabelian graph transport with exact public edge labels as a new private-inversion foundation. Spanning tree collapses all vertices in a component to a public simultaneous conjugator; common centralizer controls exact multiplicity. Distinct noncommuting cycle gains can create a unique secret still publicly invertible. Known gain-graph switching literature; **M2 novelty not passed**.

**NG-D33:** Reject factorial group-size arguments as a substitute for hardness when the candidate uses **explicit full S_k permutations**. NG-Q15 constructs a verified simultaneous conjugator by polynomial orbit-action matching without enumerating S_k, giving public polynomial exact graph recovery/UNSAT. Existing published symmetric-group conjugacy algorithms are credited; no novel foundational breakthrough is asserted.

**NG-D34:** Ten plus eight unit tests passed, with exact locally matched Git blob SHA. Separate S3 brute-force witness-count checks, S4 reference solver comparisons, and large S100 public reconstruction are recorded. No proof assistant or independent human review.

**NG-D35:** Do not silently relabel noisy group synchronization, unknown-edge observations, subgroup-restricted permutation problems or any compact abstract-group representation as solved by NG-Q15. They need new exact definitions, literature equivalence and adverse testing. Noise/robust synchronization already has published prior art.


**NG-D36 (2026-11-01):** Accept the rigorously scoped **negative cryptographic finding** NG-Q16: under public flat relative finite-group labels with independent per-edge noise/erasures, a simple public two-hop plurality can recover all ratios with a high-probability bound; strict honest two-hop majority suffices even against arbitrary adversarial bad values. **Reject** independent public edge corruption as a stand-alone cryptographic hardness/trapdoor argument. Existing Lerman–Shi group synchronization literature credited; no foundational novelty.

**NG-D37:** Preserve the exact **gauge ambiguity** NG-Q17. With iid uniform vertex labels and a ratio-only public channel, original root X_0 is exactly uniform conditional on any public data; a canonical gauge witness can be publicly reconstructed even though the original root is statistically unidentifiable. REJECT any inference that uniform hidden absolute gauge alone constitutes a functional public-key KEM or quantum security.

**NG-D38:** Preserve sparse G(n,p) isolated-vertex result NG-Q18, including exact E,Var and finite Chebyshev bound. At n=200 and edge observation p=.01, at least 95.8% isolation probability. This is **absence of public information**, not a new hard computational problem. Existing Erdos–Renyi and sparse group sync literature credited.

**NG-D39:** NG-Q16 test deliberately returns self-consistent but incorrect output on fully forged public labels. It must never be promoted as verified *planted* truth without theorem hypotheses. Other seed experiments use separately retained planted truth only for evaluation, not attacker input.

**NG-D40:** Six newly executed source/test files exactly match committed Git blobs. **24/24 new local test methods PASSED**. No outside formal checking, independent expert review, KEM construction, quantum hardness or globally original mathematics. Mathematical M2 still OPEN, all KEM gates NOT ESTABLISHED.


**Final testing addendum (2026-11-01):** The exact NG-Q16 S3 two-hop noise-distribution test and non-flat-H negative control passed, raising current NG-Q16 from 9 to 11 tests and current NG-Q16/17/18 combined execution from 22 to **24 passing tests**. Updated test blob SHA `830c0c9c196c901906aa6297cadd442f66cebbaf` matches local execution. No proof assistant or external review.
