# What Round 9 proves and what it assumes

Date: 18 November 2026. See the [complete mathematical arguments](CHALLENGE_COUPLED_DIFFERENTIAL_SOLVABILITY.md).

## Proven statements and conditional comparisons

| Statement | Status and exact dependence |
| --- | --- |
| Linear challenge coverage is in P | Written unconditional coefficient argument. |
| Quadratic challenge coverage is coNP-complete | Written unconditional reduction from 3-CNF UNSAT and polynomial verification of a missing direction. |
| Cubic challenge coverage is Pi2P-complete | Written unconditional reduction from a two-block quantified Boolean circuit and the matching quantified-verifier upper bound. |
| A single specified cubic challenge is NP-complete | Written unconditional circuit-SAT reduction. |
| The cubic universal problem is outside NP | Conditional on Pi2P not being contained in NP; for example, the usual noncollapse assumption for the polynomial hierarchy suffices. |
| No deterministic polynomial-time algorithm solves the entire quadratic/cubic family | Follows if P != NP; this is a complexity assumption, not an unconditional lower bound. |
| Quadratic coverage has an algorithm taking O(3^min(k,m) poly(L)) time | Written unconditional public algorithm. This is an UPPER bound on computational cost. |
| Homogeneous quadratic maps plus constants have a public collision in every direction | Written unconditional midpoint identity; this is an explicitly easy subclass. |
| Circuit responses correspond one-to-one with collision witnesses | Exact theorem for each fixed ternary challenge on the constructed cubic instances. |

Here P, NP, coNP and Pi2P are standard complexity classes. The completeness
proofs do not assume P != NP. A strict comparison of the named classes does.
The code validates finite instances of the reductions; the proofs are
ordinary mathematical arguments, not certificates checked by Lean, Rocq,
Isabelle or another proof assistant. Independent agent review is not external
peer review.

## The changed question

Earlier restricted NCSG-DS asks for one common witness to specified
differential constraints. Round 9 asks whether every designated translation
admits some collision of the same map. A response may change with the
challenge. The higher complexity classification belongs to this universal
decision question. It is not a theorem that an individual ciphertext, a
randomly generated polynomial or an old SG-DIFRA parameter set has become
harder to attack.

An input where every challenge succeeds is a YES instance, not a practical
algorithm for finding the response to an arbitrary challenge. Conversely,
a single NO certificate does not describe the solution-search behavior on
cryptographically generated inputs.

## Cryptographic obligations still open

This round defines no cryptographic instance distribution, average-case
inversion assumption, secret trapdoor, KEM algorithms, IND-CPA/IND-CCA game
reduction, QROM argument or concrete classical/quantum security level.

A future cryptographic continuation must give an efficient public sampler
and its complete public view, a precise secret recovery advantage, the
attacker's success game, correctness with quantified failure probability,
and attacks on the actual sampled distribution. A reduction from a
worst-case quantified decision language does not supply those items.

In particular, the historical SGD-R1/R2/R3 profiles retain their previous
status. This new theorem does not restore rejected GRS/LPN components,
invalidate the old public-inversion attacks or justify any claim of
128-, 192- or 256-bit security.

## Novelty statement

The exact formulation, degree-sensitive reductions and witness accounting
are new additions to this repository. The [primary-source comparison](RELATED_WORK_AND_CLAIM_BOUNDARIES.md)
distinguishes them from established differential counts, quantified CSPs,
and parameter-dependent linear algebra. The targeted search did not locate
this exact trichotomy, but it does not establish global originality.

**Defensible research description:** SG-DIFRA Round 9 studies universal
challenge coverage for sparse ternary finite-difference systems and gives
explicit reductions establishing a degree-sensitive worst-case complexity
classification. Cryptographic hardness and global priority remain open.
