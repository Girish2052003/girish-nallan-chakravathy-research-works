# Source and claim inventory — partial but auditable checkpoint

**Baseline:** `main@cc8f1831cbd5b21caa236331b40c545b88e3071d`, 31 October 2026. Working branch `research/sg-difra-nextgen-math` keeps original main unchanged. This is a focused inventory, **not** a full claim-by-claim audit of the complete historical repository.

| Claim identifier | Source of exact statement | Kind | Status / boundary |
| --- | --- | --- | --- |
| OLD-4.6 | `manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.md`, §4 | Public source-form local shift inversion | Existing written proof; explicit-table conditions; no machine check here |
| OLD-4.8 | Same manuscript, §4.5 | Public-evaluation local inversion | Existing randomized algorithm and written tail proof; polynomial right-table size; not a KEM |
| OLD-12.9 | Same manuscript, §12.9 | Low-width public CSP witness search | Standard variable elimination, scoped upper bound; not hardness |
| OLD-12.10 | Same manuscript, §12.10 | Public global shift criterion | Existing written proof; rank-deficient targets can remain inconclusive |
| NG-Q1 | `research-nextgen/08_THEOREMS_AND_PROOFS.md` | Complete quotient witness recovery and exact fiber count | New scoped extension; conventional proof and finite tests; originality open |
| NG-Q2 | `research-nextgen/09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md` | High-width, deficient shift rank but easy public witness family | Constructed counterexample and finite regression; no general random KEM result |
| NG-Q4 | `research-nextgen/08_THEOREMS_AND_PROOFS.md` | Exact local constant-shift probability, global shift first moment, dense overlap bound | Conventional proof, rank and 19,683-table checks; no new mathematical framework established |
| NG-Q5 | Same | Hypergraph support polynomial, induced-subhypergraph equivalence | Exact elementary equivalence; rejected as foundational novelty |
| NG-Q6 | Same | Planted collision probability and exact expected number of extra witnesses | Conventional proof, 19,683-table finite check, brute-force small fibers; does not prove hardness |
| NG-Q7 | Same and `research-nextgen/15_CLASSICAL_AND_QUANTUM_CRYPTANALYSIS.md` | Public pair projection consistency soundness + recovery campaign | Standard CSP method; conventional invariant proof; 14 locally passing tests; finite successes do not prove asymptotic probability |
| SEC-C1..C7 | `research-nextgen/21_PUBLICATION_READINESS_AND_OPEN_PROBLEMS.md` | Original KEM, private trapdoor, security and practical instantiation | NOT ESTABLISHED |

**Scientific integrity:** All older claims retain their original authorship/provenance. Original SG-DIFRA contributors are Girish Nallan Chakravathy and Sreedevi Kannan, with external tool/algorithm authors credited for relevant antecedents. Do not infer new work authorship from a repository name. Machine-checked theorems, independent external review and complete current KEM security are absent.

**Unfinished baseline items:** complete archive/manuscript inventory, original artifact byte-level verification, independent rerun of all older research checks, and complete audit of CI workflows and issues. These remain explicit tasks.


| NG-Q8 | `research-nextgen/23_NGQ8_PUBLIC_RECOVERY_THEOREM.md` | Exact local false-pair exclusion 15/52; fixed-scope public recovery failure bound `8 Σ_(pairs) (37/52)^codegree`; complete triples / anchor corollaries | Conventional finite-enumeration-assisted argument, 6 locally executed tests, no proof assistant or external review; exact ternary r=1,d=2 independently sampled source-form explicit tables only |
| NG-C05 | `research-nextgen/04_CANDIDATE_FRAMEWORK_CATALOGUE.md` | Local relation constraints as global sections of presheaf | Foundational originality **rejected as already represented in published sheaf/CSP literature**; no invented new theory |


