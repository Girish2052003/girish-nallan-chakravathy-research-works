# Proof and formal-verification status

| Item | Conventional proof | Independent finite test | Machine checked | Scope |
| --- | --- | --- | --- | --- |
| NG-Q1 exact quotient recovery and cardinality | Written in `08_THEOREMS_AND_PROOFS.md` | Random small-domain existence and count comparison | NO | Explicit local ternary tables |
| NG-Q2 high-width deficient-image family | Written in `09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md` | q=4,5,8,12 fixtures; selected exact brute-force q=4,5,8 | NO | Constructed nonuniform source-form factors |
| Existing Theorem 12.10 | Existing manuscript proof | Existing Round-8 regressions; not all independently rerun in this checkpoint | NO | Shift-only sufficient criterion |
| Post-quantum KEM security | NO | NO | NO | No complete active construction |

**Execution environment:** Lean, Lake, Rocq/Coq, Z3 and SageMath executables were not found in the available local runtime on 31 October 2026. Their absence is a tooling limitation, not a proof of falsehood or a reason to describe tests as formal verification.

**Next formal obligation:** encode the finite `F_3` version of `F(z+h)=F(z)+Gamma(h)`, direct-sum uniqueness, and the affine-fiber cardinality statement in a proof assistant. Verify exact quantified statement without replacing the original finite-table hypotheses with stronger hidden assumptions.


## NG-Q4 mathematical status

- **Conventional written proof:** NG-Q4.1 mixed-difference operator ranks, NG-Q4.2 exact local survival probability, NG-Q4.3 exact expected nonzero global shifts and half-expectation probability bound, NG-Q4.4 all-triple asymptotic bound. See `08_THEOREMS_AND_PROOFS.md`.
- **Exact finite independently implemented checks:** 19,683 potential tables; `d=2,3` operator-rank checks; rational direct-vs-weight-sum comparisons; disconnected-scope negative control. Four new unit tests pass alongside three existing quotient tests.
- **Proof assistant:** NOT EXECUTED, not machine-checked.
- **Originality:** OPEN, likely derives from established linear-structure and first-moment tools.
- **KEM security:** NOT CLAIMED.


## NG-Q6 / NG-Q7 proof status

NG-Q6 collision probability and first moment: **conventional written proof**, all 19,683 local potential tables checked for specified derivative directions, exact field/rational calculations, and full brute-force global planted fiber counts for n=4..6. No machine-checked formal theorem or external mathematical review.

NG-Q7 pair-projection filtering soundness: **conventional written invariant/termination argument**; no universal distribution-wide success guarantee. Implemented adversary and tests locally executed; 14 unit test methods (previous + new) passed. Full seeded attack campaign rerun with original public data. No Lean/Rocq/Isabelle proof, standalone KEM or quantum attack evidence.


## NG-Q8 formal-checking and finite proof-certificate boundary

Conventional argument in `23_NGQ8_PUBLIC_RECOVERY_THEOREM.md`: 624-case uniform GL(3,3) orbit reduction; exact affine-image table, model-specific local probability 15/52, independent factor probability multiplication, union bound and polynomial public one-pass reconstruction; fixed hypergraph generalization and O(n^2 log n) anchor family.

**Six new unit tests passed locally**; code/case table exact rational and independent full 19,683-Q brute checks for five cases. This is an **exhaustive finite computation plus mathematical argument**, *not* a Lean/Rocq/Isabelle checked certificate. No full human peer review or general security proof. The finite 624-case classification is a proof obligation that should be independently formalized or audited before public claims of verified originality.


## NG-Q9 formal status

Conventional written mathematical proof: exact 3-cycle count for uniform potential tables, uniform surjective-matrix counting, positive pair-exclusion event, independent-factor probability multiplication and union bound. Four new local tests passed; six low-dimensional surjective-matrix ensembles exhaustively enumerated, and d=1,2 scalar potential tables exhausted. **No proof-assistant formalization, no external expert verification.** The k=2 complete-scope edge case was identified and corrected; do not claim an n-growing complete-scope result when local arity is two.


## NG-Q10 / NG-Q11 verification

NG-Q10 complete 2-anchor star solver: conventional soundness/completeness proof, arbitrary target and table tests, unsatisfiable tests, brute-force full fiber comparisons, 5/5 new unit tests. Initial probabilistic star prototype failed the test 'recovered iff unique'; its flaw was identified and it was replaced, not quietly promoted.

NG-Q11: conventional polynomial degree proof, univariate ternary affine formula, public Gaussian solver, exact generalized Reed–Muller code-count distinguisher. Seven new unit tests pass, including 19,683 potential tables and random masked factors. An initial floating-point vs rational representation bug was corrected before acceptance.

Total of prior six NG-Q8, four NG-Q9, five NG-Q10 and seven NG-Q11 tests: **22/22 locally passed**. No complete historical repository suite, external CI, Lean/Rocq/Isabelle formal proof or peer-reviewed theorem verification was performed. Local source blob hashes match the committed GitHub files.


## NG-Q12 / NG-Q13 finite evidence and proof status — 2026-11-01

**NG-Q12:** Conventional exact proof of finite-difference image rank 6/kernel rank 3 for scalar ternary right-two-input derivative, 11232 GL(3,3) inverse-basis enumeration and complete equivalent generator recovery; 6/6 unit tests, including exhaustive all 19683 Q tables and sampled masked secret generators. No proof assistant / independent cryptanalyst.

**NG-Q13:** Conventional public group principal-isotope normalization and equivalent key reconstruction, plus conventional Fano Steiner quasigroup non-group-isotopy proof; 6/6 local tests, including all 49 Fano basepoint normalizations and full public table equality checks for generated group isotopes of sizes 3,9,27. No proof assistant / external review.

**Execution:** Combined new 12/12 tests passed on Python 3.13.5 in local container. Exact four final Git blob SHAs match locally executed bytes. Old NG-Q8..Q11 22 test methods were **not** rerun here; preserve earlier reports as historical. The new theorem names do not imply external mathematical novelty or cryptographic certification.
