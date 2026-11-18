# A planar differential with exact private inversion and a public polynomial-time bound

Fix a basis of the finite field $K=\mathbb F_{3^n}$ over $k=\mathbb F_3$. A classical planar monomial gives a natural candidate for an SG-DIFRA trapdoor. Its private decoder succeeds on every input, yet the same family admits polynomial-time public inversion. This is a control case for evaluating proposed trapdoors. The negative theorem concerns the family defined here.

## The differential and its private inverse

**Proposition 1.** For $3\nmid n$ and $a\in K^\times$, the function

$$
D_a(X)=(X+a)^{14}-X^{14}
$$

permutes $K$. Given two affine $k$-bijections $S:k^n\to K$ and $T:K\to k^n$, the map $F(z)=T(D_a(S(z)))$ also permutes $k^n$. These claims hold for every choice of the masks.

**Proof.** Coulter and Matthews, Theorem 4.1, prove that $X^{(3^j+1)/2}$ is planar on $\mathbb F_{3^n}$ precisely when $j$ is odd and $\gcd(j,n)=1$. By definition, planarity gives a permutation for each nonzero difference direction. Set $j=3$ and compose with the two bijections. [Coulter and Matthews, original proof](https://cpb-us-w2.wpmucdn.com/sites.udel.edu/dist/a/6463/files/2017/08/planar-1vircig.pdf)

For a ciphertext $c$, set $y=T^{-1}(c)$ and $U(X)=D_a(X)-y$. Its ordinary univariate degree is 13 since the leading coefficient is $14a\ne0$. The monic gcd

$$
\gcd(U(X),X^{3^n}-X)=X-\xi
$$

recovers its unique $K$-root, even if $U$ has repeated roots or further roots in an extension. Indeed, $X^{3^n}-X$ has each element of $K$ as a simple root. Computing its remainder uses $n$ cubings modulo a degree-13 polynomial. The private inverse is $S^{-1}(\xi)$.

The original planarity proof also identifies $D_1(X)=-C_{13}(X-1)$ for the Dickson polynomial with parameter one, characterized by $C_j(u+u^{-1})=u^j+u^{-j}$. Here $\gcd(13,3^{2n}-1)=1$ since 3 has order 3 modulo 13 and $3\nmid n$. If $m$ is a positive inverse of 13 modulo $3^{2n}-1$, then $D_a^{-1}(y)=a(1+C_m(-y/a^{14}))$. For each $x\in K$, the two roots of $u^2-xu+1$ belong to $\mathbb F_{3^{2n}}^\times$, so $C_{13m}(x)=x$. This justifies the formula without any assumption about the coordinate degree of the inverse. The scaling identity $D_a(X)=a^{14}D_1(X/a)$ allows both scalar factors to be absorbed into the masks. All these keys lie in one affine equivalence class.

## Size of the public map

In the chosen basis, $X^{14}=X^9X^3X^2$ has coordinate degree at most four, since $X\mapsto X^3$ and $X\mapsto X^9$ are $k$-linear. Taking a finite difference cancels its terms of degree four. Thus the explicit public map has coordinate degree at most three, including after affine masking and reduction by $z_j^3=z_j$. Publishing all canonical coefficients requires $n(\binom{n+3}{3}-n)$ trits. This counts monomials of total degree at most three after removing the $n$ pure cubes. A point ciphertext requires $\lceil n\log_2(3)/8\rceil$ bytes with single-integer base-three packing. For example, $n=122$ gives a 25-byte point and **7,677,285 bytes** for the densely packed coefficient vector, excluding framing. These are representation sizes, not security estimates.

## Why exact private decoding still fails to give one-wayness

**Theorem 2.** Suppose a public map has the form $T\circ f\circ S$ with the affine $k$-bijections above, and the public key gives the reduced coordinate polynomials. Suppose $f\in K[X]$ has ordinary degree $d\ge2$ bounded independently of $n$. On any output having exactly one preimage under the map, the preimage is deterministically computable in polynomial time in $n$, with the degree bound fixed. In particular, the planar family of Proposition 1 is publicly invertible for every ciphertext and every key.

**A bounded-degree proof.** For the planar family take $d=13$ and the degree cutoff $B=36$. The general argument uses $B=\max\{d,3(d-1),2d\}$. Start with the coordinates of $F(z)-c$ and the equations $z_j^3-z_j$. Consider the smallest $k$-vector space $V$ of polynomials of degree at most $B$ containing those equations and closed under multiplication whenever the product stays within that degree. This space is obtained by ordinary linear algebra on at most $M=\binom{n+B}{B}$ monomials. Specifically, repeatedly span $V$ together with the products $z_j(V\cap k[z]_{\le B-1})$ until the dimension stops increasing. At most $M$ strict dimension increases are possible. Sequential multiplications by variables then realize multiplication by any polynomial within the degree cap. Every member of $V$ vanishes on every solution.

Write $L(z)=S(z)$ as a $K$-valued affine form in the visible variables and set $U(X)=f(X)-T^{-1}(c)$. In the following, membership of a $K$-valued polynomial means that **all** its $k$-coordinate polynomials lie in $V$. This convention allows arbitrary $K$-linear combinations and multiplication by $K$-valued polynomials within the degree cap, because field multiplication is bilinear over $k$. If $p$ has total degree $e$, each coordinate of $p$ has degree at most $e$.

The coordinatewise reduction of $U(L)$ is the $k$-linear inverse of the output mask's linear part applied to the public $F(z)-c$. Its coordinates belong to $V$. Before reduction $U(L)$ has total degree at most $d$. Each step replacing a monomial containing $z_j^3$ by the corresponding monomial containing $z_j$ changes it by a multiple of a field equation of degree at most $d$. Therefore the coordinates of the full $U(L)$ also belong to $V$.

Let $r_i(X)$ be the remainder of $X^{3^i}$ modulo $U$, of degree at most $d-1$. Let $L_i(z)$ be the affine form obtained by raising each coefficient of $L$ to $3^i$ and leaving the variables unchanged. On trit points this form evaluates to $L(z)^{3^i}$. We show inductively that the coordinates of $L_i-r_i(L)$ belong to $V$. For $i=0$ this is the zero polynomial. Cubing the previous relation is permitted within degree $3(d-1)$. Also, $L_i^3-L_{i+1}$ is a $K$-linear combination of the $z_j^3-z_j$. Finally,

$$
r_i(X)^3-r_{i+1}(X)=H_i(X)U(X)
$$

is a polynomial identity of degree at most $3(d-1)$. Multiplying the previously derived $U(L)$ by $H_i(L)$ is within the same bound. Combining these three identities proves the induction.

At $i=n$ we have $L_n=L$. Since $r_n\equiv X^{3^n}\pmod U$ and there is precisely one field root $\xi$, the monic gcd of $U$ and $X-r_n$ is $X-\xi$. The univariate Bézout identity expresses this gcd as a sum of multiples of $U$ and $X-r_n$, each of degree at most $2d$. Substitution of $L$ gives $L-\xi$ coordinatewise in $V$. The $n$ coordinates of $L-\xi$ are affine equations with independent linear parts, since $S$ is a bijection. Thus the public linear consequences in $V$ determine the unique preimage. The hidden coordinates served only to prove that these consequences exist in the public space. This argument gives an asymptotic upper bound and supplies no estimate of actual cost at $n=122$.

**Relation to prior work.** Huang, Kosters, Yang and Yeo already prove an extension-degree-independent last fall degree bound for a descended univariate system with its field equations. In Theorem 4.5 of their preprint take the singleton $\{U\}$ of degree 13, $q=3$, $d=13$. Their $\tau(26,3,1)=\lfloor4(\log_3(13)+1)\rfloor=13$ meets the degree hypothesis. Proposition 2.6 handles changes of basis of the equations and affine variable substitutions. With trit field equations, replacing an initially cubic coordinate by its reduced form changes only scalar multiples of the field equations. Proposition 2.8 relates the bound to solving the radical descended system, which here has one solution. The elementary cutoff 36 above gives a direct family-specific proof. This application follows the established work on hidden field equations. [Huang, Kosters, Yang and Yeo, Theorem 4.5, Propositions 2.6 and 2.8, and Section 5](https://arxiv.org/pdf/1505.02532)

## Consequence for encapsulation

For a KEM that sends $c=F(z)$ and derives a $b$-bit session key as a publicly computable $H(pk,c,z)$, Theorem 2 recovers the required input on every honest ciphertext. Comparing the recomputed key with the challenge key gives distinguishing gap $1-2^{-b}$ in the real-vs-uniform definition, already without decapsulation queries. Ciphertext checks computed from the same recoverable $z$ do not change this conclusion. Private inversion and correctness are unconditional. Worst-case hardness of a separate universal-differential language supplies no lower bound for this sampled one-preimage problem.
