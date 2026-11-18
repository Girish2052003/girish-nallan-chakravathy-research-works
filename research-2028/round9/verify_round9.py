"""Reproduce finite Round-9 evidence; optionally rerun the 15 existing programs.

Usage (from repository root):
  python3 research-2028/round9/verify_round9.py --legacy --output-dir /tmp/round9
Output times are execution metadata, not cryptanalytic benchmarks.
"""
import argparse
import concurrent.futures
import hashlib
import io
import json
import platform
from pathlib import Path
import subprocess
import sys
import time
import unittest
from datetime import datetime, timezone

import test_differential_challenges as checks


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEGACY = (
    "formal-verification-and-mathematical-proofs/test_sg_difra.py",
    "formal-verification-and-mathematical-proofs/profile_bounds.py",
    "research-2028/profile_cost_audit.py",
    "research-2028/toy_hidden_mds_attack.py",
    "research-2028/math/multidirection_cocycle.py",
    "research-2028/attacks/public_ideal_membership_break.py",
    "research-2028/attacks/ternary_affine_line_leakage.py",
    "research-2028/attacks/fixed_field_mds_hbce_ppt_break.py",
    "research-2028/attacks/ternary_parallel_line_collision.py",
    "research-2028/attacks/public_decapsulation_recovery.py",
    "research-2028/attacks/public_second_difference_subspace_recovery.py",
    "research-2028/attacks/public_first_difference_local_inversion.py",
    "research-2028/attacks/public_global_treewidth_witness_recovery.py",
    "research-2028/attacks/test_public_oracle_local_inversion.py",
    "research-2028/attacks/test_public_global_shift_witness_recovery.py",
)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def source_hashes():
    paths = set(ROOT.glob("research-2028/**/*.py"))
    paths.update(ROOT.glob("formal-verification-and-mathematical-proofs/*.py"))
    paths.update((HERE / "CHALLENGE_COUPLED_DIFFERENTIAL_SOLVABILITY.md",
                  HERE / "RELATED_WORK_AND_CLAIM_BOUNDARIES.md",
                  ROOT / ".github/workflows/build-research.yml"))
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(paths)}


def run_legacy(index_path, destination):
    index, path = index_path
    started = time.perf_counter()
    try:
        proc = subprocess.run([sys.executable, path], cwd=ROOT, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              timeout=120, check=False)
        status, output = proc.returncode, proc.stdout
    except subprocess.TimeoutExpired as exc:
        status = 124
        partial = exc.stdout or ""
        if isinstance(partial, bytes):
            partial = partial.decode("utf-8", errors="replace")
        output = partial + "\nTIMEOUT after 120 seconds\n"
    name = f"legacy-{index:02d}-{Path(path).stem}.log"
    (destination / name).write_text(output, encoding="utf-8")
    return {"program": path, "returncode": status, "log": name,
            "elapsed_seconds": round(time.perf_counter() - started, 6)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legacy", action="store_true",
                        help="Also rerun all 15 prescribed pre-Round-9 programs")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    destination = args.output_dir.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    before = source_hashes()
    started = utc_now()
    stream = io.StringIO()
    checks.COUNTS.clear()
    suite = unittest.defaultTestLoader.loadTestsFromModule(checks)
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    (destination / "round9-tests.log").write_text(stream.getvalue(), encoding="utf-8")
    legacy = []
    if args.legacy:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(run_legacy, pair, destination)
                       for pair in enumerate(LEGACY, start=1)]
            legacy = [future.result() for future in futures]
    after = source_hashes()
    stable = before == after
    passed = result.wasSuccessful() and stable and all(x["returncode"] == 0 for x in legacy)
    git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False)
    evidence = {
        "research_round": 9,
        "scope": "Finite arithmetic and reduction tests; not proof-assistant verification, "
                 "average-case hardness, quantum hardness, or a KEM security certificate.",
        "started_utc": started, "finished_utc": utc_now(),
        "python_version": platform.python_version(),
        "base_checkout_commit": git.stdout.strip() if git.returncode == 0 else None,
        "source_hashes_stable_during_run": stable,
        "source_sha256": before,
        "round9_tests": {"run": result.testsRun, "failures": len(result.failures),
                         "errors": len(result.errors), "skipped": len(result.skipped),
                         "finite_case_counts": dict(sorted(checks.COUNTS.items())),
                         "log": "round9-tests.log"},
        "legacy_programs": legacy,
        "passed": passed,
        "timing_note": "Legacy programs may run concurrently; times are not security estimates.",
    }
    (destination / "results.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": passed, "round9_tests": evidence["round9_tests"],
                      "legacy_passed": sum(p["returncode"] == 0 for p in legacy),
                      "legacy_run": len(legacy), "sources_stable": stable,
                      "evidence_directory": str(destination)}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
