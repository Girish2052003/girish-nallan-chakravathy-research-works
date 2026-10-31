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


## NG-Q5 — hypergraph enumerator equivalence (mathematical rejection, not originality)

Fix scopes `E` on `n` global variables, allowing repeated factor scopes, and let `hit_H(S)` count scopes intersecting `S` with multiplicity. Define `P_H(z)=sum_(nonempty S subset V) 2^|S| z^(hit_H(S))`. This is invariant under arbitrary relabeling of global coordinates because support sizes and edge incidences are preserved. A ternary vector with support `S` has exactly `2^|S|` possible nonzero value choices, so by NG-Q4.3, `P_H(alpha_(r,d))=E[|D|-1]` for the independent source-form distribution.

**Exact equivalence:** Let `E[T]` denote all scopes wholly contained in `T`. With `T=V minus S`, the number of edges meeting `S` equals `m-|E[T]|` and `|S|=n-|T|`. The term `S=empty` contributes exactly 1, so

`P_H(z) = sum_(T subset V) 2^(n-|T|) z^(m-|E[T]|) - 1.`

This is a reindexed induced-subhypergraph edge-count enumerator. **No new axioms or foundational novelty.** It could be a useful distributional diagnostic, but naming it does not create a new mathematical structure.

**Example:** One 3-variable factor on n=4 yields `P_H(z)=2+78z` and `P_H(5/39)=12`, in agreement with independently tested direct sum. Formalization and serious polynomial-invariant prior-art comparison remain unperformed.


---

# NG-Q6 — Planted-witness collision probability and high-density uniqueness bound

**Status:** Exact scoped probabilistic theorem with conventional written proof; exhaustive finite checks; **not** proof-assistant-checked or independently peer-reviewed. The conclusion is about the **number** of solutions, not the cost of finding one. It is not a security theorem.

## Model

Use the same independently randomized source-form factor distribution and fixed public scopes as NG-Q4, with `r,d>=1`. Fix any planted `s in F_3^n` **independent** of all local random samplers and set each public target to `t_i=f_i(s restricted to S_i)`. Let `F` be the full public factor-output map and `k(h)` be the number of scopes met by the support of `h`.

## Lemma NG-Q6.1 — exact local collision probability

For two *distinct, fixed* inputs `x,y in F_3^(r+d)` independent of the local random coins,

`Pr[f(x)=f(y)] = beta_(r,d) = (3^d-1)/(3^(r+d)-1)`.

**Proof.** Let `h=y-x !=0` and write `Bh=(h_L,v)`. Uniform `B in GL(r+d,3)` sends `h` uniformly among all `3^(r+d)-1` nonzero vectors. If `v=0`, then `h_L!=0` and `f(y)-f(x)=A h_L!=0`, so a collision is impossible. If `v!=0`, then the potential-dependent part of the difference is the fixed-table-coordinate mixed derivative `Delta_v Delta_a Q(u_R)`. This is a nonzero linear functional of the uniform scalar table: for `v=a,2a`, it is a nonzero multiple of the three-point sum along an a-cycle; for independent `a,v` it is a four-point alternating combination with nonzero coefficients. Therefore it is uniform in `F_3` for one component and uniform in `F_3^r` for independent `r` components, regardless of `A h_L`, giving collision probability `3^(-r)`. Exactly `3^r*(3^d-1)` nonzero ambient directions have `v!=0`; average over B to get the displayed beta. QED.

For the original small scalar source geometry `(r,d)=(1,2)`, `beta=4/13` exactly. The event concerns a *fixed pair* independent of the factor randomness, not an adaptive query chosen after seeing public factor tables.

## Theorem NG-Q6.2 — exact expected number of additional global witnesses

For any independently fixed `s` and fixed scope collection,

`E[|F^(-1)(F(s))|-1] = sum_(h in F_3^n excluding 0) beta_(r,d)^(k(h))`.

Therefore

`P[ F^(-1)(F(s)) contains a different global witness ] <= min(1, sum_(h!=0) beta_(r,d)^(k(h)))`.

**Proof.** For a nonzero global `h`, the planted `s+h` gives the same joint target as `s` precisely when all touched independent local factor outputs collide. Untouched factor inputs are identical and pass automatically; each touched factor collides with exact probability beta by NG-Q6.1, independently across factors. Thus its indicator expectation is beta to the number of touched factors. Sum over all `h!=0`; linearity of expectation is valid even when different h collision events are dependent. The event of non-uniqueness entails at least one additional witness, so Markov's bound proves the second assertion. QED.

