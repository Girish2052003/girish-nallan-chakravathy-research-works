# SG-DIFRA security redesign, October 2026 — EUROCRYPT 2028 research track

**Status: security not established for the standalone SG-DIFRA KEM.** This is a proof/attack ledger, not a deployment certification. All claims below are either proved mathematical lemmas, reproducible finite calculations, conditional reductions, or explicitly open questions. Do not promote the profiles to 128/192/256-bit security ratings.

## Source provenance and author preservation

The immutable author-supplied source file was \`SG_DIFRA_PQC_KEM.pdf\` (26 pages, date embedded by pdfTeX 2026-09-11), by **Girish Nallan Chakravathy and Sreedevi Kannan**. SHA-256 of exact original PDF bytes:

\`24461af422a6a7d1fbadcc29fe4fe372761805a846226d6d343e7180c5382f4d\`

The existing \`archive/SG_DIFRA_PQC_KEM_ORIGINAL_EXTRACTED_TEXT.txt\` records the entire extracted text but is **not** the actual PDF, and is not typesetting-equivalent. The exact binary original is kept as a verified author-upload in the working session; do not claim that the GitHub text archive reproduces it byte-for-byte.

The paper's original exact finite-difference/NCSG mathematics, its prior negative attacks, GRS framing and the original three research parameter sets are preserved in the text, and are **not** attributed to lattice KEM mathematics. ML-KEM is discussed only as an **optional, explicitly separate hedge**, not as the invention or hardness source of SG-DIFRA.

## Valid exact results

**Lemma G (geometry projection).** Conditioned on a legal public NCSG fiber collection \`F\`, all fibers have identical cardinality \`B=3^d\`; each good position \`sigma_i\` is selected uniformly and decoy labels are sampled independently. After canonical flattening, the label distribution \`H_flat\` does not depend on \`F\`. The published NCSG supports/tables have mutual information zero with \`H_flat\` despite being publicly named. Proof: the conditional distribution of the position of each planted row is uniform on \`[B]\` for every \`F\`; decoy-row and planted-row laws are independent of the names of these positions. Thus \`P(H_flat=h|F=f)=P(H_flat=h)\` for all legal \`f\`.

**Lemma S (master secret elimination).** Given the secret key and its selected positions \`sigma_i=R_i s_N+delta_i\`, put \`s'=0\`, \`R_i'=I\`, \`delta_i'=sigma_i\`. The new key decrypts every possible ciphertext identically: it selects precisely the same coordinates, uses the same secret good set/permutation, and runs the same decoder. Hence the NCSG master secret \`s\` is *not* essential to encryption security; the real secret is the hidden planted row indexing. This does not imply that hidden indexing is cryptographically hard.

**Lemma M (MDS relation threshold).** Given pairwise distinct GRS evaluation points and full row rank \`T\`, every subset of at most \`u\` planted rows is linearly independent, and the first all-planted linear dependence has \`u+1\` rows. This only bounds *one attack shape*.

**Lemma C (idealized correctness).** With exact independently sampled 3/16 symbol errors, the bit-zero decoding failure is bounded by \`P(Bin(M,3/16)>floor((M-u)/2))\`. The bit-one false-accept probability is bounded by a union of radius-\`t\` balls around \`Q^u\` GRS codewords. Repeated-bit majority gives a finite probability bound. This does not assert a tested constant-time GRS decoder.

## Quantified major efficiency defect

With \`q=m3^d\`, \`N\` field coordinates per public row, \`ell\` message bits and \`T_rep=7\`, the **absolute packing lower bounds** (excluding metadata, per-bucket NCSG data, tags, alignment, hashes, and packet framing) are:

| Original research profile | \`q\` | Public label matrix \`q*N*10/8\` bytes | Ciphertext \`q*ell*7*10/8\` bytes |
|---|---:|---:|---:|
| SGD-R1 | 27,648 | 22,118,400 (21.09 MiB) | 77,414,400 (73.83 MiB) |
| SGD-R2 | 124,416 | 149,299,200 (142.38 MiB) | 487,710,720 (465.12 MiB) |
| SGD-R3 | 497,664 | 796,262,400 (759.38 MiB) | 2,786,918,400 (2,657.81 MiB) |

These are exact lower bounds from the *current design*. Neither stronger assumptions nor a KEM combiner repairs the extreme ciphertext expansion. A compactness redesign would have to replace bitwise full-length ciphertexts by a new code/noise mechanism and **restart** correctness and cryptanalysis. Publishing the original parameters as a practical KEM would be misleading.

## Attack surface still unclosed

- **Average-case hidden planted MDS subset recovery:** broad subspace/robust subspace clustering attacks, projected code Schur-square distinguishers, support recovery, GRS filtration/code equivalence, quantum subset search. Theorem M does not bound these.
- **q-ary noisy linear equations:** rank-based partial decoding, nearest-codeword/ISD, BKW-type elimination, Fourier bias, algebraic methods, quantum noisy-inference algorithms, attacks amortized across many ciphertexts sharing \`H\`.
- **CCA leakage:** malformed ciphertext paths, decoder success/failure/timing, secret-dependent evaluation counts, re-encryption errors, ciphertext length acceptance, parser equivalence; no audited constant-time reference implementation presently exists.
- **Multi-user/security-model issues:** key-dependent/random-oracle games, adversarially correlated public keys, strong versus weak ciphertext robustness, implicit-rejection behavior, uniform random coins, actual resource-bounded QROM reduction.
- **Efficiency failure:** the measured multi-GB ciphertext bound for SGD-R3.
- **Asymptotic theorem gap:** fixed \`GF(2^10)\` caps distinct public GRS evaluation points at 1024. The separate family construction below repairs **syntax/correctness only**.

No legitimate scientific statement can prove absence of every future classical or quantum cryptanalytic algorithm.

## Recommended protection — optional ML-KEM-1024 parallel hybrid

**Hybrid construction specification (not original SG-DIFRA):**

1. \`Hybrid.Gen\`: independently generate \`(ek_S,dk_S)\` for SG-DIFRA and \`(ek_M,dk_M)\` for ML-KEM-1024. Serialize with fixed version and explicit checked lengths.
2. \`Hybrid.Encap\`: obtain \`(ct_S,ss_S) <- SG.Enca(ek_S)\` and \`(ct_M,ss_M) <- MLKEM.Enca(ek_M)\` with **independent fresh randomness**; form \`ct = encode(ct_S,ct_M)\`.
3. Compute \`K = W(ss_M,ss_S; encode(ek_M,ek_S,ct_M,ct_S,version,context))\`, where \`W\` is a **specified and verified split-key-PRF combiner core** in the security model.
4. \`Hybrid.Decap\`: canonically parse both ciphertexts, execute both component decaps according to their defined failure semantics, and derive \`K\` using the identical \`W\` input order and context.

**Conditional theorem H.** Under the published Giacon–Heuer–Poettering hypotheses (independent ingredient key generation, correctly implemented component KEM semantics and an appropriate split-key PRF core), a parallel combiner remains IND-CCA secure if at least one ingredient is IND-CCA secure in the same model, subject to reduction loss. If ML-KEM-1024 remains IND-CCA secure against the considered QPT adversaries and the core meets the **quantum** split-key condition, the *hybrid* can be protected despite failure of standalone SG-DIFRA. Proof: application of an existing generic combiner theorem, **not** a new result about SG-DIFRA's hardness.

NIST SP 800-227 (September 2025) provides KEM combiner guidance and treats additional public-key/ciphertext binding. The July 2026 CFRG hybrid-KEM Internet-Draft discusses \`UniversalCombiner\` with both secrets, public keys and ciphertexts. For the final protocol, adopt a *specific* fully encoded standardized/peer-reviewed instantiation, and test reduction assumptions before claiming anything formal. A simple test use of SHA3-256 does **not** by itself prove quantum split-key PRF security.

**Protection is not standalone SG-DIFRA security.** It also cannot make an infinitely secure mechanism, and it does not repair ciphertext expansion.

Sources:
- https://csrc.nist.gov/pubs/fips/203/final
- https://csrc.nist.gov/pubs/sp/800/227/final
- https://csrc.nist.gov/presentations/2025/split-key-prfs
- https://datatracker.ietf.org/doc/draft-irtf-cfrg-hybrid-kems/
- https://www.douglas.stebila.ca/research/papers/CIC-MilSteSte26/
- https://arxiv.org/abs/1307.6458

## EUROCRYPT 2028 gates (scientific, not marketing)

1. Frozen public generator distribution and portable test fixtures for all three profiles; original source SHA and versioned design history preserved.
2. Byte-complete, auditable standalone \`Gen/Encap/Decap\` implementation and serialisation; no production use until independent testing.
3. Independent offensive implementations for hidden-subspace, GRS structure and q-ary LPN, with reproducible classical/quantum *upper bounds* on attack costs.
4. Cryptographic theorem relating the **actual sampled public distribution** to a recognized decisional hardness assumption or a separate new, independently motivated hardness assumption with serious evidence. NP-completeness and MDS distance alone do not count.
5. A uniform polynomial-time asymptotic ensemble. See \`ASYMPTOTIC_SYNTAX_AND_CORRECTNESS.md\` for a correctness-only proposal.
6. Actual FO/QROM proof with complete games, oracle bounds, multi-user and decapsulation failure losses.
7. Independent, separate security track for the ML-KEM-backed hybrid using the current combiner theorem.
8. Honest communication of public-key/ciphertext lower bounds and feasible research-only demonstrations.
9. Peer review, academic novelty survey, and blinded manuscript/author policy verification after the official EUROCRYPT 2028 call appears.

**Conference status (10 Oct 2026):** No official EUROCRYPT 2028 CFP/deadline was verified. Do not invent dates. The previous EUROCRYPT 2027 submission deadline was 17 September 2026.

**Precise status**: Validated algebraic sublemmas + finite correctness arithmetic + critical attack/efficiency findings + a conditional standard-KEM hybrid protection path. **Standalone IND-CPA/IND-CCA not proved; "100% secure" is not an attainable cryptographic certification.**
