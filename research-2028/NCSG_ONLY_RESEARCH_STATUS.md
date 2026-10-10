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

## Additional exact NCSG-only mathematics: directional-entropy versus potential leakage

For $t$ independent directions $a_1,\ldots,a_t$ in $\mathbb{F}_p^d$, the public joint gradient operator $D_AQ=(\Delta_{a_1}Q,\ldots,\Delta_{a_t}Q)$ has kernel dimension $rp^{d-t}$ and image dimension $r(p^d-p^{d-t})$ for $r$-output tables. Uniform tables map to the uniform joint derivative image; entropy equals $r(p^d-p^{d-t})\log_2p$. Constructive path integration recovers $Q$ up to independent coset constants. **Publishing more independent complete derivatives exposes *more* of $Q$**, even though it adds more algebraic relations. The F3 rank tests cover $(d,t)=(2,1),(2,2),(3,1),(3,2),(3,3)$. This is a rigorous leakage constraint, not a new KEM.

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

## 10 October additional red-team pass — theorem F: ternary fiber affine-line leakage

**Exact mathematical closure of a proposed design trap, not a standalone KEM break.** The original source samples $f(x)=Au_L+\Delta_a Q(u_R)$ over $\mathbb F_3$, $Bx=(u_L,u_R)$, with $r=k-d$. **Every** fiber $S=f^{-1}(b)$, for **every** valid choice of $A,B,a,Q,b$, is a disjoint union of $3^{d-1}$ affine three-point lines. Proof: telescoping $\sum_{j=0}^2\Delta_a Q(z+ja)=0$ implies the derivative is affine along every $a$-orbit; solving the unique left-coordinate constraint makes the resulting point assignment affine along that orbit; the invertible $B^{-1}$ preserves lines. Any such three points satisfy $x_0+x_1+x_2=0$.

The implications differ crucially by version:

- **Mathematics of source public fibers:** for R1 $(k,d)=(5,3)$, the guaranteed line partition is **9 triples** in each 27-point fiber; R2 $(7,4)$ gives **27 triples** in each 81-point fiber; R3 $(9,5)$ gives **81 triples** in each 243-point fiber. Since all fibers are explicitly enumerated in the source, any observer can discover such zero-sum triples in $O(k|S|^2)$ ternary operations using pairs $(x,y)$ and set lookups of $-x-y$. Randomized invertible $B$ cannot hide this deterministic property.
- **Insecure NCSG-affine labeling candidate:** if a proposed cryptographic redesign binds the public linear rows to ternary assignments by an affine map $h(x)=Lx+c$, then every such triple gives a public weight-three row relation. Under ternary symmetric noise of rate $\nu$, the event that the corresponding three observed ciphertext symbols sum to zero has probabilities $(1+2(1-3\nu/2)^3)/3$ for the noisy-linear zero message and $1/3$ for uniform one. At $\nu=3/16$ the gap is exactly $2(23/32)^3/3\approx0.247538$ before using more than one triple. This breaks that *hypothetical* redesign's IND-CPA message-hiding attempt.
- **NOT an attack on the source SG-DIFRA-MDS bit ciphertext:** the archived labels are **independently sampled in $K=\mathbb F_{2^{10}}$**, not $h(x)=Lx+c$ over $\mathbb F_3$. Even translating a ternary relation to an unrelated characteristic-two alphabet is invalid. No evidence of a ciphertext relation in those dense labels follows from this theorem alone.
- **No instant fix:** hiding ternary rows with independent random labels restores public-row indifference and reintroduces the previously proved *NCSG-removability* defect. Choosing nonlinear assignment-dependent labels may avoid three-term linear cancellation, but not the automatically renewed high-degree/spectral/local-bias attack obligations. No NCSG-only KEM or three secure parameter sets are certified as of this pass.

