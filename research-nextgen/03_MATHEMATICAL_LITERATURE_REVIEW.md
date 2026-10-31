# Focused mathematical prior-art notes — incomplete landscape investigation

**Not a worldwide novelty certification.** This page records only the sources actually identified while investigating public constant-difference directions and quotient-search decompositions. Full comparative study of topology, chain complexes, representation theory, noncommutative algebra, coding theory, lattices, etc., remains open.

1. P. Charpin and G. Kyureghyan, *When does G(x) + γTr(H(x)) permute F_(p^n)?*, **Finite Fields and Their Applications** 15 (2009), pp. 615–632. The published discussion treats linear structures and a decomposition through a lower-dimensional linear map. Bibliographic metadata/precise theorem need independent primary-source verification. Related text: https://www.researchgate.net/publication/267662759_When_does_GxgTrHx_permute_p_n
2. *Permutations via linear translators*, **Finite Fields and Their Applications** 45 (May 2017), pp. 19–42, DOI: 10.1016/j.ffa.2016.11.009. Already studies translation directions and induced permutations. Author names and complete theorem details require inspection: https://doi.org/10.1016/j.ffa.2016.11.009
3. *On derivatives of polynomials over finite fields through integration*, **Discrete Applied Mathematics** 217, Part 2 (30 January 2017), pp. 294–303, DOI: 10.1016/j.dam.2016.07.025. Discusses derivatives and linear structures: https://doi.org/10.1016/j.dam.2016.07.025
4. Rina Dechter, *Bucket Elimination: A Unifying Framework for Reasoning*, **Artificial Intelligence** 113 (1999), pp. 41–85, DOI: 10.1016/S0004-3702(99)00059-4. Classical efficient low-width CSP solver, already credited in the SG-DIFRA manuscript.

**Equivalence danger:** `D={h : F(x+h)-F(x) is constant in x}` is the established linear-structure idea, not an original structure merely because it is called a global shift space. Quotienting a vector space by a linear subspace, extending a basis, solving linear equations, and enumerating a transversal are also standard algebra and algorithms.

**Potential project-specific contribution being assessed:** applying the exact quotient search to the author's *overlapping public NCSG factor maps*, with a constructive high-width, shift-rank-deficient family defeating a proposed security intuition. This may still be an elementary consequence of known theory. It must not be advertised as a new foundational mathematics.

**Research comparison still required:** published algorithms for vectorial-function linear structures, additive group-action symmetry reduction, CSP symmetry/quotient variable elimination, average-case planted CSP work, and succinct-oracle complexity. A novel cryptographic hardness assumption is neither proposed nor supported in this checkpoint.


## Primary-source follow-up — linear structures and first moments (31 October 2026)

**Checked the actual mathematical statement** of Pascale Charpin and Gohar Kyureghyan, *When does G(x)+γTr(H(x)) permute F_(p^n)?*, *Finite Fields and Their Applications* **15(5)**, pp. 615–632 (2009), DOI **10.1016/j.ffa.2009.07.001**. Author-hosted paper: https://www-rocq.inria.fr/secret/Pascale.Charpin/ffa-ChaKyu-09.pdf. Its Section 2, Definition 1 calls a direction a linear structure exactly when a finite derivative is constant; Proposition 1 says the structures plus zero form an F_p-linear subspace. The paper attributes earlier work to X. Lai, *Additive and linear structures of cryptographic functions*, FSE 1994 / LNCS 1008 (1995), pp. 75–85. This strongly confirms that the basic D and its additive algebra **are prior art**, not discoveries here.

**First-moment method prior art:** Dimitris Achlioptas and Cristopher Moore, *Random k-SAT: Two Moments Suffice to Cross a Sharp Threshold*, *SIAM Journal on Computing*, DOI **10.1137/S0097539703434231**, studies random CSP moment methods; source: https://epubs.siam.org/doi/10.1137/S0097539703434231. Colin Wei and Stefano Ermon, *General Bounds on Satisfiability Thresholds for Random CSPs via Fourier Analysis*, *AAAI 2017*, DOI **10.1609/aaai.v31i1.11136**, is additional broader random-CSP comparison (https://ojs.aaai.org/index.php/AAAI/article/view/11136).

**New scope under investigation:** NG-Q4 uses elementary but exact finite-field operator rank counting to derive an exact local constant-derivative probability and a closed-form **global** first moment for the specified independently randomized NCSG source form. This model-specific calculation may be original to the project, but an appropriate prior theorem may already subsume it. No claim of globally original mathematics or peer-reviewed novelty follows.


## Pair-projection consistency prior art (31 October 2026)

Alan K. Mackworth, *Consistency in networks of relations*, **Artificial Intelligence** 8(1), pp. 99–118 (1977), DOI **10.1016/0004-3702(77)90007-8**. Primary journal metadata: https://www.sciencedirect.com/science/article/pii/0004370277900078. The published work explicitly covers local node/arc/path consistency methods for constraint networks. The implemented NG-Q7 use of pairwise projections of higher-arity public relations is in this **pre-existing CSP-consistency family**. No original algorithmic discovery should be attributed to the generic filtering method.

NG-Q6 uses a model-specific local collision calculation and a standard first-moment argument; this does not create a new field of probabilistic combinatorics. A systematic comparison to planted CSP uniqueness and polynomial-time reconstruction theorems remains necessary. No unsupported global novelty claim is made.


## Newly checked planted CSP and cohomological antecedents (1 November 2026)

- **Arpon Basu, Jun-Ting Hsieh, Andrew D. Lin, Peter Manohar**, *Solving Random Planted CSPs Below the n^(k/2) Threshold*, **ICALP 2026**, DOI **10.4230/LIPIcs.ICALP.2026.23**, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2026.23. A peer-reviewed algorithmic result for **Boolean** planted k-ary CSPs with stated constraint counts and Sum-of-Squares techniques; not claimed to have the same ternary finite-difference sampler or to subsume NG-Q8 without an explicit reduction.
- **Adam Ó Conghaile**, *Cohomology in Constraint Satisfaction and Structure Isomorphism*, **MFCS 2022**, DOI **10.4230/LIPIcs.MFCS.2022.75**, https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2022.75. Published presheaf/global-section modeling of CSPs and cohomological local-consistency refinement: direct prior art against ungrounded 'new local-to-global sheaf mathematics' claims.
- **Samson Abramsky, Adam Brandenburger**, *The Sheaf-Theoretic Structure of Non-Locality and Contextuality*, **New Journal of Physics** 13 (2011), arXiv:1102.0264, https://arxiv.org/abs/1102.0264. Global-section local-to-global obstructions predating any SG-DIFRA-inspired renaming.
- **Alan K. Mackworth**, *Consistency in networks of relations*, **Artificial Intelligence** 8(1), pp.99–118 (1977), DOI **10.1016/0004-3702(77)90007-8**. Classical local consistency algorithm foundations.

**Interpretation:** The NG-Q8 numerical constant and sampler-specific inequality could still be a publishable narrow result, but originality is **not established** merely by deriving a new rational number. The core local consistency and sheaf formulation have significant antecedents.
