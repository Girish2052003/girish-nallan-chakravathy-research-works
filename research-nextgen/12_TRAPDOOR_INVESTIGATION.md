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


## NG-Q16/NG-Q17/NG-Q18: why noisy/partial public ratios are not a demonstrated trapdoor

Noisy flat group ratios do **not** inherently create secret-only inversion: NG-Q16 publicly reconstructs true relative group labels when each pair has enough clean two-hop evidence, including explicit adversarial and stochastic conditions. Those algorithms use no private labels or planted coordinates.

Absolute root X_0 of iid uniform group secrets remains exactly uniform conditional on relative-only publication (NG-Q17). This reflects a **global gauge symmetry**, not computationally difficult public inversion. A sender who only receives relative public information does not thereby acquire a mathematical mechanism for computing a key that depends on an unobserved absolute gauge; a legitimate complete KEM correctness reduction would have to specify and justify such a mechanism separately.

At sparse observation densities with isolated vertices (NG-Q18), *intercomponent* relative offsets cannot be recovered from the public data under uniform independent secrets, but the uncertainty arises from absent identifying measurements rather than from an original one-way problem with a private trapdoor. Without a new independent mathematical primitive, correctness proof and formal indistinguishability security experiment, **reject** this noise/gauge/sparsity reformulation as a new secure KEM construction.


## NG-Q19: public full-matrix equivalent-secret reconstruction

Hidden invertible vertex matrices X_v over full GL(k,Fp) do not supply demonstrated private inversion in exact public graph transport B_uv=X_u^-1 H_uv X_v. Public spanning tree gives one root T; public linear algebra computes its entire intertwiner space. For p>k, random combinations yield an invertible root with provably high probability per independent attempt, recovering an **equivalent globally valid vertex assignment**. Equivalent secrets may not equal planted X; if a hypothetical KEM relies on a truly secret quantity not invariant under this equivalence, a complete scheme and its key-derivation algorithm would need separate analysis. No such KEM is defined.

Reject hidden noncommutative matrices as cryptographic asymmetry merely because GL(k,Fp) has enormous formal group order. This is established module-isomorphism algebra, not a credible new secret trapdoor. No final C3 pass.
