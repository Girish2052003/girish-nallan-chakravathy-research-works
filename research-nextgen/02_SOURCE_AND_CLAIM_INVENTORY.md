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
