# Round 8 follow-up: reproducible verification record

Audit base: `3ae8afc68f561a52d83ef597ef0b1830b702993e`. Recorded on 11 October 2026.

All **15 verification programs** in the research workflow completed with exit status zero. The [manifest](results.json) records the commands, Python version, UTC execution timestamps, individual logs and SHA-256 hashes of the actual mathematical sources and build inputs. The two new suites contain 9 oracle-inversion tests and 11 global-shift tests. The repaired Round-6 suite contains 5 tests. Other programs include exhaustive finite checks and numerical calculations rather than unit-test counts.

These outputs validate the recorded finite examples and implementation regressions. They are **not** proof-assistant verification, a security certificate, a lower bound against all attacks, or evidence that a replacement KEM has been achieved. Fixed seeds reproduce experiments; the probability theorems separately assume independent uniform sampling. Elapsed times were measured with up to three independent programs running concurrently and are not benchmarks.

## Reproduce the mathematical programs

From the repository root, inspect `results.json`, then run its recorded Python commands. This standard-library replay also checks that the audited source files match their recorded bytes:

```sh
python3 - <<'PY'
import hashlib, json, subprocess, sys
from pathlib import Path
record = json.loads(Path('research-2028/evidence/round8-followup/results.json').read_text())
for name, expected in record['source_sha256'].items():
    actual = hashlib.sha256(Path(name).read_bytes()).hexdigest()
    assert actual == expected, f'Source changed since this audit: {name}'
for case in record['programs']:
    subprocess.run([sys.executable, *case['argv'][1:]], check=True)
PY
```

Every raw log is retained in this directory. Outputs are finite evidence for the statements in [the follow-up results](../../ROUND8_FOLLOWUP_RESULTS.md) and the corresponding manuscript proofs. All 13 prior programs also passed before the follow-up edits. The reordered-table test first failed against the old Round-6 loop; the `eta=1e-320` test first exposed an overflow in the new oracle budget, then passed after stable logarithms and exact rational tail checks were added.

## Document verification

Both existing manuscripts were rebuilt from Markdown to editable Word with Pandoc, then rendered to PDF. The active paper has 40 pages and 992 OfficeMath nodes; the short archive has 11 pages and 186 OfficeMath nodes. The publication logs record checks for converted formulas, critical theorem text, preserved field/noise formulas, and broken-glyph fallback. Rendered pages were also inspected visually; crowded tables, a clipped numerical exponent, and malformed delimiters were repaired before publication.

The workflow rebuilds both documents and repeats the publication gates. Its generated files may have different binary hashes because the CI toolchain and timestamps differ. Scientific inputs must remain identical to the audited source hashes; a binary rebuild is not an additional cryptographic result.

## Review scope

Separate agent reviews challenged the proof conditioning, input-representation costs, attack/public-secret interfaces, negative test cases, and publication concurrency guard. No critical or important mathematical or implementation blocker remained in that review. This is an internal computational review, not external peer review or a proof-assistant certificate. The repository remains a cryptanalytic research draft with no certified replacement KEM or security levels.
