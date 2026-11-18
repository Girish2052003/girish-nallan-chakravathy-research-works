# The exact number of challenges needed to refute a quadratic policy

A single challenge fixes two ternary address vectors and a putative circuit transcript. A policy has to reuse its answer every time it sees the same local address. This note measures how many explicit challenges an observer must retain before these reuse requirements can contradict one another.

## Statement

Let a Boolean circuit compute a **symmetric** adjacency relation on the binary addresses of a finite undirected graph $G$. Apply `compile_nonconnectivity` in [quadratic_compiler.py](quadratic_compiler.py) with start vertex $p$ and target vertex $q$. The response on the first address is called $A$, the response on the second is called $B$, and both take values in $\mathbb F_3$. Every helper may see the entire challenge. A subset of challenges is *refuting* if no single pair of tables $A,B$, together with allowed helpers, satisfies the collisions for all challenges in that subset.

**Proposition.** If $p,q$ are disconnected, there is no refuting subset. Otherwise let $d$ be their graph distance, with $d=0$ allowed. The least cardinality of a refuting subset is

$$
  \begin{cases}d,&d\text{ odd},\\d+1,&d\text{ even}.\end{cases}
$$

This counts distinct complete challenges, including their wire transcripts. It bounds the size of a refutation presented as a list of challenges. A symbolic proof may be much shorter.

## Proof

For a challenge with addresses $a,b$ and wire transcript $w$, project out all full-view helpers. The guard construction has precisely the following effects.

1. If $a=p$, the challenge pins $A(p)=0$, independently of $b,w$. If $b=q$, it pins $B(q)=1$, independently of $a,w$.
2. If $a=b$ is a binary address, the challenge imposes $A(a)=B(b)$, independently of $w$.
3. If both addresses are binary and $w$ is a correct accepting gate transcript for adjacency, the challenge imposes $A(a)=B(b)$.

There are no further projected constraints. In each indicator stage the helper assignments are determined by the current challenge and the two labels. A malformed transcript turns off the edge guard, but it can still activate a diagonal equality or a pin. A nonbinary address can never create an equality. The opposite binary address can still activate its own pin. The compiler therefore does not discard these challenges wholesale.

Given a set of challenges, form a bipartite graph with vertices $A(u)$ and $B(u)$ for binary addresses $u$. Add the equality edge from items 2 or 3 whenever it is imposed. One challenge adds at most one edge, even if both guards hold. The selected constraints are inconsistent exactly when both pins are active and their vertices lie in the same connected component. Indeed, otherwise each connected component can be assigned one label respecting its active pin, and every unmentioned ternary address and every helper can be filled in. If the two pins lie in the same component, equality forces $0=1$ in $\mathbb F_3$.

Suppose a subset of size $k$ refutes. Its equality graph contains a simple path from $A(p)$ to $B(q)$. Its length is odd by bipartiteness, and at most $k$. Project each vertex to its binary address. An equality on a diagonal leaves the address fixed, and every other step follows an edge of $G$. Erasing pauses gives a walk from $p$ to $q$. Consequently the path length is at least $d$. This also proves that no subset refutes disconnected endpoints.

Conversely, take a shortest path from $p$ to $q$. If its length is even, append one diagonal step at $q$. Starting at $A(p)$, alternate between the $A$ and $B$ copies along this walk. Symmetry ensures that for each genuine edge we can present the pair in whichever order puts the $A$ endpoint on the left, and supply its correct accepting transcript. For a diagonal step any transcript works. If $p=q$ this consists of one diagonal challenge. The first chosen challenge pins $A(p)$, the last pins $B(q)$, and their chain equates the two. The path uses the displayed number of distinct challenges. This proves the formula.

## A compact family with an exponentially long refuting list

Take binary addresses of width $n\ge2$, interpreted as integers. Join exactly the consecutive integers in the path

$$
  0,1,2,\ldots,2^n-1.
$$

Use the two ends as anchors. This adjacency relation is symmetric and has a Boolean circuit of $O(n)$ fan-in-two AND/NOT gates: a ripple-carry circuit tests ordinary increment in either direction and rejects overflow. The two endpoints have odd distance $2^n-1$. By the proposition **every set of fewer than $2^n-1$ challenges can share a collision policy**, and some set of exactly $2^n-1$ cannot.

At width two the refuting chain is $A(0)=B(1)=A(2)=B(3)$. The first challenge pins the left end to zero, and the last pins the right end to one. Any two challenges still admit a shared policy. In particular each individual challenge in the family has a collision.

The circuit and compiled vector potential use $O(n)$ gates, rows and monomials. Their sparse wire and coordinate indices cost $O(\log n)$ bits apiece, hence $O(n\log n)$ bits in the two-private-label representation with a common full view for the helpers. A format that explicitly repeats that view for each helper incurs additional encoding overhead. The exponent above is in *address width*. It does not give a lower bound on general algorithms or on the size of other kinds of proof.

## Reproduction

From this directory run `python3 -m unittest -v test_obstruction`. The tests build the Boolean circuit, evaluate it on every binary address pair at widths 2, 3 and 4, build the bipartite equality graph and compute the exact distances. At width two they separately enumerate all 6,561 ternary assignments to the two tables on binary addresses, and verify that every pair of challenge effects permits a common assignment. They also check subsets along a shortest refutation and evaluate actual compiled polynomial differences for representative valid, malformed and nonbinary challenges.
