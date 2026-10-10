---
title: "SG-DIFRA: An Attack-Driven Study of NCSG Fibers and Hidden-MDS KEMs"
subtitle: "Revised mathematical analysis and security-status correction — research draft, 10 October 2026"
author:
  - "Girish Nallan Chakravathy"
  - "Sreedevi Kannan"
date: "10 October 2026"
lang: en
geometry: "margin=27mm"
fontsize: 11pt
colorlinks: true
numbersections: true
---

> **Security notice.** This document is a revised research draft based on the author's 26-page SG-DIFRA-MDS manuscript. It is **not** a security certificate, a proof that MDS-HBCE or q-ary LPN is hard, or a valid claim of 128-, 192-, or 256-bit IND-CCA security. A complete reference implementation and independently reviewed concrete estimates are absent. The source paper is preserved conceptually in the sections below, with newly identified caveats and theorems made explicit.

# Abstract

SG-DIFRA is an attack-driven experimental key-encapsulation proposal constructed by separating public nonlinear constraint-system geometry (NCSG), secret incidence, and a hidden generalized Reed–Solomon (GRS) label system. Its earlier Boolean-fiber design leaked period-pair linear relations; dense labeling removed those relations but did not protect a shared planted secret; secret incidence repaired public-fiber correlation but an initial low-noise binary ciphertext was broken by nearly clean information sets and low-weight hidden-code dependencies. The current large-field version employs symbols from $K=\mathbb F_{2^{10}}$, a hidden length-$M$, dimension-$u$ GRS code, and independently sampled $K$-symmetric symbol error of probability $\nu=3/16$. Algebraic identities establish exact fiber regularity, derivative entropy, planted-row independence through weight $u$, and finite correctness bounds.

This revision supplies a further exact result: after canonical flattening, the NCSG predicates and targets are statistically independent of the public label matrix, and the master secret can be eliminated from the decryption key without changing any decapsulation outcome. Consequently the proved NCSG worst-case facts do not imply the encryption security of this construction. A second issue is that the fixed field forces $M\le1024$, so three finite parameter records do not instantiate a growing asymptotic security family. The remaining one-bit security is only a conditional hybrid statement assuming **MDS-HBCE** and **$1024$-ary LPN**, neither of which has been justified by a concrete security estimator or reduction to an established problem. The resulting contribution is a transparent cryptanalytic case study and falsifiable construction proposal, **not a proven post-quantum KEM**.

**Keywords:** nonlinear constraints; finite differences; key encapsulation; Reed–Solomon; noisy linear equations; cryptanalysis; correctness bounds; quantum random oracle model.

# 1. Context, definitions and threat model

Let $\mathbb F_p$ denote the field with $p$ elements and $K=\mathbb F_{2^{10}}$ the field with $Q=1024$ elements. For a map $P:\mathbb F_p^N\rightarrow\mathbb F_p^t$ and a direction $a$, define

$$
\Delta_aP(w)=P(w+a)-P(w).
$$

The NCSG differential-solvability problem asks whether given differential equations $\Delta_{a_j}P_j(w)=b_j$ have a common solution. This is a *worst-case* decision language. The cryptographic challenge in the present candidate instead concerns an *average-case* public-label distribution and noisy samples over $K$. These are different mathematical claims and no implication between their hardness has been proved.

The adversary sees the entire public key, including all supports, predicates, target values, fiber sets, dense field labels, profile constants, and ciphertexts. A chosen-ciphertext adversary may make decapsulation queries subject to the standard challenge-ciphertext restriction. Reference security must consider attacks on the full frozen distribution, including hybrid structure, generalized birthday search, hidden-subspace recovery, large-field noisy-linear decoding, adaptive multi-target attacks, and quantum algorithms. A named work factor for a single attack is not a security lower bound.

# 2. Construction history and confirmed attacks

## 2.1 Boolean-period attack

In the original binary construction, for the map

$$
f(x)=Au_L+\Delta_aQ(u_R),\qquad (u_L,u_R)=Bx,
$$

the change $e=B^{-1}(0,a)$ obeys $f(x+e)=f(x)$ because $2a=0$. Consequently complete fibers are partitioned into public period pairs. For an old affine one-hot incidence row $h(x)$, any two distinct pairs satisfy

$$
h(x)+h(x+e)+h(y)+h(y+e)=0
$$

