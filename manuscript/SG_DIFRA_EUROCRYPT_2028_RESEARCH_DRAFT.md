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

**Round-5 security finding.** In the archived fixed-GF(1024) design, recovering one public rank-$u$ planted frame can be extended into recovery of all hidden label positions and exact public emulation of the secret bounded-distance decoder. Under explicitly polynomial public-key size and growing ambient dimension, this becomes a uniform polynomial-time honest-session-key recovery attack when the original KEM is correct. This is stronger than a public-key distinguisher, but it remains astronomically expensive at the three frozen finite profiles; it does not provide a secure NCSG-only replacement.

**Round-6 structural result.** A hidden $(r+1)$-dimensional affine-linearity subspace of each original publicly evaluable ternary NCSG predicate can be recovered by exhaustive public second-difference tests, with explicit tiny sampling-failure bounds for R1/R2/R3. This further rules out relying solely on a concealed local coordinate direction as a future cryptographic trapdoor; it does not change the independent dense-label ciphertext security game.

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

**Theorem 4.2 (exact first moment of the public affine-line statistic).** For $S=f^{-1}(b)$ sampled exactly as Section 4 with uniform $Q_0$, set $s_0=3^d$, $r=k-d$, and let $L(S)$ be the number of unordered three-point affine lines contained in the publicly enumerable $S$. The exact expected count is
$\mathbb E_{\mathrm{NCSG}} L(S)=3^{d-1} + \bigl[s_0(s_0-1)/6-3^{d-1}\bigr]3^{-r}$.
For a *uniform* subset $U$ of the same size $s_0$ chosen from $\mathbb F_3^k$ of size $N_0=3^k$, the exact expectation is
$\mathbb E_{\mathrm{unif}} L(U)=s_0(s_0-1)(s_0-2)/(6(N_0-2))$.
For the three original source local geometries, the resulting pairs (NCSG; uniform) are respectively **(21; 12.13693)**, **(66; 39.04805)**, and **(201; 120.01631)**.

**Proof.** Every three-point affine line in $S$ projects injectively under the right-block projection $Bx\mapsto u_R$ because each right block has a unique left-block point. Thus any such line corresponds to exactly one affine line in $\mathbb F_3^d$. There are $s_0(s_0-1)/6$ possible right lines. For the $3^{d-1}$ lines parallel to $a$, telescoping forces $\sum g=0$ identically, so all lift to affine lines in the fiber. For any other right-line direction $h$ linearly independent of $a$, the three arguments $z,z+h,z+2h$ and their three $a$-shifts are pairwise distinct in the table of $Q_0$. Therefore the difference of the corresponding table-value sums is uniform in $\mathbb F_3^r$, and the probability of the necessary and sufficient equality $\sum g=0$ is precisely $3^{-r}$. Summing expectations proves the NCSG identity. For a uniformly sampled $s_0$-subset of the $N_0$-point ambient space, each one of the $N_0(N_0-1)/6$ possible lines is present with probability $(s_0)_3/(N_0)_3$. Simplifying gives the displayed uniform-subset identity. $\square$

**Practical scope and first-moment limitation.** The public line-count statistic itself can be computed in quadratic time in the published fiber size. For deterministic reproducibility, the accompanying script draws 30 valid MaxEnt and 30 uniform same-size fibers per source geometry and reports midpoint-threshold classification rates in the fixed seeds. **A difference of expectations establishes nonidentity of the two distributions, but does not alone guarantee a particular single-instance success probability without variance control.** The experiment reports *empirical* performance separately and does not equate distinguishing public NCSG fibers from random subsets with breaking encrypted messages in the archived dense-label KEM. In particular, NCSG was not claimed in the source to be a pseudorandom-subset generator.

**Corollary 4.1b (conditional break of any affine ternary row labeling).** Suppose a *new candidate* uses public ternary labels $h(x)=Lx+c$ and encrypts zero with ternary inner-product observations plus independent $\mathbb F_3$-symmetric errors of nonzero probability $\nu$, while encrypting one using independent uniform $\mathbb F_3$ symbols. For any public affine-line triple, the sum of zero ciphertext symbols equals the sum of just three errors, whereas the same sum for one is uniform. Write $\alpha=1-3\nu/2$. The public statistic $Z=[v(x_0)+v(x_1)+v(x_2)=0]$ satisfies
$$
\Pr[Z=1\mid b=0]=\frac{1+2\alpha^3}{3},\quad
\Pr[Z=1\mid b=1]=\frac13,
$$
giving a one-event gap of $2|\alpha|^3/3$. At $\nu=3/16$ this gap is exactly $2(23/32)^3/3\approx0.24754$, already overwhelming for a basic distinguisher.

**Proof.** Affinity implies $\sum_j h(x_j)=L\sum_jx_j+3c=0$ in $\mathbb F_3$. Thus the inner-product term cancels. The Fourier coefficient of each independent $\mathbb F_3$-symmetric error at either nontrivial character is $1-3\nu/2$. Three independent errors have nontrivial coefficient $\alpha^3$, yielding zero-sum probability $(1+2\alpha^3)/3$ by Fourier inversion. A sum including one uniform ternary symbol is uniform. $\square$

**Scope.** This corollary is **not a break of the historical $K=\mathbb F_{2^{10}}$ version**: its dense field labels were sampled independently of assignment vectors, so the premise $h(x)=Lx+c$ over $\mathbb F_3$ fails. The theorem instead shows that replacing those labels with an apparently 'NCSG-native' *affine* assignment encoding would resurrect the old short-relation leakage, now as **three-point** rather than Boolean four-point constraints. Independent dense labels avoid this algebraic leak only by making NCSG geometry cryptographically removable, as proved in Section 6. Both design traps must be avoided *simultaneously* in any genuine NCSG-only successor.

