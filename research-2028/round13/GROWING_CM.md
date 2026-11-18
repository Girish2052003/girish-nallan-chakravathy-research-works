# Varying the exponent in the masked Coulter–Matthews family

The Round 12 field construction hid a fixed degree-13 univariate difference under two affine masks. Allowing its exponent to grow gives genuinely different permutations and retains fast private decoding. We prove that the complete dense coefficient key still determines a polynomial-time public inverse, uniformly over the exponent and for every ciphertext. The complexity measure here is the actual encoded key length. The proof makes no estimate of the runtime of a practical implementation at a specific dimension.

## Normal form and private inversion

Let $K=\mathbb F_{3^n}$, let $Q=3^n$, and take a positive integer $k$ with $\gcd(k,2n)=1$. Set $E_j=(3^j+1)/2$, $D_j=(3^j-1)/2$. For a nonzero field element $a$, form $f_{k,a}(t)=(t+a)^{E_k}-t^{E_k}$. Secret affine bijections over $\mathbb F_3$ act on the input and output. Publish the resulting vector map as the list of reduced coordinate coefficients, including zeros, through its full degree.

Coulter and Matthews prove planarity under exactly the stated coprimality condition. Their proof gives $f_{k,1}(t)=-C_{D_k}(t-1)$, where the Dickson polynomial satisfies $C_d(u+u^{-1})=u^d+u^{-d}$. Since $\gcd(D_k,Q^2-1)=1$, set $b=D_k^{-1}\bmod(Q^2-1)$. The inverse at $y$ is

$$ f_{k,a}^{-1}(y)=a\left(1+C_b(-y/a^{E_k})\right). $$

