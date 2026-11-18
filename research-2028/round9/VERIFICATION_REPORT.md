# Round 9 verification and research outcome

**Date:** 18 November 2026. **Starting main:**
`b0a4288dbb9dbffa647cc9eed973f76e640aa7f7`.

## Outcome

The [new mathematical note](CHALLENGE_COUPLED_DIFFERENTIAL_SOLVABILITY.md)
defines challenge-coupled differential solvability over F3 and gives full
written proofs of its degree classification. Linear potentials give a
polynomial-time decision problem, quadratic potentials give a coNP-complete
universal decision problem, and cubic potentials give a Pi2P-complete
universal decision problem. A single specified cubic challenge is
NP-complete. The potential and zero target are fixed; only the translation
direction varies with the public challenge.

The proof note includes explicit reductions, an exact per-challenge
response/witness bijection, a quadratic public decision algorithm and an
easy homogeneous-quadratic subclass. The [assumption ledger](ASSUMPTIONS_AND_SECURITY_BOUNDARY.md)
states which comparisons need unresolved complexity assumptions. The
[literature note](RELATED_WORK_AND_CLAIM_BOUNDARIES.md) records the closest
primary sources and leaves global priority open.

This advances the mathematical research question. It does not establish
harder ciphertext inversion, an average-case hard sampler, a private
trapdoor, a quantum lower bound or a secure KEM.

## Reproduction

Python 3.12.14 was used. The added code uses only the standard library.
From the repository root, run:

```sh
python3 research-2028/round9/verify_round9.py --legacy --output-dir /tmp/sg-difra-round9
```

The command runs the new tests and the 15 pre-existing prescribed research
programs, records per-program logs and SHA-256 source hashes, and exits
nonzero if a check fails or a hashed source changes during execution.
Omit `--legacy` to run only the new tests. The existing CI workflow now
includes this new test runner in addition to its previous checks.

The committed run is in [results.json](../evidence/round9/results.json),
with [new-test output](../evidence/round9/round9-tests.log) and all
[pre-existing-program logs](../evidence/round9/). Execution times are
metadata, not security benchmarks.

## Observed finite evidence

**21 new test methods passed: zero failures, zero errors and zero skipped
tests. All 15 existing research programs also returned exit code zero.**
The 24 recorded source hashes were stable throughout the final run.

| Independent finite check | Observed coverage |
| --- | ---: |
| All scalar affine maps on three ternary variables | 81 maps |
| All scalar quadratic maps on two ternary variables | 729 maps |
| Fixed challenges for those quadratic maps | 2,187 |
| Seeded vector quadratic maps, primal/dual/exhaustive agreement | 36 maps |
| Explicit homogeneous-quadratic midpoint witnesses | 108 |
| 3-CNF inputs compared with independent Boolean evaluation | 20 formulas |
| Ternary challenges for the 3-CNF reduction | 180 |
| Cubic circuit fixtures | 8 |
| Cubic collision sets exhaustively enumerated | 20 |
| Points examined in those cubic collision sets | 4,716 |

These counts are bounded examples, not samples supporting a cryptographic
security level. The 4,716 point visits span different fixtures and do not
mean 4,716 independent security experiments. The random fixtures use fixed
seeds for reproducibility. Expected collision sets use a separate direct
monomial evaluator and exhaustive enumeration. The UNSAT reduction is
compared to an independent Boolean clause evaluator. Cubic fixtures use
literal Boolean truth tables and enumerate every ternary basepoint.

## Proof and implementation review

The written proof received a separate agent review of its actual text.
The reviewer checked both reductions, the exact per-challenge bijection,
the polynomial bit-encoding costs, field signs, midpoint identity and
dual certificate normalization, and reported no substantive mathematical
defect. The proof author also independently checked the worked numerical
examples. This is agent-assisted review, not external peer review or a
proof-assistant certificate.

A fresh code reviewer identified two iterator handling defects:

1. Validating an iterable monomial consumed it before counting exponents,
   which could turn a monomial into a constant. The constructor now
   materializes the monomial exactly once.
2. Reusing an iterable challenge across affine probes could consume it
   after the first evaluation. The solver now normalizes it once at entry.

The review also identified Python Boolean values leaking into numeric
JSON positions. Numeric public inputs are now canonicalized to plain
integers. Three new regressions were run before these fixes and failed
for the observed reasons; all three passed after correction. The initial
18-test missing-implementation failure was also observed before the first
implementation. The final 21-test run and the full legacy run are preserved.

The mathematical input description was aligned with the implementation's
canonical term ordering and the vacuous zero-output case. Neither change
alters the reductions or their hardness classifications.

The code reviewer inspected the corrections, decision algorithms, reduction
signs, evidence runner and CI integration, and reported no remaining critical
or important implementation issue. The reviewer independently checked the
729 scalar quadratic maps from their original coefficients and a further
two-universal/two-response circuit against a Boolean oracle. Those additional
review experiments are not included in the committed runner's case totals.

One minor automated-test gap is deferred: the certificate-rejection test
does not yet contain the well-formed pair for `P=xy-s`, `c=1`, `lambda=2`,
which satisfies the normalization equation but fails polar annihilation.
The reviewer checked that the current implementation correctly rejects
this pair. Its cost if missed in a future change would be weaker automated
coverage of that rejection path, not a presently observed wrong answer.
The review did not re-audit the internals of the old research programs or
certify global priority. Root verification checks publication separately.

## Decisions and boundaries

- The existing source-local affine construction was not enlarged and
  relabeled as secure: its public-inversion theorems remain applicable.
- The new problem changes the quantifier structure to universal challenge
  coverage. This choice is explicit in the title, proofs and status files.
- A derivative-based quadratic inversion variant was considered, but its
  simple re-encoding would not establish a new cryptographic foundation.
- Publication follows the existing main-only repository instruction and
  the user's request to push. The update must preserve current main with
  a checked, non-force ref update.
- The October PDF/Word manuscripts remain historical snapshots. Round 9
  is a separately linked mathematical supplement; those binaries do not
  purport to contain the new proof text.

## Request coverage

| Requested outcome | Result |
| --- | --- |
| Open and inspect the actual SG-DIFRA repository | Done against the stated base commit and current proof/attack record. |
| Create a precise new mathematical problem | Defined in the proof note with sparse encoding and exact quantifiers. |
| Supply hardness theorems and proofs | Complete written reductions and matching upper bounds supplied. |
| State the assumptions | Explicit ledger separates unconditional classifications from conditional strict comparisons. |
| Supply computational evidence | Exact public algorithms, reduction code, 21 tests and 15 preserved-program checks supplied. |
| Prove that it is globally unprecedented | Not established; targeted primary-source search and comparison supplied. |
| Prove a stronger secure KEM or concrete post-quantum security | Not established; the changed decision problem does not imply those claims. |

The useful next mathematical step is qualified external review of the
classification and its closest equivalent formulations. The useful next
cryptographic step is a precise sampled inversion experiment with a real
private recovery mechanism. These are distinct research obligations.
