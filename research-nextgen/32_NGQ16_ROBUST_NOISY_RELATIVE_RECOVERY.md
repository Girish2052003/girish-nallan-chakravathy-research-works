# NG-Q16 — Exact public two-hop recovery under corruption and erasure

**Research date:** 1 November 2026. **Status:** Conventional, scoped algebra/probability proofs plus 9 local tests. **Not** novel group synchronization, external peer review, proof-assistant formalization, an original hard problem or a KEM.

## 1. Model and representation

Let G be any **finite group** with an effective public representation of group elements, multiplication and inversion. Let n>=3 vertex secrets x_0,...,x_(n-1) be arbitrary fixed elements of G (or sampled independently, independently of observation noise). Define the true, gauge-invariant, PUBLIC-TARGET *relative* labels

`R_ij=x_i^(-1)x_j`, for every unordered pair i<j; the reverse direction is `R_ji=R_ij^(-1)`.

For each unordered potential edge independently: include it in the public observation graph with probability rho; if included, publish `Y_ij=R_ij` with probability `1-epsilon`, otherwise publish an **independently uniform G element** with probability epsilon. Random replacement can coincidentally equal the true label. All choices on different unordered edges are independent, and the observation/missingness mechanism is **secret-independent beyond the true ratio labels**.

This is the **flat H=identity relative-group** special case of NG-Q14/NG-Q15. It does **not** automatically apply to arbitrary non-flat twisted H_ij public transport: two-hop products need not equal a direct label when public base holonomy is nontrivial.

The attacker receives only publicly observed edges and their Y labels. It receives no x, no corruption flags and no actual true R labels.

## 2. Public algorithm NG-Q16.1 — two-hop plurality

For every pair (i,j), enumerate intermediary vertices h distinct from i,j such that BOTH public edges (i,h) and (h,j) are observed. Compute the public oriented product

`C_h(i,j)=Y_ih Y_hj`.

Count frequencies of candidate group elements and return its **unique plurality winner** for that pair, or mark the pair unresolved if no observed two-hop path or a plurality tie. Never use the possibly corrupted direct Y_ij value to vote for that pair; only the two-hop products count.

If all pairs have unique winners, combine `x_0^*=e`, `x_j^*=R^*_(0j)` for j>=1 and verify consistency `(x_i^*)^-1 x_j^* = R^*_(ij)` for **all** pairs. If any test fails, report *inconclusive*; otherwise return **self-consistent public gauge candidate**.

A self-consistent candidate is **not a proof that it equals the true planted x or the true R** without the separate probabilistic/deterministic hypotheses below. An adversary can replace every observed label by the identity and produce a wrong but perfectly self-consistent public instance.

Reference implementation: `experiments/ng_q16_robust_relative_sync.py`, with explicit permutation group element representation and group operations O(k) each for S_k; time O(n^3) public group operations and polynomial storage. No k! enumeration.

## 3. Theorem NG-Q16.2 — deterministic adversarial majority

On an arbitrary fixed observation graph and with **arbitrary adversarial corrupted labels**, suppose for EVERY pair (i,j), strictly more than half of its **observed two-hop paths** consist of two honest (uncorrupted) edges. Then the public two-hop plurality algorithm returns **every true relative R_ij** and a gauge-normalized vertex assignment `x_i^*=x_0^-1 x_i`. It never needs to know which edges were corrupted.

**Proof:** Any honest two-hop path has public product `R_ih R_hj = x_i^-1 x_h x_h^-1 x_j = x_i^-1 x_j=R_ij`, with no commutativity assumption. All remaining paths together contribute fewer votes than the honest paths. Therefore R_ij is the unique plurality winner for every pair, and the reconstructed canonical gauge is consistent. QED.

**Degree corollary for fully observed complete graphs:** Let d_bad(i) be the number of adversarially corrupted edges incident on vertex i. For each pair (i,j), at most d_bad(i)+d_bad(j) of the n-2 two-hop paths can contain a bad edge (a conservative union bound). Thus it suffices that

`d_bad(i)+d_bad(j) < (n-2)/2` for ALL pairs.

In particular, max bad degree `Delta < (n-2)/4` suffices. This guarantees exact *relative-label* recovery even when bad labels are maliciously chosen, for any finite group with effective operations; it makes no group-size assumptions.

**Missing edges:** The basic deterministic statement remains valid when some paths are unavailable; it counts **observed** two-hop paths and requires strict honest majority *among them*. The per-vertex degree corollary applies only to the complete observation graph.

## 4. Theorem NG-Q16.3 — independent random noise+erasure upper bound

Fix a group G of size M>=2, a true ratio R_ij, and a particular wrong g!=R_ij. For each intermediary h, define

`Z_h=1{C_h=R_ij}-1{C_h=g}` when both edges observed, else `Z_h=0`.

For h distinct, the two involved public unordered edges form disjoint edge sets. Thus `Z_h` are **independent** variables in [-1,1]. Conditional on both edges being included, the probability that neither edge was replaced is `(1-epsilon)^2`, and then C_h=R_ij. If at least one edge is replaced by a uniform G element, the product is exactly uniformly distributed over G, irrespective of the other edge or of noncommutativity. The uniform part has equal probability of matching R_ij or g. Consequently

