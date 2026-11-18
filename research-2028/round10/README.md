# Local strategies for ternary differential collisions

**SG-DIFRA mathematical research note, 18 November 2026.**

A single challenge asks for two inputs of a polynomial map with the same output. This note asks whether two coordinates of the first input can be chosen **consistently across challenges** when each sees only its own address. The remaining coordinates may use the whole challenge. For sparse quadratic maps over the field of three elements, deciding whether these choices exist is PSPACE-complete. Allowing **one square-free cubic monomial in the entire vector map** gives an NEXP-complete problem. In both lower bounds every individual challenge can be solvable. The change concerns how multiple answers fit together.

There is also an unconditional difference in how failures can be demonstrated. For quadratic maps, a polynomial-size list of challenges always suffices to refute a policy when all responses belong to the two separate views. Adding helpers that see both addresses permits compact examples whose shortest refuting lists have exactly $2^n-1$ challenges for $n$-bit addresses. [Two-view bound](TWO_VIEW_BOUND.md) · [Matching path calculation](OBSTRUCTION.md)

The two-table coloring argument comes from succinct graph coloring and dependency quantified Boolean formulas. Our candidate contribution is the finite-difference representation, its upper bounds, and the simultaneous sparsity and deletion guarantees below. [Prior work and publication status](RELATED_WORK.md)

## 1. The decision problem

Work over $K=\mathbb F_3$. A challenge $c=(a,b,w)$ contains two address blocks and an optional public block. The input explicitly lists all coordinates and all outputs of a vector polynomial $P$. Each component is a sparse list of nonzero monomials in reduced form (individual exponents at most two, equal terms combined modulo three). Count a term separately in each component where it appears, in the supplied coordinates. A change of variables can change this count. Let $L$ be the bit length of this description, including block sizes given by explicit lists. No truth table or succinct encoding of the coordinate list is supplied.

Write a starting point as $z=(s,x,A,B,y)$, where $x$ has one entry per challenge trit. Its prescribed shift is $h_c=(1,c,0,0,0^{|y|})$. The decision predicate is

$$
\exists f:K^{|a|}\to K,\quad \exists g:K^{|b|}\to K,\quad
\forall c=(a,b,w)\quad \exists s,x,y:\quad P(z+h_c)=P(z),
\qquad z=(s,x,f(a),g(b),y).
$$

The two functions can be arbitrary finite tables, with no bound on their circuit size. A repeated left address must receive the same left answer, even when the right address or transcript changes. The analogous rule applies on the right. The full-information choices $s,x,y$ are fresh for each challenge. The local addresses are disjoint. The construction uses equal address widths; the upper bounds also allow different widths. We refer to this problem as **local differential collision selection**. All completeness statements use deterministic polynomial-time many-one reductions.

| Input and observation restriction | Complexity |
| --- | --- |
| Affine $P$, two local trits | In P |
| Quadratic $P$, two local trits | PSPACE-complete |
| Degree at most three, at most one cubic monomial, two local trits | NEXP-complete |
| Same one-cubic budget, a supplied single challenge, local values free or fixed | In P |
| Same one-cubic budget, every challenge answered independently | coNP-complete |
| Same one-cubic budget, one local trit plus full-information witnesses | coNP-complete |

**Theorem 1 (sparse hardness).** The two completeness lower bounds with two local trits hold even if every component has at most five monomials, all monomials are square-free, and every quadratic term is the product of a moving coordinate and a stationary coordinate. The quadratic hard family has exactly one linear term. The cubic hard family has exactly one linear term and one cubic term. In the latter family, deleting either designated term separately makes every constructed instance a YES instance. Both reductions can be restricted to instances for which every individual challenge has a collision.

## 2. Quadratic upper bound

For a fixed $c$, the difference of any quadratic polynomial is affine in the starting point. A quadratic monomial with factors $z_i,z_j$ contributes $h_i z_j+h_j z_i+h_i h_j$; repeated factors obey the same identity. For each of the nine proposed pairs $(A,B)$, substitute the pair and use Gaussian elimination over $K$ to decide whether $s,x,y$ can complete it. The allowed set $R_c\subseteq K^2$ is the projection of an affine solution set. It is empty, a point, an axis-parallel line, a line describing a bijection $B=\alpha A+\beta$ with $\alpha\ne0$, or the whole plane.