| NG-Q10 | `research-nextgen/25_NGQ10_REJECTED_SPARSE_STAR.md` | Complete deterministic public solver for arbitrary ternary star-factor tables (0,1,j) and SAT/UNSAT | Proved as simple width-2/CSP cutset conditioning; **foundational novelty REJECTED**; five unit tests/finite brute checks |
| NG-Q11.1-3 | `research-nextgen/26_NGQ11_ALGEBRAIC_DEGREE_NO_GO.md` | Ternary source-form `degree<=max(1,2d-1)`; entire d=1 family affine with arbitrary global factor hypergraph publicly solvable by Gaussian elimination | Conventional proofs + public solver + finite tests; known finite-field polynomial theory; does not imply complete KEM compromise |
| NG-Q11.4 | Same | Exact local r=1,d=2 degree<=3 distinguisher; uniform function false positive 1/59049; uniform Q degree exactly3 probability 2/3 | 19,683-table exhaustive finite test plus analytic 17-coefficient count; **only local distinguishability**, no demonstrated d=2 witness recovery theorem for arbitrary scopes |


| NG-Q12.1 | `research-nextgen/27_NGQ12_PUBLIC_LOCAL_COORDINATE_RECOVERY.md` | For ternary scalar r=1,d=2 source form, Delta_(1,0)Q has 6D image, 3D kernel; 729 image functions and 27 Q per image at fixed B,A | Exact proof, full 19683-Q enumeration and six locally passing tests; novelty not certified |
| NG-Q12.2-3 | Same | Complete equivalent (B,A,Q) local recovery from public 27-entry f by all 11232 GL3 basis candidates; uniform random source-membership <=832/387420489 | Verified code and full-table check; **equivalent local representation**, not necessarily true original secret or full KEM break; finite local size only |
| NG-Q13.1-2 | `research-nextgen/28_NGQ13_REJECTED_HIDDEN_QUASIGROUP_ISOTOPE.md` | Public normalization of hidden group isotopy and full equivalent alpha',beta',gamma' via public Latin-square table | Prior classical group isotopy, not original algebra; proof and finite tests; explicit table time only |
| NG-Q13.3 | Same | Seven-point Fano Steiner quasigroup is not group-isotopic, but public left/right division remains easy | Hand proof, all 49 principal anchor normalizations tested; **non-isotopy does not imply trapdoor** |

| NG-Q14.1–2 | research-nextgen/30_NGQ14_NONABELIAN_TRANSPORT_NO_GO.md | Nonabelian public group-edge transport reduces via spanning tree to one root conjugator per connected component; solution count is common centralizer cardinality | Conventional exact proof; ten passing tests and independent small-group brute-force; existing gain-graph/switching antecedents |
| NG-Q15.1–2 | research-nextgen/31_NGQ15_SYMMETRIC_TRANSPORT_POLYNOMIAL.md | Complete deterministic polynomial-time public SAT/witness construction for explicit full symmetric-group S_k twisted graph transport | Orbit-matching constructive proof; 8 passing tests including degree-100 permutation labels; known simultaneous permutation conjugacy prior art; not arbitrary succinct group or KEM security |


| NG-Q16.1–4 | research-nextgen/32_NGQ16_ROBUST_NOISY_RELATIVE_RECOVERY.md | Public two-hop plurality recovers true relative group labels under deterministic honest-majority; independent uniform replacement noise/erasures give bound C(n,2)(|G|-1)*exp(-(n-2)*rho^4*(1-epsilon)^4/2) | Conventional proof + **11 final local tests** (9 initial, 2 later adversarial controls); **flat H=identity only**, not general twisted transport/KEM |
| NG-Q17.1–2 | research-nextgen/33_NGQ17_GAUGE_IDENTIFIABILITY.md | Independently uniform group root remains exactly uniform given ratio-only public observations; cross-component ratios uniform when graph disconnected | Exact symmetry proof + 7 local posterior tests; not a new cryptographic trapdoor or entropy-security theorem |
| NG-Q18.1–2 | research-nextgen/34_NGQ18_SPARSE_OBSERVATION_ISOLATION.md | Exact E,Var of isolated vertices in G(n,p), Chebyshev lower probability bound of isolation and cross-component non-identifiability | Standard Erdos–Renyi theory + 6 tests; not new foundational random graph theory |
