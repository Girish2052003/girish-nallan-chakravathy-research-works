# What the published graph reveals about a planted private strategy

The [Round 11 sampler](../round11/PLANTED_POLICY.md) draws independent labels $L_0,\ldots,L_{v-1}$ uniformly from three colors. For each pair, it independently retains the edge with probability $1/2$ if the two labels differ. It publishes the resulting graph $G$ and keeps $L$. The vertex count and ordering are public. The color names themselves are hidden by symmetry. The partition into color classes can nevertheless be reconstructed with high probability.

**Theorem.** For $v\ge2$, put $m=v-2$ and define

$$
\eta_m=12^{-m}\sum_{r=0}^m {m\choose r}(10+2^{-r})^{m-r},\qquad
\delta_v=\min\{1,{v\choose 2}\eta_m/3\}.
$$

There is a polynomial-time randomized procedure that, given $G$, samples a label table $L'$ for which the total variation distance between $(G,L')$ and the honest $(G,L)$ is at most $\delta_v$. Consider any KEM whose complete public and private keys are exactly this graph and table, up to public encodings. Suppose its public encapsulation uses independent fresh randomness, its honest correctness error is $\varepsilon$ averaged over key generation and encapsulation, and its shared keys are $\kappa$ bits. A passive distinguisher has raw real-versus-random probability gap at least

$$
\max\{0,1-\varepsilon-\delta_v-2^{-\kappa}\}.
$$

The statement allows arbitrary public encapsulation and efficient decapsulation algorithms and includes private decoders that use the absolute color names. The same argument permits additional public data computed from $G$ when the observer still has $G$ or can efficiently decode it. Publishing only a lossy image of the graph is a different model. Publishing additional data that depend on the private labels beyond $G$, or storing additional correlated private information, changes the key distribution.

## 1. A public equality certificate

Consider distinct vertices $i,j$. Suppose $k,\ell$ are adjacent common neighbors of both. Proper three-coloring assigns two distinct colors to $k,\ell$, so both $i$ and $j$ must use the remaining color. This certificate can never identify differently colored vertices as equal.

Fix $L_i=L_j$. Each of the $m$ other vertices independently becomes a common neighbor in the first other color class with probability $(1/3)(1/2)^2=1/12$, and in the second other class with the same probability. Write $R,B$ for the two counts. A certificate exists precisely when at least one edge joins those two sets. Given their memberships and incident edges to $i,j$, those $RB$ other edge coins are still independent and fair. The conditional probability of no certificate is $2^{-RB}$.

In particular $R$ is binomial with parameters $(m,1/12)$. Conditional on $R=r$, the count $B$ is binomial with parameters $(m-r,1/11)$. The generating function of this binomial gives

$$
\mathbb E[2^{-rB}\mid R=r]=\left((10+2^{-r})/11\right)^{m-r}.
$$

Averaging over $r$ gives $\eta_m$ exactly. A particular pair has equal original colors with probability $1/3$. A union bound over pairs therefore bounds the probability that **any** equal pair lacks a certificate by $\delta_v$. No independence between these pair events is needed. The pair-miss formula is exact; the union bound for the complete table can be loose.

On the complementary event the equality relation specified by these certificates and the diagonal gives exactly the unlabeled partition. Testing the existence of each constant-size certificate and checking the resulting relation take polynomial time in the explicit graph size. On inconsistent outputs, or if there are more than three classes, fix any fallback table. For asymptotics, divide the $m$ other vertices into disjoint pairs. Each pair is a certificate with probability $2(1/12)^2(1/2)=1/144$ conditional on $L_i=L_j$, independently across these disjoint pairs. Thus $\eta_m\le(143/144)^{\lfloor m/2\rfloor}$, which implies $\delta_v\to0$ exponentially up to a polynomial factor.

## 2. From a partition to a private-key distribution

For any partition into at most three classes, choose a deterministic naming, then apply a uniformly random permutation of the three names. The resulting table is uniform over all distinct namings of that partition. This also holds for one or two occupied classes because every naming has the same number of permutation preimages.

Conditional on $G$ and the true partition, the honest table has exactly this distribution. Indeed, permuting the names preserves the original label law and leaves every edge-generation decision unchanged. Couple an honest table and a sampled table by using the same random renaming of canonical representatives whenever their partitions agree. The public partition estimate depends only on $G$, and disagreement has probability at most $\delta_v$. This gives the claimed total variation bound. It concerns the joint distribution of graph and table. It does not say that a sample equals the original named table with high probability.

## 3. Consequence for any correct KEM using these keys

Apply honest public encapsulation with independent randomness to the graph in each distribution above. This cannot increase total variation. Running the private decapsulation algorithm with a sampled table $L'$ and fresh coins if needed therefore reproduces the honest sender's key with probability at least $1-\varepsilon-\delta_v$. The observer can use the equality test between this result and the challenge key. In the independent-uniform-key experiment the chance of equality is at most $2^{-\kappa}$, also allowing a decapsulation failure output. Subtracting the two probabilities proves the claimed raw gap. No access to the recipient's decapsulation oracle is needed.

This explains why changing from an absolute-color key to a color-renaming-invariant key cannot repair this particular sampler at large $v$. A successful receiver using the stored table would also work with a sample from its conditional distribution. The sender's encapsulation and byte encoding can be changed arbitrarily within the stated key model.

## 4. Exact finite checks and scope

| Vertices $v$ | Upper bound on $\delta_v$, rounded upwards |
| ---: | ---: |
| 81 | 1 (uninformative) |
| 122 | 0.151376 |
| 162 | 0.007899 |
| 256 | 0.000005489 |

The rows count graph vertices; they do not assign bit security or identify an SG-DIFRA parameter set. The companion tests compute the bounds by exact integer arithmetic and exhaust the conditional fixed-pair certificate law on small graphs. [Finite checks](test_planted_bound.py)

Polynomial-time coloring of planted random three-colorable graphs is well established. Alon and Kahale analyzed an equal-size-class model, including much lower edge densities than the fair retention probability here. The present calculation uses the exact iid label sampler, yields explicit failure bounds, and connects reconstruction up to color names with the KEM correctness experiment. [Alon and Kahale, SIAM Journal on Computing, 1997](https://www.cs.tau.ac.il/~nogaa/PDFS/spectfig.pdf)