in characteristic two. A noisy four-row test distinguishes planted ciphertexts. Publishing complete one-hot fibers also creates low-weight subset-sum collisions. These are genuine attacks, not merely proof limitations.

## 2.2 Changes in the intermediate designs

Candidate subsampling prevented complete-fiber publication but exposed a small-list consistency search. Odd-characteristic maximum-entropy derivatives and dense independent labels removed binary period-pair identities. Nevertheless a planted shared secret influenced public-fiber marginal distributions, permitting an attack statistic based on centered marginals. Secret incidence then generated public predicates, targets, and fibers *before* independent hidden selections, eliminating this particular correlation.

## 2.3 First secret-incidence profiles: another break

The earlier secret-incidence design used binary noise $\nu=10^{-3}$. A random invertible $N$-row subset of a public matrix was error-free with probability $(1-\nu)^N$, constant at the tested dimensions. Solving that basis and validating against other equations recovered the ephemeral vector. Repetition turned the distinguisher into a route to the deterministic FO message and shared key. An independent low-weight-relation attack targeted binary hidden codes with dual-weight examples around 5–11.

The present large-field repair changes both the code and noise rate. Its exact MDS dependency threshold removes the *specific* low-weight attack. Its $3/16$ symbol noise makes the earlier entirely-clean-basis strategy exponential in $N$. Neither assertion rules out more efficient algorithms.

# 3. NCSG worst-case mathematics

For Boolean $a,b,c,y$, work in $\mathbb F_2$ and put

$$
g(a,b,c,y)=a+b+c+ab+ac+bc+abc
+y(a+b+c+ab+ac+bc).
$$

A direct 16-case truth table gives exactly eight accepted tuples with $g=1$, and

$$
(\exists y\;g(a,b,c,y)=1)\iff (a\lor b\lor c).
$$

For a 3-CNF formula with clauses $C_j$, introduce one balancing bit $y_j$ per clause and one global direction bit $z$. Define a *single vector-valued potential*

$$
P(x,y,z)=\big(z(1+g_1(x,y_1)),\ldots,z(1+g_m(x,y_m))\big).
$$

Then $\Delta_{e_z}P=(1+g_1,\ldots,1+g_m)$; a zero target has a solution precisely when the original 3-CNF has one. The potential components have degree at most four, so this is an explicit polynomial many-one reduction proving the restricted NCSG-DS decision problem NP-complete. A distinct scalar-local fresh-direction formulation is obtained by using a separate $z_j$ for every clause. This theorem does **not** imply average-case one-wayness.

Affine covariance follows directly: if $\phi(w)=Tw+c$ with invertible $T$ and $a'=T^{-1}a$, then $\Delta_{a'}(P\circ\phi)(w)=\Delta_aP(\phi(w))$.

For an arbitrary tabulated $h$, adjoining $z$ and setting $P_h(x,z)=z\widehat h(x)$ embeds the table into a differential equation $\Delta_{e_z}P_h=h$. The representation has polynomial description only where the table itself has polynomial size.

# 4. Maximum-entropy public fibers over $\mathbb F_3$

Fix $k>d\ge1$, let $r=k-d$, sample invertible $A\in GL_r(\mathbb F_3)$, $B\in GL_k(\mathbb F_3)$, nonzero $a\in\mathbb F_3^d$ and a uniformly random table $Q_0:\mathbb F_3^d\rightarrow\mathbb F_3^r$. Set

$$
f(x)=Au_L+\Delta_aQ_0(u_R),\quad (u_L,u_R)=Bx.
$$

For every target $b\in\mathbb F_3^r$ and each right block $u_R$, the left block is uniquely

$$
u_L=A^{-1}(b-\Delta_aQ_0(u_R)).
$$

Thus each fiber has *exactly* $B_0=3^d$ elements and can be sampled without conditioning rejection. (We use $B_0$ for bucket size to distinguish it from the invertible matrix $B$.)

An intrinsic finite-difference realization is obtained by choosing a functional $\ell$ with $\ell(a)=1$ and setting

$$
P(x)=\ell(\pi_RBx)A\pi_LBx+Q_0(\pi_RBx),\qquad e=B^{-1}(0,a).
$$

Then $\Delta_eP=f$ by direct substitution. For any fixed direction $a$, a legitimate derivative $g=\Delta_aQ_0$ has sum zero on every line $\{w+ja:j\in\mathbb F_3\}$. Conversely every line-zero-sum function integrates to a table. Therefore the image dimension is