Make a vertex for every left or right table entry. Each challenge imposes its relation on the corresponding pair of vertices. An empty relation rejects immediately. A point pins two values; an axis-parallel line pins one. A bijection yields an edge labeled with its map in one direction and its inverse in the other. Full relations add nothing. This can produce parallel edges, including different constraints for the same two addresses.

Consider the graph on pairs (vertex, value). Each bijection produces three edges linking compatible values. A pin forbids the other two values at its vertex. A candidate root value fails if its reachable states include a forbidden value or a second value at the same root. If it survives, transporting it along any path assigns exactly one value to each vertex in its component. Indeed, two distinct values at a reached vertex would transport along the inverse of one of the paths to two distinct values at the root. Every pin and every edge then holds. A global assignment exists exactly when all components admit a surviving root value and there is no empty constraint.

The graph can be exponential in $L$, but each vertex, value, and challenge has a polynomial-length encoding. One can enumerate challenges while recomputing their nine-entry tables. This decides adjacency and the presence of a forbidden pin in polynomial space. Reachability in this implicit graph uses polynomial space, for instance by Savitch's recursive midpoint test over paths of at most the number of states. Testing each of the three values at each root reuses the workspace. This proves PSPACE membership for arbitrary quadratic input maps, including those outside the sparse hard family. For an affine map the difference depends only on $(1,c)$, so testing its constant and challenge coefficients for zero suffices.

## 3. How a public condition controls a quadratic difference

Here and below, stationary helpers have full information. The following three assignment types suffice for the quadratic compiler. In a displayed row the right column is one component of $P$; the component must have zero difference.

| Required relation on stationary values | Potential component |
| --- | --- |
| $v=\sum_j \lambda_j u_j$ | $s(v-\sum_j\lambda_j u_j)$ |
| $v=c_i u$ | $s v-x_i u$ |
| $v=1$ | $s(v-1)$ |

All coefficients are in $K$. Negating a whole component gives the same equation. More generally, a sum of terms $c_i u_j$ and $u_j$ gives a single row by using $x_i u_j$ and $s u_j$. No starting value for $s$ or $x$ needs to be pinned. It cancels from the difference.

To make a condition force a payload $u$ to zero, compute its indicator times $u$, then set the result to zero. For the single test $c_i=d$, the indicator is $1-(c_i-d)^2$. Generate $t=c_i u$, followed by $v=(1-d^2)u+2d\,t-c_i t$. Then $v=u$ on a match and $v=0$ otherwise. For a tuple pattern, apply this construction successively to its coordinates. For a small list of accepted tuples, add their branch outputs. Distinct accepted tuples cannot both match the same challenge. Repeated circuit input wires are allowed; infeasible tuple patterns give zero. To impose a conjunction, feed one predicate's output to the next. For fixed challenge and local values these assignments are triangular and uniquely determine the stationary helpers.

Let an AND/NOT circuit $C$ with two $n$-bit address inputs specify graph edges. Its gate list is public. The trits in $w$ propose all gate output bits. Two guards are used throughout.

* **Same vertex.** Each pair of corresponding address trits must be either $(0,0)$ or $(1,1)$. The guard ignores $w$.
* **Edge.** Both addresses are Boolean. Each proposed gate output must agree with its inputs under the stated Boolean gate, and the designated output must be one. These tests have arity at most three. A Boolean pair has a unique correct gate transcript; an accepting transcript exists exactly for a pair recognized by $C$.

The AND gate has four allowed tuples, the largest list used. Summing their four branch outputs into a fresh helper takes at most five monomials in one component. The other stages meet this bound as well. Each stage costs a constant number of rows and terms per gate, address coordinate, or anchor bit. There are $O(n+|C|)$ coordinates, rows and terms when $|C|$ counts gates; coordinate indices take $O(\log(n+|C|+2))$ bits. Invalid ternary addresses and invalid transcripts activate only the conditions whose own tests they pass.