## Corollary NG-Q6.3 — all-three-variable scopes

If each three-element global scope has one independently sampled `r=1,d=2` factor, let `m=C(n,3)`, `beta=4/13`. Then

`E[additional witnesses]=sum_(s=1)^n C(n,s)*2^s*beta^(C(n,3)-C(n-s,3))`,

and the probability of non-uniqueness is at most that quantity, clipped at one. The same first-moment argument gives `3^(-Omega(n^2))` for `n` increasing in this dense, independent-factor regime, because every nonzero shift hits at least `C(n-1,2)` factors and beta is strictly below one. QED.

Exact values for `n=4,5,6,7,8,9`: `0.878400616224922`, `0.010935126387797743`, `0.00009172016897832268`, `0.0000002936956418215655`, `2.848193335356639e-10`, `8.366395632216549e-14`. These are probability **upper bounds**, not observed frequencies.

Independent calculations enumerate all 19,683 scalar potential tables and verify that for fixed nonzero right component `v` the mixed derivative at an input equals any specific field value exactly `6561/19683=1/3` of the time. For the cited deterministic 30-instance complete-scope runs, exhaustive global enumeration finds unique fibers in 12/30, 29/30, 30/30 samples for n=4,5,6.

**Security limitation:** A unique solution may be publicly easy to find, as NG-Q7's pair-projection experiment illustrates. No hardness assumption, post-quantum security, private recovery advantage or KEM follows.

---

# NG-Q7 — Public pair-projection consistency: soundness and observed recovery

**Methodological provenance:** This is a constraint-consistency filtering technique in the established CSP family; see Alan K. Mackworth, *Consistency in networks of relations*, *Artificial Intelligence* 8(1), 99–118 (1977), DOI 10.1016/0004-3702(77)90007-8. No originality claim for generic consistency propagation.

Given explicit ternary factor tables, public scopes and public target outputs, initialize each factor relation with the local tuples satisfying its target. Initialize each occurring variable pair's allowed-value set to all `3^2=9` pairs. Repeatedly (a) delete factor tuples whose component pairs are not currently allowed and (b) intersect each pair's domain with all projected surviving factor relations containing that pair. Stop at a fixed point. If every variable's projected unary domain is a singleton, construct that full assignment and **verify all original public equations**. Otherwise report inconclusive, never falsely unsatisfiable.

**Deterministic guarantee (ordinary constraint-filtering consequence).** This iteration terminates in time polynomial in complete explicit table length, global variables and factors. It never deletes a satisfying global assignment from any surviving relation or pair domain. Any returned verified assignment is a genuine global witness.

**Proof.** Initially every satisfying assignment satisfies each factor relation and has its coordinate pairs in the unrestricted pair domains. Assume this holds before a pass. A factor tuple of a satisfying assignment cannot be removed because all of its pairs remain allowed. Each pair projection from a surviving factor relation also contains the pair induced by the satisfying assignment, so intersecting these projections cannot remove that pair. Inductively, the invariant holds at every pass. Each proper pass removes at least one element from a finite tuple relation or pair domain, never adds any; there are at most `sum_i 3^|S_i| +9*number_of_pairs` deletions, so the number of passes and work per pass are polynomial in explicit input size. The output candidate is accepted only after independently evaluating all public equations, so recovery is sound. If no singleton candidate exists, the algorithm reports inconclusive; no completeness assertion is made. QED.

**Finite campaign (no asymptotic success-rate theorem):** The exact seeded independently randomized source-form ensemble from NG-Q4, with planted target `F(s)` independent of generator randomness, yielded public recovery for complete triples at `n=5:29/30`, `n=6:30/30`, `n=7:30/30`, `n=8:30/30`, `n=9:10/10`, `n=10:10/10`, and `n=12:10/10`. Every returned witness was publicly verified. Those same generated datasets had **zero nontrivial global constant-shift subspaces** in all tested cases; thus success did not rely on NG-Q1's quotient-shift shortcut. This is a **scoped classical public-witness attack on toy-to-moderate random public constraint families**, not an IND-CCA break of a KEM.

