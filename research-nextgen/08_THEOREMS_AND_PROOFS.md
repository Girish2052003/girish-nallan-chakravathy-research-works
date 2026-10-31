# NG-Q1 — Exact public quotient witness and fiber counting

**Status:** Detailed conventional mathematical proof, finite tests; not externally peer-reviewed, not proof-assistant checked. Originality relative to general finite-function linear-structure/quotient literature **unresolved**. This strengthens the *attack analysis* of existing Theorem 12.10, not an underlying KEM.

## Definitions and hypotheses

Fix the prime field `K=F_3`. Let `V=K^n`. Let public local functions `f_i:K^{S_i}->K^{r_i}` have complete explicit finite tables, with public scopes `S_i` of distinct global coordinates. Define `F:V->W=K^R`, `R=sum_i r_i`, as the concatenation of all public factor outputs. Set

`D={h in V: F(x+h)-F(x) does not depend on x in V}`

and `Gamma(h)=F(h)-F(0)` for `h in D`. The subgroup `D` is a `K`-linear subspace and `Gamma:D->W` is linear. Let `E` be any publicly computed complementary linear subspace: `V=E direct-sum D`. Write `c=dim E=n-dim D` and `s=rank Gamma`.

The existing Round-8 `PublicShiftSystem` computes `D`, a basis, and `Gamma` from explicit factor tables. Its restriction test gives exactly `D=C(F)`, because each global coordinate projection onto a public factor scope is surjective: a constant joint derivative implies a constant derivative on every local scope, and vice versa.

## Theorem NG-Q1 (exact decomposition, completeness, exact count)

For every target `t in W`, define the feasible quotient representatives

`Z_t={z in E : t-F(z) belongs to im Gamma}`.

Then

`F^(-1)(t) = disjoint_union_(z in Z_t) [z + h_z + ker Gamma]`,

where `h_z` is any solution of `Gamma(h_z)=t-F(z)`. In particular,

`|F^(-1)(t)| = |Z_t| * 3^(dim D - rank Gamma)`.

A deterministic public algorithm can recover a witness or correctly declare **unsatisfiable** by enumerating the `3^c` representatives `z in E` and solving the linear equations for `h_z`. It can compute the exact fiber cardinality in the same enumeration. The total work is `3^c * poly(L+n+R)` after polynomial preprocessing in the *complete explicit factor-table length* `L`. Hence it is polynomial whenever `c=O(log(L+n+R))`, independently of primal graph width and of whether `Gamma` is surjective.

## Proof

1. For `h,k in D`, finite differences telescope:
`F(x+h+k)-F(x)=[F(x+h+k)-F(x+h)]+[F(x+h)-F(x)]=Gamma(k)+Gamma(h)`.
This makes `D` an additive subgroup, `Gamma` additive, and both linear over the prime field `F_3` (multiplication by 0,1,2 is repeated addition). Moreover `F(x+h)=F(x)+Gamma(h)` for every `x,h`.
2. Extend any basis of `D` to a basis of `V`, taking the extra basis vectors to span `E`. Every `x in V` has a **unique** representation `x=z+h` with `z in E,h in D`.
3. Thus `F(x)=t` iff `F(z)+Gamma(h)=t`. For fixed `z`, this linear equation is solvable precisely when `t-F(z) in im Gamma`. If solvable, its entire solution set in `D` is the affine coset `h_z+ker Gamma`.
4. Distinct `z` give disjoint subsets by uniqueness of the direct-sum decomposition. Rank-nullity gives `|ker Gamma|=3^(dim D-s)`, yielding the exact formula.
5. Every possible `x` belongs to one of these cases, so exhaustive quotient enumeration returns a witness exactly when one exists, otherwise correctly reports unsatisfiable. Public table scanning to construct `D` is polynomial in explicit input length, basis extension/linear solves are polynomial, and there are exactly `3^c` representatives. QED.

