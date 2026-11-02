# SG-DIFRA NEXT GENERATION — CURRENT STAGE STATUS AND NEXT-SESSION HANDOFF

**Tracker ID:** SGNG-TRACKER-2026-11-02-v1.0  
**Snapshot date:** 2026-11-02 (Europe/Helsinki); this is a **source-audited historical/current research snapshot**, not a claim that all archival files were re-executed in this turn.  
**Authoritative mission plan:** [35_MASTER_MISSION_PLAN.md](35_MASTER_MISSION_PLAN.md).  
**Research branch:** `research/sg-difra-nextgen-math`, NOT merged to `main`.  
**Status owner:** internal evidence-governed research audit, no independent external review.  
**START NEXT SESSION HERE:** Read 35, this file, [29_NEXT_FOUNDATIONAL_RESEARCH_GATE.md](29_NEXT_FOUNDATIONAL_RESEARCH_GATE.md), then core research status; do not rely on the last chat or on stale commit counts.

## 0. One-line answer: how many stages are left?

**Ultimate original research KEM target: 12/12 ordered scientific stages are NOT FINALLY ACCEPTED FOR A NEW ORIGINAL FRAMEWORK AND KEM.** We are **working in S01, mathematical discovery**, not yet past M2 originality. Hence **11 downstream stages remain after discovery**, and **the ongoing first stage remains to be completed**, for **12 pending stage acceptances** in total.

This is a **gated pipeline**, not a statement that zero work has been done. Substantial theorem, attack, counterexample, mathematical code and reproducibility work exists for REJECTED OR PARTIAL candidates. Later-stage *research activity* does not pass a later-stage final-KEM gate without a selected surviving mathematical object and appropriate cryptographic evidence.

**Primary mathematical-only target:** A genuine original framework (Outcome A) might justify stopping the *primary mission* after its discovery, equivalence audit, valid theorems, independent challenge and evidence without ever building a KEM. This target is **ALSO NOT YET ACCEPTED**. Research cannot honestly predict a reliable time-to-discovery, the number of rejected candidates remaining, or a percentage completion for an open originality problem.

## 1. Verified live GitHub baseline and audit limits