The scaling follows by substituting $t/a$. The Dickson identity gives $C_b\circ C_{D_k}=\mathrm{id}$ on $K$, since the roots of $u^2-tu+1$ belong to $\mathbb F_{Q^2}^{\times}$. Private decoding undoes the outer mask, applies this inverse, and undoes the inner mask. The doubling recurrences evaluate $C_b$ in $O(n)$ field operations. [Coulter and Matthews, Theorem 4.1 and its proof](https://cpb-us-w2.wpmucdn.com/sites.udel.edu/dist/a/6463/files/2017/08/planar-1vircig.pdf)

Take $r=k\bmod 2n$ and $e=\min(r,2n-r)$, so $1\le e\le n$. Equality $e=n$ forces $n=1$ by coprimality. Exponents $E_k$ and $E_r$ agree modulo $Q-1$ because $(3^{2n}-1)/2$ is a multiple of $Q-1$. Both powers send zero to zero. Also $3^e E_{2n-e}-E_e=(3^{2n}-1)/2$. Consequently $f_{2n-e,a}(t)^{3^e}=f_{e,a}(t)$ as field functions. The output Frobenius is an invertible ternary linear map and can be absorbed into the existing mask. Thus $e$ is sufficient for the analysis even when $k$ is much larger than $n$. Private computation can likewise use the residue $r$.

## Exact public degree

**Lemma.** The normalized differential, with or without the affine masks, has maximum coordinate degree exactly $e$.

In the unique univariate representation of a field function with degree below $Q$, the maximum ternary digit sum of an exponent with nonzero coefficient equals its coordinate degree. To see this, view functions $K\to K$ as a vector space over $K$. A monomial $t^j$ with ternary digit sum $w$ is a product of $w$ Frobenius-linear forms. Thus every such power with digit sum at most $d$ is represented by a polynomial of total degree at most $d$ in the input trits. These powers are independent, as their ordinary degrees are distinct and below $Q$. The number of these powers equals the number of reduced coordinate monomials of degree at most $d$, by matching the $n$ ternary digits to their exponents. They therefore form a basis for exactly this subspace.

The digits of $E_e$ are a low digit 2 and $e-1$ ones. Its total weight is $e+1$. Taking a nonzero difference cancels the top input-coordinate degree and yields degree at most $e$. The leading univariate differential term is $E_e a t^{D_e}$, with nonzero coefficient in characteristic three. The $e$ ternary digits of $D_e$ are all ones. The preceding basis characterization gives the matching lower bound. Invertible affine input and output substitutions preserve maximum coordinate degree by applying their inverses.

## A public inverse for growing exponents

**Theorem.** Let $M(n,d)$ be the count of reduced ternary monomials of total degree at most $d$ in $n$ variables. For every generated key, there is a uniform deterministic inversion procedure with time polynomial in $nM(n,e)$, the number of trits in the dense public key. The polynomial exponent in this complexity statement is independent of $e$. The result includes all generated keys, all nonzero shifts and every input or output point.

**Proof.** Work in the algebra of ternary polynomial functions on $n$ coordinates, reducing by $z_i^3=z_i$. Let $V_j$ denote the span of reduced monomials of degree at most $j$. Set $B=6e$. Given a public point $c$, start a subspace $W\subseteq V_B$ with the public coordinate equations $F_i(z)-c_i$. Repeatedly add the reduced products $z_i h$ for $h$ in a basis of $W\cap V_{B-1}$ until the space stops growing. All resulting functions vanish at the true preimage. Repeated multiplication and linearity ensure that $ph\in W$ whenever $h\in W$ and the sum of their reduced degrees is at most $B$. A $K$-valued function belongs to this construction when each of its ternary coordinates is in $W$. The same product rule applies by bilinearity of field multiplication over the base field.

Use the secret affine form $L(z)$ only to prove which consequences occur in the public space. In the normalized basis let $U(t)=f_{e,a}(t)-y$, where $y$ is the output after undoing the outer mask. Its ordinary degree is $D=(3^e-1)/2$. The coordinates of $U(L)$ are linear combinations of the public equations. For any univariate polynomial of ordinary degree below $3^e$, substitution of $L$ yields a reduced function of degree at most $2e$. Indeed, any exponent in it has at most $e$ ternary digits and each power $L^{3^j}$ is affine as a function on ternary points.

Let $r_i$ be the remainder of $t^{3^i}$ modulo $U$. We show inductively that $p_i=L^{3^i}-r_i(L)$ belongs coordinatewise to $W$. If $D>1$ then $p_0=0$. When $D=1$, $t-r_0(t)$ is a constant multiple of $U$, which gives the same starting membership. Each $p_i$ has degree at most $2e$. Cubing it within the cutoff $6e$ is permitted. Also $r_i^3-r_{i+1}=H_i U$, with $H_i$ zero or of ordinary degree at most $2D-3<3^e$. Hence $H_i(L)U(L)$ belongs to $W$ within the same degree budget. Adding this relation to $p_i^3$ gives $p_{i+1}$ in characteristic three.

At step $n$, $L^{3^n}=L$. The monic gcd of $t-r_n$ and $U$ is $t-\xi$, where $\xi$ is the unique root of $U$ in $K$. This follows from $r_n\equiv t^{3^n}\pmod U$ and the simple roots of $t^{3^n}-t$. Bézout's identity now expresses $t-\xi$ as a sum of multiples of $U$ and $t-r_n$ with multiplier degrees at most $D$. This includes the case $t-r_n=0$, where the gcd itself is a scalar multiple of $U$. After substitution of $L$, each multiplier has degree at most $2e$, and the two factors already belong to $W$ with degree at most $2e$. This proves that every coordinate of $L-\xi$ is present. Its $n$ affine coordinate equations have independent linear parts because the secret input mask is invertible. The publicly computed subspace $W\cap V_1$ therefore determines the preimage by linear algebra.

The space $V_B$ has dimension $M(n,6e)\le M(n,e)^6$. For this inequality, split the sorted variables in any reduced monomial of degree at most $6e$ into six blocks of size at most $e$. Each block remains reduced, and multiplying the tuple recovers the starting monomial. The closure has at most $M(n,6e)$ strict dimension increases. Products by a single variable, echelon forms and intersections all use a polynomial number of operations in this dimension and $n$. This proves the claimed bound using the actual dense key representation. The sender's unique point is recovered for every honest output. A hashed-preimage KEM on this family consequently gives a passive probability gap of $1-2^{-b}$ for a $b$-bit shared key.

The reduced-function proof extends the fixed-degree reasoning in [Round 12](../round12/PLANAR_FAMILY.md). Related bounds in the HFE literature use univariate gcd calculations and Frobenius relations under Weil descent. Huang, Kosters, Yang and Yeo give such a bounded-degree gcd result in Proposition 4.3. No priority claim is made for the method. [Huang et al., 2015](https://arxiv.org/pdf/1505.02532)

## Wire sizes and scope

The exact coefficient count for one coordinate is

$$ M(n,e)=\sum_{j=0}^{\lfloor e/3\rfloor}(-1)^j\binom{n}{j}\binom{n+e-3j}{e-3j}. $$

This is inclusion–exclusion on the forbidden exponents of three or more. A vector of $h$ trits needs $\lceil h\log_2(3)/8\rceil$ bytes. In the following table $e=5$, each $n$ is compatible with planarity, and each field size is at least the indicated domain target.

| Domain target | $n$ | Trit coefficients $nM(n,5)$ | Dense public key bytes | Ciphertext bytes |
| ---: | ---: | ---: | ---: | ---: |
| $2^{128}$ | 81 | 2,798,603,379 | 554,460,177 | 17 |
| $2^{192}$ | 122 | 30,902,771,166 | 6,122,466,684 | 25 |
| $2^{256}$ | 162 | 164,721,340,962 | 32,634,643,562 | 33 |

These are exact counts for the declared layout. We did not materialize those public keys. For growing $e$ the dense length becomes superpolynomial along any subsequence where $e\to\infty$ as $n\to\infty$, since for every fixed $d\le e$, $M(n,e)\ge\binom nd$. A different compact representation has its own security and efficiency questions. The theorem concerns a key containing the full reduced coefficients, and does not rule out unrelated SG-DIFRA maps or provide attack timings at these dimensions. [Finite checks](test_cm_extent.py)