**Independent logical challenge:** No claim is made that large graph width is necessary or that small codimension occurs on the intended random NCSG security distribution. The algorithm is exponential if `c` grows linearly in succinct input length. An exact linear structure may not be efficiently discoverable from a succinct oracle in that regime. The factor tables, not only one target relation, are required.

**Formal verification:** NONE. The existing Round-8 script and new Python regression validate particular finite instances; they do not formally check this universal statement. No security assumption is established.


---

# NG-Q4 — Exact global shift-survival first moment for independently randomized source-form NCSG

**Status:** Conventional proof and independent local finite checks; not proof-assistant-checked or externally reviewed. This concerns a very specific random source form, not KEM key secrecy or average-case constraint-solving hardness. Methodological antecedents include finite-field linear structures and the standard first-moment method.

## Model, quantifiers, and notation

Fix integers `r>=1`, `d>=2`, `k=r+d`; let `V=F_3^n`. Fix an arbitrary collection of **public ordered coordinate scopes** `S_1,...,S_m`, each containing exactly `k` distinct global indices. Independently for every factor `i`, sample a uniform invertible `B_i in GL(k,3)` and an independent uniform table `Q_i:F_3^d -> F_3^r`. Fix any nonzero `a_i in F_3^d` and any invertible `A_i in GL(r,3)`; these may be deterministic, since they do not affect the event analyzed. Define `u=B_i x`, partitioned into `u_L in F_3^r` and `u_R in F_3^d`, and define

`f_i(x) = A_i u_L + Q_i(u_R+a_i)-Q_i(u_R)`.

Let `F:V->(F_3^r)^m` concatenate the public `f_i(x|S_i)`. Define the global constant-shift space

`D={h in V : F(x+h)-F(x) is independent of x in V}`.

For `h`, put `k(h)=#{i:h restricted to S_i is nonzero}`.

## Lemma NG-Q4.1 — local mixed-difference ranks

For a **uniform** scalar potential table `Q:F_3^d -> F_3` and fixed `a!=0`, the linear operator `L_(a,v)=(T_v-I)(T_a-I)` on table functions, with `(T_v Q)(x)=Q(x+v)`, has ranks:

- `3^(d-1)` if `v=a` or `v=2a`;
- `4*3^(d-2)` if `v` is independent of `a`.

The one-dimensional subspace of globally constant tables lies in the image of either operator. Therefore the probability `L_(a,v)Q` is globally constant is `3^(-(rank-1))`. With an independent uniform `r`-component potential, raise that probability to the `r`th power.

**Proof.** For one 3-cycle of translations in direction `a`, `N=T_a-I` has rank 2, `N^2` rank 1 and `N^3=0` over characteristic 3. If `v=a`, the operator is `N^2`. If `v=2a`, `T_(2a)-I=(I+N)^2-I=2N+N^2`; multiplying by `N` gives `2N^2`. There are `3^(d-1)` independent a-cosets. For independent `a,v`, choose them as the first two coordinates in an invertible linear basis; translation acts on independent 3-cycles, so on each 9-point orbit `L` is the tensor product of two rank-2 operators and has rank 4. There are `3^(d-2)` orbits. The all-one table belongs to the image: the all-one triple lies in the image of `N` (its entries sum to zero in characteristic 3) and the image of `N^2`; tensoring gives the same for 9-point orbits, and choices can be made independently across orbits. Thus the intersection of the image with the globally constant tables is exactly one-dimensional. Uniform table sampling maps uniformly onto the operator image, giving the claimed probabilities. Independent output coordinates multiply probabilities. QED.

## Theorem NG-Q4.2 — exact fixed-direction survival probability

For every fixed nonzero `h in F_3^k`, under an independently uniform local `B,Q` as specified,

`P[h in C(f)] = alpha_(r,d)`, where

`alpha_(r,d) = ((3^r-1) + 3^r*(2*3^(-r*(3^(d-1)-1)) + (3^d-3)*3^(-r*(4*3^(d-2)-1)))) / (3^(r+d)-1)`.

For `(r,d)=(1,2)`, this is **exactly `5/39`**.

