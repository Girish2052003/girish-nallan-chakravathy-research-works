# What a target of 2^b queries requires

A Round 11 ciphertext encodes the image of a uniformly chosen point under a publicly evaluable permutation on $N=3^n$ points. The unique preimage determines the shared key. This note asks two finite questions. How large must the domain be before generic search takes a specified number of queries for a one-half chance of recovery? How large must it be before the particular Round 12 quantum reduction could certify a one-half upper bound on the raw distinguishing gap using a worst-case-over-algorithms inversion bound? Both questions give necessary size filters. Passing them establishes no security rating. For native candidates with a different challenge distribution or a many-to-one map, the marked set and verification predicate must be identified afresh.

## Classical trials and quantum phase queries

Put $B=2^b$. A blind, nonrepeating classical search considers $k$ candidate inputs with recovery probability $k/N$ under a uniform challenge. Its first one-half success occurs at $\lceil N/2\rceil$ trials. Its mean position of the correct input is $(N+1)/2$. Here a trial counts one candidate including the final tested or guessed candidate. Requiring the first one-half point to be at least $B$ gives $N>2B-2$. In particular, for exactly $2^{192}$ uniformly distributed possibilities, the average position is $2^{191}+1/2$. An algebraic way to recover the preimage could take far less work.

For quantum search, one phase query marks all inputs mapping to the challenge. Start in a uniform superposition of the domain. More generally let $t$ be the number of marked inputs, with $1\le t\le N$, and set $\theta=\arcsin\sqrt{t/N}$. The standard search iteration rotates the two-dimensional state by $2\theta$, so after $j$ iterations its recovery probability is $\sin^2((2j+1)\theta)$. This calculation counts abstract phase calls. It omits reversible public-map computation, uncomputation, state preparation, reflections, gates, memory, clock speed and error correction. [Boyer, Brassard, Høyer and Tapp, *Tight bounds on quantum searching*](https://arxiv.org/abs/quant-ph/9605034)

The first $j$ giving probability at least one half is

$$J=\left\lceil\frac{\pi}{8\theta}-\frac12\right\rceil.$$

Indeed, for $\theta\le\pi/4$ the first angle crossing $\pi/4$ lies at most $2\theta$ beyond it, and hence at most $3\pi/4$. For $\theta\ge\pi/4$, $j=0$ already suffices. Therefore

$$J\ge B\quad\Longleftrightarrow\quad N>t\,\csc^2\!\left(\frac{\pi}{8B-4}\right).$$

The single-target permutation game has $t=1$. For $t$ distinct target ciphertexts under **one** such key, the same calculation applies to recovering any of their preimages. A phase call then includes testing membership in the target set. The same-key calculation does not give a multi-user IND reduction. In the named KEM, a solver with success $p$ yields passive raw distinguishing gap $p(1-2^{-256})$. A one-half recovery probability and a one-half distinguishing gap are separate thresholds.

For example, in the Round 12 planar layouts at $n=82,122,163$, respectively, $\log_2 J$ is approximately $63.635$, $95.334$, and $127.826$. These are costs of one generic quantum procedure in its own query units. The [planar proof](../round12/PLANAR_FAMILY.md) already gives a public polynomial-time inverse. Neither computation benchmarks actual hardware.

## What the current quantum reduction can certify

In the one-stage single-user experiment of [Rounds 11 and 12](../round12/GENERATED_DIFFERENTIAL_REDUCTION.md), the raw IND gap obeys $\Delta\le 2H\sqrt{p_R}$ for $H\ge 1$ quantum hash queries. The reduction constructs an inverter $R$ with success probability $p_R$, classical decapsulation access for the adversary, and an independent auxiliary ideal quantum oracle for the inverter. The actual cost of $R$ includes the simulated adversary and the coherent public computations. To obtain a numerical security bound, one possible approach upper-bounds the success of **every** inverter within a resource envelope covering $R$. Denote the optimum in that envelope by $p^\star$. To certify $\Delta\le1/2$ by this substitution, the bound used must satisfy $p^\star\le 1/(16H^2)$.

Suppose the envelope being used includes all the standard search procedures on the unique preimage with at most $Q$ phase queries, including their other required resources. Their known success probabilities already force the following **necessary condition on that proof method**:

$$N\ \ge\ \csc^2\!\left(\frac{\arcsin(1/(4H))}{2Q+1}\right).$$

To prove it, put $\alpha=\arcsin(1/(4H))$ and $\theta=\arcsin(1/\sqrt N)$. If $\theta>\alpha$, sampling at $j=0$ already exceeds the allowable inversion probability. Otherwise, whenever $(2Q+1)\theta>\alpha$, the **first** $j\le Q$ for which $(2j+1)\theta>\alpha$ gives an angle at most $3\alpha<\pi/2$. Its success therefore exceeds $1/(16H^2)$. This argument avoids assuming that search success is monotone for arbitrarily large query counts. Taking $H=Q=B$ gives the table below. Equality of these budgets is an illustrative convention. A comparison against a real adversary must derive the inverter's allowed resources from simulation costs.

The classical one-stage reduction gives $\Delta_{\rm cl}\le p_{\rm cl}$ without the quantum query-measurement loss. Removing the decapsulation oracle gives IND-CPA. The Round 11 two-stage version adds $2q_{\rm pre}/N$ to the appropriate upper bound, where $q_{\rm pre}$ counts classical prechallenge decapsulations. A concrete use in that version must budget for this additional term. None of the reductions replaces independent cryptanalysis of the functions actually published.

## Exact profile diagnostics

Each column has its own experiment. The first two domain columns use the one-half recovery threshold. The seed column assumes a publicly checkable, injective map from a uniform $s$-bit private seed to a public key, so exactly one seed matches. Any matching seed that decodes correctly is an acceptable recovery in a noninjective construction, and the number of matches can change the calculation. For nonuniform seeds the probability law matters. The seed column is in **bits**. Byte counts in the table encode just one whole ternary point with fixed width $\min\{w:256^w\ge 3^n\}$. They would be ciphertext payload sizes for the Round 11 permutation format.

| Exponent $b$ | Classical minimum trits | Quantum minimum trits | Point bytes | Unique seed minimum bits | Reduction minimum trits at $H=Q=2^b$ | Point bytes at that width |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 128 | 82 | 164 | 33 | 259 | 327 | 65 |
| 191 | 122 | 243 | 49 | 385 | 486 | 97 |
| 192 | 122 | 244 | 49 | 387 | 489 | 97 |
| 256 | 163 | 325 | 65 | 515 | 650 | 129 |

In particular the $2^{191}$ row answers the literal question about **serial phase-query count**. NIST security categories 1, 3 and 5 use comparisons with key search on 128-, 192- and 256-bit block ciphers respectively, with attention to computational model and quantum circuit depth. The table does not assign these categories. It also cannot give public-key or private-key byte counts for a future generator. [NIST post-quantum security evaluation criteria](https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization/evaluation-criteria/security-%28evaluation-criteria%29)

## How to reproduce the integers

The calculator uses rational arithmetic. Given $0<u\le x\le v<1$, the elementary bounds $u-u^3/6\le\sin x\le v$ enclose $\csc^2x$. For the first threshold use $3.14<\pi<22/7$. For the second, with $s=1/(4H)$, integrating the derivative of arcsine yields $s\le\arcsin s\le s/(1-s^2)$. After dividing by $2Q+1$, the same sine bounds apply. In every tabulated case the entire rational interval lies strictly between two consecutive powers of the base, which certifies the minimal integer exponent regardless of equality conventions. Test-only floating-point comparisons check the formulas independently at small inputs. From the repository root run

```sh
python3 research-2028/round13/profile_budgets.py
python3 -m unittest discover -s research-2028/round13 -p test_profile_budgets.py -v
```
