# Understanding NG-Q1/Q2 in three levels

## Level 1 — absolute beginner

Imagine a big puzzle with two knobs, `x` and `y`. A public machine shows two numbers:

`A=x+y*y` and `B=2*x+y*y`. We count in threes: after 2 comes 0, so `3=0` and `4=1`.

We are given `A=1,B=1` and want any two knob settings that produce those numbers.

An old shortcut tried changing only the `x` knob from `x=0,y=0`. Every extra 1 on `x` changes `A` by 1 but `B` by 2. It cannot reach `(1,1)` from `(0,0)` with that change alone.

Our stronger method says: **Try the genuinely different settings of the `y` knob too.** For `y=1`, `y*y=1`, and `x=0` gives `A=1,B=1` immediately. For `y=2`, the square is 4, which equals 1 when counting in threes; that also works.

The important thing is **not** a new secret code. It is another way an outsider can solve a puzzle using only public information. For a cryptosystem, that's a warning: hiding a puzzle's answer is useless if outsiders have a shortcut.

## Level 2 — university mathematics

Let `F:F_3^n -> F_3^R` be a public finite-field map formed from overlapping local factors. Define its constant-difference directions `D={h: Delta_h F is constant}`, a subspace, and the linear increment map `Gamma(h)=F(h)-F(0)`. Choose a complement `E` with `F_3^n=E direct-sum D`.

Every vector `x` uniquely equals `z+h`, with `z in E`, `h in D`, and `F(x)=F(z)+Gamma(h)`. Thus testing all quotient representatives `z` and solving a linear system in `h` **fully solves** the public preimage problem, using `3^(n-dim D)` quotient trials. The exact number of preimages is `|Z_t| * 3^(dim D-rank Gamma)`.

For the two-variable example, `D` consists of shifts `(h,0)`; `Gamma(h,0)=(h,2h)`. `E` consists of vectors `(0,y)`, so its dimension is 1. The target `(1,1)` is not in `im Gamma` from `F(0)=(0,0)`, but checking `z=(0,1)` gives `F(z)=(1,1)`.

## Level 3 — research defense

**What exactly is the result?** A complete quotient-enumeration attack and exact fiber formula under *explicit complete public local function tables*. It refines the sufficiency-only Round-8 Theorem 12.10. The constructed NG-Q2 family also disproves the inference that high primal width plus deficient global shift rank implies hardness.

**Is it new mathematics?** Not established. Linear structures, quotient spaces, affine cosets, orbit arguments and Gaussian elimination are established. The possibly project-specific result is their explicit exploitation for overlapping SG-DIFRA-source-form public factors, with a high-width counterexample. A serious literature comparison may show the result is a direct corollary of existing work.

**Does the attack break a deployed SG-DIFRA KEM?** No complete active NCSG-only KEM exists. The tests concern controlled finite constraint systems and a specially constructed nonuniform family, not an independently sampled full-size KEM distribution.

**Does small quotient dimension imply easy recovery?** Yes for this precise *explicit-table* model when that dimension is logarithmic in encoded input size and can be computed from the public tables. It does not extend automatically to succinct oracles, hidden scopes, or unknown factor functions.

**Why isn't this proof-assistant verified?** The written proof and tests exist; no Lean/Rocq/Isabelle checker has verified the formal statement in this execution.

**What's the next substantive problem?** Establish whether the proposed global distribution generically has a small exploitable quotient, or shift attention to mathematical structures with a credible *genuinely private* recovery advantage and originality evidence, rather than repackaging known symmetries.


## NG-Q4 and NG-Q5 in three levels

**Level 1 — tiny everyday picture.** Imagine one person trying to slide every connected puzzle piece in a particular direction without changing how the puzzle behaves. For one randomly mixed three-input ternary piece, any particular nonzero slide survives with probability **5 out of 39**. Several independently mixed puzzle pieces must all accept that same slide; the chance gets smaller when the slide touches more pieces. Having almost no successful slides is **not** the same as having an unsolvable puzzle—another kind of shortcut may exist.

**Level 2 — university mathematics.** Let `D=C(F)` be the global constant-derivative subspace for `F=(f_i)`; for a fixed nonzero shift `h`, `P(h in D)=alpha^(k(h))` where `k(h)` counts factors with nonzero restricted input shift. Summing indicators gives `E(|D|-1)=sum_(h!=0)alpha^(k(h))`; because any nontrivial F3-subspace contains at least two nonzero vectors, `P(D!={0})<=E(|D|-1)/2`. The expression is a support-hit hypergraph polynomial evaluated at `alpha`. Its complement representation uses induced subhypergraph edge counts, making the polynomial a familiar enumerator in different notation.

**Level 3 — critical research defense.** The local alpha formula relies on independent uniformly sampled invertible masks and independent uniform potential tables, not an arbitrary source sampler. The all-triple global result is strong only for its dense independent-factor ensemble and does not speak to average-case planted witness hardness or post-quantum KEM security. The primitive techniques—linear structures and first moments—are established in earlier published mathematics. NG-Q5 has an explicit graph-polynomial equivalence; a new mathematical framework **has not emerged**. The correct deliverable is an openly scoped negative/structural cryptanalytic result.
