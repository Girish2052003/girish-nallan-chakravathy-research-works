# Reproducibility record — NG-Q1/Q2

## Source and scope
- Upstream authoritative baseline: `main@cc8f1831cbd5b21caa236331b40c545b88e3071d`.
- Working branch: `research/sg-difra-nextgen-math`.
- New code: `research-nextgen/experiments/public_global_quotient_witness_recovery.py`.
- Independent test: `research-nextgen/experiments/test_public_global_quotient_witness_recovery.py`.
- Imported previous implementation (not copied into the branch): `research-2028/attacks/public_global_shift_witness_recovery.py`.
- GitHub new-code blob SHA after canonical-path fix: `889cb3bb8472de57f621df7bcf591149703ea28c`. GitHub test blob SHA after q=12 extension: `41c4f875284d6ba3ef3ad78374193bb6224ce272`. These are *Git blob identifiers*, not SHA-256 hashes.

## Local execution
Environment: Linux x86_64, kernel 6.18.57; Python 3.13.5 (2026-10-31). No paid services.

From the repository root, run:

```sh
cd research-nextgen/experiments
python -m unittest -v test_public_global_quotient_witness_recovery
```

The test imports the canonical prior Round-8 code by path; no installation or additional Python package is required.

Local working-directory prototype (using a small behaviorally equivalent copy of the old Round-8 support module) recorded 3 passing unittest methods. Fixed randomness seed: 20261031; 48 random small systems, each tested against all nine two-scalar targets and brute-force exact counts. High-width examples q=4,5,8 each recovered target in two quotient cosets and had `(n,m,width,dim D,rank Gamma,c)` respectively (5,6,4,4,4,1), (6,10,5,5,5,1), (9,28,8,8,8,1). Further locally checked q=12 (13 variables, 66 factors, width 12, 2 solution cosets). Separate brute-force counts at q=4,5,8 matched formula exactly (2 solutions). The original `Delta_a Q` source-form identity was independently checked on 54 scalar triples for b=0,1.

Local test code SHA-256 before the later GitHub canonical-import and q=12 adjustments: source `97d00c9d195975520076f9d0f45acadf34d2accfb811fa9b85fe1d99f8fc565e`; test `011e9b8d91a5fb69fbb1b645caee2b5a09a412da9ca48db0fae333db4636214d`. **These are historical local-prototype hashes, not hashes of final GitHub blobs.**

**CI status:** the committed GitHub version was not separately executed by GitHub Actions during this checkpoint. Do not label it CI-verified until an actual run succeeds. The mathematical family is constructed; these are not random-profile security experiments.


## Follow-up NG-Q3 negative control

Additional file: `experiments/random_source_shift_codimension_probe.py`, run locally under Python 3.13.5 with fixed generator seeds, no dependencies beyond Python standard library and the previous Round-8 public-shift module. Command from repo root: `python research-nextgen/experiments/random_source_shift_codimension_probe.py`.

Results: 180 tiny toy source-form instances, 172 with `dim D=0` and 8 with `dim D=1`. n=4,5,6; policies n factors or every triple; 30 trials each. Outcome demonstrates a **limitation** of the quotient attack rather than generic NCSG insecurity. Final GitHub code has not been rerun in CI; local source-equivalent prototype was executed. See `09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md`.


## NG-Q4 checked execution and GitHub code identity

New files: `experiments/public_global_shift_survival_bound.py` and `experiments/test_public_global_shift_survival_bound.py`.
Local execution: Linux, Python **3.13.5**; no paid tools, external cloud or APIs. Command:

```sh
cd research-nextgen/experiments
python -m unittest -v test_public_global_shift_survival_bound test_public_global_quotient_witness_recovery
python public_global_shift_survival_bound.py
```

Outcome: **7 tests passed** after correcting one initial false test expectation, in about 0.3 seconds locally. Exact local table counts: parallel **2187/19683**, independent **729/19683**; local survival alpha **5/39**. Previous quotient tests still pass. Full random-source monitoring was run from a local preexisting copy of `random_source_shift_codimension_probe.py` using `sample(n,m,seed=20261101+10000*n+j)` with (n,m,trials)=(4,4,500),(5,10,120),(6,20,60), producing nonzero-shift counts 9,0,0.

**File identity verified against GitHub connector's returned blob SHA:** local `git hash-object` equals connector blob SHA `e9bbabd1e0db7a33a79a292e7eac721d1ff78f8b` for the new mathematical script and `b1012d99d2a44e1e0444fc504ca69e6c6613167a` for the new unit test. SHA-256 of the local files respectively: `0fc6c614fdc15f3118dedab0bc5abb1de5a9f26dfce0dc1cb65839e5f1ec31a9`, `2b8422dfcbb9db5e373a9cf1b4bd26868365e61df92e470fc118fb4efdde6469`. GitHub Actions CI has not been run for this branch; **do not claim CI pass**.


## NG-Q6 / NG-Q7 exact code, environment, commands and outputs

Run from `research-nextgen/experiments` using Python 3.13.5 (tested Linux x86_64 kernel 6.18.57):

```sh
python -m unittest -v test_planted_witness_uniqueness_bound test_public_pair_consistency_attack test_public_global_shift_survival_bound test_public_global_quotient_witness_recovery
python planted_witness_uniqueness_bound.py
python run_public_pair_consistency_campaign.py
```

**14 tests passed** locally after earlier NG-Q4 test correction; five new code/script artifacts are matched byte-for-byte to GitHub via their Git blob hashes:

