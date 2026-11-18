# Round 13 · Can the private shortcut survive publication?

We built two candidate KEMs over the ternary field and analyzed the public information in each. One result strengthens the earlier security reduction. For a specified distribution of affine-masked power permutations, an inverter that succeeds on fresh keys and ciphertexts can be used on **every promised key and ciphertext in the family**. The concrete cubic permutations nevertheless have a public inverse. A second construction uses a shared finite difference and fails a different test. A quantum observer can predict its shared value even when the public functions have short circuit descriptions of unrestricted degree.

The [constructive KEM criterion](CONSTRUCTIVE_KEM_CRITERION.md) gives a sufficient condition for a future native key generator to inherit both IND-CPA and IND-CCA, including the quantitative post-quantum bound.

## The reduction requested for the KEM

Let $F=T\circ (x\mapsto x^e)\circ S$ on a field of $N=3^n$ elements. The exponent is public and coprime to $N-1$. The two affine masks are independent and uniform before taking the equivalent compact representation. The receiver uses their inverses and a private change of coordinates to recover the sender's exact input. The sender hashes that input using the [Round 11 KEM](../round11/TRANSFORM.md).

**The reduction.** If an inverter succeeds with probability $p$ on a fresh public key and uniformly random ciphertext point, at most two invocations suffice to invert *each* promised key and target with probability at least $\max(0,(Np-1)/(N-1))$. The proof accounts separately for the image of the hidden origin. For instance, average success of one half gives success of at least $(N-2)/(2(N-1))$ even on a target chosen in advance. In the classical random-oracle model, a KEM distinguisher of raw gap $\Delta$ supplies an inverter with $p\ge\Delta$. In the quantum random-oracle model, the one-stage bound is $p\ge\Delta^2/(4q_H^2)$ for $q_H\ge1$ hash queries, classical decapsulation and the independent auxiliary ideal oracle specified in Round 11. These include IND-CPA as the case with zero decapsulation queries. [Orbit reduction](ORBIT_REDUCTION.md)

Through the [Round 12 public circuit compiler](../round12/GENERATED_DIFFERENTIAL_REDUCTION.md), the recovered input gives a unique collision witness for the original generated cubic instance. The promise matters. Every input to the theorem must be a disguise of the fixed power map at the specified dimension. The theorem supplies no reduction from arbitrary cubic potentials or from Round 10's NEXP-complete strategy problem. Nor does it prove that inversion within the promise is hard.

## What happens when actual keys are generated

| Candidate | Honest recovery | Consequence of publication |
| --- | --- | --- |
| Affine-masked field power $x^{1+3^i+3^j}$ with three distinct powers | Undo the output mask, apply the inverse exponent, then undo the input mask. This recovers the exact sender input on every generated key. | The third finite difference determines a field of public linear operators that suffices to invert every ciphertext in polynomial time. This holds for every placement of the three powers for which the exponent gives a permutation. [Cubic theorem and prior work](HIDDEN_CUBIC_MONOMIAL.md) |
| Commuting differences | The sender and receiver both obtain $P(a+b)-P(a)-P(b)+P(0)$ for their two private shifts, then derive the same key. | With explicit coefficients the shared value is publicly computable on every honest ciphertext. With publicly evaluable circuits and a fresh independent uniform sender shift, a quantum observer can predict it with probability at least $15/16$ in the stated model. [Proof and worked example](COMMUTING_DIFFERENCES.md) · [Equivalent secret shifts](TRANSLATION_CLASSES.md) |
| Round 12 field differential with growing exponent | The receiver can invert the differential by undoing its masks and using a Dickson polynomial. | Even letting the exponent grow, a full dense coefficient key admits deterministic public inversion on every ciphertext in time polynomial in its actual encoded length. [Varying-exponent theorem](GROWING_CM.md) |

The first two rows have working KeyGen, Encaps and Decaps implementations. For the concrete public encodings each gives a passive real-versus-uniform distinguishing gap of $1-2^{-256}$. This already rules out IND-CPA and IND-CCA. These mathematical results do not measure the wall-clock cost of one full-sized public inversion. For the third row we exercised small instances and calculated the large layouts. The conclusions concern the stated families.

## Compact bytes and the three targets