**Important limits:** Empirical success on deterministic test seeds cannot certify full distribution recovery or a polynomial-time algorithm that always succeeds. The chosen public source generator uses tiny r=1,d=2 local tables and dense complete-triple constraints. Sparse and different source distributions can remain inconclusive. This is not independent expert cryptanalysis or proof-assistant verification.


---

# NG-Q8 — Exact local pair-projection leakage and high-probability public planted-witness recovery

**Full audited theorem and computational finite classification:** [23_NGQ8_PUBLIC_RECOVERY_THEOREM.md](23_NGQ8_PUBLIC_RECOVERY_THEOREM.md). The exact sampler is r=1,d=2, F3, uniform B in GL3, uniform independent potential table Q, independent factors and explicit public local tables.

**NG-Q8.1:** A fixed incorrect two-coordinate assignment is excluded from a single factor's public target-fiber projection with exact probability **15/52**, via complete classification of the 624 ordered independent 3D direction pairs and their uniform affine 3-coordinate images of the nine uniform table entries. This finite case table has independent 19,683-Q-table validations. The complement survival probability is **37/52**.

**NG-Q8.2:** For any fixed triple-scope multihypergraph H with independent local factors and pair codegrees d_ij, public **one-pass** pair-projection intersection recovers the independent planted s with probability at least
`1-min(1,8*sum_(i<j)(37/52)^d_ij)`.
Proof: each planted pair survives every projection, each of its eight alternatives survives independent incident factor tests with probability (37/52)^d_ij; union bound over alternatives and pairs; if all pair domains singleton, reconstruct and publicly verify. Polynomial explicit-table cost.

**NG-Q8.3:** On the complete 3-uniform hypergraph d_ij=n-2, so public recovery failure is at most `min(1,8*C(n,2)*(37/52)^(n-2))` and tends to zero as n grows. This upgrades NG-Q7's empirical success to a **mathematically scoped asymptotic public-recovery theorem**, but does not prove that iterative consistency succeeds for all n.

**NG-Q8.4:** Distinct triples intersecting a selected t-vertex anchor set, t<=n-2, have min pair codegree t and `C(n,3)-C(n-t,3)=O(t*n^2)` factors. Choosing t proportional to log(n/eta) obtains polynomial-time planted recovery with failure <=eta using `O(n^2 log(n/eta))` factors. This rejects another candidate family as a defensible *hard witness* distribution.

The elementary projection method and planted-CSP recovery landscape have extensive prior art. **Model-specific math is documented; genuinely new foundational mathematics remains unestablished.** No formal proof assistant, independent external audit, quantum security argument or active KEM is claimed.


---

# NG-Q9 — Fixed-local-arity public high-codegree recovery bound

**Complete detailed theorem and proof:** [24_NGQ9_GENERAL_ARITY_PROJECTION_BOUND.md](24_NGQ9_GENERAL_ARITY_PROJECTION_BOUND.md).

For fixed r,d>=1, k=r+d, over F3, independent uniform B in GL(k,3), independent uniform r-vector potential Q:F3^d->F3^r, and fixed nonzero a, the probability that `Delta_aQ` is globally constant is exactly `3^(-r*(2*3^(d-1)-1))`. Conditional on this event, the public local map is affine with a uniformly sampled full-row-rank r-by-k linear part. Using exact finite-field rank-matrix enumeration, calculate the positive `gamma_(r,d)` probability that a wrong two-coordinate assignment cannot be repaired by any choice of the other k-2 coordinates. Put `epsilon_(r,d)=gamma_(r,d)*3^(-r*(2*3^(d-1)-1))>0`.

For any fixed k-uniform public factor multihypergraph with independent local source forms and pair codegrees d_ij, a public polynomial-explicit-input one-pass projection attacker recovers the independently planted s with failure probability at most `min(1,8*sum_(i<j)(1-epsilon_(r,d))^d_ij)`. For **k>=3**, complete k-uniform scopes have d_ij=C(n-2,k-2), making the bound tend to zero as n grows. **For k=2, one independent factor per pair has codegree one and does NOT provide a recovery theorem; independently repeated pair factors with growing multiplicity can.**

The epsilon bound can be extremely small, unlike NG-Q8's exact 15/52 for (r,d)=(1,2). This is a mathematical upper bound on public inversion complexity under a specified ensemble, not a security theorem, standalone KEM or novel mathematical foundation. Four new locally executed tests passed after two documented test-expectation/implementation corrections. No proof assistant or external peer reviewer.
