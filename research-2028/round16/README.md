# One generated witness problem for standalone SG-DIFRA

Round 16 gives the standalone KEM one explicit hardness question at each target. If an efficient quantum observer can distinguish the real shared key from a random one with sufficient advantage, the reduction yields a solver for a fresh instance of the following problem. The solver's success and resources depend on the observer's advantage and the cost of simulating it. This is a conditional result for a code-based KEM with its own private decoder. A concrete security rating remains open.

## What does the solver receive?

Choose a uniformly random matrix $B$ over $\mathbb F_3$. Secretly choose a vector $e$ by selecting exactly $w$ positions uniformly and putting an independent 1 or 2 in each selected position. Publish $B$, $w$ and $y=Be$ modulo three. The solver must return a vector of weight $w$ that gives the published $y$. Here weight counts the nonzero positions as an ordinary integer. The row and column counts below specify the complete public matrix in the underlying hardness experiment. The KEM has its own seeded public-key format.

For example, take $B=\left(\begin{smallmatrix}1&0&1&2\\0&1&2&1\end{smallmatrix}\right)$ and $e=(1,0,2,0)^\top$. Then $w=2$ and the two row sums before reduction are 3 and 4, so the public syndrome is $(0,1)^\top$. The [cubic differential encoding](../round14/WEIGHTED_DIFFERENCE.md) preserves each witness. The [uniqueness proof](UNIQUE.md) bounds the chance that two allowed vectors share a syndrome on a random matrix at the registered dimensions. Uniqueness tells us how many answers exist. Computational hardness concerns how much work it takes to find one.

## What changed in the KEM?

In the new layout the number of rows used to hide the receiver's private checks equals the number of parity checks needed to analyze the sender's noise. A random permutation and fresh random columns take one instance of the shorter public problem to the exact distribution needed for the longer one. The receiver still uses the private disjoint checks and the existing error-correcting decoder. The [security proof](MATCHED_PROOF.md) gives the IND-CPA and IND-CCA inequalities for one honest recipient, quantum access to the ideal hash functions, and classical adaptive decapsulation queries. The implementation instantiates the hashes with domain-separated SHAKE256.

| Target label | Public problem rows × columns | Weight | Public key, bytes | Private key, bytes | Ciphertext, bytes |
|---|---:|---:|---:|---:|---:|
| 128 | 5,478,678 × 8,209,152 | 768 | 3,868,545,931 | 80 | 2,169,320 |
| 192 | 12,119,412 × 18,161,280 | 1,152 | 12,620,284,606 | 96 | 4,798,645 |
| 256 | 21,397,976 × 32,067,072 | 1,536 | 29,506,137,220 | 112 | 8,472,375 |

All three return a 32-byte shared key. The table gives exact serialization widths calculated from the implementation. The end-to-end runs used small instances. The reference Python code is variable-time. At the middle target the public key is about 16% smaller than the [previous standalone layout](../round15/SIZES.md). It still exceeds 12 GB.

For readers keeping the earlier wire format, a [separate folding proof](FOLDING.md) links the two old security games to a common search distribution with different dimensions. The note identifies a quantitative limit of that reduction at the middle target.

## What would substantiate the 192 target?

The open task is to evaluate full-input classical and quantum decoding at the exact middle-row dimensions. An assessment should specify the success probability, time, working memory, matrix access and preprocessing for the best applicable methods. It should compare those resources with the quantitative losses in the [reduction](MATCHED_PROOF.md). An oracle-query budget of $2^{191}$ and a claimed requirement of $2^{191}$ physical operations are different quantities. Concrete estimates must also identify which evidence supports the hardness assumption. A lower cost found by any applicable algorithm would constrain the claim, while benchmarking a collection of methods cannot prove a lower bound on every algorithm.

## Run the reference example

From `research-2028/round16`, run the following with Python 3. It generates an actual small key pair, encapsulates and checks the recipient's answer. The printed lengths are `1675 34 107 32` in bytes.

```sh
python3 - <<'PY'
from matched_kem import MatchedKEM

kem = MatchedKEM(16, 2, 3, slack=64, nonce_bytes=16)
pk, sk = kem.keygen()
ct, sender_key = kem.encaps(pk)
assert kem.decaps(sk, ct) == sender_key
print(len(pk), len(sk), len(ct), len(sender_key))
PY
python3 challenge.py
python3 challenge.py --cubic
python3 -m unittest discover -s . -p 'test_*.py' -v
```

The challenge generator emits only public data. The tests check small exchanges, rejection of malformed ciphertexts, the finite distribution identities, witness encodings, uniqueness estimates, parameter sizes and numerical reduction bounds.
