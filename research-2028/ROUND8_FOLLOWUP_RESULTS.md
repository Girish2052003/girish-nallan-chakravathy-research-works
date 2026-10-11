# Round 8 follow-up results

Updated 11 October 2026. Audit base: `3ae8afc68f561a52d83ef597ef0b1830b702993e`.

**The requested secure replacement KEM has not been achieved.** This follow-up supplies stronger negative results and repairs defects in the research evidence. It does not certify SGD-R1/R2/R3, establish an exponential attack lower bound, or close IND-CPA/IND-CCA/QROM security.

## Results added to the existing paper

| Result | Exact scope | Consequence |
| --- | --- | --- |
| Theorem 4.8 | Public evaluation of the source local map, with polynomial nonlinear-table size | Polynomial-time randomized inversion without the complete public truth table |
| Corollary 4.8a | A sound recovered section of the constant-increment map | Exact uniform public sampling of every local fiber |
| Corollary 4.8b | Uniform input, ciphertext only `f(x)`, public deterministic key derivation, deterministic decapsulation | Correctness error `delta` gives public session-key recovery at least `1 - 2 delta - eta` |
| Theorem 12.10 | Complete local function tables and compatible global constant shifts | Public recovery for targets in the increment image, independently of primal width |
| Explicit high-width family | Restricted block upper triangular source coordinates and private left blocks | Unbounded primal width coexists with polynomial public witness recovery |

The complete arguments are in the [active manuscript](../manuscript/SG_DIFRA_EUROCRYPT_2028_RESEARCH_DRAFT.md). They were cross-reviewed for mathematical scope and conditioning; this is not a claim of external peer review or proof-assistant verification. Elementary linear algebra and probability are used; novelty relative to the literature has not been established.

## Executable evidence

- [Public evaluation attacker and uniform sampler](attacks/public_oracle_local_inversion.py), with [tests](attacks/test_public_oracle_local_inversion.py).
- [Public global shift attacker](attacks/public_global_shift_witness_recovery.py), with [tests](attacks/test_public_global_shift_witness_recovery.py).
- [Fixed Round-6 attacker and reordered-table regression](attacks/public_second_difference_subspace_recovery.py).
- [Recorded verification outputs and source hashes](evidence/round8-followup/README.md).

Reproduce the new suites with Python 3.10 or later:

```sh
python research-2028/attacks/test_public_oracle_local_inversion.py
python research-2028/attacks/test_public_global_shift_witness_recovery.py
python research-2028/attacks/public_second_difference_subspace_recovery.py
```

The oracle suite inverts all 9/27/81 local targets for two samples of each original local geometry. A `(k,d)=(24,3)` fixture has 282,429,536,481 possible inputs, but needs 11,678 evaluations including twenty target inversions and their independent checks. This is one reproducible experiment, not a claim to have evaluated that entire domain. Exact small-domain enumeration checks uniform fiber sampling. Probability tails are checked with rational arithmetic; deterministic test seeds are distinct from the theorem's independent uniform sampling model.

The global suite checks recovered spaces against 32 exhaustively evaluated small maps. Its fixed-local-size high-width families have primal widths 3/7/11 and full increment ranks 6/28/66. Separate satisfiable source-form examples have no useful global shifts and must return **inconclusive**. Neither an inconclusive attack nor large width is security evidence.

## Defects repaired

1. Round 6 skipped the first public-table dictionary key, assuming it was zero. A reordered legitimate table lost two directions. The regression failed before the loop was fixed and passes afterward.
2. The new oracle budget overflowed for the valid small error budget `eta=1e-320`. Stable logarithms and exact rational tail checks now handle the case.
3. Round 8 mixed primal and incidence graph terminology, overstated an exported unsatisfiability certificate, applied a residual-factor size bound to input factors, and omitted the distinction between an available order and optimal treewidth. These claims now match the actual algorithm.
4. Section 12.6 incorrectly suggested that more relations sharing a witness could make the ideal span full. Evaluation at that witness keeps the span proper; the paragraph is corrected.
5. The publishing workflow checked only one source before publishing both documents. It now checks both sources and the mathematical/build inputs against the original build commit throughout retries.

## What a replacement still needs

The missing item is a construction with an actual private recovery advantage: a public encapsulation algorithm, a precisely defined ciphertext distribution, and a secret decapsulation mechanism that escapes these attacks while preserving correctness. A planted hard problem, inaccessible original coordinates, an added hash, or a larger graph does not itself supply that mechanism.

No active replacement KeyGen/Encaps/Decaps implementation or complete security reduction exists here. No three security levels can be responsibly derived yet. The existing files remain a cryptanalytic research draft. EUROCRYPT 2027's official submission deadline was 17 September 2026 at 23:59 AoE, as verified from the [conference site](https://eurocrypt.iacr.org/2027/); this update is not a submission-ready 2027 paper.
