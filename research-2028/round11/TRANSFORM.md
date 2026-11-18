# Conditional security of the hashed-permutation KEM

The question addressed here is precise. Suppose a compact, quantum-one-way trapdoor permutation over ternary vectors has already been constructed. What security would the encapsulation wrapper inherit? This note proves perfect correctness and gives quantitative IND-CCA reductions for an ideal hash. The permutation premise is open for SG-DIFRA. The included public-shear backend is a correctness control with a public inverse.

The construction follows the hashed-preimage pattern of Shoup's RSA-KEM. RSA is historical context only. The quantum proof uses the query-measurement argument underlying one-way-to-hiding. [RSA-KEM and its antecedents, RFC 9690](https://www.rfc-editor.org/rfc/rfc9690.html) · [Ambainis, Hamburg and Unruh, CRYPTO 2019](https://kodu.ut.ee/~unruh/publications/semiclassical.html)

## Premises, encoding and algorithms

For each security parameter, fix a suite, a dimension $n$ and $D=\mathbb F_3^n$. Write $N=3^n$. A permutation key generator samples $(pk,sk)$ independently of the ideal hash. Each generated public key defines an efficiently and deterministically evaluable bijection $F_{pk}:D\to D$. The private algorithm recovers its unique inverse on *every* point of $D$. Both sides recover the same canonical public-key bytes. These are mathematical hypotheses on every generated key. Uniform draws from $D$ are ideal samples in the game. Sampling a rank with rejection implements that law using expected polynomial time.

Let $E$ encode a trit vector as a fixed-length, big-endian base-three rank using the shortest byte width that accommodates all $N$ vectors. Only ranks below $N$ and the exact width are accepted. Define $S_{pk}(x)$ to be the injective framing of the following five byte strings: versioned KDF domain, suite identifier, eight-byte big-endian dimension, public-key bytes, and $E(x)$. The implementation prefixes every string with its length as an eight-byte big-endian integer and uses a 32-byte output. The members of $\{S_{pk}(x):x\in D\}$ are efficiently recognizable for the target key. No other byte string, including a different suite or different public-key encoding, belongs to that target slice.

* **KeyGen.** Generate the permutation keys and associate their canonical encodings with the agreed suite and dimension.
* **Encaps.** Draw $X$ exactly uniformly from $D$. Return the ciphertext $E(F_{pk}(X))$ and shared key $H(S_{pk}(X))$.
* **Decaps.** Reject a malformed ciphertext with $\bot$. For a canonical ciphertext $E(y)$, return $H(S_{pk}(F_{sk}^{-1}(y)))$, where $F_{sk}^{-1}$ denotes the private inverse.

For honest keys and ciphertexts, the two hash inputs are identical, so correctness holds with probability one. Each canonical encoding names a unique permutation output. In particular there is no alternate accepted byte string representing the challenge point.

## Games and concrete advantage

The one-stage, single-user KEM game gives the distinguisher the public key, a challenge ciphertext $E(Y)$ and a challenge key. In the real game the challenge key is the result of the honest encapsulation. In the random game it is an independent uniform key of the same length. Throughout the game the adaptive **classical** decapsulation oracle rejects $E(Y)$, rejects malformed ciphertexts, and answers every other valid ciphertext. The adversary may also evaluate the public permutation itself. We use the raw distinguishing gap

$$
\Delta=\left|\Pr[\mathrm{output}\ 1\mid\mathrm{real}]-\Pr[\mathrm{output}\ 1\mid\mathrm{random}]\right|.
$$

In the inversion game, sample the same permutation keypair, then $X\gets D$ uniformly, and give $(pk,Y=F_{pk}(X))$ to the inverter. Its success probability is $\Pr[F_{pk}(\widehat X)=Y]$. The classical proof can simulate its random functions by ordinary lazy sampling. For the quantum theorem we state the inversion experiment with access to an **independent auxiliary ideal quantum random function**. Its domain can be tagged to supply the independent functions below. This model explicitly accounts for the resource used by the quantum simulator. No unrelativized concrete bound or substitution theorem for SHAKE256 is asserted.

## A common simulation

Given $(pk,Y)$, sample a challenge key $K^*$ uniformly. Use independent random functions $G:D\to\{0,1\}^{\ell}$ and $J$ on other input strings with the same output length. Here $\ell$ is the shared-key length in bits. Define the following two hash frontends on *all* byte strings:

$$
 H_0(S_{pk}(x))=G(F_{pk}(x)),\qquad
 H_1(S_{pk}(x))=
 \begin{cases}
 K^* & F_{pk}(x)=Y,\\
 G(F_{pk}(x)) & F_{pk}(x)\ne Y.
 \end{cases}
$$

For every off-slice string $u$, set $H_0(u)=H_1(u)=J(u)$. Use $G(y)$ for every permitted canonical decapsulation query $E(y)$. The simulator never needs the trapdoor. On a superposition of target and other strings, it reversibly recognizes the target slice, evaluates $F_{pk}$ on that branch, implements the selected oracle and uncomputes its workspace.

