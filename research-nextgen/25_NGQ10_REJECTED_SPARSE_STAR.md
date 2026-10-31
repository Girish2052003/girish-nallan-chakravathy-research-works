# NG-Q10 — Rejected sparse-star trapdoor candidate: deterministic public recovery

**Date:** 1 November 2026. **Status:** Conventional correctness proof + executable counterexample; mathematically redundant with bounded-treewidth CSP solving. **Candidate REJECTED** as a new mathematical framework or cryptographic hardness basis.

## Proposed direction and the adversarial failure

The proposed planted NCSG distribution used ternary variables x_0,...,x_(n-1), with all local 3-ary factors on scopes of the form (0,1,j) for 2<=j<n. It allowed any number of independently drawn source-form factors on the *same* scope and suggested O(n log n) repeated factors as a way to force planted witness uniqueness.

A preliminary probabilistic bootstrap proposed: solve a repeated three-anchor (0,1,2) constraint first, then use repeated (0,1,j) factors to identify each leaf value. That bootstrap had a union bound based on existing NG-Q6 local collision probability beta=4/13.

**Critical failure caught before promotion:** The first small-fiber regression found an instance where the preliminary two-stage singleton test was inconclusive even though the **whole global witness was unique**. Leaf constraints can disambiguate anchor choices. Therefore the proposed algorithm was not equivalent to complete global solving, and treating its failure as uniqueness failure was incorrect.

More importantly, the entire repeated-factors argument was unnecessary: **the complete global problem is publicly solvable deterministically even with one factor per leaf, or with arbitrary nonlinear correlated source factors.** No randomness, sampling assumption, or planted witness is necessary.

## NG-Q10.1 — Complete public solver for 2-anchor star CSP

Let V={0,...,n-1} range over an arbitrary finite alphabet of q>=2 values. All public factors (including repeated ones) have scopes of form (0,1,j), 2<=j<n, and arbitrary, explicit public tables with target values. Inputs can be satisfiable or unsatisfiable, planted or unplanted; table functions need not satisfy the SG-DIFRA source form.

**Algorithm:** Try all q^2 assignments (a,b) to x_0,x_1. For each j>=2, compute

L_j(a,b)={z in alphabet: every public factor on (0,1,j) accepts (a,b,z)}.

If any L_j is empty, discard (a,b). If all are nonempty, choose one value from each L_j independently and output the full assignment after verifying every public equation. If all q^2 anchor assignments are discarded, report UNSAT.

**Correctness proof:** Any satisfying assignment has some first-two-coordinate values (a,b). For that pair, its individual x_j lies in each L_j(a,b), so the algorithm never rejects that pair. Conversely, if every L_j(a,b) is nonempty, choose one accepted local value per j. A factor on (0,1,j) depends on no other leaf, so all chosen values together satisfy every factor. Therefore the procedure decides satisfiability **exactly** and recovers a valid witness whenever one exists. QED.

**Complexity:** At most q^2 anchor pairs; each of the m factors is evaluated on at most q candidate values and each leaf is checked, giving O(q^3(m+n)) simple table evaluations/comparisons (loose upper bound), and polynomial time in the complete public input size. For q=3 this is O(m+n), even when **m=Theta(n)**. In graphical language, the primal graph has a tree decomposition with bags {0,1,j} and width at most two. The algorithm is a special case of standard cutset conditioning and bucket elimination, not newly invented mathematical theory.

**Prior art:** Rina Dechter, *Bucket elimination: A unifying framework for reasoning*, Artificial Intelligence **113** (1999), 41–85, DOI **10.1016/S0004-3702(99)00059-4**, https://www.sciencedirect.com/science/article/pii/S0004370299000594. Known conditioning and induced-width algorithms subsume this computation.

## Tests and documented rejected assertions

Source: `experiments/ng_q10_public_star_no_go.py` and `experiments/test_ng_q10_public_star_no_go.py`. Five new test methods passed locally, with 80 independent arbitrary-table/target instances for n=3..6 checked against complete brute-force solution sets; separate planted trials n=4,8,32,128; explicit contradictory/unsatisfiable controls; q=4 test; scope-validation rejection. Demonstration used a single independent NCSG source-form factor per leaf at n=8,32,128, and the solver returned valid witnesses in every demonstrated instance.

Before this accepted replacement, a preliminary unreleased prototype failed a regression because it rejected globally unique instances if the anchor-only constraints were ambiguous. **Preserve this negative result; do not claim the preliminary prototype was correct or completed.**

Git blob SHA: solver `3dd82b72d49717d17a745d71f23d45168b012e31`; tests `e066b9770ccdbeac6b81e51d41b80b89cae958a8`. Both hashes match locally executed copies. No GitHub Actions / machine proof / independent external audit.

## Scientific decision

**REJECT the sparse two-anchor NCSG family as a hard secret-witness problem, at any factor count or nonlinear potential distribution under complete public local table access.** This is not a new mathematical theorem in a foundational sense: it is a special bounded-treewidth case of known CSP algorithms. It also cannot be used to argue that general high-width/sparse hypergraphs are publicly easy. Next candidate must not simply rebrand a known separator/conditioning attack.
