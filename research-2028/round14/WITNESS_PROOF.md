# From a distinguisher to a witness of generated ternary constraints

The base security proof compares two distributions of *decision* instances. Here we show the positive consequence for *search*. If a quantum circuit distinguishes a fresh ternary syndrome from a uniform target with raw gap $\delta$, a polynomial quantum computation recovers the actual planted vector with average probability at least $4\delta^2/9$. The two parameter regimes in the KEM have different dimensions and weights. A break can give a solver for at least one of them. The promise is random generated instances with the named distributions.

## One syndrome game

Let $A$ be an iid uniform matrix in $\mathbb F_3^{d\times m}$, and let $s$ be an independent uniform signed vector of Hamming weight $w$. In the real decision experiment the input is $(A,Y=As)$; the random experiment uses the same matrix law and independent uniform $Y\in\mathbb F_3^d$. Let $a(A,Y)$ be a decision circuit's probability of accepting. Set $p_R=\mathbb E[a(A,As)]$, $p_U=\mathbb E[a(A,U)]$ and $\delta=|p_R-p_U|$. In the search experiment, an output $s'$ of weight $w$ satisfying $As'=Y$ is accepted. Returning the originally drawn $s$ suffices even when there are several witnesses.

**Theorem.** Under these definitions, access to a coherent implementation of the decision circuit and its adjoint gives search success at least $4\delta^2/9$. Each is used once per run, in addition to polynomial work on the public data. The reduction applies also when the decision computation uses independent ideal quantum oracles, provided the solver has the same oracle resource and can run the circuit and its adjoint. The theorem is an algorithm-existence reduction for explicit efficient circuits. An external service supplying only classical decision bits would be a different model.

**Proof.** For fresh $r\in\mathbb F_3^m$, $b\in\mathbb F_3^d$, $c\in\mathbb F_3$, consider
$$A'=A+br^\top,\qquad Y'=Y+cb.$$
Condition on the secret $s$, on $r,c$, and on fixed independent auxiliary ideal functions. Since the original $A$ is uniform, $A'$ is uniform and independent of $b$. The identity
$$Y'=A's+(c-r^\top s)b$$
shows what each choice of $c$ does. When $c=r^\top s$, the new pair is a real instance for this $s$. For either other $c$, the nonzero multiple of the independent uniform $b$ makes $Y'$ uniform independently of $A'$. This property is asserted in the average experiment over the original instance.

Write $\omega=\exp(2\pi i/3)$. Purify the decision computation, phase-flip its acceptance bit, and uncompute. The amplitude on its original clean workspace, for a fixed pair $(A',Y')$, is $1-2a(A',Y')$. This follows by subtracting the probability mass on the accepting part from that on the rejecting part. The input registers are kept unchanged. Classical random choices and intermediate measurements can be recorded coherently.

Prepare independent uniform registers for $r,b,c$. On this superposition compute $(A',Y')$ reversibly from the given search instance. Apply the phase operation and uncompute the modified data, contributing also the phase $\omega^c$. Unprepare the uniform $b,c$ registers and take the negative-sign ternary Fourier transform on $r$. For the original secret $s$, the amplitude on the output $s$ with all auxiliary registers clean is exactly
$$
Z(A,s)=\mathbb E_{r,b,c}\left[
 \omega^{c-r^\top s}\big(1-2a(A+br^\top,As+cb)\big)
\right].
$$
The normalizations are averages because the input registers were uniform and each clean-register or Fourier-output coefficient contributes the corresponding uniform magnitude. Measuring the output and returning a verified candidate succeeds on this joint event. It therefore succeeds with probability at least $|Z(A,s)|^2$ for that instance. There is no postselection assumption in this inequality.

