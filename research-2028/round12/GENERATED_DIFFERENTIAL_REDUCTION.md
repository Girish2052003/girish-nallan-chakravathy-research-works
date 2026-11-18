# What a KEM distinguisher solves on generated differential instances

Fix a key generator from the [Round 11 KEM theorem](../round11/TRANSFORM.md). Assume each honestly generated key defines a permutation $F_{pk}:D\to D$, where $D=\mathbb F_3^n$, an efficient private inverse, and a publicly constructible polynomial-size arithmetic circuit for evaluating $F_{pk}$. Under those premises, a distinguisher against the hashed-permutation KEM yields a solver for a specific cubic finite-difference search distribution. The search and public permutation inversion have identical optimal success up to the stated polynomial conversion costs. The distribution is defined independently of the hash and of the KEM distinguishing game.

## One cubic potential for a public key

Construct a deterministic, topologically ordered ternary straight-line circuit from $pk$. Each gate produces one fresh trit $w_j$. A gate is multiplication of two wires or field constants, or an affine combination of earlier wires and input trits, with any number of explicitly listed operands. An output $o_i$ is a wire, an input, or a field constant. The reference implementation expresses a literal constant operand or output using an affine gate of arity zero. A public encoding specifies the ordering and the $n$ output indices. For input trits $x=(x_i)$, write $w(x)$ for the complete evaluated gate transcript. Let the residual of gate $j$ be $R_j(x,w)=w_j-g_j(x,w_{<j})$.

For $g$ gates use variables $z=(s,u,x,w)$ in blocks of lengths $1,n,n,g$. For a ciphertext point $c\in D$ define the genuine translation $h_c=(1,c,0,0)$. First form the following active components, once per key, before choosing $c$:

$$
P^{\rm active}_{pk}(s,u,x,w)=
\left(
\tfrac12 s(s-1),\quad
((s-1)u_i)_{i=1}^n,\quad
(sR_j(x,w))_{j=1}^g,\quad
(s(o_i(x,w)-u_i))_{i=1}^n
\right).
$$

Here $1/2=2$ in the field. The challenge slots $u$ move while the potential, proposed preimage $x$ and wire values $w$ stay fixed. This uses the clock and pinning construction of [Round 9, Theorem 4](../round9/CHALLENGE_COUPLED_DIFFERENTIAL_SOLVABILITY.md) with ternary arithmetic directly on the preimage.

To make the bare Round 9 instance self-contained, append one constant-zero output component as a delimiter. Next append one constant component $1+b$ per bit $b$ of a public byte string $t$, in byte order, most significant bit first. Call the resulting potential $P_{pk}$. In an experiment with a fixed public suite and dimension, $t$ is the canonical public-key encoding. If parameters vary, $t$ is a publicly parseable, length-framed encoding of the suite, dimension, and public key. The decoder reads the maximal trailing sequence of constant-one or constant-two components, requires the preceding zero component, and converts the sequence back to bytes in its original order. Even an empty string has its own delimiter. The tag changes no finite differences. It preserves all information needed to run the KEM adversary using only $P_{pk}$.

**Theorem 1 (bijection per challenge).** For any public arithmetic map of this form, including a map that is not a permutation, projection to $x$ is a bijection

$$
\{z:P_{pk}(z+h_c)=P_{pk}(z)\}\longrightarrow F_{pk}^{-1}(c).
$$

Its inverse is $x\mapsto(0,0,x,w(x))$.

**Proof.** The differences of the first component and the next $n$ components are $s$ and $u_i+s c_i$. At a collision these equations first force $s=0$, then $u=0$. At such a basepoint the remaining differences are precisely $R_j(x,w)$ and $o_i(x,w)-c_i$. Induction in circuit order forces every $w_j$ to its evaluated value, including any unused intermediate gates. Conversely, evaluating the circuit on a preimage gives zero differences in every component. The two maps are inverses, even when there are no preimages.

The tagged potential has $1+2n+g$ variables, $2+2n+g+8|t|$ outputs, and total degree at most three, where $|t|$ is the tag length in bytes. More generally, for $k$ raw inputs and $m$ selected outputs, the same construction has $1+m+k+g$ variables and $2+2m+g+8|t|$ outputs. Its witness bijection requires no restriction on $k,m$ or on output-wire reuse. With $g_\times$ multiplication gates and affine arities $a_j$, the total number of nonzero monomial occurrences is at most

$$
2+4m+8|t|+2g_\times+\sum_{j\text{ affine}}(2+a_j).
$$

Combining equal terms can only decrease the count. Canonical sparse coordinate and output indices take $O(\log(2+k+m+g+|t|))$ bits each. The KEM uses $k=m=n$. Lifting a preimage needs one circuit evaluation. Projection reads the $n$ preimage trits. This representation is a proof device and adds no bytes to the Round 11 ciphertext.