| File under experiments | Verified Git blob SHA |
| --- | --- |
| public_pair_consistency_attack.py | `5564d9b7ae2fd1c2eb459cb8527c4607d37aac2c` |
| test_public_pair_consistency_attack.py | `4be418d482888d1e34812d774d167b5ade233bbc` |
| planted_witness_uniqueness_bound.py | `2e06dcb876cfb119e63141e6571f89de20fe7f2e` |
| test_planted_witness_uniqueness_bound.py | `cc63524450fa15259bd9bb9473374807912c5c80` |
| run_public_pair_consistency_campaign.py | `5fa3ad6cbacb984fc7ef6fcf374d664635394995` |

**Seed policy:** local sampled public factor seed `20261110+1000*n+100*m+j`; independent planted witness seed `public_seed+123456`; `j=0,...,trials-1`. n/trials: (4,30),(5,30),(6,30),(7,30),(8,30),(9,10),(10,10),(12,10). Factor counts `m=C(n,3)`; public factor samplers come from the already committed `random_source_shift_codimension_probe.py`.

Campaign: public recoveries 12/30,29/30,30/30,30/30,30/30,10/10,10/10,10/10 in that n order; `dim D=0` on **every** sample; for n=4,5,6 fully exhaustive solution enumeration gives unique counts 12/30,29/30,30/30. SHA-256 of the locally run campaign script: `f47eb58deec69475bb9a24bad5801007272361808892d8fbe0c87c374995b849`. Other files' SHA-256 are available in locally maintained audit hashes; Git blob hashes above establish identity with checked code.

**Limits:** Neither GitHub Actions CI nor a proof assistant has executed these additions; this records direct local executions and exact source identity. No paid API, rented cloud, secret keys or external KEM were used. All source-form inputs are explicitly finite, not calibrated real-world KEM parameters.


## NG-Q8 verified local execution and exact committed source identities (2026-11-01)

Environment: `Linux 6.18.57 x86_64`, Python `3.13.5`; pure Python standard library, zero paid services. Network DNS did not allow cloning the repository inside the local execution container, so the complete **older** 14-test suite has **not** been rerun in this continuation; historical NG-Q7 results remain separately recorded as prior checkpoint evidence. The *new* NG-Q8 files were locally executed and then committed by GitHub connector, after which the server-returned blob SHA was compared to `git hash-object` on the executed bytes.

| New file | Exact Git blob SHA (local and GitHub match) | Local SHA-256 |
| --- | --- | --- |
| `experiments/ng_q8_recovery.py` | `26a8e75aeae20c44ddecc2f494a83778c0307ea4` | `487344b4ff72e3b69136931191cb5f874b84651ff46f9b9c2029fb7f28979e7b` |
| `experiments/test_ng_q8_recovery.py` | `eeb3cc35e0e7ea9335384cb37b0ee6bc39535fef` | `5f58c3b564384031221111ee449006cf2c28a55e1fda59f7fd6c0041e1eec369` |

Commands from repository root:
```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q8_recovery
python ng_q8_recovery.py
```
**Result: 6/6 new independent tests passed in ~2 seconds locally.** Exact rank/failure cases: rank1/failure0=48, rank1/failure1/3=36, rank2/failure2/9=108, rank2/failure4/9=108, rank3/failure8/27=324, for 624 independent ordered vector pairs; exact rejection 15/52. One case of each of five categories was independently validated by evaluating **all 19,683 Q tables**; independent 10,000-random-sample direct calculation agreed within 0.025 of 15/52. Additional tests verified public-only witness integrity and anchor hypergraph codegrees and a deliberately underconstrained inconclusive example.

Deterministic research-only demonstration inside `ng_q8_recovery.py`: n=6: 0/12, n=12: 0/10, n=20:1/5, n=30:2/3 **one-pass recovered**. This is deliberately distinct from earlier stronger iterative NG-Q7 success and is consistent with the high-probability theorem's coarse small-n bound.

**Proof-assistant status:** `lean`, `lake`, `coqc`, `rocq`, `z3`, `cvc5`, `sage` executable names were not found in the local PATH. NO Lean/Rocq/Isabelle checker ran. **CI status:** No new GitHub Actions workflow result obtained; passing local Python is not CI or universal formal proof.

This derivation depends on **independent uniform masks and potential tables**, complete explicitly public three-input local factor maps, independently chosen planted s, and fixed public factor scopes. It cannot be transferred silently to a redesigned secret-dependent factor sampler.


## NG-Q9 exact general arity finite checks and source identities

Source: `experiments/ng_q9_general_bound.py` (Git blob `7a371c9032a5f983a673a55af54196604ddba297`). Independent test: `experiments/test_ng_q9_general_bound.py` (Git blob `a014337d35cd5328005a59af3849821975cddb86`). Both local `git hash-object` values **matched the final GitHub fetched/updated blob SHA**.

```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q9_general_bound
python ng_q9_general_bound.py
```

**Result:** 4/4 tests passed in Python 3.13.5, Linux x86_64. Enumerates every full-row-rank r-by-(r+d) matrix for six small (r,d) pairs, all scalar Q tables for d=1,2, exact rational gamma/epsilon values, k=2 complete-scope negative control and independent repeated-pair positive control. Initial test harness list+tuple concatenation error was corrected. A later test incorrectly expected a **nontrivial conservative bound** for k=3,n=60; the bound there is actually clipped to 1, and the corrected test checks a valid larger-size analytic case. The theorem itself was restricted explicitly to k>=3 for complete unique scopes; k=2 repeated independent factors require growing codegree. No CI/proof-assistant run; no earlier full historical test rerun.
