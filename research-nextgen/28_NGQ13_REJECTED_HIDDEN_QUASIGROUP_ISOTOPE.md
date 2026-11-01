# NG-Q13 — Rejected nonassociative/quasigroup novelty candidate

**Status:** A deliberately separate mathematical candidate outside finite-difference CSPs, tested and rejected as already-established group-isotopy theory and publicly reversible with explicit operation tables. **Not a newly invented mathematical structure, KEM or security proof.**

## Candidate and strict prior-art question

Let `G=(F3)^m` be an elementary abelian group of order `N=3^m`. Let `alpha,beta,gamma:G→G` be *independently chosen arbitrary secret bijections*. Define a publicly given binary operation

`T(x,y)=gamma^(-1)(alpha(x)+beta(y))`.

Each public T table is a Latin square (quasigroup): fixing x, or fixing y, leaves a permutation of the opposite input. For generic choices of the three secret bijections, the public T may appear nonassociative/noncommutative. The tempting story would be that the hidden isotopy and nonlinear multiplication produce a new private inversion structure. **The story is mathematically false under these exact assumptions.**

Group and quasigroup *isotopy*, Latin squares, and their cryptographic uses are well-established. Primary literature includes Jack Allsop, *Isotopisms of quadratic quasigroups*, Algebraic Combinatorics 9(1), 75–94 (2026), DOI 10.5802/alco.467; and Chauhan, Gupta and Verma, *Quasigroups and their applications in cryptography*, Cryptologia 45(3), 227–265 (2021), DOI 10.1080/01611194.2020.1721615. Neither the basic structure nor the public normalization below warrants a foundational novelty claim.

## Theorem NG-Q13.1 — public group-law normalization

Pick any publicly known x0,y0 in G. Put

`R(x)=T(x,y0)`; `L(y)=T(x0,y)`; `p=T(x0,y0)`.

The quasigroup property makes R and L bijections, whose inverses are obtained directly from a public table column and row. Now define a new **public** operation

`P(a,b)=T(R^(-1)(a), L^(-1)(b))`.

Then `P` is an abelian group law with identity p, and

`gamma(P(a,b))=gamma(a)+gamma(b)-gamma(p)`.

In particular, `h(a)=gamma(a)-gamma(p)` is a group isomorphism from the publicly normalized `(G,P)` to ordinary `(G,+)`. The operation P can be constructed with O(N²) public table operations.

**Proof:** From `gamma(R(x))=alpha(x)+beta(y0)`, `gamma(L(y))=alpha(x0)+beta(y)`, and `gamma(p)=alpha(x0)+beta(y0)`, if `a=R(x)` and `b=L(y)`, then

`gamma(P(a,b))=alpha(x)+beta(y)=gamma(a)+gamma(b)-gamma(p)`.

Because gamma is a bijection, this formula is precisely addition transported by h, yielding associativity, commutativity, identity p, inversion, and exponent three. QED.

## Theorem NG-Q13.2 — fully equivalent public isotopy key recovery

A deterministic attacker given only the complete public T table can compute **an equivalent triple of bijections (alpha',beta',gamma')** such that

`T(x,y)=gamma'^(-1)(alpha'(x)+beta'(y))`

for every pair (x,y), without seeing the original secret alpha,beta,gamma.

**Proof:** Construct P and p by NG-Q13.1. Because P is a publicly represented elementary abelian group of size 3^m, find an isomorphism `psi:(G,P)→F3^m` by public generation: start with the identity p; select any element outside the subgroup generated so far, adjoin its three cosets, and give their members a new coordinate in {0,1,2}; continue until N elements are labeled. Verify the resulting coordinate map against **every** public P table entry; the process terminates because every nonzero elementary abelian group element has order three, and all newly adjoined cosets are disjoint.

Set

`gamma'(z)=psi(z)`, `alpha'(x)=psi(R(x))`, `beta'(y)=psi(L(y))`.

NG-Q13.1 implies `P(R(x),L(y))=T(x,y)`, so homomorphicity of psi gives

`gamma'(T(x,y))=alpha'(x)+beta'(y)`.

All three resulting maps are bijective; hence they form a **complete equivalent secret isotopy decomposition**, verified on all N² table entries. Public normalization and coordinate recovery run in time polynomial in the explicit N×N table representation. QED.

**This is not a claim of polynomial time in succinct input length m** when the operation table is not given. An algorithm polynomial in N can be exponential in m. Non-isotopic arbitrary quasigroups are excluded, and the implementation explicitly rejects non-Latin or non-elementary-abelian input.

## Separate elementary no-trapdoor observation

For any *explicit* Latin-square operation table T, solving `T(x,y)=z` for y given x,z is publicly possible by looking across the known row x; exactly one entry equals z. This does not require the secret alpha,beta,gamma. Thus hiding an isotopy is not by itself a trapdoor for the basic left or right division operation.

Neither theorem proves that every quasigroup cryptosystem is insecure: an entirely different cryptographic scheme, succinct description or additional hardness assumption needs its own analysis.

## Executed adversarial evidence

- Source `experiments/ng_q13_isotope_no_go.py`, exact Git blob SHA `229f0c6d06c5dd429f4cf8747567c64f9ee116a5`.
- Independent tests `experiments/test_ng_q13_isotope_no_go.py`, exact SHA `762d82b136ba5e50f035d182afcd672ca5a64783`.
- **Five** local unittest methods passed. Uniform random alpha/beta/gamma permutations on N=3,9,27; multiple public basepoints; the reconstructed normalized P matched the secret-formula verification on all N² pairs; recovered public equivalent coordinate maps passed all Cayley-table addition tests; recovered equivalent (alpha',beta',gamma') matched every original T entry; direct public row inversion and malformed non-Latin input rejection independently tested.
- The first test version covered P/coordinate recovery in 4 methods; a fifth method was added to challenge the stronger full equivalent-permutation reconstruction. Both source and test were rerun, and Git blob hashes match exact committed bytes.

```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q13_isotope_no_go
python ng_q13_isotope_no_go.py
```

The mathematics is conventional, not proof-assistant checked or independently peer reviewed; no CI claim. The public table is a strong information-disclosure assumption: no statement is made about succinct operation oracles or constructions with genuinely non-isotopic structure.

## Scientific decision and constructive next research question

**Reject** hiding an abelian group behind three arbitrary secret permutations as a new nonassociative mathematical foundation or private division trapdoor. It is **exactly an isotope of a known group** and can be publicly normalized when the operation table is explicit.

A legitimate future study must specify an algebraic structure that is *not* merely isotopic to a known group, define a genuinely non-reducible property and useful difficult problem, compare with loop/quasigroup classification and cryptanalytic prior art, and produce a meaningful secret-only recovery advantage. **No such original construction has been discovered at this checkpoint.**