**Example.** Let $F(x_1,x_2)=(x_1,x_2+x_1^2)$. For the empty-tag illustration use $w_1=x_1^2$, $w_2=x_2+w_1$, and output $(x_1,w_2)$. For $c=(2,1)$, the unique preimage is $(2,0)$. In the order $(s,u_1,u_2,x_1,x_2,w_1,w_2)$, the basepoint $(0,0,0,2,0,1,1)$ and its translate $(1,2,1,2,0,1,1)$ both have the all-zero potential value.

## The exact average-case search game

Sample $(pk,sk)$ from the specified key generator independently of all ideal hash functions. Draw $X$ uniformly from $D$, set $C=F_{pk}(X)$, and hand the solver the bare Round 9 pair $(P_{pk},C)$. It succeeds by returning any $z$ with $P_{pk}(z+h_C)=P_{pk}(z)$. The public tag recovers the canonical key bytes and any nonfixed parameters. Conversely, this public information deterministically reconstructs the entire potential. A permutation makes $C$ uniform given $pk$, and gives exactly one collision basepoint for every $C$.

**Theorem 2 (inversion equivalence).** Given $(P_{pk},C)$, a collision solver can read the public tag, run an inverter on $(pk,C)$, and lift its returned preimage using the reconstructed circuit. Conversely, an inverter can compile $P_{pk}$, run a collision solver, check the returned basepoint, and project it to $x$. On success each direction preserves probability exactly. Invalid answers may be verified and mapped to failure. Both transformations work pointwise and hence for the sampled distribution, also with the same independent auxiliary oracle in quantum experiments. Encoding the public tag inside the listed potential preserves the exact game even when distinct canonical key encodings yield the same evaluation map. The proof needs no external key as advice to the collision solver.

## Conditional IND-CCA and IND-CPA reductions

Use the single-user hashed-permutation KEM and its canonical byte framing from Round 11. The ciphertext encodes $C$ and the shared key is $H(S_{pk}(X))$, where $S_{pk}$ injectively frames the suite, dimension, public key and preimage with the KDF domain. Honest decapsulation using the private inverse agrees with probability one. Write $\Delta$ for the absolute difference between real-game and random-game acceptance probabilities. In the one-stage adaptive game, decapsulation has classical access and excludes the exact challenge ciphertext.

**Corollary 3.** For a classical random-oracle distinguisher there exists a solver for the generated differential game with success $p_{\rm cl}$ such that

$$
\Delta_{\rm cl}\le p_{\rm cl}.
$$

For a quantum random-oracle distinguisher making $q_H\ge1$ hash queries, there exists a solver with success $p_{\rm q}$ such that

$$
\Delta_{\rm q}\le\min\{1,\,2q_H\sqrt{p_{\rm q}}\}.
$$

The quantum solver has an independent auxiliary ideal quantum random function as in Round 11. Both games have gap zero with no hash queries in this one-stage convention. For two-stage games permitting $q_{\rm pre}$ classical prechallenge decapsulations, add $2q_{\rm pre}/3^n$ to the respective upper bounds and clip at one. Removing decapsulation access gives the IND-CPA specialization.

**Proof.** Round 11 simulates nonchallenge decapsulation by associating an independent random label $G(y)$ to each output point $y$. On framed preimages the simulated hash is $G(F_{pk}(x))$. Bijectivity makes this a random function and preserves consistency. Reprogramming the value on the unique challenge preimage couples the random and real games. A classical query at that input supplies a preimage. In the quantum proof, measuring a uniformly chosen query input and applying the hybrid bound gives the displayed factor $2q_H$. These are exactly the inversion reductions proved in [Round 11](../round11/TRANSFORM.md), with its processing costs, ideal-oracle model and prechallenge correction. Apply the lifting direction of Theorem 2 to each recovered preimage. The extra work after inversion is one public arithmetic circuit evaluation. In particular, a one-stage gap $\Delta>0$ gives success at least $\Delta$ classically and at least $\Delta^2/(4q_H^2)$ in the stated quantum experiment.

**Converse.** A collision solver of success $p$ gives an IND-CPA distinguisher of raw gap $p(1-2^{-b})$ for a $b$-bit shared key. Run the solver without giving it the challenge key, check the witness, and return zero on failure. On success, project to $x$, query $H(S_{pk}(x))$ and test equality with the challenge key. Real acceptance has probability $p$. Random acceptance has probability $p2^{-b}$. Any auxiliary random function required by the solver can be supplied independently, or implemented by domain separation on a disjoint ideal-hash slice. For example, for an auxiliary oracle with the same output width, prefix its input bytes by `ff` (hex). The target KDF slice begins with the eight-byte length of a short fixed domain label, so these inputs are disjoint. This simulation works coherently and uses one public ideal-hash call per auxiliary call, plus one comparison hash on a successful witness. The distinguisher needs no decapsulation queries.

Every generated potential here already satisfies the universal Round 9 decision question. A decision oracle that simply answers YES is correct throughout this distribution and need not produce a witness. Thus the proved equivalence identifies the exact *generated fixed-challenge search* assumption for this KEM. Establishing it requires a specific key generator whose public circuit resists inversion on uniformly sampled images. The planar and two-layer controls in this round admit public polynomial-time recovery. The reduction gives neither control a positive security level, and supplies no concrete finite-size work factor for a future family.
