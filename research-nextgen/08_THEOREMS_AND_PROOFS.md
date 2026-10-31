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
