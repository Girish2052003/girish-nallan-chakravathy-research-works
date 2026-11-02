# NG-Q20 — Hankel-basis reconstruction versus membership-only needle barrier

**Research date:** 2026-11-02. **Type:** Independent evaluation of a proposed noncommutative word-product public evaluator as a next-generation mathematical candidate. **Status:** Two scoped conventional proofs and 10 passing local Python tests, NOT novel foundational mathematics, a post-quantum hardness proof, machine-checked theorem, independent human review or a KEM.

## 1. Candidate: word-dependent tensor / matrix-product evaluations

Fix a finite field F_p for prime p, alphabet Σ of size s>=2, and dimension d>=1. A secret representation consists of a row α in F_p^(1xd), matrices M_a in F_p^(dxd) indexed by a in Σ, and column β in F_p^(dx1). For each word w=a_1...a_t in Σ*, its scalar output is

f(w) = α M_(a_1) ... M_(a_t) β, with f(empty)=αβ.

Matrices need NOT commute, and need NOT be invertible. The proposed public information is an evaluator that allows an outsider to request f(w) on chosen words. This is an **abstract membership-oracle model**, not a concrete publicly encoded key. The important access assumption must not be silently replaced with the normal cryptographic public-key model, where an evaluator must be implemented from a finite public key without exposing a planted secret.

A candidate may claim that recovering an equivalent collection of hidden M_a from public f is hard merely because matrix products do not commute. NG-Q20 tests that claim, then independently tests the oracle-access boundary.

This is **the classical weighted finite automaton / recognizable formal power series** model, not an invented category of algebra.

## 2. Definitions

Define the word-indexed (generally infinite) Hankel matrix H_f by H_f(u,v)=f(uv), where u,v range over Σ*. Its rank over F_p is r. The representation has dimension d so r<=d. A **minimal** realization means r=d.

A finite *Hankel basis* is an explicitly supplied pair of d-word lists P=(p_i), S=(s_j) such that the dxd matrix H=(f(p_i s_j)) is invertible in F_p. The public evaluator returns values f(w). **Providing or finding P,S is part of the actual input-access assumption.**

For each a in Σ, define H_a=(f(p_i a s_j)), the public row h_S=(f(s_j)) and column h_P=(f(p_i)).

## 3. Theorem NG-Q20.1 — reconstruct ALL word outputs from a public full-rank Hankel basis

If f has Hankel rank exactly d, the public evaluator f and a PROVIDED Hankel basis P,S permit reconstruction of an equivalent d-dimensional representation (α',N_a,β'):

N_a = H^(-1) H_a,
α' = h_S,
β' = H^(-1) h_P.

Then for EVERY word w in Σ*, f(w)=α' N_w β'. This reconstruction uses at most (s+1)d²+2d public membership evaluations, each on a word p_i a s_j, p_i s_j, p_i or s_j. If basis words have lengths <=d-1, queries have length <=2d-1. The field arithmetic after obtaining values is polynomial in s,d,log p for an already validated field.

**Proof:** Write R for the dxd matrix with i-th row α M_(p_i), C for the dxd matrix with j-th column M_(s_j) β. Then H=RC and H_a=R M_a C. Since H is invertible, both R and C are invertible. Therefore H^(-1)H_a = C^(-1) M_a C, h_S=α C, and H^(-1)h_P=C^(-1) β. For every word w, multiply these identities and cancel adjacent C/C^(-1): α' N_w β' = α C (C^(-1) M_w C) C^(-1) β = α M_w β=f(w). In particular the reconstructed internal matrices may differ from the planted ones, but the entire public input-output function is identical. QED.

**Public-query complexity is CONDITIONAL on P,S already being available.** It is an incorrect generalization to claim the above d² query bound automatically includes discovering a full-rank basis using only membership queries. Also, testing that a proposed dxd H is invertible does not by itself establish that the GLOBAL infinite Hankel rank is exactly d; the theorem requires the rank-d promise (or an independently established minimal representation upper bound).

