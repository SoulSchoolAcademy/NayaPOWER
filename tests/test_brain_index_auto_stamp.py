"""Tests for tools/brain_index_auto_stamp.py -- the drift-enforcement mechanism.

Behavioral proof (the #2230 shape): an unstamped BRAIN/ change is detected
and healed by committing the official generator's receipt files; every
failure mode aborts without committing or pushing anything.

The stub generator stands in for tools/regenerate_brain_index.py here to keep
the suite fast and hermetic. The REAL generator is exercised by the recorded
end-to-end proof (see hidden_files/drift-enforcement-20261011.md) and the
receipt-set coupling test below.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATOR = REPO_ROOT / "tools" / "brain_index_auto_stamp.py"
REAL_GENERATOR = REPO_ROOT / "tools" / "regenerate_brain_index.py"

GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "test",
    "GIT_AUTHOR_EMAIL": "test@test",
    "GIT_COMMITTER_NAME": "test",
    "GIT_COMMITTER_EMAIL": "test@test",
    "GIT_CONFIG_NOSYSTEM": "1",
    "HOME": "/tmp",  # keep global gitconfig out of the picture
}


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, env=GIT_ENV
    )


STUB_GENERATOR = """\
import argparse, os, sys
from pathlib import Path
ap = argparse.ArgumentParser()
ap.add_argument("--root", required=True)
args = ap.parse_args()
root = Path(args.root)
mode = os.environ.get("STUB_MODE", "stamp")
if mode == "fail":
    print("stub: generator failed", file=sys.stderr)
    sys.exit(1)
if mode == "evil":
    (root / "BRAIN" / "EVIL.md").write_text("not a receipt\\n")
if mode == "stamp":
    (root / "BRAIN" / "NAYAPOWER-BRAIN-INDEX.json").write_text(
        '{"stamped": true}\\n')
sentinel_dir = os.environ.get("STUB_SENTINEL_DIR")
if sentinel_dir:
    (Path(sentinel_dir) / "SENTINEL").write_text("generator ran\\n")
print("stub: ok")
"""


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    git(r, "init", "-q", "-b", "main")
    (r / "BRAIN").mkdir()
    (r / "BRAIN" / "CURRENT-MISSION-STATE.md").write_text("# mission\n")
    (r / "tools").mkdir()
    (r / "tools" / "stub_gen.py").write_text(STUB_GENERATOR)
    git(r, "add", "-A")
    git(r, "commit", "-qm", "base")
    return r


def run_orchestrator(repo: Path, *args: str, env_extra: dict | None = None,
                     sentinel_dir: Path | None = None):
    env = {**GIT_ENV, **(env_extra or {})}
    if sentinel_dir is not None:
        env["STUB_SENTINEL_DIR"] = str(sentinel_dir)
    return subprocess.run(
        [sys.executable, str(ORCHESTRATOR), "--root", str(repo),
         "--generator", "tools/stub_gen.py", *args],
        capture_output=True, text=True, env=env,
    )


def head_count(repo: Path) -> int:
    return int(git(repo, "rev-list", "--count", "HEAD").stdout.strip())


def test_unstamped_change_is_detected_and_healed(repo: Path):
    """The #2230 shape: BRAIN/ md changed, index stale -> detected, then healed."""
    # dry-run detects
    p = run_orchestrator(repo, "--dry-run", env_extra={"STUB_MODE": "stamp"})
    assert p.returncode == 0, p.stderr
    assert "STAMP-NEEDED" in p.stdout
    assert head_count(repo) == 1  # nothing committed by a dry run
    # real run heals
    p = run_orchestrator(repo, env_extra={"STUB_MODE": "stamp"})
    assert p.returncode == 0, p.stderr
    assert "STAMP-COMMITTED" in p.stdout
    assert head_count(repo) == 2
    files = git(repo, "show", "--name-only", "--pretty=format:", "HEAD").stdout.split()
    assert files == ["BRAIN/NAYAPOWER-BRAIN-INDEX.json"]
    # second run: already stamped -> nothing to do
    p = run_orchestrator(repo, "--dry-run", env_extra={"STUB_MODE": "stamp"})
    assert "NO-STAMP" in p.stdout
    assert head_count(repo) == 2