## 4. PSPACE hardness with quadratic potentials

Reduce from the complement of succinct undirected $s$–$t$ reachability, which is PSPACE-complete. A Boolean circuit specifies adjacency on all $n$-bit strings. If the encoding designates an undirected edge whenever either order is reported, equality is symmetric, so a report in either order suffices. The source theorem is Theorem 38 of Balcázar, Lozano and Torán. [Source paper](https://www.uni-ulm.de/fileadmin/website_uni_ulm/iui.inst.190/Mitarbeiter/toran/succinct.pdf)

Call the two distinguished vertices $p$ and $q$. Implement four rules using the quadratic compiler.

1. Equal Boolean addresses force $A=B$.
2. An accepting edge transcript forces $A=B$.
3. Left address $p$ forces $A=0$.
4. Right address $q$ forces $B=1$.

The last guard uses a helper initialized to $B-1$, which contributes the sole linear term (up to sign) across the potential. All other rows use mixed quadratic terms. If tables exist, rule 1 gives one label per Boolean vertex and rule 2 makes it constant along every edge. Rules 3 and 4 then put $p$ and $q$ in distinct components. Conversely, if they lie in different components, give the component of $q$ label one and all other components label zero. Use the labels in both tables and extend to non-Boolean addresses arbitrarily. Every challenge admits the computed helpers. Deleting the one linear term allows both tables and all stationary coordinates to be zero.

For the additional promise of individual solvability, first append two fresh vertices as leaves attached solely to $p$ and $q$, respectively. Tag the new addresses and leave unused encodings isolated. The adjacency circuit grows polynomially. The new distinguished vertices are distinct and nonadjacent, and their connectivity is exactly the original connectivity. In a single challenge, simultaneously pinning the left value to zero and the right to one can occur only on this nonadjacent ordered pair. Neither equality guard then fires. If at most one pin fires, equal local values can satisfy all active rules. Hence every challenge individually admits a collision on both YES and NO outputs of this reduction.

## 5. NEXP hardness from one cubic term

Use succinct graph 3-colorability, which is NEXP-complete. The published two-address reduction of Chen, Huang, Lu and Tan, Section III.A, uses local colors, agreement on equal addresses and disagreement on edges. We use that argument and implement its color comparison with **one multiplication of two stationary helper values**. [Source paper](https://arxiv.org/pdf/2208.06014)

Create stationary helpers $T,D,M,N,Q$. Require

$$
T=1,\qquad D=A-B,\qquad M=D-T,\qquad N=D+T,\qquad Q=MN .
$$

The first four relations use Section 3. The fifth is the single component $sQ-sMN$, whose difference is $Q-MN$. It contains the only cubic monomial in the whole list, and $s,M,N$ are three distinct coordinates. The only linear monomial is $-s$ in $s(T-1)$. Impose the same-vertex guard on payload $D$, and the edge guard on payload $Q$. Each guard uses only mixed quadratics.

| $D=A-B$ | $M=D-1$ | $N=D+1$ | $Q=MN$ |
| --- | --- | --- | --- |
| 0 | 2 | 1 | 2 |
| 1 | 0 | 2 | 0 |
| 2 | 1 | 0 | 0 |

Thus $Q=0$ on an edge precisely when the two colors differ. A proper 3-coloring supplies both tables on Boolean vertices; assign arbitrary entries elsewhere. Conversely the diagonal forces a single color per Boolean vertex, and the accepting transcript for every edge forces its endpoints to differ. A winning pair of tables restricts to a proper coloring. No gate transcript or helper can change a table entry.

For individual solvability use loopless graphs. This restriction preserves hardness even for a source convention allowing loops. Replace each vertex $v$ by four copies $(v,i)$, $0\le i<4$. Between distinct originals retain the original edges on copy zero. If $C(v,v)=1$, make its four copies a complete graph on four vertices, omitting all loops. Otherwise the extra three copies are isolated. The transformed circuit has polynomial size and preserves 3-colorability in both directions. On a loopless graph a single challenge can demand equal colors or different colors, never both. Both types admit a choice. In particular, $K_4$ gives a concrete NO instance where each challenge succeeds separately.

**Deleting the cubic monomial.** The exceptional row now enforces $Q=0$. Take both tables constantly zero, $T=1$, $D=0$, $M=2$, $N=1$ and $Q=0$. All guards accept every challenge with their computed helpers.

**Deleting the linear monomial instead.** The first row now enforces $T=0$. Both tables and all stationary helpers can be zero, including in the product row. These deletion certificates are statements about these constructed instances. They do not give a polynomial-time algorithm for all quadratic inputs.

**Upper bound.** Guess both tables explicitly, enumerate challenges, and guess the remaining coordinates separately for each. The number of trits guessed and the time needed are at most $2^{\mathrm{poly}(L)}$, even accounting for sequential lookup on a Turing machine. All rows can be evaluated in polynomial time at a specified point. This proves NEXP membership, hence completeness with the stated one-cubic restriction.

## 6. Which part of the problem is hard?

**Proposition 2.** With at most one cubic monomial and all other terms quadratic or lower, a specified challenge has a polynomial-time existence test. Enumerate values for the at most three starting coordinates appearing in that term. This gives at most $3^3=27$ trials, also when some indices repeat. Its entire difference is then known. The remaining system is affine in the unfixed coordinates and is decided by Gaussian elimination. Fixed local values can be added as equations.

If each challenge can choose its own complete answer, a NO certificate is a single failed challenge. If just one scalar is restricted to a local address, a NO certificate consists of one address and at most three compatible full challenges. For each possible local value one of them prevents that value from working. Conversely, if no such address exists, choose an admissible value independently at every address. Proposition 2 verifies the proposed failures in polynomial time. Both universal variants are in coNP. Hardness already holds on the purely quadratic inputs of [Round 9](../round9/CHALLENGE_COUPLED_DIFFERENTIAL_SOLVABILITY.md); an unused stationary local coordinate embeds those inputs in the one-local-scalar variant.

The quadratic path construction also gives exact numbers of challenges needed to expose a conflict. For a path on $2^n$ vertices with opposite pinned endpoints, the smallest inconsistent subset of whole challenges has size $2^n-1$. A three-edge path already needs three. This lower bound is on explicitly listed challenges, measured against address width; a symbolic description of the same obstruction can be short. [Obstruction theorem and proof](OBSTRUCTION.md)

## 7. Assumptions and scope

The reductions, upper bounds and deletion properties use no unproved complexity separations. Let $H$ denote the new NEXP-complete language. The nondeterministic time hierarchy gives $\mathrm{NP}\subsetneq\mathrm{NEXP}$. Thus Round 9's NP-complete fixed cubic language reduces to $H$, and $H$ cannot reduce back to it in polynomial time. A reverse reduction would place every NEXP language in NP. This gives an unconditional sense in which the new problem is harder. A strict separation from Round 9's $\Pi_2^{\mathrm P}$-complete universal language requires $\Pi_2^{\mathrm P}\ne\mathrm{NEXP}$. A strict separation between the PSPACE and NEXP classifications here requires $\mathrm{PSPACE}\ne\mathrm{NEXP}$. [Time hierarchy reference](https://staff.science.uva.nl/r.dehaan/complexity2025/files/lecture4.pdf)

The input here is a map and an observation pattern; the output is a yes/no answer about the existence of two functions. A cryptographic hardness assumption would additionally need a sampled input distribution, a defined adversarial task, and a justified success bound. These proofs provide none of the three for an SG-DIFRA KEM. They also give no quantum running-time lower bound. The contribution is public as an AI-assisted research note. Global priority, independent expert review, and venue acceptance are open. The companion tests check implementations on finite inputs. The reductions above carry the asymptotic claims. [Verification and reproduction](VERIFICATION.md)
