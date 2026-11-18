# Standalone KEM under one generated ternary witness assumption

Round 16 chooses fresh dimensions so that the receiver's private-check problem and the sender's masking problem follow from **one distribution** at each target. The assumption concerns a single public ternary matrix, a target, and a specified Hamming weight. It makes no reference to a KEM, a private decoder, or an encryption oracle. Its concrete computational difficulty remains open. The dimension change means that the premise for this KEM differs from the Round 15 premise.

## A common syndrome distribution

Work over $\mathbb F_3$. In the real distribution, draw an independent uniform $d\times r$ matrix $B$ and uniform signed weight-$w$ vector $e$ of length $r$. Its support is a uniform $w$-subset; each nonzero entry is independently 1 or 2. Supply $(B,Be)$. In the comparison distribution supply $(B,U_d)$ for an independent uniform target. Let $\eta$ bound the absolute difference in acceptance probabilities of all distinguishing circuits used by the reductions, at their actual resources. The search version gives a real sample and asks for any weight-$w$ vector with the given syndrome. As in [the cubic encoding](../round14/WEIGHTED_DIFFERENCE.md), this is equivalently a distribution of generated fixed-challenge SG-DIFRA collisions with a polynomial-time witness bijection.

The [matched implementation](matched_kem.py) uses $t$ public check columns, $m$ base columns and $N=m+t$ transmitted trits. The linear mask has dimension $h$, the quadratic block has $a=n(n+1)/2$ features and $d=h+a$. Set the receiver's check weight and sender's noise weight both to $w$. The implementation starts with $m=4(t-1)w$, adds one if necessary for parity, chooses $h=(m+t-a)/2$, and enforces
$$
d=N-h<r=m-(t-1)w.
$$
The new suite identifier separates all four hashed roles from prior suites. The native signed error is sampled directly on the $N$ transmitted coordinates. The receiver subtracts its disjoint checks, leaving at most $w$ incorrect trits. The [Golay–Reed–Solomon correction proof](../round15/OUTER.md) therefore recovers the original message for every honestly generated private key and every allowed sender tape. Full ciphertext replay verifies honest encapsulations.

## Reduction to the common input

**Private check hybrids.** Start with independent uniform base rows and exact private sampling. Replace the $t$ check syndromes one at a time by independent uniform columns. Draw the other $t-1$ disjoint signed supports first, including dummy supports for already replaced columns. Exactly $r$ base positions remain. Into those positions embed the supplied $B$, then fill the other base columns with fresh iid trits. Use the supplied target as the selected check syndrome. The planted case and the uniform case are the two neighboring hybrids. In the game of guessing a fair message-choice bit the total loss is at most $t\eta$. This is the [private check reduction](../round14/BASE_PROOF.md) with the matched dimensions.

**Padding the same input.** Append $N-r$ independent uniform columns to $B$ and apply an independent uniform permutation to all $N$ columns, giving $H$. Keep the original target $y$. In the planted case the hidden vector is the permuted $(e,0^{N-r})$, a uniform signed weight-$w$ vector on $N$ positions. For each fixed permutation the matrix $H$ is iid uniform and independent of the initial $e$. Its law is identical for all permutations, so it is independent of the permuted error as well. Therefore $(H,y)$ is an exact length-$N$ planted syndrome sample. In the other case $y$ is independent uniform. This transformation runs from the shorter common input to the longer problem handled by a tester.

**From parity checks to noisy words.** Write $p_j=\prod_{i=0}^{j-1}(1-3^{i-N})$, the probability that $j$ uniform rows of length $N$ are linearly independent. If $H$ lacks row rank $d$, return a fixed decision. Otherwise sample the rows of $G$ as a uniform ordered basis of $\ker H$, whose dimension is $N-d=h$. Sample $W$ uniformly from the solutions of $HW=y$. Conditional on full rank, $G$ is a uniform full-row-rank $h\times N$ matrix by change-of-basis symmetry. With planted error $E$, $W=E+G^\top u$ for uniform $u$. With uniform $y$, $W$ is uniform and independent of $G$. The signed gap of the resulting syndrome test is $p_d$ times the conditional generator test gap; the matrix marginal is identical in the two experiments. For an iid generator the deficient fraction is $1-p_h$, where a raw gap is at most one. Thus the noisy-word distinguishing gap is at most
$$
(p_h/p_d)\eta+(1-p_h).
$$
After the private-check hybrids, the public KEM matrix is iid. The sender's $h$ linear rows use $G$. The reduction independently simulates the quadratic rows, quadratic features and chosen plaintext offset. Adding them to $W$ gives real encryption or an independent uniform body. The private-check and payload reductions both consume a single sample of the *same* common experiment per invocation.

## Concrete inequality and scope

