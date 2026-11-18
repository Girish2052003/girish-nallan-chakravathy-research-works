# Round 14 · A ternary differential KEM with a private decoder

This supplement gives explicit key generation, encapsulation and decapsulation, and proves that honest parties always derive the same 32-byte key. It gives a **conditional IND-CCA theorem against quantum computation**. The KEM also satisfies conditional IND-CPA security. The theorem assumes sparse errors are hard to find in two precisely specified distributions of random ternary linear systems. Both search problems have exact encodings as fixed-challenge cubic SG-DIFRA collisions.

This is a **code-based extension of SG-DIFRA**. A cubic finite difference is computed during encryption. The proof of secrecy relies on random-code decoding. It does not establish a code-free NCSG assumption, a numerical quantum work factor, or the security of any preceding candidate. The three illustrated large layouts are too costly for practical deployment. The reference implementation is variable-time research Python. No full-size key was generated for the size calculations.

## How the receiver gets the key

1. The receiver chooses a random ternary matrix and a collection of secret, signed groups of column positions. Each position belongs to at most one group. The public key includes one check column for each group, equal to its signed sum of matrix columns. The private key retains the groups.
2. The sender chooses a fresh, uniformly random message. The sender encodes it with a public error-correcting code and masks it using a finite difference of the public cubic map. A small fixed number of signed errors is added. The sender hashes the message to obtain the shared key.
3. The receiver applies the secret groups to subtract the masks. Each error can spoil at most one recovered coordinate. The public error-correcting code recovers the original message. The receiver reconstructs the entire ciphertext and derives the same key only if every byte matches. The full formal algorithms also bind the hash inputs to the suite and public key.

For a one-bit example, repeat the bit 1 as three trits. A single allowed error can change a private-check result to $(1,0,1)$. The other two coordinates still give the receiver the bit 1. The proof extends this reasoning to *all* valid keys, messages and sender coin tapes. The primary layouts use a public Reed–Solomon code to carry more message bits per check.

## The security result

| Statement | Result |
|---|---|
| The recipient always recovers the honest sender's key | Proved for all allowed errors, including the implemented finite coin sampler |
| IND-CPA | A successful message distinguisher separates planted sparse syndromes or noisy random codewords from uniform, up to explicit statistical terms |
| IND-CCA | Single-recipient theorem in the quantum random-oracle model, with adaptive classical decapsulation queries and explicit rejection |
| Connection to SG-DIFRA | A nonnegligible KEM distinguisher in the asymptotic family gives a quantum solver for one of two generated fixed-challenge cubic witness distributions, subject to the negligible terms and resources specified in the proofs |
| Three finite security targets | Exact wire-size arithmetic and sufficient bounds on the underlying distinguishing advantages. The actual decoding costs at these dimensions remain open |
| Originality and implementation assurance | A research construction combining established code-based encryption ideas, discrete differences and the FO transform. Priority and side-channel resistance have not been established |

The two decoding experiments can be specified before defining any KEM. One asks for a sparse vector underlying a public check column. The other concerns sparse errors in a random linear codeword. The reduction to SG-DIFRA preserves the corresponding search witnesses and their instance distributions. It does not turn a break into a solver for every instance of the earlier worst-case universal or strategy problem.

## Proofs and source

| Question | Where to look |
|---|---|
| What distributions and private equations does the base scheme use? | [Base construction, correctness and CPA proof](BASE_PROOF.md) · [PKE](differential_pke.py) |
| Why can the receiver correct every allowed error? | [Public outer code](OUTER_CODE.md) · [Encoder and decoder](outer_code.py) |
| How does chosen-ciphertext security follow, and what does the reduction lose? | [QROM proof and assumptions](CCA_PROOF.md) · [KEM](differential_kem.py) |
| What search problem would distinguishing solve? | [Quantum witness reduction](WITNESS_PROOF.md) · [SG-DIFRA collision bijection](WEIGHTED_DIFFERENCE.md) · [Compiler](weighted_difference.py) |
| What is transmitted and what does it cost? | [Parameter calculations and query budgets](PARAMETERS.md) · [Size calculator](parameters.py) |
| How can recipients transmit fewer matrix entries? | [Seeded per-key encoding and additional ideal hash assumption](SEEDED_MATRIX.md) · [Shared-matrix encoding and setup cost](SHARED_MATRIX.md) |

The seeded option transmits a 32-byte public seed with the check columns. Its private key stores just the seed and signed supports. Each party must still generate and process the public matrix. The shared-matrix option uses a fully uniform authenticated setup. The original dense encoding proves the base result without a seeded matrix assumption. An optional [two-seed private format](PRIVATE_SEED.md) keeps only the public matrix seed and a secret expansion seed, with a separate hash domain for secret expansion. Its quantum random-oracle proof includes the cost of queries to that domain. With a concrete expander its pseudorandomness is a further premise. Each representation includes its own stated setup, oracle and resource costs.

## Reproduce a complete exchange

From the repository root, run the following with Python 3. The parameters in this example are small enough for a laptop.

```sh
cd research-2028/round14
python3 - <<'PY'
from differential_kem import DifferentialKEM
from differential_pke import Params

p = Params(bits=16, h=12, n=3, m=256, w=3, z=3, slack=64, outer="rs")
kem = DifferentialKEM(p, nonce_bytes=16)
public, private = kem.keygen()
ciphertext, sender_key = kem.encaps(public)
assert kem.decaps(private, ciphertext) == sender_key
changed = bytes([ciphertext[0] ^ 1]) + ciphertext[1:]
assert kem.decaps(private, changed) is None
print(len(public), len(private), len(ciphertext), len(sender_key))
PY
python3 -m unittest discover -s . -p 'test_*.py' -v
python3 parameters.py
```

The 16-bit toy exchange prints `1020 1118 73 32` in bytes. For the shortest private-key format, substitute `from private_seed import PrivateSeedKEM` and `kem = PrivateSeedKEM(p, nonce_bytes=16)`. This toy exchange prints `139 34 73 32` in bytes. To inspect a full target without generating its matrix, call `private_seed.research_profile(192)` and read `public_bytes`, `private_bytes` and `ciphertext_bytes`. The tests also check noncanonical encodings, all tiny private support choices, real finite-difference arithmetic, decoding across the correction radius, independent known-answer bytes, and the syndrome-to-collision and Fourier identities. Computational checks exercise the algorithms. The hardness premises remain open regardless of the test count.

## Related work

Random-code encryption using sparse vectors and noisy codewords predates this work. The project-specific part here is the specified disjoint-support private decoder, its error bound, the differential representation, and the composed reductions for these distributions. The quadratic feature block can be simulated by the reduction. It supplies no independent security estimate. [Zémor, notes on Alekhnovich's cryptosystems](https://www.math.u-bordeaux.fr/~gzemor/alekhnovich.pdf)

The chosen-ciphertext theorem uses the published explicitly rejecting Fujisaki–Okamoto transform. The two ideal hash functions in that argument are instantiated by separately framed SHAKE256 calls in the reference. The seeded option uses a third domain for matrix expansion. [Hövelmanns and Majenz, PQCrypto 2024](https://doi.org/10.1007/978-3-031-62746-0_11)
