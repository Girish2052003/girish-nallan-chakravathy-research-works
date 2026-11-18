# A centered public encoding for the masked power permutation

Let $K=\mathbb F_{3^n}$ and $F=T\circ E\circ S$, where $E(x)=x^e$ is a permutation and the public exponent $e=1+3^i+3^j$ has three distinct ternary digits ($0<i<j<n$). The suite fixes the dimension, exponent and field basis. The [reference backend](compact_orbit.py) publishes the input center $c=S^{-1}(0)$, its output $v=T(0)$, and the coefficients of the centered function $H(z)=F(c+z)-v$. This encoding saves bytes relative to the [dense cubic implementation](orbit_backend.py). The [public inversion theorem](HIDDEN_CUBIC_MONOMIAL.md) applies equally to both representations.

## Why the bytes depend only on the public function

Write $A,B$ for the linear parts of $S,T$. Then $H(z)=B((Az)^e)$ and $F(x)=v+H(x-c)$. Since $e$ is odd, $H(-z)=-H(z)$. Both coordinates and their individual exponent reductions are over the ternary field. Uniqueness of the reduced representative makes the coefficients of every even-total-degree monomial zero.

The center is unique. Every center $c$ satisfies $F(2c-x)=2F(c)-F(x)$. Two distinct centers give, by composing their reflections, a nonzero input translation with constant output difference. In central coordinates this would imply that $(t+h)^e-t^e$ is constant in $t$ for some nonzero $h$. Its ordinary univariate expansion has the nonzero term $h t^{e-1}$, since $e=1$ modulo three. Its degree is $e-1>0$ and $e<3^n$, so it cannot be constant on $K$. Thus any two secret presentations of the same function give the same $c$, the same $v$, and the same reduced coefficients. Publishing either representation identifies the same mathematical function.

For the [orbit randomization theorem](ORBIT_REDUCTION.md), if $F'(x)=V(F(U(x)))$ with public affine masks $U,V$ having linear parts $U_0,V_0$, its compact triple is

$$c'=U^{-1}(c),\qquad v'=V(v),\qquad H'(z)=V_0(H(U_0z)).$$

Substitution and coefficient reduction at degree at most three take polynomial time. The formula computes the canonical new encoding using public information. Re-encoding functions this way therefore transports the fresh-key and target law exactly. The compact implementation inherits the dense implementation’s normalized private-mask sampler, with the first inner matrix column fixed and omitted from the private encoding. Both backends sample the same secret distribution. To see that this preserves the full-mask public law, start from independent uniform full affine masks, put $a=A(1)$ and multiply $S$ on the left by $a^{-1}$ and the input of $T$ by $a^e$. The composition stays equal to $F$. Conditional on any $a\ne0$, the normalized inner linear part is uniform among matrices fixing $1$, its offset stays uniform, and the outer affine mask stays independently uniform. This is exactly the implemented distribution.

## Wire format and sizes

In one base-three vector, list first the $n$ coordinates of $c$, then the $n$ coordinates of $v$. Next list all nonzero-degree *slots* of degrees one and three, storing a zero coefficient whenever present in the layout. Use increasing total degree, then lexicographic order on nondecreasing variable-index tuples. For degree three omit the $n$ triples with all three indices equal, because $x_k^3=x_k$. For every monomial list all $n$ output coefficients before advancing to the next one. The first trit is the most significant digit. A fixed-width big-endian byte string encodes the resulting integer. The parser checks the exact length and rejects unused ranks. As in the dense backend, canonical syntax alone does not certify that arbitrary received coefficients form an honest permutation.

There are $n+\binom{n+2}{3}-n=\binom{n+2}{3}$ monomial slots per output. With $w(t)=\lceil t\log_2(3)/8\rceil$, the compact public width is $w(2n+n\binom{n+2}{3})$. The secret width is $w(2n^2+n)$, the ciphertext width is $w(n)$ and the derived key has 32 bytes. The external suite identifier uses ASCII `SG-DIFRA/R13/centered-affine-power/v1/` followed by $i,j$ as unsigned four-byte big-endian integers. The KEM frames this identifier, dimension and full compact public bytes in its KDF as specified in [Round 11](../round11/TRANSFORM.md). The two suites therefore derive separate keys despite representing the same permutation.

| Field degree | Dense public bytes | Centered public bytes | Public bytes saved | Private bytes | Ciphertext bytes |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | 25 | 18 | 7 | 8 | 1 |
| 82 | 1,603,272 | 1,548,004 | 55,268 | 2,681 | 17 |
| 122 | 7,677,285 | 7,495,956 | 181,329 | 5,922 | 25 |
| 163 | 24,171,671 | 23,740,067 | 431,604 | 10,561 | 33 |
| 164 | 24,764,906 | 24,325,325 | 439,581 | 10,690 | 33 |
| 244 | 119,928,669 | 118,483,795 | 1,444,874 | 23,639 | 49 |
| 325 | 375,211,457 | 371,800,509 | 3,410,948 | 41,918 | 65 |

The first row was serialized and exercised end to end. The larger rows are exact calculations for the format. They give no performance measurements or security ratings. Optimal public compression remains open even for this family.

## Direct compilation and verification

To compile from the secret, the implementation forms the three Frobenius powers of each input-mask column. For a term $z_iz_jz_k$, the coefficient is the sum of products for the distinct assignments of its indices to the three factors. A reduced linear slot collects the corresponding pure cube. The output mask’s linear part then gives the public coordinate coefficients. The sender subtracts $c$, evaluates these terms and adds $v$, using only the packed public bytes. For the differential witness relation, `compact_public_circuit` lowers these public translations and the centered polynomial into ordinary ternary arithmetic gates for the [Round 12 compiler](../round12/GENERATED_DIFFERENTIAL_REDUCTION.md).

The [four regressions](test_compact_orbit.py) test all 81 inputs of a masked dimension-four permutation against the dense backend and the compiled witness relation, and all 81 encapsulation choices with separate sender and receiver instances. They compare two distinct Frobenius-related normalized private presentations with identical public bytes. They also cover malformed widths and ranks, suite separation, and the six calculated profile sizes. From the repository root run

```sh
python3 -m unittest discover -s research-2028/round13 -p 'test_compact_orbit.py' -v
```
