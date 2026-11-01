# SG-DIFRA Next Generation — exploratory branch

**Baseline:** `main@cc8f1831cbd5b21caa236331b40c545b88e3071d`.

**Status at this checkpoint:** an exact public quotient attack and mathematical negative example have written proofs and local finite tests, **not** novelty certification, proof-assistant verification, an original secure mathematical foundation, or a post-quantum KEM.

## Read in order

1. [00_RESEARCH_CHARTER.md](00_RESEARCH_CHARTER.md) — priorities, checkpoint and acceptance gates.
2. [01_EXISTING_RESEARCH_BASELINE.md](01_EXISTING_RESEARCH_BASELINE.md) — partial source-verified handover and preexisting attacks.
3. [03_MATHEMATICAL_LITERATURE_REVIEW.md](03_MATHEMATICAL_LITERATURE_REVIEW.md) — narrow, openly incomplete prior-art study.
4. [05_ORIGINALITY_AND_EQUIVALENCE_AUDIT.md](05_ORIGINALITY_AND_EQUIVALENCE_AUDIT.md) — why no foundational novelty claim is warranted.
5. [08_THEOREMS_AND_PROOFS.md](08_THEOREMS_AND_PROOFS.md) — theorem NG-Q1 with full written proof.
6. [09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md](09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md) — source-form high-width counterexample NG-Q2.
7. [10_FORMAL_VERIFICATION_STATUS.md](10_FORMAL_VERIFICATION_STATUS.md) — what is and is not machine checked.
8. [18_REPRODUCIBILITY_MANIFEST.md](18_REPRODUCIBILITY_MANIFEST.md) — environment, seed and test instructions.
9. [19_RESEARCH_DECISION_AND_REJECTION_LEDGER.md](19_RESEARCH_DECISION_AND_REJECTION_LEDGER.md) — supported/refuted/open decisions.
10. [21_PUBLICATION_READINESS_AND_OPEN_PROBLEMS.md](21_PUBLICATION_READINESS_AND_OPEN_PROBLEMS.md) — scientific limitation and research continuation.
11. [22_THREE_LEVEL_EXPLANATION_AND_DEFENSE.md](22_THREE_LEVEL_EXPLANATION_AND_DEFENSE.md) — absolute beginner, university and critical defense explanations.

## Reproduce

```sh
cd research-nextgen/experiments
python -m unittest -v test_public_global_quotient_witness_recovery
```

The code reuses the original Round-8 `PublicShiftSystem` rather than copying the earlier solver into this branch. Historical SG-DIFRA files and all preexisting attack evidence are preserved on main.


## New checkpoint — NG-Q4 / NG-Q5

- [Updated conventional proofs: exact random-source shift survival and hypergraph enumerator equivalence](08_THEOREMS_AND_PROOFS.md)
- [Counterexamples, 680 extra randomized controls and the stronger half-expectation bound](09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md)
- [Rejected/evaluated mathematical candidates](04_CANDIDATE_FRAMEWORK_CATALOGUE.md)
- [Deterministic exact probability calculator](experiments/public_global_shift_survival_bound.py)
- [Independent unit tests](experiments/test_public_global_shift_survival_bound.py)

```sh
cd research-nextgen/experiments
python -m unittest -v test_public_global_shift_survival_bound test_public_global_quotient_witness_recovery
python public_global_shift_survival_bound.py
```

The **locally executed files were byte-identical to the GitHub blobs** and passed seven mathematical unit tests. GitHub CI did not independently run these tests. New mathematical foundations, security assumptions, private trapdoors, KEM construction and formal proof-assistant acceptance remain OPEN.


## Further continuation — NG-Q6 and NG-Q7

The first-moment theorem NG-Q6 shows that the planted witness in the independently sampled dense source-form family is overwhelmingly likely to be **unique**. The classical public NG-Q7 pair-projection consistency attack then recovers those witnesses in every tested dense case for n>=6, despite zero global additive shift space. This is an **attack-driven negative result** about the proposed intuition 'high width + no shifts + unique secret = hardness'; it is **not** a proof that all dense NCSG samplers are easy.

