# Verification record

The local run on 18 November 2026 used CPython 3.12.14 and passed all 16 Round 11 test methods with zero failures, errors or skips. The unchanged Round 10 suite also passed all 22 methods. Reproduce both runs from the repository root.

```sh
python3 -m unittest discover -s research-2028/round11 -p 'test_*.py' -v
python3 -m unittest discover -s research-2028/round10 -p 'test_*.py' -v
```

| Subject | Evidence |
| --- | --- |
| End-to-end KEM control | With three trits, all 27 public translations and all 27 encapsulation preimages gave 729 successful sender/receiver sessions. Testing each at the three possible clock values gave 2,187 independently evaluated differences of the literal polynomial. The image contained all 27 values for each key. |
| Actual Round 10 policy | The tests compile three planted fixtures using the unmodified Round 10 graph compiler. There are 486 comparisons of the actual outputs at the base and shifted points. The cases include nonbinary addresses and invalid circuit traces. A deliberately wrong color pair fails a real edge constraint. |
| Exact agreement probability | For vertex counts one, two and three, enumeration covered every assignment of colors and edge coins. The 237 configurations, aggregated separately by vertex count, verify equal posterior weights for all three labels in 29 graph/vertex cases. |
| Serialization and wire behavior | The small-domain codec checks every vector through dimension six, including leading zero trits. For the three-trit control every possible one-byte ciphertext is checked for correct canonical acceptance or rejection. Tests exercise length, unused ranks, typed keys, suite and dimension binding, malformed inputs, and a known-answer vector. |
| Profile accounting | Integer arithmetic checks both sides of each trit and byte threshold. An additional randomized smoke run used 100 fresh keys and encapsulations at each profile. Every pair of shared keys matched, and the observed lengths matched the published table. |
| Fixed-challenge bound | Direct checks cover the two reduced ternary cubic monomial types and all possible small shifts used in the fixtures. The special clock term is checked separately at every three-trit point and for all three target values. |

## Deterministic wire example

Use the built-in public shear at dimension three. In this example the KeyGen uniform rank is 21 and the encapsulation uniform rank is 16, both written in decimal. The following values are in hexadecimal.

| Field | Value |
| --- | --- |
| Public key | `15` |
| Stored private key | `0f` |
| Ciphertext | `00` |
| 32-byte shared key | `f1e92c2a0982b717244afda29ab9b571239c738ab9bb9f1cb1a5b37faea733f1` |

The fixture belongs to the publicly invertible control. The finite checks verify arithmetic, agreement and serialization. The conditional security statements use proofs in stated ideal-oracle models. No test establishes the assumed one-way trapdoor or concrete post-quantum security. This work received separate AI-assisted mathematical review; external cryptographic review remains open.

[Algorithms](README.md) · [Security reduction](TRANSFORM.md) · [Feasibility](FEASIBILITY.md) · [Planted policy](PLANTED_POLICY.md)
