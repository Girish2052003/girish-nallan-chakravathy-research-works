# One generated witness problem for the existing standalone KEM

The [Round 15 native KEM](../round15/NATIVE_PROOF.md) inherits two average-case distributions from Round 14. Its public checks use an iid ternary matrix with $d$ rows and $r$ columns and a signed vector of weight $w$. Its payload uses an iid $h$-by-$N$ generator matrix and noise of weight $z=w$. Here $N$ is the **original Round 14** payload length, before Round 15 projects its ciphertext. This note gives one sufficient sparse-witness assumption for the two existing games at each target. It changes only the security reduction. It gives no numerical estimate of the difficulty of the new assumption.

## Common source and theorem

Write $D=N-h$, $k=D-d$ and $n_*=r+k$. The three [published layouts](../round14/PARAMETERS.md) satisfy $0\le k\le r$, $n_*\le N$, and $D<n_*$. In the source experiment, draw $A$ uniformly in $\mathbb F_3^{D\times n_*}$. Choose $e$ independently with a uniform size-$w$ support and iid uniform signs in $\{1,2\}$. Give the solver $(A,y=Ae)$ and accept any weight-$w$ vector with syndrome $y$. The [Round 14 cubic encoding](../round14/WEIGHTED_DIFFERENCE.md) gives an equivalent generated fixed-challenge differential-witness problem. The matrix and planted vector are sampled independently of the recipient key and the KEM game.

| 192-target quantity | Value |
|---|---:|
| Key experiment $d,r$ | 14,426,208 rows; 21,612,672 columns |
| Payload experiment $h,N$ | 14,407,680 generator rows; 43,241,800 columns |
| Common source $D,n_*,w$ | 28,834,120 rows; 36,020,584 columns; weight 1,152 |
| Single-coordinate buckets $r-k$ | 7,204,760 |
| Two-coordinate buckets $k$ | 14,407,912 |
| Probability that the planted support hits distinct buckets | 0.9853834454, rounded |

Let $P_*$ bound the probability of finding an accepted source witness at resources covering the appropriate simulations. Let $\epsilon_1,\epsilon_2$ be the raw distinguishing gaps for the key and payload games respectively. Define
$$
p=\frac{[x^w](1+2x)^k(1+x)^{r-k}}{\binom{n_*}{w}},
\qquad \gamma=\prod_{j=0}^{k-1}(1-3^{j-D}).
$$
The bracket extracts the coefficient of $x^w$; the empty product equals one. Put $\rho_G=1-\prod_{j=0}^{h-1}(1-3^{j-N})$ and $\rho_H=1-\prod_{j=0}^{D-1}(1-3^{j-N})$. With the coherent decision circuits and auxiliary-oracle resources in the [Round 14 quantum search theorem](../round14/WITNESS_PROOF.md), the following bounds hold, clipped at one:
$$
\epsilon_1\le\frac32\sqrt{\frac{P_*}{p\gamma}},
\qquad
\epsilon_2\le \rho_G+\frac{1-\rho_G}{1-\rho_H}\frac32\sqrt{P_*}.
$$
These ideal-arithmetic bounds use exact sampling. Budget additional approximation and capped-sampler error when implementing the reductions with a finite gate set. At the 192 target the multiplicative factor on $\sqrt{P_*}$ in the key bound is about $1.5111$. The subsequent statistical corrections and FO security losses of the native KEM still apply.

## Why folding gives the key experiment

1. Partition the $n_*$ input positions into $r$ known buckets: $k$ pairs and $r-k$ singles. Mark one representative in each bucket. Call their original matrix columns $C_1,\dots,C_r$. For every pair, form a difference column equal to the second column minus its representative. Write $L$ for the $D\times k$ difference matrix. The transformation from $A$ to $(C,L)$ is invertible and linear. Therefore $C$ and $L$ are independent uniform matrices.
2. The simulator may abort upon $\operatorname{rank}L<k$, which is detectable from its input. Full column rank occurs with probability $\gamma$. On success, choose a full-row-rank $d\times D$ matrix $Q$ with kernel equal to the column span of $L$. Then $Q$ annihilates every difference, so both members of a pair have the same projected column. Conditional on $L$, $QC$ is an iid uniform $d\times r$ matrix. The sum $s_j$ of input error coefficients in bucket $j$, taken modulo three, satisfies $(QC)s=Qy$.
3. Choose an independent uniform permutation of the $r$ bucket labels and apply it to both the projected column order and the unknown folded vector. The simulator can permute the columns without knowing that vector. Conditional on **distinct occupied buckets**, it now presents exactly the key experiment's planted distribution: a uniform matrix and uniform signed weight-$w$ vector, independently. Random labels matter because a pair has twice as many positions as a single. The input signs are independent and remain uniform. The collision-free event has probability $p$ by counting selections of zero or one support position per bucket. It is independent of the rank event. The simulator need not detect it. A simple lower bound follows by a union bound, $p\ge 1-k w(w-1)/(n_*(n_*-1))$.
4. The quantum Fourier reduction in Round 14 recovers the *planted* vector in the exact key experiment with average probability at least $4\epsilon_1^2/9$. Undo the bucket label permutation on its output. Set each representative's tentative coefficient to the recovered bucket sum, with every pair's second coefficient initially zero. The remaining syndrome equals $L v$ for the vector of true second coefficients whenever the recovered sums are right. Solve this linear system and, in each pair, subtract $v_j$ from the representative and assign $v_j$ to the second position. Because $L$ has full column rank, the solution is unique on this event. Check the final weight and syndrome. This constructs a source solver with success at least $p\gamma\cdot4\epsilon_1^2/9$, which proves the first bound.

