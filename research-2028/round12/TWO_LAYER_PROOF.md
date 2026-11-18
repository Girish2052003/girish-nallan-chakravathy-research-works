# Degree filtration decides both modes and recovers the input in permutation mode

Let $K=\mathbb F_3$, let $x\in K^n$ and let

$$
 Z=Ax+a,\qquad H=T_1(Z),\qquad Y=MH+d,\qquad F(x)=BT_2(Y)+b .
$$

The matrices $A,B$ are invertible. Each $T_i$ has a (secret) triangular presentation whose $j$th output is the $j$th input plus a polynomial of degree at most two in earlier inputs. In the implementation these polynomials are homogeneous, but the argument also permits constants and linear terms. Index the coordinates from zero. The key provides the reduced degree-at-most-four coordinate functions of $F$ in the public input coordinates. The following proof uses only those functions. It does not need the hidden coordinate ordering, coefficients or affine transformations.

**Theorem.** For every generated permutation-mode key ($M$ invertible), every $F(x)$ determines $x$ by a public deterministic computation of polynomial cost in the explicit description length. For every loss-mode key with $\operatorname{rank}(M)=r<n$, a public deterministic polynomial-time test distinguishes it from every permutation-mode key with zero error. Together these facts refute both average-case one-wayness and key-mode indistinguishability for this construction, for any distribution of masks satisfying the stated hypotheses.

## Finite-field function arithmetic

Use the algebra $\mathcal A=K[X_1,\ldots,X_n]/(X_1^3-X_1,\ldots,X_n^3-X_n)$. Every function on $K^n$ has a unique representative with individual exponents at most two. Uniqueness follows by applying the univariate fact that a degree-at-most-two polynomial vanishing at all three field points is zero, one variable at a time; equality of finite cardinalities then gives existence. Let $V_j$ be the vector subspace whose reduced representatives have total degree at most $j$. Reduction by the defining relations never increases degree. Thus products of two elements of $V_2$ belong to $V_4$. In particular $\dim V_1=n+1$, $\dim V_2=\binom{n+2}2$ and $\dim V_4=\binom{n+4}4-n(n+1)$. No exponential truth table is required for arithmetic at these degree bounds.

A coordinate function $g\in\mathcal A$ will be **known from the ciphertext** when the computation has a formula, using the public output coordinates, that satisfies $g(x)=\widehat g(F(x))$ for every $x$. Such formulas can be stored as arithmetic circuits, sharing earlier intermediate computations. Constants and each $F_i$ have this property. Linear combinations and products preserve it. In particular it is possible to retain a publicly evaluable expression while taking the basis of an intersection with $V_j$: form the candidate functions' reduced coefficient vectors, find the nullspace for coefficients of degrees greater than $j$, and take an independent basis of the resulting polynomials. Keep the corresponding linear-combination coefficients at both steps. Every operation is ordinary finite-field linear algebra.

## First intersection, recovering middle coordinates

Start with $W=\langle 1\rangle\subseteq V_2$. Replace $W$ repeatedly by

$$
 \left(\operatorname{span}(1,F_1,\ldots,F_n)+W+
             \operatorname{span}\{uv:u,v\in W\}\right)\cap V_2 .
$$

A basis of $W$ suffices for enumerating products by bilinearity. Each space contains the preceding one. At most $\dim V_2-1$ strict increases occur. Stop when the space no longer grows. Every function in the final space is known from the ciphertext by the preceding construction.

We claim $Y_j\in W$ for each $j$. The public algorithm need not identify it by name. First, $T_{2,j}(Y)$ lies in the original span of $1,F_1,\ldots,F_n$, because $B$ is invertible. Second, $Y_j$ has degree at most two in $x$ by its defining expression $MT_1(Ax+a)+d$. For $j=0$ the outer triangular correction is constant. Inductively, suppose $Y_i\in W$ for every $i<j$. The correction in the $j$th outer shear is a linear combination of $1$, elements of $W$, and products of elements of $W$. Subtract it from $T_{2,j}(Y)$. The result is $Y_j$, and its degree at most two puts it inside the intersection defining the fixed point. This proves the claim without knowing the shear. In permutation mode, $M^{-1}(Y-d)=H$. Therefore $H_j\in W$ for every $j$ in that mode.

## Second intersection, recovering the public input

Keep this final $W$ fixed. Start $U=\langle1\rangle\subseteq V_1$. Replace it by

$$
 \left(W+U+\operatorname{span}\{uv:u,v\in U\}\right)\cap V_1
$$

until the dimension stabilizes. The degree before intersection is now at most two. At most $n$ strict increases are possible. Again the algorithm stores an expression in the public output for every resulting basis element.

In permutation mode $H_j=T_{1,j}(Z)$ lies in $W$. Because $Z_j$ has degree at most one in the public input, the same triangular induction puts every $Z_j$ in $U$. The constants and $Z_0,\ldots,Z_{n-1}$ span $V_1$ since $A$ is invertible. Thus $U=V_1$. Solve once for the coefficients of each public input coordinate $X_i$ in the obtained basis. At any received $y=F(x)$, evaluating those basis circuits and linear combinations returns $x$ exactly. All permutation-mode outputs are valid and possess one preimage.

In loss mode, every element of $U$ is still known from $F$. Write $\dim U=1+u$, and choose $u$ affine forms independent modulo constants. Their linear parts have rank $u$, so together they take exactly $3^u$ values as $x$ varies. Their joint outputs factor through $F(x)$, whose image has exactly $3^r$ elements, since the other layers are bijections. This gives $u\le r<n$. In particular the test "does $\dim U=n+1$?" separates the two modes perfectly. This does not assert that $u=r$ on loss-mode keys.

