# Shortening the standalone KEM with a certified decoding-failure bound

The [Round 16 KEM](../round16/MATCHED_PROOF.md) corrects every legal error. This variant trades a small, explicitly bounded probability of honest decoding failure for fewer public check columns. It retains the same ternary hardness experiment at each target. We give a bound for **every generated key and every message** over the sender's finite random encryption tape. Concrete decoding hardness and the cost of this construction at the named sizes remain open.

## Construction and receiver

Let $w$ be the original weight of both sender errors and private checks, $N_0$ the Round 16 full body length, $r$ the common source column count, and $d$ the common row count. Choose a radius $u$ from $0$ through $w$. Use the public [Golay–Reed–Solomon code](../round15/OUTER.md) for the original message width and radius $u$, of ternary length $t$. Require $t$ no larger than the original length. Choose $m=r+(t-1)w$ and transmit $N=m+t$ trits. These choices leave the common source dimensions, the numbers of linear and quadratic mask variables, the unchanged full coin space and the nonce width intact. The key still consists of a public row seed and $t$ secret-check syndromes in the existing block format. Key generation and encryption have distinct suite tags across variants and radii. The receiver reconstructs its private checks from its seed. [Reference](outer_kem.py)

Draw a signed weight-$w$ error on **all $N_0$ positions** and project to the first $N$ coordinates. The body adds these trits to the public mask and the shorter encoded message. The private subtraction cancels the mask exactly. Each of the $t$ disjoint private checks has $w$ base coordinates and one transmitted check coordinate. These $t$ groups are disjoint. A residual whose group is untouched is correct. Let $H$ count errors hitting the union of the groups. The number of incorrect residuals is at most $H$, even when several errors hit one group or cancel. Thus $H\le u$ guarantees correct decoding and verification by full re-encryption. For $u=w$ this argument gives perfect correctness again.

## A bound for every honest key and message

The union of relevant coordinates has size $U=t(w+1)$. For any fixed secret checks, a uniformly random $w$-element error support on $N_0$ coordinates gives $H$ the hypergeometric distribution with population $N_0$ and $U$ selected elements. The public matrix, message, error signs and masking variables do not affect this count. For any real $x\ge 1$,

$$
\mathbb E[x^H]=\sum_{j=0}^{w}\binom wj(x-1)^j\frac{(U)_j}{(N_0)_j}
\le (1+(x-1)U/N_0)^w,
$$

where the falling-factorial ratio is the chance that $j$ specified draws all hit the union. It is at most $(U/N_0)^j$. Markov's inequality bounds $\Pr[H>u]$ by the last expression divided by $x^{u+1}$.

The actual encryption draws a uniform integer on $2^b$ possibilities and reduces it modulo the joint rank count $A$ of the mask and signed error. The sender tape satisfies $2^b\ge 2^\sigma A$. A particular rank has probability at most $\lceil 2^b/A\rceil/2^b\le (1+2^{-\sigma})/A$. Summing over any bad set preserves this multiplicative factor, including very rare events. Therefore at tilt $x=6$ the finite-tape failure probability satisfies

$$
\delta_{\rm wc}\le\min\!\left(1,(1+2^{-\sigma})\frac{(1+5U/N_0)^w}{6^{u+1}}\right).
$$

The guarantee also holds for the seeded matrix and the real private sampler. Each generated key has precisely the required disjoint supports. A fresh honest encapsulation in the ideal-hash experiment uses the same random-tape law for its chosen message. Applying the numerical failure probability to a fixed SHAKE implementation entails the usual hash-model assumption.

## Composition with the one-distribution theorem

The [original key hybrid](../round16/MATCHED_PROOF.md) uses a $d$-by-$r$ challenge in the coordinates outside the other $t-1$ checks, exactly $m-(t-1)w=r$ positions. Only the number of column hybrids changes. In the payload hybrid, use the original common-syndrome padding, full-rank conversion and affine-fiber sampling at the original $N_0,h,d$. Project **both** its generator and its received word onto the first $N$ coordinates. The planted case gives the masking rows plus the projected signed error in the new protocol. Independent uniform input gives independent uniform output under projection. Add the quadratic rows and shorter encoded message as before. These two steps preserve the Round 16 common decision assumption at its actual dimensions and the [generated-witness implication](../round16/MATCHED_PROOF.md). In the base bound substitute the new $t$ and keep the original rank-defect terms. The joint encryption-coin and seeded-row couplings still apply.

Let $q=q_G+q_H$ count FO hash queries and let $q_D$ count classical decapsulation queries. Use the same one-recipient quantum random-oracle experiment as Round 16. The public uniform nonce supplies the same spread. The explicit-reject FO theorem with nonzero worst-case decryption error adds at most $20(q+2q_D+1)^2\delta_{\rm wc}$ to the previous **raw** KEM gap. This conservative expression counts both the extra hash calls in the simulator and the decryption calls in its failure-finding bound. The factor of two converts guessing advantage to the raw gap. Set $q_D=0$ for KEM IND-CPA. [Hövelmanns and Majenz, Theorems 1–3 and Definition 4](https://eprint.iacr.org/2023/1811.pdf)

If the game permits prechallenge decapsulations, add $2q_{\rm pre}/2^\ell+2\delta_{\rm wc}$ instead of the previous $2q_{\rm pre}/2^\ell$. To see this, fix the keys and random functions and call a message good when its canonical deterministic FO encryption decodes to itself. Good messages have distinct ciphertexts because base decryption is deterministic. For a uniform independent hidden challenge message, at most $q_{\rm pre}$ good messages can yield a ciphertext on a fixed phase-one query list. The expected fraction of bad messages is at most $\delta_{\rm wc}$. Couple the game on the complement of these events, and sum over both challenge worlds. The private-expansion seed hybrid is unchanged apart from $t$. The simulator supplies the same rejection behavior even when an honest input fails.

## Registered half-radius costs

| Target | $u$ | $t$ | Public key, bytes | Private key, bytes | Ciphertext, bytes | Per-key, per-message failure probability below |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 384 | 2,028 | 2,201,315,732 | 80 | 1,935,303 | $2^{-399}$ |
| 192 | 576 | 2,952 | 7,088,151,760 | 96 | 4,272,336 | $2^{-607}$ |
| 256 | 768 | 3,888 | 16,482,794,077 | 112 | 7,536,917 | $2^{-813}$ |

The three size rows and Chernoff bounds use exact integer arithmetic. At the 192 target the KEM public key uses 43.84% fewer bytes and the ciphertext uses 10.97% fewer bytes than the Round 16 format. For $q,q_D\le 2^{191}$ the raw failure term including the optional $2\delta_{\rm wc}$ is below $2^{-217}$, since $20(3\cdot 2^{191}+1)^2+2<2^{390}$. The 192 target's displayed Round 16 sufficient conditional gap examples still follow: the coefficient $2(t+p_h/p_d)$ decreases by 4,608, while the old gap proof has ample slack for this additive term. The width figures come from serialization arithmetic. The executed exchange uses a small test fixture. The numerical failure certificate bounds honest decoding failure, including any key disagreement, and its effect on the security proof. It supplies no positive lower bound on computational hardness.
