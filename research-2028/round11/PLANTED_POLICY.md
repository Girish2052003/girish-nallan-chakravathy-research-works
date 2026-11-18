# Planting a complete Round 10 strategy and testing agreement

Round 10 asks for two local tables whose answers fit **all** public challenges of one ternary polynomial map. Here we generate a public map together with those tables. The private holder can answer every challenge efficiently. We then ask whether a sender can share the secret by selecting a public vertex and using its planted color. In this experiment the exact best agreement probability is $1/3$, even for an unlimited sender. [Round 10 construction](../round10/README.md) · [Implementation](planted_policy.py)

## Generating the map and its private strategy

Fix a public vertex count $v\geq1$. Independently choose $L_0,\ldots,L_{v-1}$ uniformly from $\{0,1,2\}$. For each unordered pair $i<j$, draw an independent fair bit $B_{ij}$. Include the edge $ij$ exactly when $L_i\ne L_j$ and $B_{ij}=1$. Publish the resulting simple graph $G$. Keep the color table $L$.

Use binary addresses of width $d=\max(1,\lceil\log_2 v\rceil)$. Additional binary addresses represent isolated vertices. The deterministic Boolean circuit from [planted_policy.py](planted_policy.py) checks whether its two addresses name the endpoints of an edge of $G$. Apply the [Round 10 cubic compiler](../round10/cubic_compiler.py) to this public circuit. The bitset of $G$ suffices to reproduce the circuit and the potential. The only private information in this construction is $L$.

For either local table, answer a real vertex address $i$ with $L_i$. Answer padded or nonbinary addresses with zero. Equal binary addresses receive the same answer. Whenever the edge guard activates, a genuine planted edge has different endpoint colors. The compiler's full-information helper assignments are then available by forward evaluation for each challenge, including malformed gate transcripts. This produces a collision for **every** challenge under one consistent pair of local tables. The holder unpacks the color vector once, reads each local address in $O(d)$ bit steps and looks up its color. Helper computation costs polynomial time in the compiled description. This proves efficient private policy evaluation on the planted distribution. It gives no lower bound for producing a policy from the public description. All generated graphs are YES instances, so their yes/no Round 10 answer is already known.

## What a sender can agree on

**Proposition.** Suppose a sender gets $G$ and uses fresh independent randomness $R$. From that view it produces a transcript (which may include any ciphertext), selects a real vertex $I$ and guesses a trit $Z$. A holder responds with the original planted label $L_I$. The probability that $Z=L_I$ is exactly $1/3$. This holds conditional on every supported public graph. An abstaining sender has success at most $1/3$ when abstention counts as failure.

**Proof.** Fix any permutation $\pi$ of the three labels. Replacing all $L_i$ by $\pi(L_i)$ preserves their joint law and every predicate $L_i\ne L_j$. Keeping all edge coins fixed therefore leaves the public graph identical. Condition on any supported $G=g$. For every real vertex $i$, the conditional probabilities of the events $L_i=0,1,2$ are equal by the permutation symmetry. They sum to one. Conditioning additionally on the sender's independent coins leaves this true. With $g$ and the coins fixed, the transcript, $I$ and $Z$ are fixed. Hence the success probability is $1/3$. Averaging over the coins proves the proposition. The same argument applies to a derived public potential because the potential is a deterministic function of $G$.

Even a triangle exhibits the problem. Its only proper partition consists of three singleton vertices. There are still six assignments of the three **named** colors to those vertices. At each vertex every possible label occurs twice. Identifying the correct partition in this case does not recover the holder's label name.

The proof concerns agreement on the absolute color, or on an injective recoding of it. It neither analyzes secrets invariant under global label permutations nor models published color anchors or a private input-dependent reconciliation protocol. A constant recoding can yield agreement while carrying no entropy. Any other proposed encapsulation map needs its own correctness and secrecy arguments.

## Exact sizes and checks

With $v$ supplied out of band, the public graph naively uses one bit per possible edge. We store bits for unordered pairs in lexicographic order, beginning at the least significant bit, in a little-endian byte string of length $\lceil\binom v2/8\rceil$. Unused high bits must be zero. This is the fixed layout of the experiment. No compression optimality claim is made for planted graphs. The private encoding uses the [shared canonical ternary codec](research_kem.py) and requires $\lceil v\log_2(3)/8\rceil$ bytes. The generated table is uniform on all $3^v$ possibilities before publication. A shorter fixed-length seed cannot reproduce this exact table distribution, since it has fewer than $3^v$ possible outputs. A different compact key distribution would be a separate candidate. These lengths describe a public instance and its witness. The experiment does not produce a KEM ciphertext or shared key.

| Real vertices | Graph bytes | Packed-color bytes |
| ---: | ---: | ---: |
| 3 | 1 | 1 |
| 16 | 15 | 4 |
| 256 | 4,080 | 51 |

The [tests](test_planted_policy.py) enumerate all 237 equally weighted color/coin configurations within the separate sizes one, two and three and check all 29 supported graph/vertex posterior histograms. They also compile three three-vertex fixtures and directly test $P(z)=P(z+h)$ in 486 challenge-and-response evaluations, including invalid addresses and malformed transcripts. A separate check confirms that giving adjacent vertices the same color violates an actual compiled potential on a correct edge transcript. Run from the repository root with

```sh
python3 -m unittest discover -s research-2028/round11 -p test_planted_policy.py -v
```
