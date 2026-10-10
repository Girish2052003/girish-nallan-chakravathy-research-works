---
title: "SG-DIFRA: From Broken Hidden-MDS KEM to an NCSG-Only Mathematical Research Program"
subtitle: "NCSG-only authorship constraint — cryptanalysis, exact obstructions, and research direction, 10 October 2026"
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

> **Security notice.** This NCSG-only mathematical research draft is a revision based on the author's 26-page SG-DIFRA-MDS manuscript. The GRS/LPN iteration is historical and is not a new approved active KEM. It is **not** a security certificate, a proof that MDS-HBCE or q-ary LPN is hard, or a valid claim of 128-, 192-, or 256-bit IND-CCA security. A complete reference implementation and independently reviewed concrete estimates are absent. The source paper is preserved conceptually in the sections below, with newly identified caveats and theorems made explicit.

# Abstract

SG-DIFRA is an attack-driven experimental key-encapsulation proposal constructed by separating public nonlinear constraint-system geometry (NCSG), secret incidence, and a hidden generalized Reed–Solomon (GRS) label system. Its earlier Boolean-fiber design leaked period-pair linear relations; dense labeling removed those relations but did not protect a shared planted secret; secret incidence repaired public-fiber correlation but an initial low-noise binary ciphertext was broken by nearly clean information sets and low-weight hidden-code dependencies. The archived 2026 large-field iteration employed symbols from $K=\mathbb F_{2^{10}}$, a hidden length-$M$, dimension-$u$ GRS code, and independently sampled $K$-symmetric symbol error of probability $\nu=3/16$. Algebraic identities establish exact fiber regularity, derivative entropy, planted-row independence through weight $u$, and finite correctness bounds.

This revision supplies a further exact result: after canonical flattening, the NCSG predicates and targets are statistically independent of the public label matrix, and the master secret can be eliminated from the decryption key without changing any decapsulation outcome. Consequently the proved NCSG worst-case facts do not imply the encryption security of this construction. A second issue is that the fixed field forces $M\le1024$, so three finite parameter records do not instantiate a growing asymptotic security family. The archived iteration's one-bit security is only a conditional game-hybrid statement assuming **MDS-HBCE** and **$1024$-ary LPN**, neither of which has been justified by a concrete security estimator or reduction to an established problem. The resulting contribution is a transparent cryptanalytic case study and falsifiable construction proposal, **not a proven post-quantum KEM**.

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


## 4.1 New exact affine-line leakage in every ternary MaxEnt fiber

The source's maximum-entropy theorem is correct as an entropy statement **over the image of a fixed finite-difference operator**. It does not imply that the sampled public fibers resemble random subsets. At the very profile parameters originally proposed, a deterministic geometric dependency remains.

**Theorem 4.1 (canonical affine-line decomposition of each fiber).**
Let $p=3$, $k>d\ge1$, $r=k-d$, $A\in GL_r(\mathbb F_3)$, $B\in GL_k(\mathbb F_3)$, $a\ne0$ in $\mathbb F_3^d$, and $Q_0:\mathbb F_3^d\to\mathbb F_3^r$ be an arbitrary table. For
$$
f(x)=Au_L+\Delta_a Q_0(u_R),\qquad (u_L,u_R)=Bx,
$$
and any target $b\in\mathbb F_3^r$, the fiber $f^{-1}(b)$ is the **disjoint union of $3^{d-1}$ affine lines**, each containing exactly three points in $\mathbb F_3^k$. Every such line $\{x_0,x_1,x_2\}$ satisfies
$$
x_0+x_1+x_2=0\quad\text{in }\mathbb F_3^k.
$$
In particular, every public fiber contains at least $3^{d-1}$ distinct three-point zero-sum subsets. The fibers cannot be treated as random affine-free subsets.

**Proof.** Put $g=\Delta_aQ_0$. The $3^{d-1}$ cosets $z+\langle a\rangle$ partition the right-block space. The source's exact telescoping identity gives
$$
g(z)+g(z+a)+g(z+2a)=0.
$$
For any triple $g_0,g_1,g_2$ of elements of a vector space over $\mathbb F_3$, the identity $g_0+g_1+g_2=0$ is equivalent to $g_j=g_0+j(g_1-g_0)$ for $j=0,1,2$. Thus, as $u_R$ runs along one $a$-coset, $g$ is *affine-linear in the line parameter* $j$. Since the fiber equation uniquely specifies
$$
u_L(j)=A^{-1}(b-g(z+ja))
=A^{-1}(b-g(z))-jA^{-1}(g(z+a)-g(z)),
$$
the paired points $(u_L(j),z+ja)$ form an affine line in $\mathbb F_3^k$. The invertible linear map $B^{-1}$ maps affine lines to affine lines. Distinct right cosets yield disjoint lines. There are $3^{d-1}$ of them, covering all $3^d$ points. Summing the three points of any affine line over characteristic three gives zero. $\square$

