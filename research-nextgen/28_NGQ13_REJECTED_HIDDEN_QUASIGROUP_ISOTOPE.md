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

- Source `experiments/ng_q13_isotope_no_go.py`, exact Git blob SHA `c3ddb3e6945f03d8bcc161a4f52de9567e7e9224`.
- Independent tests `experiments/test_ng_q13_isotope_no_go.py`, exact SHA `a48c170cadd5cda090b3e5cc9d6bec154a8c1bc5`.
- **Six** local unittest methods passed. Uniform random alpha/beta/gamma permutations on N=3,9,27; multiple public basepoints; the reconstructed normalized P matched the secret-formula verification on all N² pairs; recovered public equivalent coordinate maps passed all Cayley-table addition tests; recovered equivalent (alpha',beta',gamma') matched every original T entry; direct public row inversion and malformed non-Latin input rejection independently tested.
- The first test version covered P/coordinate recovery in 4 methods; a fifth method was added to challenge the stronger full equivalent-permutation reconstruction, and a sixth added a non-group-isotope Fano-plane control. Both source and test were rerun, and Git blob hashes match exact committed bytes.

```sh
cd research-nextgen/experiments
python -m unittest -v test_ng_q13_isotope_no_go
python ng_q13_isotope_no_go.py
```

The mathematics is conventional, not proof-assistant checked or independently peer reviewed; no CI claim. The public table is a strong information-disclosure assumption: no statement is made about succinct operation oracles or constructions with genuinely non-isotopic structure.

## Scientific decision and constructive next research question

**Reject** hiding an abelian group behind three arbitrary secret permutations as a new nonassociative mathematical foundation or private division trapdoor. It is **exactly an isotope of a known group** and can be publicly normalized when the operation table is explicit.

A legitimate future study must specify an algebraic structure that is *not* merely isotopic to a known group, define a genuinely non-reducible property and useful difficult problem, compare with loop/quasigroup classification and cryptanalytic prior art, and produce a meaningful secret-only recovery advantage. **No such original construction has been discovered at this checkpoint.**


## NG-Q13.3 — genuine non-group-isotope negative control: Fano Steiner quasigroup

**Definition:** Represent the seven nonzero binary three-vectors by public symbols `0,...,6`, i.e. symbol x represents x+1 in F2^3. Put `x⋆x=x`, and for distinct x,y put `x⋆y=((x+1) XOR (y+1))-1`. Distinct nonzero binary vectors have a nonzero, distinct XOR, giving a valid seven-element Latin square. The operation is commutative, idempotent, and satisfies the **Steiner identity** `x⋆(x⋆y)=y`.

**Proposition:** This public operation is **not an isotope of any group** of order seven, but its left/right division remains trivial from the public Latin-square rows/columns.

**Proof:** Every group of order seven is cyclic, hence isomorphic to (F7,+). Suppose `T(x,y)=gamma^(-1)(alpha(x)+beta(y))` for bijections to F7. Commutativity gives `alpha(x)-beta(x)=c` for all x. Idempotency gives `gamma(x)=alpha(x)+beta(x)=2 beta(x)+c`. Thus

`T(x,y)=beta^(-1)((beta(x)+beta(y))/2)`.

The Steiner identity would require
`beta(x⋆(x⋆y)) = (3 beta(x)+beta(y))/4 = beta(y)`
for all x,y. Multiplying by 4 yields `3 beta(x)=3 beta(y)`. Because 3 is invertible in F7 and beta is bijective, this is impossible. Therefore the Fano Steiner quasigroup is **not** group-isotopic. QED.

**Independent finite check:** For each of 49 public anchor pairs (x0,y0), construct the normalized operation P and test associativity for all 7^3 triples. **Zero of the 49** normalized operations is associative; 49/49 public divisions remain trivial because T is Latin. All other NG-Q13 tests still pass. The resulting combined NG-Q12+NG-Q13 test suite has **12/12 locally passing unit tests**. This does **not** invent the Fano plane or Steiner quasigroup.

**Research lesson:** 'Not isotopic to a group' is a meaningful structural distinction but **does not supply public-key secrecy or secret-only local division** under an explicit public operation table. A future mathematical proposal would additionally need a credible hard problem, private trapdoor, and explicit comparison with already studied Steiner/loop/quasigroup theory.
