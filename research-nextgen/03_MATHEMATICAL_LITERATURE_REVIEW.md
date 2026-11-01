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


## 1 November 2026 antecedents for NG-Q10 / NG-Q11

- **Rina Dechter**, *Bucket elimination: A unifying framework for reasoning*, Artificial Intelligence 113 (1999), 41–85, DOI 10.1016/S0004-3702(99)00059-4, https://www.sciencedirect.com/science/article/pii/S0004370299000594. Complete CSP solutions by variable conditioning or width-based elimination are prior art. NG-Q10's public 2-anchor star solver is a textbook width-two special case.
- **Tali Kaufman and Dana Ron**, *Testing Polynomials over General Fields*, SIAM Journal on Computing, DOI 10.1137/S0097539704445615, https://epubs.siam.org/doi/10.1137/S0097539704445615. Published finite-field low-degree property tests and generalized Reed–Muller interpretations; source-form NG-Q11 degree filtration is not newly invented mathematics.
- **Arnab Bhattacharyya and Abhishek Bhowmick**, *Using Higher-Order Fourier Analysis over General Fields* (ECCC TR15-077, 2015), https://eccc.weizmann.ac.il/report/2015/077/. Further prior art on finite-field polynomials, affine-invariant properties and low-degree algebraic structure.
- Standard generalized Reed–Muller codes evaluate low-degree polynomial functions over finite fields. The dimension of degree<=3 scalar functions on F3^3 is exactly 17 of the 27 function-space dimensions, yielding the exact 1/59049 false-positive probability for the public NG-Q11 local degree predicate.

**Limit:** A model-specific formulation or a new rational count is not a globally novel algebraic theory. Claims about complete secure KEMs or key hiding do not follow solely from function distinguishability.


## 1 November 2026 — algebraic equivalence and nonassociativity prior-art update

