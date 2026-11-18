# What Round 10 proves about a potential KEM

Round 10 asks whether one pair of functions can answer every challenge using two separate views. An encapsulation mechanism samples a fresh public ciphertext and establishes a key on honestly generated public keys. This note compares the two tasks. All complexity assertions below are classical and concern the stated input encodings. Sections 3 and 4 use the standard model, with public polynomial-time algorithms and finite random tapes. [Round 10 definition and proofs](../round10/README.md) · [NIST SP 800-227, definitions and security experiments](https://doi.org/10.6028/NIST.SP.800-227)

## 1. A constructive bound for any prescribed difference

**Proposition 1.** Let $P$ be an explicitly listed vector polynomial over $\mathbb F_3$, in reduced form, of total degree at most three. Let $t$ be the total number of degree-three monomials across its output rows. Given a displacement $h$, an arbitrary target $d$, and specified values for any subset of the starting coordinates, a deterministic algorithm either finds a compatible $z$ satisfying

$$
P(z+h)-P(z)=d
$$

or determines that none exists. It needs at most $3^{2t}$ affine-system solves and $3^{2t}\operatorname{poly}(L)$ total time, where $L$ includes all the input data.

**Proof.** For each square-free cubic $x_i x_j x_k$, choose two of its coordinates for enumeration. For each reduced cubic $x_i^2 x_j$ with $i\ne j$, choose $x_i$. These are the only possibilities, since individual exponents in reduced ternary polynomials are at most two. Form the union of all chosen coordinates, so there are at most $2t$ of them. Retain the given values of any coordinates in this union that are already pinned. Enumerate the trits for the rest.

For any one assignment, each cubic monomial evaluated at $z$ is affine in the remaining unknowns. The same holds at $z+h$, since $h$ is fixed. For a lower-degree product, the identity

$$
(z_i+h_i)(z_j+h_j)-z_i z_j=h_i z_j+h_j z_i+h_i h_j
$$

shows that its difference is affine even before enumeration. The identity also covers squares. Subtract $d$ in each row and impose the remaining pinned values. Gaussian elimination over $\mathbb F_3$ decides the resulting affine system and returns a solution when it is consistent. Every possible solution falls into one enumerated assignment, and each returned solution satisfies the original equations. This proves the bound.

**The published one-term form.** Round 10's cubic graph compiler has only the exceptional term $-sMN$. The two helper coordinates $M,N$ are stationary and the clock displacement is one. Its difference is exactly $-MN$. Enumerating $M$ alone therefore suffices. At most **three** affine-system solves recover a witness or establish inconsistency, for any target and any consistent set of prescribed starting values. If $M$ or $N$ is already known, a single affine solve suffices. For an arbitrary cubic monomial with arbitrary displacements, Proposition 1 instead gives up to nine solves for one term. The same algorithm accommodates fixed local response values, including prefix constraints. Repeated feasibility checks can therefore return the lexicographically first witness in polynomial time when $t$ is bounded.

These statements apply when the published description, the displacement, the target and the prescribed values are public inputs. In particular, a design that derives its shared key by applying a public function to **any** such witness, with the same key for every witness, has a public polynomial-time key computation on the one-term family. A design using the lexicographically first witness has the same issue. A proposed scheme that encodes information about one distinguished witness separately needs its own agreement and hiding arguments.

## 2. How much of the universal problem reaches a ciphertext?

**A finite list.** Suppose a public instance explicitly lists polynomially many challenges and requires consistent local responses on that list. Guess one trit per distinct left address and one per distinct right address, then guess full starting-coordinate completions for the listed challenges. Equality of repeated local answers is built into this representation. Direct evaluation verifies every difference in polynomial time. Consequently this explicit-list feasibility language is in NP. Completeness for the unrestricted, succinctly universal NEXP language cannot transfer by a polynomial-time many-one reduction to this explicit-list language, since NP is properly contained in NEXP. The explicit-list observation alone gives no average-case algorithm for the joint constraints. [Nondeterministic time hierarchy](https://staff.science.uva.nl/r.dehaan/complexity2025/files/lecture4.pdf)

**A planted public key.** If a generator first chooses a pair of valid local strategies and outputs a public map satisfied by them, every honestly generated map answers YES to the universal decision question. One could still posit a search assumption involving a hidden strategy on a distribution of such maps. This requires specifying the generated distribution and defining which response or key counts as a successful recovery. A worst-case decision theorem establishes neither of these properties.

**The length of the private description.** A table with an $n$-trit input and one ternary output has $3^n$ entries. A private circuit of polynomial size may describe some such tables compactly. A different assertion would be that *every* YES map of the NEXP-complete one-cubic language has two such circuits, with one fixed polynomial bound in input length. Under that assertion, guess both circuits and universally quantify the polynomial-length challenge. Evaluate their outputs and apply Proposition 1 with these two trits fixed. This is a $\Sigma_2^{\mathrm P}$ procedure for the entire language and would imply $\mathrm{NEXP}\subseteq\Sigma_2^{\mathrm P}$. This conditional statement makes no restriction on using short secrets for a deliberately chosen key distribution.

## 3. A boundary for direct reductions to honest session-key recovery

Take any KEM with public polynomial-time encapsulation, polynomially bounded encapsulation randomness, deterministic decapsulation, and **perfect correctness**. Perfect correctness here means that decapsulation outputs the encapsulated key for every honestly generated key pair and every permitted encapsulation random tape. Include the security parameter in unary in the instance when needed. For legal $pk$ and $c$ in the image of encapsulation, the recovered key is unique. Indeed, any two encapsulations giving the same $c$ must produce the output of the same deterministic decapsulation with a fixed compatible secret key.

In the Python control, uniform sampling from a non-power-of-two set uses rejection and has expected polynomial running time. Each supported outcome still has a short public certificate. Supply the encapsulation preimage vector, or the first accepted random draw encoding its rank, and recompute the same ciphertext and key directly. The argument below only needs such short, efficiently verifiable certificates.

**Proposition 2.** Suppose a deterministic polynomial-time procedure decides a language $L$ given oracle access to *exact* session-key recovery. On each input, every query on the truthful computation path is promised to use a legal public key and a ciphertext in the image of encapsulation for that key. The queries may be adaptive. Then $L\in\mathrm{NP}\cap\mathrm{coNP}$.

**Proof.** To certify the final output bit, supply the answer $k_i$ and an encapsulation random tape $r_i$ for each successive query $(pk_i,c_i)$. Simulate the procedure. Check by public evaluation that encapsulation under $pk_i$ using $r_i$ produces exactly $(c_i,k_i)$, then return $k_i$ to the procedure. The first query is legal. Its verified answer must be the unique truthful key, so the next query is again on the truthful path. Induction proves the same for every query. Conversely, a truthful transcript has such certificates because every queried ciphertext is in the image. There are polynomially many polynomial-size certificates. Verifying a transcript ending in one certifies membership, and verifying a transcript ending in zero certifies nonmembership.

It follows **unconditionally** that this particular deterministic reduction cannot decide the unrestricted Round 10 NEXP-complete language. Otherwise that language would be in NP and every NEXP language would reduce to an NP language, contrary to the nondeterministic time hierarchy. The statement covers exact recovery on valid inputs with perfect correctness. A randomized reduction to an average-case IND distinguisher is a different hypothesis. Malformed inputs and nonzero decryption-failure probabilities also require separate arguments. The proof does not resolve those cases. Restricted worst-case-to-average-case reductions have a broader research literature. [Akavia, Goldreich, Goldwasser and Moshkovitz, STOC 2006](https://people.csail.mit.edu/akavia/2006-stocAGGM.pdf)

## 4. A related boundary for an exact public support test

For canonical encodings and a fixed $\kappa$-bit key length, define

$$
E=\{(pk,c,k):\exists r\quad \mathrm{Encaps}(pk;r)=(c,k)\}.
$$

The equation writes the ciphertext before the key. The inclusion $E\in\mathrm{NP}$ follows by supplying $r$ and rerunning public encapsulation. It does not require validity recognition for arbitrary public keys. On an honest public key and an honestly sampled ciphertext, perfect correctness gives a unique matching key. The indicator of $E$ therefore accepts a real challenge key with probability one and an independent uniform key with probability exactly $2^{-\kappa}$. This is an exact computationally unbounded reference distinguisher. Membership in NP alone gives no efficient implementation for a real adversary.

A deterministic polynomial-time many-one reduction from the whole Round 10 NEXP-complete language to this exact support test is impossible by the same hierarchy argument. An adaptive reduction that asks membership and nonmembership questions about $E$ does not satisfy Proposition 2's transcript hypotheses, since a negative support answer need not have a short certificate.

## Consequence for the design goal

For a reduction from a proposed KEM, the useful direction is an algorithm that takes a successful KEM adversary and uses it to solve the proposed hard task with quantified probability and cost. A construction can target a *new* average-case trapdoor problem, provided it specifies efficient public sampling and encapsulation, private recovery, correctness, and a security argument for the actual ciphertext and key distributions. Neither fixed-instance witness recovery nor the NEXP decision theorem supplies that trapdoor. Concrete claims such as $2^{191}$ operations require an attack model and parameter-specific analysis in addition to an asymptotic reduction.
