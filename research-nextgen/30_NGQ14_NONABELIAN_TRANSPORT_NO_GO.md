# NG-Q14 — Nonabelian graph transport is public conjugacy, not a private trapdoor

**Research date:** 1 November 2026. **Status:** Exact conventional algebraic proof, explicit deterministic public inversion, 10 locally executed tests including independent exhaustive small-group enumeration. **Not a new mathematical foundation, machine-checked proof, independently peer-reviewed result, or functioning KEM.**

## 1. Precise mathematical model

Let G be **any group**, possibly nonabelian. Let V be the vertices of an arbitrary finite graph; each *oriented* public edge e=(u,v) has two public group labels H_e and B_e. The proposed secret is a vertex assignment (x_v) in G^V satisfying

`B_e = x_u^(-1) H_e x_v.`

Reversing e replaces both edge labels by their inverses. Parallel edges are permitted. The attacker knows V, all edges, H_e and B_e and the group representation; it knows no x_v.

This candidate is mathematically **distinct** from scalar finite-difference NCSG and nonassociative Latin-square isotopy; however it fits **existing nonabelian gain-graph/switching and group-synchronization theory** (see prior art below).

## 2. Theorem NG-Q14.1 — exact spanning-tree reduction

In any connected component, select a root r and a public spanning tree T. Let H_v (respectively B_v) be the ordered product of H edge labels (respectively B labels) on the oriented tree path from r to v, using inverses when traversing an edge backward. Then an assignment satisfies all *tree* edges if and only if, for some freely chosen t in G,

`x_v = H_v^(-1) t B_v` for every v,

where t=x_r. For any remaining edge e=(u,v), define public fundamental-cycle gains

`C^H_e = H_u H_e H_v^(-1)`, `C^B_e = B_u B_e B_v^(-1)`.

The assignment extends to **all** edges precisely when

`C^B_e = t^(-1) C^H_e t` for every non-tree edge.

**Proof:** Along a tree path, adjacent equations telescope without commuting any factors, yielding `B_v=x_r^(-1) H_v x_v`. Solving for x_v gives the stated formula and satisfies all tree edges. For an arbitrary e, substitute these expressions into `B_e=x_u^(-1) H_e x_v`, multiply on the left by B_u and right by B_v^(-1), and simplify to obtain the simultaneous conjugacy condition. Each step is reversible. QED.

Consequently the entire hidden-vertex recovery problem is reduced to **one group variable per connected component**, subject to simultaneous conjugacy constraints on its fundamental cycles. The number of independent non-tree edges in a connected undirected simple graph is `m-n+1` (parallel edges count separately); tree-edge constraints reduce to identities.

## 3. Theorem NG-Q14.2 — exact cardinality and common centralizer

Assume a connected component's public conjugacy constraints have at least one solution t0. Let

`Z_G(C^H) = {c in G : c C^H_e = C^H_e c for every non-tree edge e}`.

Then the complete set of possible component root values is exactly `Z_G(C^H) t0` and the complete set of **vertex assignments** has cardinality `|Z_G(C^H)|`. With no satisfying root the graph has no satisfying assignment. For several independent components, multiply their per-component cardinalities.

**Proof:** Every c in Z_G(C^H) gives a root c t0 with `(ct0)^(-1) C^H_e (ct0)= t0^(-1) C^H_e t0=C^B_e`. Conversely, if t is any satisfying root, then `t C^B_e t^(-1)=C^H_e=t0 C^B_e t0^(-1)`, so `t t0^(-1)` centralizes all C^H_e. Thus t=c t0 with c in the common centralizer. By the tree path formula, distinct roots give distinct full vertex assignments and there is no other freedom. Distinct graph components have independent constraints, proving the product statement. QED.

**Special case:** If all H_e are identity, `C^H_e=1` for every cycle. Either some C^B_e is nonidentity and the instance is inconsistent, or all are identity and every t in G works. In the latter case the secret is recoverable up to the inevitable simultaneous left-multiplication symmetry. The loss of a unique original secret does **not** mean the public equations are hard to solve.

## 4. Exact S3 counterexamples

Using the six permutations in S3, let `a=(01)` and `c=(012)`, which do not commute. Put identity public H labels on a 4-vertex spanning tree and put a and c on two non-tree edges. Generate matching public B labels from a chosen secret x.

- A tree only: no cycle conditions; **6** possible secret assignments.
- One cycle constraint with H gain a transposition: centralizer size **2**.
- Two independent cycles with gains a and c: their common centralizer is trivial, so **exactly one** full secret assignment survives. The deterministic public method recovers precisely the planted secret.
- One cycle whose H gain is a transposition and B gain is a 3-cycle: these have incompatible conjugacy classes, so **zero** solutions.
- Two disconnected tree components: exact solution count **6*6=36**.

**Lesson:** Noncommutativity and even the *uniqueness* of the hidden secret do not imply secrecy or hard inversion. These statements are straightforward consequences of public group operations and centralizer algebra.

## 5. Reproducible algorithm and testing

`experiments/ng_q14_nonabelian_transport.py` implements group multiplication for explicit permutations, BFS forest path labels, all chord-cycle constraints, finite S_k root enumeration (k<=6 in the reference implementation), complete verified witness recovery, inconsistency and exact solution counts. It is **polynomial in explicit finite group order |G|**, not in succinct permutation degree k, because S_k has k! elements; do not extrapolate this implementation to large S_k.

`experiments/test_ng_q14_nonabelian_transport.py` contains **10 locally passing tests**: S3 noncommutativity and centralizers, public flat-gauge count, unique-root noncommuting example, two-root single-chord case, inconsistent conjugacy, false flat label, disconnected component count, 40 random planted S3 fixtures compared against brute-force *all* assignments, random S4 witness checks and malformed input rejection.

**Exact final Git blobs matched to locally executed code:**
- `ng_q14_nonabelian_transport.py` — `426c00561012c82e9a8cb4dbe11e3a7fe894eafe`
- `test_ng_q14_nonabelian_transport.py` — `fa3db43fb57fc09884732e518d9839a8ab7c3454`

## 6. Prior art, originality and security limits

The mathematical vocabulary of **gain graphs**, *balanced graphs*, *switching equivalence*, *spanning-tree normalization* and *nonabelian cycle holonomy* predates this project. For example, *On cospectrality of gain graphs* (2022), DOI [10.1515/spma-2022-0169](https://doi.org/10.1515/spma-2022-0169), explicitly discusses tree balancing and nonabelian switching/cycle conjugation. Bradley Stich, *Strong Recovery in Group Synchronization*, Rose-Hulman Undergraduate Mathematics Journal 24(1), 2023, https://scholar.rose-hulman.edu/rhumj/vol24/iss1/2/, studies related recovery under noisy observations.

The group transport derivation is therefore an auditable **rejection of a tempting cryptographic premise**, not a certification of original mathematics. Generic group enumeration is not a cryptographically viable universal attack in succinctly represented groups. The stronger polynomial result for *full symmetric groups* with explicit permutations is developed separately in NG-Q15.

**Disposition:** REJECT noiseless public nonabelian transport labels alone as a basis for a private vertex-inversion trapdoor. A different, rigorously specified mathematical problem is necessary; simply adding noncommutativity does not meet the originality or hardness gates.
