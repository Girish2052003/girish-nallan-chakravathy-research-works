# Three profile targets and exact byte accounting

The three nominal targets in the SG-DIFRA manuscript are 128, 192 and 256 bits. The current control exercises the key agreement and serialization code at three domain capacities. Its public inverse uses a linear number of trit operations on unpacked vectors. The separate costs of byte conversion and Python integer arithmetic are outside that count. Each row below therefore measures the control's actual byte lengths and carries **no security rating**. [Original profile table, §11](../../manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.md)

| Nominal target | Uniform trits $n$ | Public key, bytes | Stored private key, bytes | Ciphertext, bytes | Shared key, bytes | Mean blind guesses for a uniform preimage |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 81 | 17 | 17 | 17 | 32 | $(3^{81}+1)/2$ |
| 192 | 122 | 25 | 25 | 25 | 32 | $(3^{122}+1)/2$ |
| 256 | 162 | 33 | 33 | 33 | 32 | $(3^{162}+1)/2$ |

Each control key or ciphertext contains one dense vector of $n$ trits. The public key stores the translation vector, the private key its componentwise negative, and the ciphertext the image vector. The map fixes the nonlinear term in its definition. Transmitted matrices and additional transmitted vectors each consume zero bytes. The dimensions and suite are agreed out of band. The shared key is local output. These figures exclude transport framing and interpreter memory.

**Why 25 bytes at the middle target?** There are $3^{121}<2^{192}\leq 3^{122}$ possible ternary strings on the two sides of the threshold. All 122-trit vectors must fit, so a 24-byte field, with exactly $2^{192}$ encodings, is too small. A 25-byte field suffices. In general, packing a vector as a base-three integer needs the smallest integer $w$ satisfying $256^w\geq 3^n$. Unused encodings must be rejected. This is optimal fixed-length packing for the entire domain. A restricted input distribution or a different algebraic map would require separate accounting.

**What $2^{191}$ measures.** For a unique, uniform 192-bit preimage, checking each possibility once in a fixed order until identifying it costs $(2^{192}+1)/2=2^{191}+1/2$ checks on average. For the 122-trit domain the corresponding mean is $(3^{122}+1)/2$, approximately $2^{192.365}$. These numbers describe a single blind enumeration procedure. The control's public inversion formula is much faster at every size. The original manuscript separately reports $2^{191.72}$ for one clean-basis method on the *archived 128-target profile*. Neither computation establishes a lower bound on an optimal adversary.

Classical trials, quantum circuit resources and a classical or quantum adversary's advantage in an IND-CCA experiment measure different things. NIST uses reference attack costs, including AES key search, for comparisons across classical and quantum cost models. No such rating or concrete work factor has been established for a new SG-DIFRA trapdoor. [NIST post-quantum cryptography FAQ](https://csrc.nist.gov/projects/post-quantum-cryptography/faqs)

## Historical dense design

| Archived profile | Public label matrix alone, bytes | Ciphertext vector payload, bytes |
|---|---:|---:|
| SGD-R1 | 22,118,400 | 77,414,400 |
| SGD-R2 | 149,299,200 | 487,710,720 |
| SGD-R3 | 796,262,400 | 2,786,918,400 |

The repository's historical audit counts $10qN$ public label bits and $10q\ell\cdot 7$ ciphertext bits for $q$ rows over the 1,024-element field. It does not give the complete private key serialization. The small test controls use a different, publicly invertible map. A secure replacement could require additional stored trapdoor information, public coefficients or ciphertext material. Its key and ciphertext sizes are undetermined. [Archived size audit](../SECURITY_REDESIGN_AND_PROOF_LEDGER.md)

Run the exact integer arithmetic and its tests from this directory.

```sh
python3 profile_sizes.py
python3 -m unittest -v test_profile_sizes
```
