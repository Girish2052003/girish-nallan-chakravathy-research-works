# What can be proved about the two generated decoding problems?

The two finite experiments below admit unconditional lower bounds when we count how much of the challenge an observer reads. For the 192 target, give the observer the complete public matrix and unlimited computation on that matrix. With at most **547 quantum coordinate queries to the syndrome**, its raw distinguishing advantage is at most $2^{-280}$. For the noisy-codeword experiment, the corresponding guarantee extends to **1,629,420 quantum coordinate queries**. In a complementary classical model the observer gets the entire syndrome first. Even **18,261,799 adaptive requests for whole matrix columns** give raw advantage at most $2^{-280}$ in the key experiment.

A coordinate query below returns one ternary symbol at an address that may be in quantum superposition. A column request returns one column at a classical address. The real KEM supplies its full encoded inputs. Reading all challenge trits costs at most the challenge length in the coordinate-query model. These bounds therefore address limited observations; establishing the target work factor for algorithms using the full representation remains open.

## The two distributions

Use the [Round 14 generated instances](../round14/BASE_PROOF.md). In the key experiment $B$ is an iid uniform $d\times r$ ternary matrix, $S$ is uniform among all $W=2^w\binom rw$ signed weight-$w$ vectors, and the challenge is $Y=BS$ or independent uniform $Y$. In the payload experiment $G$ is an iid uniform $h\times N$ matrix and the challenge is $Y=G^\top u+E$ or uniform. Here $u$ is uniformly random in the ternary $h$-dimensional space and $E$ is an independent signed weight-$z$ error. Raw advantage is the absolute difference between acceptance probabilities. Probabilities average over all public matrices and generator coins. In the quantum whole-matrix experiment, auxiliary information may depend on the public matrix, independently of the hidden challenge given that matrix. In the classical column experiment, all initial advice and preprocessing must be independent of the unopened matrix; the specified syndrome and requested columns are the only instance-dependent data available.

## Quantum observers with the whole matrix

Put $M(n,D)=\sum_{j=1}^{\min(n,D)}2^j\binom nj$. Write $q$ for the number of quantum queries to $O_Y|i,b\rangle=|i,b+Y_i\bmod3\rangle$ or its inverse.

**Theorem.** In the key experiment the raw advantage is at most $\min(1,\tfrac12\sqrt{M(d,2q)/W})$. In the payload experiment it is at most $\min(1,M(N,2q)/3^h)$. Matrix-dependent preprocessing and computation between queries can be unlimited.

