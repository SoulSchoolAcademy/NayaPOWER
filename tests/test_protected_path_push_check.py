"""Tests for tools/protected_path_push_check.py.

Positive control: a merge touching .github/workflows/ with no exception marker
must be flagged (exit 1, names the file).
Negative controls: valid marker -> clean; unprotected paths only -> clean;
empty range -> clean.
Sync: the script's protected-path tuple must equal the gate's canonical tuple.
"""
import importlib.util
import os
import subprocess
import sys
import tempfile

import pytest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "tools",
                      "protected_path_push_check.py")
GATE = os.path.join(os.path.dirname(__file__), "..", "tools", "auto_merge_gate.py")


def git(cwd, *args):
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                       timeout=60)
    assert p.returncode == 0, p.stderr
    return p.stdout.strip()


@pytest.fixture()
def repo():
    d = tempfile.mkdtemp(prefix="ppw-")
    git(d, "init", "-q")
    git(d, "config", "user.email", "t@t")
    git(d, "config", "user.name", "t")
    git(d, "commit", "-q", "--allow-empty", "-m", "root")
    return d


def run_check(repo, base, head, *extra):
    p = subprocess.run(
        [sys.executable, SCRIPT, "--base-ref", base, "--head-ref", head,
         "--repo-dir", repo, *extra],
        capture_output=True, text=True, timeout=120)
    return p


def make_merge(repo, path, message):
    """Create a --no-ff merge on main touching `path` with `message`."""
    git(repo, "checkout", "-q", "-b", "feature")
    full = os.path.join(repo, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write("x\n")
    git(repo, "add", path)
    git(repo, "commit", "-q", "-m", "feature work")
    git(repo, "checkout", "-q", "-")
    git(repo, "merge", "-q", "--no-ff", "feature", "-m", message)
    git(repo, "branch", "-q", "-D", "feature")


def test_violation_without_marker(repo):
    """POSITIVE: protected path, no exception -> flagged, exit 1."""
    base = git(repo, "rev-parse", "HEAD")
    make_merge(repo, ".github/workflows/evil.yml", "direct merge, no proof")
    head = git(repo, "rev-parse", "HEAD")
    p = run_check(repo, base, head)
    assert p.returncode == 1, p.stdout + p.stderr
    assert "VIOLATION" in p.stdout
    assert ".github/workflows/evil.yml" in p.stdout


def test_clean_with_valid_marker(repo):
    """NEGATIVE: valid supreme-law exception marker -> clean, exit 0."""
    base = git(repo, "rev-parse", "HEAD")
    make_merge(repo, ".github/workflows/ok.yml",
               "Merge pull request #9999\n\n"
               "Supreme-law-exception: ratified_by=Shawn Vibert "
               "evidence=6102792630 scope=worker protocol enforcement gates")
    head = git(repo, "rev-parse", "HEAD")
    p = run_check(repo, base, head)
    assert p.returncode == 0, p.stdout + p.stderr
    assert "clean" in p.stdout


def test_clean_unprotected_only(repo):
    """NEGATIVE: no protected paths touched -> clean, exit 0."""
    base = git(repo, "rev-parse", "HEAD")
    make_merge(repo, "tools/helper.py", "harmless tool")
    head = git(repo, "rev-parse", "HEAD")
    p = run_check(repo, base, head)
    assert p.returncode == 0, p.stdout + p.stderr


def test_empty_range(repo):
    """NEGATIVE: base == head -> clean, exit 0."""
    head = git(repo, "rev-parse", "HEAD")
    p = run_check(repo, head, head)
    assert p.returncode == 0, p.stdout + p.stderr


def test_prefixes_in_sync_with_gate():
    """The tripwire's list must equal the gate's canonical list, mechanically."""
    spec = importlib.util.spec_from_file_location("ppw", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    gate_src = open(GATE).read()
    assert "PROTECTED_PATH_PREFIXES" in gate_src
    gspec = importlib.util.spec_from_file_location("gate", GATE)
    gmod = importlib.util.module_from_spec(gspec)
    gspec.loader.exec_module(gmod)
    assert tuple(mod.PROTECTED_PATH_PREFIXES) == tuple(gmod.PROTECTED_PATH_PREFIXES), (
        f"tripwire {mod.PROTECTED_PATH_PREFIXES} != gate {gmod.PROTECTED_PATH_PREFIXES}")
