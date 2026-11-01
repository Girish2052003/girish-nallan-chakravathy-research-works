# Computational hardness evaluation — NG-Q4 / NG-Q6 / NG-Q7

**Status: NO defensible average-case hardness assumption or original KEM security.** This is a first analysis of one explicitly defined research distribution, not a general security conclusion.

## Precisely defined planted-source search distribution

For a security-index candidate `n`, let global variables range over `F_3^n`; for each of the `m=C(n,3)` three-element scopes independently sample a uniform `B_i in GL(3,3)`, uniform scalar potential table `Q_i:F_3^2->F_3`, and uniform nonzero scalar `A_i`. Use fixed nonzero direction `a=(1,0)`, and publish the complete explicit local tables `f_i(x)=A_i u_L+Delta_a Q_i(u_R)`, with `u=B_i x`. Choose a uniformly random global witness `s` independent of factor sampling and publish `t=F(s)`.

**Search problem:** Given only scopes, all public factor tables and `t`, output *any* `x` satisfying `F(x)=t`. Input representation length is polynomial in n for this particular dense fixed-local-arity family. This is **not** an encryption/KEM security game. Even finding a valid witness need not imply correct KEM decapsulation for an unspecified future design.

## Observations established or tested

- NG-Q4: a fixed nonzero local shift survives with exact probability 5/39. For fully independently sampled complete-triple scopes, nonzero global additive shifts disappear with explicitly bounded high probability. This **removes one public shortcut**, not all public solving strategies.
- NG-Q6: a fixed distinct pair of local inputs collides with exact probability 4/13. Under the stated independent planted sampling, full global non-uniqueness is bounded by an exact first moment; probability becomes small with dense overlap. This **shows near-unique solutions**, not one-wayness.
- NG-Q7: **public pair-projection consistency** (known CSP filtering) reconstructs planted global witnesses in every tested complete-triple instance for n=6,7,8,9,10,12, without original secrets or constant-shift directions. For n=5, 29/30 trials recovered. These are finite data, not a distribution-wide polynomial-time success theorem.
- The full complete-triple primal graph is `K_n`, width `n-1`; graph width alone did not predict the observed easy recovery.

## Relevant algorithmic upper bounds and caveats

- Plain exhaustive global witness search: at most `3^n` full assignments and polynomial factor evaluation each.
- NG-Q1 public additive quotient search: `3^(n-dim D) * poly(L)`, often no improvement for this dense independent sampler.
- Classical variable elimination: `poly(L,n) * 3^(w+1)` for an available induced-width-w ordering; complete triples have width n-1.
- NG-Q7 public pair consistency: polynomial in explicit input length per completed propagation, but has no proven general witness-recovery success probability over all independently sampled factors. It reports **inconclusive**, never a false successful witness.
- Multi-user, quantum, spectral, polynomial-elimination, Gröbner, and malformed ciphertext attacks have not been comprehensively performed here.

## Scientific decision

**Do not promote a dense, nearly unique, zero-shift global NCSG instance family as a hard distribution.** The positive experimental public recovery is a material attack, and uniqueness is not an inversion hardness proof. The candidate is **unsuitable for a positive trapdoor/KEM hardness claim at this checkpoint**, although a fully asymptotic public pair-recovery theorem is not established.

Relevant prior art: Alan K. Mackworth, *Consistency in networks of relations*, *Artificial Intelligence* 8(1), 99–118, 1977, DOI 10.1016/0004-3702(77)90007-8. Methodology is not novel CSP theory. Independent peer-review and proof-assistant formalization have not occurred.


## NG-Q8 decisive asymptotic public-recovery obstruction

The previous NG-Q7 result only established **bounded experimental** public recovery on dense independent source-form factors. [NG-Q8](23_NGQ8_PUBLIC_RECOVERY_THEOREM.md) now proves a high-probability public **one-pass** recovery result for the exact independent r=1,d=2 ternary distribution: each wrong projected pair survives a relevant local factor with exact probability 37/52. With pair codegrees d_ij, failure is at most `8 sum_(i<j)(37/52)^d_ij`; for every triple scope this is `8*C(n,2)*(37/52)^(n-2)`, negligible as n grows. An anchor-based distinct-scope construction uses `O(n^2 log n)` factors and is likewise publicly easy in this model with appropriate codegree.

