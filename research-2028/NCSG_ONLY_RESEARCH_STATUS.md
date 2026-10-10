# SG-DIFRA — NCSG-only direction, no external KEM ingredient

**Freeze date:** 2026-10-10. **Authors:** Girish Nallan Chakravathy and Sreedevi Kannan, following the uploaded original manuscript.

## Binding design requirement

Only mathematics intrinsic to the author's NCSG framework may form the active *candidate's* public-key hard problem and trapdoor. Existing finite-field theory, NP reductions, standard security notions and literature citations may be used as general tools, **not as a substitute KEM, an additional ingredient, or a disguised copy of someone else's design**.

The previously added optional ML-KEM KEM-combiner path has been **withdrawn from the active research draft** at the author's explicit direction. A finite-correctness result concerning GRS-coded labels in the 2026 source is retained only as a historical finding; it is not certified or used as the engine of the new proposal. Previous publications, including Hair–Sahai's CSP-based PKE, are cited for intellectual provenance and novelty assessment, **not** incorporated as implementation ingredients.

## Current mathematical status

| Fact or proposal | Exact result | Security implication |
|:--|:--|:--|
| NCSG-DS restricted Boolean NP-completeness | Original reduction applies under stated formal encoding | Worst-case NP theorem; not an average-case KEM proof |
| MaxEnt ternary fiber size and derivative entropy | Original algebra, stable | Exact structural property only |
| Fixed-field MDS dependency threshold | Original algebra, stable | No bound on general hidden-code attacks |
| NCSG label projection | Exact independence: F and H_flat independent under the archived generator | NCSG is removable in archived KEM; fails author's originality constraint |
| Multi-direction NCSG cocycle | Commuting finite derivatives give zero discrete curl, and line-zero-sums characterize integrability on each plane | Exact mathematical theorem, **not hardness** |
| Potential recovery from complete public derivatives | Constructive path integration | **Public inversion** of this naive approach |
| Coupled witness targets b_i=f_i(s_N) | Coupled to secret witness but biased and correlated | Published target leakage reappears; no hardness proof |
| Polynomial ideal ciphertext C=sum h_i r_i, degree bound D | Public low-degree ideal span is explicitly computable | **Fully broken distinguisher** without secret, via GF(3) Gaussian elimination |
| Full NCSG-only KEM | Not yet specified or proved | **No IND-CPA/CCA proof and no secure profiles** |
| Original SGD-R1/2/3 labels | Historical finite parameters | **Not** certified 128/192/256-bit levels |

## Negative theorems and reproducible scripts

1. **Cocycle integration (necessary and sufficient).** On a two-dimensional \(\mathbb F_3\)-torus, every legitimate pair of directional derivatives satisfies \(\Delta_b g_a=\Delta_a g_b\) and has zero sum on each direction's periodic orbit. Conversely those constraints permit path-independent integration, unique up to a constant. See \`math/multidirection_cocycle.py\`. A published table of all directions is *easy to integrate*; no one-wayness follows.
2. **Public ideal-membership break.** Given publicly readable zero polynomials \(r_i(X)\) and ciphertext \(C=\sum_{\deg h_i\le D} h_i r_i\), compute the coefficient vectors of \(X^\alpha r_i\) for \(|\alpha|\le D\), and compare rank after adding \(C\). This always recognizes an honestly generated zero ciphertext, without the secret witness. The span rank \(R\) is **always strictly less** than the ambient dimension \(V\): every public ideal generator vanishes at the witness while the constant polynomial one does not, hence \(W_D\subseteq\ker(\mathrm{ev}_s)\subsetneq V_t\). A uniform one ciphertext is falsely accepted with exact probability \(3^{R-V}\le1/3\), so the public rank distinguisher succeeds with probability **at least 5/6**, regardless of the secret witness and without assuming anything cryptographically hard. For fixed total degree, the attack is polynomial-time. See \`attacks/public_ideal_membership_break.py\`.
3. **Former planted-code subspace attack.** A toy exact finite-GF(1024) exhaustive solver in \`toy_hidden_mds_attack.py\` recovers hidden planted rows of a small past design. This is a structural research regression, not the active primitive.
4. **Exact size obstacle.** The historical GRS-label design requires at least 77,414,400, 487,710,720, and 2,786,918,400 bytes of ciphertext in the three profiles. \`profile_cost_audit.py\` verifies lower bounds. No current NCSG-only replacement has enough specification to claim smaller numbers.

## Author-origin protocol selection criteria

A future self-contained KEM must:
- Couple genuine NCSG finite-difference structure to encryption so that removing the public NCSG data **changes the security-relevant distribution**; prove this by an explicit conditional distribution or dependency lemma.
- Define public \`Gen\`, \`Encap\`, secret \`Decap\` at bit and byte level without requiring external KEM ingredients.
- Be correct with precisely bounded false-accept and false-reject probabilities while resisting all *public* zero-test, span, low-degree, derivative, membership, spectral and local bias attacks.
- Prove a *conditional IND-CPA reduction* to a **new, clearly sampled average-case problem** or a known assumption genuinely implied by the exact NCSG distribution; do not infer security from NP-completeness.
- Give a complete QROM CCA transform with explicit loss and an actual independently tested reference implementation.
- Specify scalable, efficient algebraic parameter families, then independently estimate concrete classical and quantum security across three **new** profiles.
- Include a separate prior-art comparison: being formulated with new symbols does not establish cryptographic novelty; public-key encryption from CSPs is an existing research direction (Hair–Sahai, arXiv:2604.10479, 2026).

## What cannot be promised

No universal theorem can establish that no future adversary will ever break an unstandardized, newly proposed public-key primitive. The current artifacts prove specific algebra and specific breaks, but **do not** provide the user's requested formally verified end-to-end KEM. No secure novel parameters have been justified. The ethical publication position is to keep this explicit, rather than to manufacture hardness proofs.

## Source and calendar

Exact author PDF bytes SHA-256: \`24461af422a6a7d1fbadcc29fe4fe372761805a846226d6d343e7180c5382f4d\` (26 pages). The text-only archive is **not** the actual PDF binary; see \`archive/SOURCE_ORIGINAL_BINARY_MANIFEST.md\`. The official 2027 paper deadline publicly listed was 17 September 2026, already elapsed as of this 10 October 2026 document. The 2028 conference is a **forward research target**, without a verified CFP or deadline.
