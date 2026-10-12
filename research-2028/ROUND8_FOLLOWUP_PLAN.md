# Round 8 follow-up implementation plan

> Execution: continue the author-authorized audit and repairs without another approval gate. Use the existing NCSG-only direction; publish on main only.

**Goal:** resolve concrete defects in the current evidence, test proposed escape routes from the known attacks, and update the existing manuscript and generated documents. A secure new KEM is the requested research goal, not an assumed outcome of this plan.

**Baseline:** main at `3ae8afc68f561a52d83ef597ef0b1830b702993e`. All 13 existing verification programs reproduced successfully before edits.

**Design:** maintain distinct models for local public evaluation, explicit global factors, and the archived MDS KEM. Preserve earlier valid proofs. Add attacks only with a complete mathematical argument, public-only interfaces, and independently checked fixtures. Do not substitute an existing KEM or assert an unproved hardness assumption as a solution.

**Review focus:** a failed attack is inconclusive; finding any witness does not automatically recover a KEM key; input representation costs must be charged; high primal width is not a lower bound; randomized public evaluation is not a quantum random oracle model; an algebraic proof plus Python tests is not machine-checked KEM security.

## Tasks

- [x] Inspect the exact repository, original text, current claims, and build workflow; reproduce baseline regressions.
- [x] Prove and test a public-evaluation-only local inversion extension, including its failure/query bounds and final output validation.
- [x] Prove and test a global constant-shift criterion, including a high-primal-width easy family and an inconclusive case.
- [x] Correct primal/incidence-width wording, unsupported certificate wording, residual-factor size wording, and the contradictory ideal-span repair paragraph.
- [x] Add a precise security target and information-flow obligation, without certifying any profile or introducing a placeholder KEM.
- [x] Integrate scripts into CI, retain reproducible outputs, and guard both manuscripts and mathematical build inputs against stale publication.
- [x] Update README and current ledgers; rebuild the existing Word/PDF documents and inspect rendered pages.
- [x] Independently review changed proofs and code; run all 15 verification programs and both publication gates; prepare the verified update for main.

## Decisions

- The fresh checkout is isolated from any user's working files; no extra remote branch is needed.
- The request authorizes repairs, document updates and pushing them. It does not justify a false success claim if the required novel cryptographic construction cannot be established.
- New negative results eliminate proposed repairs; they are not repairs to KEM confidentiality. The final report must state that distinction.

## Publication and continuation

Publish this reviewed source and both rebuilt document pairs on main with a non-force update checked against the observed parent. Check the resulting remote tree and workflow before reporting publication success. Git history and the associated Actions run are the authoritative publication record.

The author authorized a further automatic design-and-attack pass after this update. That pass must start from current main, preserve existing valid results, and seek a concrete private recovery advantage outside the models already ruled out. An unsuccessful attack is not a hardness proof; no replacement KEM or three security levels may be announced without the required construction and security argument.

On 12 October the author extended this authorization to recurring research passes. Each pass must resume the recorded state, pursue a specific construction or obstruction, preserve reproducible evidence, and publish authorized updates on main. Scheduling status must be verified separately; this instruction alone does not mean a background task exists. Failed attacks, larger parameters, or additional iterations cannot serve as a stopping rule certifying unbreakability. A security conclusion requires the complete construction and explicit, justified security arguments, with assumptions and unresolved limits stated accurately.
