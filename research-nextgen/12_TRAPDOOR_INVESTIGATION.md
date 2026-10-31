# Private trapdoor analysis — negative checkpoint

**No genuinely private trapdoor identified or demonstrated.**

The previously published NCSG local source form is publicly invertible under the Round-7/Round-8 hypotheses. NG-Q1 improves explicit public global search in high-width special cases, and NG-Q7 obtains public witnesses by standard constraint consistency on dense independently sampled global source-form systems.

NG-Q4's lack of nonzero additive shifts and NG-Q6's near-unique planted witness result are **not** evidence that the planted witness can be recovered only using private information. NG-Q7 demonstrates the danger of that inference: the publicly known factor tables and targets often suffice.

A valid future trapdoor proposal must provide a secret-only decapsulation or inversion advantage, explicitly address equivalent secret/witness recovery, survive public propagation, polynomial methods and other relevant attacks, define sampled input/output distributions and state exact correctness. The new experiments do not certify all independent NCSG constructions as insecure. They do **reject** promoting the tested dense distribution solely because it lacks symmetries and often has unique planted witnesses.

**Status:** C3 failed/not established; future trapdoor development remains OPEN. No KEM specified, security proof claimed, parameter security certified or formal checker passed.


## NG-Q8 new asymptotic trapdoor rejection

For independently generated complete-triple source-form functions (or pair-codegree logarithmic anchor hypergraphs) with explicit public tables, [NG-Q8](23_NGQ8_PUBLIC_RECOVERY_THEOREM.md) constructs a public-only polynomial-time planted-witness finder with provably overwhelming recovery probability as n grows, conditional only on the specified sampling model. Therefore **mere possession of the planted assignment cannot be a credible private trapdoor on these distributions**. This is stronger than the earlier finite NG-Q7 campaign; still not a universal impossibility theorem for other mathematical structures or ciphertext designs.

Status: **REJECT these specific planted-witness distributions as proposed secret-only inversion engines**. A different genuine trapdoor, mathematical novelty and correct complete KEM interface are still absent.
