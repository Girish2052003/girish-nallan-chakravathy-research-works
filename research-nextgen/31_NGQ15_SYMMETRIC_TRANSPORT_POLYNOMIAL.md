# NG-Q15 — Polynomial-time public vertex recovery for symmetric-group graph transport

**Date:** 1 November 2026. **Status:** Conventional constructive proof, complete algorithm, independent small-group exhaustive comparisons, and eight locally executed tests including S_100 cases. NOT new foundational mathematics, independent peer review, machine proof, or a secure KEM.

## 1. Definition and reduction

Use the NG-Q14 model for arbitrary publicly specified graph edges:

`B_(u,v) = x_u^(-1) H_(u,v) x_v`,

but now every secret x_v and every public H,B edge label is an *explicit permutation* of k points, in the **full** symmetric group S_k. Input size is polynomial in k,n and the edge count m (every permutation is a k-entry vector). No truth table of all k! permutations is given or required. k can grow.

By NG-Q14, in each connected component a BFS spanning tree produces public products H_v, B_v and public cycle permutation tuples `A_e=H_u H_e H_v^(-1)`, `D_e=B_u B_e B_v^(-1)`. All solutions correspond to roots t in S_k satisfying

`t^(-1) A_e t = D_e` for all e,

and then to the explicit vertex assignments `x_v=H_v^(-1) t B_v`.

Thus the residual problem is **simultaneous conjugacy of tuples of permutations**. This was already studied and solved algorithmically in the literature, not invented here.

## 2. NG-Q15.1 — complete elementary simultaneous-conjugator algorithm

Given tuples `A=(A_1,...,A_s)`, `D=(D_1,...,D_s)` of explicit permutations on the same k-point set, a deterministic algorithm finds a t satisfying `t^(-1) A_i t = D_i` for every i, or correctly declares that none exists, in **polynomial time in k and s**.

**Algorithm:** Rewrite each condition as `A_i t=t D_i`. Form orbits of the generated actions of A and D on {0,...,k-1}, using publicly known permutations and inverses. A conjugator must map each D-orbit bijectively to an A-orbit of the same *colored permutation action type*. For a chosen D-orbit representative b and candidate A-orbit point a, force t(b)=a. Propagate the equality

`t(D_i(y))=A_i(t(y))`

and its inverse-direction counterpart along all colored action edges. Reject if any point would receive incompatible images or if injectivity fails. A successful propagation gives an exact orbit bijection. Try all a in each unused size-matching A-orbit; if one works, assign the entire orbit and move to the next D-orbit. If none works, declare impossible. Finally verify all original simultaneous conjugacy equations.

**Completeness:** An actual conjugator maps each D-orbit onto an isomorphic A-orbit. Trying the genuine image of b forces the unique equivariant map across that transitive orbit, so the propagation will find it. If a D-orbit matches some candidate A-orbit, those two orbits have the same action type; choosing one leaves all other copies of that isomorphism type interchangeable. Therefore the greedy choice of *any* matching unused orbit cannot block an existing global conjugator. Conversely, if all candidates fail, no orbitwise equivariant global bijection can exist. The final point map is globally a permutation because orbit images are pairwise disjoint and have total cardinality k. Direct equation checking establishes soundness.

**Complexity:** Orbit discovery uses at most O(s k) permutation applications. Across at most k D-orbits and at most k candidate target points/orbits per stage, there are O(k²) pointed-map attempts; each propagates across at most k points with O(s) generator/inverse transitions, costing O(s k). Hence an uncomplicated implementation has conservative time O((s+1)k³), space polynomial in k,s. This bound is deliberately loose. **It avoids enumeration of k! permutations.**

If s=0, all t are valid; the algorithm returns the public identity permutation as one witness. Nontransitive actions and repeated/isomorphic orbit types are covered.

## 3. NG-Q15.2 — full public graph transport decision and witness theorem

For every graph with n vertices and m edges with explicit public S_k transport labels H_e,B_e, the satisfiability of `B_e=x_u^(-1)H_e x_v` and one satisfying full vertex assignment can be decided and constructed **in deterministic time polynomial in k,n,m**.