$$
\dim_{\mathbb F_3}\mathrm{Im}(\Delta_a)
=r(3-1)3^{d-1},
$$

and the image of a uniform table is uniform on that image, with entropy

$$
H(\Delta_aQ_0)=2r3^{d-1}\log_2 3.
$$

All of these statements are unconditional finite-field mathematics; their proof gives no noisy-encryption pseudorandomness claim.

# 5. Current hidden-MDS label construction

Select a profile $(n,k,d,r,m,M,u,N,\nu,\ell,\kappa_F,T_{\mathrm{rep}})$ with $M\le1024$, $u<M$ and $u\le N$. Independently sample $m$ NCSG supports, predicates and targets and enumerate $m$ fibers $S_i$, each of size $B_0=3^d$. Sample a master secret $s\in\mathbb F_3^n$ and a hidden set $\mathcal C\subseteq[m]$ of size $M$. For each $i$ sample invertible $R_i$ and a point $\sigma_i$ inside $S_i$ if $i\in\mathcal C$ and outside otherwise. Store $\delta_i=\sigma_i-R_is_{\mathcal N(i)}$ privately. The full NCSG public layer is generated independently of $s$.

For public distinct evaluation points $\alpha_1,\ldots,\alpha_M\in K$ and multipliers $v_i\ne0$, define the GRS generator matrix

$$
G_i=v_i(1,\alpha_i,\alpha_i^2,\ldots,\alpha_i^{u-1})\in K^u.
$$

Choose full-row-rank $T\in K^{u\times N}$ and a secret bijection $\pi:\mathcal C\rightarrow[M]$. All public row labels initially are sampled independently and uniformly from $K^N\setminus\{0\}$. In each good bucket replace exactly one label with

$$
h_{i,\sigma_i}=G_{\pi(i)}T.
$$

The concatenated public matrix $H$ has $q=m3^d$ rows. The temporary $T$ is erased after key generation.

The MDS theorem gives $C_G=[M,u,M-u+1]_{1024}$. Every at most $u$ distinct planted rows is independent and every $u+1$ planted rows are dependent, because the map $z\mapsto zT$ is injective. This is a **linear-algebraic statement only**.

## 5.1 Exact noise and bit encryption

Each independent error coordinate $E$ equals zero with probability $13/16$ and each specific nonzero symbol with probability $(3/16)/(1023)$. For bit zero sample $t\leftarrow K^N$, $e\leftarrow E_\nu^q$ and output

$$
v=Ht+e.
$$

For bit one sample $v\leftarrow K^q$ uniformly. To decode, the secret key identifies the $M$ good bucket coordinates, reorders them via $\pi$, and applies a bounded-distance GRS decoder with

$$
t_{\mathrm{dec}}=\left\lfloor\frac{M-u}{2}\right\rfloor.
$$

Return zero if and only if a codeword at distance at most $t_{\mathrm{dec}}$ is found. Every other word decodes to one. For a bit-zero ciphertext,

$$
p_0\le\mathrm{Pr}[\mathrm{Bin}(M,3/16)>t_{\mathrm{dec}}].
$$

For a uniform bit-one ciphertext, the Hamming-ball union bound is

$$
p_1\le 1024^{u-M}\sum_{j=0}^{t_{\mathrm{dec}}}{M\choose j}1023^j.
$$

Strict majority across seven fresh encryptions per message bit yields the standard binomial majority tail. The full-message error is bounded by $\ell$ times that tail.

# 6. New theorem: removal of NCSG geometry without cryptographic effect

**Theorem (distributional projection).** Assume all public fibers have the fixed size $B_0$ and their chosen positions within good buckets are uniform. Let $F$ be all public NCSG data and $H_{\mathrm{flat}}$ the ordered matrix of labels after canonical bucket enumeration. Then

$$
\mathcal L(H_{\mathrm{flat}}\mid F=f)=\mathcal L(H_{\mathrm{flat}})
\quad\text{for each legal }f.
$$

Moreover a secret key $(s,\mathcal C,\{R_i,\delta_i\},\pi)$ is functionally equivalent, on all ciphertexts, to one with $s'=0$, $R'_i=I_k$, $\delta'_i=\sigma_i$, and the same $\mathcal C,\pi$.