In the average over $A,s$ and auxiliary oracles, the three values of $c-r^\top s$ have probabilities one third each. The zero case contributes $(1-2p_R)/3$. The two nonzero cases contribute $(\omega+\omega^2)(1-2p_U)/3$. Using $\omega+\omega^2=-1$ gives $\mathbb E Z=-2(p_R-p_U)/3$. Hence $\mathbb E|Z|^2\ge|\mathbb E Z|^2=4\delta^2/9$, as claimed. The displayed constants use ideal ternary Fourier gates; a finite universal gate set can approximate them to any stated inverse-polynomial or negligible error with polynomial overhead. Fischer and Stern used the binary version of the rank-one matrix and syndrome shift in their search reduction for fixed-weight binary vectors. Adcock and Cleve developed quantum Goldreich–Levin extraction. Sudo, Hara, Tezuka and Yoshida give a prime-alphabet quantum Goldreich–Levin theorem and a two-invocation reduction for LWE. The proof here specializes these ideas to the two ternary syndrome distributions and tracks the constants for this composition. [Fischer and Stern, Theorem 3](https://www.di.ens.fr/~stern/data/St58.pdf) · [Adcock and Cleve](https://arxiv.org/abs/quant-ph/0108095) · [Sudo et al., IEICE 2025](https://doi.org/10.1587/transfun.2024EAP1004)

## Applying the result to the two KEM assumptions

For the first experiment of the [base proof](BASE_PROOF.md), put $(d,m,w)=(d,r,w)$ in the theorem, where $r$ is the number of base coordinates left after excluding the other $t-1$ secret supports. Let $P_1$ be an upper bound on quantum search success for that generated syndrome distribution at resources covering the conversion above. Then $\epsilon_1\le (3/2)\sqrt{P_1}$.

For the payload experiment, use a second independent iid parity-check instance whose matrix $H$ has dimensions $(L-k)\times L$ and whose signed witness has weight $z$. Write $P_2$ for the corresponding upper bound on search success. Let $\rho_G$ and $\rho_H$ denote the rank-deficiency probabilities of iid uniform $k\times L$ and $(L-k)\times L$ matrices. For any iid uniform $a\times L$ matrix with $a\le L$ the exact deficiency probability is $1-\prod_{i=0}^{a-1}(1-3^{i-L})$. These probabilities agree across the real and uniform experiments because the marginal law of the matrix is the same. Any test of the full-rank parity-check experiment extends to the iid experiment by returning a fixed bit on deficient matrices. This multiplies its signed gap by $1-\rho_H$. Transporting the full-rank game to the uniform-generator game as in the base proof gives
$$
\epsilon_2\le \rho_G+\frac{1-\rho_G}{1-\rho_H}\frac32\sqrt{P_2}.
$$
Random basis and fiber sampling in the full-rank simulation may use expected polynomial time. To obtain fixed-size quantum circuits for that tester, cap every rejection loop using independent blocks of randomness, return a fixed result on exhaustion, and include the sampler's statistical error. For example the probability that a uniform square ternary matrix is invertible is at least one half, so $j$ independent trials leave failure probability at most $2^{-j}$. This error can be made negligible. A finite-resource estimate must pay for these operations and both calls to the purified tester.

Combined with the base theorem, the ideal-randomness, two-message raw IND-CPA gap is at most $2t\epsilon_1+2\epsilon_2$, clipped to one. The [chosen-ciphertext proof](CCA_PROOF.md) then accounts for finite-tape sampling, the transform's oracle queries, and its security loss. With polynomial dimensions, negligible rank corrections and sampler errors, and the stated asymptotic hash/nonce parameters, a nonnegligible KEM advantage gives nonnegligible success on at least one generated sparse witness distribution. Each security claim uses the adversary resources after the corresponding reductions. The theorem provides no numerical hardness bound for the witness distributions themselves.

## The precise SG-DIFRA search relation

For either syndrome game, use the ternary public map
$$Q_A(s)=(As,\operatorname{bin}(\operatorname{wt}(s))).$$
Here the binary count is written least-significant bit first. The squares $s_i^2$ indicate nonzero trits and a binary counter over arithmetic gates computes their integer sum. Apply the [Round 12 cubic compiler](../round12/GENERATED_DIFFERENTIAL_REDUCTION.md) with recoverable public matrix metadata and challenge $(Y,\operatorname{bin}(w))$. Its collision basepoints correspond one-to-one to weight-$w$ solutions of $As=Y$. The [explicit compiler and bijection](WEIGHTED_DIFFERENCE.md) work for rectangular matrices and multiple witnesses. The resulting implication concerns these generated fixed-challenge cubic instances. Their hardness assumption has its origin in random-code decoding. No step reduces arbitrary instances of the separate universal or strategy decision problems to this KEM.

[Exact finite Fourier-identity checks](test_witness_identity.py) enumerate the real and uniform samples and use rational arithmetic in the ternary cyclotomic field to check the amplitude average and squared bound.
