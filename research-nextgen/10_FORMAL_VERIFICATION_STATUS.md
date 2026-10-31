# Proof and formal-verification status

| Item | Conventional proof | Independent finite test | Machine checked | Scope |
| --- | --- | --- | --- | --- |
| NG-Q1 exact quotient recovery and cardinality | Written in `08_THEOREMS_AND_PROOFS.md` | Random small-domain existence and count comparison | NO | Explicit local ternary tables |
| NG-Q2 high-width deficient-image family | Written in `09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md` | q=4,5,8,12 fixtures; selected exact brute-force q=4,5,8 | NO | Constructed nonuniform source-form factors |
| Existing Theorem 12.10 | Existing manuscript proof | Existing Round-8 regressions; not all independently rerun in this checkpoint | NO | Shift-only sufficient criterion |
| Post-quantum KEM security | NO | NO | NO | No complete active construction |

**Execution environment:** Lean, Lake, Rocq/Coq, Z3 and SageMath executables were not found in the available local runtime on 31 October 2026. Their absence is a tooling limitation, not a proof of falsehood or a reason to describe tests as formal verification.

**Next formal obligation:** encode the finite `F_3` version of `F(z+h)=F(z)+Gamma(h)`, direct-sum uniqueness, and the affine-fiber cardinality statement in a proof assistant. Verify exact quantified statement without replacing the original finite-table hypotheses with stronger hidden assumptions.
