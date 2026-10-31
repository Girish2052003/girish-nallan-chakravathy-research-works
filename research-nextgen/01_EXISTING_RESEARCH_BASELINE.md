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
