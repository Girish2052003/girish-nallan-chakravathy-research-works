# NCSG KEM research continuation

Updated 12 October 2026 after the Round-8 follow-up publication checks.

**The secure replacement KEM remains unconstructed and unproved.** The current work establishes attacks and precise obstructions, not exponential hardness or certified 128/192/256-bit profiles. Preserve that distinction in every continuation.

## Completed work to reuse

- Mathematical follow-up: commit `40703b21e1e4f7f47dea56e8f6b8a2252951c8e1`; see [results](ROUND8_FOLLOWUP_RESULTS.md) and [recorded evidence](evidence/round8-followup/README.md).
- Public-evaluation inversion (Theorem 4.8), exact uniform fiber sampling (Corollary 4.8a), and a correctness-to-key-recovery obstruction for the explicitly specified local wrapper (Corollary 4.8b).
- Public compatible global shifts (Theorem 12.10), including a restricted high-width easy family and satisfiable instances on which the method is inconclusive.
- The repaired Round-6 dictionary-order bug, robust tiny-error-budget calculation, corrected scope/complexity claims, and source-aware publication guard.
- All 15 workflow programs passed. Source commit `6784f96458fd5236b95ce0b46d87ce70a9e02c0e` passed [CI run 38244685690](https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/actions/runs/38244685690), producing reviewed binary commit `4b5ae2ae3e96b8a9a03284ee90092cf9170fd33c`. The final PDFs have 45 and 13 pages under the CI renderer. This is artifact and finite-regression verification, not KEM security verification.

## Next concrete scientific question

Identify an efficient **private recovery mechanism**, with exact public KeyGen/Encaps interfaces and a deterministic or precisely randomized Decaps algorithm, outside the source-local models already excluded. Before assigning any hardness assumption, exhibit why the holder of the private information can recover the encapsulated key and why the same public equations do not already provide equivalent recovery.

Start with one explicit candidate or narrowly stated obstruction. Promising questions to investigate, without assuming a positive answer, are:

1. If the nonlinear dimension grows and the local function is generated succinctly, what is the exact sampler and how does secret inversion work? The original uniform potential-table sampler has an exponential generation cost in that regime. A new sampler changes the distribution and needs fresh attacks.
2. If encapsulation restricts its input distribution, is that restriction publicly sampleable, how does decapsulation identify the same key, and does public fiber sampling or a distribution-weighted variant still recover it? Uniform-input Corollary 4.8b must not be asserted outside its hypotheses.
3. If new global coupling is introduced, specify its private decoding advantage. Large primal width, overlap, and failure of the global-shift attack alone establish no hardness. Check the actual sampled public instances and ciphertexts.

Do not repeat the existing 15 programs as the sole contribution of a pass. Record the candidate, exact assumptions, theorem or counterexample, executable evidence, and the next unresolved question. A useful negative result is acceptable; inventing a secure construction or security estimate is not.

## Publication and recurring work

The author explicitly authorized recurring research and direct updates to the existing documents, code, evidence and README on `main`. Fetch current main, preserve unrelated edits, and publish with a non-force update checked against the observed parent. Do not create another official branch. Coordinate with any active pass before writing, and update this checkpoint after substantive work.

The authorized recurrence is not itself proof that an automation is active. Verify scheduling through the task service and report any scheduling/access blocker accurately. Do not create duplicate loops or change unrelated automations.

The current publishing fixes are already complete. Keep native Word equations; use `pdfinfo` for page counts; compare local and remote rendering when they use different LibreOffice versions. The publishing gate rejects fallback glyphs and unintended imaginary-part symbols, and permits whitespace-only line wrapping in the mandatory security-status phrase. Preserve these checks while focusing subsequent work on the scientific construction problem.
