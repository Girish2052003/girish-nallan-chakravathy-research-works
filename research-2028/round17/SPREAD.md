# Ciphertext spread from the ternary error

For a fixed public key and message, the spread parameter $\gamma$ bounds the probability of the most likely randomized base ciphertext by $2^{-\gamma}$. The [explicit-reject FO theorem](../round14/CCA_PROOF.md) uses this quantity to bound the chance of querying particular ciphertexts. The ternary error already gives enough spread to exceed the registered nonce lengths on both the [full matched layout](../round16/MATCHED_PROOF.md) and the shorter half-radius layout.

## Point probabilities

Write $N$ for the full length of the noise vector, $w$ for its signed Hamming weight, $D$ for the number of coordinates deleted before transmission and $W_N=2^w\binom Nw$. For a uniform signed error, a specified remaining vector with $j$ nonzero coordinates has probability
$$
a_j=\frac{2^{w-j}\binom D{w-j}}{W_N}.
$$
There are $w-j$ further signs and positions to choose in the discarded coordinates. The feasible range is $\max(0,w-D)\le j\le\min(w,N-D)$. With $D=0$ every feasible outcome has mass $1/W_N$. With $D\ge 2w$ the maximum is $a_0=\binom Dw/\binom Nw$, since the sequence $2^k\binom Dk$ is increasing through $k=w$ by its consecutive-term ratio $2(D-k+1)/k$.

The implementation draws one finite rank for the sender's input variables and error together. Let there be $V$ input choices, $A=VW_N$ joint ranks, and $b$ tape bits with $2^b\ge A2^\sigma$. Reducing the tape modulo $A$ gives each joint rank $k$ or $k+1$ preimages, where $k=\lfloor2^b/A\rfloor\ge2^\sigma$. Conditional on any fixed input choice, each signed noise vector therefore has probability at most $(k+1)/(kW_N)\le(1+2^{-\sigma})/W_N$. This bound survives projection with the corresponding fiber size. Conditional on these input variables, the ciphertext body adds a fixed ternary vector to the projected noise. Addition is bijective, and canonical serialization is injective. Averaging over the input choices gives the uniform-in-key, uniform-in-message guarantee
$$
p_{\max}\le (1+2^{-\sigma})\max_j a_j .
$$
This inequality does not require secrecy of the matrix or successful private decoding.

## Registered profiles

The integer $\gamma$ below is the largest one certified by the last inequality. Write $Q=2^{b_0-1}$ at target label $b_0$ and cap $q_G,q_D$ by $Q$. In the repository's raw-gap convention the FO spread term is at most $240 Q^2 2^{-\gamma/2}$. The last two columns give integers $u$ for which this term is less than $2^{-u}$. All figures use exact integer comparisons in the [finite checks](test_spread.py).

| Target | Full $N$ | Dropped $D$ in half-radius layout | Prior nonce bits | Full body $\gamma$ | Short body $\gamma$ | Full $u$ | Short $u$ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 128 | 10,949,100 | 1,181,184 | 640 | 12,467 | 2,467 | 5,971 | 971 |
| 192 | 24,220,296 | 2,656,512 | 896 | 19,350 | 3,673 | 9,285 | 1,446 |
| 256 | 42,763,056 | 4,721,664 | 1,152 | 26,424 | 4,883 | 12,694 | 1,923 |

An independent uniform $s$-bit nonce multiplies the bound on each complete-ciphertext probability by $2^{-s}$. Each body-only $\gamma$ already suffices for the Round 16 spread calculation. A fresh suite may therefore encode a zero-byte nonce, allocate the FO coin digest directly to the body tape and compare the entire re-encrypted body in decapsulation. Randomized base IND-CPA is preserved by discarding the independent nonce, and the private message decoder already ignores that field. Removing bytes from old ciphertexts changes the hashed suite and replay format. The saving is exactly 80, 112 and 144 bytes respectively. Correctness and all remaining terms in the security inequality must be assessed for the chosen decoder.