**Reproduction**: [\`attacks/ternary_affine_line_leakage.py\`](attacks/ternary_affine_line_leakage.py), Python stdlib, tests nine random-field constructions spanning exact R1/R2/R3 local geometries. The script uses independent random full-rank change-of-basis matrices and enumerates triple dependencies **from the public fiber set alone**. Formal theorem statement/proof in the active 2028 manuscript Section 4.1.

**Publication category:** a falsifiable structural theorem and a conditional three-term statistical distinguisher, *not* a proof that an original post-quantum KEM is secure, nor established novelty relative to all finite-field literature.

### Exact public-fiber first-moment distinguisher (supplement to theorem F)

For a uniformly sampled original MaxEnt ternary predicate $f$ and any target $b$, let $L(f^{-1}(b))$ count the publicly visible three-point affine lines. Put $s_0=3^d$, $r=k-d$, and $N_0=3^k$.

- NCSG source **exact expectation**: $3^{d-1}+[s_0(s_0-1)/6-3^{d-1}]3^{-r}$.
- Uniform arbitrary subset of size $s_0$ from $\mathbb F_3^k$ **exact expectation**: $s_0(s_0-1)(s_0-2)/[6(N_0-2)]$.
- The three original profile local geometries give $(21,12.13693)$, $(66,39.04805)$, $(201,120.01631)$ for (NCSG, uniform) first moments, respectively. The expected public line count is roughly 1.67–1.73 times larger under the source's sampler.

**Proof:** For a right-block affine line parallel to $a$, the source's derivative telescoping forces a matching line in the fiber. For any nonparallel right line, the two summands of the translated $Q_0$ table use six pairwise distinct uniformly sampled points, so the sum derivative is uniform in $\mathbb F_3^r$ and vanishes with probability $3^{-r}$. Sum over all $s_0(s_0-1)/6$ right lines. For the null sample, use the hypergeometric probability a given ambient line is fully selected. Full proof in active manuscript Theorem 4.2.

The reproducible threshold-statistic test samples 30 source and 30 uniform public fibers for each original profile and calculates its observed accuracy; it **does not** claim a finite universal advantage for an arbitrary non-sampled instance. Even a strong public NCSG-vs-uniform fiber distinguisher is **not** an IND-CPA attack on the archived independently random dense labels. It rules out unjustified pseudorandom-fiber assumptions for NCSG-dependent future designs.

## Round 3 — unconditional asymptotic failure of the archived fixed-field MDS-HBCE assumption (10 Oct 2026)

The original SG-DIFRA-MDS source samples a public hidden GRS frame over the permanently fixed field $K=\mathbb F_{2^{10}}$ of size $Q=1024$, with distinct evaluation points. This forces **$M\le1024$ and $u+1\le1024$ at every security parameter**.

**Theorem / constructive attack:** Enumerate all $(u+1)$-subsets of public-label rows and run Gaussian elimination. A planted public key always contains a rank-$u$ set, so the distinguisher accepts with probability one. In the null distribution of $q$ independently uniform *nonzero* vectors of $K^N$, the probability of *any* dependent $(u+1)$-subset is bounded by

$$
{q\choose u+1}\left(1-\prod_{i=1}^{u}\frac{Q^N-Q^i}{Q^N-1}\right).
$$

The inner factor is the exact rank-dependency probability for a fixed subset (conditioning row by row), and the outer union bound covers all subsets. If the public key has polynomial size $q=\operatorname{poly}(\lambda)$ and $N=\Omega(\lambda)$, this is negligible. Because $u+1\le1024$ is an absolute constant, at most $q^{1024}\operatorname{poly}(N)$ operations suffice: **a uniform PPT distinguisher**, despite the gigantic degree, refutes an asymptotic MDS-HBCE indistinguishability assumption against all PPT/QPT adversaries.

**Critical evidential boundary:** This is an **asymptotic break of the fixed-field planted-key assumption**, NOT a practical break at the frozen SGD-R1/R2/R3 parameters and not direct message/shared-key recovery. Direct subset enumeration requires $\log_2{q\choose u+1}\approx656.94,1136.78,1718.10$ subsets for the three finite parameter sets, before field elimination. These are astronomical upper bounds on naive attack work, not lower bounds on optimized attacks. The original source's candidate-only relation heuristic is a different cost model and does not constitute a matching bound.

**Repair obligation:** A changing security parameter cannot coexist with a universally PPT-hard MDS-HBCE assumption using the **same fixed GF(1024) distinct-point GRS family**, polynomial-size keys and growing $N$. A field growing with $\lambda$ or an independently conceived algebraic encoding must be specified and cryptanalysed afresh; such a change is not a secure-KEM proof. The active objective remains original NCSG-native encryption, not adapting any other published KEM.

**Automated checks:** [fixed-field asymptotic distinguisher](attacks/fixed_field_mds_hbce_ppt_break.py) uses exact GF(1024) row arithmetic and planted/null simulation, independently exhausts all ordered nonzero triples in GF(3)^3 to verify the exact null dependency formula, and prints the finite-profile enumeration budgets. The active manuscript contains the full proof at Section 9.1.

**Evidence status:** A rigorous asymptotic counterexample to the source's claimed assumption family; it is a conditional theorem for explicitly quantified growth. It does not prove the currently unconstructed NCSG-only target IND-CPA/CCA secure.

## Round 4 — certified finite-profile single-fiber geometric distinguisher (10 Oct 2026)

**Source:** the original 26-page SG-DIFRA manuscript, sections 5 and 5.1: ternary MaxEnt differential predicate $f(x)=Au_L+\Delta_aQ(u_R)$ with $(u_L,u_R)=Bx$, where $Q$ is sampled uniformly over tables. This entry adds a genuinely *finite-parameter* statistical guarantee to earlier round-2/3 geometric expectation findings. It **does not claim IND-CPA/CCA break of the archived GF(1024) dense-label KEM**.

**Deterministic public-only attack:** Given one enumerated ternary NCSG fiber $S\subseteq\mathbb F_3^k$ of size $s=3^d$, enumerate all 3-point affine lines via public pair lookup $z=-x-y$. Normalize direction vectors to projective representatives. Output "MaxEnt" if at least **three distinct contained affine lines have the same direction**. Complexity $O(ks^2)$ operations (including hash lookups).

**Exact uniform direction lemma:** for each of the $L=3^{d-1}$ forced $a$-coset lines, the direction in external coordinates is $v_z=B^{-1}(-A^{-1}T_z,a)$ where $T_z=Q(z)+Q(z+a)+Q(z+2a)$. Across the disjoint $a$-cosets, the $T_z$ are independent uniform $\mathbb F_3^r$ vectors. Since all images have the same nonzero right coordinate $a$, their projective directions are independent uniform among exactly $m_0=3^r$ possibilities, even conditioned on secret coordinate changes $A,B,a$. This is a *stronger* restriction than the earlier guaranteed-line theorem.

**Exact planted acceptance lower bound (occupancy):** let $L=3^{d-1}$, $m_0=3^r$. Sum over nonnegative integer $j$ such that $a_j=L-2j\ge0$, $c_j=m_0-a_j-j\ge0$. The no-triple occupancy probability is
$$
m_0^{-L}\sum_j m_0!L!/[a_j!j!c_j!2^j].
$$
Its complement lower-bounds the detector acceptance under the original MaxEnt fiber distribution.

**Exact uniform-subset false-positive upper bound:** for $n=3^k$, $s=3^d$, ambient projective directions number $(n-1)/2$. Every direction has $n/3$ pairwise disjoint affine lines; triple parallel-line choices number $(n-1)/2\,\binom{n/3}{3}$. Any specified nine distinct points appear in a uniform size-$s$ subset with probability $(s)_9/(n)_9$. Thus Markov bounds the false-positive probability by
$$
\frac{n-1}{2}\binom{n/3}{3}\frac{(s)_9}{(n)_9}.
$$

| 2026 source local profile | Exact source event lower bound | Exact uniform-null event upper bound | **Certified advantage lower bound** |
|:--|--:|--:|--:|
| $(k,d,r)=(5,3,2)$ R1 | 0.5547368172 | 0.0069043849 | 0.5478324323 |
| $(7,4,3)$ R2 | 0.9470512035 | 0.0059101459 | 0.9411410576 |
| $(9,5,4)$ R3 | 0.9999123630 | 0.0026602674 | 0.9972520957 |

**Reproduction:** [public-only line-collision attack](attacks/ternary_parallel_line_collision.py) checks all exact symbolic rational bounds, exhaustively checks 19,683 GF(3) scalar potential tables for the reduced $(d,r)=(2,1)$ ensemble (2,187 tables have three forced parallel lines, exactly 1/9), and samples 24 NCSG + 24 random same-size fibers per source geometry using independent invertible hidden bases. The finite trials check implementation consistency, not the derivation of the bound.

**What this fails to establish:** In the *archived* MDS-HBCE Plant-vs-Null key games, the public NCSG fibers are sampled identically in both games; this test has **zero cryptographic distinguishing advantage from the public-fiber marginal alone**. The published GF(1024) labels do not inherit any asserted ternary-linear row relation. This is a firm negative result against pretending those source fibers are pseudorandom subsets and a strong design gate for future NCSG-*coupled* encodings, **not** an active standalone cryptographic KEM or verified 128/192/256-bit security theorem. Full KEM implementation, correctness, quantum/classical attack assessment, IND-CPA, IND-CCA and QROM proof remain open.

**Terminology:** these finite-geometry counts may follow from elementary standard finite-field facts. They are proved here for this exact sampler; absolute literature novelty has **not** been demonstrated. The source manuscript's NP-completeness result concerns worst-case satisfiability, not average-case indistinguishability.

## Round 5 — archived SG-DIFRA-MDS KEM confidentiality breach, not merely an MDS-HBCE distinguisher

**Version scope (10 October 2026):** This is a mathematical attack on the original 2026 **fixed-field GF(1024) hidden-GRS/noisy-linear KEM** under the explicitly stated polynomial-size asymptotic family. It is NOT a break of a complete new NCSG-only KEM, which does not yet exist.

**Theorem 9.2, documented in the active research manuscript, has three constructive stages.** First, enumerate all $(u+1)$-row public label subsets to locate a dependent set of planted rows; any $u+1$ planted GRS rows have rank $u$ and any $u$ are independent. Conditioned on no mixed false positive, its rank-$u$ span $W$ identifies **all** planted row positions via public membership tests. Second, those public planted rows already generate the coordinate-permuted secret GRS code. Enumerate every $u$-position information set and solve its public linear system, accepting bit zero iff the received $M$-symbol word is within the secret decoder's original radius. Since $M-t_{\mathrm{dec}}\ge u$ and the MDS distance exceeds twice this radius, this procedure returns **exactly the secret decoder's bit on every ciphertext**, even malformed ones. Third, reconstruct all repetitions and the majority-decoded FO message, perform the public deterministic re-encryption check, and derive the actual honest encapsulated session key whenever real secret-key Decap is correct.

For the original field $Q=1024$, mixed-subset dependence and random decoy inclusion are jointly upper-bounded by

$$
\varepsilon_{\mathrm{row}}\le
\left[(u+1)\binom{q}{u+1}+q-M\right]
\frac{Q^u-1}{Q^N-1}.
$$

With $q=\operatorname{poly}(\lambda)$, $N=\Omega(\lambda)$ and $1\le u<M\le1024$, this is negligible. If the KEM has key-agreement failure $\delta(\lambda)$ and returns $\kappa$-bit keys, real-versus-uniform key distinguishing advantage is at least $1-\varepsilon_{\mathrm{row}}-\delta(\lambda)-2^{-\kappa}$.

**The three frozen finite profiles are not thereby practically broken.**

| Archived | log2 public planted-row subset work | log2 public decoder information sets |
|:--|--:|--:|
| SGD-R1 | 656.94 | 203.57 |
| SGD-R2 | 1136.78 | 307.12 |
| SGD-R3 | 1718.10 | 410.76 |

The numbers estimate THIS naive exhaustive algorithm's enormous finite workload, not a minimum security level and not proof of finite IND-CCA hardness. The constant bounded field cardinality makes it **uniform classical polynomial-time** only under the explicitly specified asymptotic scaling. Potentially better finite classical and quantum attacks remain unbounded by these values.

**Reproduction:** research-2028/attacks/public_decapsulation_recovery.py reuses the actual GF(1024) Round-3 sampler. It verifies 12/12 toy planted-row reconstructions, 96/96 exact private/public bit-decision agreements, ten deterministic-re-encryption checks, and real shared-key extraction in every successful honest toy decapsulation. It does not claim full R1/R2/R3 feasibility or QROM formal verification.

**No complete fix or secure replacement yet.** Public NCSG geometry remains cryptographically removable from the archived design; stronger local NP-completeness, maximum entropy, noise levels, secret incidence or row permutation do not repair the published code's public-decodability. A genuinely NCSG-essential new trapdoor, a scalable security assumption, independent classical/quantum cryptanalysis and a correct IND-CPA-to-IND-CCA argument remain open. No existing standardized KEM or hybrid was introduced.
