# NG-Q1/Q4/Q6/Q7 reference programs and reproducibility

**Status:** exploratory research-only Python 3.13.5, not production cryptography or a complete KEM implementation.

## Publicly committed code

| Purpose | Exact source path below `research-nextgen/experiments` |
| --- | --- |
| Reuse Round-8 global shift algebra | `public_global_quotient_witness_recovery.py` (imports canonical older shift solver) |
| Public quotient tests | `test_public_global_quotient_witness_recovery.py` |
| Source-form sampling | `random_source_shift_codimension_probe.py` |
| Exact random shift bound | `public_global_shift_survival_bound.py` |
| Independent rank and potential-table tests | `test_public_global_shift_survival_bound.py` |
| Planted uniqueness probability | `planted_witness_uniqueness_bound.py` |
| Planted uniqueness checks | `test_planted_witness_uniqueness_bound.py` |
| Public-only pair consistency adversary | `public_pair_consistency_attack.py` |
| Public attack unit checks | `test_public_pair_consistency_attack.py` |
| Combined seeded campaign | `run_public_pair_consistency_campaign.py` |

All source-form factor tables are complete explicit ternary maps. The pair attacker receives public functions/scopes/targets, not generating hidden matrices or planted secret; it verifies any accepted witness against the full original public factor system and otherwise returns *inconclusive*.

## Local execution commands

```bash
cd research-nextgen/experiments
python -m unittest -v test_planted_witness_uniqueness_bound test_public_pair_consistency_attack test_public_global_shift_survival_bound test_public_global_quotient_witness_recovery
python public_global_shift_survival_bound.py
python planted_witness_uniqueness_bound.py
python run_public_pair_consistency_campaign.py
```

Result: **14 unittest methods passed** in the local Linux Python 3.13.5 runtime, and the complete seed-fixed campaign reproduced the recorded results. The five newly committed NG-Q6/Q7 source files were byte-matched against executed local copies by Git blob hash. See `18_REPRODUCIBILITY_MANIFEST.md` for identifiers, parameters and outputs.

**Limitations:** no CI run, no Lean/Rocq/Isabelle machine proof, no actual IND-CPA/IND-CCA KEM, no audited byte format, no quantum attack model, no constant-time or production security certification. This is mathematical experimental software, not encryption for real use.
