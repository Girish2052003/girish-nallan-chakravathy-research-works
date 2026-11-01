# NG-Q12 — Exact finite-difference image and equivalent public local coordinate recovery

**Status:** Conventional exact finite-field proof; six locally executed unit tests including exhaustive 19,683-potential enumeration; no proof assistant or independent peer review. **Not a new foundational mathematical theory, universal multivariate key-recovery theorem or completed KEM break.**

## Precise local source model

Work over F3 with local scalar map `f:F3^3 -> F3` given by

`f(x)=A u_0+Q(u_1+1,u_2)-Q(u_1,u_2)`, `u=Bx`,

where `A in {1,2}`, `B in GL(3,3)`, and `Q:F3^2->F3` is an arbitrary nine-entry potential table. Only the full 27-entry public truth table f is given to the attacker. The coordinate matrix B and Q may be secret, but no other cryptographic protocol or global generator is specified.

This is the **fixed arity** r=1,d=2 source form with right difference direction (1,0); it is not a proof about every other NCSG variant.

## Lemma NG-Q12.1 — exact image and kernel of the public finite difference

Define `(Delta Q)(z,w)=Q(z+1,w)-Q(z,w)`. Its image is **exactly** the six-dimensional F3-vector space

`H={g:F3^2->F3 : for each w, g(0,w)+g(1,w)+g(2,w)=0}`.

It has 3^6=**729** elements. Its kernel is the three-dimensional space of Q constant along each three-cycle of z; there are 3^3=**27** kernel elements. For fixed B and fixed nonzero A, the 3^9=19,683 potential tables therefore produce exactly 729 distinct f functions, each with 27 potential-table representatives.

**Proof:** Telescoping the three differences around z=0,1,2 gives zero, so every image function lies in H. Conversely, for any g in H define, independently for each w, `Q(0,w)=0`, `Q(1,w)=g(0,w)`, and `Q(2,w)=g(0,w)+g(1,w)`. Then `Delta Q=g` at z=0,1; at z=2 the H sum-zero constraint gives `Delta Q(2,w)=g(2,w)`. All solutions Q differ by an arbitrary constant independently on each of the three w-cycles. B is invertible and A fixed, so the map g→f is injective. QED.

## Theorem NG-Q12.2 — complete public equivalent local representation recovery

Given any complete public scalar table f:F3^3→F3, there is an explicit **deterministic** algorithm which either returns a triple `(B',A',Q')` of the specified source form satisfying the table at all 27 inputs or correctly declares that no representation exists in this precise model.

**Algorithm and proof:** Enumerate every inverse coordinate change `C=B'^(-1) in GL(3,3)`, of which there are exactly

`|GL(3,3)|=(27-1)(27-3)(27-9)=11232`.

Define `h(u)=f(Cu)`. For each of the nine fixed right coordinates (z,w), calculate `h(0,z,w)`, `h(1,z,w)`, `h(2,z,w)`. A valid representation must have the same nonzero `A'=h(1,z,w)-h(0,z,w)` for every (z,w) and satisfy `h(2,z,w)=h(0,z,w)+2A'`. Put `g(z,w)=h(0,z,w)`; it must satisfy the three cycle-sum constraints of NG-Q12.1. If these conditions pass, integrate g publicly to Q' using the explicit cycle construction above, calculate B'=C^(-1), and **verify the entire original public table**. Return the first verified triple.

Any generated f has its actual C among the 11232 candidates and therefore passes. Conversely, if all candidates fail, no representation exists: every valid B' has its inverse in the enumerated set and would have satisfied the conditions. Every accepted reconstructed triple is verified against all public values, so soundness and completeness are exact. This is a constant-size local exhaustive algorithm—at most 11232 candidate transforms and 27 table lookups per candidate plus fixed-size checks. **Do not extrapolate its practical complexity to growing k or succinct function representations.** QED.

A returned B',A',Q' may differ from the originally planted generator parameters: **equivalent local generator recovery is not the same as original secret-key recovery**. Global shared parameters and a KEM secret were not modeled.

## Theorem NG-Q12.3 — stronger local public membership distinguisher

For a uniformly sampled scalar function U:F3^3→F3 (27 independent uniform outputs),

`Pr[U belongs to the above source-form family] <= (11232*2*3^6)/3^27 = 832/387420489 ~=2.1475374267e-6`.

**Proof:** For each of the 11232 choices of B and two nonzero choices of A, NG-Q12.1 allows exactly 729 functions. Counting all parameter representations gives at most 11232*2*729 distinct functions; some functions may admit more than one B or A and are consequently counted more than once. Divide this upper bound by the uniform function space size 3^27. QED.

This is an **upper bound**, not an exact membership probability. It is stronger than the earlier NG-Q11 degree<=3 uniform random false-positive probability 1/59049, but the comparison is between two different local predicates. No IND-CCA or key secrecy conclusion follows merely from public distinguishability.

## Executed finite checks

Source `research-nextgen/experiments/ng_q12_public_coordinates.py`, exact Git blob SHA `f02c2af18877832520b8e5cba14fd28b5da2d56a`. Independent tests `test_ng_q12_public_coordinates.py`, SHA `0c930f22ffa50cd4b1d44f5bbd1d215376e7bdb5`.

Six local unittest methods passed: exhaustive 11232 distinct invertible matrices and sampled inverses; exhaustive all 19,683 potentials yielding precisely 729 different g tables with 27 preimages each; 15 random masked source forms with equivalent reconstructed generators and full-table verification; zero and 12 independently random nonsource functions rejected; exact fraction; malformed input rejection.

```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q12_public_coordinates
python ng_q12_public_coordinates.py
```

**Correction captured:** The first local enumeration draft used a redundant erroneous `all` test where an `any` test was intended when detecting dependent second rows. Its independent rank-3 filter still rejected dependent matrices and returned the correct 11232, but the redundant condition was fixed and all tests rerun **before** GitHub commit. No incorrect theorem or source output is retained.

No GitHub Actions run or formal assistant theorem checker was completed.

## Originality and security boundary

Hidden linear changes and equivalent secret keys have extensive prior art in the **Isomorphism of Polynomials (IP/IP1S)** literature. Compare Fouque, Macario-Rat, Stern, *Key Recovery on Hidden Monomial Multivariate Schemes*, EUROCRYPT 2008, DOI 10.1007/978-3-540-78967-3_2; and *On enumeration of polynomial equivalence classes and their application to MPKC*, Finite Fields and Their Applications 18(2), 283–302 (2012), DOI 10.1016/j.ffa.2011.09.001.

The small-NCSG-family exact counts are a **scoped application** of linear-algebraic finite differences and exhaustive group-coordinate search, not proof of an original foundational algebra or a generalized hidden-polynomial-isomorphism attack. Fixed-size public table enumeration is not an asymptotic quantum or security claim.

**Decision:** Do not promote scalar three-input hidden B/A/Q parameters alone as a viable private-local-trapdoor premise when the entire 27-entry local function is public. A future KEM would require an independently justified secret and security game beyond these equivalent representations.
