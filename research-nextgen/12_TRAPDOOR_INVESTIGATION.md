# Private trapdoor analysis — negative checkpoint

**No genuinely private trapdoor identified or demonstrated.**

The previously published NCSG local source form is publicly invertible under the Round-7/Round-8 hypotheses. NG-Q1 improves explicit public global search in high-width special cases, and NG-Q7 obtains public witnesses by standard constraint consistency on dense independently sampled global source-form systems.

NG-Q4's lack of nonzero additive shifts and NG-Q6's near-unique planted witness result are **not** evidence that the planted witness can be recovered only using private information. NG-Q7 demonstrates the danger of that inference: the publicly known factor tables and targets often suffice.

A valid future trapdoor proposal must provide a secret-only decapsulation or inversion advantage, explicitly address equivalent secret/witness recovery, survive public propagation, polynomial methods and other relevant attacks, define sampled input/output distributions and state exact correctness. The new experiments do not certify all independent NCSG constructions as insecure. They do **reject** promoting the tested dense distribution solely because it lacks symmetries and often has unique planted witnesses.

**Status:** C3 failed/not established; future trapdoor development remains OPEN. No KEM specified, security proof claimed, parameter security certified or formal checker passed.


## NG-Q8 new asymptotic trapdoor rejection

For independently generated complete-triple source-form functions (or pair-codegree logarithmic anchor hypergraphs) with explicit public tables, [NG-Q8](23_NGQ8_PUBLIC_RECOVERY_THEOREM.md) constructs a public-only polynomial-time planted-witness finder with provably overwhelming recovery probability as n grows, conditional only on the specified sampling model. Therefore **mere possession of the planted assignment cannot be a credible private trapdoor on these distributions**. This is stronger than the earlier finite NG-Q7 campaign; still not a universal impossibility theorem for other mathematical structures or ciphertext designs.

Status: **REJECT these specific planted-witness distributions as proposed secret-only inversion engines**. A different genuine trapdoor, mathematical novelty and correct complete KEM interface are still absent.


## NG-Q9 general rejection condition

For *fixed* source-form local arity k=r+d and uniform independently sampled B,Q in the public explicit-table model, NG-Q9 proves a positive lower bound epsilon_(r,d) on the local ability to reject a wrong pair. With sufficiently large pair codegrees, a fully public polynomial-time attacker reconstructs the planted s with high probability. Thus a planted assignment is **not** a defensible secret-only trapdoor on that high-codegree distribution, even for other fixed r,d. Weak conservative bounds at practical n may give no conclusion. The argument does not cover arbitrary correlated generators or all possible new mathematical trapdoors.


## NG-Q10 / NG-Q11: further rejection of fake private trapdoors

Two-anchor star schemes have a deterministic public complete solver; no planted secret advantage. Any ternary NCSG source-form scheme with d=1 has a deterministic public Gaussian solver on any overlap pattern, including dense/high-treewidth families; neither secret generating B, A, Q nor nonlinear-looking Q notation hides a witness inversion trapdoor. A recovered witness need not equal an original planted s when the global map has multiple preimages, and no full KEM exists to evaluate decapsulation secrecy. For d=2 only a local degree distinguisher was proved, so no KEM claim follows.

## NG-Q14 / NG-Q15: rejected graph-transport trapdoor

Secret vertex group values in B_uv=x_u^-1 H_uv x_v are not a private inversion advantage when public exact H/B labels are available. On a tree, choosing one public root already reconstructs a valid full vertex assignment; on cycles, unknown roots reduce to simultaneous conjugacy. An S3 example has a **unique original planted assignment**, yet public exact inversion recovers it. For explicit full S_k permutations even the conjugacy step is polynomial in k by orbit-action matching. This makes the entire tested noncommutative transport family unsuitable as the presumed **private** trapdoor engine.

A noisy, partial, subgroup-restricted or succinctly encoded alternative would be a **different mathematical problem**, requiring fully new definitions and public attacks. Group synchronization with noise is already extensively studied and cannot be treated as inherently novel or quantum hard.