Let $\nu\le2^{-\sigma}$ bound the finite joint encryption-coin sampling distance and $s_A$ be the public matrix row sampler's excess bits. The [row-lifting coupling](../round14/SEEDED_MATRIX.md) changes the whole programmed target slice by at most $d2^{-s_A}$, with fresh independent oracle values outside it. For a raw two-message PKE distinguishing gap the resulting bound is
$$
\epsilon\le\min(1,C\eta+U),\quad C=2(t+p_h/p_d),\quad
U=2(1-p_h)+2\nu+2d2^{-s_A}.
$$
The factor of two converts excess fair-bit guessing success to a raw gap. The receiver's hidden check seed is accounted for in the final KEM experiment.

Use one honest recipient, independent ideal hash domains with quantum queries, adaptive classical decapsulation requests, and the usual challenge-ciphertext restriction. Let $q_G,q_H$ count FO hash queries, $D$ be their combined query depth, $q=q_G+q_H$, $q_D$ the decapsulation count, and $q_S$ the private-expansion hash count. Write $\ell$ for message bits, $s$ for nonce bits, $\kappa$ for private seed bits and $s_S$ for private check sampling slack. Put $R=D+q_D$. The [published FO argument as instantiated in Round 14](../round14/CCA_PROOF.md) and the [private-seed hybrid](../round14/PRIVATE_SEED.md) give
$$
\Delta\le\min(1,8\sqrt{R\epsilon}+\Lambda),\qquad
\Lambda=16(q+q_D)2^{-\ell/2}
+48q_D(q_G+4q_D)2^{-s/2}
+2q_{\rm pre}2^{-\ell}
+4q_S2^{-\kappa/2}+2t2^{-s_S}.
$$
Here $q_{\rm pre}$ counts prior classical decapsulation queries in the two-stage convention and can be zero for challenge-at-start games. The independent uniform nonce in randomized base encryption supplies $s$ bits of ciphertext spread. Set $q_D=q_{\rm pre}=0$ for IND-CPA. Bounds refer to the simulation's time, oracle access, and quantum memory, including matrix generation, basis/fiber sampling, and FO simulation. The formulas use exact random sampling inside the reductions. Rejection sampling can use expected polynomial time or be capped with its statistical error explicitly added. The implementation uses domain-separated SHAKE256 as a concrete instantiation of the ideal hashing assumptions.

**Witness consequence.** For $R>0$ and $x_+=\max(x,0)$, a KEM raw gap $\Delta$ forces at least one common-game distinguishing circuit to achieve a raw gap of at least
$$
\delta_* = \frac{1}{C}\left(\frac{(\Delta-\Lambda)_+^2}{64R}-U\right)_+ .
$$
Use the maximum over the finite set of hybrid testers in the derivation above. The [ternary quantum witness reduction](../round14/WITNESS_PROOF.md) applied to such a tester recovers a planted witness with probability at least $4\delta_*^2/9$. It needs a coherent implementation of the tester and its adjoint; a finite gate set must account for approximation and bounded-sampling errors. This is a reduction to one generated sparse witness distribution. It neither proves hardness of that distribution nor turns an arbitrary worst-case challenge into this generated one.

## The 192 target

Here $w=1152$, $t=5256$, $d=12{,}119{,}412$, $r=18{,}161{,}280$, $h=12{,}100{,}884$ and $N=24{,}220{,}296$. Set $Q=2^{191}$ and bound each of $q,q_D,q_S$ by $Q$. Then $R\le2Q$. Both rank defect probabilities are below $2^{-1000}$ since $1-p_j<3^{j-N}/2$. It follows that $C<10{,}516<2^{14}$. With $\sigma=320$, $s_A=s_S=576$, $\ell=\kappa=512$ and $s=896$, we have $U<2^{-318}$ and
$$
\Lambda\le 32Q2^{-256}+240Q^22^{-448}+2Q2^{-512}
+4Q2^{-256}+2t2^{-576}<2^{-57}.
$$

| Hypothetical common raw gap at the composed resources | Consequence for guessing whether the KEM key is genuine |
|---|---|
| $\eta\le2^{-224}$ | Success below $50.8\%$ |
| $\eta\le2^{-280}$ | Success below $1/2+2^{-34}$ |

Indeed the two base gaps are below $2^{-210}$ and $2^{-266}$ respectively, using $C<10{,}516$. Their leading FO terms are below $2^{-6}$ and $2^{-34}$. Add $\Lambda$ and convert the raw gap to guessing probability $1/2+\Delta/2$. Going the other way, a raw KEM advantage at least $1/8$ in that budget gives a common-game distinguishing gap above $2^{-221}$ and planted search success above $2^{-444}$ in the ideal reduction. For this coarse lower bound use $\Delta-\Lambda>1/16$, $64R\le2^{198}$ and $C<2^{14}$. These figures express the loss of the reduction. Oracle counts alone give no bound on all physical operations, and the example supplies no numerical full-input decoding-hardness estimate.