## 4. Lemma NG-Q20.2 — existence of short Hankel basis, but NOT efficient search

In every minimal d-dimensional representation, there exist P,S of size d whose words have length at most d-1.

**Proof:** Let R_l be the linear span of rows α M_w for |w|<=l. If α=0 then f=0 and d cannot be a positive minimal dimension. Hence R_0 has dimension one. If R_l=R_(l+1), the span is invariant under right multiplication by each M_a and cannot grow in later steps. Since minimal realization has reachability span dimension d, dimensions must strictly grow until d, achieved no later than l=d-1. Similarly the column spans of M_w β (with word length <=l) reach all d no later than d-1 by the same invariance argument. Select d independent reachable rows indexed by P and d independent observable columns indexed by S; their product H=RC is invertible. QED.

This is a combinatorial EXISTENCE lemma. Naively enumerating all s^0+...+s^(d-1) words to locate the basis is **exponential in d when s>=2**, and nothing in the lemma improves that search complexity. A public evaluator that exposes H and index sets would be a stronger interface than a generic membership oracle.

## 5. Theorem NG-Q20.3 — needle family defeats unconditional polynomial membership-only discovery

For alphabet Σ with s>=2 and each hidden target word u in Σ^L, define f_u(w)=1 if w=u and f_u(w)=0 otherwise (over any field). This series has Hankel rank **exactly d=L+1**.

**Proof of minimal rank:** A d-state realization uses basis states 0,...,L: α=e_0^T and β=e_L. The transition matrix for symbol a advances i→i+1 only if the i-th symbol of u is a, and sends all mismatches to zero, with no outgoing transition from L. Therefore f_u(w) is one exactly at word u and zero elsewhere, giving rank <=L+1. Conversely choose P=(u[:i])_(i=0..L) and S=(u[i:])_(i=0..L). Then H_f(P_i,S_j)=1 iff i=j: if i !=j, the concatenated word has length L+i-j != L, hence value zero; if i=j its concatenation is u. This identity submatrix has rank L+1. QED.

Suppose u is uniform among s^L possible L-symbol words, the public oracle returns ONLY f_u(w), and an attacker makes at most q<s^L adaptive membership queries followed by one final guess for u. Every query of length not L returns zero regardless of u, and each query of length L can rule out at most ONE target. With q distinct candidate queries, the probability of hitting u is at most q/s^L; if no hit, one final guess succeeds on at most one of the remaining candidates, total

**Pr[correctly identify u] <= (q+1)/s^L.**

The same bound holds for randomized adaptive algorithms after averaging their internal randomness. A deterministic algorithm promised only needle instances needs at least s^L-1 tests in the worst case to identify u with certainty. If the class additionally includes the zero function and it must distinguish that zero function, s^L queries are needed to certify it against all needles. Thus membership-only exact learning can require exponential query complexity in minimal dimension d=L+1. QED.

**MAJOR cryptographic limitation:** This does NOT demonstrate a secure public-key primitive. The oracle model assumes a public evaluator can implement the secret needle indicator while withholding u. A real freely inspectable public-key implementation might reveal u. No trapdoor algorithm, receiver/sender key agreement or quantum security game is given. Exponential black-box *information* complexity is not automatically exponential cryptographic hardness, and standard query models differ from ordinary public-key representations.

## 6. Independent testing and original development correction

New executed source: experiments/ng_q20_hankel_oracle.py; local SHA `530bb4ff34140a28650e5c873efec06f3702fe33`. New test: experiments/test_ng_q20_hankel_oracle.py; local SHA `d53970b6eab6aa6048e17e4c1905087917f766b4`. Confirm these exact Git blob values AGAINST GITHUB before claiming byte identity.

