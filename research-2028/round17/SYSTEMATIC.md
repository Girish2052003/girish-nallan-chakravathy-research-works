# Standalone KEM with an identity block and private ciphertext replay

The primary 192 layout has a 7,088,151,760-byte public key, a 96-byte private key and a 1,871,132-byte ciphertext for **every** generated key. Its receiver reconstructs at most 1,152 public matrix rows while verifying one ciphertext, without regenerating the public key. The proof uses the same Round 16 ternary decoding distribution. A conditioning factor below two in the base security bound pays for choosing an identity block. The reference implements both the shorter profile, whose certified honest key-disagreement probability is below $2^{-607}$, and a perfect-correctness profile. The security of concrete SHAKE256 and the computational hardness at the named dimensions remain assumptions.

## Algorithms and exact correctness

Let $d,m,t,w$ be the underlying full- or short-radius parameters. Replace its public iid base matrix by $A=[I_d\mid B]$, where the public seed expands $d$ independent ternary rows of length $m-d$ in the ideal description. As before, the private seed expands to disjoint signed check columns $S$. Publish the matrix seed and $V=AS$, packed in the same blocks of up to 64 rows. For the $i$-th row one needs only the $i$-th entry of the pivot part of each private check plus its inner product with row $i$ of $B$ on the remaining positions. Key generation streams the rows of $B$.

Now the public row space has generator $[I_d\mid B\mid V]$. Start from the encoded message in the final $t$ coordinates and the finite-tape signed noise projected to the $N=m+t$ transmitted positions. Write this word as $(x,u,v)$ in blocks of lengths $d,m-d,t$. The unique representative with zero pivot coordinates has transmitted remainder
$$
(u-B^\top x,\ v-V^\top x).
$$
The encrypted message contributes zero to $x$. Projecting the selected native noise therefore gives at most $w$ nonzero pivot entries. The sender streams through the relevant rows of $B,V$ and adds the surviving nonpivot errors directly. The original random linear and quadratic masks vanish in this quotient, exactly as in the [row-space proof](QUOTIENT.md). The coin derivation still uses the original finite joint rank distribution. The sender also transmits the selected nonce.

The private decoder conceptually lifts the remainder by prefixing $d$ zeros, then applies its original residual computation and message decoder. When comparing the proposed ciphertext with its re-encryption, it computes the required rows of $V$ from the regenerated private checks, row by row. It returns the candidate's hash-derived key only on exact equality of the entire ciphertext, including the nonce. Malformed encodings and a failed decode return the explicit failure symbol. For every legal private key, taking the quotient preserves its residual exactly. Thus the full-radius decoder has perfect correctness. The [other decoder](outer_proof.md) has the same per-key per-message bound on decoding failure over honest base coins. In the ideal hash model this bound also applies to an honest KEM exchange over the coins oracle and message, with fresh oracle values in this suite.

The coins hash and shared-key hash use separate domains and bind the suite and 32-byte public matrix seed. Consequently the receiver knows the complete hash context from its private key. In the one-recipient experiment the seed is sampled independently of those oracle domains. The two selected slices on messages are independent random functions conditional on the seed and the key-generator domains. Other hash slices remain independent. An adversary may evaluate the public algorithms using any proposed key or the same seed, with all its queries charged to the game. These arguments do not supply multi-recipient or key-binding security. In particular the seed is not asserted to be a collision-resistant commitment to the entire key.

## The security reduction

Begin with the **explicit iid** base encryption game from the chosen radius proof, with original $d$ rows and independent entries of the $d$-by-$m$ base matrix $A_0$. Split $A_0=[P\mid U]$ at the first $d$ coordinates. If $P$ is invertible, left multiplication by $P^{-1}$ yields $[I_d\mid B]$ with $B=P^{-1}U$. Conditional on any invertible $P$, the columns of $B$ are independent uniform vectors. The secret columns $S$ retain their original distribution, independently of $P,U$. Accordingly the transformed public check matrix $P^{-1}(A_0S)$ has precisely the required law. The simulator can compute that matrix from the original public coefficients without knowing $S$.

Pass the normalized public key to the systematic base adversary and forward its selected challenge messages. Given the original randomized base ciphertext, eliminate the first $d$ positions using the normalized rows. Every original mask term lies in their span. Conditional on invertibility the result has the exact systematic ciphertext law, including the finite-tape distribution of the projected noise. Attach an independent uniform nonce of the new width. If $P$ is singular, the simulator returns a fixed answer independent of its challenge bit (dummy challenge messages may be supplied as required by the game). Both worlds have the same invertibility probability
$$
p_*=\prod_{j=1}^{d}(1-3^{-j})\ge 1-\sum_{j=1}^{d}3^{-j}>1/2 .
$$
Therefore the signed gap of the old game for this simulator is $p_*$ times the systematic explicit-base gap. If the original explicit-base raw gap is at most $\epsilon_0$, the systematic explicit-base gap is at most $\epsilon_0/p_*$. These resource comparisons must include the simulator's dense conditioning and projection, even though the systematic KEM itself avoids elimination.

To implement the systematic key with a seed, first apply that conditioning argument to the exact **unseeded** matrix. Independently apply the [public row-oracle coupling](../round14/SEEDED_MATRIX.md) to the $d$ rows of the uniform tail $B$ with the new row length and fresh suite label. Each row's actual modulo sampler has variation distance at most $2^{-s_A}$ in that ideal hash model. The simulation lifts a row to a uniformly chosen preimage in the programmed hash slice, with fresh independent outputs elsewhere, exactly as in the linked proof. The total addition to the raw two-message bound is at most $2d2^{-s_A}$. Do not condition an already fixed SHAKE seed on an invertible submatrix. The actual key generator produces the identity block directly.

