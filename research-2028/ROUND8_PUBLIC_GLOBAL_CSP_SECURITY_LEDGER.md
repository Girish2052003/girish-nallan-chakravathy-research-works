# Round 8 — Public global witness recovery and security gate

**Date:** 10 October 2026  
**Status:** Complete *scoped* adversarial proof and tested regression. **No KEM security proof, secure parameter set, or submission closure.**  
**Prior rounds:** [Round 7 first-difference local inversion](../research-2028/attacks/public_first_difference_local_inversion.py) remains valid. Nothing in Round 8 conceals, deletes, or repairs its unconditional attack. The original local MaxEnt construction is **not** an acceptable standalone cryptographic trapdoor.

## 1. Exact threat model and source preservation

An adversary sees public factor scopes $S_i\subseteq \{1,\ldots,n\}$, each output target $t_i$, and the corresponding explicitly enumerable ternary relations
$R_i = \{x\in\mathbb{F}_3^{S_i}: f_i(x)=t_i\}$.
The global task is to find $s\in\mathbb{F}_3^n$ satisfying $s|_{S_i}\in R_i$ simultaneously. Hidden matrices $A_i,B_i$, finite-difference directions and potential tables are NOT adversary inputs. Round 7 already proves the original source-form local $f_i$ can be inverted publicly when its complete table is available.

A real KEM would require a specific **key generation, public key, secret key, ciphertext, shared-key derivation, encapsulation and decapsulation** interface. None has been supplied for an active NCSG-only KEM after the earlier GF(1024) construction was rejected. Thus a generic CSP attack is **not** evidence of an IND-CCA break of a nonexistent completed KEM. The claimed new cryptographic trapdoor and three final bit-security levels remain undefined.

## 2. Theorem: the standard low-width elimination attack

Construct the **primal graph** $G$ on the global variables, with edges between all variables appearing together in one public constraint scope. For a specified variable elimination order, write $w$ for the induced width, i.e. the largest number of still-uneliminated neighbors of any eliminated variable.

**Theorem R8.1 (unconditional, standard variable-elimination consequence).** For any publicly given *explicit* ternary factor tables and an elimination order of width $w$, a deterministic public-only algorithm outputs a satisfying assignment or an exact unsatisfiability certificate by table elimination in time $\operatorname{poly}(n,m,L)3^{w+1}$, with factor tables of at most $3^w$ entries, where $L$ is the public explicit-input length. Accordingly, public NCSG witness search is polynomial in the explicit input size whenever $w=O(\log(n+L))$.

**Proof.** Eliminate variable $v$. Let the bucket contain all constraints mentioning $v$. Their union of scopes has at most $w+1$ variables. For every assignment to the remaining bucket variables, test all three choices of $v$; keep the residual assignment exactly when some value satisfies every bucket constraint, remembering one successful value. Replace the bucket by the resulting existential projection. The original system is satisfiable exactly when the projected system is, because existential projection preserves and reflects solution existence. Apply this equivalence inductively. If a projection is empty, the system is unsatisfiable. Otherwise reconstruct the complete witness by reversing the eliminations and consulting the recorded choices. Each bucket processes at most $3^{w+1}$ assignments and polynomial-factor table lookups, proving the bound. QED.

**Limits:** This is a standard constraint-programming result and is **not claimed as newly invented theory**. If the public instances have hidden, unavailable scopes or only succinct descriptions that require expensive expansion, charge those costs or prove a different model. The theorem gives an **upper bound on a known attack**, not an adversarial lower bound. It says nothing about quantum query bounds, side-channel behavior, or arbitrary high-width instances.

## 3. Consequences for one-wayness claims

**Corollary R8.2 (restricted distribution).** If a proposed planted-witness hardness assumption promises hard witness recovery on public instances whose primal-graph width is $O(\log L)$, and its distribution supports efficient public reconstruction of such an order, the claim is false for that restricted distribution: Theorem R8.1 gives a public polynomial-time witness finder. If an easy recognizable subdistribution occurs with nonnegligible probability in a broader generator, it provides a corresponding nonnegligible witness-finding attack against the broader distribution. Its mere existence, without sufficient probability mass, does not prove average-case insecurity of the full generator.

A requirement to resist **this one attacker** at nominal work $2^\lambda$ would suggest $w+1\gtrsim\lambda/\log_2 3$ after accounting for polynomial costs and input encoding. This is only a necessary screening condition, **not** a security-level estimator: other attacks could be much faster, and high treewidth never suffices to prove hardness. No mathematical proof currently rules out all polynomial-time attacks on the user's proposed NCSG direction, nor is any finite evidence capable of proving a construction “unbreakable.”

**Public hints are public.** A public key or ciphertext may legitimately carry helper information for algorithms, but anything computable from them is also computable by a passive adversary. Neither a public truth table nor a publicly reconstructible affine shift can be called a secret decapsulation trapdoor. A secret trapdoor must be precisely specified, necessary to decapsulation and unreachable under a clearly articulated computational model/assumption.

