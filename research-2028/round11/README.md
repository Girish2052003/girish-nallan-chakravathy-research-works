# From local differential collisions to key encapsulation

**Round 11 · 18 November 2026 · SG-DIFRA research implementation**

Can the recipient's short private key solve an SG-DIFRA challenge that a sender can create and an outsider cannot solve? We built two experiments. The first instantiates a planted private strategy in the exact Round 10 graph compiler. The second implements three end-to-end KEM operations and a finite-difference permutation whose private decoder is fast. Both identify a concrete missing property. **This round supplies working research code and negative results. A secure original SG-DIFRA KEM and its three claimed security strengths remain open.**

## The experiments

| Experiment | What succeeds | What happens to secrecy |
| --- | --- | --- |
| Planted Round 10 graph | Key generation creates a graph and a private coloring. The receiver can consistently answer all challenges using that coloring. | The sender's public information does not identify the receiver's absolute color, even with unlimited computation. For a vertex selected using that information, any sender guess succeeds with probability exactly $1/3$. |
| Finite-difference permutation control | KeyGen, Encaps and Decaps run end to end, including packing, 32-byte key derivation and ciphertext validation. For every key and every input, the receiver recovers the sender's key. | The public translation vector also suffices to invert the permutation. Its IND-CPA distinguishing gap is $1-2^{-256}$. It consequently fails IND-CCA as well. |
| Hashed-permutation transform with a future backend | The interfaces and proof specify exactly how a genuine private inverse would give key agreement and how an IND-CCA adversary would yield an inverter in ideal-oracle models. | No concrete SG-DIFRA backend currently satisfies the required average-case one-wayness. The theorem does not instantiate that premise. |

### A receiver who knows a winning policy

Sample ternary colors for vertices, then sample edges only between differently colored vertices. The secret coloring gives the two local functions that the Round 10 construction requires. Relabel all three colors by one permutation and the graph distribution stays the same. The public graph cannot tell the sender which absolute name the receiver stores for a color. Conditioning on the graph and on independent sender randomness leaves a selected vertex's color uniform. The code checks agreement with the actual cubic potential. This result is specific to the proposed absolute-color secret; a protocol using a different, relabeling-invariant quantity needs a fresh agreement and hiding argument. [Sampler, symmetry proof and tests](PLANTED_POLICY.md)

### A fast decoder that everyone can use

For $x,b\in\mathbb F_3^n$ with $n\ge3$, the test backend uses

$$
 F_b(x)=x+b+e_3x_1x_2,\qquad P_b(s,x)=sF_b(x).
$$

Here $e_3$ is the third unit vector, using mathematical indices starting at one. The difference in the clock direction is $P_b(s+1,x)-P_b(s,x)=F_b(x)$. The sole cubic term in the potential is $s x_1 x_2$ in the third output. This control sends a generally nonzero image value. In fact $P(s,x)=sF(x)$ represents any map $F$ by a clock difference. The representation itself confers no one-wayness. It does not query the universal Round 10 decision language.

KeyGen samples $b$, publishes its canonical packing and stores the packing of $-b$. To invert $y$, subtract $b$ coordinatewise, obtaining $u$. The first two entries of $u$ equal $x_1,x_2$; its third entry is $x_3+x_1x_2$. Subtract the product from that third entry. This proves bijectivity and perfect correctness. The public key determines the stored private vector and all of these operations. In a CPA experiment an observer can compute the honest 32-byte key from each ciphertext and compare it with the challenge key. The comparison succeeds with probability one in the real experiment and $2^{-256}$ in the random experiment. These are exact probabilities for this control, with the concrete public KDF as well as an ideal hash. They disqualify the control at all three dimensions. [Code](research_kem.py)

The direct Round 10 construction cannot gain a trapdoor merely by increasing dimensions. For its exceptional clock term, fixing either one of the two stationary factors leaves an affine system. Trying that factor's three possible values suffices to recover a valid witness for a **specified** public challenge and target whenever one exists. The same distinction applies to a canonical witness. The general sparse-cubic bound, the limits of this conclusion for a distinguished planted witness, and a complexity barrier to a direct worst-case reduction appear in the [feasibility proof](FEASIBILITY.md).

