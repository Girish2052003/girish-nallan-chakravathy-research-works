# From generated inversion to every key and ciphertext in a masked-monomial orbit

Fix a public extension basis for $K=\mathbb F_{3^n}$, $N=3^n$, and a known positive odd exponent $e$ with $\gcd(e,N-1)=1$. The map $E(x)=x^e$ permutes $K$. The public key represents the ternary coordinate functions of $F=T\circ E\circ S$, with $S,T$ **independent, exactly uniform affine bijections** of the $n$-dimensional ternary vector space. The secret key stores a presentation $(S,T)$. All public encodings in this experiment canonically represent the function. Distinct presentations of the same function must give the same public bytes. The suite, field basis, degree layout, and exponent are fixed public parameters.

This defines a different key distribution from Round 12's SHAKE-expanded private seeds. The theorem also differs from the Coulter–Matthews construction, whose central map is a *difference* of monomials. Here the central map is the monomial itself. The compiled cubic differential problem uses the [Round 12 witness bijection](../round12/GENERATED_DIFFERENTIAL_REDUCTION.md).

**Theorem.** Suppose an algorithm given an honestly sampled public key and a uniform output $c\in K$ computes $F^{-1}(c)$ with probability $p$. There is a randomized algorithm that, for **each** public function in this affine orbit and **each** $c\in K$, computes the preimage with probability at least

$$p_* = \max\left(0,\frac{Np-1}{N-1}\right).$$

It uses at most two calls to the given algorithm, polynomial-time operations on the specified dense key encoding, and no secret key. The average includes key generation as well as the target. The theorem also applies to a quantum algorithm with classical input and output and the independent ideal-oracle resource of Round 11.

## Generating a fresh presentation

Write $M_\lambda(x)=\lambda x$ for $\lambda\in K^\times$. This is a ternary-linear isomorphism. The monomial satisfies

$$E\circ M_\lambda=M_{\lambda^e}\circ E.$$