## All-key spread for transmitting a coset

Suppose the encoder also takes the quotient of the $N-D$ visible coordinates by a public linear subspace of rank $a\le d$. Its canonical serialized value identifies a coset. For each fixed key, message and sender input variables, a specified coset requires that the original signed error lie in a fixed affine fiber. The composite linear map from all $N$ coordinates has kernel of dimension $D+a\le k=D+\min(d,N-D)$. Translation by the fixed clean body changes only the fiber's offset.

In any affine fiber of dimension $u$, some $u$ coordinate positions determine the entire vector in the fiber: take as columns a full-rank minor of a basis matrix for its direction subspace. Every vector in the fiber of signed weight exactly $w$ has at most $w$ nonzero positions among these $u$ coordinates. Its restriction therefore has at most $\sum_{i=0}^{\min(u,w)}2^i\binom ui$ possibilities. This quantity is nondecreasing in $u$ because a restriction can be extended by zeros. The same pointwise finite-coin bound gives
$$
p_{\max,\mathrm{quotient}}\le \min\left(1,
 \frac{1+2^{-\sigma}}{2^w\binom Nw}
 \sum_{i=0}^{\min(k,w)}2^i\binom ki\right).
$$
No rank-distribution assumption is used. The uniform bound applies separately to every key, including a deficient public row space. Rank zero permits the sharper projected-noise bound above. Widths in the next table are the minimum whole nonce bytes certified by this quotient bound to recover the previous total spread target. Further quantum security terms still apply.

| Target | Prior spread target | Full quotient body $\gamma$ | Full nonce bytes | Short quotient body $\gamma$ | Short nonce bytes |
|---:|---:|---:|---:|---:|---:|
| 128 | 640 | 767 | 0 | 550 | 12 |
| 192 | 896 | 1,150 | 0 | 821 | 10 |
| 256 | 1,152 | 1,534 | 0 | 1,092 | 8 |

The [calculator](spread.py) uses exact integers to sum the displayed binomial terms. Descending from $T_i=2^i\binom ki$, it obtains $T_{i-1}=T_i i/[2(k-i+1)]$ by exact division. The width follows by rounding the uncovered spread bits upward to whole bytes. In the short middle suite a ten-byte nonce and the quotient body together provide at least $821+80=901$ spread bits.

## Queries before challenge delivery

For a variant whose decoder may fail, let $\delta$ bound the per-key per-message failure probability of base encryption with a uniform tape. For fixed recipient keys and random oracles write $F(m)$ for the complete deterministic FO encryption of $m$. Call a message good when the private base decoder returns $m$ from $F(m)$. The restriction of $F$ to good messages is injective, since the decoder returns a single answer. For any set $S$ of at most $q_{\rm pre}$ earlier ciphertexts, the number of messages whose FO encryption belongs to $S$ is at most $q_{\rm pre}$ plus the number of bad messages. The still-hidden uniformly selected challenge message is independent of the prechallenge decisions after fixing the keys and oracles. For each message the FO coin oracle supplies a uniform tape before conditioning; by averaging over its choice, the expected bad fraction is at most $\delta$.

Consequently the probability of having already submitted the future challenge is at most $q_{\rm pre}2^{-\ell}+\delta$ for $\ell$ message bits. The argument allows the early query set to correlate with which messages are bad. Coupling each of the real and random key experiments to one that blacklists that challenge throughout yields raw-gap overhead at most $2(q_{\rm pre}2^{-\ell}+\delta)$. When $q_{\rm pre}=0$ the overhead is zero directly. With perfect correctness take $\delta=0$. The full QROM bound separately includes the FO theorem's decryption-failure term for an imperfect scheme.

The spread calculation concerns the finite random tapes of the base PKE. The KEM theorem models the domain-separated FO functions as quantum random oracles. Replacing those ideal functions by the fixed SHAKE256 implementation remains a cryptographic modeling assumption.
