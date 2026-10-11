"""Tests for tools/d32_scan.py — the D32 live-operation wiring.

Every test uses a synthetic git repo (tmp_path) with real commits, so the
diff machinery is exercised, not mocked. Each test asserts the EXACT
per-file verdict and the scanner exit code.
"""

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.d32_scan import added_line_numbers, scan_file, scan_pr

GOOD_DOC = """# Clean report

We tracked 58 directives (#2175).

## WHAT THIS DOES NOT CLAIM

Does not claim enforcement.
"""

BAD_DOC = """# Sloppy report

We shipped 99 features. It is verified awesome.
"""


def _git(repo: Path, *args: str) -> str:
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True,
                       text=True, check=True)
    return r.stdout


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A git repo with one committed BRAIN/ doc."""
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@t.t")
    _git(r, "config", "user.name", "t")
    (r / "BRAIN").mkdir()
    (r / "BRAIN" / "doc.md").write_text(GOOD_DOC)
    _git(r, "add", ".")
    _git(r, "commit", "-qm", "base")
    return r


def _commit(repo: Path, msg: str = "x") -> None:
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", msg)


def _scan(repo: Path, scope: str = "BRAIN/") -> dict:
    base = _git(repo, "rev-parse", "HEAD~1").strip()
    head = _git(repo, "rev-parse", "HEAD").strip()
    import os
    cwd = os.getcwd()
    os.chdir(repo)
    try:
        return scan_pr(base, head, scope)
    finally:
        os.chdir(cwd)


# ---------------------------------------------------------------------------
# Verdict policy
# ---------------------------------------------------------------------------

def test_new_clean_file_passes(repo: Path):
    (repo / "BRAIN" / "new.md").write_text(GOOD_DOC)
    _commit(repo)
    report = _scan(repo)
    by_path = {f["path"]: f for f in report["files"]}
    assert by_path["BRAIN/new.md"]["verdict"] == "PASS"
    assert report["verdict"] == "PASS"


def test_new_bad_file_fails(repo: Path):
    (repo / "BRAIN" / "new.md").write_text(BAD_DOC)
    _commit(repo)
    report = _scan(repo)
    by_path = {f["path"]: f for f in report["files"]}
    assert by_path["BRAIN/new.md"]["verdict"] == "FAIL"
    assert report["verdict"] == "FAIL"
    rules = {v["rule"] for v in by_path["BRAIN/new.md"]["violations"]}
    assert {"R1", "R2", "R3"} <= rules


def test_modified_file_new_violation_fails(repo: Path):
    """An unsourced number ADDED to an existing doc blocks the PR."""
    p = repo / "BRAIN" / "doc.md"
    p.write_text(GOOD_DOC + "\nWe also shipped 42 widgets.\n")
    _commit(repo)
    report = _scan(repo)
    by_path = {f["path"]: f for f in report["files"]}
    assert by_path["BRAIN/doc.md"]["verdict"] == "FAIL"
    assert report["verdict"] == "FAIL"
    assert any(v["rule"] == "R1" and "'42'" in v["text"]
               for v in by_path["BRAIN/doc.md"]["violations"])


def test_modified_file_old_violations_warn_only(repo: Path):
    """Pre-existing violations are grandfathered: WARN, never FAIL."""
    # Base doc already violates R1/R2 on line 1; the PR only touches line 3.
    p = repo / "BRAIN" / "doc.md"
    p.write_text("We shipped 99 features.\n\nSome other text.\n")  # R1+R2 on L1
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "base with violations")
    p.write_text("We shipped 99 features.\n\nSome other text!\n")  # typo on L3 only
    _commit(repo)
    report = _scan(repo)
    by_path = {f["path"]: f for f in report["files"]}
    assert by_path["BRAIN/doc.md"]["verdict"] == "WARN"
    assert report["verdict"] == "PASS"  # warnings never block
    assert by_path["BRAIN/doc.md"]["warnings"], "expected grandfathered warnings"


def test_modified_file_missing_r2_warns_not_fails(repo: Path):
    """A modified doc without DOES-NOT-CLAIM warns; it does not block."""
    p = repo / "BRAIN" / "doc.md"
    # GOOD_DOC has R2; strip it, keep numbers sourced.
    no_r2 = "# Clean report\n\nWe tracked 58 directives (#2175).\n"
    p.write_text(no_r2)
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "base without R2")
    p.write_text(no_r2 + "\nTypo fix.\n")
    _commit(repo)
    report = _scan(repo)
    by_path = {f["path"]: f for f in report["files"]}
    assert by_path["BRAIN/doc.md"]["verdict"] == "WARN"
    assert report["verdict"] == "PASS"
    assert any(w["rule"] == "R2" for w in by_path["BRAIN/doc.md"]["warnings"])


def test_no_brain_changes_passes(repo: Path):
    (repo / "other.txt").write_text("We shipped 99 features.\n")
    _commit(repo)
    report = _scan(repo)
    assert report["files"] == []
    assert report["verdict"] == "PASS"


def test_non_md_changes_ignored(repo: Path):
    (repo / "BRAIN" / "img.png").write_bytes(b"\x89PNG 99")
    _commit(repo)
    report = _scan(repo)
    assert report["files"] == []
    assert report["verdict"] == "PASS"


# ---------------------------------------------------------------------------
# Diff plumbing
# ---------------------------------------------------------------------------

def test_added_line_numbers(repo: Path):
    p = repo / "BRAIN" / "doc.md"
    lines = GOOD_DOC.splitlines(keepends=True)
    lines.insert(2, "ADDED LINE HERE.\n")
    p.write_text("".join(lines))
    _commit(repo)
    base = subprocess.run(["git", "rev-parse", "HEAD~1"], cwd=repo,
                          capture_output=True, text=True,
                          check=True).stdout.strip()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo,
                          capture_output=True, text=True,
                          check=True).stdout.strip()
    import os
    cwd = os.getcwd()
    os.chdir(repo)
    try:
        added = added_line_numbers(base, head, "BRAIN/doc.md")
    finally:
        os.chdir(cwd)
    assert added == {3}, added


def test_scan_file_unit_new():
    """Unit: new-file status fails on any violation."""
    r = scan_file(BAD_DOC, "A", set())
    assert r["verdict"] == "FAIL"
    assert r["violations"] and not r["warnings"]
    r2 = scan_file(GOOD_DOC, "A", set())
    assert r2["verdict"] == "PASS"


def test_scan_file_unit_modified_grandfathers():
    """Unit: old-line violations warn; added-line violations fail."""
    doc = "We shipped 99 features.\n\nWe also shipped 42 widgets.\n"
    # Line 1 (old): R1 violation -> warn. Line 3 (added): R1 violation -> fail.
    r = scan_file(doc, "M", {3})
    assert r["verdict"] == "FAIL"
    assert any("'42'" in v["text"] for v in r["violations"])
    assert any("'99'" in v["text"] for v in r["warnings"])