**10/10 Python 3.13.5 unit test methods passed** after a local test-driven correction. They include exhaustive 16 distinct binary needles of length four with public Hankel-basis reconstruction, needle Hankel ranks L+1 for L<=6, exact no-hit query indistinguishability, random minimal finite-field d=2,3,4 realizations across p=2,3,7,11, openly NONCOMMUTING matrices, random words and exhaustive outputs up to length eight, malformed basis/oracle rejection and exact q-guess bound fractions.

**Preserved initial failed test:** The first needle generation API inferred its alphabet as the letters that appear in u. For needle u='aaaa', the test's advertised public alphabet ('a','b') then contained 'b' which the internal transition map lacked, causing a ValueError. This was an implementation/modeling inconsistency, not a counterexample to the theorem. Revised needle(word,p,alphabet=...) now supports an explicit alphabet, including symbols absent from the needle, and all 10 methods pass. Do not claim the first run passed.

Demo with d=3 over F7 reconstructed equivalent functions with only **15 distinct** public oracle values when a basis was already known, and validated all words length <=8. No formal proof assistant, CI, external human peer review or complete KEM experiment was run.

Reproduction:

    cd research-nextgen/experiments
    python -m unittest -v test_ng_q20_hankel_oracle
    python ng_q20_hankel_oracle.py

**The exploratory_hankel_basis function is explicitly exponential** in d and used only for tiny test fixtures. Its successful use in random toy experiments is NOT evidence of a polynomial basis-finding algorithm for every function.

## 7. Rigorous prior-art / equivalence assessment

**J. W. Carlyle and A. Paz**, *Realizations by stochastic finite automata*, Journal of Computer and System Sciences 5(1), 26–40 (February 1971), DOI 10.1016/S0022-0000(71)80005-3, https://www.sciencedirect.com/science/article/pii/S0022000071800053. This seminal finite-Hankel-rank-to-linear-realization characterization predates this project.

**Artem Kaznatcheev and Prakash Panangaden**, *Weighted automata are compact and actively learnable*, Information Processing Letters 171, 106133 (October 2021), DOI 10.1016/j.ipl.2021.106133, https://www.sciencedirect.com/science/article/pii/S0020019021000478. Explicit learning over arbitrary fields using membership AND equivalence queries, showing why the two query models must not be conflated.

**Laure Daviaud and Marianne Johnson**, *Feasability of Learning Weighted Automata on a Semiring*, Logical Methods in Computer Science 21(3), 2025, DOI 10.46298/lmcs-21(3:15)2025, https://lmcs.episciences.org/16316. Discusses mathematical limitations of weighted-automata learning under different semirings and query access.

**Giuseppe D'Alconzo**, *Monomial isomorphism for tensors and applications to code equivalence problems*, Designs, Codes and Cryptography 92 (2024), 1961–1982, DOI 10.1007/s10623-024-01375-0, https://link.springer.com/article/10.1007/s10623-024-01375-0. Tensor-isomorphism reductions are established mathematics as well, so merely writing word products as tensor networks does not create foundational novelty.

The concrete elementary word-needle bound and constructive Hankel formulas are **scoped rediscoveries/applications of classic recognizable series and learning-theory insights**, not asserted to be new global mathematical results.

## 8. Decision and exact handoff gate

**NG-C17 (tensor/word-product oracle secret representation): REJECT as a newly original mathematical framework.** If a full Hankel basis is publicly supplied and rank is d, all outputs have an equivalent recovered linear representation. If only membership queries are supplied, the needle family demonstrates potentially exponential query-only search but **no cryptographically implementable trapdoor or independently hard computational problem**. More clever parameter increases, names, or encoding of old finite-state matrix products are not a mathematical migration.

**NO STAGE/GATE PROMOTION.** S01 remains ACTIVE; S02–S12 not accepted for a new original KEM. M2 and C2/C3 not passed, M5 unchecked. Continue exploring genuinely new mathematical objects and invariants, or separately improve independent baseline/proof-assistant evidence. Preserve all tests, rejected candidates and the distinction between *membership black-box query security* and an inspectable public key.
