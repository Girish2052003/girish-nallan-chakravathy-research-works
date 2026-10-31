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


## New checkpoint — NG-Q4 / NG-Q5

- [Updated conventional proofs: exact random-source shift survival and hypergraph enumerator equivalence](08_THEOREMS_AND_PROOFS.md)
- [Counterexamples, 680 extra randomized controls and the stronger half-expectation bound](09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md)
- [Rejected/evaluated mathematical candidates](04_CANDIDATE_FRAMEWORK_CATALOGUE.md)
- [Deterministic exact probability calculator](experiments/public_global_shift_survival_bound.py)
- [Independent unit tests](experiments/test_public_global_shift_survival_bound.py)

```sh
cd research-nextgen/experiments
python -m unittest -v test_public_global_shift_survival_bound test_public_global_quotient_witness_recovery
python public_global_shift_survival_bound.py
```

The **locally executed files were byte-identical to the GitHub blobs** and passed seven mathematical unit tests. GitHub CI did not independently run these tests. New mathematical foundations, security assumptions, private trapdoors, KEM construction and formal proof-assistant acceptance remain OPEN.


## Further continuation — NG-Q6 and NG-Q7

The first-moment theorem NG-Q6 shows that the planted witness in the independently sampled dense source-form family is overwhelmingly likely to be **unique**. The classical public NG-Q7 pair-projection consistency attack then recovers those witnesses in every tested dense case for n>=6, despite zero global additive shift space. This is an **attack-driven negative result** about the proposed intuition 'high width + no shifts + unique secret = hardness'; it is **not** a proof that all dense NCSG samplers are easy.

**Reproduce (from this directory's experiments subfolder):**

```sh
cd research-nextgen/experiments
python -m unittest -v test_planted_witness_uniqueness_bound test_public_pair_consistency_attack test_public_global_shift_survival_bound test_public_global_quotient_witness_recovery
python planted_witness_uniqueness_bound.py
python run_public_pair_consistency_campaign.py
```

Fourteen local unittest methods pass; the 30-/10-trial attack campaign is recorded in [15_CLASSICAL_AND_QUANTUM_CRYPTANALYSIS.md](15_CLASSICAL_AND_QUANTUM_CRYPTANALYSIS.md). All five new source files have exact matching Git blob identifiers to locally run copies.

Read [11_COMPUTATIONAL_HARDNESS_ANALYSIS.md](11_COMPUTATIONAL_HARDNESS_ANALYSIS.md), [12_TRAPDOOR_INVESTIGATION.md](12_TRAPDOOR_INVESTIGATION.md), and [15_CLASSICAL_AND_QUANTUM_CRYPTANALYSIS.md](15_CLASSICAL_AND_QUANTUM_CRYPTANALYSIS.md). The mathematical proofs remain in [08_THEOREMS_AND_PROOFS.md](08_THEOREMS_AND_PROOFS.md), and the explicit negative findings in [09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md](09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md). A genuine new foundational framework and a secure private-trapdoor KEM are **NOT** established.


## End-of-execution scientific checkpoint

- [Focused source and claim inventory](02_SOURCE_AND_CLAIM_INVENTORY.md)
- [Implementation and testing](17_IMPLEMENTATION_AND_TESTING.md)
- [Internal research verdict and exact open gates](20_FINAL_INDEPENDENT_RESEARCH_VERDICT.md)

**Scientific boundary:** A mathematically correct project-specific probability bound, tested public witness attack, or likely unique planted assignment is not a novel fundamental mathematical framework and not a secure KEM. The main branch is preserved; experimental conclusions require further mathematical novelty comparison, proof-assistant work and independent cryptanalysis.
