# A shorter ternary code for the receiver's residuals

The private-check calculation from Round 14 returns a public codeword with at most $z$ corrupted trits. This variant uses a concatenation of two classical codes. A Reed–Solomon code spreads information over several field symbols, and a ternary extended Golay code protects the six-trit groups in each symbol. Their distances multiply. Fewer secret checks and check columns suffice for the same message width and guaranteed error bound. The outer code is public and introduces no decoding-hardness assumption.

| Design target | Message bits | Correctable trit errors | RS dimension $k$ | RS length $L$ | New trits $t$ | Round 14 trits |
|---|---:|---:|---:|---:|---:|---:|
| 128 | 384 | 768 | 41 | 297 | 3,564 | 10,997 |
| 192 | 512 | 1,152 | 54 | 438 | 5,256 | 18,760 |
| 256 | 640 | 1,536 | 68 | 580 | 6,960 | 24,984 |

## Encoder and distance

Work over the ternary field. For the six-trit inner messages use the systematic length-12 linear code with generator $[I_6\mid B]$. Its parity matrix is the Paley conference matrix of order six. Index the coordinates by infinity and $0,1,2,3,4$. Its diagonal is zero, its off-diagonal infinity entries are one, and its other entries are one for nonzero squares modulo five and minus one for nonsquares, using the difference of the indices. The listing in [the encoder](concatenated.py) is in this order.

The row products give $BB^\mathsf{T}=5I_6$ over the integers with signed entries. Thus $I_6+BB^\mathsf{T}=0$ over the ternary field. Each codeword has zero self-dot-product, so its Hamming weight is divisible by three. In a systematic word of total weight three, a data part of weight one produces five nonzero parity symbols. A data part of weight two would require a parity part of weight one, whose inverse image under $B^{-1}=2B^\mathsf{T}$ has weight five. A nonzero data part cannot have zero parity because $B$ is invertible. These cases eliminate weight three. Any generator row has weight six, proving minimum distance exactly six. The dimension follows from the identity block. A minimum-distance word in any of several parallel copies shows that the grouped inner distance is also six.

For $K$ bits and error bound $z$, choose the smallest positive integer $g$ such that
$$q=3^{6g},\qquad k=\lceil\log_q(2^K)\rceil,\qquad L=k+\lfloor z/3\rfloor\le q.$$
Represent the message integer in $k$ base-$q$ digits and treat these as polynomial coefficients, low degree first. Evaluate the resulting polynomial at the $L$ distinct field elements of ranks zero through $L-1$ in the declared polynomial basis. Split each field rank into $g$ base-729 digits from least to most significant and encode each six-trit group with the inner code. All profiles in the table have $g=1$. The ternary length is $t=12gL$. The field follows the same modulus-selection convention as the [Round 14 encoder](../round14/OUTER_CODE.md).

Two distinct polynomials of degree less than $k$ agree at no more than $k-1$ evaluation points. The outer distance is at least $D=L-k+1=\lfloor z/3\rfloor+1$. Each differing symbol alters at least six transmitted trits. Therefore $6D>2z$, so the radius-$z$ balls around supported messages are disjoint.

## Recovery for every pattern of at most $z$ errors

First find a nearest inner codeword for each group using a table of minimum-weight coset representatives. Compute a syndrome from the six parity trits minus the parity of the six data trits. All the errors having that syndrome form the same coset. Fill the table in increasing weight, and subtract a first minimum-weight representative to recover a nearest word. The table has 729 entries regardless of the outer dimensions. Parallel groups have additive Hamming distance, so each outer symbol gets a closest symbol and a distance $r$ to it, equal to the sum of the group distances.

The decoder tries the three reliability thresholds $j=3,2,1$. Retain the nearest symbol if $r<j$ and erase it otherwise. For a proof, choose a threshold uniformly from the three. Each symbol is then erased with probability $p=\min(1,r/3)$. If the nearest symbol is the transmitted one, its expected contribution to the count $2E+S$ of twice retained errors plus erasures is $p\le e/3$, where $e$ is the number of actual corruptions in that symbol. Otherwise the expected contribution is $2-p$. If $r<3$, the two distinct inner words imply $e+r\ge6$, giving $2-p\le e/3$. If $r\ge3$, nearest decoding gives $e\ge r\ge3$, also sufficient. Summing gives $\mathbb E[2E+S]\le z/3<D$. At least one of the three deterministic trials has $2E+S<D$. No probabilistic correctness premise is needed.

Puncture the erased positions. For that trial, the number $n=L-S$ of retained evaluations satisfies $2E\le n-k$. When $n-k$ is odd, discard one more retained evaluation; $\lfloor(n-k)/2\rfloor$ stays the same. Apply the [Round 14 Gao decoding argument](../round14/OUTER_CODE.md) with the vanishing polynomial of these *retained evaluation points* and correction radius $(n'-k)/2$ for the resulting even difference. It recovers the transmitted degree-less-than-$k$ polynomial. Finally re-encode the recovered message, require a valid $K$-bit integer, and check trit distance at most $z$ from the received word. This final check also prevents an unsuccessful earlier trial from accepting another supported message. The algorithm rejects when none passes.

The three trials use $O(L^2)$ field operations and $O(L)$ field elements of scratch space, in addition to the linear-size input/output buffers, inner lookup tables and field representation. The target profiles use table-based arithmetic in the same degree-six polynomial basis. The algorithm is a variable-time public-code reference.

The [tests](test_concatenated.py) verify the exact inner weight distribution, all cosets, all messages and allowed error patterns for a tiny code, errors requiring threshold erasures, malformed received words and one complete outer-code message at the full declared error radius for each target. These checks support the implementation. The guaranteed decoding radius follows from the argument above.

The inner-code parameters and this decoding method are classical. [Tonchev, *An Introduction to Coding Theory*, theorem 8.1](https://pages.mtu.edu/~tonchev/Coding-Theory-Tohoku-June-09.pdf) · [Forney, *Concatenated Codes*](https://ntrs.nasa.gov/citations/19660011586) · [Roth, *Introduction to Coding Theory*, chapter on concatenated codes](https://doi.org/10.1017/CBO9780511808968.013)
