# SG-DIFRA Next Generation — exploratory branch

**Baseline:** `main@cc8f1831cbd5b21caa236331b40c545b88e3071d`.

**Status at this checkpoint:** an exact public quotient attack and mathematical negative example have written proofs and local finite tests, **not** novelty certification, proof-assistant verification, an original secure mathematical foundation, or a post-quantum KEM.

## Read in order

1. [00_RESEARCH_CHARTER.md](00_RESEARCH_CHARTER.md) — priorities, checkpoint and acceptance gates.
2. [01_EXISTING_RESEARCH_BASELINE.md](01_EXISTING_RESEARCH_BASELINE.md) — partial source-verified handover and preexisting attacks.
3. [03_MATHEMATICAL_LITERATURE_REVIEW.md](03_MATHEMATICAL_LITERATURE_REVIEW.md) — narrow, openly incomplete prior-art study.
4. [05_ORIGINALITY_AND_EQUIVALENCE_AUDIT.md](05_ORIGINALITY_AND_EQUIVALENCE_AUDIT.md) — why no foundational novelty claim is warranted.
5. [08_THEOREMS_AND_PROOFS.md](08_THEOREMS_AND_PROOFS.md) — theorem NG-Q1 with full written proof.
6. [09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md](09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md) — source-form high-width counterexample NG-Q2.
7. [10_FORMAL_VERIFICATION_STATUS.md](10_FORMAL_VERIFICATION_STATUS.md) — what is and is not machine checked.
8. [18_REPRODUCIBILITY_MANIFEST.md](18_REPRODUCIBILITY_MANIFEST.md) — environment, seed and test instructions.
9. [19_RESEARCH_DECISION_AND_REJECTION_LEDGER.md](19_RESEARCH_DECISION_AND_REJECTION_LEDGER.md) — supported/refuted/open decisions.
10. [21_PUBLICATION_READINESS_AND_OPEN_PROBLEMS.md](21_PUBLICATION_READINESS_AND_OPEN_PROBLEMS.md) — scientific limitation and research continuation.
11. [22_THREE_LEVEL_EXPLANATION_AND_DEFENSE.md](22_THREE_LEVEL_EXPLANATION_AND_DEFENSE.md) — absolute beginner, university and critical defense explanations.

## Reproduce

```sh
cd research-nextgen/experiments
python -m unittest -v test_public_global_quotient_witness_recovery
```

The code reuses the original Round-8 `PublicShiftSystem` rather than copying the earlier solver into this branch. Historical SG-DIFRA files and all preexisting attack evidence are preserved on main.
