"""Conformance: TRIAL-EVIDENCE-V1.

Canonical spec: BRAIN/03-KERNEL/SCHEMA/TRIAL-EVIDENCE-V1.json.
Verifier under test: tools/verify_trial_evidence.py.

Origin: Trial-4 (2026-10-07) claimed PASS on summary statistics while its raw
data lived at /tmp/trial4/RESULTS.md on an ephemeral session tmpfs. The reboot
wiped it; Naya 2's independent verification returned INCONCLUSIVE. A verifier
that cannot disagree with that claim shape is not a verifier.

Controls:
  - POSITIVE: descriptor citing real in-repo files -> verifier PASSES.
  - NEGATIVE: /tmp-shaped path (Trial-4's exact shape) -> verifier FAILS.
  - NEGATIVE: nonexistent relative path -> verifier FAILS.
  - NEGATIVE: absolute path outside the repo -> verifier FAILS.
  - NEGATIVE: empty evidence list -> verifier FAILS.
  - COMMITTED mode: untracked worktree file -> FAILS; git-tracked file -> PASSES.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "BRAIN" / "03-KERNEL" / "SCHEMA" / "TRIAL-EVIDENCE-V1.json"
VERIFIER = ROOT / "tools" / "verify_trial_evidence.py"

# A file that is guaranteed tracked at HEAD on any sane checkout of this repo.
TRACKED_FIXTURE = "BRAIN/03-KERNEL/SCHEMA/VERIFY-NODE-SCHEMA.json"


def load_spec() -> dict:
    return json.loads(SPEC.read_text(encoding="utf-8"))


def run_verifier(descriptor: dict, *extra: str) -> subprocess.CompletedProcess:
    desc_path = Path("/tmp") / f"trial_desc_{abs(hash(json.dumps(descriptor, sort_keys=True))) % 10**8}.json"
    desc_path.write_text(json.dumps(descriptor), encoding="utf-8")
    try:
        return subprocess.run(
            [sys.executable, str(VERIFIER), str(desc_path), "--repo", str(ROOT), *extra],
            capture_output=True,
            text=True,
        )
    finally:
        desc_path.unlink(missing_ok=True)


def trial_descriptor(*paths: str) -> dict:
    return {
        "trial_id": "trial-99-conformance",
        "claim": "conformance probe claim",
        "raw_evidence_paths": list(paths),
    }


# ---------------------------------------------------------------------------
# Spec integrity
# ---------------------------------------------------------------------------

def test_spec_is_candidate_with_required_rules():
    spec = load_spec()
    assert spec["status"] == "CANDIDATE"
    assert "/tmp/**" in spec["rules"]["forbidden_locations"]
    assert "durable_location" in spec["rules"]
    desc = spec["rules"]["descriptor"]
    for field in ("trial_id", "claim", "raw_evidence_paths"):
        assert field in desc["required"], f"descriptor must require {field}"


# ---------------------------------------------------------------------------
# Positive control — real in-repo evidence passes
# ---------------------------------------------------------------------------

def test_positive_in_repo_evidence_passes():
    proc = run_verifier(trial_descriptor(TRACKED_FIXTURE, "BRAIN/03-KERNEL/SCHEMA/TRIAL-EVIDENCE-V1.json"))
    assert proc.returncode == 0, f"verifier rejected sound evidence:\n{proc.stderr}"
    assert "OK" in proc.stdout


# ---------------------------------------------------------------------------
# Negative controls — each must fail closed
# ---------------------------------------------------------------------------

def test_negative_ephemeral_tmp_path_fails():
    # Trial-4's exact claim shape: raw data on ephemeral /tmp.
    proc = run_verifier(
        trial_descriptor("/tmp/trial4/RESULTS.md")
    )
    assert proc.returncode == 2, "verifier MUST reject /tmp evidence (Trial-4 class)"
    assert "ephemeral" in proc.stderr.lower()


def test_negative_var_tmp_path_fails():
    proc = run_verifier(trial_descriptor("/var/tmp/trial9/results.json"))
    assert proc.returncode == 2, "verifier MUST reject /var/tmp evidence"


def test_negative_missing_relative_path_fails():
    proc = run_verifier(trial_descriptor("trials/trial-99/DOES-NOT-EXIST.json"))
    assert proc.returncode == 2, "verifier MUST reject unresolvable paths"
    assert "does not resolve" in proc.stderr


def test_negative_absolute_path_outside_repo_fails():
    proc = run_verifier(trial_descriptor("/etc/hostname"))
    assert proc.returncode == 2, "verifier MUST reject absolute paths outside the repo"


def test_negative_empty_evidence_list_fails():
    proc = run_verifier({"trial_id": "t", "claim": "c", "raw_evidence_paths": []})
    assert proc.returncode == 2, "verifier MUST reject an empty evidence list"


def test_negative_malformed_descriptor_fails():
    proc = run_verifier({"trial_id": "t"})
    assert proc.returncode == 2, "verifier MUST reject a descriptor with no evidence list"


# ---------------------------------------------------------------------------
# --committed mode: evidence must be git-tracked
# ---------------------------------------------------------------------------

def test_committed_mode_rejects_untracked_file(tmp_path):
    scratch = tmp_path / "scratch-results.json"
    scratch.write_text("{}", encoding="utf-8")
    # tmp_path is outside the repo -> also exercises the out-of-repo rule.
    proc = run_verifier(
        {"trial_id": "t", "claim": "c", "raw_evidence_paths": [str(scratch)]},
        "--committed",
    )
    assert proc.returncode == 2


def test_committed_mode_accepts_tracked_file():
    proc = run_verifier(trial_descriptor(TRACKED_FIXTURE), "--committed")
    assert proc.returncode == 0, f"tracked in-repo file must pass --committed:\n{proc.stderr}"


# ---------------------------------------------------------------------------
# Adversarial regression: attacks that defeated the verifier before the
# resolve-and-contain fix (TRUTH-AGENT independent review, 2026-10-07).
# A bare string-prefix check cannot see through symlinks or `..` traversals:
# each of these sailed through as "OK" before the fix.
# ---------------------------------------------------------------------------

def _adv_scratch():
    scratch = ROOT / "_adv_evidence_scratch"
    scratch.mkdir(exist_ok=True)
    return scratch


def _cleanup_adv_scratch():
    import shutil

    shutil.rmtree(ROOT / "_adv_evidence_scratch", ignore_errors=True)


def test_adversarial_symlink_to_tmp_fails(tmp_path):
    """An in-repo symlink pointing at /tmp must NOT pass as durable evidence."""
    target = tmp_path / "RESULTS.md"
    target.write_text('{"raw": "ephemeral"}', encoding="utf-8")
    scratch = _adv_scratch()
    link = scratch / "via-link.md"
    try:
        link.symlink_to(target)
        proc = run_verifier(trial_descriptor("_adv_evidence_scratch/via-link.md"))
        assert proc.returncode == 2, (
            "DEFEATED: verifier accepted an in-repo symlink to /tmp as durable evidence"
        )
        assert "escapes" in proc.stderr
    finally:
        _cleanup_adv_scratch()


def test_adversarial_traversal_to_tmp_fails(tmp_path):
    """A `..` traversal escaping the repo to /tmp must NOT pass."""
    target = tmp_path / "RESULTS.md"
    target.write_text('{"raw": "ephemeral"}', encoding="utf-8")
    # tmp_path is /tmp/pytest-*/... ; walk from the repo-relative scratch dir
    # up to the common /tmp ancestor. Compute the traversal dynamically.
    rel_up = "/".join([".."] * (len(ROOT.resolve().parts) - 1))
    scratch = _adv_scratch()
    evil = f"_adv_evidence_scratch/{rel_up}{str(target)[1:]}"
    try:
        proc = run_verifier(trial_descriptor(evil))
        assert proc.returncode == 2, (
            "DEFEATED: verifier accepted a ../.. traversal to /tmp as durable evidence"
        )
    finally:
        _cleanup_adv_scratch()


def test_adversarial_symlink_outside_repo_fails():
    """An in-repo symlink pointing outside the repo must NOT pass."""
    scratch = _adv_scratch()
    link = scratch / "etc-link.md"
    try:
        link.symlink_to("/etc/hostname")
        proc = run_verifier(trial_descriptor("_adv_evidence_scratch/etc-link.md"))
        assert proc.returncode == 2, (
            "DEFEATED: verifier accepted an in-repo symlink to /etc as durable evidence"
        )
        assert "escapes" in proc.stderr
    finally:
        _cleanup_adv_scratch()


def test_adversarial_symlink_committed_mode_fails(tmp_path):
    """--committed must not be fooled by a tracked symlink to ephemeral bytes."""
    target = tmp_path / "RESULTS.md"
    target.write_text('{"raw": "ephemeral"}', encoding="utf-8")
    scratch = _adv_scratch()
    link = scratch / "via-link.md"
    try:
        link.symlink_to(target)
        proc = run_verifier(
            trial_descriptor("_adv_evidence_scratch/via-link.md"), "--committed"
        )
        assert proc.returncode == 2, (
            "DEFEATED: --committed accepted a symlink to ephemeral evidence"
        )
    finally:
        _cleanup_adv_scratch()


def test_adversarial_ephemeral_repo_root_fails(tmp_path):
    """A repository root on ephemeral storage fails the whole claim."""
    desc_path = tmp_path / "d.json"
    desc_path.write_text(
        json.dumps({"trial_id": "t", "claim": "c", "raw_evidence_paths": ["x.md"]}),
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, str(VERIFIER), str(desc_path), "--repo", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2, "verifier MUST reject an ephemeral repository root"
    assert "ephemeral" in proc.stderr.lower()

def test_trial4_regression_would_have_failed():
    """Replays Trial-4's claim shape: summary stats, raw data at /tmp.

    The verifier must FAIL this — had it existed on 2026-10-07, Trial-4's
    claim could not have posted without durable evidence, and Naya 2's
    INCONCLUSIVE verdict would have been a pre-claim rejection instead.
    """
    descriptor = {
        "trial_id": "trial-04",
        "claim": "PASS: cold-successor knowledge trial, Fisher p=0.0007, Cohen h=2.214",
        "raw_evidence_paths": ["/tmp/trial4/RESULTS.md"],
        "posted_at": "2026-10-07T14:00:00Z",
    }
    proc = run_verifier(descriptor)
    assert proc.returncode == 2, (
        "REGRESSION: verifier accepted Trial-4's ephemeral evidence shape — "
        "the check is vacuous and the hole is NOT closed."
    )