**Proof.** Conditioning on $F=f$ fixes the names of $B_0$ bucket positions but changes neither the uniform good-set choice nor the secret ordering, full-rank embedding, uniformly chosen good positions, or independent decoy rows. Consequently the conditional law of ordered labels is constant in $f$. For the second claim,

$$
R'_is'_{\mathcal N(i)}+\delta'_i=0+\sigma_i
=R_is_{\mathcal N(i)}+\delta_i
$$

for each index. Both decapsulation procedures select identical rows and run the same deterministic decoder, hence agree on every possible ciphertext. $\square$

**Security interpretation.** The theorem does not break MDS-HBCE or q-ary LPN; instead it proves the purported NCSG hardness is not exercised by the cryptographic channel. An actual NCSG-hard KEM would require a new coupling between the finite-difference distribution and hidden labels, plus new average-case and chosen-ciphertext analyses. Merely asserting NCSG-DS NP-completeness cannot supply that coupling. The public NCSG material can therefore be described as a mathematically exact, cryptographically redundant indexing layer.

# 7. Assumption boundary and conditional hybrid

Define *PlantMDS-HBCE* as the ordered public label distribution in Section 5 and *NullMDS-HBCE* as the same distribution with each planted label independently replaced by uniform nonzero $K^N$ row. The **MDS-HBCE assumption** is that no efficient, appropriately resource-bounded adversary distinguishes these games. This assumption has no proof here.

Define $1024$-ary LPN as the indistinguishability of

$$
(H,Ht+e)\quad\text{and}\quad(H,U)
$$

for independent uniform $H\leftarrow K^{q\times N}$, $t\leftarrow K^N$, $e\leftarrow E_\nu^q$ and $U\leftarrow K^q$. The **LPN assumption** for this particular high-redundancy field distribution has not been certified by an estimator or reduction.

A straightforward triangle hybrid, provided all exact games are specified, gives an upper bound of the form

$$
\mathrm{Adv}_{\mathrm{bit}-CPA}(\mathcal A)
\le \mathrm{Adv}_{\mathrm{HBCE}}(\mathcal B)
+\mathrm{Adv}_{\mathrm{qLPN}}(\mathcal D)
+\frac{q}{1024^N}.
$$

This is a conditional reduction, not independent evidence that either advantage is small. A message ciphertext consists of $\ell T_{\mathrm{rep}}$ fresh copies under one fixed public key; a standard telescoping hybrid incurs at most that many one-bit terms, with resource overhead that must be recorded in any concrete certificate.

# 8. FO-style KEM interface and unresolved QROM proof

The original design draws an $\ell$-bit message $\mu$, derives deterministic encryption coins from a domain-separated oracle binding the canonical public key and $\mu$, encrypts all bits, and derives a session key from $\mu$ and the full ciphertext. Decapsulation decodes a candidate message, deterministically re-encrypts, and uses domain-separated implicit rejection with secret fallback material on mismatch.

An authentic QROM IND-CCA theorem for this exact implementation requires explicit random-oracle experiments, domain separators, byte-level unambiguous encodings, a verified reduction satisfying the hypotheses of the chosen FO/MRE result, its query/depth losses, and the full-message decryption-error bound. Those steps are **not** provided by assuming the transform conclusion. Consequently this draft makes no unconditional end-to-end QROM claim.

## 8.1 Grover and message-space limits

Public deterministic re-encryption makes the message a candidate for exhaustive verification. For an $\ell$-bit message, generic quantum message search takes order $2^{\ell/2}$ oracle-verification steps, before gate/depth overhead. The source message lengths 320, 448, 640 correspond to exponents 160, 224, 320 **for this attack only**, not complete post-quantum security levels.

# 9. Fixed-field scaling obstruction

**Proposition.** With $K=\mathbb F_{2^{10}}$ and $G_i=v_i(1,\alpha_i,\ldots,\alpha_i^{u-1})$ for pairwise distinct $\alpha_i\in K$, every valid fixed-field profile satisfies $M\le1024$.

**Proof.** The map $i\mapsto \alpha_i$ is an injection from a set of cardinality $M$ into $K$, which has cardinality $1024$. $\square$

