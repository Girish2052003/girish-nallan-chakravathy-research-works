# Private trapdoor analysis — negative checkpoint

**No genuinely private trapdoor identified or demonstrated.**

The previously published NCSG local source form is publicly invertible under the Round-7/Round-8 hypotheses. NG-Q1 improves explicit public global search in high-width special cases, and NG-Q7 obtains public witnesses by standard constraint consistency on dense independently sampled global source-form systems.

NG-Q4's lack of nonzero additive shifts and NG-Q6's near-unique planted witness result are **not** evidence that the planted witness can be recovered only using private information. NG-Q7 demonstrates the danger of that inference: the publicly known factor tables and targets often suffice.

A valid future trapdoor proposal must provide a secret-only decapsulation or inversion advantage, explicitly address equivalent secret/witness recovery, survive public propagation, polynomial methods and other relevant attacks, define sampled input/output distributions and state exact correctness. The new experiments do not certify all independent NCSG constructions as insecure. They do **reject** promoting the tested dense distribution solely because it lacks symmetries and often has unique planted witnesses.

**Status:** C3 failed/not established; future trapdoor development remains OPEN. No KEM specified, security proof claimed, parameter security certified or formal checker passed.
