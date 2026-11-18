# Challenge-coupled differential solvability over the ternary field

**Date:** 18 November 2026. **Status:** written mathematical proofs with finite
executable checks and agent review; not proof-assistant certification or
external peer review. See the [assumption ledger](ASSUMPTIONS_AND_SECURITY_BOUNDARY.md)
and [verification record](VERIFICATION_REPORT.md).

**Research question.** Given one sparse polynomial map over $\mathbb F_3$, does every direction in a specified affine family translate *some* input to a second input with the same output? A different input may answer each direction. For maps of total degree at most one, two, and three, respectively, the resulting worst-case decision problem is in $\mathrm P$, is $\mathrm{coNP}$-complete, and is $\Pi_2^{\mathrm P}$-complete.

The [earlier NCSG-DS result](../../manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.md) concerns a given system of differential equations with an existentially quantified common solution. Here the public challenge selects a translation of a single potential. The target is always the zero vector. The distinction between a single challenge and universal coverage is essential to the classification below.

## 1. Input, witnesses, and degree

Write $z=(s,x,y)\in\mathbb F_3^{n}$, where $s$ is one coordinate, $x$ has $k$ coordinates, $y$ has $r$ coordinates, and $n=1+k+r$. The input consists of labeled, explicitly listed coordinates in these three blocks and a vector potential $P=(P_1,\dots,P_m)$ with explicitly listed outputs. We allow $m=0$, whose answer is vacuously YES; all hardness reductions use $m\geq1$. A component is a sparse list of its nonzero monomials. Use coefficients in $\{1,2\}$, list factors by increasing coordinate index with exponent one or two, combine equal monomials modulo three, and sort terms by total degree and then lexicographically by the repeated-index tuple. The empty monomial is the constant one and an empty term list is the zero polynomial. These are the unique reduced polynomial representatives of functions on $\mathbb F_3^n$. The degree bound refers to the largest sum of exponents of a listed monomial. We include zero components at every degree. The size $L$ counts the full bit encoding, including the coordinate lists, output delimiters, terms, and indices. Thus $n,m\leq O(L)$ even when many coordinates are unused.

For $c\in\mathbb F_3^k$ let $h_c=(1,c,0^r)$. All these directions are nonzero. Define

$$
N_P(c)=\#\{z\in\mathbb F_3^n:P(z+h_c)-P(z)=0^m\}.
$$

For degree bound $d$, **challenge-coupled differential solvability**, denoted here by $\mathcal D_d$, asks whether

$$
\forall c\in\mathbb F_3^k\quad N_P(c)>0.
$$

The potential is fixed before $c$ is chosen. There are no input truth tables, challenge-dependent targets, or supplied constraints on the witness. The zero-length block conventions are the usual ones. In particular $k=0$ gives the single direction $(1,0^r)$. We also consider the **fixed-challenge problem** whose input includes one $c$ and whose question is $N_P(c)>0$. All completeness statements below use deterministic polynomial-time many-one reductions.

| Degree bound | Fixed challenge | All challenges |
| --- | --- | --- |
| At most 1 | In $\mathrm P$ | In $\mathrm P$ |
| At most 2 | In $\mathrm P$ by linear algebra | $\mathrm{coNP}$-complete |
| At most 3 | $\mathrm{NP}$-complete | $\Pi_2^{\mathrm P}$-complete |

## 2. Affine potentials

**Theorem 1.** For $d\leq1$, the universal question can be decided by inspecting the input coefficients.

**Proof.** Write $P(z)=b+A_s s+A_x x+A_y y$. For every $z$ the difference is $A_s+A_x c$. This vanishes for every $c$ exactly when $A_s=0$ and all columns of $A_x$ vanish, as follows by testing $c=0$ and each coordinate vector. If the difference vanishes, $z=0$ supplies a witness. If a column is nonzero and $A_s=0$, its coordinate vector is a failing challenge. If $A_s\ne0$, the zero challenge already fails. This also proves the fixed-challenge claim. $\square$

For example, take $k=r=1$ and $P(s,x,y)=(2y+1,2x+y+1)$. Its difference is $(0,2c)$. Challenge $c=0$ admits all $27$ basepoints and $c=2$ has difference $(0,1)$ everywhere, so the universal answer is NO.

## 3. Quadratic potentials

**Theorem 2.** The universal problem $\mathcal D_2$ is $\mathrm{coNP}$-complete.

