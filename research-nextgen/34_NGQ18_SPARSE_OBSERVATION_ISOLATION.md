# NG-Q18 — Sparse public observations: exact isolated-vertex obstruction

**Research date:** 1 November 2026. **Status:** Classical Erdős–Rényi random graph moments and a basic gauge-information obstruction, exact rational finite checks, six locally passing tests. **Not a new random-graph theorem, new one-way function, or KEM security guarantee.**

## 1. Why this is a necessary countercontrol to NG-Q16

NG-Q16 proves public exact relative-label reconstruction under sufficiently informative, independently corrupted dense ratio observations. **Without enough observed edges**, there may be no mathematical information about the relative group offset between distinct connected components, even if every observed edge is correct and group operations are free.

Assume n>=2 vertices, each with an independently uniformly sampled finite-group secret X_i. For every unordered potential edge, reveal it independently with probability `p`, forming an Erdős–Rényi observation graph `G(n,p)`. If present, its relative label may be exact or corrupted by a ratio-only observation channel; missingness is independent of X. For any observed disconnected graph, NG-Q17.2 proves that a cross-component ratio `X_u^-1 X_v` is still uniformly distributed even after conditioning on **all** observed public labels and the graph.

Thus **the mere presence of an isolated vertex is an information-theoretic obstacle to reconstructing all cross-vertex ratios**, not proof that the instance forms a computationally hard cryptographic problem. One could still output an arbitrary gauge-compatible *guess*, but it cannot recover the true uniformly random cross-component value with probability better than 1/|G| from that data alone.

## 2. Theorem NG-Q18.1 — exact finite first and second moments

Let `I_i` indicate that vertex i is isolated, and `X=sum_i I_i` count isolated vertices. Then, for 0<=p<=1,

`mu=E[X] = n*(1-p)^(n-1)`,

`E[X²] = n*(1-p)^(n-1) + n*(n-1)*(1-p)^(2n-3)`,

and therefore

`Var(X) = mu + n*(n-1)*(1-p)^(2n-3) - mu²`.

**Proof:** A fixed vertex is isolated when all n-1 incident independent edges are missing, probability (1-p)^(n-1). Two distinct vertices are both isolated when every edge incident on either is missing: 2(n-1)-1=2n-3 **distinct** edge-absence events, so `E[I_i I_j]=(1-p)^(2n-3)`. Expand `X²=sum_i I_i+sum_(i != j) I_i I_j` and subtract (E[X])². QED.

## 3. Theorem NG-Q18.2 — explicit isolation and non-identifiability probability

For `mu>0`, Chebyshev's inequality gives

`P[X=0] <= Var(X)/mu²`.

Consequently

**`P[at least one isolated vertex] >= max(0,1-Var(X)/mu²)`.**

This is a finite-n *lower bound* on an information-theoretic **non-identifiability event**, under the independent graph sampler. It is **not** a computational hardness statement.

At n=200, p=1/100, exact rational arithmetic gives

- `E[X] ≈ 27.066600981406456` isolated vertices.
- `P[at least one isolated vertex] >= 0.9580035924814697`, using the conservative Chebyshev bound.

For n=100, p=.01 the bound is >= .9729532096383526; for n=500,p=.01 it is >= .6905714847234732; these are separate finite regimes, not a monotonic-in-n claim at fixed p.

## 4. Asymptotic obstruction in the standard low-density regime

When `p_n <= (1-delta)*(log n)/n` for a fixed delta>0 and sufficiently large n, we have `mu_n = n(1-p_n)^(n-1) >= n^(delta+o(1)) -> infinity`, while

`Var(X_n)/mu_n² = 1/mu_n + (1-1/n)/(1-p_n) - 1 -> 0`

(assuming `p_n -> 0`, as holds in this regime). Hence `P[X_n>=1]->1`. With overwhelmingly likely isolation, cross-component relative labels remain unidentifiable under independent uniform secret priors.

This is a textbook part of the **Erdős–Rényi connectivity threshold at log(n)/n**; it is not original SG-DIFRA mathematics. The displayed variance expression is exact, and the asymptotics need no new assumptions beyond the stated observation model.

## 5. Reproduction and independent checks

Source: `research-nextgen/experiments/ng_q18_sparse_observation_no_go.py`, Git blob `5805c9d2701f9decc85d8c7523fa0ed65a9cb857`. Tests: `test_ng_q18_sparse_observation_no_go.py`, Git blob `685cfdb448ff81688898d8955fbec3ab6710dc08`.

Six locally passing tests include:
- Exact n=2 isolation distribution and variance, including p=0 and p=1.
- **All eight** possible simple graphs on three vertices, enumerated and weighted by p=2/5, matching exact first and second moments.
- Exact rational bounds over n=5,20,100 with several densities and endpoint controls.
- Conservative explicit isolation probabilities for n=200/500.
- Twenty seeded G(200,1/100) samples, verifying a high observed frequency of isolated vertices (empirical diagnostic only).
- Invalid inputs rejected.

```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q18_sparse_observation_no_go
python ng_q18_sparse_observation_no_go.py
```

The combined NG-Q16/17/18 suite passed **24/24 local tests**; the six final Python code/test files were committed byte-identically as verified by Git blob SHA. No proof assistant or independent human reviewer.

## 6. Prior art and revised cryptographic research gate

Classic Erdős–Rényi graph connectivity and isolation thresholds use precisely these first/second moments. See Rick Durrett, *Random Graph Dynamics*, Chapter 2, section 2.8, https://sites.math.duke.edu/~rtd/RGD/RGD.pdf; see also Sebastien Roch's course notes on Erdős–Rényi connectivity threshold, https://people.math.wisc.edu/~roch/teaching_files/833.f14/mdp-chap2-web.pdf. **Bradley Stich**, *Strong Recovery In Group Synchronization* (2023), https://scholar.rose-hulman.edu/rhumj/vol24/iss1/2/, explicitly studies positive dense and negative sparse group synchronization regimes.

**Disposition:** A sparse public observation graph may prevent recovery of global relative group offsets for purely *information-theoretic reasons*. This does **not** make sparse noisy group synchronization a new foundational mathematical construction or a viable secret-only inversion trapdoor. Any future cryptographic design must prove legitimate encapsulation correctness and indistinguishability within a fully specified scheme, not merely point to absent information or disconnected edges.


**Latest NG-Q16–Q18 check (1 November 2026):** In addition to the earlier 22 passing tests, two new independently implemented NG-Q16 tests verify all 36 S3 noise-label pairs with exact rational probabilities and explicitly falsify extension of the two-hop identity to non-flat group transport. **Final total: 24/24 locally passing tests (11 NG-Q16, 7 NG-Q17, 6 NG-Q18).** Updated executable test Git blob: `830c0c9c196c901906aa6297cadd442f66cebbaf`. No machine-checked proof or external review.
