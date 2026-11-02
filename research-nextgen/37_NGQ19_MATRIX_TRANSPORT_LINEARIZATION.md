# NG-Q19 — Public matrix-group graph transport linearization and no-go

**Date:** 2026-11-02. **Scientific status:** exact conventional mathematical argument plus 12 passing locally executed tests, without proof-assistant verification or external peer review. This is NOT an original foundational algebra, KEM, quantum hardness result or private trapdoor.

## Model

Let p be prime, k>=1, G=GL(k,F_p). A graph with vertices v publishes invertible matrices H_uv and B_uv for each oriented edge, related by **B_uv = X_u^(-1) H_uv X_v**, for unknown vertex matrices X_v in G. Every public matrix entry is available to the adversary. Finding ANY valid equivalent vertex assignment is the public search task; recovering the original representative is a different question. No KEM shared secret has been defined.

## NG-Q19.1 — public linear intertwiner reduction

Choose a public spanning tree in each connected component and multiply public H and B labels along oriented root paths to obtain H_v and B_v. The NG-Q14 telescoping identity gives **X_v = H_v^(-1) T B_v** with one invertible root matrix T per component.

For each non-tree edge e=(u,v), put public cycle matrices A_e=H_u H_e H_v^(-1) and D_e=B_u B_e B_v^(-1). The edge equation becomes **T^(-1) A_e T = D_e**, equivalently **A_e T = T D_e**. The latter is a set of homogeneous LINEAR equations in the k^2 unknown entries of T. Gaussian elimination gives a public vector-space basis W_1,...,W_d for all solutions T, regardless of the graph width and the noncommutativity of matrix multiplication.

If d=0, no invertible T exists, so the system is provably UNSAT. If d>0, an invertible T, if found, reconstructs a complete public graph witness via the tree identity and can be checked against every original public edge. The existence of some nonzero solution does NOT imply an invertible solution.

## NG-Q19.2 — scoped randomized polynomial-time public recovery for p>k

Suppose the intertwiner space contains at least one invertible T_0, as every planted instance does. Pick coefficients c_i independently uniformly in F_p and set T=sum_i c_i W_i. The polynomial P(c)=det(sum_i c_i W_i) is NONZERO since one coefficient vector evaluates to det(T_0) != 0, and its total degree is k.

By the Schwartz–Zippel bound, **Pr[T singular] <= k/p**. If p>k, each public random trial therefore finds an invertible solution with probability at least 1-k/p; after N independent trials, the failure probability is at most **(k/p)^N**, conditional on existence of a valid root. The linear system, uniform coefficient sampling, inverse checks and reconstruction require time polynomial in graph size, k, log(p), and N **assuming the input prime field has already been validated**. An independently supplied primality certificate or a separate polynomial-bit-complexity primality algorithm would be needed for a fully poly(log p) field-validating implementation. The reference program uses simple trial-division primality validation, which is **NOT polynomial in log(p)**; therefore its end-to-end execution is not claimed polynomial in the bit length of arbitrarily large p. For c connected components, the overall probability that some planted component fails is bounded by c*(k/p)^N by a union bound.

For p<=k the probability bound is trivial and this elementary implementation does NOT claim a general efficient decision algorithm. Existing algorithms for module isomorphism over finite fields address the broader mathematical problem, but this experiment does not reproduce their full guarantee.

**Soundness distinction:** a verified invertible witness always satisfies the public equations. If random trials find none, report INCONCLUSIVE, not UNSAT; UNSAT may be reported directly only when the linear solution space is zero-dimensional. A different globally valid witness from the originally planted X is still a successful equivalent-public-representation attack, not automatically a KEM secret-key recovery attack.

## Counterexamples and executable evidence

A=I and D=[[1,1],[0,1]] have a nonzero space of singular intertwiners T but no invertible T. Random sampling yields INCONCLUSIVE; it must not declare UNSAT. By contrast, A=I and D=2I over F_5 force T=0 and give a genuine unsatisfiability certificate.

Locally written source: experiments/ng_q19_matrix_transport.py, SHA from git hash-object **b1635b98795f544da2652669b0f383c1c1e256bd**.
Local independent tests: experiments/test_ng_q19_matrix_transport.py, SHA **8d8bc8335e3265989ffd39b3bf94a7109ee428e9**.

**12/12 locally executed Python 3.13.5 tests passed**, including all 36 ordered pairs in GL(2,F_2) compared with independent full finite-group enumeration; exact 625-matrix invertible fraction 96/125 in Mat_2(F_5); small nullspace brute comparison; randomly hidden simultaneous transformations k=2,3,4,6; full planted-graph public recovery for k=2,3,5,7 at p=5,11,17,101; disconnected and isolated vertices; contradictory cycles; nonzero but singular-only solution space; malformed/composite-field controls. Demonstration found verified public witnesses, often different from the planted representatives.

To reproduce: from research-nextgen/experiments run **python -m unittest -v test_ng_q19_matrix_transport** and **python ng_q19_matrix_transport.py**.

**IMPORTANT SOURCE-INTEGRITY RULE:** The SHA values above are locally executed source hashes. Compare them to the fetched GitHub code blob hashes before asserting GitHub-byte identity. If source differs, independently run the committed version and state the mismatch; do not claim false matching. No CI/proof assistant or total historical suite was executed in this checkpoint.

## Exact prior art, equivalence and conclusion

Alexander L. Chistov, Gábor Ivanyos and Marek Karpinski, *Polynomial Time Algorithms for Modules over Finite Dimensional Algebras*, ISSAC 1997, 68–74, DOI **10.1145/258726.258751**, https://doi.org/10.1145/258726.258751, explicitly treat module isomorphism as simultaneous nonsingular matrix conjugacy. Ivanyos and Qiao, *Algorithms Based on Star-Algebras ...*, SIAM J. Comput., DOI **10.1137/18M1165682**, https://doi.org/10.1137/18M1165682, develop related module-isomorphism methods for polynomial isomorphism and other applications. The determinant argument is a standard application of polynomial identity testing. These are established mathematics.

**Decision NG-C16: REJECT hidden full GL(k,F_p) exact graph transport as a genuinely new mathematical foundation or demonstrated private trapdoor.** For p>k planted instances are recoverable by the explicit public one-sided randomized witness finder with the bound above; for smaller p our tool gives no universal guarantee. No official mathematical migration or new KEM is justified. S01 stays ACTIVE, M2 and C2/C3 remain NOT PASSED, and all subsequent KEM gates remain blocked. Record negative results and advance the next-session handoff without inflating stage numbers.
