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