The compact power-map public format stores the unique center pair and only the degree-one and degree-three terms of its centered map. The private format takes advantage of a scalar symmetry to omit a whole matrix column. The ciphertext encodes one ternary point, and the shared key occupies 32 bytes. These are actual format widths. No optimality among all encodings is asserted. [Private encoding](ORBIT_ENCODING.md) · [Public encoding](COMPACT_PUBLIC.md) · [Compact public evaluation](compact_orbit.py)

| Minimum domain size | Dimension | Dense public key | Compact public key | Compact private key | Ciphertext |
| --- | ---: | ---: | ---: | ---: | ---: |
| $2^{128}$ | 82 | 1,603,272 B | 1,548,004 B | 2,681 B | 17 B |
| $2^{192}$ | 122 | 7,677,285 B | 7,495,956 B | 5,922 B | 25 B |
| $2^{256}$ | 163 | 24,171,671 B | 23,740,067 B | 10,561 B | 33 B |

A separate calculation addresses a different meaning of “$2^{191}$ work.” Suppose the unit is **one serial quantum phase query** marking the one correct preimage, and the goal is to delay generic search reaching a **one-half** success probability. In that model a point requires at least 243 trits, or **49 bytes**, to clear the $2^{191}$ threshold. Checking the proposed 128, 192 and 256 exponents gives the following exact minimum widths.

| Serial phase-query target | Minimum trits | Point bytes | Compact public/private bytes at an implemented dimension |
| --- | ---: | ---: | ---: |
| $2^{128}$ | 164 | 33 | 24,325,325 / 10,690 |
| $2^{192}$ | 244 | 49 | 118,483,795 / 23,639 |
| $2^{256}$ | 325 | 65 | 371,800,509 / 41,918 |

The public and private byte counts in the last column describe the failed cubic candidate at those dimensions. The generic thresholds assume uniform permutation inputs and a single target. They are necessary filters under this particular cost model. They do not include the cost of implementing each call, guarantee that generic search is optimal for a structured key, or establish NIST security categories. The [parameter proof](PROFILE_BOUNDS.md) also quantifies the additional loss of the current quantum reduction and gives exact integer certificates for the table.

## What the literature supplies

The hidden-monomial analysis builds on Fouque, Macario-Rat and Stern's work. The commuting-difference result uses ideas from fixed-prime quantum hidden translation and states the prediction guarantee for this specific exchange. The cited earlier methods and the absence of external peer review matter for any originality claim. [Hidden monomials, EUROCRYPT 2008](https://crypto.orange-labs.fr/papers/eurocrypt2008-19.pdf) · [Friedl et al. on hidden translation](https://arxiv.org/abs/quant-ph/0211091)

Hair and Sahai's November 2026 revision gives conditional public-key encryption using expanding codes and assumptions about planted hypergraphs and noisy predicates. Their binary noisy-code construction distinguishes two ciphertext distributions using secret positions. A ciphertext can occur under either message bit. Their proof therefore supplies neither the exact permutation inverse for this KEM nor concrete SG-DIFRA parameter estimates. [Hair and Sahai, sections 3.2–3.3](https://arxiv.org/html/2604.10479v2)

## Reproduce

From the repository root, with Python 3.10 or later, run

```sh
python3 -m unittest discover -s research-2028/round13 -p 'test_*.py' -v
python3 research-2028/round13/profile_budgets.py
```

All 25 Round 13 test methods passed locally, along with the 87 earlier test methods in Rounds 9–12. Exact counting checks include all 186,624 affine-mask pairs in a nine-element field example, and Fourier identities for all 512 binary-valued maps on the nine-element domain. [Orbit-law checks](test_orbit_law.py) · [Fourier checks](test_fourier_identities.py)

The finite tests also exercise private inversion, shared-key agreement, canonical encodings, per-challenge witnesses, and the probability identities used in the proofs. Full affine-mask operations are exercised at small field sizes. At the six large field dimensions the tests verify field moduli, central power inverses and wire-size arithmetic. Large public keys were not materialized and no quantum hardware experiment was run. The packet supplies a conditional reduction and reproducible exclusions of candidates. An instantiated native post-quantum KEM with defensible concrete strength remains open.