Thus an asymptotic assertion quantified over all security parameters cannot be inferred from the original three fixed profiles. One **possible research direction**, not a validated repair, is to define $K_\lambda=\mathbb F_{2^{h(\lambda)}}$ with $h(\lambda)\ge\lceil\log_2M(\lambda)\rceil$, provide deterministic irreducible-polynomial generation and exact sampling, and then restate and reassess **both** hardness assumptions as uniform ensembles. A growing field may change attack costs and distributional properties; security does not follow merely from lifting the capacity limit.

# 10. Re-evaluation of concrete attacks

The original random-clean-basis method chooses $N$ linearly independent public equations and solves the noiseless candidate. Its clean probability is $(13/16)^N$ and expected number of independent trials is $(13/16)^{-N}$ *if the method tests fresh random bases and neglects its own computational cost*. This is **not** an information-theoretic minimum complexity, nor a general ISD/BKW bound. Better attacks might use partial errors, structured elimination, hybrid decoding, or quantum algorithms.

The planted-code dependency minimum is exactly $u+1$. This removes the old low-weight relation family **inside the planted subset**, but no theorem prevents adversaries from exploiting the large public matrix as a whole, all high-order relations, label distributions, or known GRS structural invariants. These possibilities remain open.

A mixed-relation union bound can be derived by exposing at least one independent nonzero decoy row last. For a fixed support size $j\le u$ and a fixed projective coefficient vector, that row has at most one satisfying value among $1024^N-1$ possible nonzero labels. Summing over supports and projective vectors yields the source bound

$$
\mathrm{Pr}[\exists\text{ a relation of weight }\le\tau]
\le
\frac{1}{1024^N-1}
\sum_{j=1}^{\tau}{q\choose j}\frac{1024^j-1}{1023},
\qquad \tau\le u.
$$

