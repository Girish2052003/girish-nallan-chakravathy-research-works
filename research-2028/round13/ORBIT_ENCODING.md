# Exact private representation of the affine-power orbit

Each parameter set specifies a polynomial basis of $K=\mathbb F_{3^n}$, with first basis element $1$, and public exponents $0<i<j<n$. The central map is $f(t)=t^d$ for $d=1+3^i+3^j$. The exponent is verified coprime to $3^n-1$ for every listed profile. The private inverse applies the inverse output mask, raises to $d^{-1}\bmod(3^n-1)$, and inverts the input mask. Both exponents are positive on zero. Field arithmetic and profile widths have been tested through $n=325$. The implementations use variable-time Python arithmetic.

## Why one affine column can be omitted

For an unrestricted inner affine bijection $S$, let $\lambda=S_{\rm lin}(1)$. It is a nonzero element of $K$. Write $M_t$ for multiplication by $t$ in the field. Replace the two masks by

$$S'=M_{\lambda^{-1}}\circ S,\qquad T'=T\circ M_{\lambda^d}.$$

Because $f(\lambda x)=\lambda^d f(x)$, $T'\circ f\circ S'=T\circ f\circ S$ pointwise. The linear part of $S'$ sends $1$ to $1$, so its first matrix column is $(1,0,\ldots,0)^\intercal$. Conversely every normalized pair $(S',T')$ and every $\lambda\ne0$ give exactly one unrestricted pair $S=M_{\lambda}\circ S'$ and $T=T'\circ M_{\lambda^{-d}}$. This is a bijection of the unrestricted mask space with the product of the normalized pair space and $K^\times$. Therefore choosing the normalized inner mask uniformly, and the outer mask uniformly and independently, reproduces the **exact original distribution of public functions**. Raw private pairs and normalized private pairs have different supports.

The implementation draws all free matrix entries independently and uniformly over $\mathbb F_3$, rejecting and retrying when a matrix is singular. Each translation vector is independent and uniform. The fixed input column is reinstated at parse time. This uses $2n^2+n$ private trits. It removes $n$ stored trits from the unrestricted two-matrix representation, without claiming bit-optimal compression of the remaining invertibility constraints or other symmetries.

## Wire layout

The private key concatenates four lists in order. Store the inner matrix in row-major order with column zero omitted from every row, then its translation vector. Append the whole outer matrix in row-major order, then its translation vector. The base-three rank treats the first trit as the most significant digit. For any list of $h$ trits its rank occupies exactly $\lceil h\log_2(3)/8\rceil$ bytes, big endian. The parser rejects incorrect lengths, unused ranks and singular private matrices.

The dense public key lists one $n$-trit output vector for each reduced monomial of degree at most three, including all zeros. Sort monomials by total degree and then lexicographically by their sorted, repeated variable indices. The field basis encodes $\sum_i a_i t^i$ by coefficients $(a_0,a_1,\ldots)$, so field element $1$ is the first basis element. The cubic compiler multiplies the three affine $K$-valued Frobenius factors and reduces $x_i^3=x_i$ before applying the output mask. It transmits no mask or field-factor description inside the public key. The suite and dimension are external. The suite is the ASCII string `SG-DIFRA/R13/affine-power/v1/` followed by the two indices in unsigned four-byte big-endian format. The Round 11 shared-key derivation also binds the dimension and public bytes.

| Dimension $n$ | $(i,j)$ | Full cubic public key | Old private bytes | Normalized private bytes | Ciphertext bytes | Shared-key bytes |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 82 | (22, 53) | 1,603,272 | 2,697 | 2,681 | 17 | 32 |
| 122 | (33, 78) | 7,677,285 | 5,946 | 5,922 | 25 | 32 |
| 163 | (44, 104) | 24,171,671 | 10,593 | 10,561 | 33 | 32 |
| 164 | (45, 105) | 24,764,906 | 10,723 | 10,690 | 33 | 32 |
| 244 | (66, 157) | 119,928,669 | 23,688 | 23,639 | 49 | 32 |
| 325 | (87, 208) | 375,211,457 | 41,982 | 41,918 | 65 | 32 |

Each public size is the packed width of $n(\binom{n+3}{3}-n)$ trits. The full layout directly accepts the Round 12 monomial-major cubic circuit adapter. The reduced private encoding changes the receiver's stored bytes and preserves every public key and ciphertext of the same masked function. These numbers are exact layouts for research candidates with public inversion results. We did not run full-size public-key generation. [Backend](orbit_backend.py) · [Tests](test_orbit_backend.py)