def test_generator_failure_is_fail_closed(repo: Path):
    p = run_orchestrator(repo, env_extra={"STUB_MODE": "fail"})
    assert p.returncode == 2
    assert "ABORT-GENERATOR-FAILED" in p.stdout
    assert head_count(repo) == 1


def test_unexpected_files_are_fail_closed(repo: Path):
    """A generator that touches anything outside the receipt set aborts."""
    p = run_orchestrator(repo, env_extra={"STUB_MODE": "evil"})
    assert p.returncode == 2
    assert "ABORT-UNEXPECTED-FILES" in p.stdout
    assert head_count(repo) == 1
    # the evil file is still uncommitted in the worktree (nothing was staged)
    assert (repo / "BRAIN" / "EVIL.md").exists()


def test_dirty_worktree_refuses_before_generator_runs(repo: Path, tmp_path: Path):
    """SN-0327: regen on a dirty worktree is a lie generator -- refuse."""
    (repo / "BRAIN" / "CURRENT-MISSION-STATE.md").write_text("# changed\n")
    p = run_orchestrator(repo, env_extra={"STUB_MODE": "stamp"},
                         sentinel_dir=tmp_path)
    assert p.returncode == 2
    assert "ABORT-DIRTY-WORKTREE" in p.stdout
    assert not (tmp_path / "SENTINEL").exists()  # generator never invoked
    assert head_count(repo) == 1


def test_push_to_remote_works_end_to_end(repo: Path, tmp_path: Path):
    bare = tmp_path / "remote.git"
    git(tmp_path, "init", "-q", "--bare", str(bare))
    subprocess.run(["git", "--git-dir", str(bare), "symbolic-ref",
                    "HEAD", "refs/heads/main"], check=True)
    git(repo, "remote", "add", "origin", str(bare))
    git(repo, "push", "-q", "origin", "main")
    p = run_orchestrator(
        repo, "--push-to", "main", env_extra={"STUB_MODE": "stamp"})
    assert p.returncode == 0, p.stderr
    assert "PUSHED" in p.stdout
    clone = tmp_path / "clone"
    git(tmp_path, "clone", "-q", str(bare), str(clone))
    assert (clone / "BRAIN" / "NAYAPOWER-BRAIN-INDEX.json").read_text() == \
        '{"stamped": true}\n'


def test_push_failure_exits_3_and_keeps_local_commit(repo: Path):
    p = run_orchestrator(
        repo, "--push-to", "main", "--remote", "file:///nonexistent-remote",
        env_extra={"STUB_MODE": "stamp"})
    assert p.returncode == 3
    assert "ABORT-PUSH-FAILED" in p.stderr
    assert head_count(repo) == 2  # committed locally, not pushed


def test_not_a_repo_aborts(repo: Path, tmp_path: Path):
    p = run_orchestrator(tmp_path)
    assert p.returncode == 2
    assert "ABORT-NOT-A-REPO" in p.stdout


def test_receipt_set_matches_generator():
    """The orchestrator's fail-closed set must track the official generator's
    RECEIPT_PATHS -- if the generator ever owns a new receipt file, this test
    fails loudly instead of the orchestrator silently aborting."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "regen", str(REAL_GENERATOR))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    spec2 = importlib.util.spec_from_file_location(
        "stamp", str(ORCHESTRATOR))
    orch = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(orch)

    assert set(orch.RECEIPT_PATHS) == set(mod.RECEIPT_PATHS), (
        f"orchestrator {sorted(orch.RECEIPT_PATHS)} != "
        f"generator {sorted(mod.RECEIPT_PATHS)}"
    )
