"""Regression tests for tools/test_brain_index_adversarial.sh harness behavior.

The adversarial harness must FAIL LOUDLY (exit 3, named FATAL) when it cannot
create a scratch clone, instead of letting later steps run against a missing
directory and producing misleading per-case FAILs that blame the generator.
(2026-10-01: /tmp exhaustion once made the harness report 3/5 with case FAILs
that blamed the generator for a dead clone.)

These tests run the harness script with a sabotaged source so the very first
scratch clone fails, then assert the harness aborts with the loud FATAL path.
"""

import pathlib
import shutil
import subprocess
import tempfile

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
HARNESS = REPO_ROOT / "tools" / "test_brain_index_adversarial.sh"


def _run_harness_copy_with_broken_repo(tmp_path):
    """Copy the harness outside any git repo (so its REPO=parent dir is not a
    repo) and run it. The first scratch clone must fail loudly."""
    dest = tmp_path / "test_brain_index_adversarial.sh"
    shutil.copy(HARNESS, dest)
    return subprocess.run(
        ["bash", str(dest)],
        capture_output=True,
        text=True,
        timeout=120,
    )


def test_adversarial_harness_fails_loudly_on_broken_clone():
    assert HARNESS.is_file(), f"harness script missing: {HARNESS}"
    with tempfile.TemporaryDirectory(prefix="adv-harness-") as td:
        proc = _run_harness_copy_with_broken_repo(pathlib.Path(td))
    out = proc.stdout + proc.stderr
    assert proc.returncode == 3, (
        f"expected exit 3 (harness/environment failure), got {proc.returncode}\n{out}"
    )
    assert "FATAL" in out, f"expected a named FATAL line in output:\n{out}"
    assert "scratch clone" in out, f"expected 'scratch clone' in FATAL message:\n{out}"
    assert "ENVIRONMENT failure" in out, (
        f"expected the FATAL path to label this an ENVIRONMENT failure, not a generator verdict:\n{out}"
    )
    # Fail-fast: no per-case PASS/FAIL lines may be emitted before the abort.
    assert "FAIL:" not in out.split("FATAL")[0], (
        f"misleading case FAILs were emitted before the FATAL abort:\n{out}"
    )
    assert "PASS:" not in out, f"unexpected case PASS lines from a broken harness run:\n{out}"


def test_adversarial_harness_full_run_still_passes_on_clean_tree():
    """The real harness, unmodified source, must still exit 0 with 6/6 PASS
    after the hardening change (guard against the fix breaking the normal path)."""
    proc = subprocess.run(
        ["bash", str(HARNESS)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, f"harness full run failed:\n{out}"
    assert "6 passed, 0 failed" in out, f"expected 6/6 PASS signal:\n{out}"