**Membership.** For a fixed $a=h_c$, put $D(z)=P(z+a)-P(z)$. Differencing a polynomial of degree at most two cancels its quadratic part in $z$. Thus $D(z)=M_a z+b_a$, where $b_a=D(0)$ and column $i$ of $M_a$ is $D(e_i)-D(0)$. Sparse evaluation and Gaussian elimination decide consistency in time polynomial in $L$ and return a witness whenever one exists. A challenge $c$ with an inconsistent system is a polynomial-length certificate for a NO instance of the universal question.

**Hardness.** Take a nonempty 3-CNF formula $\varphi$ on $k$ Boolean variables. It suffices to use the $\mathrm{coNP}$-complete UNSAT problem for clauses of exactly three literals, allowing repetitions. A shorter nonempty clause can be padded by repeating a literal. Trivial source cases such as an empty conjunction or an empty clause can be decided directly and replaced by fixed source instances. Denote the Boolean assignment selected by a ternary challenge by $\beta_i=c_i^2$. Each $\beta_i$ is zero or one, and the map onto Boolean assignments is surjective.

We first give a system in the unshifted witness wires $y$. For each clause $j$, make a free scalar $\alpha_j\in\mathbb F_3$ and write $w_{j,0}=\alpha_j$ as an alias. For its $t$th literal, $1\leq t\leq3$, on variable $i$, add fresh wires $p_{jt},q_{jt},w_{jt}$ and require

$$
p_{jt}=c_i w_{j,t-1},\qquad
q_{jt}=c_i p_{jt},\qquad
w_{jt}=
\begin{cases}
w_{j,t-1}-q_{jt},&\text{for the positive literal }\beta_i,\\
q_{jt},&\text{for the negative literal }\neg\beta_i .
\end{cases}
$$

Add the final equation $\sum_j w_{j,3}=1$. Indeed, $q_{jt}=\beta_i w_{j,t-1}$, so each step multiplies the incoming wire by the indicator that the current literal is false. At the end $w_{j,3}=\alpha_j$ if the entire clause is false and is zero otherwise. A false clause permits setting its $\alpha_j=1$ and all other selectors to zero. When all clauses are true the left side is always zero. Thus, for fixed $c$, the wire system is solvable exactly when $\varphi(\beta)$ is false. The free selectors prevent simultaneous falsification of three clauses from being mistaken for zero modulo three.

To turn these equations into a *single potential*, move each equation to the left and use one output component per row. Every row is a sum of terms of the form $\ell(c)v$, with $\ell(c)=a+\sum_i b_i c_i$ affine and $v$ an unshifted wire, and possibly a constant $d_0$. Replace each $\ell(c)v$ by $(as+\sum_i b_i x_i)v$ and each $d_0$ by $d_0s$, then add the terms. Their differences along $h_c$ are $\ell(c)v$ and $d_0$, respectively, for every basepoint $(s,x,y)$. Every component has degree at most two. All wires, rows and monomial occurrences total $O(k+|\varphi|)$ in variable/literal units, including the single summation row. Indexing them in binary adds at most a logarithmic factor to this structural size. For every $c$, the added basepoint coordinates $s,x$ are free and do not alter solvability. Surjectivity of $c\mapsto\beta$ gives

$$
P\in\mathcal D_2\quad\Longleftrightarrow\quad
\varphi\text{ is unsatisfiable}.
$$

This proves hardness and completes the proof. $\square$

For a numerical instance of the reduction, take $\varphi=(u\lor u\lor u)\land(\neg u\lor\neg u\lor\neg u)$ and $c=2$, so $\beta=1$. Choose the second selector to be one and the first to be zero. Each of the three negative-literal steps takes incoming $1$ to $(p,q,w)=(2,1,1)$, giving a final sum of one. At $c=0$ the first clause supplies the witness, and at $c=1$ the second does. Dropping the negative clause gives a NO instance, since $c=1$ then forces a final sum of zero.

### Two tractable quadratic regimes

**Proposition 3.** The universal quadratic problem admits a deterministic algorithm using $O(3^{\min(k,m)}\,\operatorname{poly}(L))$ time. A homogeneous quadratic map plus a constant has a collision for every challenge.

**Proof.** Write $P=Q+H+b$, with $Q$ homogeneous quadratic and $H$ linear. Define the vector-valued polar form $B_Q(u,a)=Q(u+a)-Q(u)-Q(a)$, bilinear in its arguments. The change of basepoint $u=z+a/2$ gives

$$
\Delta_a P(z)=B_Q(u,a)+H(a).
$$

Here $2^{-1}=2$ in $\mathbb F_3$ and $B_Q(a,a)=2Q(a)$. If $H=0$, the midpoint choice $u=0$, equivalently $z=-a/2=a$, always works.

