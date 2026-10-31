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
