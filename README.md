# Girish Nallan Chakravathy — Research Works

## SG-DIFRA: attack-driven post-quantum KEM research

This repository hosts the **SG-DIFRA cryptanalysis and revision project**, based on the author-supplied 26-page `SG_DIFRA_PQC_KEM.pdf` manuscript with original PDF timestamp 11 September 2026.

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

**Active direction:** NCSG-only; no ML-KEM, parallel KEM fallback, or pre-existing KEM as an ingredient. The archived MDS and noisy-linear constructs are prior iterations and must not be claimed as an original secure design.

**Scientific gate:** This is a reproducible *research draft*, not a submission-ready, formally proved or independently accredited KEM. Missing hard-distribution proofs cannot be asserted into existence.

## EUROCRYPT 2028 research target — October 2026 revision

**Research status (not a security certificate):** The *standalone* SG-DIFRA-MDS proposal has **not** been shown IND-CPA or QROM IND-CCA secure. Two central hardness assumptions (MDS-HBCE and q-ary LPN) remain unproved and without a complete classical/quantum concrete attack-cost analysis. The public NCSG fiber geometry is cryptographically redundant in the specified current label distribution; its valid NP-completeness theorems are kept and distinguished from cryptographic security.

The NCSG-only research track preserves the original theorems and attack-driven history while adding:
- [EUROCRYPT 2028 complete research-target draft](manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.md) — [PDF](manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.pdf) / [Word](manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.docx). Both binaries are generated and equation-gated in CI. This is **not** a submitted or accepted conference paper.
- [Security redesign and theorem ledger](research-2028/SECURITY_REDESIGN_AND_PROOF_LEDGER.md).
- [Exact key/ciphertext cost script](research-2028/profile_cost_audit.py); current SGD-R1/R2/R3 single ciphertexts need at least **77,414,400 / 487,710,720 / 2,786,918,400 bytes**, before framing.
- [Toy hidden-MDS subspace attack](research-2028/toy_hidden_mds_attack.py). Recovers planted positions in exhaustive small exact GF(1024) examples, **not** a real-size break.
- Automated mathematical integrity check of both Word/PDF manuscripts after build.

**Original manuscript provenance:** the author-uploaded 26-page original PDF has SHA-256 \`24461af422a6a7d1fbadcc29fe4fe372761805a846226d6d343e7180c5382f4d\`. The repository's [original extracted-text archive](archive/SG_DIFRA_PQC_KEM_ORIGINAL_EXTRACTED_TEXT.txt) preserves textual content, **not the exact binary PDF**. Do not cite it as a bit-identical source. Contributors are listed as **Girish Nallan Chakravathy and Sreedevi Kannan**, matching the uploaded original.

**EUROCRYPT 2028 schedule:** no official 2028 paper CFP/deadline has been verified as of 10 October 2026. Do not invent the date or assert submission readiness.

**Important research distinction:** algebraic identities, finite exhaustions, regression-test passes, and the statement of a conditional reduction **cannot prove** that all practical or future cryptanalytic attacks are impossible.

### Research milestones and independent validation gates

Unresolved cryptographic obligations are tracked openly as [new hardness-assumption analysis](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/1), [complete byte-level KEM and QROM audit](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/2), [ciphertext expansion redesign](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/3), [byte-exact original PDF archival](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/4), and [2028 CFP / anonymization readiness](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/5). [Original binary provenance](archive/SOURCE_ORIGINAL_BINARY_MANIFEST.md) records its exact SHA-256 and verifies that the extracted-text copy is not mislabeled as the original PDF.

### Author-directed NCSG-only reset (2026-10-10)

**Superseding instruction:** No external KEM, ML-KEM ingredient, hybrid security fallback, or borrowed code/noisy-linear construction forms the active SG-DIFRA research direction. Earlier GRS/noisy-linear work and its attacks are maintained only as historical, independently falsifiable research. The 2028 manuscript is [the active NCSG-only research draft](manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.md), with [PDF](manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.pdf) and [Word](manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.docx) generated only after scientific checks. Its unconditional results include a multi-direction ternary discrete-curl integrability theorem, a constructive recovery proof, and a public bounded-degree ideal-membership attack. Code: [integrability regression](research-2028/math/multidirection_cocycle.py) and [rank distinguisher](research-2028/attacks/public_ideal_membership_break.py). See [current security and originality status](research-2028/NCSG_ONLY_RESEARCH_STATUS.md).

**STOP gate:** There is **no** standalone NCSG-based IND-CPA/IND-CCA proved KEM here, and no justified current or replacement 128/192/256-bit security claims. The no-holes request is not mathematically certifiable. Never label the active draft 'formally verified secure' or 'conference-ready' without completing the assumptions, reduction, full reference code, independent attacks, and venue formatting. EUROCRYPT 2027's listed submission deadline was 17 September 2026; EUROCRYPT 2028 is the next research target.

The binding NCSG-only, no-reuse-of-existing-KEM design constraint and all remaining cryptographic theorem gates are tracked in [issue #6](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/6). A complete security proof is still **open**, irrespective of passing algebraic tests.

### Independent October 10 finite-difference adversarial pass

The [active manuscript](manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.md), Section 4.1, now contains a theorem absent from the original 26-page SG-DIFRA paper: **each public ternary maximum-entropy fiber splits into $3^{d-1}$ affine three-point lines**. The exact source profile geometries therefore have publicly discoverable zero-sum triples, R1 **9** per 27-point fiber, R2 **27** per 81-point fiber, R3 **81** per 243-point fiber. [Executable reproducer](research-2028/attacks/ternary_affine_line_leakage.py) checks three independently randomized bases per original profile and exhaustively checks **all 19,683** ternary scalar tables for $(d,r)=(2,1)$ under a fixed coordinate direction. This is a proved property of the author's NCSG sampler and a future design filter, **not a break of the archived GF(1024) independent dense-label ciphertext layer**.

A hypothetical ternary *affine* assignment-to-label encryption would inherit a public weight-three relation, giving a three-symbol noisy-ciphertext zero-sum event gap $2(23/32)^3/3\approx0.247538$ at error rate $3/16$. Hence simply replacing the archived independent labels by affine NCSG-dependent labels is a *provably insecure repair*. NCSG-dependence **and** absence of public linear parity relations are both necessary constraints on future proposals, not sufficient conditions for IND-CPA security.

**Current disposition:** no secure replacement algorithm has been proved, three new profile security levels cannot be claimed, and full IND-CCA/QROM verification is open. Cryptographic security and a novel trapdoor cannot be established by repetition of the audit alone. EUROCRYPT 2027's 17 September 2026 submission deadline has passed; **EUROCRYPT 2028** remains the prospective target, subject to the actual call for papers.

**Second independent exact result:** Theorem 4.2 gives a closed-form first-moment line-count distinguisher for *public NCSG fibers versus uniform same-size subsets*. The source-vs-uniform expected number of three-point affine lines is (21 vs 12.14), (66 vs 39.05), (201 vs 120.02) for R1/R2/R3 geometries. The [stdlib attack script](research-2028/attacks/ternary_affine_line_leakage.py) includes 19,683-table exhaustive checking and fixed-seed 30+30 Monte Carlo comparisons per geometry. A public fiber-ensemble distinguisher does not break the archived KEM's dense-label ciphertext, nor establish a new secure KEM. The manuscript specifies the exact scope and proofs.
