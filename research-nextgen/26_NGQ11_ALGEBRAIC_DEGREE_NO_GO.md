# NG-Q11 — Finite-difference algebraic degree collapse and public linearization

**Date:** 1 November 2026. **Status:** Conventional written proofs, independent finite enumeration and public recovery code. **Not** a newly invented algebraic theory, machine-checked proof, reviewed cryptography or complete KEM.

## Exact model

Work over `F3`. Let `r,d>=1`, `k=r+d`, invertible `B in GL(k,3)`, `A in GL(r,3)`, nonzero `a in F3^d`, and an arbitrary map `Q:F3^d -> F3^r`. Given `x in F3^k`, put `u=Bx=(u_L,u_R)` with `r` left and `d` right coordinates. Define the publicly evaluable local source form

`f(x)=A u_L + Delta_a Q(u_R) = A u_L + Q(u_R+a)-Q(u_R)`.

No randomness, independence, secrecy, special distributions or planted witness assumptions are needed for the deterministic mathematical statements.

All public local function tables are assumed complete and accurate. The public solver does not receive the hidden generating `B,A,Q`.

## NG-Q11.1 — Deterministic algebraic-degree upper bound

Every output coordinate of f, represented by its unique reduced polynomial function over F3 with each input-variable exponent in {0,1,2}, has algebraic degree at most

`max(1,2d-1)`.

**Proof:** Each coordinate of any function `Q:F3^d -> F3` has a unique reduced polynomial of total degree at most `2d`. Translation `z -> z+a` preserves the highest-degree homogeneous term of any polynomial, and subtraction of the original polynomial cancels those highest-degree terms, decreasing total polynomial degree by at least one (possibly to zero). This proves `deg(Delta_a Q) <= 2d-1` in the original right coordinates. The term `A u_L` has degree one. Substituting the linear map `u=Bx` cannot increase total degree; reduction modulo `x_i^3-x_i` can only decrease it. Hence the asserted bound. QED.

