"""Controls for tools/verify_gitdata_merge_tree.py (ACT: no phantom work).

The tool is the mechanical form of the 2026-10-07 law: never trust a
git-data "merge" without diffing the result against a real local merge.

Every test builds a hermetic synthetic repo in tmp_path — deterministic,
no dependence on NayaPOWER's own history, no network.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[1] / "tools" / "verify_gitdata_merge_tree.py"


def _git(repo, *args):
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, timeout=120,
    )
    assert proc.returncode == 0, f"git {' '.join(args)} failed: {proc.stderr[:300]}"
    return proc.stdout.strip()


def _init_repo(path):
    _git(path, "init", "-b", "main", "-q")
    _git(path, "config", "user.email", "test@example.com")
    _git(path, "config", "user.name", "test")
    _git(path, "config", "commit.gpgsign", "false")
    (path / "seed.txt").write_text("seed\n")
    _git(path, "add", "seed.txt")
    _git(path, "commit", "-qm", "seed")
    return _git(path, "rev-parse", "HEAD")


def _commit_on(repo, branch, filename, content, message, base):
    _git(repo, "checkout", "-q", "-b", branch, base)
    (repo / filename).write_text(content)
    _git(repo, "add", filename)
    _git(repo, "commit", "-qm", message)
    return _git(repo, "rev-parse", "HEAD")


def _diverging_pair(repo):
    """base C; A adds side-a.txt, B adds side-b.txt. True merge has both."""
    c = _init_repo(repo)
    a = _commit_on(repo, "side-a", "side-a.txt", "a\n", "base side", c)
    b = _commit_on(repo, "side-b", "side-b.txt", "b\n", "head side", c)
    return a, b


def _run(repo, base, head, tree):
    proc = subprocess.run(
        [sys.executable, str(TOOL), base, head, tree, "--repo", str(repo)],
        capture_output=True, text=True, timeout=300,
    )
    return proc.returncode, json.loads(proc.stdout)


def _tree_of(repo, sha):
    return _git(repo, "show", "-s", "--format=%T", sha)


def test_true_merge_commit_verifies_match(tmp_path):
    """Positive control: a real local merge's tree passes the gate."""
    a, b = _diverging_pair(tmp_path)
    _git(tmp_path, "checkout", "-q", a)
    _git(tmp_path, "merge", "-q", "--no-ff", "-m", "real merge", b)
    merge_commit = _git(tmp_path, "rev-parse", "HEAD")
    code, verdict = _run(tmp_path, a, b, _tree_of(tmp_path, merge_commit))
    assert code == 0, verdict
    assert verdict["verdict"] == "MATCH"
    assert verdict["safe_to_move_ref"] is True


def test_head_tree_only_merge_is_refused_and_names_dropped_files(tmp_path):
    """Negative control: the exact 2026-10-07 failure class. A 'merge' whose
    tree is just the head's tree (base-side changes silently dropped) must
    be REFUSED, and the dropped files named."""
    a, b = _diverging_pair(tmp_path)
    broken_tree = _tree_of(tmp_path, b)  # tree = head tree: side-a.txt dropped
    code, verdict = _run(tmp_path, a, b, broken_tree)
    assert code == 1, verdict
    assert verdict["verdict"] == "MISMATCH"
    assert verdict["safe_to_move_ref"] is False
    assert "side-a.txt" in verdict["dropped_files"]
    assert "side-b.txt" not in verdict["dropped_files"]


def test_fast_forward_pair_head_tree_verifies_match(tmp_path):
    """A fast-forward-able pair merges to the head tree — that is correct,
    and the gate must not false-positive on it."""
    c = _init_repo(tmp_path)
    b = _commit_on(tmp_path, "ahead", "ahead.txt", "x\n", "ahead", c)
    code, verdict = _run(tmp_path, c, b, _tree_of(tmp_path, b))
    assert code == 0, verdict
    assert verdict["verdict"] == "MATCH"


def test_conflicted_pair_is_inconclusive_never_blessed(tmp_path):
    """A pair that does not merge cleanly cannot be verified this way —
    INCONCLUSIVE (exit 2), never MATCH."""
    c = _init_repo(tmp_path)
    a = _commit_on(tmp_path, "side-a", "seed.txt", "AAA\n", "conflict a", c)
    b = _commit_on(tmp_path, "side-b", "seed.txt", "BBB\n", "conflict b", c)
    code, verdict = _run(tmp_path, a, b, _tree_of(tmp_path, b))
    assert code == 2, verdict
    assert verdict["verdict"] == "INCONCLUSIVE"
    assert verdict.get("safe_to_move_ref", False) is not True


def test_garbage_sha_fails_closed(tmp_path):
    """Garbage input fails closed as INCONCLUSIVE — never blessed."""
    c = _init_repo(tmp_path)
    code, verdict = _run(tmp_path, c, "deadbeef" * 5, "cafe" * 10)
    assert code == 2, verdict
    assert verdict["verdict"] == "INCONCLUSIVE"


def test_usage_error_exits_2(tmp_path):
    proc = subprocess.run(
        [sys.executable, str(TOOL), "only-one-arg"],
        capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 2
