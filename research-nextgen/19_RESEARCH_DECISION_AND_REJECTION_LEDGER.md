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