Fix any one presentation $F=T E S$ of the challenge key for the *analysis*. The reduction does not need this presentation. Call the target regular for this presentation if $w=T^{-1}(c)$ is nonzero. Sample independent uniform affine bijections $A,B$, form the canonical public representation of $F'=B F A$, and send the inverter $(F',c'=B(c))$. An inverse answer $x'$ yields the original answer $A(x')$, which can be checked by evaluating $F$. The pair $(S'=S A,T'=B T)$ is distributed as independent fresh affine masks. In hidden coordinates, $c'=T'(w)$.

To see the precise joint law on a regular target, introduce a uniform auxiliary $\lambda\in K^\times$ for the proof. The pair

$$(S'',T'')=(M_\lambda S',\;T'M_{\lambda^{-e}})$$

has exactly the fresh product distribution even conditional on $\lambda$, since left or right multiplication by a fixed bijection permutes the finite affine group. It is therefore independent of $\lambda$. The public function remains $T'' E S''=T' E S'=F'$. The public target is $c'=T''(\lambda^e w)$. For nonzero $w$ the element $\lambda^ew$ is uniform in $K^\times$ and independent of $(S'',T'')$. Consequently the remasked public pair has precisely the law of a fresh key and a fresh output drawn uniformly **among the $N-1$ noncentral outputs of its sampled presentation**. This is a distribution on public pairs defined by a sampling experiment. The reduction never has to decide whether a public function has several presentations with different centers.

Let $p_{\rm reg}$ be the inverter's success in this regular experiment and $p_0$ its success on the output $T(0)$ of a fresh presentation. An independent uniform target lies at the sampled center with probability $1/N$. Thus

$$p=(1-1/N)p_{\rm reg}+p_0/N,\qquad p_{\rm reg}\ge p_*.$$

The first remasking method attains success $p_{\rm reg}$ on every regular promised input. The randomization also shows uniformity of the induced distribution over the orbit as *functions*, since each orbit element has the same number of presentations. Uniform output sampling is equivalent to honest encapsulation's uniform preimage sampling because $F$ is a permutation.

## The remaining output at the center

For the same fixed presentation put $x_0=S^{-1}(0)$ and $c_0=T(0)$. Oddness of $E$ and affineness of the masks give the exact reflection identity

$$F(2x_0-z)=2c_0-F(z)\quad\text{for every }z\in K.$$

On any input, choose a known $z$ satisfying $F(z)\ne c$ by trying two distinct points. Form the second target $u=2c-F(z)$. Run the regular remasking method on $u$, unmask the answer $x_u$ and test whether $(z+x_u)/2$ is a preimage of the original $c$. The division is ternary field division by two. If $c=c_0$, then $u\ne c_0$ is regular, $x_u=2x_0-z$, and the tested candidate is precisely $x_0$. If $c\ne c_0$, the first method already has the claimed success. Use fresh masks and inverter randomness for both calls, return any candidate passing the original equation, and declare failure if neither passes. Equivalently, always perform both independently and verify both results. An erroneous candidate cannot pass for any input other than the unique preimage. This proves the pointwise bound also when the center is not identifiable publicly.

## Computation and security consequence

Exactly uniform affine masks can be sampled in expected polynomial time by sampling a uniform ternary matrix until it is invertible and adding an independent uniform offset. The probability of invertibility is $\prod_{i=1}^n(1-3^{-i})$ and stays above $1/2$ by the union/product bound $\prod(1-x_i)\ge 1-\sum x_i$ at finite $n$. A bounded-time version must account for its rejection tail. Keeping the whole affine description in the *public* key would invalidate the distributional premise. The receiver inverts privately by applying $T^{-1}$, powering by the inverse of $e$ modulo $N-1$, then applying $S^{-1}$. An inverse exponent is chosen positive to treat zero correctly.

For the complexity claim use a full dense reduced coefficient list up to a public total degree bound $d\le 2n$. If $M$ monomials are admitted, the vector key contains $nM$ ternary coefficients. An invertible affine input substitution cannot increase total degree. Each stored monomial can be expanded by at most $d$ multiplications by affine forms, reducing $X_i^3=X_i$ after each multiplication. All intermediate degrees in such a product are bounded by the number of factors used, at most $d$. The destination coefficient list and the linear output transformation therefore cost polynomial time in $nM$. Key generation can also interpolate from the public lower set of $M$ ternary points at degree $d$ using the triangular multivariate Newton basis, evaluating the secret presentation at each point. For the compact cubic encoding in this round, the center pair transforms to $(A^{-1}(c_{in}),B(c_{out}))$ and the centered odd cubic undergoes only the linear parts of the two masks. Hence the public compact key can also be remasked canonically in polynomial time, as detailed in [the compact public encoding](COMPACT_PUBLIC.md). General compressed encodings may have different costs. For an auxiliary ideal random function, masks, inputs and the fixed public function are sampled independently of that function. Each inverter call has the stated marginal success in the same oracle experiment. Verification makes independence between the two success events unnecessary.

Compose this randomization with the conditional [Round 11 KEM transform](../round11/TRANSFORM.md) and the [Round 12 cubic compiler](../round12/GENERATED_DIFFERENTIAL_REDUCTION.md). For a one-stage classical ideal-hash KEM distinguisher with raw gap $\Delta$, take $p\ge\Delta$ in the displayed bound. For the stated quantum random-oracle game with $q_H\ge1$ public hash queries, an independent auxiliary ideal oracle, and classical decapsulation queries, take $p\ge\Delta^2/(4q_H^2)$. Each verified preimage lifts by forward circuit evaluation to the unique witness for the original compiled cubic potential and requested target. This gives a **promised worst-case** consequence for every canonically encoded key in this orbit at a fixed dimension and exponent. Reading the embedded public tag suffices when the supplied input is its canonical compiled differential instance. The theorem gives no conversion from an arbitrary cubic potential, arbitrary permutation, or arbitrary globally quantified Round 10 instance into this orbit.

As a numerical illustration of the probability statement, if $p=1/2$ on generated keys then every promised input has success at least $(N-2)/(2(N-1))$ with at most two calls. The result transfers existing hardness **if** the promised orbit is hard. Highly structured examples can have publicly efficient inverses on every input and still satisfy the theorem. No concrete post-quantum hardness rating or originality of random self-reduction follows. Random self-reduction is an established method for relating distributions on instances to worst-case problems. [Feigenbaum and Fortnow](https://doi.org/10.1137/0222061)


The quantitative statement is per dimension. To infer negligible distinguishing advantage for an asymptotic family from worst-case hardness, the hardness premise must cover the same lengths as the claimed security guarantee. A solver with noticeable average success at infinitely many lengths gives a pointwise solver on those lengths. It need not work at all other lengths. No separation of complexity classes or concrete attack lower bound is assumed to follow from the reduction.
