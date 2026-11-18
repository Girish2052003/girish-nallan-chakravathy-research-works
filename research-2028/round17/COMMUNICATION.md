# How much information must cross between the matrix and the syndrome?

Give one party the entire random ternary matrix $B$ from the [Round 16 experiment](../round16/MATCHED_PROOF.md). Give a second party the entire syndrome $Y$. The first party can read and preprocess every matrix entry. The second can read every syndrome coordinate. Suppose the parties try to decide whether $Y=Be$ for a hidden signed vector $e$ of weight $w$, or $Y$ was sampled independently and uniformly. At the middle target, even 18,310 bits of two-way classical communication give raw distinguishing advantage at most $2^{-280}$. There is no limit on either party's local computation in this model.

## A second-moment identity

Let $B$ be iid uniform of size $d\times r$ over $\mathbb F_3$, and draw $e$ independently, uniformly from the set $S$ of all $W=2^w\binom rw$ vectors of weight $w$, where $1\le w\le r$. Each marginal, $B$ or $Y$, has the same law in both experiments. In particular $Y$ is uniform since, for any fixed nonzero $e$, the product of a uniformly random row with $e$ is uniform.

For a real or complex function $f$ of a syndrome, set $(Tf)(B)=\mathbb E_e f(Be)$. Use the uniform probability measure on each input space for inner products and $L^2$ norms. Assume $\mathbb E_Y f(Y)=0$. For linearly independent $e,e'$, the pair $(Be,Be')$ is uniform on the product of two syndrome spaces by row independence and surjectivity. The only vectors in $S$ proportional to a given $e$ are $e$ and $-e$. Thus expanding the squared norm gives
$$
\|Tf\|_2^2=\frac1W\bigl(\|f\|_2^2+
\mathbb E_Y f(Y)\overline{f(-Y)}\bigr)
\le \frac2W\|f\|_2^2 .
$$
The cross term is real by the symmetry $Y\mapsto -Y$. Equality holds for centered even functions, and centered odd functions are annihilated. For instance $f(Y)=\mathbf{1}_{Y=0}-3^{-d}$ attains equality if $d\ge1$.

## Interactive classical communication

**Theorem.** For a protocol exchanging at most $c$ bits on every input, with unlimited local computation and input-independent private or shared classical randomness, the raw gap between acceptance probabilities in the two experiments is at most $\min(1,\sqrt{2^{c+1}/W})$.

**Proof.** First fix all random tapes. For a Cartesian product $A\times J$ of matrix and syndrome sets, write $p_A,p_J$ for their probabilities under the corresponding uniform marginals. Its two probabilities differ in absolute value by
$$
\left|\mathbb E_B(\mathbf{1}_A(B)-p_A)\,
     T(\mathbf{1}_J-p_J)(B)\right|
\le \sqrt{\frac2W\,p_A(1-p_A)p_J(1-p_J)}
\le \sqrt{\frac2W\,p_Ap_J}.
$$
A binary protocol of depth $c$ has at most $2^c$ terminal transcripts. For each transcript the compatible input pairs form a rectangle: each message only restricts the sender's input given the preceding transcript. If the final decision stays private to one party, restricting that party's inputs to acceptance still gives one accepting rectangle per transcript. The rectangles are disjoint. Their total product-distribution probability $\sum p_Ap_J$ is at most one. Summing the last displayed bound over the accepting rectangles and applying Cauchy–Schwarz proves the assertion. Averaging over the fixed random tapes preserves the bound. [Standard transcript-rectangle lemma, Roughgarden, Chapter 4](https://arxiv.org/abs/1509.06257)

## A single quantum message

**Theorem.** Suppose the matrix holder sends a single state of $q$ qubits and the syndrome holder decides using an arbitrary syndrome-dependent measurement. With input-independent classical shared randomness and no prior shared entanglement the raw gap is at most
$$
\min\left(1,\sqrt{\frac{2^q-1}{2W}}\right).
$$

**Proof.** Fix the shared classical randomness. Let $M=2^q$, let $\rho(B)$ be the $M$-dimensional transmitted density matrix after averaging the sender's private randomness, and put $\bar\rho=\mathbb E_B\rho(B)$. In the planted joint distribution define $\tau(Y)=\mathbb E[\rho(B)\mid Y]-\bar\rho$. The conditional-expectation operator taking a function of $B$ to its planted conditional expectation given $Y$ is the adjoint $T^*$ in the two uniform marginal inner products. Constants map to constants under both $T$ and $T^*$. On centered functions they have equal operator norms, hence each has norm at most $\sqrt{2/W}$. Apply the adjoint bound entry by entry to $\rho(B)-\bar\rho$. With $\|\cdot\|_F$ the Frobenius norm this gives
$$
\mathbb E_Y\|\tau(Y)\|_F^2
\le (2/W)\mathbb E_B\|\rho(B)-\bar\rho\|_F^2
\le (2/W)(1-1/M).
$$
The last inequality follows from $\operatorname{tr}(\rho(B)^2)\le1$ and $\operatorname{tr}(\bar\rho^2)\ge1/M$. For any measurement effect $0\le E_Y\le I$, the traceless Hermitian matrix $\tau(Y)$ satisfies $|\operatorname{tr}(E_Y\tau(Y))|\le \|\tau(Y)\|_1/2$. Apply $\|X\|_1\le\sqrt M\|X\|_F$ and Cauchy–Schwarz when averaging over $Y$. This yields the theorem. Independent local quantum ancillas can be included in the measurement effect. The proof also works with the parties' sending and receiving roles reversed because the same operator bound holds in both directions.

## Finite values and interpretation

Let $L=\lfloor\log_2 W\rfloor$. To bound the raw gap by $2^{-280}$, the stated inequalities suffice with $c=L-561$ classical bits or $q=L-559$ qubits in the specified one-way model. The [finite checks](test_communication.py) use exact integer arithmetic and exhaust the rectangle inequality on a tiny distribution.

| Matched target | $L$ | Two-way classical bits | One-way qubits without shared entanglement |
|---:|---:|---:|---:|
| 128 | 12,148 | 11,587 | 11,589 |
| 192 | 18,871 | 18,310 | 18,312 |
| 256 | 25,786 | 25,225 | 25,227 |

The ordinary SG-DIFRA challenge gives one solver both inputs directly. A two-party simulation can transfer the whole syndrome, which takes far more than the budgets in the table. Applying this theorem to the KEM would require a separate low-communication simulation of the relevant KEM distinguishers. The bounds establish a property of this distributed experiment and supply no $2^{191}$ lower bound on unrestricted computation.