`E[Z_h] = delta = rho^2 (1-epsilon)^2`.

Hoeffding's inequality on m=n-2 variables, each supported on an interval of length 2, gives

`Pr[count(g) >= count(R_ij)] <= exp(-(n-2)*delta^2/2)`.

A union bound over the M-1 alternative values and C(n,2) unordered pairs yields

**`Pr[at least one pair is wrong, tied, or unresolved] <= min(1, C(n,2)*(M-1)*exp(-(n-2)*rho^4*(1-epsilon)^4/2))`.**

Therefore, whenever the RHS is small, the algorithm recovers all true relative labels with the corresponding high probability; in particular for **fixed M and fixed rho>0, epsilon<1**, the bound vanishes exponentially in n apart from a polynomial prefactor. If M grows with n (e.g. M=k! for S_k), the bound requires the displayed quantitative condition; do **not** silently drop the M-1 factor. QED.

This is a mathematically elementary model-specific union bound, **not** the sharp robust synchronization threshold and not claimed novel.

## 5. Corollary NG-Q16.4 — group-size-independent random clean-majority bound

For each possible intermediary h, independently both incident edges are observed and **not replaced** with probability `q=[rho*(1-epsilon)]^2`. Under the stronger sufficient condition `q>1/2`, Hoeffding for clean-path indicators gives

`Pr[all true ratios NOT recovered] <= min(1,C(n,2)*exp(-2*(n-2)*(q-1/2)^2))`.

The inequality treats *unobserved* paths as non-clean, hence is conservative; any wrong-label coincidences further help the correct plurality. This bound is **independent of |G|**, and therefore remains meaningful for very large explicitly represented groups as long as n and q make its RHS nontrivial.

## 6. Countercontrols, local numerical evidence and scope

Eleven locally passing unit tests include:
- noncommutative permutation order and inverse correctness;
- exact recovery on every one of six planted S3 clean 4-vertex fixtures;
- an **adversarially corrupted S4 complete graph** with 32 vertices and exactly four corrupted edges incident to each vertex, satisfying the deterministic bound and recovering all true pairs;
- **three seeds** at n=90, S3, rho=1, epsilon=.36, all true pairs recovered;
- **three seeds** at n=90, S4, rho=.78, epsilon=.10, all true pairs recovered;
- all-public-labels-missing control correctly *inconclusive*;
- deliberately forged self-consistent but **false** group-ratio table, demonstrating why self-consistency cannot certify true-secret recovery;
- conservative finite bound checks and malformed-input rejection.
- **independent exhaustive 36-outcome S3 two-edge uniform-replacement probability**: at rho=3/4, epsilon=1/2, correct-path probability=27/128, each wrong-group outcome=9/128, exact true-vs-wrong advantage=9/64, matching the algebraic formula;
- **non-flat transport counterexample** with zero corruption but public H_01 H_12 != H_02, for which naive two-hop multiplication is provably incorrect, guarding the flat-only theorem assumption.

**Caution:** At n=90 the stated Hoeffding bound can still equal its trivial cap 1. The seeded n=90 successes are **experiments**, not a consequence of a nontrivial finite bound. As a separate illustration, for n=100, |G|=6, rho=.95, epsilon=.10 the analytic bound is approximately 1.0504267e-7; this is an upper failure bound under the stated independent sampler, not an observed frequency.

Source `research-nextgen/experiments/ng_q16_robust_relative_sync.py`, exact Git blob `f1a5562a1fdbf28c0323278db76a25af05d3ac66`. Independent tests `test_ng_q16_robust_relative_sync.py`, blob `830c0c9c196c901906aa6297cadd442f66cebbaf`. Both GitHub SHA values match exact locally executed bytes, and the combined new NG-Q16+NG-Q17+NG-Q18 suite passed 24/24 methods.

```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q16_robust_relative_sync
python ng_q16_robust_relative_sync.py
```

## 7. Prior art / cryptographic disposition

**Gilad Lerman and Yunpeng Shi**, *Robust Group Synchronization via Cycle-Edge Message Passing*, Foundations of Computational Mathematics 22 (2022), 1665–1741, DOI **10.1007/s10208-021-09532-w** (published online September 2021), https://link.springer.com/article/10.1007/s10208-021-09532-w, already proves robust exact recovery under adversarial and random corrupted group ratios using cycle information. **Shi, Wyeth, Lerman**, *Robust Group Synchronization via Quadratic Programming*, ICML/PMLR 162 (2022), https://proceedings.mlr.press/v162/shi22g.html, and further literature already explore recovery thresholds and cycle consistency. The special two-hop majority bound above is straightforward existing-style synchronization mathematics, NOT a newly discovered cryptographic hardness assumption or a stronger-than-prior-art general result.

**Scientific decision:** Adding independent erasures and replacement noise to a public **flat group-ratio** variant does not, by itself, supply a private inversion trapdoor, a new foundational mathematics, or a secure post-quantum KEM. Robust public relative-label reconstruction is explicitly achievable under stated conditions; the absolute vertex gauge is inherently unidentifiable, as NG-Q17 analyzes separately.
