# NG-Q2 — High-width, rank-deficient, publicly recoverable family

**Status:** Explicit mathematical counterexample with proof, reproducible constructed fixtures. This is not a claim about uniform-random NCSG factors or finite-profile KEM security.

## Construction

For any integer `q>=4`, use global ternary variables `z,x_1,...,x_q`; let every edge `{i,j}` of the complete graph on `1,...,q` define a public scalar factor on scope `(z,x_i,x_j)`:

`f_ij(z,x_i,x_j)=x_i+x_j+b_ij*z^2 (mod 3)`,

where exactly one fixed edge `{1,2}` has `b_12=1`, and all other `b_ij=0`. Every local factor has 27 explicitly enumerable inputs, and there are `m=q(q-1)/2` factors.

**Relation to the SG-DIFRA source form:** In each local factor choose hidden-coordinate map
`(u_L,u_R1,u_R2)=(x_i+x_j,z,x_j)`, which is invertible. Set `A=1`, `a=(0,1)` and `Q(u_R1,u_R2)=b_ij*(u_R1)^2*u_R2`. Then `Delta_a Q=b_ij*z^2`, so the factors really are of the original `A u_L + Delta_a Q(u_R)` type, albeit **not** a draw from the original uniform potential distribution.

## Claims and proof

1. **Primal width `q`:** each factor links `z,i,j`. The union of all scopes makes all `q+1` variables mutually adjacent; the primal graph is `K_(q+1)`, treewidth exactly `q`.
2. **Global constant shift space has dimension `q`:** any shift with `h_z=0` changes each factor by the constant `h_i+h_j`. Any `h_z!=0` produces, on the exceptional edge, derivative `2*h_z*z+h_z^2+h_i+h_j`, which depends on `z` in `F_3`. Thus `D={h:h_z=0}`, of dimension `q`; quotient dimension `c=1`.
3. **Increment map is deficient:** `Gamma(h)_(ij)=h_i+h_j`. Its edge-sum matrix for complete `K_q` has rank `q` over `F_3`: if all pair sums vanish, a triangle implies every coordinate zero (as `2!=0` in `F_3`). Since `m>q`, `Gamma` is not surjective.
4. **A satisfiable target fails the old shift criterion:** let `t_(12)=1` and every other edge target be zero. The assignment `z=1,x_i=0` satisfies it. But `t-F(0)=t` is **not** in `im Gamma`: equations from edges `13,14,34` force `h_1=h_3=h_4=0`; edge `23` then forces `h_2=0`, contradicting `h_1+h_2=1`. Consequently existing Round-8 shift-only recovery reports inconclusive.
5. **The new quotient attack succeeds:** `E` can be spanned by the unit vector in the `z` coordinate. It checks at most three quotient representatives, including `z=1`, whose public evaluation already equals `t`. It recovers a valid witness and can count all witnesses exactly. For fixed local arity, the cost is polynomial in `q` despite unbounded width and deficient `Gamma`.

## Executed checks (Python 3.13.5; 31 October 2026)

`python -m unittest -v test_public_global_quotient_witness_recovery` executed three methods successfully in a local workspace.

| q | n | m | primal width | dim D | rank Gamma | c | cosets examined to witness |
| ---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 5 | 6 | 4 | 4 | 4 | 1 | 2 |
| 5 | 6 | 10 | 5 | 5 | 5 | 1 | 2 |
| 8 | 9 | 28 | 8 | 8 | 8 | 1 | 2 |

The regression additionally checks 48 randomized small public factor systems (`n=1,...,4`, 12 each), all nine scalar-pair targets per system, matching independent brute-force existence and exact solution counts. Tests include empty and unsatisfiable constant-factor cases. Randomness seed: `20261031`.

**Caveats:** Local tests used a lightweight reproduction of the existing Round-8 support module in the test directory; the committed new script imports the canonical Round-8 module. The new version on GitHub has not yet been separately run by CI. The family is deliberately constructed and NOT a break of real-size NCSG cryptography; it rebuts only the inference that high width plus a non-surjective shift map makes a problem hard.
