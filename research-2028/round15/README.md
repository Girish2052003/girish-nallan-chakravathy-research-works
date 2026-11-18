# Round 15 · Standalone SG-DIFRA and comparison experiments

The standalone construction uses its own ternary key generator, differential encryption rule and sparse private decoder. It needs no other KEM. Under two generated ternary decoding assumptions it has single-recipient IND-CPA and IND-CCA proofs in the stated quantum random-oracle model. The hardness of finding the hidden checks or distinguishing the noisy payloads at the actual dimensions remains unverified. The earlier worst-case theorems alone cannot settle that average-case question. [Native construction and reductions](NATIVE_PROOF.md)

## Run a standalone exchange

From the repository root, run this small engineering configuration with Python 3. It requires neither libmceliece nor Node. Its parameters test correctness and wire size; they carry no bit-security rating.

```sh
cd research-2028/round15
python3 - <<'PYTHON'
from projected_sizes import engineering_example

kem = engineering_example()
public, private = kem.keygen()
ciphertext, sender_key = kem.encaps(public)
assert kem.decaps(private, ciphertext) == sender_key
print(len(public), len(private), len(ciphertext), len(sender_key))
PYTHON
```

The four lengths are 62,573, 64, 1,273 and 32 bytes. [Source and profile limits](SIZES.md)

## Status of the hybrid comparisons, 18 November 2026

The Classic McEliece and ML-KEM integrations illustrate what a two-component construction can inherit from an external component. Neither experiment establishes the independent hardness of SG-DIFRA. After structural cryptanalysis weakened confidence in Classic McEliece's claimed margins, the German BSI advised against its use in new developments. The McEliece combination is retained for research comparison. [BSI advisory and assessment of the evidence](CLASSIC.md)

## Choosing a security foundation

| Middle profile | Public bytes | Private bytes | Ciphertext bytes | Foundation of the secrecy claim |
|---|---:|---:|---:|---|
| Classic McEliece-460896 + SG-DIFRA | 524,692 | 13,704 | 351 | Classic McEliece assumption under reassessment, plus the hash combiner |
| ML-KEM-768 + SG-DIFRA | 1,716 | 128 | 1,283 | Standardized module-lattice KEM plus the hash combiner |
| Standard ML-KEM-768 alone | 1,184 | 64 | 1,088 | Unmodified FIPS 203 component through the provider |
| Shortened native SG-DIFRA, 192 target | 15,022,416,160 | 96 | 5,482,436 | The two original Round 14 ternary decoding distributions |

The first three rows ran at full size. The last row gives exact wire calculations; complete native exchanges ran at smaller dimensions. Every row returns 32 shared bytes. The ML-KEM private widths use the provider's regenerable 64-byte seed and include the native private part when appropriate. The [code-based table](CLASSIC.md), [ML-KEM hybrid table](COMBINER.md) and [native table](SIZES.md) give all three parameter choices. These design labels and NIST's security categories do not certify a quantum cost of $2^{191}$ elementary operations.

## What the two-component proof assumes

The sender and receiver independently derive a Classic McEliece secret and a ternary SG-DIFRA secret. They hash both secrets together with both ciphertexts, the public-key context and the suite. If someone changes the second ciphertext while retaining the first, the resulting pair has a different hash input. This binding is part of the proof for an adversary that may request decapsulation of *other* ciphertexts. The [theorem and resource bounds](COMBINER.md) give the exact argument and model. Correctness is perfect in the mathematical Classic McEliece + SG-DIFRA profile. The ML-KEM-based profile inherits ML-KEM's small honest disagreement probability.

There is also a mathematical connection to SG-DIFRA in the Classic McEliece comparison. Each underlying binary decoding witness corresponds to exactly one collision witness for a generated cubic ternary differential system. The proof enforces binary inputs, computes binary parity inside the ternary field, and counts errors as ordinary integers. It gives a representation of the established decoding problem in SG-DIFRA. The source of hardness remains Goppa decoding. [Bijection, assumptions and concrete wire check](BINARY_BRIDGE.md)

## What improved for standalone SG-DIFRA

A concatenated Golay–Reed–Solomon code needs 5,256 check coordinates in the 192 layout, down from 18,760, and still corrects every pattern of up to 1,152 trit errors. A projection reuses the original decoding challenges while removing redundant transmitted coordinates. Together these changes cut the 192-target public key by 71.98% and the ciphertext by 36.01%. A proved size floor shows that changing only the outer code within this particular layout cannot shrink the public key below 10.78 GB. [Decoder and proof](OUTER.md) · [Secrecy-preserving projection](NATIVE_PROOF.md) · [Size limits and smaller experiment](SIZES.md)

We also derived explicit bounds on observers who read only part of a generated ternary instance. For example, with the complete matrix available, 547 quantum coordinate queries to the 192-target syndrome give raw distinguishing advantage at most $2^{-280}$. An adversary in the actual security game receives the complete input. Its decoding work factor remains open. [Models, proof and checked bounds](HARDNESS.md)

## Verification

With both `libmceliece1` and Node v24.22.3 available, the following commands run the comparison workflows and the complete Round 15 suite:

```sh
python3 exchange.py code-hybrid 192
python3 exchange.py ml-hybrid 192
python3 exchange.py ml-kem 192
python3 -m unittest discover -s . -p 'test_*.py' -v
```

The tests cover all six full-size composite configurations, external ML-KEM known-answer vectors, independent binary syndrome and shared-key computations, transcript binding, malformed inputs, actual native exchanges, the full outer decoder at each target radius, exact size arithmetic, and restricted-observation bounds. The native Python code and the composite protocol have no independent implementation assurance or side-channel certification. [ML-KEM provider and test-vector provenance](PRACTICAL.md) · [Code-based provider and applicability](CLASSIC.md)
