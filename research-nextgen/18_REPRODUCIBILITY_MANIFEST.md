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


## 1 November 2026: NG-Q10 / NG-Q11 code identity and combined tests

Executed on Linux Python 3.13.5 in `/mnt/data/sg_nextgen_work`. The environment's network could not resolve github.com for `git clone`; committed files were uploaded through the authenticated GitHub connector. Each returned GitHub source blob SHA was compared with the locally executed `git hash-object`:

| Exact file in research-nextgen/experiments | Identical GitHub and local blob SHA |
| --- | --- |
| `ng_q10_public_star_no_go.py` | `3dd82b72d49717d17a745d71f23d45168b012e31` |
| `test_ng_q10_public_star_no_go.py` | `e066b9770ccdbeac6b81e51d41b80b89cae958a8` |
| `ng_q11_degree_collapse.py` | `3d8abc8e8fb952215d79f182b37a152eda9b465d` |
| `test_ng_q11_degree_collapse.py` | `53d5f82c881201dc3f20db88919dd286e8732a64` |

Reproduce:

```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q8_recovery test_ng_q9_general_bound test_ng_q10_public_star_no_go test_ng_q11_degree_collapse
python ng_q10_public_star_no_go.py
python ng_q11_degree_collapse.py
```

**All 22 test methods passed locally** (6 NG-Q8 + 4 NG-Q9 + 5 NG-Q10 + 7 NG-Q11). NG-Q10 specifically compared 80 small arbitrary random *unplanted* table/target instances to exhaustive full solution enumeration and tested q=4 and deliberately contradictory cases. NG-Q11 directly enumerated all 19,683 potentials Q:F3²->F3 at B=I for exact degree-3 counts (13,122), tested random GL(3,3) masks, random d=1 scalar/vector factors and globally planted d=1 inversion.

**Preserved error trail:** Preliminary unreleased NG-Q10 bootstrap failed a global-uniqueness assertion because anchor-only ambiguity is insufficient to infer global ambiguity. We discarded the insufficient method in favor of a *complete deterministic* star solver. A preliminary NG-Q11 false-positive function used float rather than `Fraction`, causing an exact-value test failure; fixed before passing the full suite.

**No GitHub Actions CI run, proof assistant execution, public KEM or independent external review.** Old baseline artifacts beyond these four local test modules have not been completely rerun in this continuation.


## 2026-11-01 — NG-Q12/NQ-Q13 complete finite controls

New source and tests locally executed with Python 3.13.5, no third-party packages, no paid services. Final exact Git blob identities (verified with local `git hash-object` and GitHub fetched SHA):

| File under `research-nextgen/experiments/` | Executed-and-committed blob SHA |
| --- | --- |
| `ng_q12_public_coordinates.py` | `f02c2af18877832520b8e5cba14fd28b5da2d56a` |
| `test_ng_q12_public_coordinates.py` | `0c930f22ffa50cd4b1d44f5bbd1d215376e7bdb5` |
| `ng_q13_isotope_no_go.py` | `c3ddb3e6945f03d8bcc161a4f52de9567e7e9224` |
| `test_ng_q13_isotope_no_go.py` | `a48c170cadd5cda090b3e5cc9d6bec154a8c1bc5` |

```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q12_public_coordinates test_ng_q13_isotope_no_go
python ng_q12_public_coordinates.py
python ng_q13_isotope_no_go.py
```

**12/12 new tests pass**: NG-Q12 6 tests, NG-Q13 6 tests. NG-Q12 enumerates all 11232 matrices and all 19683 potential tables, checks 15 seeded hidden-coordinate public reconstructions and 12 random nonsource public tables plus edge cases. NG-Q13 checks randomized secret isotopes for m=1,2,3, public group laws, complete equivalent permutations, malformed tables, public divisions, and exhaustive 49-anchor Fano Steiner nonassociativity.

**Corrected development issue:** One initial redundant dependent-row screening condition for GL enumeration used `all` rather than `any`. The subsequent independent rank=3 filtering meant no invalid matrices or incorrect numerical results were accepted; nonetheless the condition was fixed and final tests rerun **before** commit.

**Scope:** New suites were independently executed in the current local container. The historical 22-test NG-Q8..Q11 suite is not present in this container and was **not rerun** at this checkpoint. No GitHub CI, theorem prover, human peer review, full active KEM or quantum cryptanalysis is claimed.

## NG-Q14 / NG-Q15 current local execution and GitHub source identity

Linux Python 3.13.5, pure standard library. Working files under /mnt/data/sg_research_checkpoint/experiments; authenticated GitHub connector commits only to branch research/sg-difra-nextgen-math. Each final code/test file was compared by Git blob SHA after commit and matches the locally executed version.

