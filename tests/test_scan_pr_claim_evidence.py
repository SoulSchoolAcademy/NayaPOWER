"""Tests for the claim-evidence gate's PR-body caller (wire of #2325).

Includes the wire-lane negative controls: a violation MUST go red, and a
broken caller MUST fail closed (exit 2), never silently green.
"""

import os
import subprocess
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

from scan_pr_claim_evidence import extract_evidence, extract_seat, scan  # noqa: E402


def run_scan(body, repo_root=".", seat=""):
    return scan(body, author_seat=seat, repo_root=repo_root)


# --- violations: the gate must block ---------------------------------------

def test_violation_self_attested_note():
    body = "Seat: Naya 5\n\nThe migration is independently verified. See my note SN-0999."
    result = run_scan(body, repo_root=".")
    assert result["pass"] is False
    assert any("own seat" in r for v in result["verdicts"] for r in v.reasons)


def test_violation_bare_proven():
    body = "Seat: Naya 5\n\nThis approach is proven to work at scale."
    result = run_scan(body, repo_root=".")
    assert result["pass"] is False


def test_violation_phantom_test_path(tmp_path):
    body = "Seat: Naya 5\n\nindependently verified -- see tests/test_does_not_exist.py"
    result = run_scan(body, repo_root=str(tmp_path))
    assert result["pass"] is False
    assert any("does not exist" in r for v in result["verdicts"] for r in v.reasons)


def test_violation_repetition_is_not_corroboration():
    # A note by the author's own seat merely repeats the claim.
    body = "Seat: Naya 5\n\nindependent verification complete per my note SN-0001."
    result = run_scan(body, repo_root=".")
    assert result["pass"] is False


# --- honest bodies: the gate must pass -------------------------------------

def test_honest_existing_test_path(tmp_path):
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_real.py").write_text("# real")
    body = "Seat: Naya 5\n\nindependently verified -- tests/test_real.py 14/14 green."
    result = run_scan(body, repo_root=str(tmp_path))
    assert result["pass"] is True


def test_honest_ci_run_id():
    body = "Seat: Naya 5\n\nproven by CI run 37320466571 (all green)."
    result = run_scan(body, repo_root=".")
    assert result["pass"] is True


def test_honest_other_seat_review():
    body = "Seat: Naya 5\n\nverified by Naya 4 in review -- see the scorecard."
    result = run_scan(body, repo_root=".")
    assert result["pass"] is True


def test_honest_commit_is_supporting_only():
    # A commit proves existence, never verification -- alone it must fail.
    body = "Seat: Naya 5\n\nproven in commit abc1234def."
    result = run_scan(body, repo_root=".")
    assert result["pass"] is False


# --- quiet bodies: nothing claimed, nothing to prove ------------------------

def test_clean_body_passes():
    assert run_scan("Fixes a typo in the README.", repo_root=".")["pass"] is True


def test_empty_body_passes():
    assert run_scan("", repo_root=".")["pass"] is True


def test_code_identifier_does_not_trigger():
    body = "Set outcome_verified = True before returning."
    result = run_scan(body, repo_root=".")
    assert result["attestation_count"] == 0
    assert result["pass"] is True


# --- extraction -------------------------------------------------------------

def test_seat_extraction():
    assert extract_seat("Seat: Naya 5\n\nhello") == "naya5"
    assert extract_seat("seat: coda 3") == "coda3"
    assert extract_seat("no seat here") == ""


def test_evidence_extraction_kinds():
    body = ("Seat: Naya 5\nverified by Naya 4 in review. "
            "See tests/test_x.py and CI run 37320466571. Commit abc1234def. Note SN-0042.")
    kinds = {e.kind for e in extract_evidence(body)}
    assert {"test", "ci_run", "seat_review", "commit", "note"} <= kinds


def test_own_seat_line_is_not_a_review():
    body = "Seat: Naya 5\n\nnothing else."
    assert not [e for e in extract_evidence(body) if e.kind == "seat_review"]


def test_plain_long_number_without_ci_cue_is_not_a_run():
    body = "Receipt 6107766790 posted."
    assert not [e for e in extract_evidence(body) if e.kind == "ci_run"]


# --- fail-closed: exit codes via subprocess ----------------------------------

def _cli(body_file_content=None, extra_args=()):
    cmd = [sys.executable, os.path.join(os.path.dirname(__file__), "..", "tools",
                                        "scan_pr_claim_evidence.py")]
    if body_file_content is not None:
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
            fh.write(body_file_content)
            name = fh.name
        cmd += ["--body-file", name]
    cmd += ["--repo", "."]
    cmd += list(extra_args)
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    finally:
        if body_file_content is not None:
            os.unlink(name)


def test_cli_violation_exit_1():
    p = _cli("Seat: Naya 5\n\nThis is proven. Trust me.")
    assert p.returncode == 1
    assert "FAIL" in p.stdout


def test_cli_clean_exit_0():
    p = _cli("Minor docs fix, no claims.")
    assert p.returncode == 0
    assert "PASS" in p.stdout


def test_cli_failclosed_on_unreadable_body():
    cmd = [sys.executable, os.path.join(os.path.dirname(__file__), "..", "tools",
                                        "scan_pr_claim_evidence.py"),
           "--body-file", "/nonexistent/body.md", "--repo", "."]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    assert p.returncode == 2
    assert "FATAL" in p.stderr