## Cost and cryptographic consequence

Calculations in the first iteration family use at most $O(n^4)$ candidate basis products per round, represented in a coefficient space of dimension $O(n^4)$. Each round uses polynomially many field operations, and the number of rounds is $O(n^2)$. The second iteration family is smaller. Deduplicating and expressing bases takes polynomial space and time. Each newly recorded linear combination or product can reference previously built expression nodes. Consequently total arithmetic circuit size, offline computation and online evaluation all remain polynomial in the explicit input size. This is an asymptotic bound, not a gate count or a practical timing guarantee for multi-gigabyte keys.

For a hashed-permutation KEM that derives $\kappa$ shared-key bits from the unique preimage and public context, exact recovery gives a passive real-versus-random distinguishing gap of $1-2^{-\kappa}$. Correctly computing the true shared key wins the comparison with probability one in the real game and $2^{-\kappa}$ in the random game. Thus the actual two-layer backend fails IND-CPA and IND-CCA. The abstract lossy-function theorem may hold under indistinguishability for other families, but this pair of samplers cannot instantiate it. This argument is specific to the given triangular structure, access to explicit reduced functions, and the fixed degree bounds. No general impossibility result for differential KEMs follows.

## Extension to any fixed number of triangular layers

**Theorem.** Fix an integer $L\ge1$. Let $A_0,\ldots,A_L$ be affine maps on $K^n$, and let $T_1,\ldots,T_L$ each be a triangular map of the type above, possibly using a different secret ordering at each layer. Publish all $n$ reduced coordinate polynomials of

$$
 F=A_L\circ T_L\circ A_{L-1}\circ\cdots\circ A_1\circ T_1\circ A_0.
$$

If all the affine maps are invertible then a deterministic public algorithm computes an arithmetic circuit for $F^{-1}$. It uses polynomial time in $n$ and the explicit coefficient description length for each fixed $L$. If any affine map has linear rank $r<n$, the same algorithm detects the resulting loss with zero error. The inputs to the algorithm are $n$, the public depth bound $L$, and explicit reduced coefficient vectors (or monomials with coefficients) in the public input variables. It requires all output coordinates. No intermediate maps or orderings are supplied.

**Proof.** Let $Z_1=A_0(x)$ and $Z_{i+1}=A_i(T_i(Z_i))$ for $1\le i\le L$, so $Z_{L+1}=F(x)$. The hidden vector entering $T_i$ has reduced degree at most $2^{i-1}$ componentwise. Begin with $S_{L+1}=\operatorname{span}(1,F_1,\ldots,F_n)$. For $i=L,L-1,\ldots,1$, set $d_i=2^{i-1}$. Starting from $U=\langle1\rangle$, iterate

$$
 U\ \leftarrow\ \big(S_{i+1}+U+\operatorname{span}\{uv:u,v\in U\}\big)\cap V_{d_i}
$$

until the space stabilizes, and call the result $S_i$. All basis elements remain publicly expressible in $F$ as above, including when some affine map is singular.

In permutation mode, use descending induction on $i$. By construction or the preceding stage, $S_{i+1}$ contains the coordinates of $Z_{i+1}$. Together with the constant they span the coordinates of $A_i^{-1}(Z_{i+1})=T_i(Z_i)$. With these available, apply the triangular induction in the secret ordering of $T_i$: each subtractable correction uses only constants, earlier coordinates of $Z_i$, and their pairwise products. The resulting coordinate belongs to $V_{d_i}$ by the degree bound above. At the fixed point every coordinate of $Z_i$ therefore belongs to $S_i$. Finally $S_1$ contains the coordinates of $A_0(x)$ and the constant, so $S_1=V_1$. Express the public input coordinates in its basis to obtain the inverse circuit.

If an affine map in the composition has rank $r$, the final image contains at most $3^r$ points, even if other affine maps are singular as well. The affine forms in $S_1$ factor through this image. As in the two-layer case, $\dim S_1\le r+1<n+1$, so the dimension test is exact. Each stage has at most $\dim V_{d_i}$ strict increases, and uses reduced coordinate vectors of degree at most $2d_i\le 2^L$. The dimensions of these spaces and the numbers of basis products are polynomial in $n$ for fixed $L$. The circuit with shared intermediate values has polynomial size by the same accounting. The exponent in this bound may depend on $L$. This theorem supplies no uniform polynomial-in-$n$ bound for growing depth with a succinct public representation.

## Relation to established multivariate cryptography

The two-round composition of three affine maps and two quadratic layers predates this note. Faugère and Perret describe the 2R layout, including triangular layers among the design choices, and study functional decomposition in the 2R-minus setting. Antoine Scemama uses relinearization for key recovery against the Double-Round Quadratic cryptosystem and explicitly states an independence heuristic for his linearized equations. Nie, Jiang, Hu and Ding use iterated linearization against two instances of the triangular TTM cryptosystem. These are precedents for both the architecture and the use of linear algebra in its analysis. [Faugère and Perret, CRYPTO 2006](https://www.iacr.org/archive/crypto2006/41170356/41170356.pdf) · [Scemama, ICISC 2007](https://doi.org/10.1007/978-3-540-76788-6_3) · [Nie et al., research paper](https://archive.ymsc.tsinghua.edu.cn/pacm_download/672/12600-dingjt12.pdf).

The theorem here uses the triangular identity at every layer to prove a degree-space inclusion for every generated key. Its outputs are an inverse circuit and a dimension test for the specified rank-loss modes. The proof does not recover any particular secret decomposition. These statements identify what the argument establishes for this family. Priority for the result or the method remains unverified.
