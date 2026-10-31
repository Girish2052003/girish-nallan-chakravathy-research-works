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


## New result NG-Q6 / NG-Q7 — explain in three levels

**Level 1 (absolute beginner).** You hide one answer inside lots of little overlapping number puzzles. Many little puzzles can make the answer **the only possible answer**. But that does not make it secret! The attacker can compare the allowed number pairs in every public puzzle, cross out pairs that contradict other puzzles and sometimes read the complete answer without any secret key. A unique answer is not necessarily a difficult answer.

**Level 2 (university mathematics).** For independently randomized `f_i=A_i u_L+Delta_a Q_i(u_R)`, a fixed pair of distinct local inputs collides with exact probability `beta=(3^d-1)/(3^(r+d)-1)`. For a fixed independently planted global `s`, the expected number of alternative witnesses is `sum_(h!=0)beta^(k(h))`. For complete-triple scopes this becomes a Hamming-weight sum; Markov gives a non-uniqueness bound. Public pairwise projections of each factor's target fiber can then be repeatedly intersected. The procedure is sound and terminates in polynomial explicit-input time, although not proven complete.

**Level 3 (research defense).** The uniqueness theorem is a model-specific first-moment result, not cryptographic one-wayness. The public consistency attack successfully finds solutions in all tested dense n>=6 cases, even though global additive shifts were empirically zero in the same instances. Generic CSP consistency is established prior art (Mackworth, 1977). We have not proved asymptotic public success for this ensemble, established any secure KEM interface, justified a quantum hardness assumption or discovered a new foundational mathematical framework. We reject extrapolating from 'high width + no shifts + unique witness' to post-quantum security.


## NG-Q8 — three levels

**Beginner:** Imagine a secret answer to a huge number puzzle. Every three-number puzzle is shown publicly. For a particular wrong guess about **two** numbers, one random little puzzle has a 15-in-52 chance of ruling out that wrong guess completely. If enough *independent* puzzles contain the same two numbers, the chance of the wrong guess surviving all of them keeps shrinking. Eventually an outsider can determine every pair of secret numbers just by crossing out impossible choices. **Lots of overlapping puzzles did not protect the secret.**

**University:** Over F3, each local scalar NCSG source factor is `f(x)=A(Bx)_L+Delta_(1,0)Q((Bx)_R)`. Conditional on a fixed planted x, a false two-coordinate pair survives one independent local target-fiber projection with exact probability `p=37/52`. For a fixed 3-uniform public hypergraph and pair codegrees d_ij, the union bound over eight wrong possibilities per pair gives one-pass public recovery probability at least `1-min(1,8 sum_(i<j) p^d_ij)`. Uniform independent B,Q generation is essential.

**Research defense:** The exact constant relies on a 624-case GL3 finite orbit count and independently checked affine-linear images of 9-entry potential tables. It is a **narrow model-specific polynomial-time *attack***, not an average-case hardness theorem, new algebraic structure, quantum security guarantee or KEM. Existing CSP consistency and modern planted CSP recovery research require accurate credit (Mackworth 1977; Basu et al. ICALP 2026). No genuine private trapdoor survives the analyzed high-pair-codegree distribution. Novelty, external proof review and cryptographic redesign remain open.


## NG-Q9 bigger local puzzles in easy language

**Beginner:** Even if each little puzzle now uses more than three numbers, there is some chance—sometimes **very tiny**—that one publicly visible puzzle rules out a particular wrong guess about two numbers. If enough independently created puzzles overlap on those two numbers, the bad guess has fewer and fewer places to hide. But for puzzles of only **two** numbers, having one puzzle per pair does not create more checks on that same pair as the system grows. We must count how many independent checks each pair actually gets.

**University:** For fixed r,d>=1, the event that uniform Q has globally constant `Delta_a Q` has probability `3^(-r*(2*3^(d-1)-1))`. On this event `f` is affine with a uniform full-row-rank linear map L. Exact rank-matrix counting gives positive gamma that a wrong pair difference is outside L of the free (k-2)-dimensional subspace. Product epsilon>0 lower-bounds false-pair rejection, and a pair-codegree union bound gives polynomial public recovery at sufficiently high overlap.

**Defense:** This is a *lower-bound attack event*, not an exact general local probability or a proof of hardness. A tiny epsilon may make the asymptotic theorem practically irrelevant at feasible n. One distinct factor per k-subset has growing codegree only for k>=3. The result does not prove the nonexistence of every private trapdoor, and the mathematical machinery has established prior art.
