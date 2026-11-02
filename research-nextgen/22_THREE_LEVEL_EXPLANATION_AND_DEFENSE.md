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


## NG-Q10 and NG-Q11 in three levels

**Level 1 — child-friendly:** The star puzzle had two middle numbers connecting to all other numbers. We thought many little puzzles could hide the answer, but an outsider needs to guess only **nine combinations** for those two middle numbers, then checks each remaining number separately. So we rejected it. Next we checked what a 'nonlinear-looking formula' really calculates. When there is just **one right-side input** in the ternary version, the apparent curve is actually a straight line after taking the finite difference! An outsider can solve all the public equations by ordinary algebra, even if the puzzle connections look complicated.

**Level 2 — student math:** For f=A uL+Delta_a Q(uR) over F3, any Q on d variables has unique reduced polynomial degree<=2d. Taking a finite difference decreases total degree by at least one, hence deg(f)<=max(1,2d-1). If d=1, Delta_a Q is affine and stacking public local equations yields a global linear system. If r1,d2, source local degree<=3; there are 17 reduced monomials of degree<=3 among 27, so uniform random scalar functions pass with probability 3^(-10).

**Level 3 — research defense:** NG-Q10 public star inversion is pre-existing treewidth-2 CSP conditioning, not new mathematics. NG-Q11 is an application of standard Reed–Muller/affine-invariant polynomial theory. d=1 permits deterministic public *witness* inversion for arbitrary scope graphs, but says nothing about deriving an unspecified KEM shared secret. The d=2 degree membership test only distinguishes a structured local source distribution from completely uniform function tables. 22 targeted tests passed after preserving two corrected test/prototype failures; no proof assistant or independent peer review.


## NG-Q12 and NG-Q13 — complete three-level explanation

**Baby level:** We hid the recipe for a little nine-part number puzzle. But the whole output table was public, so an outsider could try all possible small coordinate disguises and find a recipe that makes exactly the same puzzle. The recovered recipe need not be the original hidden one, but it works just as well. Next we invented an operation that *looked* nonassociative by hiding ordinary addition behind three secret shuffles. An outsider could unshuffle its publicly visible multiplication table and find a perfectly ordinary addition system underneath. We even tested a seven-element quasigroup that is **not** disguised addition; its public table still lets anyone solve one multiplication equation by looking at one row.

**University level:** For r=1,d=2, the difference `Delta_(1,0)Q` has image consisting of nine-entry g tables satisfying three independent cyclic zero-sum equations, so rank=6 and nullity=3. For any fixed invertible B and nonzero A, the scalar f family has size 3^6; enumerate 11232 B candidates and integrate Q on each cycle to reconstruct an equivalent generator. In the separate isotope T(x,y)=γ^-1(α(x)+β(y)), publicly normalize via row/column R,L to P(a,b)=T(R^-1(a),L^-1(b)), with γ(P(a,b))=γ(a)+γ(b)-γ(p). Public elementary abelian coordinates give an equivalent α',β',γ'.

**Research defense:** The first is fixed-arity explicit-table mathematics, not general efficient hidden-polynomial isomorphism in growing dimension, nor a complete KEM key-recovery theorem. The second is established quasigroup/group-isotopy theory. The Fano Steiner control proves non-isotopy but no computational hardness. New mathematical novelty and private-trapdoor security are still unsupported. **12/12 new tests**, plus conventional proofs; no CI, proof assistant, independent review or quantum security game.

## NG-Q14/NG-Q15 in three teaching levels

**Tiny example:** Imagine people at the corners of a network each hiding a colored shuffle of cards. Every line joining two corners publishes how those shuffles relate. The shuffles may not commute; doing them in different orders changes the answer. But if you follow a tree of lines, you can express every hidden shuffle using **one remaining unknown**. The extra loop lines are public checks on that unknown. With full ordinary permutations, those checks can be solved efficiently without trying every possible deck shuffle. Even when there is only ONE possible secret assignment, the outsider can still recover it.

**University:** Public H_uv and B_uv satisfy B_uv=x_u^-1 H_uv x_v in group G. Root-path products H_v,B_v give x_v=H_v^-1 t B_v, and non-tree edges require t^-1(H_u H_e H_v^-1)t=B_u B_e B_v^-1. Any root conjugator t0 generates a coset of the common centralizer; its cardinality counts full assignments. If G=S_k given by explicit permutations, solve simultaneous conjugacy by equivariant orbit matching of the A/D generator tuples. The algorithm is polynomial in k and graph size.

**Research defense:** This is gain-graph switching plus published symmetric-group simultaneous conjugacy, not new nonabelian geometry, an unconditionally hard problem, or any security reduction. Enumeration for a generic finite G can be exponential in succinct representation length; the polynomial theorem is specific to **full explicit S_k**. No noisy observations, KEM, or post-quantum parameter strength were checked. 18/18 newly executed local tests pass, but no outside reviewer or formal proof assistant verified the claims.


## NG-Q16/NG-Q17/NG-Q18 three levels — beginner to expert