| File under research-nextgen/experiments | Verified Git blob SHA |
| --- | --- |
| ng_q14_nonabelian_transport.py | 426c00561012c82e9a8cb4dbe11e3a7fe894eafe |
| test_ng_q14_nonabelian_transport.py | fa3db43fb57fc09884732e518d9839a8ab7c3454 |
| ng_q15_symmetric_transport.py | 4a576e118475360a99dca16dd74331718adbf50c |
| test_ng_q15_symmetric_transport.py | a9da0c306b01c2a1e59b93746e40aab88ada9746 |

Commands from repo root:

    cd research-nextgen/experiments
    python -m unittest -v test_ng_q14_nonabelian_transport test_ng_q15_symmetric_transport
    python ng_q14_nonabelian_transport.py
    python ng_q15_symmetric_transport.py

Result: **18/18 local unittest methods passed** in 0.119 seconds in the final verified combined run, plus direct script demonstration of exactly one S3 secret and planted S3/S7/S20/S100 public recovery (seven-node demo). NG-Q14's ten tests separately completed; NG-Q15's eight tests separately completed; combined suite passed again. Independent brute-force tests enumerate small S3 secrets; larger instances verify every original public edge equation.

A two-character formatting difference in the NG-Q14 script's main-guard line was corrected in the local executed version to match the committed Git blob, and all 18 tests rerun. No mathematics or functional change. The NG-Q14 script initially committed with this harmless formatting variance, then the local test copy was synchronized and rechecked.

NO GitHub Actions/CI run, no proof assistant, no external peer review or paid API. Prior historical NG-Q8–NG-Q13 tests were **not** rerun in this checkpoint. Explicit S_k permutations are represented as k-entry vectors, so the NG-Q15 polynomial complexity refers to k and graph size, not to arbitrary cryptographic group encodings.


## NG-Q16–NG-Q18 complete standalone local execution (1 November 2026)

Environment: Linux x86_64 Python 3.13.5, standard library only; code built/executed in local working path `/mnt/data/sg_research_checkpoint/experiments`. Network DNS to GitHub was not available from the local runtime, so files were written to the pre-existing connected GitHub experimental branch using authenticated GitHub actions; **each final GitHub blob SHA was fetched and compared to the locally executed `git hash-object`**.

| File in research-nextgen/experiments | Matching GitHub/local blob SHA |
| --- | --- |
| ng_q16_robust_relative_sync.py | f1a5562a1fdbf28c0323278db76a25af05d3ac66 |
| test_ng_q16_robust_relative_sync.py | d70752a9c9794ea6fa61d908bef88dde5c54dbce |
| ng_q17_gauge_nonidentifiability.py | bfce4036ec96e9a540b5b30c69e91d61d4150347 |
| test_ng_q17_gauge_nonidentifiability.py | b9c268bc24de3cc1dbccafd615778029bddb21c4 |
| ng_q18_sparse_observation_no_go.py | 5805c9d2701f9decc85d8c7523fa0ed65a9cb857 |
| test_ng_q18_sparse_observation_no_go.py | 685cfdb448ff81688898d8955fbec3ab6710dc08 |

Reproduction from repo root:
```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q16_robust_relative_sync test_ng_q17_gauge_nonidentifiability test_ng_q18_sparse_observation_no_go
python ng_q16_robust_relative_sync.py
python ng_q17_gauge_nonidentifiability.py
python ng_q18_sparse_observation_no_go.py
```

**RESULT:** All **22/22 newly executed unit test methods PASS** in a final combined run (9 NG-Q16, 7 NG-Q17, 6 NG-Q18; ~2.75s). Exact root posterior histogram S3 is 1/6 for each of its six roots. Exact isolation numeric outputs include n=200,p=0.01 expected 27.06660098 isolated and isolation probability >=.95800359.

**NG-Q16 evidence boundaries:** six random-noise/erasure seed runs recovered all n=90 true relative pairs; their analytic Hoeffding finite-n bound often equals 1 (trivial), so their success is empirical, not a stronger formal finite result. Separate S4 n=32 adversarial corrupted-degree test meets the deterministic theorem. An explicit wholly forged, self-consistent but false public table is retained as a **negative control**—'self_consistent' must never be described as certified original secret recovery.

**NG-Q17 and NG-Q18 independent controls:** exact `Fraction` arithmetic, small complete posterior enumeration over S3 secret tuples, all eight n=3 graphs enumerated, correct p endpoints and 20 seeded G(200,0.01) graph experiments.

**External verification status:** NO GitHub Actions/CI, Lean/Rocq/Isabelle formal proof assistant, independent human peer review, production KEM build, quantum cryptanalysis or paid inference. Historical NG-Q14/Q15 tests and all earlier baseline tests were not rerun this turn; do not aggregate historical test claims as current execution.