| Item | Observed/evidence |
| --- | --- |
| Official repo | https://github.com/Girish2052003/girish-nallan-chakravathy-research-works |
| Default branch | `main` (verified GitHub repo metadata) |
| Default branch baseline SHA | `cc8f1831cbd5b21caa236331b40c545b88e3071d` when this audit began |
| Existing experimental branch at audit start | `research/sg-difra-nextgen-math`; **217 commits ahead, 0 behind**, 63 changed files vs `main` |
| This governance upgrade | New `35_MASTER_MISSION_PLAN.md` and `36_STAGE_STATUS_AND_NEXT_SESSION_HANDOFF.md`, README discoverability changes; exact later head must be refreshed next session |
| Historial active research draft | `manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.md` in `main`; says NCSG-only research DIRECTION, NOT approved KEM |
| Historical active status | `research-2028/NCSG_ONLY_RESEARCH_STATUS.md` in `main`; old local/public CSP attacks, NCSG-only secure scheme OPEN |
| Original source binary | `archive/SOURCE_ORIGINAL_BINARY_MANIFEST.md` exists; byte-exact original 26-page PDF **not confirmed stored in GitHub** (#4 OPEN) |
| GitHub issues | #1, #2, #3, #4, #5, #6 **all OPEN** at audit; details in Section 7 |
| CI evidence | For one inspected last branch commit, combined commit statuses **empty** and PR-associated workflow runs **empty**. This does **not** prove no workflows or no CI across the entire repository; systematic workflow listing/archival run audit remains OPEN |
| Previous test evidence | Most recent NG-Q16/17/18 local executed **24/24** Python tests (11+7+6) with six exact Git blob hashes. Older cases have their **own historical test reports**; no unified all-research, all-branches clean CI rerun was observed in this audit |
| Authors' earlier work | Girish Nallan Chakravathy and Sreedevi Kannan: maintain original author credit, archival claims and original security rejections |

**Important source mismatch:** Some older append-only sections report `9 NG-Q16 + 7 NG-Q17 + 6 NG-Q18 = 24`, which is arithmetically false; the final correction documents `11+7+6=24`. Use the FINAL matching test file `test_ng_q16_robust_relative_sync.py` blob `830c0c9c196c901906aa6297cadd442f66cebbaf`, not intermediate snapshots. Cleanup should not erase historical corrigenda.

## 2. The exact twelve sequential stages — CURRENT STATUS

**Status vocabulary:** `PASS` = exit criteria for a *selected qualifying new foundation* met; `ACTIVE` = current work without accepted gate; `EVIDENCE ONLY` = real completed work on rejected/partial models, but no final-stage pass; `BLOCKED` = cannot legitimately enter accepted stage before prerequisites; `NOT STARTED` = no qualifying new-system work yet.

| Stage | Original sequence | Current stage status for FINAL original KEM | Evidence actually achieved | Blocking condition |
| ---: | --- | --- | --- | --- |
| **S01** | Mathematical discovery | **ACTIVE — NOT PASS** | NG-Q1..Q18 mathematically specified/tested candidate-specific results; some useful negative statements | **No genuinely original substantive mathematical framework accepted; M2 not established** |
| S02 | Originality evaluation | **EVIDENCE ONLY — NOT PASS** | Many documented reductions to existing algebra, CSPs, polynomial IP, gain graphs, group synchronization; [05 audit](05_ORIGINALITY_AND_EQUIVALENCE_AUDIT.md) | Need serious originality evidence for a SURVIVING candidate, not just rejected candidates |
| S03 | Theorems | **EVIDENCE ONLY — NOT PASS FOR SELECTED FRAMEWORK** | Conventional candidate-specific theorems NG-Q1..NG-Q18 and original scoped results in [08](08_THEOREMS_AND_PROOFS.md) | No selected new framework and its integrated theorem suite |
| S04 | Proofs | **EVIDENCE ONLY — NOT PASS FOR SELECTED FRAMEWORK** | Detailed conventional proofs and exact model-specific calculations | Foundational acceptance missing; no machine-checked foundational selected theorem |
| S05 | Counterexamples | **STRONG EVIDENCE — STILL NOT FINAL PASS** | Public inversion attacks, reject/repair ledger [09](09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md), independent finite and adversarial controls | Need to challenge a selected surviving original mathematical construction |
| S06 | Computational hardness | **EXPLORATORY NEGATIVE — NOT PASS** | Public weak/easy families and asymptotic public-recovery bounds, worst-case and distribution critiques [11](11_COMPUTATIONAL_HARDNESS_ANALYSIS.md) | No credible new average-case hard distribution plus classical/quantum attack bounds |
| S07 | Private trapdoor | **BLOCKED/NO VIABLE CANDIDATE** | Many publicly recoverable 'hidden' representations rejected [12](12_TRAPDOOR_INVESTIGATION.md) | No demonstrated secret-only efficient inversion with no known efficient public equivalent |
| S08 | Cryptographic construction | **NOT STARTED FOR APPROVED NEXT-GEN DESIGN** | Historical SG-DIFRA KEM drafts exist but are attacked/archived | No valid foundation or trapdoor; absent `13_CANDIDATE_KEM_SPECIFICATION.md` |
| S09 | Security analysis | **BLOCKED FOR NEW KEM** | Historical negative cryptanalysis and risk lists; no new security reduction | No complete active KEM for correctness, IND-CCA or QROM; absent `14_CORRECTNESS_AND_SECURITY_PROOFS.md` |
| S10 | Implementation | **MATH CODE EXISTS; NEW KEM NOT STARTED** | Many reproducible public solvers, samplers, exhaustive Python finite experiments | No executable byte-exact full new KeyGen/Encaps/Decaps; [17](17_IMPLEMENTATION_AND_TESTING.md) describes mathematical scripts |
| S11 | Independent cryptanalysis | **INTERNAL ATTACK EVIDENCE ONLY** | Extensive self-critical campaigns on prior research and rejected candidates [15](15_CLASSICAL_AND_QUANTUM_CRYPTANALYSIS.md) | No accepted full KEM to attack; no external independent reviewer documented |
| S12 | Reproducible evidence | **RESEARCH EVIDENCE ONGOING; FINAL PACKAGE BLOCKED** | [18](18_REPRODUCIBILITY_MANIFEST.md) logs scripts, seeds, Git SHA, tests; decision ledger | Full fresh integrated CI, formal proof evidence where justified, KEM evidence/parameters, external challenge not complete |

**Count:** 0/12 sequential S-stage *final KEM acceptances*; 12 still pending; 11 downstream of S01. **NOT** 0% useful research. **NOT** a claim the final goal is feasible or guaranteed.

## 3. The sixteen OPERATIONAL phases — SEPARATE CURRENT STATUS

These are not twelve sequential stage approvals; several are cross-cutting and recurring.

| Phase | Mission workstream | Status | Evidence or main blocker |
| --- | --- | --- | --- |
| **I** | Historical end-to-end baseline audit | **PARTIAL** | [01](01_EXISTING_RESEARCH_BASELINE.md) explicitly labels itself *partial*; full archive, source hashes, all historical programs and CI logs not exhaustively reverified |
| **II** | Global mathematical landscape/literature | **ACTIVE / PARTIAL** | [03](03_MATHEMATICAL_LITERATURE_REVIEW.md) has meaningful prior art, but broad primary-paper coverage across all requested 13+ mathematical areas not completed |
| **III** | Original mathematical framework discovery | **ACTIVE / BLOCKED ON SUCCESS** | 15 candidate groups/variations and NG-Q1..Q18 investigated; NONE accepted as new foundational mathematics |
| **IV** | Novelty and equivalence gate | **ACTIVE / NO SELECTED PASS** | [05](05_ORIGINALITY_AND_EQUIVALENCE_AUDIT.md) rejects apparent novelty; no surviving distinct framework |
| **V** | Theorems and conventional proofs | **SUBSTANTIAL CANDIDATE WORK / OPEN** | [08](08_THEOREMS_AND_PROOFS.md); no selected foundational theorem suite |
| **VI** | Counterexample & formal-verification campaign | **STRONG FINITE TESTING / FORMAL OPEN** | [09](09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md), [10](10_FORMAL_VERIFICATION_STATUS.md); none of the selected foundational claims checked by Lean/Rocq/Isabelle |
| **VII** | Computational hardness | **NEGATIVE/EXPLORATORY** | NG-Q8/9/14/15/16 public recovery obstructions; credible new average-case hardness remains missing |
| **VIII** | Private trapdoor | **NO VIABLE CANDIDATE** | Local coordinate, hidden isotopy, graph transport and gauge hypotheses fail in stated models |
| **IX** | Original cryptographic construction | **BLOCKED** | Missing active fully specified original new KEM |
| **X** | Correctness and security proof | **BLOCKED** | No accepted new full KEM/correctness distribution/IND-CPA/IND-CCA/QROM argument |
| **XI** | Full adversarial cryptanalysis | **PARTIAL / FULL NEW-SCHEME BLOCKED** | Historical KEM attack rounds, new candidate-specific public attacks; no surviving full scheme or external independent review |
| **XII** | Experimental implementation | **MATH PROTOTYPES EXISTS; KEM MISSING** | Many tested Python scripts; not a byte-exact end-to-end KEM |
| **XIII** | Parameters and performance | **HISTORICAL NEGATIVE / NEW NOT STARTED** | Archived cipher sizes/historical profiles analyzed; new growing KEM profiles cannot be justified |
| **XIV** | Rejection, repairs, research pivots | **ACTIVE, WELL EVIDENCED** | [19](19_RESEARCH_DECISION_AND_REJECTION_LEDGER.md), NG-D1..NG-D40; keep doing this |
| **XV** | Reproducibility/evidence governance | **ACTIVE / PARTIAL** | [18](18_REPRODUCIBILITY_MANIFEST.md) seeded scripts and hashes; no verified complete current CI or universal machine-proof coverage |
| **XVI** | Scientific manuscript development | **HISTORICAL DRAFT EXISTS; NEXT-GEN NOT READY** | Main `manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.md`; Track A/B new original work not established; Track C unjustified |

**Do not total these sixteen phase labels as a completion percentage.** They are mixed continuous workstreams, not 16 completed milestones. A phase with genuine output can remain PARTIAL and an acceptance gate can still be blocked.

## 4. All 12 binding acceptance gates — VERIFIED CURRENT CLASSIFICATION

| Gate | Final goal status | Proper interpretation |
| --- | --- | --- |
| **M1** Mathematical consistency | **CANDIDATE-SCOPED evidence; FINAL OPEN** | Existing defined mathematical objects are well formed, but **no selected ORIGINAL framework** to certify |
| **M2** Mathematical originality | **NOT PASSED — PRIMARY BLOCKER** | Published equivalent structures repeatedly found; no defensible original foundation established |
| **M3** Mathematical theorem validity | **CANDIDATE-SCOPED conventional proofs; FINAL OPEN** | Precise scoped arguments/tests, but no selected foundational new result suite independently accepted |
| **M4** Independent mathematical challenge | **INTERNAL ADVERSARIAL EVIDENCE; FINAL OPEN** | Executed counterexample/exhaustive tests, not external independence or surviving selected framework review |
| **M5** Formal verification | **NOT DONE** | No exact selected theorem checked by Lean/Rocq/Isabelle/HOL; Python tests != machine proof |
| **C1** Computational problem | **NO QUALIFYING NEW FOUNDATION** | Existing public problems were often easy; no accepted cryptographic sampled problem |
| **C2** Hardness credibility | **NOT PASSED** | No credible new average-case quantum-relevant hardness; worst-case NP-completeness insufficient |
| **C3** Private trapdoor | **NOT PASSED — CRYPTOGRAPHIC BLOCKER** | No secret-only inversion advantage; many public equivalent-secret attacks |
| **C4** Complete KEM | **NOT PASSED** | No approved fully specified original KeyGen, Encaps and Decaps |
| **C5** Security argument | **NOT PASSED** | No complete correctness/IND-CCA/QROM proof for new system |
| **C6** Independent cryptanalysis | **NOT PASSED FOR NEW KEM** | Existing attacked candidates/historical work, no complete surviving system or external independent review |
| **C7** Practical instantiation | **NOT PASSED** | No new justified parameter levels, performance, full implementation or measurements |

**Important language discipline:** M1/M3/M4 have real *candidate-scoped* scientific achievements but **no final accepted SG-DIFRA Next Generation pass**. C1 does not pass merely because a public search problem has been named. M5 would need recorded exact machine-checked sources (none currently documented).

## 5. Required 22 deliverables — PRESENT does not mean COMPLETE

| # | File ID / name | GitHub branch existence | Actual completion assessment |
| ---: | --- | --- | --- |
| 1 | `00_RESEARCH_CHARTER.md` | PRESENT | Active checkpoint charter; complemented by new full mission plan |
| 2 | `01_EXISTING_RESEARCH_BASELINE.md` | PRESENT | **PARTIAL**, as declared in its title |
| 3 | `02_SOURCE_AND_CLAIM_INVENTORY.md` | PRESENT | **PARTIAL**; new negative claims appended |
| 4 | `03_MATHEMATICAL_LITERATURE_REVIEW.md` | PRESENT | Growing, not complete global primary-source audit |
| 5 | `04_CANDIDATE_FRAMEWORK_CATALOGUE.md` | PRESENT | Many candidates/rejections; no winner |
| 6 | `05_ORIGINALITY_AND_EQUIVALENCE_AUDIT.md` | PRESENT | Candidate rejections, overall M2 OPEN |
| **7** | **`06_SELECTED_MATHEMATICAL_FRAMEWORK.md`** | **ABSENT** | **Correctly deferred**: no accepted original discovery |
| **8** | **`07_DEFINITIONS_AXIOMS_AND_EXAMPLES.md`** | **ABSENT** | Correctly deferred as canonical selected-new-structure definitions |
| 9 | `08_THEOREMS_AND_PROOFS.md` | PRESENT | Candidate results, none machine-checked new framework |
| 10 | `09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md` | PRESENT | Substantial candidate-specific negative evidence |
| 11 | `10_FORMAL_VERIFICATION_STATUS.md` | PRESENT | Records no proof assistant checking |
| 12 | `11_COMPUTATIONAL_HARDNESS_ANALYSIS.md` | PRESENT | Negative attacks and candidate issues, no credible surviving hard distribution |
| 13 | `12_TRAPDOOR_INVESTIGATION.md` | PRESENT | Failed candidates, no acceptable trapdoor |
| **14** | **`13_CANDIDATE_KEM_SPECIFICATION.md`** | **ABSENT** | Correctly deferred; no justified original standalone KEM |
| **15** | **`14_CORRECTNESS_AND_SECURITY_PROOFS.md`** | **ABSENT** | Correctly deferred; no complete new KEM proof |
| 16 | `15_CLASSICAL_AND_QUANTUM_CRYPTANALYSIS.md` | PRESENT | New mathematical/public attacks; not full quantum-secure KEM analysis |
| **17** | **`16_PARAMETER_AND_EFFICIENCY_ANALYSIS.md`** | **ABSENT** | Correctly deferred; no new candidate parameters |
| 18 | `17_IMPLEMENTATION_AND_TESTING.md` | PRESENT | Research math scripts; NOT a KEM reference implementation |
| 19 | `18_REPRODUCIBILITY_MANIFEST.md` | PRESENT | Good local per-checkpoint records; CI/full integration unverified |
| 20 | `19_RESEARCH_DECISION_AND_REJECTION_LEDGER.md` | PRESENT | Active candidate rejection decisions through NG-D40 |
| 21 | `20_FINAL_INDEPENDENT_RESEARCH_VERDICT.md` | PRESENT | Internal session checkpoint **only**, despite file title |
| 22 | `21_PUBLICATION_READINESS_AND_OPEN_PROBLEMS.md` | PRESENT | Future manuscript not ready; open scientific blockers |

**Exact inventory:** **17 of 22 requested named files were present** at audit start, **5 of 22 absent on purpose**. No omitted selected framework/KEM files were invented to make a dashboard look complete. The new governance plan and handoff are **supplemental**, not a false claim that 22 original scientific deliverables are complete.

## 6. Candidate research actually accomplished

**Established/project-specific mathematical evidence, with stated limits:**
- NG-Q1–Q7: public additive quotient/difference, model-specific collision/survival probabilities, finite public witness attacks, numerical countercontrols.
- NG-Q8: exact local false-pair rejection probability 15/52 in independent ternary r=1,d=2 public source sampler; high-overlap public polynomial planted recovery bound.
- NG-Q9: positive but often tiny fixed-arity local rejection bound; sufficiently high pair-codegree public recovery.
- NG-Q10: sparse two-anchor star deterministic bounded-width public CSP solving.
- NG-Q11: d=1 ternary source factors are affine/publicly Gaussian-solvable; r1,d2 public degree distinguisher, not KEM break.
- NG-Q12: equivalent local three-input generator coordinates publicly recoverable when 27-entry table explicitly public.
- NG-Q13: simple hidden elementary-abelian quasigroup isotopes publicly normalized; Fano nonisotopic but publicly divisible control.
- NG-Q14: exact nonabelian graph-transport spanning-tree reduction and common-centralizer solution count.
- NG-Q15: polynomial public full S_k explicit-permutation transport recovery via simultaneous conjugacy orbit matching.
- NG-Q16: under precise flat ratio/noise assumptions, adversarial majority and independent replacement Hoeffding public recovery conditions.
- NG-Q17: original absolute root gauge remains statistically uniform under iid uniform secrets and relative-only publication.
- NG-Q18: exact random graph isolation moments and sparse cross-component identifiability obstruction.

These are **valuable negative/equivalence findings**, not certification of world-first algebraic theory or PQ hardness. Details and caveats belong to [08](08_THEOREMS_AND_PROOFS.md), [09](09_COUNTEREXAMPLES_AND_NEGATIVE_RESULTS.md), [18](18_REPRODUCIBILITY_MANIFEST.md), [19](19_RESEARCH_DECISION_AND_REJECTION_LEDGER.md), [29](29_NEXT_FOUNDATIONAL_RESEARCH_GATE.md), and [32–34](32_NGQ16_ROBUST_NOISY_RELATIVE_RECOVERY.md).

**No independent human mathematical novelty verification, no selected framework, no credible trapdoor and no original KEM.** Mathematically scoped negative results should not be mistaken for final mathematical Outcome A or KEM Outcome E.

## 7. Six open GitHub issues (source-of-truth blockers, not invented deadlines)

- [#1 Archived MDS-HBCE asymptotic public-decapsulation break; finite attack study open](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/1)
- [#2 Byte-exact full KEM, QROM and timing/side-channel audit](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/2)
- [#3 Archived huge-ciphertext feasibility/parameter redesign](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/3)
- [#4 Exact historical author-uploaded original-PDF binary preservation](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/4)
- [#5 EUROCRYPT 2028 CFP, anonymous-source version, citation and rights audit](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/5)
- [#6 NCSG-only complete secret-essential trapdoor and independent IND-CCA proof](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/issues/6)

**Nuance:** #6 is the *historical NCSG-only design branch* requirement, not a mandate to force the mathematically original Next Generation program to stay within NCSG. Never silently close/rewrite it. No issue closed in this governance audit. Main unchanged.

## 8. NEXT HIGHEST-VALUE ACTIONS (ordered; autonomy retained)

1. **Continue the primary mathematics discovery campaign, not KEM cosmetics.** Define at least one precise scalable object with new proposed nontrivial invariant, operations, complexity measure, and exact compact public encoding, *outside* the rejected coordinate-hiding, low-degree, public-CSP, group-isotope and public gain-graph templates. Write down a testable statement and its nearest published antecedents **before** promoting a name.
2. **Adversarial novelty/equivalence test.** Try explicit isomorphisms, representation-theoretic transport, polynomial-system encodings, graph-code/cocycle changes, CSP formulations and known trapdoor-algebra reductions; document failures and actual remaining novelty, not just failed keyword search.
3. **Close Phase-I source audit gaps** independently of discovery progress: inventory all historical program counts, exact source hashes and proof statements; verify active vs archived KEM, true binary original PDF presence and Actions/CI results. Update [01](01_EXISTING_RESEARCH_BASELINE.md) and [02](02_SOURCE_AND_CLAIM_INVENTORY.md) with actual rechecked evidence, never guessing.
4. **Formalize one modest correct theorem** (e.g. exact finite-field finite-difference image or absolute gauge information theorem) in Lean/Rocq if no-cost tooling is available, checking source against the *exact* conventional claim. This improves M5 evidence for *that theorem only*, not M2 or the future KEM.
5. **After a candidate survives M2/M3/M4**, construct and challenge a precise average-case hard problem (C1/C2) and secret-only inversion (C3). Only then create `06_`, `07_`, `13_` and other otherwise absent files with *actual* validated content.
6. Maintain the negative result catalogue and provenance. Do not publish or merge on enthusiasm. No 128/192/256 security claims without quantified attack costs and justification.

**Success at next session:** a new *specific falsifiable* mathematical claim with appropriate proof/counterexample/prior art or an independent substantive audit/formal proof result. A failed candidate with reproducible counterexample is valid progress, but it does not pass a final acceptance gate.

## 9. MANDATORY CHECKPOINT HANDOFF TEMPLATE (append after actual work)

For each new session, ADD a dated section below with:
- Exact `main` SHA, branch name and branch head commit SHA; ahead/behind; checked issues/CI status.
- Theorem/candidate IDs; hypotheses, proof/counterexample/finite experiments; exact code, Python/tool version, random seeds, outputs and Git blob hashes.
- Which **S-stage**, **I–XVI phase**, and **M1–M5/C1–C7 gate** statuses changed and WHY, or explicitly **NO GATE CHANGE**.
- Any disproved security claim/novelty equivalent; attribution and links to authoritative primary literature.
- Updated 22-document presence/completeness checklist if status changes.
- Selected next scientific action and the hard blocker; no fictitious milestone percentages or time-to-breakthrough.
- Do NOT overwrite historical rows or silently promote an earlier partial result.

## 10. Formal final outcome at this audit checkpoint

**Mathematical track:** substantial internal **scoped negative results and method-specific theorems**; novel foundational framework **NOT ESTABLISHED**. An externally verified original Track A framework has not been obtained. Outcome is presently **F / inconclusive with supported negative mathematical results**; a more positive B outcome would require evidence that a specific statement is genuinely new rather than a known corollary.

**Cryptographic track:** **F — no qualified standalone post-quantum KEM**, no defensible C2/C3 or IND-CCA/QROM, no validated new parameters. An attacked historical candidate is NOT an active solution.

**Do not conflate:** 217 previously accumulated experimental commits, many checked finite scripts, and 24 tests in the most recent suite are valuable research outputs, NOT a measure of distance to a mathematically new one-way trapdoor.

**This handoff stays the FIRST reference for future research sessions.**


---

## HANDOFF APPENDIX — 2026-11-02: NG-Q19 matrix-transport public inversion

**Read in this order next time:** [35_MASTER_MISSION_PLAN.md](35_MASTER_MISSION_PLAN.md), THIS handoff (latest appendix), [37_NGQ19_MATRIX_TRANSPORT_LINEARIZATION.md](37_NGQ19_MATRIX_TRANSPORT_LINEARIZATION.md), [29_NEXT_FOUNDATIONAL_RESEARCH_GATE.md](29_NEXT_FOUNDATIONAL_RESEARCH_GATE.md), [19_RESEARCH_DECISION_AND_REJECTION_LEDGER.md](19_RESEARCH_DECISION_AND_REJECTION_LEDGER.md). Always re-query live main/branch SHA rather than assuming the figures here remain current.

**Baseline from authenticated live repository at this continuation start:**
- Default main unchanged SHA **cc8f1831cbd5b21caa236331b40c545b88e3071d**.
- Experimental research branch initially **226 ahead / 0 behind**, **65 changed files** versus main, containing the two canonical governance documents and earlier NG-Q1–NG-Q18 results.
- Experimental branch only modified with new theorem, code, independent tests, source/literature/claim updates and this handoff; no force push/merge, no main edit.
- The **end-of-session branch HEAD and updated ahead/files** are to be read from live GitHub compare immediately before the final report; the numbers above are *START* not *end* counts.

### What was actually investigated?

**Candidate NG-C16:** Full noncommutative matrix group GL(k,Fp) as hidden vertex transformations on publicly exact group-transport edges, mathematically distinct from the earlier explicit symmetric permutations but still reducible to published module-isomorphism machinery.

**Finding NG-Q19.1:** Any such connected graph can be normalized through a public tree to one unknown invertible root matrix T whose cycle conditions **A_e T=T D_e** are LINEAR in k² entries. Any invertible solution gives a valid equivalent full public witness; Gaussian elimination finds the full solution space.

**Finding NG-Q19.2:** For prime p>k, whenever a valid planted T exists, the determinant of a uniformly sampled public solution-space element is a nonzero degree-k polynomial. Each sample is invertible with probability at least **1-k/p**; N independent trials fail with probability at most **(k/p)^N**, under the fixed public instance and random fresh coefficients. Thus a polynomial randomized public witness finder exists on the stated p>k scaling, *assuming a validated prime field*. The reference code's prime-checker is simple trial division and therefore its whole runtime is **NOT asserted polynomial in log p**.

**Negative controls:** Nonzero intertwiner space with only singular matrices yields INCONCLUSIVE, not UNSAT; a zero-dimensional intertwiner space proves UNSAT. p<=k is NOT covered by a useful Schwartz–Zippel bound from this reference method; do not imply all small fields insecure by this very implementation. Published module-isomorphism algorithms are separate pre-existing literature.

**Originality:** The key algebra was already examined in *Polynomial Time Algorithms for Modules over Finite Dimensional Algebras*, Chistov–Ivanyos–Karpinski, ISSAC 1997, DOI 10.1145/258726.258751. NG-C16 is **REJECTED for claimed mathematical originality/private inversion**, not rebranded as a discovery.

### Execution and integrity

- **12/12 newly executed local NG-Q19 tests passed** under Python 3.13.5, including an independent finite brute enumeration over GL(2,F2), exact 96/125 invertibility over Mat_2(F5), randomized planted matrix tuples and graph instances up to k=7,p=101, malformed data and singular-only/UNSAT negative controls.
- New executable [source](experiments/ng_q19_matrix_transport.py) locally run and GitHub SHA matched: **b1635b98795f544da2652669b0f383c1c1e256bd**.
- New [test suite](experiments/test_ng_q19_matrix_transport.py) locally run and GitHub SHA matched: **8d8bc8335e3265989ffd39b3bf94a7109ee428e9**.
- The theorem and exact caveats appear in [37_NGQ19_MATRIX_TRANSPORT_LINEARIZATION.md](37_NGQ19_MATRIX_TRANSPORT_LINEARIZATION.md).
- **NOT rerun:** historic earlier test suites, entire archive, CI/GitHub Actions, any proof assistant, complete KEM, independent human cryptanalysis. Neither 12/12 current local tests nor earlier 24/24 current-at-the-time NG-Q16–18 tests constitute a full-repository green CI report.

### Acceptance gate and stage delta — explicitly NO GATE CHANGE

| Item | Previous state | Now after NG-Q19 | Rationale |
| --- | --- | --- | --- |
| **Sequential S01** mathematical discovery | ACTIVE, not accepted | **ACTIVE, not accepted** | NG-C16 rejected as established module isomorphism, not original mathematics |
| **Sequential S02–S05** originality/theorems/proofs/counterexamples | Candidate work, no final acceptance | **Additional candidate-specific evidence; still no final acceptance** | Valid negative model-specific proof does not certify a selected novel framework |
| **Sequential S06–S12** hardness→KEM→evidence | No qualified full KEM acceptance | **UNCHANGED / NOT ACCEPTED** | Public recovery defeats this candidate; no complete surviving new scheme |
| **Phase II** prior art | Partial | **Expanded** | Chistov–Ivanyos–Karpinski ISSAC 1997 + later module isomorphism background |
| **Phase III–VI** candidate/proof/challenge | Active/partial | **More candidate-specific negative work** | NG-Q19 theorem, 12 independent tests, singular controls |
| **Phase VII–VIII** hardness/trapdoor | Negative, no survivor | **Additional REJECTED premise** | Public matrix-space inversion with quantitative p>k bound |
| **Phase XIV/XV** reject/reproducibility | Active/partial | **Expanded** | NG-D41–D43 and exact SHA-identical executed source |
| **Mathematical M1/M3/M4** | Candidate-scoped proof/test evidence | **NG-Q19 scoped evidence added; final gates OPEN** | No accepted original framework |
| **M2 originality** | NOT PASSED | **NOT PASSED** | Classical finite-field module-isomorphism equivalence |
| **M5 formal proof** | NOT CHECKED | **NOT CHECKED** | No Lean/Rocq/Isabelle runs |
| **Cryptographic C1–C7** | NO FINAL PASS | **NO FINAL PASS** | No new credible average-case hard problem, secret-only trapdoor, full KEM or security reduction |

**Count remains EXACTLY: 12 of 12 ordered S-stage final KEM approvals are pending, including the active first; 11 stages follow mathematical discovery.** This is not a percentage of intellectual work or a time estimate. The mathematical-only original discovery outcome likewise remains unestablished.

**New required files:** The historical count of original mandatory 22 deliverables remains 17 present, 5 scientifically deferred; file 37 is a supporting proof, not a falsely completed selected-framework/KEM specification.

### Next autonomous research action

Do **not** merely enlarge hidden noncommuting matrix dimensions or choose p<=k as a cosmetic 'repair'. Instead prioritize an entirely different precisely defined scalable mathematical object with a genuine non-reducible invariant, and **test explicit reductions to finite-field modules, matrix intertwiners, tensor isomorphism, group actions, CSP, polynomial interpolation and known public graph switching before claiming novelty**. If no defensible candidate is found, a rigorous independent Phase-I baseline/CI audit or a real machine-checked candidate-scoped theorem provides useful research progress without pretending that it advances the KEM acceptance gates.

**Current mathematical verdict:** negative/inconclusive with model-specific results; no new original foundational framework. **Current cryptographic verdict:** Outcome F, no accepted private-trapdoor PQ KEM.



### Additional independent finite completeness check (2 November 2026)

For ALL 36 ordered pairs (A,B) in GL(2,F_2)^2, an independent enumeration of all six possible invertible T found exactly **14 conjugate pairs** and **22 nonconjugate pairs**. The reference public algorithm returned **14 verified invertible witnesses**, **16 PROVEN_UNSAT (zero intertwiner space)**, and **6 INCONCLUSIVE (nonzero intertwiner space containing no invertible matrix)**. Hence its 36-pair regression establishes **soundness of every definitive answer**, NOT a complete finite-field decision algorithm; six negative pairs were intentionally *not* decided by this simple method. The numbers were recalculated after the original 12 tests with an independent Counter over all 36 cases, without changing the two already-committed executable files.

This sharpens the restriction **p>k** for the proven probabilistic bound: the p=k=2 data do not justify a public-recovery completeness theorem. Stronger general module-isomorphism algorithms are established elsewhere, but are not implemented or verified here.


---

## NG-Q20 — SECOND 2026-11-02 MISSION HANDOFF: finite word-product tensor/automata candidate

**Read next session in order:** canonical [35 master mission plan](35_MASTER_MISSION_PLAN.md), THIS handoff *including this newest appendix*, [38 NG-Q20 theorem/limitations](38_NGQ20_HANKEL_WORD_ORACLE_BOUNDARIES.md), [29 next foundational originality gate](29_NEXT_FOUNDATIONAL_RESEARCH_GATE.md), [19 rejection ledger](19_RESEARCH_DECISION_AND_REJECTION_LEDGER.md). Query the LIVE default-branch and experimental branch commits again; this is a dated snapshot, not an automatic monitor.

### Baseline and purpose

- Branch at start of this NG-Q20 continuation: `research/sg-difra-nextgen-math` was **251 commits ahead, 0 behind main**, 68 changed files; verified default `main` SHA `cc8f1831cbd5b21caa236331b40c545b88e3071d`.
- This work **does not repair or rename the rejected NG-Q19 matrix graph transport**. It tests a structurally different kind of input: **a word-dependent scalar output** from a sequence of noncommuting hidden transition matrices, with a specified public **membership evaluation oracle**.
- The public evaluator / ordinary inspectable public key distinction is ESSENTIAL: a black-box membership oracle can hide a needle word only by assumption. No independently evaluable cryptographic public-key representation hiding that word was constructed.

### What was proved, exactly

**NG-Q20.1 public Hankel equivalence theorem:** f(w)=alpha M_w beta over F_p, minimal Hankel rank d. IF a full-rank dxd Hankel submatrix H(P,S) is PROVIDED publicly, recover equivalent state transitions by H^-1 H_a, α'=(f(s_j)), β'=H^-1(f(p_i)), for **every word w**, with at most (s+1)d²+2d membership evaluations. This is conditional on a known sufficient PUBLIC Hankel basis; the query bound does NOT include FINDING that basis. The basis can be selected among words length <=d-1 by minimal-reachability arguments, but brute search of all such words is exponential in d.

**NG-Q20.3 needle information theorem:** for uniform hidden u in Sigma^L, f_u(w)=1 iff w=u has Hankel rank d=L+1. A classical membership-only algorithm using q<s^L adaptive oracle probes and one final guess identifies u with probability <=(q+1)/s^L. This is an **ORACLE QUERY** lower bound, not a computationally secure KEM hardness proof. With standard coherent quantum access, Grover search uses O(s^(L/2)) queries; existing BBBV 1997/Zalka 1999 quantum search bounds are acknowledged, but no quantum code was executed here. Neither model specifies a public-key protocol or private trapdoor.

**Originality:** these are **known weighted-automata/rational-series/Hankel mathematics** (Carlyle–Paz 1971; Kaznatcheev–Panangaden 2021; Daviaud–Johnson 2025). The proposed hidden word-product family NG-C17 fails the required *original mathematical framework* criterion; no worldwide novelty claim is made.

### Local execution and committed integrity

- **10/10 new local Python 3.13.5 unit tests PASS** after correcting an initial needle fixture that accidentally omitted a symbol in the stated public alphabet (first run: 9 pass, one error; final: all pass).
- [Public reconstruction code](experiments/ng_q20_hankel_oracle.py): EXACT local + GitHub blob SHA **530bb4ff34140a28650e5c873efec06f3702fe33**.
- [Independent tests](experiments/test_ng_q20_hankel_oracle.py): EXACT local + GitHub blob SHA **d53970b6eab6aa6048e17e4c1905087917f766b4**. The first GitHub test-file draft differed in one explicit-alphabet fixture; it was corrected via a further commit and the final blob was confirmed equal to the locally passing source.
- Test scope: 16/16 binary length-four needle realizations, word-prefix/suffix rank identities, random minimal noncommuting matrix automata over F2/F3/F7/F11, F5 explicit noncommutativity, exact oracle-call upper bound, invalid inputs and oracle indistinguishability. Seed 20261102. Demo rank-3 F7 family recovered a fully equivalent output function using 15 public evaluations GIVEN an invertible basis, verified on all words length <=8.
- Proof-checker/CI: **not done**. Local executable PATH lacked lean/lake/coqc/z3/sage; no machine-checked theorem, no independent human review, no current complete historical-suite rerun. Code includes an **exponential basis discovery diagnostic**, and a naive trial-division prime validator; neither is claimed polynomial in bit-length for arbitrary prime modulus.

### Exact gate/phase decision — NO GATE CHANGES

| Item | Status before NG-Q20 | Status after NG-Q20 |
| --- | --- | --- |
| Sequential **S01 mathematical discovery** | ACTIVE, not accepted | **ACTIVE, not accepted** (NG-C17 rejected for known algebra) |
| Sequential **S02–S05** novelty/theorems/proofs/counterexamples | Candidate work exists, not finally passed | Additional correct candidate-specific theory and tests; **not passed for selected original math** |
| Sequential **S06–S12** hardness/trapdoor/KEM/security/implementation/independent cryptanalysis/evidence | NO accepted new original KEM stages | **UNCHANGED**; no full KEM exists |
| Operational Phase II prior-art | Partial, expanding | Expanded by weighted automata + tensor equivalence + oracle-learning sources |
| Operational Phase III–VI | Active candidate challenge | NG-Q20 precisely defined, proofs and adversarial control preserved; formal proof assistant still OPEN |
| Operational Phase VII–VIII | No credible accepted hardness/trapdoor | Classical needle ORACLE lower bound is NOT C2/C3 and public Hankel access offers equivalent reconstruction |
| Phase XIV/XV | Active rejection/evidence | NG-D44–D46, 10 local tests, two code hashes preserved |
| **M2**, C2, C3 | NOT PASSED | **NOT PASSED** |
| **M5** machine proof | NOT PASSED | **NOT PASSED** |
| All remaining M/C final KEM gates | No accepted next-gen full construction | **NO GATE CHANGE** |

**Exact stage count:** still **12/12 final KEM stage acceptances pending**, including active S01; 11 downstream after accepted novel mathematical discovery. This is not an estimated percentage of R&D effort or a guarantee that a new KEM can be discovered.

**Original 22 mandatory deliverables:** still 17 present, five scientifically deferred; file 38 is a supporting research theorem/counterexample record, not a substituted "selected mathematical framework" or complete KEM specification.

### Handoff priority for next session

Do not spend another cycle on mere repackaging of hidden groups, matrices, tensor-train gauge, recognizable formal series or CSP. The **highest-value unanswered PRIMARY mission question is still a substantive original mathematical operation, invariant, or nontrivial theorem that survives equivalence challenges**. Choose an actual scalable object and test its differentiating invariant, explicitly attempting reduction to existing polynomial systems, weighted automata, tensor equivalence, sheaf/CSP and group actions. Or make independent progress on Phase-I old-source audit / specific formal theorem proof using only no-cost available resources. Any genuine counterexample remains valuable, but **do not overstate it as progress on KEM acceptance gates**.

**Final current verdict:** mathematically useful but foundationally non-novel negative evaluation; cryptographic Outcome F, no original post-quantum KEM or justified private trapdoor. Next session should read BOTH governance docs before new commits.
