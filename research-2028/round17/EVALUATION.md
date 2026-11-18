# How much of the Round 16 public key is needed to evaluate encryption?

In the Round 16 middle layout, the check block takes almost the smallest possible space even if a compact public key only promises to **evaluate** its action. Under the public-key indistinguishability assumption below, a fixed-width key that reproduces the original check outputs on 99% of random inputs needs at least **12,620,190,503 bytes** of recipient-specific data beyond the separately supplied public matrix seed. Adding that 32-byte seed brings the total to **12,620,190,535 bytes**. The original public key uses 12,620,284,606 bytes. At most 94,071 bytes separate this lower bound from the published layout.

## Statement

Write $H$ for the published $d$-row, $t$-column matrix of private-check syndromes. At an encryption input $u$ of $h$ trits and $x$ of $n$ trits the sender evaluates
$$
f_H(u,x)=H^\mathsf{T}\big(u,(x_i x_j)_{i\le j}\big),\qquad
d=h+n(n+1)/2.
$$
The check portion of the ciphertext body adds a known outer-code word and prescribed noise to this vector. Thus a drop-in evaluator that returns the original body for prescribed sender inputs and noise gives access to $f_H$ by subtracting those known terms. An evaluator providing only a distributionally equivalent randomized ciphertext or an entirely different encapsulation falls outside this claim.

Fix a public encoder and evaluator. Allow both access to the public matrix seed, the agreed public parameters and any shared randomness independent of the real key generation. Include the entire public oracle as side information whenever the indistinguishability experiment provides one. Charge all their work and oracle access to the reduction. The encoder sees the real public data and supplies a string of exactly $b$ bits. Each evaluation uses that string, the public side information, the chosen input and fresh evaluation coins. All recipient-specific information passed from encoder to evaluator, apart from the specified side information, must fit in the $b$ bits. Define $1-e$ to be a lower bound on the probability that the evaluator returns the exact $t$-trit output, averaging over honest keys, public setup, encoder and evaluator coins and independent uniform inputs $(u,x)$.

Assume a raw gap at most $\mu$ for the efficient public test below between the genuine joint public data and the game with $H$ replaced by an independent uniform $d\times t$ ternary matrix. This is the public-check hybrid in the [Round 16 proof](../round16/MATCHED_PROOF.md), with its seed and sampling terms included when using the seeded wire format. The whole-key gap $\mu$ concerns a test of one set of $t$ columns. It may include a factor $t$ when justified from single-syndrome hardness. Independent uniform $H$ in the comparison game must be independent of all side information the evaluator can access before receiving its string. This assumption leaves the concrete hardness of the decoding problem open.

**Theorem.** For every positive integer $T$ for which the encoder and $T$ tests fall in the assumed resources,
$$
(1-e)^T \le \mu + 2^b/3^{dt} + (7/9)^T.
$$

**Distance lemma.** For distinct matrices $H,J$, the fraction of uniform inputs on which $f_H=f_J$ is at most $5/9$. Some output coordinate of the difference has a nonzero coefficient vector. Any nonzero linear term involving $u$ makes the scalar result uniform for fixed other variables. Otherwise the polynomial is a nonzero homogeneous quadratic in $x$. Over $\mathbb F_3$, a nonsingular change of variables diagonalizes its symmetric matrix. This preserves uniform inputs. In rank one the quadratic vanishes with probability $1/3$. In rank at least two, condition on all except two nonzero diagonal terms. Each of the two independent input squares is zero with probability $1/3$ and one with probability $2/3$. Equal coefficients give a three-value distribution with masses $1/9,4/9,4/9$ up to permutation. Opposite coefficients give $5/9,2/9,2/9$. Adding the conditioned constant preserves the maximal mass bound. The joint output can agree only if this scalar coordinate agrees. When $n\ge2$, the example $x_1x_2$ is zero on exactly $5/9$ of inputs.

**Proof of the theorem.** Fix the public side information and one output string from the encoder. For two matrices, use the same random evaluation at the same input in both comparisons with their exact outputs. The two correctness indicators sum to at most one plus the indicator that the exact outputs agree. By the lemma their expected sum is at most $1+5/9$. At most one matrix can therefore have success probability strictly greater than $7/9$ for this string. With $2^b$ available strings, an independent uniform matrix gets access to such a string with probability at most $2^b/3^{dt}$.

Run the encoder once, then compare $T$ independent predictions against direct computation of the supplied $H$ on fresh uniform inputs. Accept when all predictions match. Conditioned on the public setup, $H$ and the encoder output, these comparisons are independent and have common success probability $p$. On honest keys, the expectation of $p^T$ is at least $(1-e)^T$ by convexity. In the uniform game, the exceptional matrices contribute at most $2^b/3^{dt}$, and for the other matrices the conditional acceptance is at most $(7/9)^T$. Applying the assumed gap proves the claim.

The same setup with perfectly correct evaluation admits a direct reconstruction argument. Set $x=0$ and query each unit $u$ to obtain all linear rows. With $u=0$, query each unit $x$ for the square rows. Query $x=e_i+e_j$ for $i<j$ and subtract the two already known square rows to obtain the cross row. These $d$ evaluations recover all of $H$. The resulting inequality is $1\le\mu+2^b/3^{dt}$ when the assumed resources cover these evaluations. The randomized theorem needs only $T$ evaluations.

## Exact arithmetic at the 192 target

Use $e\le1/100$, $\mu\le1/4$, and $T=16$. The inequality
$$
(99/100)^{16}-(7/9)^{16}-1/4 > 1/2
$$
gives $b>dt\log_2(3)-1$. At $d=12{,}119{,}412$ and $t=5{,}256$ there are $dt=63{,}699{,}629{,}472$ trits. The exact integer comparisons $2^{176251}<3^{111202}$ and $3^{190537}<2^{301994}$ give rational lower and upper bounds for $\log_2 3$. With these bounds,
$$
  8\times12{,}620{,}190{,}502
  < dt\log_2(3)-1
  < dt\log_2(3)
  < 8\times12{,}620{,}190{,}503.
$$
Every fixed byte width therefore needs at least 12,620,190,503 bytes for the check information. Encoding the whole block as a single base-three integer would attain this byte width. Such a large integer is unnecessary for the proof and potentially expensive in an implementation. The actual [Round 16 implementation](../round16/matched_kem.py) inherits blockwise packing over 64 rows. The [finite checks](test_evaluation.py) verify the exact inequalities and exercise the distance and reconstruction arguments on small fields of inputs.

The accounting assumes the matrix seed remains separately framed as in the current layout. With the seed available to the evaluator at no cost, the proven bound applies solely to the additional check data. The result applies to the Round 16 dimensions and to accurately evaluating its specified sender map. A different public computation, a different layout, or a new source of correlated setup needs its own analysis.
