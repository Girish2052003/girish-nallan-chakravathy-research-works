# Public Reed–Solomon payload encoding

The `rs` suite encodes a fixed-width message in fewer ternary coordinates than bitwise repetition for the three illustrative layouts. Its correction guarantee covers the residual that the private checks produce. All field data and evaluation points are public.

## Encoding and length

For a message of $K\ge1$ bits and a bound of $z\ge0$ corrupted trits, choose the smallest $b\ge1$ for which $k+2z\le3^b$, with $k$ the least integer satisfying $3^{bk}\ge 2^K$. Write $q=3^b$, $L=k+2z$ and $t=bL$. The field uses the Round 12 polynomial basis where an irreducible modulus is tabulated. Otherwise choose the first monic irreducible in order of increasing base-three rank of its lower coefficients, skipping zero constant terms. The implementation checks irreducibility with the finite-field Rabin criterion.

Expand the integer message in $k$ base-$q$ digits, least significant first. Interpret these digits as the coefficients, starting at degree zero, of a polynomial $f$ over $\mathbb F_q$. Evaluate $f$ at the distinct field elements of rank $0$ through $L-1$. Expand the resulting field ranks into $b$ ternary basis coordinates each, again least significant first. A field rank names a polynomial-basis element. Operations on ranks are field operations.

**Correction theorem.** Every codeword with at most $z$ altered trits decodes to the original message. Two distinct messages give polynomials whose difference has at most $k-1$ roots, hence their evaluations differ in at least $L-k+1=2z+1$ symbols. Changing at most $z$ trits affects at most $z$ symbols. The original evaluations are therefore the unique codeword within the symbol radius.

## Decoder

Use Gao's partial Euclidean decoding algorithm. Let $G=\prod_i(X-a_i)$ and interpolate $R$ of degree less than $L$ with $R(a_i)=y_i$. Starting from $(G,0),(R,1)$, apply the Euclidean recurrence to the pairs $(r,v)$, preserving $r\equiv vR\pmod G$. Stop at the first pair with $\deg r<k+z$, counting zero as degree $-\infty$. Initially $v=1$. After any Euclidean step $\deg v=L-\deg r_{\rm prev}$, as follows from the leading term of the quotient times the preceding multiplier. Thus the stopping multiplier is nonzero and has degree at most $z$.

Let $E$ be the product of the $X-a_i$ at actual symbol errors, so $\deg E\le z$. Since $G$ divides $E(R-f)$, it divides $E(r-vf)$. The latter polynomial has degree less than $L$, forcing $r=vf$. This includes the zero message and every error count below the bound. The implementation divides, checks degree and distance, and rejects a recovered integer of rank $2^K$ or greater. A word outside all supported message balls returns failure. With schoolbook polynomial arithmetic the decoder uses $O(L^2)$ field operations, counting an inversion as a field operation, and $O(L)$ working field elements.

The security reductions rely on the separate generated-key assumptions and on the injectivity and correction radius proved here. The RS code supplies public error correction. [Gao, *A New Algorithm for Decoding Reed–Solomon Codes*](https://www.math.clemson.edu/~sgao/papers/RS.pdf)
