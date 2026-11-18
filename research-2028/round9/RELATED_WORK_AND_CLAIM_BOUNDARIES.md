# Prior work on ternary zero-difference coverage

**Literature search date: 18 November 2026.** The degree classification in this round concerns a decision problem. One input specifies a vector polynomial by its component monomials over the field of three elements. The question is whether each challenge direction admits a collision. The witness may depend on the challenge.

**Follow-up on prior work, 18 November 2026.** Corollary 10 of Buss, Frandsen and Shallit gives a short alternative route to the quadratic coverage lower bound. The matrix specialization and its translation are written out in the [Round 10 literature comparison](../round10/RELATED_WORK.md#what-the-older-matrix-theorem-gives-for-round-9).

## What the decision problem measures

Let $P:\mathbb F_3^n\to\mathbb F_3^m$ have total degree at most $d$ in each component. Put $h_c=(1,c,0)$ for $c\in\mathbb F_3^k$, with a trailing zero block of length $n-k-1$. For a direction $h$ and target $b$, write

$$
\delta_P(h,b)=\#\{w\in\mathbb F_3^n:P(w+h)-P(w)=b\}.
$$

The question is whether $\delta_P(h_c,0)>0$ for every $c$. This notation makes two connections precise. Nyberg studied upper bounds on differential counts [1]. Ding and Tan studied functions for which the zero-output count is constant over every nonzero direction [2]. Here, counts may vary, only positivity matters, and the directions form a specified affine flat. Supplying the entire value table of $P$ would allow a direct scan polynomial in the table's length. The theorem measures complexity in the length of the sparse polynomial input.

## What the degree classification contributes

| Total degree cap | Worst-case classification | Role of the finite difference |
| --- | --- | --- |
| 1 | In $\mathrm P$ | For an affine map, the difference depends only on the direction. An affine identity in $c$ can be checked by its constant and linear coefficients. |
| 2 | $\mathrm{coNP}$-complete | Each fixed direction gives an affine system in the witness. A direction where the system is inconsistent certifies a NO instance. |
| 3 | $\Pi_2^{\mathrm P}$-complete | Each fixed direction gives quadratic equations in the witness. The reduction encodes a two-block quantified decision problem through the permitted directions of one vector polynomial. |

The ingredients have distinct precedents. Discrete derivatives lower degree [3]. The polynomial hierarchy and the role of bounded quantifier alternation in constraint satisfaction predate this construction [4,5]. The contribution claimed here is the classification under the simultaneous restrictions above, together with the output-dimension bound below. The reductions in this round are needed to establish completeness for these restricted inputs.

For the quadratic case, write $P=Q+L+b$ with homogeneous quadratic part $Q$, linear part $L$, and define $B_Q(u,h)=Q(u+h)-Q(u)-Q(h)$. Centering at $u=w+h/2$ gives the condition $B_Q(u,h)=-L(h)$. Thus the right-hand side must lie in the image of a matrix depending on $h$. Parameter-dependent rank and range compatibility are established topics [6,7]. For example, when the family $B_Q(\cdot,h)$ determines $L(h)$ uniquely, the induced map on the matrix family is range-compatible precisely when all the directions admit witnesses.

An inconsistent direction admits a linear functional $\lambda\in\mathbb F_3^m$ with $\lambda^\top B_Q(\cdot,h)=0$ and $\lambda^\top L(h)=1$. The second equality follows by scaling a nonzero pairing. For fixed $\lambda$ both conditions are affine in $c$. Enumerating the $3^m-1$ nonzero functionals therefore gives a deterministic $O(3^m\operatorname{poly}(N))$ algorithm, where $N$ is the encoded input length. In particular, logarithmically many outputs suffice for polynomial running time. Homogeneous quadratic maps give an even simpler test case: the two points $-h/2$ and $h/2$ have equal images in every direction.

## Comparison with SG-DIFRA and the limits of the theorem

The earlier restricted NCSG-DS theorem asks whether a specified difference constraint has a witness. Challenge coverage asks whether a potentially different witness exists for each of exponentially many directions specified compactly. The latter requirement explains the second quantifier block. A polynomial-time many-one reduction establishes a worst-case comparison. An unconditional strict separation from the earlier NP-complete decision problem would also require separating complexity classes. In particular, putting the cubic problem in NP would imply $\Pi_2^{\mathrm P}\subseteq\mathrm{NP}$ and collapse the polynomial hierarchy to NP.

The language specifies neither a distribution on maps nor a distributional witness-recovery experiment. Worst-case completeness leaves the success probability on any chosen sampler undetermined. Goldreich's local-function work illustrates the additional step of specifying a construction and stating its inversion conjecture explicitly [8]. This round supplies no average-case hardness reduction, secure KEM, concrete classical security level, or quantum security estimate.

## Search scope and priority

The search covered publicly indexed publisher records, author copies, arXiv and the Electronic Colloquium on Computational Complexity. Search terms included “zero difference balanced functions,” “differential spectrum zero column,” “discrete antiderivatives finite fields,” “quantified quadratic systems finite fields,” “bounded alternation quantified constraints,” “matrix space rank universal solvability,” and “range-compatible affine maps.” The comparison used primary papers from the returned records. These searches located the components described above. They did not establish earlier publication of the exact sparse ternary affine-flat degree trichotomy. Global priority remains unverified, including possible equivalent formulations under other terminology.

## Primary sources

1. Kaisa Nyberg, *Differentially uniform mappings for cryptography*, EUROCRYPT ’93, proceedings published 1994. Defines differential uniformity through upper bounds on counts for input and output differences. [DOI](https://doi.org/10.1007/3-540-48285-7_6) · [Author copy](https://users.ics.aalto.fi/knyberg/publications/diffuni.pdf)
2. Cunsheng Ding and Yin Tan, *Zero-Difference Balanced Functions With Applications*, 2012. Studies constant zero-difference counts across nonzero directions and constructs families with this property. [DOI](https://doi.org/10.1080/15598608.2012.647479)
3. Ana Sălăgean, *Discrete antiderivatives for functions over* $\mathbb F_p^n$, 2020 (online 2019). Proposition 1 gives degree reduction under differentiation and its behavior under coordinate changes. The paper also treats reconstruction from derivative functions supplied in specified representations. [DOI](https://doi.org/10.1007/s10623-019-00687-w)
4. Larry J. Stockmeyer, *The polynomial-time hierarchy*, 1976. Develops the hierarchy and exhibits a complete problem at its second level. [DOI](https://doi.org/10.1016/0304-3975(76)90061-X)
5. Michael Bauland, Elmar Böhler, Nadia Creignou, Steffen Reith, Henning Schnoor and Heribert Vollmer, *The Complexity of Problems for Quantified Constraints*, 2010. Classifies quantified Boolean constraint problems under restrictions on relations and alternation. [DOI](https://doi.org/10.1007/s00224-009-9194-6) · [Authors’ report](https://eccc.weizmann.ac.il/report/2007/023/download/)
6. Jonathan F. Buss, Gudmund S. Frandsen and Jeffrey O. Shallit, *The Computational Complexity of Some Problems of Linear Algebra*, 1999. Studies minimum and maximum rank over substitutions into a parameterized matrix, with complexity depending on the field and restrictions. [DOI](https://doi.org/10.1006/jcss.1998.1608)
7. Clément de Seguins Pazzis, *Quasi-range-compatible affine maps on large operator spaces*, published online 2015. Studies when a prescribed vector lies in the image of each operator of an affine matrix space, including the distinction between a witness depending on the operator and a fixed evaluation vector. [DOI](https://doi.org/10.1080/03081087.2015.1071316) · [Author preprint](https://arxiv.org/abs/1505.02315)
8. Oded Goldreich, *Candidate One-Way Functions Based on Expander Graphs*, 2000, revised 2011. Defines a distinct inversion candidate from overlapping local predicates and identifies its hardness as a conjecture. [DOI of revised chapter](https://doi.org/10.1007/978-3-642-22670-0_10) · [Author page with both versions](https://www.wisdom.weizmann.ac.il/~oded/ow-candid.html)