**Proof.** Fix the public matrix. Put $\omega=\exp(2\pi i/3)$ and use characters $\chi_a(y)=\omega^{a^\top y}$ on challenge words. After at most $q$ queries, every final amplitude is a sum of characters whose frequency vectors have at most $q$ nonzero coordinates. Indeed the target register in the ternary Fourier basis gains a phase depending on a single queried trit. Multiplying by that phase increases the support size by at most one. Query-independent unitaries take linear combinations and preserve the bound. Squaring amplitudes and summing them gives an acceptance function $f(y)$ supported on frequencies of weight at most $2q$. Classical randomness and intermediate measurements are covered by mixing or purification. This is the polynomial method for quantum queries specialized to ternary symbols. [Beals, Buhrman, Cleve, Mosca and de Wolf, *Quantum Lower Bounds by Polynomials*](https://arxiv.org/abs/quant-ph/9802049)

Write $\widehat f(a)=\mathbb E_{y\,\text{uniform}}f(y)\overline{\chi_a(y)}$ and let $b_B(a)=\mathbb E_S\chi_a(BS)$. The constant Fourier term cancels in the difference of the two acceptance probabilities. Parseval gives $\sum_{a\ne0}|\widehat f(a)|^2=\operatorname{Var}(f)\le1/4$ since $0\le f\le1$. Cauchy–Schwarz bounds the conditional gap by half the square root of $\sum_{0<\operatorname{wt}(a)\le2q}|b_B(a)|^2$. For any nonzero fixed $a$, the vector $B^\top a$ is uniform over $\mathbb F_3^r$. Orthogonality gives

$$
\mathbb E_B |b_B(a)|^2
=\mathbb E_{S,S'}\mathbb E_B\,\omega^{a^\top B(S-S')}
=\Pr[S=S']=1/W.
$$

Here $S,S'$ are independent and uniform over the signed supports. Jensen's inequality and the triangle inequality bound the raw average gap by the stated square root. The acceptance function may depend on the whole matrix because the conditional variance bound holds separately for each matrix.

For the payload, the character mean vanishes whenever $G a\ne0$, since the independent uniform $u$ then has zero character mean in direction $G a$. If all nonzero $a$ of weight at most $2q$ satisfy $G a\ne0$, every observable low-weight character mean agrees exactly with uniform. This holds regardless of the noise distribution provided the noise is independent of $u$ for fixed $G$. For each fixed $a\ne0$, the probability $G a=0$ is $3^{-h}$. A union bound over the allowed frequencies bounds the probability of an exceptional matrix by $M(N,2q)3^{-h}$. Even on exceptional matrices a raw gap is at most one. This proves the second assertion.

## Classical observers with the whole syndrome

Alternatively, give an observer $Y$ for free and let it request at most $v$ distinct columns of $B$, in any adaptive order. Its advantage in the key experiment is at most $\binom vw/\binom rw$, with zero numerator for $v<w$.

**Proof.** The planted syndrome is uniform for each fixed signed support. Sample a uniform syndrome and a hidden signed support independently. The real matrix then has the uniform matrix law conditioned on $BS=Y$. Any requested sequence of columns with at least one support position still unseen has its ordinary iid matrix law: one remaining support column with nonzero coefficient can enforce the syndrome for every assignment of the visible columns. Couple this to an ordinary unconditioned matrix, returning identical columns until the query would reveal the last support position. The response at that step can be generated with the conditioned law, after which the coupling may diverge. In the unconditioned run the whole query set depends on the independent matrix, the uniform syndrome and the observer's randomness. It is independent of the uniformly sampled support. Padding repeated or missing queries to $v$ distinct columns bounds the probability that this set contains the entire support by the displayed ratio. This proof allows unlimited computation on each transcript. The model does not give the observer other matrix encodings or access to the seed of a generated matrix.

## Certified profile values

Each entry is a number of allowed queries at which the stated raw gap is at most $2^{-280}$.

| Round 14 target | Key experiment, quantum syndrome coordinates | Payload experiment, quantum word coordinates | Key experiment, classical matrix columns |
|---:|---:|---:|---:|
| 128 | 363 | 636,758 | 6,560,396 |
| 192 | 547 | 1,629,420 | 18,261,799 |
| 256 | 753 | 2,893,365 | 33,821,781 |

The [calculator](query_bounds.py) uses exact integer inequalities. For $1\le D\le n$, set $x=D/(2n)$. Then $M(n,D)\le x^{-D}(1+2x)^n\le(2en/D)^D<(6n/D)^D$. Certify an integer $k$ with $6n\le D2^k$ and use $M(n,D)\le2^{kD}$. For the key denominator use the integer floor of $\log_2 W$, obtained from the bit length of $W$. For the payload denominator use $3^h\ge2^{\lfloor19h/12\rfloor}$, which follows from $3^{12}>2^{19}$. The classical thresholds come from exact binomial comparisons. The first two columns are conservative integer certificates. The final column is the largest query count satisfying this particular bound.

The [finite checks](test_query_bounds.py) independently enumerate character moments for small ternary matrices, inspect classical marginals, and verify the numerical inequalities. The code generates no KEM, attack or recovered key. The classical decoding literature treats hardness on random full-matrix instances as a computational hypothesis. The distribution and field in each application matter. [Alekhnovich, *More on Average Case vs Approximation Complexity*](https://www.cs.toronto.edu/~toni/Courses/PCP/handouts/misha.pdf)

## Comparison with worst-case reductions

Brakerski, Lyubashevsky, Vaikuntanathan and Wichs relate a worst-case binary decoding problem to average-case Learning Parity with Noise in a specified high-noise regime. A 2026 preprint gives a different low-noise result over the binary field, under a simultaneous worst-case assumption on decoding a code and distinguishing noisy codewords of its dual. These results explain why the choice of field, noise law, parameters and starting assumption matters. Applying such a result to SG-DIFRA would require a reduction to its two exact signed-weight ternary distributions and resource accounting at the proposed parameters. The coordinate-query bounds above stand on their separate unconditional arguments. [Brakerski et al., *Worst-Case Hardness for LPN and Cryptographic Hashing via Code Smoothing*](https://eccc.weizmann.ac.il/report/2018/056/) · [*Towards Worst-case Hardness for Low-Noise LPN*](https://arxiv.org/abs/2606.05834)
