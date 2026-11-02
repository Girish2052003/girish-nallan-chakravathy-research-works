# Existing research baseline (partial audit, not yet comprehensive)

Reference commit: `cc8f1831cbd5b21caa236331b40c545b88e3071d`.
Authoritative sources: root `README.md`, `MATHEMATICAL_FAMILY_AND_PROOF_STATUS.md`, `research-2028/ROUND8_FOLLOWUP_RESULTS.md`, `research-2028/ROUND8_PUBLIC_GLOBAL_CSP_SECURITY_LEDGER.md`, `research-2028/NCSG_ONLY_RESEARCH_STATUS.md`, `research-2028/SECURITY_REDESIGN_AND_PROOF_LEDGER.md`, and active `manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.md`.

| Earlier claim | Precisely recorded model | Baseline status and limitation |
| --- | --- | --- |
| Restricted NCSG-DS NP-completeness | Polynomial Boolean 3-SAT reduction | Written proof in existing source, not an average-case cryptographic hardness result |
| Original local ternary MaxEnt fiber and differential identities | Explicit finite-field source form | Written algebraic results and bounded programs, not universal KEM security |
| Theorem 4.6 public local inversion | Source-form local map, complete table | Written unconditional argument for this specified model; local trapdoor rejected |
| Theorem 4.8 public-evaluation local inversion | Source-form map and polynomial-size nonlinear right table; randomized probes | Written theorem and finite regressions, with explicit probability/error budget |
| Corollary 4.8b local-wrapper key recovery | Uniform source input, ciphertext only `f(x)`, public deterministic derivation | Scoped key-recovery obstruction, not general impossibility theorem |
| Theorem 12.9 public bounded-width solving | Explicit ternary factors and supplied low-width elimination order | Known variable-elimination method, not a novel hardness lower bound |
| Theorem 12.10 public global constant shifts | Complete tables, targets in `F(0)+im Gamma` | Public witness recovery independent of width; target outside image is inconclusive |
| Historical fixed-field hidden-GRS construction | Original GF(1024) and specified growth | Asymptotic public decapsulation obstruction; does not certify a finite-profile attack |
| New NCSG-only KEM and IND-CCA/QROM | No completed byte-exact current scheme | OPEN; no validated 128/192/256-bit instantiations |

**Classification restriction:** The statements above reflect existing written proofs and recorded tests; they have not been independently reproduced wholesale in this checkpoint and are not designated MACHINE-CHECKED. See their original documents for assumptions and attacks.

**Author provenance:** Older original work names Girish Nallan Chakravathy and Sreedevi Kannan. Preserve historical negative results; never silently import the archived hidden-MDS/noisy-linear design into a claimed standalone replacement.

**Not audited yet:** entire archive, all 15 historical program outputs and original file hashes, all manuscript claims, CI logs and worldwide literature. Thus this is an initial source-based handover, not acceptance of the entire old research as independently validated.


## 2026-11-02 focused continuation audit — verified sources and retained gaps

**This is an additional source-level check, NOT a comprehensive historical re-verification or claim that this baseline has become COMPLETE.** Read [35_MASTER_MISSION_PLAN.md](35_MASTER_MISSION_PLAN.md) and [36_STAGE_STATUS_AND_NEXT_SESSION_HANDOFF.md](36_STAGE_STATUS_AND_NEXT_SESSION_HANDOFF.md) before further work.

- GitHub repository metadata confirms default branch `main`; branch comparison at audit entry confirms `main` baseline SHA `cc8f1831cbd5b21caa236331b40c545b88e3071d`, with experimental branch then 217 commits ahead, 0 behind, 63 changed research files. Two canonical governance files have since been added to the experimental branch and must be counted in a fresh comparison.
- Main `README.md` explicitly classifies the active SG-DIFRA state as **research rather than a security-certified deployed KEM** and distinguishes archived GF(1024) code constructs from the NCSG-only mathematical research direction.
- Main `research-2028/NCSG_ONLY_RESEARCH_STATUS.md` (fetched live at blob `08ceb76fa1b88173220feba024a79d3f89263771`) lists existing scoped public CSP attacks and says **OPEN:** new full NCSG-only scheme, secret indispensability, complete correctness, classical/quantum IND-CCA, three validated security levels and practical attack study.
- Main `manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.md` (fetched live at blob `88c8a7a2d06a57c1757ed90e6d691083c50a9c44`) explicitly identifies itself as a **research draft with no validated NCSG-only KEM or security levels**, and preserves both credited author names.
- Main `archive/SOURCE_ORIGINAL_BINARY_MANIFEST.md` confirms the byte-exact author-original PDF was not previously committed by the text-only repository workflow; GitHub issue [#4](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/4) remains OPEN. No original PDF binary was silently substituted.
- Github issues [#1](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/1) through [#6](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/6) were all fetched and are **OPEN**, including full original trapdoor/KEM/IND-CCA blocker #6. These issues concern some historical NCSG-only work and must not be reinterpreted as banning the independent next-generation mathematical search.
- One inspected latest prior experimental commit had **no combined check statuses** and no **PR-associated workflow runs** surfaced by available GitHub connector endpoints. This is a limited check, not a declaration that GitHub Actions workflows never existed or that the entire repo has no CI.
- The latest research-nextgen NG-Q16/Q17/Q18 independent test suite has **24/24 current tests** (11+7+6) in documented local execution; this audit did not rerun old test suites or claim formal proof-assistant verification. Earlier erroneous 9+7+6=24 summaries have been repaired to distinguish intermediate 22/22 from final 24/24.

**Status remains PARTIAL.** To close the historical audit, systematically enumerate repository trees, archived 15-program outputs, byte-exact manuscript/binary sources, historical workflow definitions and logs, original R1/R2/R3 parameter attack evidence, all referenced claims, and independent tool-version reproducibility. Until done, never classify the full repository as independently formally audited.
