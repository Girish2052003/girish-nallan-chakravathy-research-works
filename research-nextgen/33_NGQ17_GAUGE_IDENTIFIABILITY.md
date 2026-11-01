# NG-Q17 — Exact gauge non-identifiability alongside public relative recovery

**Research date:** 1 November 2026. **Status:** Conventional symmetry/information theory, rigorous finite-group proof, exact rational posterior enumeration for toy S3 cases, 7 locally passing tests. **Not** a new cryptographic security proof or a new group-theoretic framework.

## 1. The subtle distinction

NG-Q14 and NG-Q15 recovered **some valid** hidden-vertex representation from exact public transport. NG-Q16 publicly recovers all relative group labels under independent corruption/erasure with a suitable guarantee. But a valid relative-label reconstruction may NOT identify the *original absolute planted vertex secrets*. This is a mathematically unavoidable ambiguity, not evidence of cryptographic hardness.

For **flat group synchronization** with observed ratios `R_ij=x_i^-1 x_j`, simultaneously left-multiplying all vertex secrets by an arbitrary `t in G` leaves every R_ij unchanged:

`(t x_i)^-1 (t x_j) = x_i^-1 x_j`.

If the observation graph has disconnected components, each component has its own independent left-multiplication symmetry, because no published edge joins the components. This symmetry remains under any corrupting channel whose likelihood depends **only on internal true ratios and the public missing-edge pattern**.

Important: the same global left-gauge transformation need **not** preserve arbitrary twisted NG-Q14 labels `x_u^-1 H_uv x_v` if t does not commute with H_uv. All NG-Q17 claims are deliberately scoped to the **flat H=identity ratio** model.

## 2. Theorem NG-Q17.1 — absolute gauge is information-theoretically unidentifiable

Let G be a finite group of cardinality M, and assume vertex secrets `X_0,...,X_(n-1)` are **independently uniformly sampled** from G. Publish any randomized observation D whose conditional distribution depends on X **only through the true pair ratios** `X_i^-1 X_j`, with any secret-independent erasure/noise randomness.

Then for any possible published D with nonzero probability and every g in G,

`Pr[X_0=g | D] = 1/M`.

Equivalently, `I(X_0; D)=0` and the conditional entropy of the original absolute root coordinate is exactly `H(X_0|D)=log_2 M` bits.

**Proof:** Define `Z_i=X_0^-1 X_i` for i>=1 and let `Z_0=e`. The map

`(X_0,X_1,...,X_(n-1)) <-> (X_0,Z_1,...,Z_(n-1))`

is a bijection on G^n. Since the X variables are independent uniform, the pair (X_0,Z_1,...,Z_(n-1)) is jointly uniform, hence X_0 is independent of Z. Every true relative label satisfies `X_i^-1 X_j=Z_i^-1 Z_j`, so the conditional distribution of D depends only on Z. Thus D is independent of X_0. Bayes' rule gives the claimed exact posterior uniformity. QED.

**Attacker interpretation:** Recovering every ratio (or a canonical witness with `Z_0=e`) can be **easy**, while recovering the originally sampled X_0 is **information-theoretically impossible** from D alone. This does not make X_0 a valid public-key KEM trapdoor: a public-key encapsulator would need a defined way to derive the same shared key, plus correctness and IND-CCA/QROM reductions, none of which is established here.

## 3. Theorem NG-Q17.2 — relative offsets between components remain uniform

Let the observed graph (the graph of actually present public edges, including potentially corrupted values) have c>=2 connected components, and let X_v be independent uniform G. Assume the observation graph's inclusion pattern is independent of the hidden X and each observed label depends only on true vertex ratios within its own component, with independent noise.

Then, conditional on the full public data D, for any vertices u,v in **different** observed components,

`Pr[X_u^-1 X_v = g | D] = 1/M` for all g in G.

**Proof:** Parameterize each component C by its own root T_C and gauge-normalized internal coordinates Z_v=T_C^-1 X_v. Under the uniform independent prior, the component roots `T_C` are independent uniform and independent of all within-component normalized coordinates. Public data only concerns within-component ratios and the secret-independent graph pattern, so the component roots remain conditionally independent uniform after observing D. For u in C, v in D different components,

`X_u^-1 X_v=Z_u^-1 T_C^-1 T_D Z_v`.

The relative component root `T_C^-1 T_D` is uniform G even conditional on all public data and all within-component Z. Left/right multiplication by fixed Z_u^-1,Z_v preserves uniformity. QED.

**Noiseless exact solution count:** If an observed graph with c components has completely consistent exact pair ratios, and G is finite, there are exactly `|G|^c` original vertex assignments consistent with those ratios (choose one arbitrary root per component). Modulo one global left gauge, there remain `|G|^(c-1)` relative component-gauge alternatives. These counts concern assignments to exact equations, not noisy maximum-likelihood solutions.

## 4. Exact independent finite posterior checks

Source: `research-nextgen/experiments/ng_q17_gauge_nonidentifiability.py` (Git blob `bfce4036ec96e9a540b5b30c69e91d61d4150347`). Tests: `test_ng_q17_gauge_nonidentifiability.py` (blob `b9c268bc24de3cc1dbccafd615778029bddb21c4`).

Seven passing methods test:
- Exhaustive 6^3=216 equiprobable secret triples over S3 with missing and corrupted public data; root posterior **1/6 at each of six permutations**, in exact `Fraction` arithmetic.
- The same uniform original-root ambiguity with **every true relative label published perfectly**.
- Two disconnected S3 components with four secret vertices: every cross-component relative label has posterior exactly **1/6**, even with perfect internal ratios.
- The same cross-component uniformity with nonzero replacement noise and erased external edges.
- Public likelihood invariance under independently left-multiplying entire observed components.
- Two distinct absolute vertex assignments producing the **identical complete true relative table**.
- Malformed graph/likelihood inputs rejected.

The exhaustive exact posterior tool runs on toy S_k with k<=4 and n<=5 because its `(k!)^n` cost is exponential; it verifies the proof on finite examples, **not** a polynomial attack. The actual theorem applies to any finite G under its explicitly uniform independent prior.

Combined NG-Q16/Q17/Q18 local suites passed 24/24 methods, with source bytes matched to GitHub content hashes. No CI, proof assistant or external reviewer.

```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q17_gauge_nonidentifiability
python ng_q17_gauge_nonidentifiability.py
```

## 5. Scientific classification and prior art

These exact group-action invariances, gauge choices and component decomposition are standard in group synchronization, spanning-tree switching and statistical identifiability theory. Relevant established literature includes **Lerman and Shi**, *Robust Group Synchronization via Cycle-Edge Message Passing* (2022), DOI 10.1007/s10208-021-09532-w, and **Bradley Stich**, *Strong Recovery In Group Synchronization* (2023), https://scholar.rose-hulman.edu/rhumj/vol24/iss1/2/.

**Verdict:** Do not equate an absolute hidden gauge with a new private trapdoor or computational cryptographic security. Conversely, do not equate successful public relative recovery with identifying an arbitrary secret root. Public relativity can be computationally easy while the arbitrary absolute gauge remains perfectly statistically hidden. Both statements can be simultaneously true without any secure KEM construction.


**Final testing addendum (2026-11-01):** The exact NG-Q16 S3 two-hop noise-distribution test and non-flat-H negative control passed, raising current NG-Q16 from 9 to 11 tests and current NG-Q16/17/18 combined execution from 22 to **24 passing tests**. Updated test blob SHA `830c0c9c196c901906aa6297cadd442f66cebbaf` matches local execution. No proof assistant or external review.