**Corollary 4.1a (efficient public enumeration of dependencies).** Given the complete public fiber as an enumerated set $S$, every three-point zero-sum subset can be found without knowing $A,B,Q_0,a$ by iterating pairs $x,y\in S$, $x\ne y$, and checking if $-x-y\in S$. Hash-set implementation uses $O(|S|^2\,k)$ field operations. If $S$ is already published, this is polynomial in its *actual input size*, irrespective of how the internal table was sampled.

**Corollary 4.1b (conditional break of any affine ternary row labeling).** Suppose a *new candidate* uses public ternary labels $h(x)=Lx+c$ and encrypts zero with ternary inner-product observations plus independent $\mathbb F_3$-symmetric errors of nonzero probability $\nu$, while encrypting one using independent uniform $\mathbb F_3$ symbols. For any public affine-line triple, the sum of zero ciphertext symbols equals the sum of just three errors, whereas the same sum for one is uniform. Write $\alpha=1-3\nu/2$. The public statistic $Z=[v(x_0)+v(x_1)+v(x_2)=0]$ satisfies
$$
\Pr[Z=1\mid b=0]=\frac{1+2\alpha^3}{3},\quad
\Pr[Z=1\mid b=1]=\frac13,
$$
giving a one-event gap of $2|\alpha|^3/3$. At $\nu=3/16$ this gap is exactly $2(23/32)^3/3\approx0.24754$, already overwhelming for a basic distinguisher.

**Proof.** Affinity implies $\sum_j h(x_j)=L\sum_jx_j+3c=0$ in $\mathbb F_3$. Thus the inner-product term cancels. The Fourier coefficient of each independent $\mathbb F_3$-symmetric error at either nontrivial character is $1-3\nu/2$. Three independent errors have nontrivial coefficient $\alpha^3$, yielding zero-sum probability $(1+2\alpha^3)/3$ by Fourier inversion. A sum including one uniform ternary symbol is uniform. $\square$

**Scope.** This corollary is **not a break of the historical $K=\mathbb F_{2^{10}}$ version**: its dense field labels were sampled independently of assignment vectors, so the premise $h(x)=Lx+c$ over $\mathbb F_3$ fails. The theorem instead shows that replacing those labels with an apparently 'NCSG-native' *affine* assignment encoding would resurrect the old short-relation leakage, now as **three-point** rather than Boolean four-point constraints. Independent dense labels avoid this algebraic leak only by making NCSG geometry cryptographically removable, as proved in Section 6. Both design traps must be avoided *simultaneously* in any genuine NCSG-only successor.

