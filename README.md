# Girish Nallan Chakravathy — Research Works

## SG-DIFRA: attack-driven post-quantum KEM research

This repository hosts the **SG-DIFRA cryptanalysis and revision project**, based on the author-supplied 26-page `SG_DIFRA_PQC_KEM.pdf` manuscript dated October 2026.

**Security status: experimental, not independently validated.** The original manuscript proves several algebraic facts and correctness estimates. Its end-to-end IND-CPA/IND-CCA security relies on unproved distributional assumptions (MDS-HBCE and 1024-ary LPN), and its three profile estimates are not full attack-cost analyses. No finite collection of scripts establishes the absence of all cryptanalytic attacks.

The 2026-10-10 audit adds:
- an exact **cryptographic projection theorem**: the public NCSG geometry and master secret can be deleted without changing the distributions of the encryption-relevant public labels or the decryption result; this demonstrates that the NCSG component is not presently a security foundation;
- a **fixed-field scaling obstruction**: with `GF(2^10)`, the described distinct-evaluation-point GRS construction requires `M <= 1024`, so fixed finite profiles do not support an asymptotic negligible-advantage theorem;
- revised mathematical claims, separation of symbolic proofs from assumptions, executable toy attack regressions, and corrected publication-readiness terminology.

Files added in subsequent commits will be indexed here. Archive and verification materials are research artifacts, **not claims that the scheme is secure or certified**.

### Research and publication caution

The original paper lists author names. An actual double-blind conference submission, if accepted by the venue, requires an anonymized version and a check of the final call for papers. Public research repository material can affect anonymity; obtain venue-specific guidance.

**EUROCRYPT 2027:** The publicly listed submission deadline was September 17, 2026 (Anywhere on Earth); on October 10, 2026 that deadline has passed. Recheck the official conference site before planning any submission.

### Reproducibility

See `formal-verification-and-mathematical-proofs/` for claims and scripts, `manuscript/` for revised text, and `.github/workflows/` for artifact builds where available.

### File map (direct repository links)

- [Revised research manuscript source](manuscript/SG_DIFRA_REVISED.md)
- [Revised PDF](manuscript/SG_DIFRA_REVISED.pdf) and [editable Word](manuscript/SG_DIFRA_REVISED.docx) — built by [GitHub Actions](.github/workflows/build-research.yml); verify the latest successful run before treating a binary as present.
- [Original 26-page manuscript, text extraction](archive/SG_DIFRA_PQC_KEM_ORIGINAL_EXTRACTED_TEXT.txt) — for archival traceability only; mathematical typesetting may be degraded. The original uploaded PDF is authoritative.
- [Mathematical proof-status and cryptanalysis ledger](formal-verification-and-mathematical-proofs/INDEPENDENT_SECURITY_AUDIT.md)
- [Field, MDS and toy attack regression](formal-verification-and-mathematical-proofs/test_sg_difra.py)
- [Three profile correctness and specific attack arithmetic](formal-verification-and-mathematical-proofs/profile_bounds.py)

**Scientific gate:** This is a reproducible *research draft*, not a submission-ready, formally proved or independently accredited KEM. Missing hard-distribution proofs cannot be asserted into existence.

## EUROCRYPT 2028 research target — October 2026 revision

**Research status (not a security certificate):** The *standalone* SG-DIFRA-MDS proposal has **not** been shown IND-CPA or QROM IND-CCA secure. Two central hardness assumptions (MDS-HBCE and q-ary LPN) remain unproved and without a complete classical/quantum concrete attack-cost analysis. The public NCSG fiber geometry is cryptographically redundant in the specified current label distribution; its valid NP-completeness theorems are kept and distinguished from cryptographic security.

The new research track preserves the original theorems and attack-driven history while adding:
- [EUROCRYPT 2028 complete research-target draft](manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.md) — [PDF](manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.pdf) / [Word](manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.docx). Both binaries are generated and equation-gated in CI. This is **not** a submitted or accepted conference paper.
- [Security redesign and theorem ledger](research-2028/SECURITY_REDESIGN_AND_PROOF_LEDGER.md).
- [Exact key/ciphertext cost script](research-2028/profile_cost_audit.py); current SGD-R1/R2/R3 single ciphertexts need at least **77,414,400 / 487,710,720 / 2,786,918,400 bytes**, before framing.
- [Toy hidden-MDS subspace attack](research-2028/toy_hidden_mds_attack.py). Recovers planted positions in exhaustive small exact GF(1024) examples, **not** a real-size break.
- [Hybrid KDF and canonical encoding test harness](research-2028/hybrid_wireformat_and_kdf_harness.py); **not** an audited KEM implementation.
- An **optional** independently generated ML-KEM-1024 parallel ingredient under a published split-key-PRF-combiner theorem; if the standard component and combiner are secure in the same security model, it can protect the *hybrid* even if standalone SG-DIFRA is broken. It does **not** prove the new SG-DIFRA assumption or solve ciphertext expansion.
- Automated mathematical integrity check of both Word/PDF manuscripts after build.

**Original manuscript provenance:** the author-uploaded 26-page original PDF has SHA-256 \`24461af422a6a7d1fbadcc29fe4fe372761805a846226d6d343e7180c5382f4d\`. The repository's [original extracted-text archive](archive/SG_DIFRA_PQC_KEM_ORIGINAL_EXTRACTED_TEXT.txt) preserves textual content, **not the exact binary PDF**. Do not cite it as a bit-identical source. Contributors are listed as **Girish Nallan Chakravathy and Sreedevi Kannan**, matching the uploaded original.

**EUROCRYPT 2028 schedule:** no official 2028 paper CFP/deadline has been verified as of 10 October 2026. Do not invent the date or assert submission readiness.

**Important research distinction:** algebraic identities, finite exhaustions, regression-test passes, and the statement of a conditional reduction **cannot prove** that all practical or future cryptanalytic attacks are impossible.

### Research milestones and independent validation gates

Unresolved cryptographic obligations are tracked openly as [new hardness-assumption analysis](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/1), [complete byte-level KEM and QROM audit](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/2), [ciphertext expansion redesign](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/3), [byte-exact original PDF archival](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/4), and [2028 CFP / anonymization readiness](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/5). [Original binary provenance](archive/SOURCE_ORIGINAL_BINARY_MANIFEST.md) records its exact SHA-256 and verifies that the extracted-text copy is not mislabeled as the original PDF.