## KEM interface and security statement

Choose a backend explicitly. It must sample a key pair, validate its public key, evaluate a permutation $F_{pk}$ of the entire ternary domain, invert it with $sk$, and recover the exact public encoding from $sk$.

1. **KeyGen** returns the backend's matching typed public and private keys.
2. **Encaps** samples an exactly uniform ternary vector $x$, sends the unique fixed-width encoding of $F_{pk}(x)$, and derives 32 bytes from the suite, dimension, public key and packed $x$.
3. **Decaps** rejects any malformed or noncanonical ciphertext with a failure result, applies the private inverse to the parsed image and uses the same key derivation.

On the wire the first trit is the most significant base-three digit. Its integer rank is encoded in fixed-width big-endian bytes. An unused rank or an additional leading byte is invalid. The Python KDF uses SHAKE256 and separately prefixes each field with its eight-byte big-endian byte length. In order, the fields are the fixed protocol label, suite identifier, eight-byte dimension, public encoding, and packed preimage. The suite and dimension are agreed out of band. The code is a correctness reference and contains no constant-time engineering or side-channel validation.

In the conditional security theorem, a successful IND-CCA adversary gives an inverter on a **uniform image under a fresh generated public key**. Classical and quantum hash-query bounds, the treatment of malformed ciphertexts, and the model of decapsulation queries are explicit. IND-CPA follows by allowing zero decapsulation queries. The theorem uses the established hashed-permutation design; security of the concrete SHAKE256 implementation and one-wayness of a new SG-DIFRA algebraic primitive would be additional claims. [Transform and security reductions](TRANSFORM.md) · [NIST SP 800-227](https://doi.org/10.6028/NIST.SP.800-227)

## The three requested profiles

| Nominal goal | Domain of the control | Public key | Stored private key | Ciphertext | Shared key |
| --- | --- | ---: | ---: | ---: | ---: |
| 128 bits | 81 trits | 17 B | 17 B | 17 B | 32 B |
| 192 bits | 122 trits | 25 B | 25 B | 25 B | 32 B |
| 256 bits | 162 trits | 33 B | 33 B | 33 B | 32 B |

These lengths are optimal fixed-width encodings of the respective full vectors. The control transmits no matrix. A secure instantiation has no established public-key, private-key or ciphertext byte count. For a uniform 192-bit secret, $2^{191}+1/2$ is the expected number of guesses for one blind, nonrepeating enumeration when the correct guess is publicly recognizable. The repository's separate historical $2^{191.72}$ estimate concerns one clean-basis method at its archived **128-target** profile. Neither number implies a lower bound against classical or quantum algorithms. [Integer calculations and archived dimensions](SIZES.md)

## Reproduce

Run the following from the repository root with Python 3.10 or later.

```sh
python3 -m unittest discover -s research-2028/round11 -p 'test_*.py' -v
python3 research-2028/round11/profile_sizes.py
```

The [verification record](VERIFICATION.md) includes a deterministic test vector. For an interactive check, start Python in this directory and run

```python
from research_kem import PublicShearControl, ResearchKEM

control = ResearchKEM(PublicShearControl(122))
public, private = control.keygen()
ciphertext, sender_key = control.encaps(public)
receiver_key = control.decaps(private, ciphertext)
assert receiver_key == sender_key
assert list(map(len, (public.encoded, private.encoded, ciphertext, sender_key))) == [25, 25, 25, 32]
```

## Remaining cryptographic question

A positive native result would need a specified distribution of public keys and ciphertexts, private recovery of the sender's particular secret, and evidence that public recovery on this distribution is hard. To derive the requested worst-case guarantee, one would further need a reduction that uses an average-case KEM adversary to solve arbitrary instances of the claimed hard problem, with a stated success probability, resource loss and oracle model. The deterministic valid-ciphertext recovery route is ruled out under the hypotheses of the feasibility proof. An asymptotic reduction alone would still leave concrete profile security, byte costs and implementation behavior to establish. Existing CSP-based encryption illustrates why these details matter: published constructions specify their own planted distributions and decoding structure. [Hair and Sahai, April 2026 version](https://arxiv.org/abs/2604.10479v1)