**Proof.** A uniformly random `B in GL(k,3)` sends any fixed nonzero `h` uniformly among the `3^k-1` nonzero vectors. Among these, exactly `3^r-1` have right component `v=0`; their derivative is constant regardless of `Q`. There are `3^r*2` vectors with `v=a` or `v=2a`, and `3^r*(3^d-3)` with independent nonzero right `v`. Lemma NG-Q4.1 supplies their independent potential-table probabilities. The left linear term `A u_L` contributes a constant to every derivative and does not change whether the full derivative is constant. Average over these disjoint classes to obtain the exact fraction. For `r=1,d=2`: `(2+3*(2/9+6/27))/26 = 5/39`. QED.

## Theorem NG-Q4.3 — exact first moment and probability bound

For every fixed scope collection and every `n>=0` with valid scope sizes,

`E[|D|-1] = sum_(h in F_3^n\{0}) alpha_(r,d)^(k(h))`.

Consequently,

`P[D != {0}] <= min(1, (1/2)*sum_(h != 0) alpha_(r,d)^(k(h)))`.

**Proof.** For a fixed nonzero global `h`, each local factor whose scope misses its support has zero input shift and automatically passes the constant-derivative criterion. For each of the `k(h)` remaining factors the restriction is nonzero, hence independently passes with probability `alpha_(r,d)` by NG-Q4.2. Because local `B_i,Q_i` are sampled independently, the global survival probability is their product. Linearity of expectation of indicators gives the exact expected number of nonzero global constant shifts. Finally `D` is an `F_3`-linear subspace, so if nontrivial it contains at least two distinct nonzero vectors `h,2h`. Pointwise `|D|-1 >= 2*1_{D!={0}}`, and taking expectations proves the stated upper bound. QED.

## Corollary NG-Q4.4 — all-triples scopes and asymptotic restriction

For exactly one independently randomized local factor on **every** three-element subset of `[n]`, put `m=C(n,3)` and `alpha=5/39`. Then

`E[|D|-1] = sum_(s=1)^n C(n,s)*2^s*alpha^(C(n,3)-C(n-s,3))`,

with `C(u,3)=0` for `u<3`. Moreover,

`P[D!={0}] <= min(1, (3^n-1)*alpha^(C(n-1,2))/2)`,

which is `3^(-Omega(n^2))` as `n` increases under this **dense independent-factor** distribution. The sharper exact-sum bound from NG-Q4.3 is available for finite `n`.

**Proof.** Group nonzero `h` by Hamming weight `s`: there are `C(n,s)*2^s` such shifts, each meeting `C(n,3)-C(n-s,3)` scopes. Every nonzero shift meets at least the `C(n-1,2)` triple scopes containing any one supported variable. Substitute these counts in NG-Q4.3. Since `0<alpha<1`, the final expression decays as asserted. QED.

## Adversarial review, limits, and status

This theorem does **not** say that finding a witness is hard, that random targets are satisfiable, that planted instances conceal their witnesses, or that no public algorithm exploits other algebraic structure. It only bounds the probability that the **particular additive constant-shift space** is nontrivial. Its strongest regime uses all `C(n,3)` independent factor functions; sparse scopes and correlated generation can behave differently. The probability bound is over fresh local `B_i,Q_i` randomness *conditional on fixed public scopes*, not over unknown KEM key distributions.

Independent checks: all 19,683 scalar potential tables for `d=2` gave `2187/19683=1/9` for parallel `v`, `729/19683=1/27` for independent `v`; direct matrix rank calculations for every nonzero `v` in `d=2,3` matched Lemma NG-Q4.1. Exact rational arithmetic matched the scope-enumeration and weight-enumeration formulas for `n=3,4,5`. A mistaken initial test expectation for a disconnected-scope case (26/3 instead of 12) was **corrected** before accepting the final seven-test suite.

These are conventional written proofs and finite checks, **not** Lean/Rocq machine proofs. Prior-art novelty relative to Charpin–Kyureghyan linear-structure theory and standard random-CSP first-moment methods remains **open**; no foundational mathematical originality is asserted.