**Beginner:** Imagine 100 friends each secretly choosing how to shuffle a deck. Each pair of friends publicly reports how their shuffles compare, but some reports are missing or wrong. If enough pairs have correct reports, an outsider can check many paths through other friends and **vote out the incorrect relationships**. If only two disconnected groups of friends report among themselves, nobody can know how the two groups' secret shuffles relate. And even when every relationship is known, everyone can still globally change their secret shuffles together without changing any relationship at all. That last ambiguity is not proof a secure encryption system has been invented!

**University:** On a finite noncommutative group G, the pair ratio is R_ij=x_i^-1 x_j. Independent observations Y_ij are included with prob rho and uniformly replaced with prob epsilon. Two-hop products Y_ih Y_hj are true on two honest edges and uniform if at least one is uniformly replaced. Comparing the true group label to a wrong one yields independent Z_h∈[-1,1] with E[Z_h]=rho²(1-epsilon)². Hoeffding+union bound gives failure <=C(n,2)(|G|-1)*exp(-(n-2)rho^4(1-epsilon)^4/2). Under iid uniform secret vertices, x_0 stays independent of all ratio data due to the free global left action. A disconnected observed graph gives per-component left gauges; G(n,p) isolation first/second moments quantify a frequent low-density obstruction.

**Research defense:** These are **known theory applications** with different mathematical meanings. NG-Q16's high-probability result is *algorithmic public ratio recovery* under a fixed noise model; no arbitrary non-flat twisted H extension. NG-Q17's posterior symmetry is information-theoretic *absolute gauge non-identifiability*, not a computational hardness claim. NG-Q18's low-density isolation is graph missingness, not NP-hardness or a private trapdoor. All 22 new targeted tests passed and source identities matched; prior art and proof-assistant/external-review boundaries remain explicit.


**Latest NG-Q16–Q18 check (1 November 2026):** In addition to the earlier 22 passing tests, two new independently implemented NG-Q16 tests verify all 36 S3 noise-label pairs with exact rational probabilities and explicitly falsify extension of the two-hop identity to non-flat group transport. **Final total: 24/24 locally passing tests (11 NG-Q16, 7 NG-Q17, 6 NG-Q18).** Updated executable test Git blob: `830c0c9c196c901906aa6297cadd442f66cebbaf`. No machine-checked proof or external review.


## NG-Q19: three explanation levels (2 November 2026)

**Level 1, little-child English:** Think of each person in a network secretly keeping a small square of numbers (a matrix), and each friendship line publishing how the two squares relate. Hiding the squares does not automatically secure them. A public detective follows enough friendship lines to express all hidden squares using **one remaining unknown square**, then writes ordinary add/subtract number equations to find possible answers. A random solution often works directly. If it does, the detective checks every friendship line publicly. So this attempted hiding trick is **not a new mathematical encryption secret**.

**Level 2, university:** In GL(k,Fp), B_uv=X_u^-1 H_uv X_v. A spanning tree yields X_v=H_v^-1 T B_v. Chords give A_e T=T D_e, a homogeneous k²-variable linear system. If its solution space contains an invertible T_0 and p>k, det(sum c_i W_i) is a nonzero degree-k polynomial, so uniformly random coefficients produce an invertible T with probability at least 1-k/p. N independent attempts fail with probability <=(k/p)^N. Nonzero vector space does not guarantee invertibility; the unipotent counterexample prevents false UNSAT claims.

**Level 3, research defense:** This is a graph-switching reduction to finite-field module isomorphism and known Schwartz–Zippel polynomial identity testing. The recovered matrix may be an equivalent witness, not the secret originally sampled. The p>k guarantee assumes an already validated prime field; Python's naive primality validator is not poly(log p). p<=k is not covered by the elementary guarantee, and separate published general module-isomorphism results are not reproduced. Twelve independent local tests and conventional proof do NOT establish original mathematics, quantum hardness, trapdoor or KEM IND-CCA.


## NG-Q20 explained in three levels — hidden word-product matrices

**Beginner:** Imagine two secret boxes with number rules. If you feed a sequence of letters (like 'abba') to the boxes, they secretly multiply number tables and return one number. If an outsider knows enough special examples, they can use ordinary school-table calculations to make a **new box that always gives the same answers**. But if the box says 1 for just ONE hidden word and 0 for every other word, finding that word by asking yes/no questions might take many guesses. Importantly: a public program must be inspectable, so simply assuming an opaque magic box hides its answer does NOT create an encryption system.

**University:** Finite-field recognizable f(w)=alpha M_w beta has Hankel H(u,v)=f(uv). If rank(H)=d and a full dxd minor H_(P,S) is supplied, equivalent transition matrices are N_a=H^-1 H_a; initial h_S and terminal H^-1 h_P. Equivalent outputs agree on all words, not just finite tests. The needle series 1_{w=u} at |u|=L has Hankel rank L+1 (identity Hankel block from prefixes/suffixes); q classical membership calls plus one guess succeed at most (q+1)/s^L for uniformly hidden u.

**Research-defense:** These are established weighted automata and query-model facts. Finding the full Hankel basis is **not included** in the polynomial reconstruction query count; a toy finder enumerates exponentially many candidate words. Classical membership-only needles are NOT practical post-quantum KEMs: no public-key encoding, no trapdoor, no security game, and Grover offers O(s^(L/2)) quantum search under coherent oracle access. Ten independent tests pass; no formal proof assistant, new mathematical originality or credible IND-CCA.