**Prior art:** Algebraic-degree filtrations, affine-invariant function spaces and generalized Reed–Muller codes are well-established: Kaufman and Ron, *Testing Polynomials over General Fields*, SIAM Journal on Computing, DOI 10.1137/S0097539704445615 (https://epubs.siam.org/doi/10.1137/S0097539704445615), and standard generalized Reed–Muller code literature. The argument is an elementary application, not proof of foundational novelty.

## NG-Q11.2 — Entire d=1 ternary source-form family is publicly affine

If **d=1** (any r>=1), every local f is an **affine full-row-rank map** of its k=r+1 public inputs, regardless of the nonlinear-looking potential table Q and matrix B. In particular, f is `Mx+b` with `rank(M)=r`.

**Proof:** Any vector Q:F3->F3^r is represented by `Q(z)=c0+c1*z+c2*z^2` (componentwise). For any a!=0,

`Q(z+a)-Q(z)= c1*a+c2*(2*a*z+a^2)`,

which is affine in z. Thus `f(x)=[A | 2*a*c2] Bx + (a*c1+a^2*c2)`. Because A is invertible, the block `[A | 2*a*c2]` has row rank r, and multiplying by invertible B preserves its rank. QED.

**Global corollary NG-Q11.3:** Form any global system of explicit public local d=1 factors on arbitrary scopes of size r+1, including arbitrarily dense or high-treewidth overlap, and any target outputs. Stacking each public local equation gives **one public linear system `M_global*x=b_global` over F3**. Gaussian elimination either recovers a satisfying global witness or correctly proves the public target inconsistent, in polynomial time in public input size. Any original secret generating B,A,Q is unnecessary. For a planted target at least one witness exists. This is deterministic, not probabilistic, and it applies even if the factors are correlated or generated adversarially within the stated source form.

**Important limitation:** A recovered global witness is not necessarily the same planted witness if multiple solutions exist, and without a specified KEM one cannot infer IND-CCA breaking or decapsulation-key recovery.

## NG-Q11.4 — Exact public degree distinguisher for r=1,d=2

For `r=1,d=2,k=3`, every source-form f has degree <=3 regardless of B,A,Q. A uniformly random scalar function `U:F3^3->F3`, sampled by choosing its 27 output-table entries independently and uniformly, has degree <=3 with **exact probability 3^(-10)=1/59049**.

**Proof:** Every function on F3^3 corresponds uniquely to 27 reduced coefficients indexed by `(e1,e2,e3) in {0,1,2}^3`. The condition degree<=3 restricts the ten coefficients on monomials with total degree >=4 to zero; the remaining 17 coefficients are unrestricted. The evaluation-to-coefficient map is an invertible 27x27 linear transformation over F3, so a uniform function table maps to 27 independent uniform coefficients. Exactly `3^17` of all `3^27` functions have degree<=3, hence probability `3^-10`. Every source-form local function passes this test by NG-Q11.1. QED.

**Sharper exact source distribution:** For uniform `Q:F3^2->F3` and any invertible B, the source-form scalar has **degree exactly 3 with probability 2/3**. In coordinates `z,w`, the degree-3 component of `Delta_(1,0) Q` is `2*c_(2,2)*z*w^2`, where `c_(2,2)` is the reduced-polynomial coefficient on `z^2*w^2`. It is independent uniform over F3. An invertible linear change of variables preserves algebraic degree of a finite-field polynomial function (substitution never raises degree, and the inverse substitution gives the reverse inequality). Thus degree exactly 3 iff `c_(2,2)!=0`, probability 2/3. Exactly **13,122** of all **19,683** possible nine-entry scalar Q tables have degree-3 source forms for fixed A=1,B=I.

**Interpretation:** The predicate `degree(f)<=3` perfectly accepts the above source-form family and accepts a uniform random function with probability exactly 1/59049. This is a strong **local statistical distinguisher**, not inherently an encryption key-recovery attack. Being visibly structured is not by itself a proof that a cryptosystem is insecure.

## NG-Q11.5 — General arbitrary-output distinguisher count

For `k=r+d` and `D=max(1,2d-1)`, let

`M(k,D)=#{e in {0,1,2}^k : sum(e)<=D}`.

A uniform random vector-valued function `U:F3^k->F3^r` satisfies `degree(U_j)<=D` for every output component j with exact probability

`3^(-r*(3^k-M(k,D)))`.

Every source-form factor with the stated d,r satisfies these degree bounds. This claim compares explicit public local tables to **uniformly random full tables**; it says nothing about a pseudorandomness/security game using a distribution with publicly known structure.

## Exact executable checks

- Source: `research-nextgen/experiments/ng_q11_degree_collapse.py`, Git blob `3d8abc8e8fb952215d79f182b37a152eda9b465d`.
- Independent tests: `research-nextgen/experiments/test_ng_q11_degree_collapse.py`, Git blob `53d5f82c881201dc3f20db88919dd286e8732a64`.
- Locally executed with Python 3.13.5 Linux x86_64; **7/7 new tests passed**: interpolation identities k=1..4, 200 random d=1 factors of dimensions r=1,2, arbitrary global planted d=1 linear witness recovery, inconsistent target and nonlinear rejection, exhaustive all 19,683 Q tables with 13,122 degree-3 outputs, 200 random invertible masked r1d2 functions, and 3,000 independent uniform scalar functions as a negative control.
- Source and tests' Git blob hashes were matched to executed local files. **22/22** tests passed when combined with prior NG-Q8, NG-Q9 and new NG-Q10 suites.
- One development mistake was caught: the initial degree false-positive helper returned a floating-point power rather than an exact `Fraction`. The helper was corrected and full tests rerun before accepting the result.

```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q8_recovery test_ng_q9_general_bound test_ng_q10_public_star_no_go test_ng_q11_degree_collapse
python ng_q11_degree_collapse.py
```

**Status limitations:** Proofs are conventional, not Lean/Rocq/Isabelle checked. No independent external cryptanalysis or peer review; no novel algebraic foundation, trapdoor or complete KEM. Degree distinguishing and deterministic d=1 inversion are separate claims and must not be conflated.

## Scientific disposition

**Reject any d=1 ternary source-form public-factor witness-inversion hardness claim** under these explicit-table assumptions: public Gaussian elimination solves the whole problem regardless of width. **For d>=2**, a low-degree public invariant is established; this alone does **not** prove witness recovery easy. A genuinely independent mathematical research direction remains necessary. Existing affine/Reed–Muller mathematics takes priority over invented new terminology.
