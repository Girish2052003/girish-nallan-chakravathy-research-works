# Publication and open-problem checkpoint

**Research stage:** attack-driven mathematical cryptanalysis. This checkpoint is **not** evidence for an original foundational mathematical system, an independently secure KEM, a formal proof certificate, EUROCRYPT 2028 readiness, or accepted publication.

## Findings worth preserving
- An exact quotient-space decomposition and cardinality formula for explicit overlapping ternary finite-field constraint systems (NG-Q1).
- A high-width, deficient-shift-rank, publicly solvable NCSG-source-form counterexample family (NG-Q2).
- Finite reproducibility with brute-force comparisons, deliberately maintained independently of novelty and KEM-security assertions.

## Open scientific questions
1. Does NG-Q1/Q2 reduce immediately to known linear-structure quotient or CSP symmetry algorithms? Which exact prior theorem applies?
2. How does global shift codimension scale on the real proposed random source-form NCSG instance generator?
3. Are there useful public nonlinear quotient invariants beyond ordinary shift symmetries, and are they already studied?
4. Can a genuinely novel mathematical framework survive equivalence checks independently of cryptography?
5. Is any defensible average-case hardness distribution and *genuinely private* recovery advantage available?
6. Could a future complete, byte-exact, independently challenged standalone KEM be constructed? No such current result exists.
7. Can exact NG-Q1 be formalized in Lean/Rocq/Isabelle with matching quantified claims?

**Verdict for the presently executed checkpoint:** strongest result is a scoped negative/algorithmic mathematical contribution with originality unresolved. Mission-level classification: **Outcome F (negative or inconclusive research result) for cryptography, with mathematically supported negative findings**; do not claim Outcome A/B/D/E. Future work may change this only through new evidence.


**Additional caution from random control:** NG-Q3 found zero public constant-shift dimension in 172 of 180 small uniform-source-form overlapping systems. Thus the new exact quotient algorithm does not currently give useful evidence of a generic public attack on the intended random global instance family. It nevertheless invalidates the proposed inference that large width and deficient shift rank alone imply hardness. Both statements can be true.


## Updated scientific verdict after NG-Q4

A model-specific exact probability theorem and global first-moment bound now strengthen the mathematical negative/structural knowledge. At dense independent overlap, lack of nonzero global additive shift is provably overwhelmingly likely **under the exact sampler stated**; the original attack may therefore lose its speed advantage on that distribution. This is not a KEM-security proof or a general lower bound on any algorithm. Basic linear-structure machinery and first-moment methods pre-exist SG-DIFRA.

**Mathematical novelty gate M2 remains not passed**; complete alternative mathematical framework, private trapdoor and IND-CCA/QROM construction are **not established**. Outcome at this checkpoint remains **F for cryptographic completion**, and **C for possible further mathematically substantive research** pending originality investigation. Do not submit or announce a new cryptosystem.

Next highest value: verify the exact global shift-tail theorem in a proof assistant, compare to published linear-structure/random-CSP theorems, probe alternative local-to-global invariants and independently randomized planted global witness distributions. If another candidate looks equivalent to existing cohomology, representation, or group-action structures, record the equivalence rather than renaming them.


## NG-Q6 / NG-Q7 verdict amendment

NG-Q6 gives an exact model-specific planted-witness uniqueness bound, and NG-Q7 publicly recovers solutions on all tested n>=6 dense independently sampled source-form fixtures despite absence of global shift symmetries. These findings **reject one possible security intuition**, not establish a new cryptographic security engine. They use known finite-field linear structures, standard first moments and classical constraint consistency.

**Highest-value next mathematical task:** investigate whether nonlinear overlap invariants beyond public additive symmetry exist and survive a *serious equivalence audit*. For cryptography, an independently motivated average-case hard distribution and genuinely private trapdoor remain absent. More finite success cases cannot substitute for universal proofs or independent cryptanalysis. Current result merits an accurate cryptanalytic/structural research report; M2 mathematical novelty and C1-C7 security success **not established**.