For general $H$, the linear equation in $u$ is inconsistent exactly when a vector $\lambda\in\mathbb F_3^m$ annihilates $B_Q(\,\cdot\,,a)$ but does not annihilate $H(a)$. This is the left-nullspace consistency criterion. A nonzero value of $\lambda^\top H(a)$ can be scaled to one. A checkable obstruction is therefore a pair $(c,\lambda)$ satisfying

$$
\lambda^\top B_Q(e_j,h_c)=0\ \ (1\leq j\leq n),
\qquad \lambda^\top H(h_c)=1 .
$$

For fixed $\lambda$, these are affine linear equations in $c$. Enumerate the $3^m-1$ nonzero $\lambda$ and solve for $c$, stopping at an obstruction. Alternatively enumerate the $3^k$ challenges and solve directly for $z$ by Theorem 2. Taking the smaller bound proves the proposition. In particular $k=O(\log L)$ or $m=O(\log L)$ suffices for polynomial time at degree two. $\square$

For example, with $k=r=m=1$, $P(s,x,y)=xy-s$, the fixed-challenge equation is $cy=1$. For $c=1,2$ choose $y=1,2$ respectively. For $c=0$, $B_Q(\,\cdot\,,h_0)=0$ and $H(h_0)=2$, so $\lambda=2$ certifies inconsistency. Removing the term $-s$ yields a homogeneous quadratic for which $z=h_c$ works for all three challenges.

## 4. Cubic potentials

**Theorem 4.** The universal problem $\mathcal D_3$ is $\Pi_2^{\mathrm P}$-complete. On the instances of the reduction, the number of collision basepoints at each direction equals the number of accepting Boolean responses to its associated universal input.

**Membership.** The challenge and the basepoint have polynomial length, and the two evaluations and equality test take polynomial time in $L$. This is a universal polynomial-length choice followed by an existential polynomial-length choice and a deterministic polynomial-time test. Ternary strings can be encoded by two bits per coordinate, mapping the fourth bit-pair to zero, so the domain choice gives the usual $\Pi_2^{\mathrm P}$ predicate.

**Hardness.** Start with the truth problem for a Boolean circuit assertion $\forall U\in\{0,1\}^k\,\exists V\in\{0,1\}^b:\ C(U,V)=1$. The two-block circuit problem is $\Pi_2^{\mathrm P}$-complete by the quantified polynomial-verifier characterization. Given any language in this class, compile its polynomial-time test into a polynomial-size circuit in polynomial time, fixing the original instance and leaving the universally and existentially quantified strings as circuit inputs. Use Boolean constants, AND gates of fan-in two, and NOT gates. This is a complete gate basis with constant overhead for standard fan-in-two Boolean operations.

Let $y$ contain one wire $u_i$ for each universal bit, one wire $v_j$ for each response bit, and one output wire per gate. In a temporary variable block $X$ define residuals $G_j(X,y)$ as follows.

| Condition | Residual to be set to zero |
| --- | --- |
| Associate a ternary value $X_i$ to its Boolean bit | $u_i-X_i^2$ |
| Restrict a response to a Boolean bit | $v_j(v_j-1)$ |
| AND gate with inputs $a,b$ and output $w$ | $w-ab$ |
| NOT gate with input $a$ and output $w$ | $w-(1-a)$ |
| Accept the final circuit output $o$ | $o-1$ |

Constants may be used directly as gate inputs or as $o$. Circuit input/output wires are reused by identifier. Every residual has total degree at most two. For each $X=c$, the $u_i$ are fixed to $(c_i^2)_i$. Each valid choice of Boolean response gives unique values of all gate wires in circuit order. Conversely a solution to the residual equations gives exactly an accepting Boolean response, since the field equations for the gates preserve Boolean values starting from valid inputs.

The vector potential contains one component to fix $s$, one for each shifted $x_i$, and one for each residual.

$$
P_{\rm pin}=\tfrac12s(s-1),\qquad
P_i=(s-1)x_i\quad(1\leq i\leq k),\qquad
P_{G_j}=sG_j(x,y)\quad\text{for each residual}.
$$

Their first differences include

$$
\Delta_{h_c}P_{\rm pin}=s,\qquad
\Delta_{h_c}P_i=x_i+s c_i .
$$

Zero target first forces $s=0$ and then forces $x=0$. At precisely this basepoint in the shifted blocks the remaining differences are

$$
\Delta_{h_c}\big(sG_j(x,y)\big)\big|_{s=0,x=0}=G_j(c,y).
$$

Consequently, for every $c$ the projection of a collision basepoint to its $v$ wires is a bijection onto $\{V:C((c_i^2)_i,V)=1\}$. Its inverse sets $s=x=0$, sets each $u_i=c_i^2$, and evaluates the gates on that $V$. In particular there is no multiplicity from the two possible nonzero representations of a universal bit once $c$ has been fixed. Since the square map covers every Boolean input, every challenge has a collision exactly when the quantified circuit is true.