**Hardness decision:** The proposed dense/anchor overlapping independent-source families cannot be invoked as credible asymptotically one-way planted-witness problems in the specified explicit-table model: a polynomial-time public adversary now has a proved overwhelming recovery probability. Sparse low-pair-codegree systems, correlated factor secrets, succinct local functions and different nonlinear foundations remain separate open questions; no general NCSG impossibility theorem is claimed.


## NG-Q9 general fixed-arity obstruction

NG-Q9 extends the **possibility of high-probability public pair-projection recovery** from the exact (r,d)=(1,2) sampler to arbitrary fixed r,d>=1 over F3, under fully independent uniform B,Q local source forms, public complete local truth tables and pair codegrees large enough to compensate for the *strictly positive but possibly minuscule* local rejection lower bound epsilon_(r,d). The general bound is `8 sum_(i<j)(1-epsilon_(r,d))^d_ij`. Complete k-uniform scopes imply a negligible public recovery failure bound for **k>=3**; **k=2** needs repeated constraints to grow pair coverage. Do not apply these asymptotic results to finite profiles lacking a nontrivial quantitative bound or to correlated/succinct NCSG designs.

The claimed independent-source high-overlap planted-witness hardness is therefore contradicted for these exact growing distributions by an explicit public polynomial-time algorithm, even though no general statement about every NCSG variant is proved.


## NG-Q10 / NG-Q11 additional unconditional public shortcuts

**NG-Q10:** Any public CSP whose every factor touches only two shared hubs and one other leaf, with arbitrary local predicates, is solved by enumerating q² hub assignments and independent leaf checks. This is classical bounded-treewidth cutset conditioning; probabilistic source-form hiding or O(n log n) factor count does not create a hard problem on that support graph.

**NG-Q11:** Over F3, any source-form family with nonlinear-right dimension d=1 is **affine**, no matter how nonlinear the initial Q function appears. Any global public explicit-table system assembled from such local factors reduces to public linear algebra, regardless of primal graph treewidth or random generator independence. **Reject** d=1 as a witness-inversion hardness foundation. For d>=2, finite-difference degree bound `max(1,2d-1)` exposes public algebraic structure, but a distinguisher alone is **not** a fast solver or cryptographic one-wayness refutation.

## NG-Q14 / NG-Q15: no hardness from noncommutative public exact transport

The public exact model B_uv=x_u^-1 H_uv x_v is a nonabelian gain-graph switching system. A spanning-tree gauge collapse replaces n unknown vertices per connected component with one public simultaneous conjugator t. This refutes any claimed hardness based merely on many vertices, graph density, noncommutative edge multiplication or unique hidden assignment. A finite enumeration attack costs O(|G| times graph size), **not** polynomial in succinct log |G|.

For full explicit symmetric groups S_k, NG-Q15 upgrades to a polynomial-in-k,n,m public recovery/UNSAT algorithm. Matching the orbits of colored permutation actions provides a verified root conjugator without k! enumeration. This particular representation is therefore **not a defensible hard witness problem**, under exact noiseless public H/B labels. Neither theorem is a lower bound for other group problems nor a quantum security result. No mathematically independent average-case hard problem remains established.


## NG-Q16/NG-Q17/NG-Q18: recovered information versus truly absent information

Under complete/near-complete **flat** public relative group observations, noisy pair labels remain publicly reconstructible in polynomial group operations under specific deterministic or independent-noise assumptions (NG-Q16), even on noncommutative S_k represented by explicit permutations. For fixed |G|, fixed positive rho and fixed replacement rate epsilon<1, the finite Hoeffding error bound vanishes asymptotically as n grows; for large |G| keep the explicit |G|-1 factor or use the stronger clean-majority event.

Conversely, even perfect recovery of every ratio leaves the original absolute group root X_0 **unidentifiable** under iid uniform secrets (NG-Q17); this is gauge symmetry, not computational hardness. If the graph is disconnected, intercomponent ratios have no information in the public observations; NG-Q18 quantifies isolated vertices in sparse G(n,p) and their obstruction. Missing information and a provably hard inversion problem are not interchangeable.

No novel average-case computational hardness assumption, private-trapdoor advantage or security-parameter quantum reduction emerges from switching between dense noisy recovery and sparse information-theoretic failure.