**Hidden polynomial equivalence:** Pierre-Alain Fouque, Gilles Macario-Rat and Jacques Stern, *Key Recovery on Hidden Monomial Multivariate Schemes*, EUROCRYPT 2008, DOI 10.1007/978-3-540-78967-3_2 (https://crypto.orange-labs.fr/acg/publication/infoPublication.php?id=83); and *On enumeration of polynomial equivalence classes and their application to MPKC*, Finite Fields and Their Applications 18(2), 283–302 (2012), DOI 10.1016/j.ffa.2011.09.001 (https://www.sciencedirect.com/science/article/pii/S1071579711000797). These explicitly discuss hidden linear changes of variables and equivalent secret keys. NG-Q12's exact finite-difference image and local coordinate scan are **model-specific**, not a newly discovered general polynomial-isomorphism theory.

**Quasigroup isotopy:** Jack Allsop, *Isotopisms of quadratic quasigroups*, Algebraic Combinatorics 9(1), 75–94, published March 2026, DOI 10.5802/alco.467 (https://alco.centre-mersenne.org/articles/10.5802/alco.467/); Dimpy Chauhan, Indivar Gupta and Rashmi Verma, *Quasigroups and their applications in cryptography*, Cryptologia 45(3), 227–265 (2021), DOI 10.1080/01611194.2020.1721615 (https://www.tandfonline.com/doi/abs/10.1080/01611194.2020.1721615). Quasigroups, Latin squares, hidden isotopies and their cryptographic assessment have **substantial published prior art**. NG-Q13's normalization is a standard principal-isotope/transport identity, not a new nonassociative algebra.

**Classical countercontrol:** The Fano-plane Steiner quasigroup (seven nonzero binary 3-vectors with XOR third-point operation) supplies an example that is non-group-isotopic, proved by a direct Steiner-identity contradiction over F7. It is not claimed new, cryptographically hard or proof of a new private trapdoor.

**Novelty assessment:** A serious new foundation must first pass known-isomorphism/isotopy and equivalence tests; new names, alternate notation and publicly reconstructible hidden coordinates do not suffice. No positive newly original construction was independently verified this turn.

## 1 November 2026 — nonabelian gain graphs and simultaneous permutation conjugacy

- On cospectrality of gain graphs, DOI 10.1515/spma-2022-0169, https://doi.org/10.1515/spma-2022-0169: explicitly covers nonabelian gain-graph switching, tree balancing, and cycle-gain conjugacy. NG-Q14 belongs to this pre-existing mathematical framework.
- Bradley Stich, Strong Recovery In Group Synchronization, Rose-Hulman Undergraduate Mathematics Journal 24(1), 2023, https://scholar.rose-hulman.edu/rhumj/vol24/iss1/2/: considers noisy graph group-synchronization and recovery; public noisy-edge modification is not independently novel without serious comparison.
- Andrej Brodnik, Aleksander Malnic, Rok Pozar, The simultaneous conjugacy problem in the symmetric group, Mathematics of Computation, DOI 10.1090/mcom/3637, https://doi.org/10.1090/mcom/3637; and A subquadratic algorithm for the simultaneous conjugacy problem, Journal of Graph Theory (2022), DOI 10.1002/jgt.22798, https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.22798: published efficient simultaneous conjugacy of explicit permutation tuples.

Thus NG-Q14 and NG-Q15 provide an original-to-this-project negative analysis of a proposed trapdoor, but not original group-action mathematics or a newly invented polynomial-time conjugacy algorithm.


## NG-Q16–NG-Q18 close prior art (1 November 2026)

**Robust finite/compact group synchronization with adversarial or random edge corruption:** Gilad Lerman and Yunpeng Shi, *Robust Group Synchronization via Cycle-Edge Message Passing*, Foundations of Computational Mathematics 22(6), 1665–1741 (2022), online September 2021, DOI **10.1007/s10208-021-09532-w**, https://link.springer.com/article/10.1007/s10208-021-09532-w. This established strong deterministic and stochastic recovery using **cycle consistency**. NG-Q16's elementary two-hop voting and Hoeffding bounds are not independent inventions of a new field or necessarily stronger thresholds.

**Alternative recovery methods:** Yunpeng Shi, Cole M. Wyeth, Gilad Lerman, *Robust Group Synchronization via Quadratic Programming*, ICML 2022, https://proceedings.mlr.press/v162/shi22g.html, uses corruption estimation and structural cycle consistency. Bradley Stich, *Strong Recovery In Group Synchronization*, Rose-Hulman Undergraduate Mathematics Journal 24(1), 2023, https://scholar.rose-hulman.edu/rhumj/vol24/iss1/2/, presents dense positive and sparse negative group synchronization results. **Higher-order group synchronization**, Research in the Mathematical Sciences (2026), DOI 10.1007/s40687-026-00627-w, https://link.springer.com/article/10.1007/s40687-026-00627-w, extends synchronization to hypergraphs; avoid rebranding a higher-order synchronization variant as SG-DIFRA novelty.

**Erdos–Renyi graph isolation/connectivity:** Rick Durrett, *Random Graph Dynamics*, chapter 2 §2.8, https://sites.math.duke.edu/~rtd/RGD/RGD.pdf; Sebastien Roch, random graph notes, https://people.math.wisc.edu/~roch/teaching_files/833.f14/mdp-chap2-web.pdf. The NG-Q18 exact isolated-vertex moments and second-moment non-isolation bound are textbook random-graph arguments, NOT novel mathematics.

**Group gauge ambiguity:** standard group synchronization identifiability/transport-of-structure consequence; NG-Q17 does not establish a private-key security theorem. Recovery of equivalence classes and non-identifiability of absolute representatives are distinct.

**M2 originality:** NOT PASSED for NG-Q16/NG-Q17/NG-Q18; the narrow model-specific negative security conclusions are potentially useful design filters but are not a newly invented mathematical direction.
