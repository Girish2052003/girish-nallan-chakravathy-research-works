# Round 9: challenge-coupled differential solvability

Date: 18 November 2026. Base: `b0a4288dbb9dbffa647cc9eed973f76e640aa7f7`.

## Intent and scope

The user requested a computationally harder, novel SG-DIFRA mathematical
problem, with proofs, assumptions and a repository update. The deliverable
is a precise new research formulation and verified reduction implementations.
Global priority, average-case hardness, concrete cryptographic strength and
a secure KEM are not established by this work.

For a succinct vector polynomial over F3, ask whether every direction
`h(c)=(1,c,0)` has a zero finite difference at some point. All directions
refer to the same public potential and the same zero target. The witness
may depend on the challenge. This changes the decision task from one
existential solution to universal challenge coverage; it does not increase
the security of the old KEM by assertion.

## Approaches considered

1. Larger old affine-source maps: rejected because the repository already
   proves public constant-shift inversion for their specified regime.
2. Ternary derivatives of succinct cubic potentials as inversion problems:
   these include a restricted quadratic-system representation; simply
   relabeling them would not establish a new hardness foundation.
3. Challenge-coupled coverage with a degree classification: selected here
   because complete reductions, easy boundaries and a falsifiable claim
   can be supplied. The degree classification is a project contribution
   pending independent proof review and a fuller priority search.

## Specification

- Explicit variable list `(s,x_1,...,x_r,y_1,...,y_t)`; no exponentially
  large dimensions represented merely by a short binary integer.
- Sparse reduced polynomials over F3; maximum total degree 1, 2 or 3.
- Decision: `for every c in F3^r, some w has P(w+h(c))=P(w)`.
- Linear case: exact public coefficient test.
- Quadratic case: solve an affine system for each fixed challenge;
  provide both challenge enumeration and dual-output enumeration.
- Quadratic lower bound: an explicit linear-size reduction from 3-CNF
  UNSAT using a recurrence for false-literal products, without a truth
  table or a secret input to the solver.
- Cubic lower bound: an explicit linear-size reduction from Boolean
  `forall u exists v C(u,v)=1`, with a pinning gadget, the surjective
  lift `u_i=c_i^2`, Boolean constraints and quadratic gate residuals.
- Explain the exact bijection between accepting Boolean responses and
  cubic collision witnesses. A fixed cubic challenge remains NP-complete.
- Establish the homogeneous-quadratic easy case and the output-parameter
  algorithm; no exponential lower bound or quantum security is claimed.

## Implementation plan

Execution uses this fresh local clone. The repository explicitly requires
publication on `main`; no additional official branch is created. The
user's current instruction already authorizes research and push. Remote
publication must be non-force, checked against current main, preserving
unrelated changes.

### 1. Mathematical specification and independent review

- [x] Write `CHALLENGE_COUPLED_DIFFERENTIAL_SOLVABILITY.md` with complete
  reductions, degree/size accounting, assumptions and tractability cases.
- [x] Have an independent reviewer check quantifiers, signs, field
  identities, reduction directions and the exact strength of every claim.
- [x] Write `RELATED_WORK_AND_CLAIM_BOUNDARIES.md` using primary sources.

### 2. Executable reductions and decision algorithms

- [x] Write tests first in `test_differential_challenges.py`, observe the
  expected missing-implementation failure, then implement
  `differential_challenges.py` using only the Python standard library.
- [x] Verify finite differences and Gaussian solutions against direct
  enumeration, including inconsistent and zero-dimensional systems.
- [x] Compare all 729 scalar quadratic maps on two ternary variables
  against exhaustive collision search; compare seeded vector maps too.
- [x] Compare the UNSAT reduction to an independent Boolean evaluator,
  including an empty formula, tautologies and contradictions.
- [x] Exhaust small cubic fibers to check the response bijection and
  challenge-dependent witnesses; reject malformed circuit inputs.
- [x] Verify independently checkable `(challenge, dual multiplier)` NO
  certificates and reject altered certificates.

### 3. Evidence, integration and publication

- [x] Save deterministic finite evidence with input/source hashes and
  exact commands; label it as finite testing, not a universal proof.
- [x] Add the new checks to CI; update README, canonical proof status,
  continuation state and the research index without removing old attacks.
- [x] Run the existing prescribed research programs and the new checks;
  preserve complete results and resolve meaningful failures.
- [x] Obtain a fresh implementation review, apply substantive fixes,
  and inspect the full diff.
- Publication: push to main without force, then read the remote commit;
  the verified commit URL is reported with the delivered result.
- Delivery: report exact links, proof status, testing scope and remaining
  limitations alongside the verified remote commit.

## Review focus

1. `forall c exists w` must never silently become `exists w forall c`.
2. The ternary-to-Boolean square map is onto but not one-to-one; witness
   multiplicity is asserted only for each fixed ternary challenge.
3. A dual quadratic certificate uses midpoint centering and normalized
   `lambda dot L(h)=1`, including the sign over F3.
4. Sparse degree and polynomial input size must be maintained throughout
   both reductions; no hidden full table is permitted.
5. Worst-case universal verification hardness must not be described as
   planted average-case inversion hardness, quantum hardness or KEM security.

## Progress

This plan records scope and implementation choices. Completed evidence and
review findings will be recorded in `VERIFICATION_REPORT.md`.
