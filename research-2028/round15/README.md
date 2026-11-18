# Round 15 · Working KEMs and the source of their security

The code-based profile combines Classic McEliece with a ternary SG-DIFRA encapsulation. It implements key generation, encapsulation and decapsulation at three full parameter sets. At the middle setting the sender receives a **524,692-byte public key**, sends a **351-byte ciphertext**, and establishes a **32-byte shared secret**. The receiver stores **13,704 bytes**. This profile uses no lattice algorithm and no HQC component.

Its security argument has a precise premise. If Classic McEliece is IND-CCA secure and the hash used to combine the two secrets satisfies the stated quantum random-oracle bound, then the combined KEM is IND-CCA secure for one honest recipient with adaptive classical decapsulation queries. IND-CPA follows by making zero such queries. This result holds even if the smaller ternary component supplies no secrecy by itself. The implementation and parameters of the new composite are research material. FIPS 203 standardizes the separate ML-KEM ingredient in the optional lattice-backed profiles.

## Run the middle profile

On a Debian or Ubuntu Linux system, install the distribution's `libmceliece1` package. The code-based operations use the system library and Python 3. The example generates actual keys, runs both parties and prints only sizes and their agreement result.

```sh
cd research-2028/round15
python3 exchange.py code-hybrid 192
```

Use the same KEM directly in Python:

```python
from classic_kem import code_based_hybrid

kem = code_based_hybrid(192)
public, private = kem.keygen()
ciphertext, sender_key = kem.encaps(public)
receiver_key = kem.decaps(private, ciphertext)
assert receiver_key == sender_key
```

The caller agrees on the suite out of band and authenticates the recipient's public key. Encapsulation returns a ciphertext followed by the shared key. Decapsulation returns the shared key on an honest input. The reference reports explicit component or framing failures as `None` and preserves an implicitly rejecting component's returned key within the combiner.

## Choosing a security foundation

| Middle profile | Public bytes | Private bytes | Ciphertext bytes | Foundation of the secrecy claim |
|---|---:|---:|---:|---|
| Classic McEliece-460896 + SG-DIFRA | 524,692 | 13,704 | 351 | Studied binary Goppa-code KEM plus the hash combiner |
| ML-KEM-768 + SG-DIFRA | 1,716 | 128 | 1,283 | Standardized module-lattice KEM plus the hash combiner |
| Standard ML-KEM-768 alone | 1,184 | 64 | 1,088 | Unmodified FIPS 203 component through the provider |
| Shortened native SG-DIFRA, 192 target | 15,022,416,160 | 96 | 5,482,436 | The two original Round 14 ternary decoding distributions |

The first three rows ran at full size. The last row gives exact wire calculations; complete native exchanges ran at smaller dimensions. Every row returns 32 shared bytes. The ML-KEM private widths use the provider's regenerable 64-byte seed and include the native private part when appropriate. The [code-based table](CLASSIC.md), [ML-KEM hybrid table](COMBINER.md) and [native table](SIZES.md) give all three parameter choices. These design labels and NIST's security categories do not certify a quantum cost of $2^{191}$ elementary operations.

## Why the two-component key is protected

The sender and receiver independently derive a Classic McEliece secret and a ternary SG-DIFRA secret. They hash both secrets together with both ciphertexts, the public-key context and the suite. If someone changes the second ciphertext while retaining the first, the resulting pair has a different hash input. This binding is part of the proof for an adversary that may request decapsulation of *other* ciphertexts. The [theorem and resource bounds](COMBINER.md) give the exact argument and model. Correctness is perfect in the mathematical Classic McEliece + SG-DIFRA profile. The ML-KEM-based profile inherits ML-KEM's small honest disagreement probability.

There is also a mathematical connection to SG-DIFRA inside the established code-based foundation. Each underlying binary decoding witness corresponds to exactly one collision witness for a generated cubic ternary differential system. The proof enforces binary inputs, computes binary parity inside the ternary field, and counts errors as ordinary integers. It gives a representation of the established decoding problem in SG-DIFRA. The source of hardness remains Goppa decoding. [Bijection, assumptions and concrete wire check](BINARY_BRIDGE.md)

## What improved for standalone SG-DIFRA

A concatenated Golay–Reed–Solomon code needs 5,256 check coordinates in the 192 layout, down from 18,760, and still corrects every pattern of up to 1,152 trit errors. A projection reuses the original decoding challenges while removing redundant transmitted coordinates. Together these changes cut the 192-target public key by 71.98% and the ciphertext by 36.01%. A proved size floor shows that changing only the outer code within this particular layout cannot shrink the public key below 10.78 GB. [Decoder and proof](OUTER.md) · [Secrecy-preserving projection](NATIVE_PROOF.md) · [Size limits and smaller experiment](SIZES.md)

We also derived explicit bounds on observers who read only part of a generated ternary instance. For example, with the complete matrix available, 547 quantum coordinate queries to the 192-target syndrome give raw distinguishing advantage at most $2^{-280}$. An adversary in the actual security game receives the complete input. Its decoding work factor remains open. [Models, proof and checked bounds](HARDNESS.md)

## Verification

With both `libmceliece1` and Node v24.22.3 available, the following commands run the two other workflows and the complete Round 15 suite:

```sh
python3 exchange.py ml-hybrid 192
python3 exchange.py ml-kem 192
python3 -m unittest discover -s . -p 'test_*.py' -v
```

The tests cover all six full-size composite configurations, external ML-KEM known-answer vectors, independent binary syndrome and shared-key computations, transcript binding, malformed inputs, actual native exchanges, the full outer decoder at each target radius, exact size arithmetic, and restricted-observation bounds. The native Python code and the composite protocol have no independent implementation assurance or side-channel certification. [ML-KEM provider and test-vector provenance](PRACTICAL.md) · [Code-based provider and applicability](CLASSIC.md)
