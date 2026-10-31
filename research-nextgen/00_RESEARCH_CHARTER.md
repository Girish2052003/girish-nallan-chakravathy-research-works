# SG-DIFRA Next Generation — governed research checkpoint

Research baseline: `main` commit `cc8f1831cbd5b21caa236331b40c545b88e3071d` (31 October 2026).
Working branch: `research/sg-difra-nextgen-math`. Main and archived research are unchanged by this work.

**Priority:** real mathematical discovery and serious novelty/equivalence review before cryptographic design. Negative cryptanalysis is preserved. No invented KEM, bit-security level, independent peer review or proof-assistant certificate.

## Actual executed work
- Inspected authoritative README, canonical mathematical-family classification, NCSG-only status, Round-8 global attack/follow-up, security redesign ledger, and exact Theorems 4.8 and 12.10 in the active manuscript.
- Investigated established constant-difference/linear-structure literature; noted serious equivalence risk.
- Proved a *scoped mathematical extension* of the existing public-shift attack: exact quotient-space search and fiber counting for explicit ternary factor systems.
- Created a genuine high-primal-width counterexample with deficient global increment rank that the earlier shift-only test cannot solve but the quotient method can.
- Executed reproducible Python 3.13.5 finite tests (3 unittest methods, random small brute-force comparison), not a proof-assistant check or complete security test.
- Implemented and recorded code and tests in `experiments/`.

## Gates at this checkpoint
M1 (consistency): **PASS for the stated finite-field model**.
M2 (worldwide mathematical originality): **OPEN / NOT ESTABLISHED** (related linear-structure theory exists).
M3 (theorem validity): **written argument available; not externally peer reviewed**.
M4 (critical challenge): **finite counterexample and exhaustive small-domain checks completed only**.
M5 (proof assistant): **NOT EXECUTED**.
C1-C7 (new hardness, private trapdoor, KEM, cryptographic security, independent cryptanalysis, practical parameters): **NOT ESTABLISHED**.

The checkpoint does not choose a new mathematical foundation or promote an experimental KEM. Attribution to authors of previous SG-DIFRA work, Girish Nallan Chakravathy and Sreedevi Kannan, is preserved; any new work's actual authorship must be determined from contributor records rather than inferred from this document.

## Next highest-value work
(1) Seek reductions to known linear structures, group-action quotient theory and CSP decomposition;
(2) test the quotient codimension distribution for independently sampled original NCSG factors at larger public-but-feasible sizes;
(3) investigate alternative foundations, not cosmetic renaming; (4) pursue proof-assistant formalization after mathematical novelty and scope stabilize.
