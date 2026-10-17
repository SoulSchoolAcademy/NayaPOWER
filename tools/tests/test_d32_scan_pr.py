"""Tests for tools/d32_scan_pr.py — the D32 wiring seam.

The gate (tools/d32_gate.py) judges documents; this tests the WIRE: that the
scanner diffs exactly the PR's changes and nothing else. The critical
regression case is the 2026-10-11 stale-base incident: GitHub reported
pull_request.base.sha = f2c614a while the merge commit was built on b461609b,
so a SHA-based diff judged main's own progress as the PR's changes. The
scanner must resolve the merge-base live from a base REF.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.d32_scan_pr import scan, main as scan_main


VIOLATING = """# Report

We shipped 47 features. It is proven awesome.
"""

COMPLIANT = """# Report

We shipped 47 features (#1234).

## WHAT THIS DOES NOT CLAIM

Does not claim enforcement.
"""


def _git(repo: Path, *args: str) -> str:
    env = dict(os.environ,
               GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    out = subprocess.run(["git", *args], cwd=repo, capture_output=True,
                         text=True, env=env, check=True)
    return out.stdout.strip()


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q", "-b", "main")
    _git(r, "commit", "-q", "--allow-empty", "-m", "base")
    return r


def _commit_file(repo: Path, branch: str, name: str, content: str) -> None:
    _git(repo, "checkout", "-q", branch)
    (repo / name).write_text(content, encoding="utf-8")
    _git(repo, "add", name)
    _git(repo, "commit", "-q", "-m", f"add {name}")


def test_scan_passes_compliant_pr_doc(repo: Path, monkeypatch) -> None:
    _git(repo, "checkout", "-q", "-b", "pr")
    _commit_file(repo, "pr", "doc.md", COMPLIANT)
    monkeypatch.chdir(repo)
    result = scan("main", "pr")
    assert result["verdict"] == "PASS", result
    assert [d["path"] for d in result["documents"]] == ["doc.md"]


def test_scan_fails_violating_pr_doc(repo: Path, monkeypatch) -> None:
    _git(repo, "checkout", "-q", "-b", "pr")
    _commit_file(repo, "pr", "doc.md", VIOLATING)
    monkeypatch.chdir(repo)
    result = scan("main", "pr")
    assert result["verdict"] == "FAIL"
    assert result["documents"][0]["path"] == "doc.md"
    rules = {v["rule"] for v in result["documents"][0]["violations"]}
    assert rules == {"R1", "R2", "R3"}


def test_scan_passes_when_no_markdown_changed(repo: Path, monkeypatch) -> None:
    _git(repo, "checkout", "-q", "-b", "pr")
    _commit_file(repo, "pr", "code.py", "x = 1\n")
    monkeypatch.chdir(repo)
    result = scan("main", "pr")
    assert result["verdict"] == "PASS"
    assert result["documents"] == []


def test_scan_ignores_base_branch_progress_stale_base_incident(
    repo: Path, monkeypatch
) -> None:
    """Regression: the PR's diff must never include the base branch's progress.

    Reproduces 2026-10-11: PR branched at old base; main advanced with a
    violating doc; merge commit built on new main. Scanning base-ref...merge
    must judge ONLY the PR's own document. A stale recorded base SHA would
    wrongly widen the diff — the test proves both behaviors.
    """
    old_base = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "-q", "-b", "pr")          # pr branched at old base
    _commit_file(repo, "pr", "pr-doc.md", COMPLIANT)  # PR's own doc: clean
    _commit_file(repo, "main", "main-progress.md", VIOLATING)  # main moved on
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "-q", "--no-ff", "pr", "-m", "merge pr")
    monkeypatch.chdir(repo)

    # Correct wiring: live base ref -> merge commit judges only PR changes.
    result = scan("HEAD^1", "HEAD")
    assert result["verdict"] == "PASS", result
    assert [d["path"] for d in result["documents"]] == ["pr-doc.md"]
    assert result["merge_base"] == _git(repo, "rev-parse", "HEAD^1")
    assert "main-progress.md" not in [d["path"] for d in result["documents"]]

    # The bug this regresses: a stale recorded base SHA widens the diff to
    # include the base branch's own progress (this is what CI did on 2026-10-11).
    buggy = scan(old_base, "HEAD")
    assert buggy["verdict"] == "FAIL"
    assert "main-progress.md" in [d["path"] for d in buggy["documents"]]


def test_scan_fails_closed_on_bad_rev(repo: Path, monkeypatch) -> None:
    monkeypatch.chdir(repo)
    result = scan("main", "deadbeef" * 5)
    assert result["verdict"] == "SCANNER_ERROR"


def test_main_exit_codes(repo: Path, monkeypatch, capsys) -> None:
    _git(repo, "checkout", "-q", "-b", "pr")
    _commit_file(repo, "pr", "doc.md", VIOLATING)
    monkeypatch.chdir(repo)
    assert scan_main(["d32_scan_pr.py", "--base", "main", "--head", "pr"]) == 1
    (repo / "doc.md").write_text(COMPLIANT, encoding="utf-8")
    _git(repo, "add", "doc.md")
    _git(repo, "commit", "-q", "--amend", "--no-edit")
    assert scan_main(["d32_scan_pr.py", "--base", "main", "--head", "pr"]) == 0