**Proof:** Build a BFS forest and public H/B root-path products; each step uses O(k) permutation operations, so graph preprocessing is polynomial. In each connected component, form all cycle tuples from public labels, call NG-Q15.1 to obtain a root conjugator or reject, then reconstruct all vertex permutations using the NG-Q14 path formula. If any component has no root conjugator, no full assignment exists. Otherwise independently reconstructed component witnesses combine into a valid graph assignment, which is verified against every original public equation. Summing polynomial component costs yields polynomial total complexity. QED.

**Critical scope:**
- This applies to **the full symmetric group** S_k, with explicit k-entry permutation labels and *noiseless exact equations*.
- It is not an assertion about all abstract groups, arbitrary succinct encodings, subgroups specified by hard-to-use representations, non-exact/noisy edge observations, or all group-based cryptography.
- An alternative valid x_v may differ from the originally planted x_v when centralizers are nontrivial; this is a valid public *witness*, not a proof of recovering an unspecified KEM decapsulation secret.
- If the cycle tuple has trivial common centralizer, then the full hidden vertex assignment is unique. In planted S3 examples the public algorithm recovers it exactly.

## 4. Independent machine tests

Reference algorithm: `research-nextgen/experiments/ng_q15_symmetric_transport.py`, blob `4a576e118475360a99dca16dd74331718adbf50c`. Independent tests: `test_ng_q15_symmetric_transport.py`, blob `a9da0c306b01c2a1e59b93746e40aab88ada9746`.

**Eight local unittest methods passed**, covering:
- All 36 ordered pairs of S3 permutations for single simultaneous conjugacy, checked against brute-force enumeration.
- 300 independently sampled two-generator S3 tuple pairs, exact brute-force decision and witness comparison.
- Nontransitive permutation-action orbits, including a no-solution cycle-type mismatch; empty constraints.
- 120 random planted graph trials for k=3/4 and n=3/5/8, compared against the *independent* exact finite-group solver NG-Q14.
- Planted full symmetric-group graph instances with k=8,16,40,100 and 12 vertices; full public equation verification and original planted recovery.
- Contradictory cycle constraints, disconnected graphs and a component with no edges, malformed tuple rejection.

Combined NG-Q14 and NG-Q15 tests: **18/18 locally passed**, independently verified directly from Python 3.13.5. The final committed GitHub scripts' blob SHAs match locally executed copies. No GitHub CI, Lean/Rocq/Isabelle checker, or external specialist audit.

```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q14_nonabelian_transport test_ng_q15_symmetric_transport
python ng_q14_nonabelian_transport.py
python ng_q15_symmetric_transport.py
```

## 5. Exact prior-art/novelty assessment

Simultaneous conjugacy of permutation tuples is an established problem. See **Andrej Brodnik, Aleksander Malnič, Rok Požar**, *The simultaneous conjugacy problem in the symmetric group*, Mathematics of Computation (2021/2022), DOI [10.1090/mcom/3637](https://doi.org/10.1090/mcom/3637), and *A subquadratic algorithm for the simultaneous conjugacy problem*, Journal of Graph Theory (2022), DOI [10.1002/jgt.22798](https://doi.org/10.1002/jgt.22798). The latter explicitly states polynomial/subquadratic algorithms for this problem; the orbit-propagation proof here is an elementary independently implemented variant, **not an original universal algorithm**. See also nonabelian gain graph switching, [10.1515/spma-2022-0169](https://doi.org/10.1515/spma-2022-0169).

**Scientific verdict:** This is a concrete, proved, reproducible *negative trapdoor feasibility result* for a large natural noncommutative group family. It does **not** satisfy the mission's original mathematical framework goal (M2), construct a new one-way function, establish quantum hardness, or define/secure a KEM. A future proposal must first avoid reduction to existing simultaneous conjugacy, public gauge synchronization and known permutation-action orbit isomorphism.

**No merge or publication authorized by this evidence.** Preserve all prior work and the negative attack.
