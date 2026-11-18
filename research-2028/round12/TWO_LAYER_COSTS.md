# Wire cost of the two-layer evaluation map

This calculation concerns the experimental map over $\mathbb F_3$ that composes two quadratic triangular permutations and three affine transformations. The mode with an invertible middle matrix is a permutation. Replacing its middle matrix with one of rank $r=n-k$ makes the image have $3^r$ points, each with $3^k$ preimages. The table measures the cost of explicitly publishing the reduced coordinate polynomials. The degree-filtration result gives public recovery in the permutation mode and distinguishes the modes. Consequently these dimensions carry no positive security rating.

## Counting actual coefficients

Reduced polynomials over the ternary field have individual exponents at most two. There are $\binom{n+4}{4}$ unrestricted monomials of total degree at most four, including the constant. For each coordinate $i$, exactly $n+1$ of those monomials have exponent at least three on $i$: remove $x_i^3$ and the residual is constant or linear. These excluded sets are disjoint at degree four. Hence the implemented dense encoding of the vector map contains exactly

$$
 C_n=n\left[\binom{n+4}{4}-n(n+1)\right]
$$

ternary coefficients, including zeros. This is an exact count for this format; specialized structural compression could change the public-key size and what the encoding reveals.

A quadratic homogeneous shear in coordinate $j$ uses $\binom{j+1}{2}$ coefficients when there are $j$ earlier coordinates. Summing for $j=0,\ldots,n-1$ gives $\binom{n+1}{3}$ coefficients per layer. The explicit permutation-mode secret stores three $n\times n$ matrices, three $n$-trit translations and the two collections of shear coefficients. Its size in trits is

$$
 S_n=3n^2+3n+2\binom{n+1}{3}.
$$

A complete $u$-trit vector requires exactly $w(u)=\lceil u\log_2(3)/8\rceil$ bytes under fixed-width base-three ranking. Thus the reference encodings use $w(C_n)$ public-key bytes, $w(S_n)$ private-key bytes and $w(n)$ ciphertext bytes. The hashed KEM shared key uses 32 bytes. Suite and dimension are external metadata. Encoding all matrix coefficients, despite their invertibility requirement, does not imply optimal secret-key compression.

| Illustrative exponent $b$ | Lost trits $k$ | Retained trits $r$ | Dimension $n$ | Public key bytes | Private key bytes | Ciphertext bytes |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 128 | 81 | 162 | 243 | 7,283,528,690 | 982,829 | 49 |
| 192 | 122 | 243 | 365 | 54,948,471,447 | 3,290,717 | 73 |
| 256 | 162 | 324 | 486 | 228,435,938,740 | 7,721,469 | 97 |

The dimensions use the smallest integers $k,r$ with $3^k\ge 2^b$ and $3^r\ge 2^{2b}$. They illustrate two necessary considerations in a hypothetical hidden-loss proof: guessing an independent uniform member of a loss-mode fiber succeeds with probability $3^{-k}$; uniformly sampled outputs in an image of size $3^r$ may repeat after about $3^{r/2}$ samples. For an algorithm testing function collisions it must use **distinct inputs**; repeated sampling of the same input is not evidence of loss. For $Q$ distinct uniformly random inputs, each distinct pair collides with probability $(3^k-1)/(3^n-1)$ in loss mode and zero in permutation mode. A union bound gives collision probability at most $\binom Q2(3^k-1)/(3^n-1)$. The birthday scale is a classical benchmark. Neither it nor the fiber size lower-bounds the cost of inspecting algebraic keys. These are computed encoding sizes, not measurements from running multi-gigabyte parameter sets.

## A finite-field pitfall

Over $\mathbb F_3$, the expression $x^3$ and the reduced expression $x$ represent the same function. Their **formal** derivatives are respectively $0$ and $1$. Therefore comparing the Jacobian ranks of unreduced internal descriptions is not an intrinsic test on the published finite-field function. Polynomial multiplication in any reasoning about the published coordinate functions must perform the same reduction modulo $x_i^3-x_i$ as the encoder.

## Measured toy dimensions

Each entry is the median over 21 fresh private descriptions, timed sequentially in Python with `time.perf_counter`. Key generation includes compilation of the public polynomials. Public evaluation and private inversion were timed separately. The listed operations are direct backend calls. Round 11's KEM wrapper also derives the public coefficients from the private description during key generation and decapsulation.

| Dimension | Public key bytes | Private key bytes | Ciphertext bytes | Key generation ms | Public evaluation ms | Private inversion ms |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 4 | 4 | 1 | 0.444 | 0.030 | 0.070 |
| 3 | 14 | 9 | 1 | 1.250 | 0.064 | 0.104 |
| 4 | 40 | 16 | 1 | 2.966 | 0.126 | 0.174 |
| 5 | 96 | 26 | 1 | 6.821 | 0.267 | 0.217 |
| 8 | 671 | 77 | 2 | 50.565 | 1.372 | 0.573 |