**Reproduction on the exact original local parameters.** The script \`research-2028/attacks/ternary_affine_line_leakage.py\` samples random valid $A,B,Q_0$ and checks all three recorded $(k,d)$ choices $(5,3),(7,4),(9,5)$ under three independent seeds each. It confirms disjoint partitions into $9,27,81$ affine three-point lines for fibers of size $27,81,243$, respectively, and enumerates public triples using only $S$. These are fully specified local finite tests and an exact symbolic proof, not global KEM security experiments.


# 5. Archived 2026 hidden-MDS label construction (not the new candidate)

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

# 7. Assumption boundary and conditional game argument

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

# 11. Three archived research profiles (not verified for a new NCSG design)

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

# 12. Further structural cryptanalysis toward NCSG-only security

## 12.1 Serious bandwidth and storage problem in all three profiles

The matrix $H$ is dense, has $q=m3^d$ rows and $N$ coordinates in $K=\mathbb{F}_{2^{10}}$. Any faithful 10-bit-per-coordinate representation requires at least $10qN$ bits. The message ciphertext has $\ell T_{\mathrm{rep}}$ full vectors of $q$ field symbols, so even perfect cross-symbol packing requires at least $10q\ell T_{\mathrm{rep}}$ bits. For $T_{\mathrm{rep}}=7$ the arithmetic is:

| Source profile | Labels | Public label matrix (bytes) | One KEM ciphertext (bytes) |
|:--|--:|--:|--:|
| SGD-R1 | 27,648 | 22,118,400 | 77,414,400 |
| SGD-R2 | 124,416 | 149,299,200 | 487,710,720 |
| SGD-R3 | 497,664 | 796,262,400 | 2,786,918,400 |

The original profiles consequently require roughly 73.83 MiB, 465.12 MiB and 2,657.81 MiB of ciphertext **before** framing or extra metadata. These sizes are exact *lower bounds* from the original algorithms, not implementation measurements or a weak-attack estimate. A new compression claim would need to show correctness and security after the changed ciphertext distribution. An external KEM or combiner would not repair this construction's bandwidth defect.

## 12.2 Independent reduced-parameter planted-subspace recovery experiment

The GRS proof says no relation involving $\le u$ planted rows exists. It also implies that $u+1$ planted rows are dependent. This is not automatically a security guarantee: an adversary can enumerate one candidate per group, test the rank, identify a planted $u+1$-tuple, and then recover additional planted rows by checking membership in the discovered dimension-$u$ subspace. The search is not efficient for the proposed full parameters, but **the mechanism exists** and is tested on small, exact $\mathbb F_{2^{10}}$ instances.

In the accompanying `toy_hidden_mds_attack.py`, with $m=6$ buckets of size $B_0=3$, $M=5$, $u=3$, and ambient $N=6$, the attack enumerates group sets and candidate positions until finding a rank-three set of four labels; extending the recovered span identifies all five planted labels. This is a regression against too-strong security narratives; toy performance must not be extrapolated into a finite security-level claim. The attack cost increases combinatorially for the larger parameters and is not a measured full-profile break.

## 12.3 Profile-specific attack and proof matrix

| Question | Mathematically established | Still missing |
|:--|:--|:--|
| Are public NCSG fibers regular? | Exactly $3^d$ selected points per fiber | None for this local identity |
| Is the master secret $s$ hidden? | Yes, $I(s;pk)=0$ | Its absence does not imply encrypted-message secrecy |
| Can $s$ be removed without changing decryption? | Yes, exact functional equivalence | New genuine NCSG dependence if desired |
| Are planted rows independent up to $u$? | Yes, for full-rank $T$ | Hardness of finding the hidden subspace |
| Are the source finite correctness tails small? | Yes, under ideal independent error and decoder assumptions | End-to-end implementation validation |
| Is standalone SG-DIFRA IND-CPA? | Only a reduction conditional on unproved MDS-HBCE and $\mathbb F_{1024}$-LPN | Proof of those premises or independent finite estimator |
| Is standalone SG-DIFRA QROM IND-CCA? | Not established | An explicit transform reduction with losses and failure handling |
| Is a standalone NCSG-only KEM proven quantum IND-CCA? | No | A complete new trapdoor/CPA proof and quantum CCA transform |

## 12.4 Rejection of all borrowed KEM components for the active research direction

The author's design constraint is now explicit: **the next SG-DIFRA candidate must use its own NCSG-based algebraic trapdoor and encryption channel**. The GRS-coded noisy-linear layer documented in Sections 5–11 remains an **archived research iteration** for mathematical provenance and attack comparisons, not the newly approved active construction. It imports well-known GRS and noisy-linear ideas and fails the intended design-independence criterion. No standardized KEM, parallel fallback, or externally proposed KEM design is an ingredient of the active research direction.

The archived algorithms remain fully described because deleting demonstrated mistakes would conceal essential falsification evidence. **No replacement algorithm is yet certified**. The following two mathematically testable experiments are new NCSG-native directions; we must reject any candidate failing either adversarial test before treating it as a KEM.

## 12.5 NCSG-native two-direction differential compatibility theorem

Let the additive field be $\mathbb{F}_3$, let $a,b\in\mathbb{F}_3^d$ be independent, and define $g_a=\Delta_aQ$ and $g_b=\Delta_bQ$ for a hidden table $Q:\mathbb{F}_3^d\to\mathbb{F}_3^r$. Since translations commute, every realizable pair satisfies the **discrete zero-curl identity**
$$
\Delta_b g_a(x)=\Delta_a g_b(x)
$$
as well as the cyclic period conditions
$$
\sum_{j=0}^{2}g_a(x+ja)=\sum_{j=0}^{2}g_b(x+jb)=0.
$$

**Proposition 12.1 (two-direction integrability).** On every affine coset of the plane generated by $a,b$, the two cyclic line-sum conditions and the zero-curl identity are **necessary and sufficient** for some table $Q$ with $\Delta_aQ=g_a$ and $\Delta_bQ=g_b$. The potential $Q$ is determined up to one additive constant on each coset. In particular, when $d=2$, one scalar-output table has exactly $3^2-1=8$ degrees of freedom in its joint pair of derivatives, and a vector with $r$ outputs has $8r$.

**Proof.** Necessity follows by telescoping along each length-three line and the commutativity of additive translation. For sufficiency, fix one vertex and potential value zero. Define the value at every other vertex by summing the prescribed edge derivatives along any grid path using steps $a,b$. All elementary squares have zero circulation by zero-curl; all winding cycles have zero circulation by the two cyclic line-sum conditions. Every two paths are generated by these elementary cycles and winding cycles. Hence the integral is independent of path. The only freedom is an additive constant on each connected plane coset. For $d=2$, the kernel of the joint derivative map is the one-dimensional space of constant tables, yielding rank $9-1=8$ by rank-nullity. $\square$

**Theorem 12.1a (joint derivative image dimension).** More generally, let $p$ be prime, $a_1,\ldots,a_t$ linearly independent in $\mathbb{F}_p^d$, and $Q:\mathbb{F}_p^d\to\mathbb{F}_p^r$. Then the joint finite-difference operator
$$
D_AQ=(\Delta_{a_1}Q,\ldots,\Delta_{a_t}Q)
$$
has kernel dimension $r p^{d-t}$ and image dimension
$$
\dim_{\mathbb{F}_p}\mathrm{Im}(D_A)=r(p^d-p^{d-t}).
$$
For a uniformly sampled $Q$, the joint derivative tuple is uniformly distributed on this image and has Shannon entropy
$$
H(D_AQ)=r(p^d-p^{d-t})\log_2 p.
$$
Every tuple in the image determines the original potential up to one freely chosen additive constant per output coordinate and per coset of $\mathrm{span}\{a_1,\ldots,a_t\}$, recoverable by graph traversal in time polynomial in the published table size.

**Proof.** $D_AQ=0$ iff $Q$ is invariant under translation by each $a_i$, equivalently under their span $L$ of size $p^t$. The $p^{d-t}$ distinct $L$-cosets can each be assigned any independent value in $\mathbb{F}_p^r$, giving kernel dimension $rp^{d-t}$. The table space has dimension $rp^d$; rank-nullity gives the image dimension. A uniform input of a linear map is uniform on its image. Given a consistent derivative tuple, select one root in each coset and integrate along the $a_i$ edges; consistency is guaranteed for tuples in the image. $\square$

**Security corollary (public-potential leakage).** If all t directional derivative tables are published, the quotient of the hidden potential by the coset-constant kernel is **computable in polynomial time**. Additional published independent directions shrink the ambiguity from $rp^{d-1}$ (one direction) toward $r$ (full-dimensional spanning set). Therefore a cryptographic design cannot claim growing directional diversity automatically increases *potential secrecy*: for complete public derivatives the opposite can happen. This is exact finite-dimensional leakage, not a complexity assumption.

**Caution.** Public checks of zero-curl and line-sums are *efficient*. They are algebraic consistency conditions, not a hardness reduction. A secret potential cannot be made difficult merely by publishing its two directional derivative tables: the constructive proof gives a polynomial-time recovery method up to additive constants. The accompanying exact finite fixture integrates one hundred random ternary tables and rejects deliberately inconsistent derivatives.

## 12.6 New rejected NCSG-witness ciphertext: an exact public linear-algebra attack

Consider directly coupling the secret $s\in\mathbb{F}_3^n$ to public NCSG local relations $r_i(X)=f_i(X_{\mathcal{N}(i)})-b_i$ where $b_i=f_i(s_{\mathcal{N}(i)})$. This repairs the earlier defect that public geometry is completely independent of the hidden witness, but it reintroduces the shared-secret public-target bias described in Section 2. **Coupling is necessary but not sufficient for security.**

A natural original-design experiment is to encode zero as a polynomial identity vanishing at $s$,
$$
C_0(X)=\sum_{i=1}^m h_i(X)r_i(X),\quad \deg h_i\le D,
$$
and encode one as an independently uniform coefficient vector for degree at most $D+\max_i\deg r_i$. The private key can evaluate $C_b(s)$ and test for zero. However, **this mechanism is insecure** even if recovering the witness $s$ is difficult.

**Theorem 12.2 (public ideal-span distinguisher).** Let $t=D+\max_i\deg r_i$ and $V_t$ be the coefficient-vector space of degree-at-most-$t$ polynomials in $n$ variables over $\mathbb{F}_3$. Let
$$
W_D=\mathrm{span}\big\{X^\alpha r_i(X):1\le i\le m,\ |\alpha|\le D\big\}\subseteq V_t.
$$
In fact, **$W_D\neq V_t$ necessarily holds** whenever the intended secret witness $s$ exists: each generator $X^\alpha r_i$ vanishes at $s$, while the constant polynomial one does not. An attacker knowing only the public polynomials $r_i$ distinguishes $C_0$ from a uniform coefficient vector with success probability at least
$$
1-\frac12 3^{\dim W_D-\dim V_t}
$$
under equiprobable bits, and at least $5/6$ because $\dim V_t-\dim W_D\ge1$. The attack is polynomial in $\dim V_t$ and $m\binom{n+D}{D}$ and is therefore polynomial in the security parameter whenever $t$ is constant.

**Proof.** Publish all coefficient vectors of monomial multiples $X^\alpha r_i$ as rows of a matrix. By construction every $C_0$ lies in its row span $W_D$; Gaussian elimination tests span membership without knowing $s$. Since evaluation at $s$ is a nonzero linear functional on $V_t$, every generator lies in its kernel and the rank is strictly smaller than $\dim V_t$. A uniform coefficient vector lies in $W_D$ with probability exactly $3^{\dim W_D-\dim V_t}$. Classify membership as zero, nonmembership as one. Correct-classification probability is $\tfrac12(1+1-3^{\dim W_D-\dim V_t})$. The coefficient space has dimension $\binom{n+t}{t}$; for fixed $t$ all matrix dimensions are polynomial in $n$. $\square$

The companion *GF(3) attack script* implements exactly this theorem on three-variable planted relations, with 150 samples of each class. It verifies that all zero ciphertexts are recognized by public row-space membership, including when the hidden witness correctly evaluates the polynomial to zero. This is an end-to-end **distinguishing break of the proposed experiment**, not a proof that all possible NCSG KEMs are impossible.

**Why naive fixes fail.** Sampling different low-degree multipliers only changes the distribution *inside* $W_D$, not the public membership test. Using more local constraints increases the public matrix and may even make its span full, at which point the zero and one distributions and private decoding must be reanalysed. Supplying an unexpanded arithmetic circuit exposing the $h_i$ directly reveals its factorization. Increasing $D$ until the coefficient space is exponential makes naive dense ciphertext emission infeasible. Neither additive one-time masks that decouple $s$ from the public key nor introducing an unaudited hard-decomposition assumption proves security. Every such redesign needs a new exact security game.

## 12.7 NCSG-only development gates, not an unproved 'secure KEM'

A scientifically admissible replacement for Sections 5–11 must exhibit all of the following *simultaneously*: (1) a genuine joint dependence of public-key distribution and decryption on an NCSG witness (the projection theorem of Section 6 must no longer apply); (2) a public polynomial-time encryption algorithm that does not require the witness; (3) a secret polynomial-time decapsulation algorithm; (4) a public ciphertext distribution resisting simple degree, support, module-membership, rank, derivative-curl, spectral, tensor and candidate-witness tests; (5) a proven IND-CPA reduction to a *precisely stated and independently evaluated* original average-case problem; (6) a complete transform proof under explicit quantum-oracle assumptions for the target IND-CCA security; (7) an efficient, fully instantiated asymptotic sampler and nontrivial fixed parameters.

**No candidate in the current repository meets these seven gates**. It would be mathematically false to declare new SGD-R1/R2/R3 security levels or a complete KEM merely by changing the underlying distribution's name. Three future profiles should be derived **after** an eligible construction and costed against all available classical and quantum attack algorithms. The three historical profiles in Section 11 remain attack baselines, not validated instantiations of the new direction.

## 12.8 Novelty boundary and venue target

The preceding integrability lemma follows from finite difference calculus; the row-span distinguisher is elementary algebra. Their statements are rigorously demonstrable **but their originality as publishable research results is not established**. The high-corruption CSP encryption literature, including Hair–Sahai (2026), is a relevant conceptual predecessor for secret-witness problems. This project must not represent planted constraints as an entirely unprecedented idea. The structural GRS/Schur-square attack literature provides a negative boundary on the *archived* iteration, not borrowed protection for the new one. A separate novelty review and external cryptanalyst assessment are required.

**Conference calendar:** EUROCRYPT 2027's published paper submission deadline was 17 September 2026, which has already passed by this draft's date. EUROCRYPT 2028 is the forward research target from the preceding project discussion; no verified 2028 CFP/deadline has been recorded. Submission and acceptance cannot be promised.

The new NCSG-only tests and research status are documented in:
\`research-2028/math/multidirection_cocycle.py\`,
\`research-2028/attacks/public_ideal_membership_break.py\`, and
\`research-2028/NCSG_ONLY_RESEARCH_STATUS.md\`.

# 13. Verification, limitations and responsible next steps

The accompanying Python scripts verify the field modulus, exhaustive Boolean truth table, exact ternary affine-line partitions for all three source profile geometries, symbolic ternary triple leakage, small GRS row independence, functional equivalence after replacing $s$, a toy clean-basis adversary on $1024$-ary noisy samples, and analytical profile bounds. Such checks are finite evidence for corresponding algebraic properties; they do **not** establish IND-CPA or IND-CCA security against arbitrary efficient adversaries.

A publication-ready new cryptographic claim would require at least: an executable, byte-exact KEM implementation; independent cryptanalysis of the full public-label distribution and noisy sample problem; reproducible estimators including quantum work, depth and memory; a sound asymptotic parameter family; a complete QROM reduction with explicit concrete losses; a venue-compliant anonymous submission; and explicit treatment of computational/memory cost, malformed ciphertexts, fault and side-channel behavior.

# 14. Conclusion

The successive SG-DIFRA repairs address specific demonstrated weaknesses, and the surviving finite-field mathematics remains valuable. Nevertheless the proposed ciphertext-security engine is a hidden-MDS-label problem combined with noisy linear samples; the NCSG geometry is statistically and functionally redundant for security under the actual generator. The strong statement supported by this draft is therefore *attack-driven cryptographic analysis plus new mathematically checked NCSG-only obstructions*, not a formally verified post-quantum KEM. The MDS construction is retained for negative and historical study rather than promoted as the user's novel active design. Any security promotion needs new mathematics and independent cryptanalysis, not a change of adjectives.

# References

9. Hair and Sahai, *Public Key Encryption from High-Corruption Constraint Satisfaction Problems*, arXiv:2604.10479 (conceptual prior-art comparison, **not** an ingredient).
10. Couvreur et al., *On the Structure of the Schur Squares of Twisted Generalized Reed-Solomon Codes and Application to Cryptanalysis*, PQCrypto 2025 (archived iteration attack context).


1. I. S. Reed and G. Solomon, "Polynomial Codes over Certain Finite Fields," *J. Soc. Indust. Appl. Math.*, 8(2), 300–304, 1960. https://doi.org/10.1137/0108018
2. S. Gao, "A New Algorithm for Decoding Reed–Solomon Codes," in *Communications, Information and Network Security*, 2003.
3. A. Couvreur et al., "Distinguisher-Based Attacks on Public-Key Cryptosystems Using Reed–Solomon Codes," *Designs, Codes and Cryptography*, 73, 641–666, 2014. https://arxiv.org/abs/1307.6458
4. J. Ge, H. Liao, and R. Xue, "Measure-Rewind-Extract: Tighter Proofs of One-Way to Hiding and CCA Security in the Quantum Random Oracle Model," *ASIACRYPT 2024*, 2024.
5. N. Bindel et al., "Tighter Proofs of CCA Security in the Quantum Random Oracle Model," *TCC 2019*, 2019.

8. Source manuscript: Girish Nallan Chakravathy and Sreedevi Kannan, *SG-DIFRA: An Attack-Driven NCSG KEM with Secret Incidence and MDS Coding*, author-provided 26-page PDF, October 2026.

# Appendix A. Reproduction and claim labels

Run \`python formal-verification-and-mathematical-proofs/test_sg_difra.py\` and \`python formal-verification-and-mathematical-proofs/profile_bounds.py\`. A passing run is evidence only for the printed fixtures and calculations. The active construction status is **NCSG-ONLY RESEARCH DIRECTION — NO VALIDATED KEM OR SECURITY LEVELS**.

# Appendix B. Submission caution

EUROCRYPT 2028 is the research target. An official 2028 CFP and deadline have not been verified as of 10 October 2026. The previous EUROCRYPT 2027 deadline was 17 September 2026. The original paper and this credited research version are *not anonymous*. This revision is not a 2027 submission. For a future double-blind venue, apply the current published formatting, author-identification, repository and AI-use rules; do not upload the named version as an anonymous submission. Verify all bibliographic records directly from publishers before submission.