**Reproduce (from this directory's experiments subfolder):**

```sh
cd research-nextgen/experiments
python -m unittest -v test_planted_witness_uniqueness_bound test_public_pair_consistency_attack test_public_global_shift_survival_bound test_public_global_quotient_witness_recovery
python planted_witness_uniqueness_bound.py
python run_public_pair_consistency_campaign.py
```

Fourteen local unittest methods pass; the 30-/10-trial attack campaign is recorded in [15_CLASSICAL_AND_QUANTUM_CRYPTANALYSIS.md](15_CLASSICAL_AND_QUANTUM_CRYPTANALYSIS.md). All five new source files have exact matching Git blob identifiers to locally run copies.

Read [11_COMPUTATIONAL_HARDNESS_ANALYSIS.md](11_COMPUTATIONAL_HARDNESS_ANALYSIS.md), [12_TRAPDOOR_INVESTIGATION.md](12_TRAPDOOR_INVESTIGATION.md), and [15_CLASSICAL_AND_QUANTUM_CRYPTANALYSIS.md](15_CLASSICAL_AND_QUANTUM_CRYPTANALYSIS.md). The mathematical proofs remain in [08_THEOREMS_AND_PROOFS.md](08_THEOREMS_AND_PROOFS.md), and the explicit negative findings in [09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md](09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md). A genuine new foundational framework and a secure private-trapdoor KEM are **NOT** established.


## End-of-execution scientific checkpoint

- [Focused source and claim inventory](02_SOURCE_AND_CLAIM_INVENTORY.md)
- [Implementation and testing](17_IMPLEMENTATION_AND_TESTING.md)
- [Internal research verdict and exact open gates](20_FINAL_INDEPENDENT_RESEARCH_VERDICT.md)

**Scientific boundary:** A mathematically correct project-specific probability bound, tested public witness attack, or likely unique planted assignment is not a novel fundamental mathematical framework and not a secure KEM. The main branch is preserved; experimental conclusions require further mathematical novelty comparison, proof-assistant work and independent cryptanalysis.


## November 1 continuation — NG-Q8 high-probability public-recovery theorem

[NG-Q8 full theorem and assumptions](23_NGQ8_PUBLIC_RECOVERY_THEOREM.md) · [exact finite arithmetic and public-only adversary](experiments/ng_q8_recovery.py) · [independent exhaustive and recovery tests](experiments/test_ng_q8_recovery.py).

**Model-specific theorem:** one independent ternary source-form factor with three explicit public inputs excludes a fixed incorrect two-variable pair assignment with exact probability `15/52`. For fixed public 3-uniform scope hypergraph pair codegrees `d_ij`, a one-pass public algorithm recovers the independently planted witness with failure at most `min(1,8 sum_(i<j)(37/52)^d_ij)`. Complete-triples and suitable O(n^2 log n) anchor scopes therefore admit high-probability polynomial-time **public** witness recovery. This **rejects those sampled source-form distributions as cryptographic secret-hardness foundations**; it does not invalidate all NCSG CSPs or constitute any KEM-security claim.

Run `cd research-nextgen/experiments && python -m unittest -v test_ng_q8_recovery` (**6 local tests passed**). Machine-checking, external review, worldwide novelty and complete secure KEM all remain **not established**.


## NG-Q9: all fixed ternary local source-form arities at sufficient overlap

[Complete scoped general-arity theorem](24_NGQ9_GENERAL_ARITY_PROJECTION_BOUND.md) · [exact rational bound calculator](experiments/ng_q9_general_bound.py) · [independent exhaustive finite tests](experiments/test_ng_q9_general_bound.py).

For fixed r,d>=1, a small **strictly positive** probability that a random source-form local constraint publicly excludes any fixed wrong two-variable assignment yields a polynomial-time public recovery theorem when each variable pair appears in enough independently sampled factors. All unique k-element scopes suffice asymptotically **when k=r+d>=3**; k=2 needs repeated factors. The numerical lower bound can be far weaker than the exact NG-Q8 (1,2) result. **Four new local tests pass;** proof assistant, independent novelty review and original KEM are still absent.


## 1 November 2026 — NG-Q10 and NG-Q11, two additional adversarial gates

- [NG-Q10: sparse two-anchor star candidate **REJECTED** as bounded-treewidth public CSP](25_NGQ10_REJECTED_SPARSE_STAR.md); [complete solver](experiments/ng_q10_public_star_no_go.py); [tests](experiments/test_ng_q10_public_star_no_go.py)
- [NG-Q11: algebraic degree collapse and public affine inversion](26_NGQ11_ALGEBRAIC_DEGREE_NO_GO.md); [interpolation and Gaussian solver](experiments/ng_q11_degree_collapse.py); [tests](experiments/test_ng_q11_degree_collapse.py)

**Exact scope:** Every ternary d=1 source-form factor is affine, for any r>=1 and arbitrary invertible A,B, arbitrary Q; consequently arbitrary public global overlaps can be inverted **as public linear systems** (witness may differ from planted witness if multiple solutions). For scalar r=1,d=2, each public local source-form factor has algebraic degree <=3, whereas an independent uniformly random 27-entry scalar table passes this degree test with probability exactly 1/59049. This is a *distinguisher*, not a KEM security break.

The first NG-Q10 preliminary star-uniqueness test failed; a complete deterministic solver replaced the insufficient method. The NG-Q11 initial floating-point exact-probability helper was corrected. **22/22** combined NG-Q8/Q9/Q10/Q11 local tests passed after the corrections. Both new files and tests were byte-matched to GitHub blob SHA. **No foundational mathematical originality, formal proof assistant, independent cryptanalysis, private trapdoor or complete secure KEM established.**


## 1 November 2026 — NG-Q12/NQ-Q13 new mathematical-equivalence gates

**NG-Q12:** [public local equivalent-coordinate recovery](27_NGQ12_PUBLIC_LOCAL_COORDINATE_RECOVERY.md), [source code](experiments/ng_q12_public_coordinates.py), [six independent tests](experiments/test_ng_q12_public_coordinates.py). For the fully public ternary r=1,d=2 scalar local source form, the finite-difference image for fixed B,A contains exactly 729 functions, with 27 distinct Q representatives each. A complete algorithm scans the 11232 inverse GL3 coordinate bases and recovers a **verified equivalent** (B,A,Q) generator from only 27 public truth-table entries, or certifies no representation exists. A uniformly random function belongs to this precisely defined source family with probability at most 832/387420489. This does not establish KEM private-key recovery.

**NG-Q13:** [rejected hidden quasigroup/isotope idea](28_NGQ13_REJECTED_HIDDEN_QUASIGROUP_ISOTOPE.md), [source code](experiments/ng_q13_isotope_no_go.py), [six tests](experiments/test_ng_q13_isotope_no_go.py). Any public complete Latin-square operation of the form `T(x,y)=gamma^-1(alpha(x)+beta(y))` over elementary abelian F3^m has a publicly normalized group law and publicly recoverable equivalent (alpha',beta',gamma') permutations. This is **known group-isotopy theory**, not original foundational mathematics. A Fano Steiner quasigroup is genuinely *not* group-isotopic (hand proof + all 49 basepoint normalizations), but public left/right division remains easy, so non-isotopy alone supplies no trapdoor.

**Tests and scope:** 12/12 new local unit methods pass; exact committed GitHub code blobs match executed sources. No previous or new main-branch file was changed. No CI, proof-assistant formalization, independently validated worldwide novelty, original hard problem, private trapdoor or secure PQ KEM is established.


### Formal next continuation point

[29_NEXT_FOUNDATIONAL_RESEARCH_GATE.md](29_NEXT_FOUNDATIONAL_RESEARCH_GATE.md) states the exact next mathematical candidate acceptance test after NG-Q12/NG-Q13. It explicitly rejects repeated fixed-table local obfuscation, group-isotopy rebranding and unaudited hardness claims. It preserves all earlier research and keeps mathematical novelty and private KEM security as OPEN, not claimed achievements.

## 1 November 2026 — NG-Q14/NG-Q15 group-transport research checkpoint

The next tested candidate leaves finite-difference NCSG behind and uses secret noncommutative group elements at graph vertices with exact PUBLIC twisted edge relations. The result is a no-go for this proposed trapdoor family, not a new algebra.

- [NG-Q14: public spanning-tree and common-centralizer theorem](30_NGQ14_NONABELIAN_TRANSPORT_NO_GO.md)
- [NG-Q15: polynomial-time full symmetric-group public reconstruction](31_NGQ15_SYMMETRIC_TRANSPORT_POLYNOMIAL.md)
- [NG-Q14 reference algorithm](experiments/ng_q14_nonabelian_transport.py) and [10 tests](experiments/test_ng_q14_nonabelian_transport.py)
- [NG-Q15 polynomial algorithm](experiments/ng_q15_symmetric_transport.py) and [8 tests](experiments/test_ng_q15_symmetric_transport.py)

All unknown vertex group elements reduce to one simultaneous cycle conjugator per connected component. When a solution exists, the solution count equals the common centralizer size. For explicit full symmetric-group permutations S_k, colored-permutation-action orbit matching finds a public witness or detects inconsistency in time polynomial in k and graph input size, including large k=100 experiments. No factorial enumeration is used in NG-Q15.

All 18 targeted local tests passed and exact Git blobs match executed files. The algorithms have known gain-graph/simultaneous-conjugacy antecedents. No novel foundational mathematics, paid work, proof assistant, independent external review, secret-only trapdoor or secure KEM has been established. The main branch remains unchanged.
