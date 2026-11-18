# What the projected encoding costs

The three primary rows preserve the two Round 14 decoding distributions. Their exact wire sizes are below. The shared secret is 32 bytes throughout. A target label identifies a parameter family; concrete decoding strength remains unverified.

| Target | Transmitted check trits per public matrix row $t$ | Base trits $m$ | Body trits $m+t$ | Public key bytes | Private key bytes | Ciphertext bytes |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 3,564 | 11,182,848 | 11,186,412 | 3,981,553,087 | 80 | 2,216,336 |
| 192 | 5,256 | 27,666,432 | 27,671,688 | 15,022,416,160 | 96 | 5,482,436 |
| 256 | 6,960 | 49,065,984 | 49,072,944 | 35,323,168,790 | 112 | 9,722,492 |

For the 192-target row, the [Round 14 two-seed format](../round14/PRIVATE_SEED.md) used 53,618,422,002 public-key bytes and 8,567,191 ciphertext bytes. The reductions are **71.98% for the public key** and **36.01% for the ciphertext**. These are exact-size calculations rounded to two decimals. The reference expands the public matrix one row at a time. The target sizes do not represent measured exchanges at those dimensions.

## Why the old assumption dimensions survive

Let $t_0,m_0$ be the previous check count and number of base coordinates. Put $r=m_0-(t_0-1)w$. The new check count $t$ allows $m=r+(t-1)w$. In the key hybrid, after excluding all the other secret supports, exactly $r$ coordinates remain. The challenge matrix for that hybrid still has precisely $d$ rows and $r$ columns and the planted vector still has weight $w$. For the payload hybrid, project the original noisy word and generator onto their first $m+t$ coordinates. The encryption algorithm draws the error over the old length $m_0+t_0$ before that projection, which reproduces this law exactly. Details appear in the [native proof](NATIVE_PROOF.md).

Let $B(v)=\lceil v\log_{256}3\rceil$ be the byte width of $v$ ternary symbols, with $B(0)=0$. Splitting $d=64u+j$, $0\le j<64$, the public key contains $32+u B(64t)+B(jt)$ bytes. The 32 bytes hold the public matrix seed. Each complete block independently packs 64 consecutive rows of $t$ syndrome trits. The private key contains that seed and $\lceil\ell/8\rceil$ private seed bytes. The ciphertext comprises the indicated nonce and $B(m+t)$ body bytes. For the primary rows, the number of explicitly represented public ternary coefficients $dt$ is respectively 20,096,398,080, 75,824,149,248 and 178,290,923,520.

## Lower bound for this architecture

Consider designs that preserve $r,d,w,z$, the requirement to correct any $z$ trit substitutions, the public-seed plus check-column wire layout, the existing nonce width, and the body consisting of $m+t$ packed trits. The encoder must inject $M=2^\ell$ possible messages into ternary words with minimum distance at least $D=2z+1$. The following finite lower bound applies even to nonlinear outer codes.