The union bound does not address high-weight relations or non-linear distinguishers. Exact finite arithmetic and toy regressions are stored in \`formal-verification-and-mathematical-proofs/\`.

# 11. Three research profiles

| Parameter | SGD-R1 | SGD-R2 | SGD-R3 |
|:--|--:|--:|--:|
| Nominal $\lambda$ | 128 | 192 | 256 |
| $(n,k,d,r)$ | $(64,5,3,2)$ | $(96,7,4,3)$ | $(128,9,5,4)$ |
| Number of buckets $m$ | 1024 | 1536 | 2048 |
| Planted buckets $M$ | 256 | 384 | 512 |
| GRS dimension $u$ | 64 | 96 | 128 |
| Ciphertext vector dimension $N$ | 640 | 960 | 1280 |
| Labels per bucket $B_0$ | 27 | 81 | 243 |
| Total public labels $q$ | 27,648 | 124,416 | 497,664 |
| First all-planted relation weight | 65 | 97 | 129 |
| Bounded decoder radius | 96 | 144 | 192 |
| Symbol error rate | 3/16 | 3/16 | 3/16 |
| Majority repetitions | 7 | 7 | 7 |
| Message length $\ell$ | 320 | 448 | 640 |
| Fallback bits $\kappa_F$ | 384 | 576 | 768 |
| Clean-basis attack $\log_2 W$ | 191.72 | 287.58 | 383.44 |
| Analytic $\log_2$ message-failure upper bound | $-148.32$ | $-219.82$ | $-290.98$ |

**Table interpretation.** The rows labeled nominal $\lambda$ are identifiers, not certified bit-security. The clean-basis row reports exactly one method. The message-failure row is derived from idealized independent noise and bounded-distance decoding, not an execution-tested failure estimate. These profiles also have very large public keys and ciphertexts by contemporary KEM standards.

# 12. Verification, limitations and responsible next steps

The accompanying Python scripts verify the field modulus, exhaustive Boolean truth table, regular fibers in a tiny ternary fixture, small GRS row independence, functional equivalence after replacing $s$, a toy clean-basis adversary on $1024$-ary noisy samples, and analytical profile bounds. Such checks are finite evidence for corresponding algebraic properties; they do **not** establish IND-CPA or IND-CCA security against arbitrary efficient adversaries.

A publication-ready new cryptographic claim would require at least: an executable, byte-exact KEM implementation; independent cryptanalysis of the full public-label distribution and noisy sample problem; reproducible estimators including quantum work, depth and memory; a sound asymptotic parameter family; a complete QROM reduction with explicit concrete losses; a venue-compliant anonymous submission; and explicit treatment of computational/memory cost, malformed ciphertexts, fault and side-channel behavior.

# 13. Conclusion

The successive SG-DIFRA repairs address specific demonstrated weaknesses, and the surviving finite-field mathematics remains valuable. Nevertheless the proposed ciphertext-security engine is a hidden-MDS-label problem combined with noisy linear samples; the NCSG geometry is statistically and functionally redundant for security under the actual generator. The strong statement supported by this draft is therefore *attack-driven cryptographic analysis with conditional reductions*, not a formally verified post-quantum KEM. Any security promotion needs new mathematics and independent cryptanalysis, not a change of adjectives.

# References

1. I. S. Reed and G. Solomon, "Polynomial Codes over Certain Finite Fields," *J. Soc. Indust. Appl. Math.*, 8(2), 300–304, 1960. https://doi.org/10.1137/0108018
2. S. Gao, "A New Algorithm for Decoding Reed–Solomon Codes," in *Communications, Information and Network Security*, 2003.
3. A. Couvreur et al., "Distinguisher-Based Attacks on Public-Key Cryptosystems Using Reed–Solomon Codes," *Designs, Codes and Cryptography*, 73, 641–666, 2014. https://arxiv.org/abs/1307.6458
4. J. Ge, H. Liao, and R. Xue, "Measure-Rewind-Extract: Tighter Proofs of One-Way to Hiding and CCA Security in the Quantum Random Oracle Model," *ASIACRYPT 2024*, 2024.
5. N. Bindel et al., "Tighter Proofs of CCA Security in the Quantum Random Oracle Model," *TCC 2019*, 2019.
6. F. Giacon, F. Heuer, and B. Poettering, "KEM Combiners," *PKC 2018*, 2018.
7. NIST FIPS 203, "Module-Lattice-Based Key-Encapsulation Mechanism Standard," 2024. https://doi.org/10.6028/NIST.FIPS.203
8. Source manuscript: Girish Nallan Chakravathy and Sreedevi Kannan, *SG-DIFRA: An Attack-Driven NCSG KEM with Secret Incidence and MDS Coding*, author-provided 26-page PDF, October 2026.

# Appendix A. Reproduction and claim labels

Run \`python formal-verification-and-mathematical-proofs/test_sg_difra.py\` and \`python formal-verification-and-mathematical-proofs/profile_bounds.py\`. A passing run is evidence only for the printed fixtures and calculations. The project status is **RESEARCH DRAFT — CRYPTOGRAPHIC SECURITY NOT ESTABLISHED**.

# Appendix B. Submission caution

EUROCRYPT 2027's publicly listed full-paper deadline was 17 September 2026; it has elapsed as of 10 October 2026. The original paper and this credited research version are *not anonymous*. For a future double-blind venue, apply the current published formatting, author-identification, repository and AI-use rules; do not upload the named version as an anonymous submission. Verify all bibliographic records directly from publishers before submission.


# Appendix C. October 2026 Round-8 follow-up: public low-width global witness recovery

**Archival status of this manuscript:** This shorter revision records the earlier SG-DIFRA iterations; it should not be described as an actively secure NCSG-only KEM. The authoritative active research treatment is [SG-DIFRA NCSG-only draft](SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.md), Section 12.9, and the [Round-8 exact attack ledger](../research-2028/ROUND8_PUBLIC_GLOBAL_CSP_SECURITY_LEDGER.md).

In Round 7 the original ternary local source predicate was shown publicly invertible under its full-table evaluation model, so it is **not** a cryptographic trapdoor. Round 8 establishes a further structural attack boundary for *global overlapping* public ternary constraints. With known public scopes and explicit public relation tables, bucket elimination recovers a global solution or exactly detects inconsistency in time polynomial in input length times $3^{w+1}$, where $w$ is the induced width of the public primal graph. A public CSP distribution with logarithmic width therefore cannot rest its one-wayness on overlap alone. This classical CSP theorem is not presented as original new mathematics, an attack on every possible high-width construction, a measured bound on the historical full protocol's incidence topology, or a KEM IND-CCA break.

[Executable deterministic public-only tests](../research-2028/attacks/public_global_treewidth_witness_recovery.py) cover independently brute-forced CSPs and genuinely overlapping R1/R2/R3 source-local geometries. They cannot validate cryptographic bit-security or quantum hardness. No complete NCSG-only secure redesign or three certified parameter sets currently exists; Round 8 has **no formal KEM security closure**, and the 2027 conference deadline had already elapsed by this update.