This argument uses a guarantee on recovery of the *original* folded vector. A generic promise that a target solver finds some preimage would require controlling collisions between different weight-$w$ vectors. The cited Fourier theorem supplies exactly the planted guarantee used here. On a support collision the simulator may still succeed, but the lower bound gives those runs zero credit. In particular $1-p$ is **not** added to the distinguishing advantage.

An alternative lift can use just the second columns of the occupied pairs. Even without aborting on a globally deficient $L$, choose any $d$ independent row functionals annihilating its image. The conditional distribution of the projected matrix is again iid. Given a collision-free planted support, at most $w$ pair-difference columns are relevant. The support is independent of $L$, so the unconditional probability of deficiency on this true subset is at most $(3^w-1)/(2\cdot3^D)$, by a union bound over scalar-equivalence classes of nonzero null vectors. Subtracting this bound from $p\cdot4\epsilon_1^2/9$ also gives a valid search-success lower bound. This subtraction does not assume independence of the Fourier solver's success and the deficient-subset event.

## Why padding gives the payload experiment

Append $N-n_*$ fresh independent $D$-dimensional columns to $A$, conceptually append the same number of zeros to $e$, randomly permute all $N$ coordinates, and retain $y$. The resulting parity-check matrix $H$ is iid and independent of the permuted error. The permuted support is a uniform $w$-subset of $N$ positions with iid signs. Thus the resulting **planted** syndrome instance has exactly the required iid parity-check law. Any algorithm recovering its planted error lets the simulator undo the permutation and read the first $n_*$ positions.

The payload distinguishing game uses a generator matrix. To transport a full-rank parity-check instance, sample a uniform ordered basis of its kernel and a uniform point in the affine fiber with the supplied syndrome. This produces a uniform full-rank generator and either a noisy codeword or a uniform word. Discarding rank-deficient iid parity-check inputs scales the full-rank signed gap by $1-\rho_H$. The iid generator can have deficiency with probability $\rho_G$. Applying the same planted-error Fourier theorem, together with the padding argument, yields the stated second inequality. [Detailed rank and sign accounting](../round14/WITNESS_PROOF.md)

## Resource and claim boundaries

The simulator handles the **full** source matrix. At the 192 target this is 1,038,621,841,526,080 trits. Ordinary dense elimination, basis construction and conversion are polynomial but costly. For example, classical field-operation overhead for folding and lifting can be bounded by $O(D^2 n_*)$ with $O(D n_*)$ working field elements in addition to the target solver's resources. For payload padding there are $D(N-n_*)$ fresh ternary entries, and conventional full-rank parity-check/generator conversion can cost $O(N^3)$ field operations and $O(N^2)$ field elements; the coherent Fourier theorem also requires running the relevant tester and its adjoint. Bounds on $P_*$ must hold at the actual composed time, memory and oracle counts.

There is a concrete obstruction to using this search reduction to certify the earlier 192-target budget. For a fixed set of $D$ source coordinates the probability that it contains the planted support is $\binom Dw/\binom{n_*}w$. The submatrix there independently has full rank with probability $\prod_{j=1}^D(1-3^{-j})>1/2$. On their intersection the planted witness is determined by an ordinary square linear system. Thus for resources covering one such solve, the source search-success maximum is at least half this containment probability. At the 192 parameters,
$$
-\log_2\left(\binom Dw/\binom{n_*}w\right)
=\sum_{i=0}^{w-1}\log_2\frac{n_*-i}{D-i}\approx369.850.
$$
The floor exceeds $2^{-371}$. For example, forcing the displayed bound on $\epsilon_1$ below $2^{-280}$ would require $P_*<(4/9)p\gamma\,2^{-560}$, already far below that floor. Even the earlier $2^{-224}$ sufficient condition cannot be obtained by forcing this square-root bound small at those resources. This is an obstruction to those particular proof estimates. It establishes neither a native KEM break nor a corresponding lower bound on either decision advantage.

The reduction direction is specific: a distinguisher for either old distribution gives a solver for this one source. Assuming the new source is hard is sufficient for the old KEM theorem. Hardness of either old game does not establish hardness of this new source. The source's 192-target row-to-column ratio is about 0.8005; the older key matrix has a ratio about 0.6675. These are different parameter regimes. No search work factor of $2^{191}$ follows from the success factors, matrix sizes, or formula for $p$. The argument applies to generated witnesses in this code-based native research line, and supplies no worst-case-to-average-case theorem for arbitrary SG-DIFRA potentials.