**Corollary 4.1c (message recovery after aggregation, still conditional on an insecure label design).** Suppose all $m$ public buckets of the *hypothetical ternary-affine-label encryption* from Corollary 4.1b are used to encode one message bit, with independent per-coordinate symbol errors and all coordinates independently uniform under the one-bit distribution. Choose the guaranteed $3^{d-1}$ disjoint affine lines within each bucket. Then there are $T=m3^{d-1}$ **disjoint** public three-point tests whose indicators are independent, even though the encryption randomness $t$ is shared: the affine-label contributions cancel deterministically in every triple. Let $\Delta=2|1-3\nu/2|^3/3$. By a midpoint-threshold classifier and Hoeffding's inequality, the error probability for **each** bit class is at most $\exp(-T\Delta^2/2)$. At $\nu=3/16$, importing only the *geometry and bucket counts* of the three source profiles into such an insecure ternary-affine experiment would give $T=9{,}216$, $41{,}472$, $165{,}888$, respectively, and corresponding log-base-two error upper bounds approximately $-407.35$, $-1833.09$, and $-7332.37$. These numbers show the **severity of the attack on that rejected experiment**, and **are not** security levels, correctness estimates or attacks on the source $K=\mathbb F_{2^{10}}$ independent labels.

**Proof.** A full partition into disjoint triples is supplied by Theorem 4.1. Each event depends only on its own three independent error variables for bit zero, or on its own three independent uniform ciphertext variables for bit one; the common secret-noise-free inner product vanishes by the public triple relation. Their Bernoulli event means differ by $\Delta$. For each class, Hoeffding bounds crossing the midpoint by $\exp(-2T(\Delta/2)^2)$. $\square$

