"""Tests for the PR-scoped brain-index freshness wrapper
(tools/protocol/checks/brain_index_freshness_pr.py, law BRAIN-INDEX-FRESHNESS).

The wrapper exists for required-check safety: the workflow runs on EVERY
PR, and the BRAIN-scope decision happens inside the job. These tests prove
the wrapper's contract against REAL git bytes wherever the test is about
scope detection (hermetic temp repos with real commits), and stub the
underlying gate only where the test is about the wrapper's own routing —
the gate's own behavior is already proven by
tests/test_brain_index_freshness.py.
"""

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

ROOT = Path(__file__).resolve().parents[1]
WRAPPER_PATH = ROOT / "tools" / "protocol" / "checks" / "brain_index_freshness_pr.py"


def load_wrapper():
    spec = importlib.util.spec_from_file_location(
        "brain_index_freshness_pr", WRAPPER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def w():
    return load_wrapper()


def git(cwd, *args):
    subprocess.run(["git", "-C", str(cwd), *args],
                   check=True, capture_output=True)


def _head_sha(repo):
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True,
                          check=True).stdout.strip()


@pytest.fixture
def mini_repo(tmp_path):
    """A real git repo with two commits: base, and a head that changes
    non-BRAIN files only. Returns (repo_path, base_sha, head_sha)."""
    repo = tmp_path / "mini"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "test@naya.local")
    git(repo, "config", "user.name", "naya-test")
    (repo / "BRAIN").mkdir()  # a NayaPOWER-shaped tree (fail-closed needs it)
    (repo / "BRAIN" / "REAL-TREE.json").write_text("{}\n")
    (repo / "docs").mkdir()
    (repo / "docs" / "note.md").write_text("hello\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "base")
    base = _head_sha(repo)
    (repo / "docs" / "note.md").write_text("hello world\n")
    (repo / "tools").mkdir()
    (repo / "tools" / "x.py").write_text("print(1)\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "head: non-BRAIN changes only")
    return repo, base, _head_sha(repo)


@pytest.fixture
def mini_repo_brain(tmp_path):
    """A real git repo whose head commit touches BRAIN/."""
    repo = tmp_path / "minib"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "test@naya.local")
    git(repo, "config", "user.name", "naya-test")
    (repo / "BRAIN").mkdir()
    (repo / "BRAIN" / "REAL-TREE.json").write_text("{}\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "base")
    base = _head_sha(repo)
    (repo / "BRAIN" / "REAL-TREE.json").write_text('{"x": 1}\n')
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "head: BRAIN change")
    return repo, base, _head_sha(repo)


# ---- the P0 negative control: non-BRAIN PR -> NOT_APPLICABLE, cheap ----

def test_non_brain_pr_is_not_applicable_on_real_bytes(w, mini_repo):
    """Real git diff on real commits: a PR that changes only non-BRAIN
    files gets NOT_APPLICABLE with pass=True — the required check can
    never sit Pending on such a PR."""
    repo, base, head = mini_repo
    res = w.decide({"repo_root": str(repo),
                    "base_sha": base, "head_sha": head})
    assert res["pass"] is True
    assert res["details"]["verdict"] == "NOT_APPLICABLE"
    assert res["details"]["brain_touched_paths"] == []
    assert "NOT_APPLICABLE" in res["reasons"][0]


def test_non_brain_pr_never_invokes_the_gate(w, mini_repo, monkeypatch):
    """The cheap path is genuinely cheap: the underlying (expensive) gate
    is never loaded on a NOT_APPLICABLE PR."""
    repo, base, head = mini_repo

    def boom():
        raise AssertionError(
            "the gate must not be invoked for NOT_APPLICABLE")

    monkeypatch.setattr(w, "_load_gate_module", boom)
    res = w.run({"repo_root": str(repo),
                 "base_sha": base, "head_sha": head})
    assert res["pass"] is True
    assert res["details"]["verdict"] == "NOT_APPLICABLE"


# ---- BRAIN PR -> full gate, verdict propagated exactly ----

def test_brain_pr_runs_full_gate_and_propagates_pass(
        w, mini_repo_brain, monkeypatch):
    """Real git diff sees the BRAIN/ touch; a passing gate propagates as
    PASS — the wrapper never invents green, it only forwards it."""
    repo, base, head = mini_repo_brain
    called = {}

    class FakeGate:
        @staticmethod
        def check(record):
            called["record"] = record
            return {"pass": True, "reasons": ["gate: fresh"],
                    "details": {"law": "BRAIN-INDEX-FRESHNESS"}}

    monkeypatch.setattr(w, "_load_gate_module", lambda: FakeGate)
    res = w.run({"repo_root": str(repo),
                 "base_sha": base, "head_sha": head})
    assert called["record"] == {"repo_root": str(repo)}
    assert res["pass"] is True
    assert res["details"]["verdict"] == "FULL_CHECK"
    assert any("BRAIN/" in r for r in res["reasons"])


def test_brain_pr_runs_full_gate_and_propagates_fail(
        w, mini_repo_brain, monkeypatch):
    """A failing gate propagates as FAIL — the required check blocks, as
    designed. This is the enforcement path."""
    repo, base, head = mini_repo_brain

    class FakeGate:
        @staticmethod
        def check(record):
            return {"pass": False, "reasons": ["gate: DRIFT"],
                    "details": {"law": "BRAIN-INDEX-FRESHNESS",
                                "drift_items": ["x"]}}

    monkeypatch.setattr(w, "_load_gate_module", lambda: FakeGate)
    res = w.run({"repo_root": str(repo),
                 "base_sha": base, "head_sha": head})
    assert res["pass"] is False
    assert res["details"]["verdict"] == "FULL_CHECK"
    assert "DRIFT" in " ".join(res["reasons"])


# ---- unknown scope fails closed, never open ----

def test_missing_shas_fail_closed(w, mini_repo):
    """No SHAs anywhere (record or env): scope is UNKNOWN — the wrapper
    routes to FULL_CHECK, it does not guess NOT_APPLICABLE."""
    repo, _, _ = mini_repo
    env = {k: v for k, v in os.environ.items()
           if k not in ("BASE_SHA", "HEAD_SHA")}
    with mock.patch.dict(os.environ, env, clear=True):
        res = w.decide({"repo_root": str(repo)})
    assert res["details"]["verdict"] == "FULL_CHECK"
    assert res["details"]["fail_closed"] == "sha"
    assert res["pass"] is False  # scope unknown: fail, don't bless


def test_malformed_sha_fails_closed(w, mini_repo):
    repo, _, _ = mini_repo
    res = w.decide({"repo_root": str(repo),
                    "base_sha": "not-a-sha", "head_sha": "0" * 40})
    assert res["details"]["verdict"] == "FULL_CHECK"
    assert res["details"]["fail_closed"] == "sha"


def test_git_failure_fails_closed(w, mini_repo, monkeypatch):
    """git diff blows up (corrupt repo, missing objects): FULL_CHECK, not
    a silent pass."""
    repo, base, head = mini_repo

    def raising_run(*args, **kwargs):
        raise subprocess.CalledProcessError(128, "git")

    monkeypatch.setattr(w.subprocess, "run", raising_run)
    res = w.decide({"repo_root": str(repo),
                    "base_sha": base, "head_sha": head})
    assert res["details"]["verdict"] == "FULL_CHECK"
    assert res["details"]["fail_closed"] == "git-diff"


def test_non_checkout_repo_root_fails_closed(w, tmp_path):
    """repo_root that is not a NayaPOWER checkout: the wrapper admits it
    cannot verify and fails closed."""
    res = w.decide({"repo_root": str(tmp_path),
                    "base_sha": "0" * 40, "head_sha": "1" * 40})
    assert res["pass"] is False
    assert res["details"]["fail_closed"] == "repo_root"


def test_run_on_non_checkout_returns_fail_closed_without_keyerror(
        w, tmp_path):
    """Regression: CI showed `run()` raising KeyError: 'repo_root' when
    decide() failed closed before a repo root existed. run() must return
    the fail-closed decision itself — a crash is not a verdict."""
    res = w.run({"repo_root": str(tmp_path),
                 "base_sha": "0" * 40, "head_sha": "1" * 40})
    assert res["pass"] is False
    assert res["details"]["verdict"] == "FULL_CHECK"
    assert res["details"]["fail_closed"] == "repo_root"


def test_default_repo_root_resolves_to_this_checkout(w):
    """Regression: the default repo_root once pointed at tools/ instead
    of the repo root (parents[2] vs parents[3]) — every CI run failed
    closed on repo_root. The default must resolve to this checkout."""
    root = w._resolve_repo_root({})
    assert root == ROOT
    assert (root / "BRAIN").is_dir()
    assert (root / ".git").exists()


# ---- three-dot scope: the PR is not blamed for the base's newer changes ----

def test_old_pr_not_blamed_for_base_brain_changes(w, tmp_path):
    """The exact bug CI caught on the first push: base.sha is the base
    branch's CURRENT tip, which may carry BRAIN/ changes that landed
    after the PR forked. Scope must use the PR's own changeset
    (`base...head`, three-dot) — a PR that itself touches no BRAIN/
    files is NOT_APPLICABLE even when the base moved under it. Two-dot
    would have routed FULL_CHECK and failed the PR on drift it never
    introduced."""
    repo = tmp_path / "fork"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "test@naya.local")
    git(repo, "config", "user.name", "naya-test")
    trunk = subprocess.run(
        ["git", "-C", str(repo), "branch", "--show-current"],
        capture_output=True, text=True, check=True).stdout.strip()
    (repo / "BRAIN").mkdir()
    (repo / "BRAIN" / "REAL-TREE.json").write_text("{}\n")
    (repo / "docs").mkdir()
    (repo / "docs" / "note.md").write_text("v1\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "fork point")
    # the PR branch: one non-BRAIN change
    git(repo, "checkout", "-qb", "pr")
    (repo / "docs" / "note.md").write_text("v2\n")
    git(repo, "commit", "-qam", "pr: docs only")
    pr_head = _head_sha(repo)
    # the base branch advances with a BRAIN/ change AFTER the fork
    git(repo, "checkout", "-q", trunk)
    (repo / "BRAIN" / "REAL-TREE.json").write_text('{"drift": true}\n')
    git(repo, "commit", "-qam", "base: BRAIN change after fork")
    base_tip = _head_sha(repo)

    res = w.decide({"repo_root": str(repo),
                    "base_sha": base_tip, "head_sha": pr_head})
    assert res["pass"] is True
    assert res["details"]["verdict"] == "NOT_APPLICABLE", res["reasons"]
    assert res["details"]["brain_touched_paths"] == []

def test_cli_non_brain_exits_zero_on_real_bytes(mini_repo):
    """Exact CI invocation shape: BASE_SHA/HEAD_SHA env + --json, exit 0
    for a non-BRAIN PR."""
    repo, base, head = mini_repo
    env = dict(os.environ, BASE_SHA=base, HEAD_SHA=head)
    proc = subprocess.run(
        [sys.executable, str(WRAPPER_PATH), "--json",
         "--record", json.dumps({"repo_root": str(repo)})],
        capture_output=True, text=True, env=env)
    assert proc.returncode == 0, proc.stderr + proc.stdout
    payload = json.loads(proc.stdout)
    assert payload["pass"] is True
    assert payload["details"]["verdict"] == "NOT_APPLICABLE"


def test_cli_brain_touch_on_foreign_tree_exits_nonzero(mini_repo_brain):
    """BRAIN-touching PR against a non-NayaPOWER tree: the full gate runs
    and fails closed (foreign tree is not verifiable) — exit nonzero, the
    enforcement direction."""
    repo, base, head = mini_repo_brain
    env = dict(os.environ, BASE_SHA=base, HEAD_SHA=head)
    proc = subprocess.run(
        [sys.executable, str(WRAPPER_PATH), "--json",
         "--record", json.dumps({"repo_root": str(repo)})],
        capture_output=True, text=True, env=env)
    assert proc.returncode != 0, proc.stdout
    payload = json.loads(proc.stdout)
    assert payload["pass"] is False
    assert payload["details"]["verdict"] == "FULL_CHECK"


def test_exact_check_name_is_brain_index_freshness():
    """The workflow's job name must stay exactly `brain-index-freshness` —
    it is the check name Shawn marks REQUIRED in branch protection. A
    rename here silently breaks enforcement."""
    wf = (ROOT / ".github" / "workflows" /
          "brain-index-freshness.yml").read_text()
    assert "name: brain-index-freshness" in wf
    # and the trigger must NOT be paths-filtered (the P0 flaw)
    assert "paths:" not in wf.split("jobs:")[0]


def test_workflow_trigger_is_unconditional():
    """Regression guard for the exact flaw this repair fixes: a
    paths-filtered trigger leaves a REQUIRED check Pending forever on
    non-matching PRs. The `on:` block must carry no paths filter."""
    import re
    wf = (ROOT / ".github" / "workflows" /
          "brain-index-freshness.yml").read_text()
    on_block = wf.split("jobs:")[0]
    # strip comments: the header prose mentions "paths-filtered" — the
    # assertion is about the YAML trigger, not the prose.
    yaml_lines = [ln for ln in on_block.splitlines()
                  if not ln.lstrip().startswith("#")]
    yaml_block = "\n".join(yaml_lines)
    assert re.search(r"^\s*on:\s*$", yaml_block, re.M) is not None
    assert "pull_request:" in yaml_block
    assert "paths" not in yaml_block