Fix $j\le\lfloor\log_3 M\rfloor$ leading coordinates. Among the $3^j$ prefixes, one contains at least $K=\lceil M/3^j\rceil$ words. Select $K$ such words and delete their common prefix. For any remaining coordinate, write $n_0,n_1,n_2$ for its symbol frequencies. It contributes $K^2-\sum_i n_i^2\le 2K^2/3$ to the sum of the Hamming distances of all ordered word pairs. Summing over coordinates gives $K(K-1)D\le (t-j)2K^2/3$. Consequently
$$
t\ \ge\ \max_{0\le j\le\lfloor\log_3 M\rfloor}
\left(j+\left\lceil\frac{3D(K-1)}{2K}\right\rceil\right).
$$
Deleting any $D-1$ coordinates also leaves all messages distinguishable, yielding $t\ge\lceil\log_3 M\rceil+D-1$. The calculation takes the larger of these bounds. This uses the classical Plotkin bound with shortening and the Singleton bound. [Guruswami, Introduction to Coding Theory, Notes 4](https://www.cs.cmu.edu/~venkatg/teaching/codingtheory/notes/notes4.pdf)

| Target | Minimum check trits $t$ implied | Public-key floor even with a single ideal packing block (bytes) | Ciphertext floor (bytes) |
|---:|---:|---:|---:|
| 128 | 2,540 | 2,837,548,254 | 2,060,325 |
| 192 | 3,772 | 10,780,846,923 | 5,143,442 |
| 256 | 5,005 | 25,401,132,614 | 9,127,173 |

For the middle row the new public encoding is within **1.40 times** this architecture-specific lower bound and the ciphertext is within **1.07 times** its lower bound. Replacing the outer code alone cannot bring this same 192-target layout into the kilobyte range. A design that changes the trapdoor, the dimensions, the public-key structure or the error guarantee is outside this bound.

## Can a public lossless compressor shrink the same check columns?

A second counting argument addresses efficient lossless postprocessing of **existing** public keys. Give the compressor and decoder the same public seed and suite. Write $H$ for the $d\times t$ matrix of transmitted check coefficients. Suppose every relevant efficient tester has gap at most $\mu$ between the joint real distribution of the public data and $H$, and the game replacing $H$ by an independent uniform ternary matrix. The key-column hybrids give this type of assumption-dependent bound, with seed/oracle corrections for the chosen variant. Charge the compressor and decoder's running times against the assumed resources.

Suppose a public encoder emits a fixed-width $b$-bit string and the public decoder exactly reconstructs the real $H$ with probability at least $1-\eta$. Then
$$
1-\eta\ \le\ \mu+\frac{2^b}{3^{dt}}.
$$
Indeed the predicate that tests reconstruction is efficient. For a uniform $H$ and fixed public side data and random coins of the decoder, its range contains at most $2^b$ matrices. Randomized encoding does not enlarge that range. Averaging over side data and coins gives the uniform-game term. The allowed distinguishing gap bounds the difference in success probabilities. With variable bit length at most $b$, replace $2^b$ by $2^{b+1}-1$. A new key generator with additional correlated setup, a secret-only encoding, or a public representation that never reconstructs the old $H$ is outside this theorem. It shows why simply seeking a general-purpose compression algorithm for the current hard public columns cannot yield a large saving if the assumption holds.

## Smaller dimension experiments

A separate arithmetic choice sets the transmitted base $m=2tw$, $h=\lfloor m/3\rfloor$, and the source base $m_0=m+(t_0-t)w$. The native algorithm runs with these values. The source key and noise dimensions change, so a separate hardness assessment is required. Here are the resulting byte counts. The target identifies the source of the remaining layout choices.

| Target | Public key | Private key | Ciphertext |
|---:|---:|---:|---:|
| 128 | 1,294,315,463 | 80 | 1,085,357 |
| 192 | 4,222,727,200 | 96 | 2,400,356 |
| 256 | 9,872,992,406 | 112 | 4,237,558 |

A small engineering instance makes a complete exchange possible on an ordinary machine. Set $\ell=256,h=512,n=8,m_0=6440,w=4,z=64$, use the Round 14 RS source with 192 bits of coin slack, and transmit a 64-byte nonce. Key generation, encapsulation and decapsulation produced actual serialized sizes of 62,573 public-key bytes, 64 private-key bytes, 1,273 ciphertext bytes and a matching 32-byte shared key. This instance is a functional benchmark. Its check distribution has only $2^4\binom{3224}{4}<2^{47}$ possible planted signed vectors per challenge. Its key and noise assumptions are distinct from the three large rows.

From this directory run `python3 projected_sizes.py` for all tables. Reproduce the small exchange separately:

```python
from projected_sizes import engineering_example

kem = engineering_example()
public, private = kem.keygen()
ciphertext, sender_key = kem.encaps(public)
assert kem.decaps(private, ciphertext) == sender_key
print(len(public), len(private), len(ciphertext), len(sender_key))
```