Because $F_{pk}$ is a permutation, composing $G$ with it yields a uniform random function on target inputs. Thus $H_0$, the independent challenge key $K^*$ and these decapsulations give exactly the random game. Conditional on $(pk,Y)$, replacing the value at the single target input by an independent uniform key again gives a uniform random function. Under $H_1$, $K^*$ equals that value, giving exactly the real game; permitted decapsulations agree with both hash frontends. The adversary can compute hashes for arbitrarily chosen public-key strings in either world. The independent off-slice oracle accounts for them.

## Classical ROM bound

If a classical distinguisher makes at most $q_H$ hash queries, there is an inverter with success probability $p_{\mathrm{cl}}$ satisfying

$$
\Delta_{\mathrm{cl}}\le p_{\mathrm{cl}}.
$$

Run the random-game simulation. Inspect each on-slice hash query and return its $x$ if $F_{pk}(x)=Y$. Until the first such query, all responses and the challenge in the coupled real and random games are identical. The chance that the output probabilities differ is therefore at most the probability of seeing that query. Reusing the sampled response for duplicate inputs preserves the ideal-oracle distribution, including consistency between hash and decapsulation queries. The inversion cost includes the adversary, parsing, table maintenance, and at most $q_H$ forward evaluations for the simulated hash calls.

## QROM bound with classical decapsulation

Let the quantum distinguisher make at most $q_H$ sequential hash queries, counting individual input registers. A simultaneous batch may be serialized. For $q_H\ge1$, there is an inverter in the stated auxiliary-oracle experiment with success probability $p_{\mathrm q}$ such that

$$
\Delta_{\mathrm q}\le \min\{1,2q_H\sqrt{p_{\mathrm q}}\}.
$$

Here quantum access applies to the public hash. The game gives classical input and output access to decapsulation. We make no separate claim for coherent decapsulation or for implementation leakage.

**Proof.** Pad unused hash-query slots with a fixed off-slice input and disregard the answer; this also handles early termination. Condition on fixed keys, oracles and challenge values. Purify intermediary measurements and classical messages using an environment, including the decapsulation channel. All between-query operations now have a common unitary dilation in the two games. Write $\psi_i^0$ for the entire state immediately before the $i$th hash query in the random-game run, and $\Pi_*$ for the projector onto input $S_{pk}(X)$, where $X$ is the unique preimage of $Y$.

The two XOR hash-query unitaries agree on every input outside this one-dimensional input subspace (with unrestricted answer and workspace registers). On the target subspace their difference has operator norm at most two. Insert the queries of one world into the other, one slot at a time, retaining the $H_0$ prefix and $H_1$ suffix. Unitary invariance and the triangle inequality bound the distance between final state vectors by $2\sum_i\|\Pi_*\psi_i^0\|$. The difference in probability of any output event is at most the trace distance, itself bounded by this vector distance. Averaging over the sampled data and using Cauchy–Schwarz gives

$$
\Delta_{\mathrm q}\le 2q_H
 \sqrt{\mathbb E\!\left[\frac{1}{q_H}\sum_{i=1}^{q_H}\|\Pi_*\psi_i^0\|^2\right]} .
$$

The bracketed probability is achieved by an inverter: select a uniform query slot, simulate the random-game prefix with the auxiliary oracle, measure that slot's input in the computational basis, and return the decoded $x$ on a target-slice input. It may report failure on an off-slice input. The event of obtaining precisely $S_{pk}(X)$ in that measurement is exactly inversion. The inverter stops at the selected slot, so the measurement does not affect later probabilities in this experiment. Its cost includes coherent framing, public permutation evaluation and uncomputation, the independent oracle accesses and the execution of the distinguisher's prefix. The reduction incurs a quadratic loss when converting a distinguishing advantage into an inversion success probability. If $q_H=0$, the two one-stage games have identical views and $\Delta=0$.

## Prechallenge queries and CPA

A two-stage convention may allow up to $q_{\mathrm{pre}}$ classical decapsulation queries before a uniformly drawn challenge ciphertext is revealed, even if one of these queries happens to equal the later challenge. For that convention, add at most $2q_{\mathrm{pre}}/N$ to the corresponding displayed bound, clipping the final bound at one.

To see this, presample the uniformly distributed $Y$ and keep it hidden during the first stage. In each original game, conditional on $pk$, $Y$ is independent of the original hash, prechallenge randomness, and the entire original prechallenge transcript. The key correlated with the hash in the real game is revealed only later. Thus the probability that a prechallenge query names $Y$ is at most $q_{\mathrm{pre}}/N$. Modify each original game to reject $E(Y)$ before the challenge too. Couple each with its modification until the first query to $E(Y)$; each output probability changes by at most that hit probability. The modified games are covered by the earlier simulations with the challenge withheld until stage two. For the quantum bound $q_H$ counts all hash queries across both stages. Applying the triangle inequality gives the stated conservative two-game correction.

Removing the decapsulation oracle specializes these results to IND-CPA. Single-user security, perfect correctness and both ideal-hash reductions remain conditional on the listed assumptions where appropriate. An original SG-DIFRA trapdoor-permutation family, a proof of its average-case classical or quantum one-wayness, and concrete time/advantage bounds for the three profiles remain outstanding. The reference code implements a concrete KDF and a publicly invertible control. Its output agreement exercises syntax and correctness only.
