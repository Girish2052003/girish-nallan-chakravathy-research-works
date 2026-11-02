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

## NG-Q14 / NG-Q15 validation status — 2026-11-01

NG-Q14: conventional proof of spanning-tree exact reconstruction, reduction to simultaneous cycle conjugacy, common-centralizer exact witness count, and product across graph components. Ten Python regression methods passed, including independent brute-force enumeration for small S3 graphs and random S4 controls.

NG-Q15: conventional constructive polynomial-time orbit-action conjugacy solver proof for full explicit S_k, exact graph witness verification and UNSAT rejection; eight regression methods passed, including all 36 S3 single-pair cases, 300 two-generator tuple cases, 120 random planted S3/S4 graph instances compared with independent NG-Q14 solver, and k=100 planted exact recovery.

**18/18 new local tests passed** and final four new source/test Git blob hashes match execution. No Lean/Rocq/Isabelle proof assistant, independent external researcher review, KEM security game, or GitHub Actions CI was run. Full historical 34 test suite not rerun; do not count prior tests as newly executed.


## NG-Q16–NG-Q18 verified execution vs mathematical proof status (1 November 2026)

**Conventional proof only** (no formal proof assistant):
- NG-Q16 public two-hop plurality correctness under strict honest-majority, complete-graph adversarial corrupted-degree sufficient condition; independent uniform replacement/erasure path difference expectation rho²(1-epsilon)² and Hoeffding+union bound; conservative group-size-independent clean-majority alternative.
- NG-Q17 exact group gauge-independence via uniform-prior bijection and per-component relative ambiguity. Exact rational posterior checks.
- NG-Q18 exact G(n,p) isolation first/second moments and Chebyshev lower bound; textbook low-density asymptotics.

**Python 3.13.5 local execution — INTERMEDIATE then FINAL:** Initially 9 NG-Q16 + 7 NG-Q17 + 6 NG-Q18 = **22/22** test methods passed. Two later adversarial NG-Q16 tests increased that suite to 11, so **FINAL 11 + 7 + 6 = 24/24 passed**. The intermediate count must never be mislabeled as 24. Six source/test Git blobs matched byte-for-byte to the locally executed files. Prior 18 NG-Q14/Q15 tests were **not** rerun in this container; no claim of overall historical 176-commit regression coverage. No GitHub Actions CI, Lean/Rocq/Isabelle verification, external peer-review, quantum-model attack or completed KEM. Controlled finite experiments are not machine-checked universal proofs.


**Final NG-Q16 correction (same date):** Two additional local adversarial tests proved the exact rational S3 random-replacement mixing probabilities and demonstrated a zero-noise non-flat transport counterexample. NG-Q16 now has 11 tests; NG-Q17 has 7 and NG-Q18 has 6, **24/24 total**. The updated NG-Q16 test blob is `830c0c9c196c901906aa6297cadd442f66cebbaf` and matches the locally executed bytes. Earlier 22-test counts were intermediate checkpoints, not final counts.


## NG-Q19 (2026-11-02): written proof, independent finite checks; NO machine proof

Conventional finite-field algebra: graph tree telescoping to simultaneous conjugacy; linear public intertwiner-space computation; p>k Schwartz–Zippel determinant nonzero polynomial theorem; public verifier soundness and explicitly inconclusive status when only singular samples are found. Twelve new local Python 3.13.5 test methods passed, including exhaustive GL(2,F2) finite decisions and all 625 matrices over F5 at dimension 2. Both new Github source/test Git blob hashes match locally executed source: b1635b98795f544da2652669b0f383c1c1e256bd / 8d8bc8335e3265989ffd39b3bf94a7109ee428e9.

**No Lean/Rocq/Isabelle theorem has been checked.** Trial-division prime checking in the reference code is NOT polynomial in log p; the abstract public algebraic recovery bound assumes a validated prime field. No external reviewer, combined regression-suite run or KEM formal proof was performed. M5 not passed; no final selected-mathematical-framework theorem.
