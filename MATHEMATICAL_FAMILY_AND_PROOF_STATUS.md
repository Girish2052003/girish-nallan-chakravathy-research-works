# SG-DIFRA: canonical mathematical family and proof status

**Scope:** Current NCSG-only research direction. This document is a descriptive taxonomy and audit guide, not a new proof, independent peer review, novelty certification or a secure KEM.

## One mathematical home

**Umbrella discipline:** finite-field algebraic constraint-satisfaction problems (CSPs) and discrete finite-difference algebra.

**Project-specific descriptive family:** **NCSG finite-field discrete-differential constraint systems**.

**NCSG = Nonlinear Constraint-System Geometry**, the expansion in the active manuscript. It does **not** mean noncommutative structured gradient, and the research has not established noncommutative-group hardness. SG-DIFRA is the canonical project name; SG-DOFRA is not the documented name.

This family name is descriptive, **not** an assertion that a new internationally recognized mathematical field, the world's toughest problem or a secure cryptographic primitive has been established.

## Defining mathematical mechanism

Over a finite field F_p, a finite difference is

    Delta_a Q(w) = Q(w+a) - Q(w)  (in F_p).

The active mathematics connects (1) local nonlinear finite-difference constraints, (2) the geometry and algebra of their solution sets or fibers, (3) global witness problems formed by overlapping constraints, and (4) analysis of whether a supposed secret shortcut remains private given the full public constraints.

A small example over F_3: let Q(0)=0, Q(1)=1, Q(2)=0 and direction a=1. The differences at 0, 1 and 2 are 1, 2 and 0. Their sum is 0 modulo 3. This is an exact cyclic-derivative identity, NOT an encryption or one-wayness proof.

**Easy explanation:** Each public equation is a little arithmetic puzzle. Several puzzles share variables, so the same secret assignment would have to solve them together. SG-DIFRA studies the structure of these linked puzzles and the possibility of an actually private shortcut. The current repository proves multiple mathematical properties and public attacks, but has **not** shown a cryptographically secure private shortcut.

## Family boundaries

| Area | Relationship |
| --- | --- |
| Finite-field algebra, discrete derivatives, algebraic combinatorics | Defining mathematics |
| Algebraic CSPs and complexity theory | Defining global decision/witness setting |
| Multivariate polynomial methods | Closely related analysis; not exclusively an MQ scheme |
| Graph width and variable elimination | Important public-attack methods |
| Reed-Solomon/GRS, hidden-MDS, LPN/noisy linear labels | **Historical and rejected KEM iterations**, not active security engines |
| Lattice cryptography, isogenies, noncommutative groups | Not the active mathematical family |
| Post-quantum KEM | The aspirational application; **not a proved capability** |

Relevant neighboring research includes Dechter's bucket elimination (1999) and Hair–Sahai's 2026 PKE from high-corruption CSPs (https://arxiv.org/abs/2604.10479). Citing prior art is not incorporating another KEM into SG-DIFRA. Independent literature assessment is required before claiming mathematical originality.

## What the mathematical record establishes

The following are **written mathematical arguments in the active draft**, supported by finite code tests where specified. The proofs have **not been machine-checked in a proof assistant or externally peer-reviewed**.

| Result | Exact scope | Implication |
| --- | --- | --- |
| Restricted NCSG-DS NP-completeness | Section 3, polynomial Boolean reduction from 3-SAT | Worst-case decision complexity, not average-case encryption security |
| Ternary MaxEnt fiber size, affine-line structure, derivative entropy | Sections 4–4.2, original source-form maps | Exact algebra and public geometric leakage, not pseudorandomness |
| Discrete zero-curl/integrability and derivative-image rank | Section 12.5, finite-field tables and independent directions | Reconstruction/compatibility identities, not one-wayness |
| Public local right inversion and translation | Theorem 4.6, explicit public tables | Local secrecy fails in this model |
| Public-evaluation local inversion and uniform fiber sampling | Theorem 4.8 and Corollary 4.8a; complexity polynomial in 3^d and oracle evaluation | Local inversion remains easy in the specified regime |
| Local correctness-to-key recovery | Corollary 4.8b; precise uniform-input ciphertext ct=f(x) wrapper | This wrapper is insecure if correctness is high; not a universal KEM result |
| Public global constraint solving | Theorem 12.9; explicit factors, elimination width w | Standard time upper bound poly(L,n,m)*3^(w+1); low width can be easy |
| Public global constant-shift witness recovery | Theorem 12.10; complete local tables and targets in the shift image | Even some high-width distributions are publicly invertible |
| Low-degree ideal ciphertext rank test | Section 12.6, specific rejected proposal | Public distinguisher breaks that candidate |
| Fixed-field hidden-GRS attacks | Historical Sections 5–9 | Invalidates historical asymptotic claims, not a new active NCSG KEM |

A theorem being valid within its **stated model** is different from demonstrating cryptographic security. The 15 recorded successful research verification programs test bounded examples and specified calculations, not every implementation path or adversarial algorithm.

## Unresolved security and novelty obligations

There is **no completed active NCSG-only KeyGen/Encaps/Decaps specification or secure replacement**, no demonstrated indispensable private trapdoor, no established average-case NCSG hardness assumption or full reduction, no proof of IND-CPA or IND-CCA/QROM security, and no independently certified 128/192/256-bit parameter sets. The historical SGD-R1/R2/R3 labels must not be presented as new validated security levels. No overall proof-assistant verification, universal attack lower bound, or independent claim that this is the world's hardest mathematical family exists.

Any future security claim needs a precise public and secret algorithm, distribution, correctness theorem, attack analysis, justified computational assumption and cryptographic reduction. Renaming the family changes none of those requirements.

## One-sentence research description

> SG-DIFRA investigates Nonlinear Constraint-System Geometry, a finite-field discrete-differential algebraic constraint family, as a foundation for possible new cryptography; its scoped mathematics and cryptanalytic attacks are documented, but a secure post-quantum KEM has not yet been established.

## Evidence trail

- [Active 2028 research draft](manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.md)
- [NCSG-only status and theorem ledger](research-2028/NCSG_ONLY_RESEARCH_STATUS.md)
- [Round-8 CSP proof and security ledger](research-2028/ROUND8_PUBLIC_GLOBAL_CSP_SECURITY_LEDGER.md)
- [Round-8 follow-up and test record](research-2028/ROUND8_FOLLOWUP_RESULTS.md)
- [Recorded 15-program verification evidence](research-2028/evidence/round8-followup/README.md)

**Integrity rule:** Harmonize terminology without rewriting theorem hypotheses, hiding attack results, promoting tests to proof certificates or converting an archived MDS design into an active NCSG-only KEM.