All components have degree at most three, each residual contributes only a constant number of monomials, and there are linearly many variables, outputs and term occurrences in the circuit description. Binary wire indices cost at most a logarithmic factor. Reducing and sorting the sparse lists is polynomial time and preserves all component functions. This proves both the many-one reduction and the count identity. $\square$

For a small cubic check, encode the requirement that one response bit equal the selected universal bit. Use coordinates $(s,x,u,v)$ and components

$$
\big(\tfrac12s(s-1),\ (s-1)x,\ s(u-x^2),\ sv(v-1),\ s(v-u)\big).
$$

For $c=2$, the unique basepoint is $(0,0,1,1)$ and its translated endpoint is $(1,2,1,1)$. All five components vanish at both endpoints. For $c=0$ the unique basepoint is $(0,0,0,0)$, while $c=1$ gives the same basepoint as $c=2$ with a different translated endpoint. This example has $N_P(c)=1$ for every challenge.

**Corollary 5.** The fixed-challenge problem at degree at most three is $\mathrm{NP}$-complete, including when $k=1$ and the specified challenge is always $c=0$. For each fixed degree bound $d\geq3$, universal coverage remains $\Pi_2^{\mathrm P}$-complete.

**Proof.** Guessing and evaluating $z$ proves membership in $\mathrm{NP}$ for the fixed challenge. In the cubic construction take any Boolean circuit satisfiability input, add one unused universal input, and specify $c=0$. The bijection in Theorem 4 yields a collision exactly when the original circuit has an accepting input. Sparse polynomial evaluation gives the same universal upper bound for any fixed $d$, and the cubic instances already give its lower bound. $\square$

For example, a circuit asserting $v_1\mathbin{\rm AND}v_2$ with $k=1$, $c=0$ pins $s=x=u=0$ and adds Boolean wires $v_1,v_2$, a gate $w=v_1v_2$ and the condition $w=1$. Its only basepoint, in order $(s,x,u,v_1,v_2,w)$, is $(0,0,0,1,1,1)$.

## 5. What the comparison establishes

The degree-two and degree-three reductions use the same affine family of genuine translations, the same fixed field and a single vector potential with zero target. For each given direction, a quadratic potential gives affine equations in the basepoint. A cubic potential can express a complete Boolean verification problem within a single directional collision equation. A $\Pi_2^{\mathrm P}$-complete problem is outside $\mathrm{NP}$ **if** $\Pi_2^{\mathrm P}\not\subseteq\mathrm{NP}$. A strict separation between the cubic universal problem and the earlier $\mathrm{NP}$-complete NCSG-DS problem needs that unresolved complexity assumption. No assumption is needed for the completeness classifications themselves.

The [Round 8 ledger](../ROUND8_PUBLIC_GLOBAL_CSP_SECURITY_LEDGER.md) treats other input models, including explicit ternary tables, bounded-width factorizations, and targets inside a public shift image. Here one sparse public map specifies exponentially many possible challenges as $k$ grows. This universal coverage property does not ask anyone to invert an honestly sampled ciphertext. No distribution of cryptographic instances, secret recovery advantage, rate of growth of optimal attack time, or key size follows from the reductions. The private recovery question in the [continuation record](../CONTINUATION_STATE.md) remains open.

The Boolean source problems, polynomial hierarchy, and finite-difference and polarization identities have established precedents. The contribution here is the formulation and the explicit degree-sensitive realizations over $\mathbb F_3$, including the per-challenge witness bijection. The proofs establish their statements independently of whether an equivalent theorem has appeared elsewhere. Counts $N_P(c)$ are entries of the zero-output column of a difference distribution table. Zero-difference balanced functions impose equal counts in every nonzero direction, whereas the question here asks only for positive counts on the stated affine family.

## References

- Richard M. Karp, “Reducibility Among Combinatorial Problems,” 1972, including satisfiability with at most three literals per clause. [Original paper](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf)
- Larry J. Stockmeyer, “The polynomial-time hierarchy,” *Theoretical Computer Science* 3 (1976), 1–22. [Publisher record](https://doi.org/10.1016/0304-3975(76)90061-X)
- Michael Bauland and coauthors, “Quantified Constraints: The Complexity of Decision and Counting for Bounded Alternation,” 2005. [ECCC report](https://eccc.weizmann.ac.il/report/2005/024/)
- Cunsheng Ding and Yin Tan, “Zero-difference balanced functions with applications,” 2012. [Publisher record](https://doi.org/10.1080/15598608.2012.647479)
