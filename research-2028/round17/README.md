# Standalone SG-DIFRA KEM with systematic public keys

Round 17 gives key generation, encapsulation, decapsulation and a conditional IND-CCA proof for one honest recipient. IND-CPA follows in the same model by setting the number of decapsulation queries to zero. The receiver uses SG-DIFRA's own sparse private checks. The assumption is that observers with the resources used by the proof have small advantage in a specified **average-case ternary syndrome problem**. The quantum theorem also assumes ideal hash functions with quantum access and permits adaptive classical decapsulation queries. The code uses domain-separated SHAKE256. The concrete post-quantum security strength of the three profiles remains open.

## What changed on the wire?

Each public matrix begins with an identity block. This lets the sender drop a set of redundant coordinates from the ciphertext. The receiver can fill those coordinates with zeros because its private checks give the same result for every representative of the same public coset. The implementation expands at most one public matrix row per nonzero error position when forming a ciphertext. Generating a key still takes substantial work. Both linear and quadratic mask terms vanish in the transmitted representative. The earlier cubic SG-DIFRA encoding represents the same sparse decoding witness. The security foundation here is coding theory. [Systematic construction and proof](SYSTEMATIC.md) · [Coset identity](QUOTIENT.md)

| Primary target label | Public key, B | Private key, B | Ciphertext, B | Upper bound on honest failure |
|---:|---:|---:|---:|---:|
| 128 | 2,201,315,732 | 80 | 849,798 | $2^{-399}$ |
| 192 | 7,088,151,760 | 96 | 1,871,132 | $2^{-607}$ |
| 256 | 16,482,794,077 | 112 | 3,297,407 | $2^{-813}$ |

All three shared keys are 32 bytes. These are exact fixed wire sizes for every key, computed from the serialization. The failure bound applies for each generated key and each fixed message over a fresh encryption tape. Applying it to FO encapsulation uses the stated hash model. The 192 public key and ciphertext occupy 43.84% and 61.01% fewer bytes, respectively, than in Round 16. The private key is the same size. A second profile, selected by `full_radius=True`, guarantees recovery for every honest sender tape. Its 192 public key and ciphertext occupy 12,620,284,606 and 2,397,431 bytes. [Decoding-failure proof](outer_proof.md) · [Nonce and spread bounds](SPREAD.md)

## What can be claimed at the 192 target?

The common mathematical experiment draws a uniform matrix with 12,119,412 rows and 18,161,280 columns over $\mathbb F_3$. A distinguishing algorithm must tell a syndrome of a random vector of weight 1,152 from a uniformly random syndrome. A search algorithm must return a vector of that weight giving the supplied syndrome. A quantum KEM distinguisher with sufficient advantage yields a search algorithm for this generated distribution, with the losses in the proof. Loyer gives the same planted search definition for general finite fields. [Original generated-witness reduction](../round16/MATCHED_PROOF.md) · [Loyer, §2.2](https://eprint.iacr.org/2023/1263.pdf)

* **Conditional post-quantum result.** With the separate query counts in the theorem each bounded by $2^{191}$, a raw *decision* gap at most $2^{-224}$ at the simulated resources suffices for KEM guessing success below 50.8%. A gap at most $2^{-280}$ suffices for success below $1/2+2^{-34}$. Neither gap has been established against unrestricted algorithms. The proof charges simulation time and memory in addition to queries. [Quantitative assumptions](SYSTEMATIC.md) · [Exact numerical checks](test_classical.py)
* **Conditional classical result.** When all hash queries are classical, the same two success ceilings follow under substantially weaker decision-gap premises of $2^{-20}$ and $2^{-47}$, respectively. [Classical ROM proof](CLASSICAL.md)
* **Evidence on actual dimensions.** Three published classical *search* models were evaluated. At the middle target the lowest unrestricted estimate was $2^{700.68}$ ternary additions and $2^{95.72}$ field elements of memory. One quantum baseline has a scale of $2^{336.55}$ ideal predicate evaluations. Each evaluation has a resource cost of its own. These calculations cannot establish that every KEM adversary needs $2^{191}$ operations. [Classical cost models and reproduction](EVIDENCE.md) · [Classical and quantum baseline](BASELINE.md)

Two further bounds identify specific limits of the analysis. When one party receives the matrix and another receives the syndrome, even 18,310 bits of interactive classical communication give raw distinguishing gap at most $2^{-280}$. The KEM adversary receives both inputs together. Separately, the original 192 public encryption calculation leaves fewer than 95,000 bytes of savings for a broad class of drop-in compressors under its stated assumption. Round 17 changes the calculation itself. [Communication proof](COMMUNICATION.md) · [Public-key compression bound](EVALUATION.md)

## Run the implementation

From the repository root, use Python 3. The first command generates fresh keys, encapsulates and checks an entire small full-radius exchange. The second prints the three registered sizes without generating their multi-gigabyte keys. The tests also exercise the smaller half-radius wire format and invalid ciphertext handling.

```sh
python3 research-2028/round17/demo.py
python3 research-2028/round17/demo.py --sizes
python3 -m unittest discover -s research-2028/round17 -p 'test_*.py' -v
```

For a larger functional check, `python3 research-2028/round17/demo.py --timings` runs three fresh exchanges with a 512-bit message, four quadratic input variables and weight two. On CPython 3.12.14 the observed median times were 1.5354 s for key generation, 0.0213 s for encapsulation and 0.0194 s for decapsulation. All three pairs agreed. The public key, private key and ciphertext occupied 374,548, 96 and 576 bytes. The small weight makes this a timing fixture. Its resource figures do not describe the registered 192-target distribution.

The [reference implementation](systematic_kem.py) exposes `research_profile(192)`, `keygen()`, `encaps(pk)` and `decaps(sk, ct)`. The private decoder returns `None` on rejection. The Python implementation is variable-time. End-to-end runs used smaller instances. Independent cryptanalysis, concrete quantum resource estimates for this exact distribution and a production implementation remain open.
