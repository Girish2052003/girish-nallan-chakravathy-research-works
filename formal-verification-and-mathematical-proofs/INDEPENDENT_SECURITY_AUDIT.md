# SG-DIFRA-MDS: independent security review and correction ledger

**Audit date:** 2026-10-10. **Source:** author's \`SG_DIFRA_PQC_KEM.pdf\`, 26 pages, §1–§18 and appendices A–B. **Reproducibility:** \`test_sg_difra.py\` and \`profile_bounds.py\` in this directory. The audit does **not** certify quantum security.

## Executive conclusion

The original manuscript has sound, independently checkable local mathematics (the Boolean 3-SAT encoding, fixed-direction finite difference entropy identity, regular fibers, and MDS row independence), but **it is not a formally verified IND-CCA KEM**. In particular, Assumptions 1 and 2 are unproved new average-case hardness assumptions; there is no concrete attack-cost certificate for the three profiles; and the fixed 1024-element field prevents the given GRS family from supporting an unbounded asymptotic parameter sequence with growing \`M\`. The presentation must not conflate an exact relation threshold with security against hidden-subspace recovery, information-set decoding or BKW.

### New finding F1 — the NCSG layer is cryptographically redundant (exact theorem)

Write \`F\` for all published supports, predicates, targets and fiber sets, \`Hflat\` for the ordered \`mB x N\` matrix after canonical bucket enumeration, \`C\` for the good group set, \`pi\` for its ordering, and \`Sigma=(sigma_i)\` for the selected points. In Algorithm 1, every fiber has size exactly \`B=3^d\`. Conditioning on **any** fixed legal \`F\`, the algorithm:
1. independently samples \`C\`, \`pi\`, a full-rank \`T\`, and random decoy rows;
2. in each good bucket places \`G_{pi(i)}T\` at a uniformly random position \`j in [B]\`;
3. fills all other positions with independent uniform nonzero labels.

These conditional laws do not depend on \`F\`. Hence, after deterministic canonical flattening,
\[
       \Pr[H_{\rm flat}=h\mid F=f]=\Pr[H_{\rm flat}=h]
       \quad\text{and}\quad I(F;H_{\rm flat})=0.
\]
The correlation between the **names** of fiber points and their row positions is a relabelling of a uniform hidden index, not a cryptographic restriction. Both \`EncBit\` and \`PKE.Enc\` read \`Hflat\` but do not evaluate \`f_i\`, \`b_i\`, or \`N(i)\`.

Furthermore define \`sigma_i = R_i s_{N(i)} + delta_i\` in \`F_3^k\`. Given any accepted secret key, construct a functionally equivalent secret key by setting \`s'=0\`, \`R_i'=I_k\`, and \`delta_i'=sigma_i\` for all \`i\`, while preserving \`C\`, \`pi\`, and the public key. Then \`R_i' s'_{N(i)} + delta_i'=sigma_i\`. **Every** decryption decision, for **every** ciphertext, is exactly identical. Thus \`s\` is an independently masked secret used only to re-address random hidden positions: the public NCSG geometry plays no role in the actual ciphertext-security problem.

**Consequence (mandatory correction):** The paper may legitimately present a mathematically interesting NCSG-indexed *implementation* of a hidden-MDS-label scheme, but it cannot claim that NCSG worst-case hardness protects this KEM. To obtain a genuinely NCSG-based KEM one must first design a nontrivial, provably or plausibly hard *average-case coupling* between \`F\` and \`Hflat\`; doing so invalidates the independence theorem and requires a **new** attack analysis. No such coupling is established in the supplied manuscript. The reduction below therefore retains only the accurately supported label-distribution claim.

### New finding F2 — the asymptotic security claim is not instantiated

The public GRS matrix in Eq. (9) requires distinct \`alpha_1,...,alpha_M\` in \`K=GF(2^10)\`; thus
\[
                              M\le |K|=1024.
\]
For the specific ordinary GRS definition used by the paper, there is **no** infinite sequence of increasing lengths \`M(lambda)\` in this *fixed* field. Three fixed, finite profiles with nominal \`lambda=128,192,256\` are not themselves a family supporting \`negl(lambda)\` and unrestricted QPT asymptotic security. If an asymptotic formulation is desired, define \`K_lambda=GF(2^{h(lambda)})\`, specify irreducible moduli and algorithms for every \`lambda\`, guarantee \`2^{h(lambda)}>=M(lambda)\`, constrain key/ciphertext size and key generation to polynomials, and restate both hardness assumptions uniformly over that family. **Simply increasing the field size does not prove either assumption.**

### New finding F3 — original "formally verified" and QROM wording overstates the evidence

- Equation (19), \`(13/16)^(-N)\`, is the work of **one particular random clean-information-set attack**, not a lower bound on random-linear-code decoding.
- The dual-distance statement \`d_perp=u+1\` is an unconditional property of the planted GRS rows, but says nothing about general polynomial/algebraic, correlation, or subspace attacks on the full public distribution.
- \`MDS-HBCE\` (paper's Assumption 1) and \`q-ary LPN\` (Assumption 2) have not been reduced to a recognized established lattice or code assumption. They are independent open hardness hypotheses.
- Theorem 10 is a **conditional hybrid implication**, given properly formulated experiments and reductions; it is not a proof that either premise is true.
- Theorem 11 invokes external QROM FO/MRE hypotheses without defining a concrete simulator, experiment, oracle query limits, or complete advantage inequality. The wording "IND-CCA secure" must remain explicitly **conditional** and no finite profile can be called a verified security level.
- The one-bit decapsulation error bound is an analytically reproducible binomial bound, not a bit-for-bit implementation correctness proof or a side-channel guarantee.

### New finding F4 — missing reference implementation / ambiguity

The paper specifies an abstract \`XOF\` and independent random oracles but lacks reference KEM code exercising full serialization, GRS decoding, deterministically re-encrypted invalid ciphertexts, fault cases and side-channel behavior. In a QROM claim, oracle modelling and domain-separation correctness cannot be delegated to the phrase "assume transform hypotheses" while also claiming a finished proof. Key generation creates large, variable-size public predicates and labels; full byte-level resource bounds must be checked. No full production implementation was supplied for audit.

## Scope ledger: what remains valid

| Source claim | Assessment | Permitted final wording |
|---|---|---|
| Theorem 1: balanced local Boolean 3-SAT encoding | Exact algebraic reduction; truth-table reproducible | Proven worst-case NP-completeness under stated encoding |
| Theorems 3–6: table representation, regular fibers, derivative image | Linear algebra; automated small-fixture regressions | Proven mathematical identities |
| Theorem 7: \`I(s;pk)=0\` | Exact, but also demonstrates \`s\` is unnecessary to encryption security | Proven independence **not** a hiding argument for planted MDS labels |
| Lemma 1, Theorem 8: planted linear independence through \`u\` | Exact over a full-rank embedding, verified on reduced fixture | Exact dual distance \`u+1\`; no claim about all attacks |
| Theorem 9: mixed accidental dependencies | Union bound only; denominator and coefficient count check necessary for each profile | Statistical upper bound, not computational security |
| Eqs. (15)–(17): correctness tails | Numerical recomputation on original parameters | Finite analytic error upper bounds |
| Theorem 10: one-bit hybrid | Conditional on both indistinguishability games | Conditional CPA reduction, not verified hardness |
| Theorem 11: QROM CCA | Not fully instantiated | Unproved end-to-end security conditional on external theorem hypotheses |
| SGD-R1 / SGD-R2 / SGD-R3 | Named research configurations only | No 128/192/256-bit security certification |

## Compact attack-and-repair trace

**Original Boolean period.** In characteristic two the finite difference has a period: \`Delta_a Q(x+a)=Delta_a Q(x)\`. One-hot labels turn two period pairs into a public weight-four relation. **Repair already in source:** odd-characteristic predicates and dense labels.

**Original planted-fiber bias.** Public-fiber coordinate marginals correlate with a shared planted global secret. **Repair already in source:** sample the entire public NCSG layer independently of the master secret before selecting incidence.

**First secret-incidence low-noise binary break.** A selected full-rank public basis contains no errors with constant probability for \`nu=0.001\`; Gaussian elimination recovers encryption randomness and eventually FO messages. **Repair already in source:** symbol error \`3/16\` and a hidden MDS decoder. **Residual risk:** this fixes *that attack* only, not all q-ary LPN algorithms.

**Short binary hidden-code dependencies.** Dual weights about 5–11 gave cheap relation search. **Repair already in source:** GRS planted dual distance \`u+1\` (65,97,129). **Residual risk:** high-order relation searches, subspace recovery, code equivalence and ciphertext-side algorithms still unassessed.

**New F1 redundancy.** Public NCSG data are independent of flat code-label distribution. **Honest correction:** separate the mathematical NCSG results from the independently-assumed encryption-security engine; do not present the former as a security reduction. **There is no proof-preserving patch that makes NCSG essential without changing the scheme.**

**New F2 finite-field cap.** \`M<=1024\` contradicts taking growing GRS lengths with fixed K. **Proposed repair direction:** parameterize \`h(lambda)\`, supply a complete uniform sampler and rework all assumptions; the fixed SGD-R1/R2/R3 arithmetic remains unchanged.

## Three profile specifications reconstructed from the original source

| Field | SGD-R1 | SGD-R2 | SGD-R3 |
|---|---:|---:|---:|
| nominal lambda | 128 | 192 | 256 |
| (n,k,d,r) | (64,5,3,2) | (96,7,4,3) | (128,9,5,4) |
| m,M,u,N | 1024,256,64,640 | 1536,384,96,960 | 2048,512,128,1280 |
| B=3^d | 27 | 81 | 243 |
| q=mB | 27648 | 124416 | 497664 |
| GRS planted relation girth | 65 | 97 | 129 |
| exact noise rate | 3/16 | 3/16 | 3/16 |
| repetitions | 7 | 7 | 7 |
| FO message length | 320 | 448 | 640 |
| fallback secret bits | 384 | 576 | 768 |
| random-basis clean attack log2 work | 191.72 | 287.58 | 383.44 |
| upper bound on log2 full-message failure | -148.32 | -219.82 | -290.98 |

**Important:** these are reproduced **source** quantities and bounded quantities, not cryptographic-security estimates. Long-term key material and serialization may consume far more space than the cited ciphertext estimates once public predicate tables and explicit encodings are accounted for.

## What can be formally shown, and what cannot

The local field, code, and distribution statements can be verified mathematically and regression-tested. A Python regression supplies explicit finite checks, but no test suite can quantify over all PPT/QPT adversaries. The missing proofs for MDS-HBCE and q-ary LPN cannot be silently replaced with "secure" parameter labels. The remaining task is cryptanalysis and/or a security reduction to an established assumption, with independent peer review.

## Publication integrity

EUROCRYPT 2027 paper submission was publicly listed as **September 17, 2026**, which is already past as of this audit. The original 26-page PDF contains author names; a blind submission must be separately prepared under the correct venue policy. Publishing research drafts to a public repository can affect anonymity. Confirm the organizer's current policy rather than asserting a submission is ready. Reference: https://eurocrypt.iacr.org/2027/ and public deadline trackers; no claim of an official extension.

## Reproduction instructions

\`python formal-verification-and-mathematical-proofs/test_sg_difra.py\`
\`python formal-verification-and-mathematical-proofs/profile_bounds.py\`

**Reproducibility status:** independent tests of algebraic facts and small-fixture attacks. Not a complete implementation, formal protocol verification, independent cryptanalysis, or QROM theorem proof.