## 4. Implemented attack and results

Code: [public_global_treewidth_witness_recovery.py](attacks/public_global_treewidth_witness_recovery.py). Runs on Python standard library alone, with deterministic fixtures.

The regression builds the original source-form ternary local function $f(x)=Au_L+\Delta_a Q(u_R)$ with random invertible hidden matrices $A,B$. Two independent local functions are embedded into global factors sharing **one actual global variable**. Targets are planted to ensure global satisfiability, but the solver receives **only public scopes and relation tables**, not the generating secrets or planted solution. It separately checks unsatisfiable contradictions, dozens of random small CSPs against independent exhaustive ground truth, and disconnected products.

| Local source geometry | $(k,d,r)$ | 2-factor global variable count | Public observed induced width | Witness recovered? |
| --- | --- | ---: | ---: | --- |
| SGD-R1 | $(5,3,2)$ | 9 | 4 | Yes |
| SGD-R2 | $(7,4,3)$ | 13 | 6 | Yes |
| SGD-R3 | $(9,5,4)$ | 17 | 8 | Yes |

Those runs are a **deliberately restricted global-instance experiment**, not evidence that the full archived three profile constructions have these global widths. The historical SGD-R1/R2/R3 security ratings remain **UNSUPPORTED**, and all reported attack complexity should be indexed by explicit public data size.

Run:

\`\`\`sh
python research-2028/attacks/public_global_treewidth_witness_recovery.py
\`\`\`

**Important scientific boundaries:** (i) Passing randomized tests does not prove no defect in the code; (ii) the proof of Theorem R8.1 addresses the mathematically defined public-factor model, not program verification of Python semantics; (iii) the archived GF(1024) dense-label cryptanalysis remains a *separate* proven asymptotic attack from Round 5; (iv) no exhaustive classical or quantum attack portfolio exists.

## 5. Round-7 carry-forward checklist

1. The Round-7 right-inversion theorem and public fiber bijection are untouched.
2. Source local MaxEnt predication is rejected as a one-way trapdoor for every public local table; no random masking has repaired it.
3. The exact finite source bounds for R1/R2/R3 concern a different coordinate-recovery claim, not KEM bit security.
4. No statement falsely promotes a finite source-form test to an IND-CCA, QROM, or quantum hardness theorem.
5. The original author-contributed finite-difference geometry, historic attack narrative, mathematics and source manuscript are preserved. The new Round-8 public variable elimination is clearly attributed to classical CSP methodology, not mislabeled as newly invented mathematics.

## 6. Blockers to any conference-security closure

| Claim | Verifiable status at Round 8 | Required closure evidence |
| --- | --- | --- |
| Complete NCSG-only KeyGen/Encaps/Decaps with error handling | **Absent** | Byte-exact specification and runnable reference implementation |
| Actual original private decapsulation-only trapdoor | **Not established** | New construction and public/secret information-flow analysis |
| Correctness and negligible failure | **Not established** | Full correctness proof and adversarial malformed-ciphertext tests |
| Classical IND-CPA and adaptive IND-CCA | **Not established** | Defined games and complete justified reductions plus attack analysis |
| Quantum/QROM IND-CCA | **Not established** | Proper quantum proof with concrete losses and query accounting |
| Classical/quantum $\lambda=128,192,256$ equivalent security | **Not established** | Independent attack estimates of actual parameter distributions |
| No polynomial attack / exponential lower bound | **Not established** | Appropriate complexity evidence; impossible to certify by tests alone |
| Publication-ready EUROCRYPT 2027 submission | **No** | 2027 deadline had already passed by 10 Oct 2026; anonymization and scientific gates unmet |

Scientific verdict: **ROUND 8 ATTACK ANALYSIS REPRODUCED; FORMAL KEM SECURITY CLOSURE REFUSED ON THE EVIDENCE.** Research can be disseminated as accurately labeled cryptanalysis without misrepresenting a broken or unconstructed KEM as secure.

## 7. Literature/novelty caution

**Established source:** R. Dechter, *Bucket Elimination: A Unifying Framework for Reasoning*, *Artificial Intelligence* 113(1–2), 41–85 (1999), DOI: https://doi.org/10.1016/S0004-3702(99)00059-4. The CSP variable-elimination upper bound is established methodology; it is not a cryptographic novelty claim. The original source manuscript's MaxEnt geometry and source-specific tests are separately credited to their authors. A conference contribution must make a positive, falsifiable novelty case after a qualified prior-art survey. The IACR's [author guidance](https://www.iacr.org/docs/author.pdf) states that general IACR conference submissions are anonymous; public versions and credited author drafts must not be mistaken for the anonymous PDF.
