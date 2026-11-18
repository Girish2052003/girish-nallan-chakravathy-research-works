# A compact standalone private key

An optional storage format holds two seeds. One 32-byte seed is public and regenerates the base matrix. The second seed stays private and regenerates the receiver's signed supports. The receiver reconstructs its public check columns when it checks an encapsulation. This gives standalone private keys of **80, 96 and 112 bytes** in the three target rows. The public keys and ciphertexts are exactly those of the per-recipient seeded-matrix format. Even the smallest target still sends a 12.29 GB public key and a 3.35 MB ciphertext in decimal units. The byte savings do not establish a security level.

| Target | Public matrix seed | Private check seed | Standalone private key | Public key | Ciphertext |
|---:|---:|---:|---:|---:|---:|
| 128 | 32 | 48 | 80 | 12,285,243,257 | 3,348,787 |
| 192 | 32 | 64 | 96 | 53,618,422,002 | 8,567,191 |
| 256 | 32 | 80 | 112 | 126,797,581,733 | 15,210,996 |

## Algorithms and perfect correctness

Independently sample the public matrix seed and a uniform $\kappa$-bit secret check seed $K$ with $\kappa$ a positive multiple of eight. For the parameter tables use $\kappa=2b+128$ where $b$ denotes the target row. A dedicated variable-output function $F$ expands $K$ into a tape of predetermined length for the whole ordered tuple of signed supports. Its framed input binds the seeded matrix suite, private seed width, and check-sampling slack $\sigma_s$. The dedicated private-expansion domain differs from every FO and matrix domain. Regeneration uses the exact same frame. The wire orders the public matrix seed first, then the private seed.

For slot $j=0,\ldots,t-1$, let $R_j=2^w\binom{m-jw}w$ and $B_j=\lceil\log_{256}R_j\rceil$. Read $B_j+\lceil\sigma_s/8\rceil$ bytes in big-endian order. Reduce the integer modulo $R_j$. Store the resulting rank in the ordinary $B_j$-byte format and use the existing unranking algorithm on the remaining positions. This procedure always produces $t$ disjoint signed supports of the prescribed weight. Generate the syndrome columns from those supports using the seeded public matrix. The existing encapsulation and decapsulation computations apply without changing any public message. In particular, the reference's private decryption remains perfectly correct for every generated key and every honest encapsulation tape. The private storage savings require the receiver to expand the checks and recompute the syndromes.

## Security accounting for secret expansion

Consider a single target recipient. Let $\epsilon_s$ bound the raw distinguishing advantage between $F(K)$ and a uniform tape of the same length, where $K$ is hidden and uniform. The test has the resources to simulate the KEM, quantum access to the public expansion algorithm or oracle, and the same independent ideal oracles used by the seeded-matrix proof. A concrete SHAKE claim needs this post-quantum pseudorandom-generator property in the chosen oracle model.

Given a candidate tape, the tester computes all supports, generates the independent matrix seed, and builds the recipient's public key. It can simulate the whole real or random shared-key experiment, including classical decapsulation, using the expanded supports. Thus the two tape choices change the adversary's outcome probability in either world by at most $\epsilon_s$. For an independently uniform tape, each slot has statistical distance at most $2^{-\sigma_s}$ from its exact uniform rank. Indeed its possible ranks have floor or ceiling of $256^{B_j+\lceil\sigma_s/8\rceil}/R_j$ preimages. Disjoint blocks are independent; the distance of their joint distribution from independent exact ranks is at most $\nu_s=t2^{-\sigma_s}$, clipped at one. Turning ranks into supports and running the protocol are postprocessing. Therefore the seed-only format has raw single-user KEM gap at most

$$
\min\big(1,\;\Delta_{\rm seeded\ matrix}+2\epsilon_s+2\nu_s\big).
$$

Here $\Delta_{\rm seeded\ matrix}$ already includes the matrix-sampling and encryption-coin terms and the chosen-ciphertext reduction. The two additive terms arise from changing the recipient key generation in the complete experiment. They apply after the FO bound. The same argument works with zero decapsulation queries for KEM IND-CPA. The reference format using independently sampled supports retains its original theorem without this extra hypothesis.

**Independent ideal-oracle bound.** If the dedicated private expansion is itself modeled as a fourth independent quantum random oracle, $q_s$ queries by the distinguisher give

$$\epsilon_s\le\min(1,2q_s2^{-\kappa/2}).$$

To see this, sample independent $K$, a uniform tape $Y$, and a random function $F$. In the uniform-tape experiment give the tester $Y$ and access to $F$. In the generated-tape experiment give it the same $Y$ and access to $F'$ formed by replacing just the target input's output with $Y$. This second experiment has the correct joint law of a random function and its output on hidden $K$. For variable-length output, replace the relevant prefix and retain an independent suffix. In the unmodified experiment, the query state at each step is independent of $K$, even conditioned on $Y$, $F$ and the independent auxiliary oracles. The expected squared amplitude querying the target framed input is at most $2^{-\kappa}$, by summing over the distinct possible seed inputs. A single query with the two oracles changes the state-vector norm by at most twice the norm of that component. Telescoping over the queries using the unmodified states, then applying Cauchy–Schwarz and the bound of trace distance by state-vector distance, gives the inequality. The simulation can answer all target decapsulations from $Y$ without any query on the secret seed. The statement concerns oracle-independent auxiliary advice and the single target game.

With $q_s\le 2^b$, $\kappa=2b+128$ and $\sigma_s=2b+192$, the raw KEM overhead in that ideal model is at most $4\cdot2^{-64}+2t2^{-(2b+192)}$. For an asymptotic family and polynomial resource budgets, growing $\kappa$ and $\sigma_s$ superlogarithmically makes this overhead negligible when $t$ is polynomial. A fixed seed width alone provides no such asymptotic conclusion. This term is independent of the still-unrated ternary decoding premises. The proof treats a deployed hash as ideal only when that modeling assumption is explicitly adopted.

[Seed-only reference implementation](private_seed.py) · [Interoperability and sampler tests](test_private_seed.py) · [Raw byte arithmetic and decoding targets](PARAMETERS.md)
