# A polynomial bound on explicit refuting challenges with two local views

Consider the same ternary potential and shift as in [the main note](README.md), with one change to what a response may observe. The challenge is $(a,b,w)\in K^p\times K^q\times K^r$, where $K=\mathbb F_3$. Assign **every** starting coordinate, including the clock and moving base coordinates, to one of two groups. The first group is a vector $u(a)$ and the second is a vector $v(b)$. Neither sees $w$. The responses are arbitrary tables with the listed domains. There are no additional choices after the complete challenge is revealed. Coordinates may be assigned to either group regardless of which challenge coordinate shifts them. As in the main note, dimensions and components are explicitly listed.

**Theorem.** Let the potential have $m$ components of total degree at most two. Set

$$
 t=1+2r+\binom r2,\qquad M=mt,\qquad D=M(p+1)(q+1).
$$

If no pair of response tables satisfies every challenge, some set of at most

$$
 t\big[(p+1)(q+1)+(D+1)\max(p+1,q+1)\big]
$$

complete challenges already has no common solution. The two-view decision problem is coNP-complete. The upper bound permits any number of coordinates in each response vector.

## Proof

**1. Reduce the unseen block to finitely many fixed probes.** For fixed addresses and responses, each component of the difference is a polynomial of degree at most two in $w$. Use the set

$$
 W=\{0\}\cup\{e_i,2e_i:1\le i\le r\}
   \cup\{e_i+e_j:1\le i<j\le r\},
$$

where $e_i$ denotes a unit vector. The origin gives the constant coefficient. Evaluations on $e_i,2e_i$ then determine the linear and square coefficients of coordinate $i$, since the two-by-two coefficient matrix has determinant $2\ne0$ in $K$. Subtracting the known terms from the evaluation on $e_i+e_j$ gives its mixed coefficient. Thus vanishing on $W$ is equivalent to vanishing everywhere in the unseen block. For $r=0$ there is one empty probe. Use all $t=|W|$ probes to form $M$ simultaneous rows in the two observed blocks.

**2. Split each row between the two tables.** In a quadratic difference, a product of starting coordinates contributes $h_i z_j+h_j z_i+h_i h_j$. This includes squares by setting $i=j$. After an unseen probe is fixed, the difference is affine in all starting coordinates, their coefficients are affine in the addresses, and its starting-point-independent part has degree at most two in the addresses. Therefore the simultaneous rows have the form

$$
 T_L(a,b,u(a))+T_R(a,b,v(b))=0.
$$

Put every term involving a left response into $T_L$ and every term involving a right response into $T_R$. Of the address-only terms, put the purely right terms into $T_R$, the purely left terms into $T_L$, and put mixed terms and constants on either side. For a fixed $a,u(a)$, the vector $T_L$ is affine in $b$. For a fixed $b,v(b)$, the vector $T_R$ is affine in $a$. The choices remain linear in each local response. This splitting also works if a left response is a moving coordinate shifted by a right address trit.

**3. Describe agreement by a polynomial with few coefficients.** Write $\widehat a=(1,a_1,\dots,a_p)$ and $\widehat b=(1,b_1,\dots,b_q)$. A vector $Q$ affine separately in each block has one expression per row,

$$
 Q_j(a,b)=\widehat a^{\mathsf T} H_j\widehat b.
$$

There are $D$ coefficients in the matrices $H_j$. Let $I=\{0,e_1,\ldots,e_p\}$ and $J=\{0,e_1,\ldots,e_q\}$ be affine interpolation frames. Any values on $I\times J$ specify a unique such $Q$, by affine interpolation first in one block and then in the other. If tables solve every challenge, the common value $T_L=-T_R$ is separately affine: use the left expression when varying $b$ and the right expression when varying $a$. Hence it equals a $Q$ of the stated form.

For each left address $a$, let $S_a$ be the set of coefficient vectors for which **some** left response attains $T_L(a,b,u)=Q(a,b)$ for all $b\in J$. Equality then holds for every $b$ by affine interpolation. Define $S'_b$ on the right by requiring $T_R(a,b,v)=-Q(a,b)$ for $a\in I$. These sets are affine subspaces of $K^D$ or empty. In each case they are projections of the simultaneous affine equations in the candidate coefficients and the local response. The intersection of all these sets is nonempty exactly when there is a global solution: in the reverse direction choose one witnessing response separately at each address, and add the two identities.

**4. Extract a list of failing challenges.** If the intersection is empty, at most $D+1$ of the sets already have empty intersection. Indeed, start with $K^D$. As long as the current nonempty intersection still contains points excluded by the entire family, some set cuts it properly. Each nonempty proper intersection lowers affine dimension by at least one, and at most one last cut is needed to reach the empty set.

Keep the frame pairs $I\times J$. For every selected left address $a$, also keep $\{a\}\times J$. For every selected right address $b$, also keep $I\times\{b\}$. Pair each retained address pair with every probe in $W$. This gives the claimed bound on the number of full challenges. Suppose tables satisfied this finite list. On $I\times J$, interpolate $Q$ from the common values $T_L=-T_R$. For each selected left address and each $b\in J$, the right response at $b$ is fixed. Its expression $-T_R(\cdot,b,v(b))$ is affine in the first block and agrees with $Q(\cdot,b)$ throughout $I$. It agrees at the selected address as well. Its equality with $T_L$ on the retained pair therefore puts $Q$ in the selected $S_a$. The same argument interchanging the two sides puts $Q$ in every selected $S'_b$. This contradicts the empty intersection and proves the list bound.

**5. Complexity.** A NO certificate is the explicit list itself. Create one unknown vector per distinct left address in the list and one per distinct right address. Each listed challenge yields affine equations in these table entries, and Gaussian elimination checks inconsistency in polynomial time. For hardness, start with the [Round 9 quadratic universal problem](../round9/CHALLENGE_COUPLED_DIFFERENTIAL_SOLVABILITY.md). Give its complete challenge to the left view and assign all original starting coordinates to that view. Add a dummy right challenge coordinate and its moving starting coordinate, which belongs to the right view and is unused by the potential. Existence of one left table is equivalent to pointwise solvability for every original challenge. The reduction preserves degree and size up to polynomial overhead and gives coNP-hardness.

## Comparison with a full-information response

The [path construction](OBSTRUCTION.md) has two private scalar outputs and additional responses that may see the complete challenge. On addresses of width $n$, it requires exactly $2^n-1$ challenges in the shortest explicit refuting list. Its potential has $O(n)$ rows and coordinates and an $O(n\log n)$-bit sparse encoding with the common full view specified once. Thus the minimum list length is exponential in address width and superpolynomial in that encoding length. In the theorem above it is polynomial in the explicit input length. This difference in **refuting-list size** is unconditional. Moving every starting coordinate into the two local groups changes the information available to the policy; a circuit with access to the full challenge does not satisfy that hypothesis.

## Reproduction

Run `python3 -m unittest -v test_two_view_bound` in this directory. The tests reconstruct the common polynomial from frame values, check the unseen-coordinate interpolation identity, and compare direct full-table feasibility with the frame-and-subspace construction on deterministic small instances.
