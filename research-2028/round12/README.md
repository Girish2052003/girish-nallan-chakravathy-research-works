# Round 12 · What breaking the KEM would prove

A sender samples a ternary vector $x$, sends the public image $c=F_{pk}(x)$, and hashes the framed public key and $x$ to derive a 32-byte shared key. The receiver must recover exactly that $x$. This round proves how to express this task in SG-DIFRA’s finite-difference mathematics. It also determines what happens when two concrete secret-key constructions instantiate the protocol.

## A security reduction to a specified collision search

Given just the public key, compile its arithmetic evaluation circuit into **one** sparse cubic vector potential $P_{pk}$. For **every** ciphertext point $c$, its preimages correspond one-to-one to solutions of

$$P_{pk}(z+(1,c,0))=P_{pk}(z).$$

The final zero block covers both the preimage and the circuit wires. The potential stays fixed when the challenge changes. A witness contains the preimage, and a preimage uniquely determines the full witness. A public tag in constant components preserves the exact public-key encoding while leaving every collision intact. The compiled potential is a mathematical representation of the public computation. The sender still transmits only the encoded point $c$.

For example, over arithmetic modulo three let $F(a,b)=(a,b+a^2)$. For the received value $(2,1)$, the first coordinate forces $a=2$. Since $2^2=1$ in this field, the second coordinate forces $b=0$. The cubic instance has exactly one witness, with preimage $(2,0)$. In a secure family this correspondence would still hold, but recovering the witness on random generated keys would need to be hard for an observer.

**Security consequence.** In the classical random-oracle model, a one-stage IND-CCA distinguisher with raw probability gap $\Delta$ gives a solver of this generated collision search with success at least $\Delta$. In the quantum random-oracle model, the bound is $\Delta^2/(4q_H^2)$ for $q_H\ge1$ hash queries, classical decapsulation queries and the independent auxiliary ideal oracle specified in Round 11. IND-CPA follows by taking zero decapsulation queries. Conversely, search success $p$ gives a passive gap of $p(1-2^{-256})$. These results concern a uniform ciphertext under an honestly generated permutation key. On every potential in this distribution, the universal Round 9 decision question already has answer YES. The Round 10 worst-case NEXP theorem supplies no hardness bound for extracting the witness here. [Proof, game definitions and two-stage bounds](GENERATED_DIFFERENTIAL_REDUCTION.md) · [Compiler](differential_bridge.py) · [Underlying KEM transform](../round11/TRANSFORM.md)

## What happens with actual private keys

| Construction | Receiver’s capability | What the public information reveals |
| --- | --- | --- |
| Masked Coulter–Matthews differential | Undo two affine masks and recover a unique field root. This works for every ciphertext when $3$ does not divide the extension degree. | The published cubic coefficients determine the unique preimage in deterministic polynomial time for every generated key. [Proof](PLANAR_FAMILY.md) |
| Two quadratic triangular layers with affine mixing | Undo the affine maps and reverse the shears one coordinate at a time. This gives perfect recovery in permutation mode. | The reduced quartic coefficients determine a polynomial-size inverse circuit. The same method perfectly detects the proposed rank-loss mode. The proof extends to every fixed number of the specified triangular layers. [Proof and prior work](TWO_LAYER_PROOF.md) |
| Round 11’s planted three-color graph | The private table supplies a consistent color for each vertex. | With high probability the graph reveals the partition up to color names. Publicly sampling those names suffices to simulate decapsulation for **any** correct KEM retaining exactly these keys. [Theorem and finite bounds](PLANTED_KEY_THEOREM.md) |

For the first two rows, the observer can recover the 32-byte shared key from an honest ciphertext. Comparing that value with a challenge key gives gap $1-2^{-256}$ without asking the receiver any questions. This holds even with the concrete, publicly computable KDF. The polynomial complexity results are asymptotic. We did not measure a full-size public inversion. The third row is a separate probability statement about a specific key sampler, allowing arbitrary public encapsulation and fresh sender randomness.

## Exact dimensions and wire costs

The field family uses the smallest extension degrees meeting the indicated domain sizes and the requirement $3\nmid n$. The actual public encoding stores all reduced coefficients. Its width is $\lceil n(\binom{n+3}{3}-n)\log_2(3)/8\rceil$ bytes. Each field point uses $\lceil n\log_2(3)/8\rceil$ bytes. Suite and dimension are supplied out of band.

| Domain contains at least | Field degree | Dense public key | Stored private seed | Ciphertext | Shared key |
| --- | ---: | ---: | ---: | ---: | ---: |
| $2^{128}$ inputs | 82 | 1,603,272 B | 17 B | 17 B | 32 B |
| $2^{192}$ inputs | 122 | 7,677,285 B | 25 B | 25 B | 32 B |
| $2^{256}$ inputs | 163 | 24,171,671 B | 33 B | 33 B | 32 B |

These are exact sizes for the defined format. Finite field tests exercise the central private inverse at all three dimensions. Complete masked keys and KEM round trips are tested at small dimensions. No profile has an established $2^{191}$ work factor, and there is no positive security rating for these two constructions. The [two-layer cost analysis](TWO_LAYER_COSTS.md) gives the corresponding counting formulas and distinguishes calculated large layouts from small measurements.

## Reproduce

From the repository root, with Python 3.10 or later, run

```sh
python3 -m unittest discover -s research-2028/round12 -p 'test_*.py' -v
```

The local run under Python 3.12.14 passed all 28 Round 12 test methods. The earlier Round 9, 10 and 11 suites passed 21, 22 and 16 methods respectively. The new tests cover the generated cubic relation, arithmetic, exact private inversion, canonical byte layouts, KEM agreement, rejection and the finite graph probabilities. The algebraic proofs establish the asymptotic results. For one exact KEM vector, the test at field degree four fixes the private seed to hex `000102030405060708090a0b0c0d0e0f` and the encapsulation input to base-three rank four. It produces ciphertext `4c` and shared key `fbfc817ec81fc0f715d3bb2c5c8f6785497e92608f1e559e70b545d980bd8a34`. [Public-only sender and known-answer tests](test_planar_backend.py) · [Two-layer fixtures](test_two_layer.py) · [Field arithmetic](test_field3.py) · [Graph probabilities](test_planted_bound.py) · [Witness correspondence](test_differential_bridge.py)
