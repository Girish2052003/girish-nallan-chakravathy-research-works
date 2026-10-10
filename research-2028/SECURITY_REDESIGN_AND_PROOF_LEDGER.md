# SG-DIFRA security redesign, October 2026 — EUROCRYPT 2028 research track

**Status: security not established for the standalone SG-DIFRA KEM.** This is a proof/attack ledger, not a deployment certification. All claims below are either proved mathematical lemmas, reproducible finite calculations, conditional reductions, or explicitly open questions. Do not promote the profiles to 128/192/256-bit security ratings.

## Source provenance and author preservation

The immutable author-supplied source file was \`SG_DIFRA_PQC_KEM.pdf\` (26 pages, date embedded by pdfTeX 2026-09-11), by **Girish Nallan Chakravathy and Sreedevi Kannan**. SHA-256 of exact original PDF bytes:

\`24461af422a6a7d1fbadcc29fe4fe372761805a846226d6d343e7180c5382f4d\`

The existing \`archive/SG_DIFRA_PQC_KEM_ORIGINAL_EXTRACTED_TEXT.txt\` records the entire extracted text but is **not** the actual PDF, and is not typesetting-equivalent. The exact binary original is kept as a verified author-upload in the working session; do not claim that the GitHub text archive reproduces it byte-for-byte.

The paper's original exact finite-difference/NCSG mathematics, its prior negative attacks, GRS framing and the original three research parameter sets are preserved in the text, and are **not** attributed to lattice KEM mathematics. Earlier drafts discussed an ML-KEM hedge only as a historical option. The author's **current strictly NCSG-only direction rejects every borrowed KEM and hybrid fallback**. No standardized KEM is an active component. The original GF(1024) hidden-GRS/noisy-linear KEM is also archived for cryptanalysis, not the new approved algorithm.

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

## NCSG-only direction; former optional fallback withdrawn

By explicit author instruction, no external standardized KEM or KEM combiner is a component of SG-DIFRA. The previous optional fallback is **withdrawn** rather than silently relabelled as original mathematical work. The 2026 GRS/noisy-linear construction is retained only as a historical case study and is **not** promoted as a novel secure NCSG design. All new statements and reproductions are in [NCSG_ONLY_RESEARCH_STATUS.md](NCSG_ONLY_RESEARCH_STATUS.md).

The new two-direction differential-cocycle theorem gives genuine algebraic NCSG structure, but its complete derivative tables admit efficient integration. A second NCSG-coupled idea—encrypting with low-degree combinations of public polynomials vanishing at the private witness—is **insecure** under a proved public rank/membership distinguisher. Both are recorded as red-team results and do not instantiate a final KEM.

## EUROCRYPT 2028 gates (scientific, not marketing)

1. Frozen public generator distribution and portable test fixtures for all three profiles; original source SHA and versioned design history preserved.
2. Byte-complete, auditable standalone \`Gen/Encap/Decap\` implementation and serialisation; no production use until independent testing.
3. Independent offensive implementations for hidden-subspace, GRS structure and q-ary LPN, with reproducible classical/quantum *upper bounds* on attack costs.
4. Cryptographic theorem relating the **actual sampled public distribution** to a recognized decisional hardness assumption or a separate new, independently motivated hardness assumption with serious evidence. NP-completeness and MDS distance alone do not count.
5. A uniform polynomial-time asymptotic ensemble. See \`ASYMPTOTIC_SYNTAX_AND_CORRECTNESS.md\` for a correctness-only proposal.
6. Actual FO/QROM proof with complete games, oracle bounds, multi-user and decapsulation failure losses.
7. Standalone NCSG-native trapdoor and key/ciphertext games, without external KEM components.
8. Honest communication of public-key/ciphertext lower bounds and feasible research-only demonstrations.
9. Peer review, academic novelty survey, and blinded manuscript/author policy verification after the official EUROCRYPT 2028 call appears.

**Conference status (10 Oct 2026):** No official EUROCRYPT 2028 CFP/deadline was verified. Do not invent dates. The previous EUROCRYPT 2027 submission deadline was 17 September 2026.

**Precise status**: Validated algebraic sublemmas, historical finite correctness, and newly reproduced NCSG-native distinguishing breaks. **No complete NCSG-only KEM or IND-CPA/IND-CCA proof exists; "100% secure" is not an attainable cryptographic certification.**


## Round 7 — reject the original local trapdoor, distinguish exact mathematics from security (10 Oct 2026)

**Round 6 was not a cryptographic fix.** The earlier theorem and tests showed a public second-difference subspace; they never replaced the original MaxEnt function with a cryptographically secure KEM. The same function is inherently publicly invertible.

**Theorem 4.6, unconditional:** For the original $f(x)=Au_L+\Delta_aQ_0(u_R)$, $(u_L,u_R)=Bx$ with invertible $A,B$, the public constant-shift set $C(f)=\{h:f(x+h)-f(x)\text{ independent of }x\}$ is a vector space and $c_f(h)=f(h)-f(0)$ is a public linear map onto the *entire* $\mathbb F_3^r$. The hidden left-coordinate space $B^{-1}(\mathbb F_3^r\times\{0\})$ supplies a surjective restriction through $A$, but the attacker never needs to know that secret space. Publicly find $r$ shifts with independent output increments and solve an $r$-dimensional linear system for **every local target**. Success is **exactly one for every sampled potential table**, not merely overwhelming probability. **Corollary 4.6a** publicly translates the entire fiber of one local target onto that of every other target.

**Theorem 4.7, additional source-sampling result:** Except with probability bounded by $(2\cdot3^r)3^{-r(3^{d-1}-1)}+(3^d-3)3^r3^{-r(4\cdot3^{d-2}-1)}$, the public constant-shift subspace equals the formerly hidden left-coordinate shift space. For archived R1/R2/R3, bounds are 4.25033449e-7, 3.28803091e-36 and 3.39401302e-151. This bound is **NOT necessary** for the unconditional local inversion theorem.

**Reproduction:** research-2028/attacks/public_first_difference_local_inversion.py checks the 9+27+81 source local target preimages, full-fiber translation bijections, public direction additivity, finite-field mixed operator ranks, rational probability bounds, and the exhaustive 19,683-table scalar census. It is polynomial in the size of an *explicit public table* ($3^k$), not a uniform polynomial-time attack for an arbitrary succinct representation in compact $k$.

**Scope and repair action:** Reject the original source local MaxEnt inversion and hidden affine-coordinate masks as a **standalone cryptographic trapdoor**, while preserving correct public-combinatorial mathematics. This does **not** solve globally overlapping NCSG constraints, find a global secret witness, or independently break the original dense GF(1024) ciphertext. Round 5 separately disproved asymptotic security of the archived fixed-field ciphertext KEM. A genuinely original NCSG-global PKE/KEM mechanism, strong average-case cryptanalysis and complete IND-CCA/QROM security proof remain UNCONSTRUCTED and UNVERIFIED. No source profile can be certified cryptographically secure by relabeling the proofs, applying larger entropy, or asserting worst-case NP-completeness.


## Round 8 — security design rejection by public low-width global witness recovery

See [full proof and tests](ROUND8_PUBLIC_GLOBAL_CSP_SECURITY_LEDGER.md). Overlapping ternary MaxEnt public factors do **not** imply global one-wayness: with public scopes, explicit factor relations and induced width `w`, standard exact bucket elimination recovers a global witness in `poly(L,n,m)*3^(w+1)` operations; this is polynomial for `w=O(log L)`. The public-only adversary was tested on overlap-sharing source-geometry R1/R2/R3 fixtures, random brute-force cross-checks, unsatisfiable controls, and disjoint factors. The result is a theorem under explicit public-factor assumptions and a finite reproducibility result, **not** a new IND-CCA break for a fully specified redesigned scheme. Secret incidence, succinct inputs, and actual full-profile global treewidth were **not** inferred.

**Design action:** preserve Round 7; reject its original public local predicate as a trapdoor, and reject low-width overlap as a substitute. **Formal closure:** only these scoped attacks have proofs; cryptographic security, three new concrete parameters, QROM IND-CCA and submission-grade original KEM remain **OPEN / NOT VERIFIED**.