**Reproduction on the exact original local parameters.** The script \`research-2028/attacks/ternary_affine_line_leakage.py\` samples random valid $A,B,Q_0$ and checks all three recorded $(k,d)$ choices $(5,3),(7,4),(9,5)$ under three independent seeds each. It confirms disjoint partitions into $9,27,81$ affine three-point lines for fibers of size $27,81,243$, respectively, and enumerates public triples using only $S$. These are fully specified local finite tests and an exact symbolic proof, not global KEM security experiments.



## 4.2 Round-4 theorem: exact finite public-fiber distinguisher from three parallel lines

The original 2026 manuscript proves exact balanced fibers and maximal entropy for the finite differences of a fixed direction. Neither property implies pseudorandom public fibers, and the preceding affine-line theorem left a stronger question unresolved: do independently sampled NCSG fibers satisfy a **public test with a large *provable finite-parameter* distinguishing gap**, rather than just different expectations? The answer is yes. This statement is an attack on a **hypothetical pseudorandom-fiber claim**; it is *not* an attack on the ciphertext of the archived dense-label KEM.

Let $S=f^{-1}(b)\subseteq\mathbb F_3^k$ with $f$, $A$, $B$, $a$ and uniform potential table $Q_0$ as in Section 4, and let $r=k-d$. Let $\mathsf{Uniform}_{k,d}$ denote a uniformly chosen subset of $\mathbb F_3^k$ of exactly $s=3^d$ distinct elements. Define the deterministic, public-only test $D(S)$ to return one if and only if **three distinct affine three-point lines in $S$ are parallel** (have the same one-dimensional direction subspace). The test uses only the enumerated points $S$, with no knowledge of $A,B,a,Q_0,b$ or any secret incidence.

**Lemma 4.3 (independent uniform hidden directions).** In the exact MaxEnt sampler, each of the $L=3^{d-1}$ guaranteed lines from Theorem 4.1 has direction

$$
v_z=B^{-1}\bigl(-A^{-1}T_z,\ a\bigr),\qquad
T_z=Q_0(z)+Q_0(z+a)+Q_0(z+2a),
$$

where $z$ ranges over the distinct cosets of $\langle a\rangle$ in $\mathbb F_3^d$. The $T_z$ are **independent uniform** vectors of $\mathbb F_3^r$. Conditional on the sampled $A,B,a$, the associated projective directions are independent uniform among exactly $m_0=3^r$ distinct directions, all represented in the affine coset

$$
B^{-1}(\mathbb F_3^r\times\{a\})\subseteq\mathbb F_3^k.
$$

**Proof.** Put $g=\Delta_aQ_0$. The increment from the first point of an $a$-line to the second has left-block value $-A^{-1}[g(z+a)-g(z)]$. In characteristic three,

$$
g(z+a)-g(z)=Q_0(z+2a)-2Q_0(z+a)+Q_0(z)
=Q_0(z)+Q_0(z+a)+Q_0(z+2a).
$$

Distinct $a$-orbits involve disjoint entries of the uniformly sampled potential table, so their independent sums are uniform in $\mathbb F_3^r$. Applying an invertible linear map preserves uniformity and independence. Different vectors in the displayed affine coset cannot represent the *same* projective direction: a proportionality scalar over $\mathbb F_3$ must preserve the fixed, nonzero right coordinate $a$, hence equals one. Thus precisely $3^r$ direction possibilities exist. $\square$

**Theorem 4.4 (exact finite-statistical distinguishing bounds).** Let $P_1=\Pr[D(S)=1]$ for an NCSG MaxEnt fiber and $P_0=\Pr[D(U)=1]$ for $U\leftarrow\mathsf{Uniform}_{k,d}$. Set $L=3^{d-1}$, $m_0=3^r$, $n=3^k$, $s=3^d$, and for each integer $j$ put $a_j=L-2j$ and $c_j=m_0-a_j-j$. Then

$$
P_1\ \ge\ 1-\frac{1}{m_0^L}
\sum_{\substack{0\le j\le\lfloor L/2\rfloor\\c_j\ge0}}
\frac{m_0!\,L!}{a_j!\,j!\,c_j!\,2^j},
$$

and independently

$$
P_0\ \le\ \frac{n-1}{2}{n/3\choose3}
\frac{(s)_9}{(n)_9},\qquad
(x)_t=x(x-1)\cdots(x-t+1).
$$

Consequently $D$ is a classical, efficiently computed **single-fiber statistical distinguisher** with advantage $|P_1-P_0|$ at least the difference of the two displayed bounds whenever positive. The test runs in $O(ks^2)$ field operations using point hashing and normalized projective directions.

**Proof.** By Lemma 4.3, assign each of the $L$ forced affine lines an independent uniform direction among $m_0$ possibilities. If any direction is chosen at least three times, three distinct forced lines inside $S$ are parallel, so $D(S)=1$. The exact probability that no direction is used more than twice follows by counting $j$ double-occupied direction bins, $a_j=L-2j$ singly occupied bins and $c_j=m_0-a_j-j$ empty bins. For each permitted $j$, the number of assignments of the $L$ *labeled* affine lines is $m_0!/(a_j!\,j!\,c_j!)\cdot L!/2^j$. Divide by $m_0^L$ and take the complement; any accidental extra lines in $S$ can only increase the detection probability.

For the uniform-subset null, there are exactly $(n-1)/2$ one-dimensional direction subspaces in $\mathbb F_3^k$. For any direction, the ambient space partitions into $n/3$ parallel three-point affine lines; selecting three distinct lines produces nine distinct points. Hence there are $(n-1)/2\cdot{n/3\choose3}$ triples of pairwise parallel ambient lines. The probability that nine specified distinct points occur in a uniformly sampled size-$s$ subset is exactly $(s)_9/(n)_9$. The expected number of fully contained triples is therefore the second displayed expression, and Markov's inequality bounds the chance of at least one such triple. The algorithm enumerates each public affine line using pairs of points and the characteristic-three identity $x+y+z=0$, normalizes a nonzero direction by setting its first nonzero coordinate to one, and groups lines by direction. $\square$

**Exact source-parameter consequences.** These bounds concern exactly the three original ternary local profiles, without parameter interpolation or untested asymptotics:

| Profile $(k,d,r)$ | $L$ | $m_0$ | Source $P_1\ge$ | Null $P_0\le$ | Advantage $\ge$ |
|:--|--:|--:|--:|--:|--:|
| R1 $(5,3,2)$ | 9 | 9 | 0.554737 | 0.006904 | 0.547832 |
| R2 $(7,4,3)$ | 27 | 27 | 0.947051 | 0.005910 | 0.941141 |
| R3 $(9,5,4)$ | 81 | 81 | 0.999912 | 0.002660 | 0.997252 |

All displayed decimal values are rounded to six places; exact rational bounds and their full-precision evaluation are certified by the accompanying script.

For these choices $d-1=r$, so the number of independently assigned forced lines equals the number of available direction types. Thus the occupancy phenomenon strengthens rapidly across the profiles. The largest original R3 public fiber is distinguishable from a uniformly sampled same-size subset by this **purely geometric single-fiber test** with provable event-probability gap greater than $0.9972$. No secret-incidence data or plaintext ciphertext is required.

**Executable verification and attack boundary.** The reproducible standard-library script \`research-2028/attacks/ternary_parallel_line_collision.py\` computes the two bounds as *exact rational numbers*, verifies the full $3^9=19{,}683$ scalar table ensemble for $(d,r)=(2,1)$ (where precisely $2{,}187$ tables force three parallel lines), and performs an independent public-only $24+24$-fiber Monte Carlo comparison on each original geometry. The exhaustive toy identity checks $2{,}187/19{,}683=1/9$; it cannot replace the general proof. Numerical Monte Carlo detections are diagnostics, not the source of the certified inequalities.

**Cryptographic applicability is explicitly limited.** The archived SG-DIFRA-MDS **Plant and Null label distributions both use the same public NCSG fiber sampler**, and the encrypted labels were independent random $K=\mathbb F_{2^{10}}$ rows except for the hidden MDS replacement. Therefore $D(S)$ has the *same* marginal distribution in both cryptographic games, and this theorem does **not** refute MDS-HBCE or recover an encapsulated key. Indeed, exploiting this public leakage requires a *new* construction that attempts to hide NCSG geometry or assumes NCSG fibers pseudorandom. The original independent dense labeling avoids an assignment-space parity attack only at the price of the previously proved NCSG-removability defect. Neither property establishes a secure, novel NCSG-only KEM, and no claim of novel field-theoretic mathematics relative to prior literature is made here.



## 4.3 Round-6 public recovery of the hidden affine-linearity subspace

The preceding results count public affine lines in **one fiber**. Round 6 studies the stronger original-public-function access model: the original archived key-generation algorithm publishes the local MaxEnt function $f_i$ and publicly enumerates its fiber, so an adversary can evaluate the full local map $f:\mathbb F_3^k\to\mathbb F_3^r$. In the source's actual geometries $k\in\{5,7,9\}$, the entire input space contains only $243$, $2187$, or $19683$ points. Even hiding the matrices $A,B$ and the direction $a$ would not hide a structural subspace of those maps.

Define the full second finite difference along $h\in\mathbb F_3^k$ by

$$
\mathcal S_h f(x)
:=f(x)+f(x+h)+f(x+2h).
$$

Since $-2=1$ in $\mathbb F_3$, this equals $(\mathsf T_h-I)^2f(x)$, where $\mathsf T_hf(x)=f(x+h)$. For any *publicly evaluable* $f$, define its affine-linearity direction set

$$
\mathcal V(f)=
\{h\in\mathbb F_3^k:
\mathcal S_hf(x)=0\ \text{for every }x\in\mathbb F_3^k\}.
$$

**Theorem 4.5 (public recovery with an exact finite sampling-failure bound).** Sample $A\in GL_r(\mathbb F_3)$, $B\in GL_k(\mathbb F_3)$, a nonzero $a\in\mathbb F_3^d$, and an independent uniform potential table $Q_0:\mathbb F_3^d\to\mathbb F_3^r$. Set

$$
f(x)=Au_L+(\mathsf T_a-I)Q_0(u_R),
\qquad (u_L,u_R)=Bx,
\qquad r=k-d,
$$

with $d\ge2$. The hidden $(r+1)$-dimensional linear subspace

$$
V=B^{-1}\bigl(\mathbb F_3^r\times\langle a\rangle\bigr)
$$

is always contained in the publicly computable $\mathcal V(f)$. Moreover

$$
\Pr_{Q_0}[\mathcal V(f)\ne V\mid A,B,a]
\le (3^k-3^{r+1})\,3^{-2r3^{d-2}}.
$$

Thus scanning **all public directions and all public evaluation inputs** recovers $V$ exactly except with the displayed finite probability. This success statement holds uniformly for *every* invertible $A,B$ and every nonzero $a$, and the algorithm does not need any of those sampled coordinates as input.

**Proof.** Write $Bh=(v,b)$ where $v\in\mathbb F_3^r$ and $b\in\mathbb F_3^d$. Since the source term $Au_L$ is affine linear, its second difference vanishes along every $h$, and commuting finite differences gives

$$
\mathcal S_hf(x)
=(\mathsf T_b-I)^2(\mathsf T_a-I)Q_0(u_R).
$$

If $b=0$, this is zero. If $b=a$, the operator equals $(\mathsf T_a-I)^3=\mathsf T_a^3-I=0$. If $b=-a$, then $\mathsf T_b-I=(\mathsf T_a-I)(\mathsf T_a+I)$, so the operator contains the same zero factor $(\mathsf T_a-I)^3$. Both identities use $\mathsf T_a^3=I$ and characteristic three. This proves $V\subseteq\mathcal V(f)$ deterministically, including all of its $3^{r+1}$ elements.

Now fix any $h\notin V$. Its right component $b$ is linearly independent of $a$. An invertible change of right coordinates maps $a,b$ to distinct coordinate basis vectors. On the vector space of scalar tables on $\mathbb F_3^d$, the commuting operator

$$
L_{a,b}=(\mathsf T_b-I)^2(\mathsf T_a-I)
$$

is the tensor product of a one-dimensional first-difference operator of rank two, a one-dimensional squared-difference operator of rank one, and the identity on the remaining $d-2$ dimensions. Consequently its **exact** scalar rank is

$$
\operatorname{rank}_{\mathbb F_3}(L_{a,b})
=2\cdot3^{d-2}.
$$

Each coordinate of the uniformly sampled $Q_0$ is a uniform independent scalar table, so the probability that *all* $r$ output coordinates satisfy $L_{a,b}Q_0=0$ is exactly

$$
\Pr[\mathcal S_h f\equiv0]
=3^{-2r3^{d-2}}.
$$

The event $\mathcal V(f)\ne V$ implies that at least one of the $3^k-3^{r+1}$ exterior directions passes the public all-input zero test. The displayed union bound follows without assuming independence among these candidate directions. $\square$

**Practical enumeration versus asymptotic meaning.** A verifier first evaluates the published function on every element of $\mathbb F_3^k$, then checks $\mathcal S_hf(x)=0$ over every $h,x$. Its worst-case arithmetic cost is $O(kr3^{2k})$, **polynomial in the length of a complete public truth table** but exponential in the length of a succinct $k$-coordinate circuit. A short list of public evaluations can cheaply eliminate most false candidate directions; the implementation uses 32 seeded probe inputs only as a screening optimization and then **checks every input** for every surviving direction. This is not an asserted PPT attack if the function is supplied only as a succinct program with arbitrary growing $k$. For the frozen source geometries it is fully executable.

| Original local profile | $k,d,r$ | Hidden subspace $\dim V$ | Exact finite upper bound on recovery failure |
|:--|:--|--:|--:|
| SGD-R1 | $5,3,2$ | $3$ | $8/19683\approx4.06442\times10^{-4}$ |
| SGD-R2 | $7,4,3$ | $4$ | $3.62169\times10^{-23}$ |
| SGD-R3 | $9,5,4$ | $5$ | $1.70023\times10^{-99}$ |

**Code and independent finite certificates.** The script at research-2028/attacks/public_second_difference_subspace_recovery.py independently constructs source-distributed full public maps with hidden random invertible basis changes, recovers precisely the intended $V$ from *only* their public tables at all three source geometries, and tests the exact subspace dimensions $3,4,5$. Its independent GF(3) elimination computes scalar operator ranks $2,6,18,54$ for $d=2,3,4,5$. Finally it exhaustively enumerates all $3^9=19683$ scalar potentials on the smallest $d=2$ table and finds exactly $2187$ cases where a fixed independent exterior direction spuriously passes the second-difference test, confirming the theorem's $3^{-2}=1/9$ local probability. These numerical checks are reproducibility evidence for an algebraic proof, **not formal end-to-end KEM verification**.

**Consequences and design rejection rule.** Public masking by $B$ is merely a reversible change of coordinates; it does not conceal the intrinsic affine-linearity subspace of a public MaxEnt map. Any new proposal that places essential secrecy *solely* in the direction subspace $V$ fails this test when its public representation enables full evaluation at comparable sizes. **Recovering $V$ does not reveal the entire secret change of basis $B$, a global NCSG assignment $s$, or the archived GF(1024) GRS row labels.** In particular, the original archived KEM's planted/noise labels remain independently sampled conditional on NCSG public data, so this theorem alone is not an IND-CPA or IND-CCA attack on that ciphertext channel. The earlier full-code archival attack (Theorem 9.2) is separately applicable under its explicit asymptotic assumptions. A viable **genuinely original NCSG-only KEM** must derive hardness from a new publicly encryptable and secretly invertible relation that survives these public affine-direction tests; merely raising $k$ without a sampled average-case hardness reduction is not a verified fix.



## 4.4 Round-7 unconditional public local inversion: first differences eliminate the proposed local trapdoor

**Outcome of the Round-6 repair check.** Round 6 established the public recoverability of a hidden $(r+1)$-dimensional second-difference direction subspace. Its theorem and regression tests remained valid, but **the underlying original MaxEnt predicate was not repaired**: that weakness is inherent in the publicly specified function form. Round 7 strengthens the result from probable detection of a hidden direction subspace to **unconditional exact public inversion of every local predicate target** in the explicit-table model. This rules out using *the original local predicate's preimage problem* as the secret inversion trapdoor of a new KEM. It does **not** solve an arbitrary *joint* NCSG constraint system, break the independent GF(1024) dense-label ciphertext directly, or supply a replacement KEM.

Fix the original local publicly evaluable map

$$
f(x)=Au_L+\Delta_a Q_0(u_R),\qquad
(u_L,u_R)=Bx\in\mathbb F_3^r\times\mathbb F_3^d.
$$

Here $A\in GL_r(\mathbb F_3)$, $B\in GL_k(\mathbb F_3)$, $a\ne0$, and $Q_0$ is **arbitrary**, not necessarily uniformly sampled. Define the publicly testable constant-derivative direction set

$$
C(f)=\{h\in\mathbb F_3^k:\ 
f(x+h)-f(x)\text{ is independent of }x\}.
$$

For $h\in C(f)$ let $c_f(h)=f(h)-f(0)$. Unlike Theorem 4.5, this test uses **first differences**, and the result below does not need a distributional probability bound.

**Theorem 4.6 (unconditional public local right inverse).** For every legitimate $A,B,a,Q_0$, the set $C(f)$ is a linear subspace of $\mathbb F_3^k$, and $c_f:C(f)\to\mathbb F_3^r$ is a **surjective linear map**. Consequently a deterministic public-only algorithm, given the complete publicly evaluable truth table of $f$ and any target $t\in\mathbb F_3^r$, outputs an assignment $x_t$ with

$$
f(x_t)=t
$$

**with success probability exactly one**. The algorithm uses at most $O(kr3^{2k}+kr^3)$ elementary field operations for preprocessing and $O(kr+r^3)$ per target with a recovered $r$-element independent increment basis. It never knows or recovers the secret sampled coordinate matrices.

**Proof.** Translation identities show that any pair $h,h'\in C(f)$ satisfies

$$
f(x+h+h')-f(x)
=c_f(h)+c_f(h'),
$$

and hence $h+h'\in C(f)$ and $c_f(h+h')=c_f(h)+c_f(h')$. Negatives and zero are also in $C(f)$, so $C(f)$ is a subspace and $c_f$ is linear. Now consider the private-but-mathematically well-defined left shift space

$$
W_0=B^{-1}(\mathbb F_3^r\times\{0\}).
$$

For every $h\in W_0$, writing $Bh=(v,0)$, one has

$$
f(x+h)-f(x)=Av
$$

**for every** $x$, regardless of $Q_0$ or $a$. Thus $W_0\subseteq C(f)$. The restriction $c_f|_{W_0}$ is a linear isomorphism onto $\mathbb F_3^r$ because $A$ and $B$ are invertible. Therefore the *publicly defined* map $c_f:C(f)\to\mathbb F_3^r$ is necessarily surjective.

The public algorithm enumerates candidate $h$, checks $f(x+h)-f(x)$ over all public inputs $x$, retains only genuinely constant derivatives, and selects $r$ directions $h_1,\ldots,h_r$ whose **public output increments** $c_f(h_j)$ are linearly independent. Such directions exist because the image of $c_f$ is the entire output space. Solve the public linear system

$$
\sum_{j=1}^{r}\gamma_jc_f(h_j)=t-f(0)
$$

and return

$$
x_t=\sum_{j=1}^{r}\gamma_jh_j.
$$

By additivity $f(x_t)=f(0)+c_f(x_t)=t$. This holds for **every target and every potential table**, with no randomized oracle or hardness assumption. $\square$

**Corollary 4.6a (public translation equivalence of all local target fibers).** For *any* two public local targets $b,b'\in\mathbb F_3^r$, a public-only algorithm computes $h$ such that

$$
f^{-1}(b')=f^{-1}(b)+h.
$$

**Proof.** Theorem 4.6 supplies a public $h\in C(f)$ with $c_f(h)=b'-b$. By the definition of $C(f)$, $f(x+h)=f(x)+b'-b$ for **every** $x$. Translation by $h$ is invertible, so it bijectively carries all of $f^{-1}(b)$ onto all of $f^{-1}(b')$. $\square$ This equivalence is stronger than finding a single preimage and needs neither an original secret witness nor a probabilistic generic hardness assumption. It remains **local**: overlapping global constraints cannot generally be translated independently.

**Meaning of the computational bound.** Exhaustively verifying one direction requires $3^k$ function evaluations and there are at most $3^k$ directions. The loose upper bound $O(kr3^{2k})$ is therefore polynomial in the size of an **explicit** truth table, which is appropriate to the original locally enumerated construction: the frozen inputs have sizes $3^5=243$, $3^7=2187$, and $3^9=19683$. This does **not** imply polynomial inversion in the *succinct input dimension* $k$ for an arbitrary circuit representation when $k$ grows. Rather, the original small public local map cannot serve as a hidden trapdoor because valid inverse images can be synthesized openly and reused for all targets after one preprocessing pass. Nor does locally solving every predicate separately necessarily solve overlapping global constraints.

**Theorem 4.7 (exact finite bound for identifying the original left shift space).** For a uniformly independently sampled potential table $Q_0:\mathbb F_3^d\to\mathbb F_3^r$, with $d\ge2$, the hidden $r$-dimensional $W_0$ is not only contained in $C(f)$; except with the following explicitly bounded probability, it **equals** $C(f)$:

$$
\Pr_{Q_0}[C(f)\ne W_0]\ \le\
\frac{2\cdot3^r}{3^{r(3^{d-1}-1)}}+
\frac{(3^d-3)\,3^r}{3^{r(4\cdot3^{d-2}-1)}}.
$$

**Proof.** For any $h$ with $Bh=(v,b)$, the first difference is constant in $x$ if and only if the right-block mixed operator

$$
(\mathsf T_b-I)(\mathsf T_a-I)Q_0
$$

is a constant vector-valued function. If $b\in\langle a\rangle$ but $b\ne0$, the scalar operator has exact rank $3^{d-1}$, because $(\mathsf T_a-I)^2$ has rank one on each affine three-point $a$-orbit. If $b$ is independent of $a$, the scalar mixed operator has rank $4\cdot3^{d-2}$, the product of two independent one-coordinate difference ranks $2\cdot2$ and the identity on the other coordinates. In **both** cases the global constant-one function lies in the image (in characteristic three, the constant vector on a three-point orbit is in the image of a first difference). For a uniform scalar input table, the probability that an operator of rank $R$ has a **constant** output is therefore exactly $3^{-(R-1)}$; with $r$ independent output coordinates it is $3^{-r(R-1)}$. There are $2\cdot3^r$ directions with $b\in\{a,-a\}$ and $(3^d-3)3^r$ with $b$ independent of $a$. Summing these exact individual probabilities by the union bound proves the display. No independence between candidate directions is assumed. $\square$

| Original geometry | Public local target count | Unconditional local inversion | Bound on falsely enlarged $C(f)$ |
|:--|--:|:--|--:|
| SGD-R1 $(k,d,r)=(5,3,2)$ | 9 | Every target | $4.25034\cdot10^{-7}$ |
| SGD-R2 $(7,4,3)$ | 27 | Every target | $3.28803\cdot10^{-36}$ |
| SGD-R3 $(9,5,4)$ | 81 | Every target | $3.39402\cdot10^{-151}$ |

**Important ordering of claims.** The middle column's **100% exact right-inversion success** needs no source randomness, does **not** depend on recovering precisely $W_0$, and still holds if the exceptional case $C(f)\supsetneq W_0$ occurs. The last column is only a probability bound on *identifying the original coordinate shift subspace uniquely*, not a KEM advantage or a hardness level. The code in research-2028/attacks/public_first_difference_local_inversion.py validates exact public inversion of all $9$, $27$, and $81$ target values at the source geometries, public additivity of constant directions, exact GF(3) operator ranks, and an exhaustive census of all $19{,}683$ potential tables in the smallest scalar case. No secret $A,B,a,Q_0$ is supplied to its attacker.

**Repair decision, not a fictional security claim.** The original Round-6 coordinate-secret problem is **not fixed by more random masking**, since Theorem 4.6 constructs a public right inverse for every potential table. The intellectually honest corrective action is to **reject this local MaxEnt inversion as the security-bearing NCSG trapdoor**. It can remain a proved combinatorial/public-indexing ingredient, but a distinct publicly encryptable, secretly invertible **global coupling** and a sound average-case assumption would need to be designed and independently attacked before promoting a genuinely new NCSG-only KEM. The manuscript contains no such validated replacement today. In particular, the original dense GF(1024) label layer remains historically obsolete, with its separate asymptotic KEM break recorded in Theorem 9.2; it is not silently being reused as protection.


# 5. Archived 2026 hidden-MDS label construction (not the new candidate)

Select a profile $(n,k,d,r,m,M,u,N,\nu,\ell,\kappa_F,T_{\mathrm{rep}})$ with $M\le1024$, $u<M$ and $u\le N$. Independently sample $m$ NCSG supports, predicates and targets and enumerate $m$ fibers $S_i$, each of size $B_0=3^d$. Sample a master secret $s\in\mathbb F_3^n$ and a hidden set $\mathcal C\subseteq[m]$ of size $M$. For each $i$ sample invertible $R_i$ and a point $\sigma_i$ inside $S_i$ if $i\in\mathcal C$ and outside otherwise. Store $\delta_i=\sigma_i-R_is_{\mathcal N(i)}$ privately. The full NCSG public layer is generated independently of $s$.

For public distinct evaluation points $\alpha_1,\ldots,\alpha_M\in K$ and multipliers $v_i\ne0$, define the GRS generator matrix

$$
G_i=v_i(1,\alpha_i,\alpha_i^2,\ldots,\alpha_i^{u-1})\in K^u.
$$

Choose full-row-rank $T\in K^{u\times N}$ and a secret bijection $\pi:\mathcal C\rightarrow[M]$. All public row labels initially are sampled independently and uniformly from the nonzero vectors of $K^N$. In each good bucket replace exactly one label with

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
t_{\mathrm{dec}}=\operatorname{floor}((M-u)/2).
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

Define *PlantMDS-HBCE* as the ordered public label distribution in Section 5 and *NullMDS-HBCE* as the same distribution with each planted label independently replaced by uniform nonzero $K^N$ row. The **MDS-HBCE assumption** is that no efficient, appropriately resource-bounded adversary distinguishes these games. This assumption has no proof here. More strongly, **Theorem 9.2 proves this fixed-field assumption cannot justify an asymptotically secure KEM** under the stated efficient-family scaling: a public rank attack recovers the actual decoding code and encapsulated key. Any conditional upper bound in this section is therefore a historical bookkeeping identity, not a usable positive security theorem for that asymptotic family.

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


## 9.1 Round-3 negative theorem: fixed-field MDS-HBCE is asymptotically distinguishable

The original manuscript instantiates the planted public-label distribution over the **fixed** field $K=\mathbb F_{2^{10}}$ using a publicly known length-$M$ GRS frame with distinct evaluation points. Hence $M\le1024$. This implies a stronger result than the existing capacity obstruction.

**Theorem 9.1 (fixed-field rank-enumeration public-key distinguisher).** Fix $Q=1024$. In the original planted distribution let $q(\lambda)$ nonzero rows of $K^{N(\lambda)}$ be published, with $M(\lambda)$ hidden GRS rows of rank $u(\lambda)<M(\lambda)\le Q$. The null distribution replaces all planted rows with independent uniformly sampled nonzero rows. Assume $q(\lambda)$ is polynomially bounded, $N(\lambda)\ge u(\lambda)+1$, and $N(\lambda)=\Omega(\lambda)$. A uniform deterministic polynomial-time algorithm $D$ satisfies

$$
\Pr[D(\mathrm{Plant}_{\lambda})=1]=1,
$$

and

$$
\Pr[D(\mathrm{Null}_{\lambda})=1]\le
{q\choose u+1}\left(1-\prod_{i=1}^{u}
\frac{Q^N-Q^i}{Q^N-1}\right)=\operatorname{negl}(\lambda).
$$

Thus **the original fixed-field MDS-HBCE asymptotic indistinguishability assumption against all PPT or QPT adversaries is false** for such polynomial-size public-key families. This is a break of its proposed *asymptotic public-key assumption*, not a demonstrated IND-CPA/IND-CCA attack on the three finite ciphertext profiles.

**Distinguisher.** Enumerate all sets of $u+1$ rows in the published label matrix. Return planted upon finding a set of rank at most $u$ using ordinary Gaussian elimination over $K$. This does not require knowledge of the hidden bucket locations, GRS permutation, embedding matrix, or NCSG secret.

**Proof.** Every $u+1$ planted GRS rows have rank $u$ because the Vandermonde generator has row rank $u$ and multiplication by the sampled full-row-rank secret matrix preserves row dependencies. Since $M\ge u+1$, at least one enumerated set is dependent. Under the null, conditioned on $i$ earlier linearly independent uniform nonzero rows, the probability the next row belongs to their span is exactly $(Q^i-1)/(Q^N-1)$. The probability that $u+1$ fixed null rows are dependent is therefore exactly the product complement displayed above. A union bound over all subsets proves the inequality. Since the field is fixed, $u+1\le M\le1024$ for **every** security parameter, so exhaustive enumeration uses at most $O(q^{1024}\operatorname{poly}(N))$ field operations. The exponent 1024 is a fixed constant, making the attack a **uniform polynomial-time algorithm**, however infeasible at concrete sizes. Finally, the parenthetical null probability is $O(Q^{u-N})$ for bounded $u$; with $q$ polynomial and $N=\Omega(\lambda)$, the union bound is negligible. $\square$

**Finite-profile interpretation.** The exact numbers of subsets in this simple enumeration, expressed as $\log_2{q\choose u+1}$, are about $656.94$ (SGD-R1), $1136.78$ (SGD-R2), and $1718.10$ (SGD-R3), before Gaussian elimination. These huge exponents show why an asymptotic PPT attack **must not be mislabeled a practical finite-parameter attack**. More sophisticated classical or quantum attacks may be far cheaper; neither this enumerator nor the earlier source heuristics supplies a secure work-factor lower bound.

**Repair boundary.** Increasing noise or simply choosing a larger fixed $N$ cannot fix this asymptotic problem. Changing the field to grow with the security parameter or replacing the algebraic embedding might remove the particular constant-degree argument, but would require a new complete sampled assumption, cryptanalysis, decoder, efficient implementation, and quantum-aware reduction. No such unproved change may be advertised as formally secure. The author's active target remains **an original NCSG-dependent construction without any external KEM ingredient**; this theorem is an archived-GRS no-go result and a mandatory negative design gate.

**Reproduction.** The pure-Python GF(1024) attack implementation and exact GF(3) independent-probability enumeration reside in research-2028/attacks/fixed_field_mds_hbce_ppt_break.py. Finite tests check this algebra; the general asymptotic conclusion follows from the mathematical argument, not from testing.


## 9.2 Round-5 theorem: asymptotic public KEM decryption from hidden-frame recovery

Round 3 proved that the original fixed-field SG-DIFRA-MDS hidden GRS labels are distinguishable from random in uniform polynomial time in a sufficiently growing asymptotic family. A stricter red-team question is whether a successful attacker can **recover the encapsulated key**, not merely distinguish a public matrix. For this archived KEM the answer is yes, under precisely stated scaling and correctness conditions. This is a much stronger negative finding for the **original GF(1024) KEM**, not a break of a new NCSG-only design.

**Theorem 9.2 (public-decapsulation and honest shared-key recovery).** Retain the exact archived key-generation structure over fixed $K=\mathbb F_{2^{10}}$ with $Q=1024$: the published matrix $H\in K^{q\times N}$ contains $M$ hidden generalized Reed--Solomon rows $G_{\pi(i)}T$ in distinct public buckets, $T$ is uniformly full-row-rank of size $u\times N$, $1\le u<M\le Q$, and every decoy label is an independent uniform nonzero vector. Assume $q(\lambda)$ and the bit-message ciphertext length are polynomial in $\lambda$, $N(\lambda)\ge u+1$ and $N(\lambda)=\Omega(\lambda)$. There is a uniform **classical polynomial-time** algorithm which, using only $(pk,C)$, evaluates the genuine secret-key PKE decoding result for **every** ciphertext $C$ except with a key-generation failure probability at most

$$
\varepsilon_{\mathrm{row}}
\le
\left[(u+1)\binom{q}{u+1}+q-M\right]
\frac{Q^u-1}{Q^N-1}.
$$

If the original KEM has honest key-agreement failure at most $\delta(\lambda)$ and returns $\kappa$-bit keys, the same algorithm derives the honest encapsulated shared key whenever honest decapsulation is correct, giving a real-versus-random key distinguishing advantage at least

$$
1-\varepsilon_{\mathrm{row}}-\delta(\lambda)-2^{-\kappa}.
$$

In particular, **this archived fixed-field KEM fails its intended asymptotic confidentiality goal** whenever its intended correctness is high; this result is stronger than a planted-key distinguisher alone.

**Proof, stage I (recover all hidden row positions).** Enumerate every public $(u+1)$-subset and locate one with rank $u$ using Gaussian elimination. An all-planted subset always exists, since any $u$ genuine GRS rows are independent and any $u+1$ are dependent. Consider a mixed subset with $j\le u$ planted rows, hence $j$ initially independent rows; sequentially reveal its independent nonzero decoys. Before the first dependent row appears, the next decoy lies in the span of at most $u$ preceding rows with probability at most $(Q^u-1)/(Q^N-1)$. A union bound over at most $u+1$ exposures and $\binom{q}{u+1}$ mixed subsets bounds the probability that any mixed subset is dependent by the first summand of $\varepsilon_{\mathrm{row}}$.

On the complementary event the located dependency consists of planted rows only; it spans precisely the secret $u$-dimensional row space $W=\operatorname{rowspan}(T)$. A public membership test $h_i\in W$ then locates **every** planted row. Any nonzero decoy independently lands in $W$ with exact probability $(Q^u-1)/(Q^N-1)$. A final union bound over $q-M$ decoys yields the second summand. Thus the adversary obtains the entire hidden coordinate set without recovering the NCSG master secret, the affine incidence masks, the GRS permutation or the ephemeral embedding matrix itself.

**Proof, stage II (emulate the secret decoder without the GRS permutation).** Extract all $M$ recovered planted rows into a canonically ordered public matrix $H_P\in K^{M\times N}$. Its column-space code is a coordinate permutation of the secret GRS code, of dimension $u$ and minimum distance $M-u+1$; the hidden full-row-rank $T$ does not change the code image. Public linear algebra supplies a generator $\widetilde G\in K^{M\times u}$ for that code. Every $u$ rows of $\widetilde G$ are independent. For an arbitrary received vector $y\in K^M$, enumerate each $u$-subset $J$ of row positions, solve the public square system

$$
\widetilde G_Jx=y_J,
$$

and return bit zero iff any solution has

$$
d_H(\widetilde Gx,y)\le t_{\mathrm{dec}},
\qquad t_{\mathrm{dec}}=\operatorname{floor}((M-u)/2).
$$

If secret bounded-distance GRS decoding accepts, some codeword agrees with $y$ in at least $M-t_{\mathrm{dec}}\ge u$ positions. One enumerated $u$-set consists entirely of agreeing positions, and its unique solution recreates that codeword. Conversely, a public solution within radius is a valid codeword that the secret GRS decoder must accept. Uniqueness holds because the code minimum distance exceeds $2t_{\mathrm{dec}}$. **The publicly reconstructed DecBit is identical to the original secret DecBit on every received word**, even malformed ciphertexts, once the planted positions are found.

**Proof, stage III (honest encapsulated-key recovery).** Run the public decoder on the source's independent ciphertext repetitions and reconstruct the same majority-decoded message $\mu'$ as secret PKE.Dec. Derive deterministic coins from public $(pk,\mu')$, re-encrypt and compare with the received $C$. On a match compute the same public-domain-separated session-key hash as the original decapsulation. On an honest encapsulation for which secret decapsulation returns the encapsulated key, this computes that key without $sk$. A KEM real-versus-random challenger key matches the adversary's publicly recovered key with probability at least $1-\varepsilon_{\mathrm{row}}-\delta$ when real and at most $2^{-\kappa}$ when uniformly random. This proves the claimed advantage. $\square$

**Cost and honest limits.** Public row discovery costs at most $\binom{q}{u+1}$ finite-field rank tests. Public bit decoding uses at most $\binom{M}{u}$ square linear solves per component, with only polynomial processing per test. Since the **fixed field forces $u<M\le1024$**, both combinatorial exponents are fixed absolute constants, even though the resulting algorithms are completely infeasible for the original finite profiles:

| Original frozen profile | log2 row-subset tests | log2 public decode information sets |
|:--|--:|--:|
| SGD-R1 | 656.94 | 203.57 |
| SGD-R2 | 1136.78 | 307.12 |
| SGD-R3 | 1718.10 | 410.76 |

These are *enormous work estimates for this particular exhaustive classical algorithm*, NOT security lower bounds and NOT practical secret-key compromises of the published frozen sizes. Other classical or quantum methods may be less expensive. The theorem states a bona fide **asymptotic confidentiality break** of the original fixed-field KEM under explicit efficient scaling and adequate correctness; it does **not** establish a numerical finite-profile IND-CCA advantage for a feasible attacker.

**Why the old repairs do not fix this.** Public-geometry balancing, a stronger NP-completeness proof for NCSG-DS, arbitrary hidden affine incidence masks, obscuring $\pi$, and increasing symbol noise cannot remove the already published hidden-code row-space. An asymptotically growing field may avoid this **particular** constant-degree enumeration argument but requires a newly specified, independently attacked distribution and hardness assumption; it does not establish security. Most importantly, the user-directed new cryptographic goal is a genuinely NCSG-essential scheme with a novel trapdoor. **No such complete secure KEM is currently established by this manuscript**, and the three frozen profiles cannot be certified safe by changing words or parameter labels.

**Reproduction.** The pure-Python test research-2028/attacks/public_decapsulation_recovery.py uses the original fixed-GF(1024) planted-frame sampler from Round 3. It recovers the entire planted row set for twelve reduced keys, verifies 96 secret/public DecBit matches on both ciphertext classes, and tests deterministic re-encryption and publicly recovered genuine shared keys in a small three-repetition KEM fixture. This is toy *verification of the attack algorithm*, not an execution of the astronomical R1/R2/R3 search or a QROM security proof.


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
