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