More explicitly, with $t$ the chosen check count, $p_h,p_d$ the Round 16 rank probabilities on the **original** full-length source, $\nu$ the joint coin sampling distance and $\eta$ the raw common ternary distinguishing gap at the composed resources, the randomized PKE bound is
$$
\epsilon_{\rm sys}\le\min\left(1,
\frac{2(t+p_h/p_d)\eta+2(1-p_h)+2\nu}{p_*}+2d2^{-s_A}\right).
$$
Apply the explicit-reject KEM transform to this base scheme using its actual combined spread from the [affine-fiber count](SPREAD.md). Use the corresponding worst-case correctness term, the seed-hiding hybrid and the two-stage correction from the radius proof. This yields conditional single-recipient IND-CCA with classical adaptive decapsulation and quantum hash queries. The IND-CPA conclusion follows by setting the decapsulation count to zero. The [classical ROM argument](CLASSICAL.md) also covers the shorter decoder and charges its failure bound. The ordinary conditional coding assumption applies to the ideal iid ternary problem at the specified dimensions. The public-key protocol uses its own private decoder and domain-separated SHAKE256 as the implemented hash. Its constant-time behavior and target-scale work factors have not been established.

## Concrete 192-target implication

For the primary half-radius suite, $t=2952$, $p_*>1/2$, $2(t+p_h/p_d)/p_*<11{,}816$ and the additive PKE terms are below $2^{-316}$. The spread is at least 901 bits; using 896 bits conservatively recovers the earlier target. For a single honest recipient let $q$ count the two FO hash oracles together, $D$ their combined query depth, $q_D$ the classical decapsulation queries, $q_{\rm pre}$ the prechallenge subset and $q_S$ the private-seed oracle queries. With $\ell=\kappa=512$ and $s_S=576$, a sufficient bound on the raw quantum KEM distinguishing gap is the smaller of one and
$$
8\sqrt{(D+q_D)\epsilon_{\rm sys}}
+16(q+q_D)2^{-256}+48q_D(q+4q_D)2^{-448}
+2q_{\rm pre}2^{-512}+4q_S2^{-256}+2t2^{-576}
+\bigl(20(q+2q_D+1)^2+2\bigr)2^{-607}.
$$
The last extra $2\delta$ can be omitted when $q_{\rm pre}=0$. In the formula it is conservatively included even in that case. This uses the published explicit-rejection theorem and the [per-key decoding bound](outer_proof.md).

Taking $q,q_D,q_S\le2^{191}$ yields guessing success below 50.8% if $\eta\le2^{-224}$, and below $1/2+2^{-34}$ if $\eta\le2^{-280}$. These sufficient implications are checked using [exact rational arithmetic](test_classical.py). Conversely, a raw KEM gap of at least $1/8$ at that query budget implies the existence of a common-syndrome tester with raw gap above $2^{-221}$ in the ideal reduction. Indeed the additive KEM terms sum to less than $1/16$, $64(D+q_D)\le2^{198}$, and subtracting $2^{-316}$ then dividing by $11{,}816<2^{14}$ yields that lower bound on $\eta$. The [coherent witness reduction](../round14/WITNESS_PROOF.md) gives planted search success at least $4\eta_{\rm tester}^2/9>2^{-444}$ for that tester. The resource budget must include the tester, its adjoint, oracle simulations and full-matrix operations. This implication concerns the generated witness distribution, and gives no numerical lower bound on all algorithms solving it.

## Exact widths and resources

| Target | Outer radius | Public key, bytes | Private key, bytes | Nonce, bytes | Ciphertext, bytes |
|---:|---:|---:|---:|---:|---:|
| 128 | Half | 2,201,315,732 | 80 | 12 | 849,798 |
| 192 | Half | 7,088,151,760 | 96 | 10 | 1,871,132 |
| 256 | Half | 16,482,794,077 | 112 | 8 | 3,297,407 |
| 128 | Full | 3,868,545,931 | 80 | 0 | 1,083,802 |
| 192 | Full | 12,620,284,606 | 96 | 0 | 2,397,431 |
| 256 | Full | 29,506,137,220 | 112 | 0 | 4,232,857 |

Each ciphertext width is fixed by the profile because its public generator has the identity block. Each shared key is 32 bytes. The reference holds the public wire key at the sender, validates its packed blocks, and regenerates at most $w$ tail rows during encapsulation. At decapsulation it checks the exact profile length before parsing, holds the private supports and one remainder, and regenerates at most $w$ tail rows during replay. Temporary packing buffers, the finite joint rank, code tables and the public key at key generation/encapsulation must also be counted. Generating the entire key still requires $d$ tail expansions and computation of its explicit $dt$ public check trits. This is a substantial cost at the three registered dimensions. None of the three target keys was generated in these tests.

The [implementation](systematic_kem.py) and [tests](test_systematic.py) include direct comparison to the ordinary row-space projection, exhaustive small matrix conditioning, and checks that private replay avoids constructing the whole public key. With the small half-radius fixture, a real exchange gives a 393-byte public key, a 33-byte private key, a 25-byte ciphertext, and matching 32-byte shared keys. For inspection without allocating a target key, use:

```python
from systematic_kem import research_profile

kem = research_profile(192)
print(kem.public_bytes, kem.private_bytes, kem.ciphertext_bytes)
```
