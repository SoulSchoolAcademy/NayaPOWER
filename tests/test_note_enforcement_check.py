"""Tests for tools/note_enforcement_check.py (W4 truth-enforcement wiring rung).

The tool is deliberately report-only ("A gate that fired on every legitimate
note would be a gate that got deleted"). What must not drift silently is the
measurement contract: which paths count as notes, which count as enforcement,
and the shape of the JSON report. These tests pin that contract.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    spec = importlib.util.spec_from_file_location(
        "note_enforcement_check", ROOT / "tools" / "note_enforcement_check.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def mod():
    return load_module()


# --- is_note_path -----------------------------------------------------------

NOTE_HITS = [
    "BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/IB-SMART-NOTE-20261005-foo.md",
    "docs/SMART-NOTE-0123-whatever.md",
    "tools/SMART_NOTE_helper.py",
]

NOTE_MISSES = [
    "docs/regular-design-note.md",
    "tools/truth_state_guard.py",
    "tests/test_note_enforcement_check.py",
]


@pytest.mark.parametrize("path", NOTE_HITS)
def test_is_note_path_hits(mod, path):
    assert mod.is_note_path(path) is True


@pytest.mark.parametrize("path", NOTE_MISSES)
def test_is_note_path_misses(mod, path):
    assert mod.is_note_path(path) is False


# --- is_enforcement_path ----------------------------------------------------

ENFORCEMENT_HITS = [
    "tests/test_something.py",
    ".github/workflows/kernel-tests.yml",
    "tools/truth_state_guard.py",
    "supabase/migrations/20261008_x.sql",
    "kernel/value_calculus.py",
    "supabase/functions/nayanet-github-dispatch/index.ts",
    "docs/SOME-CONTRACT-V1.md",
    "BRAIN/01-GOVERNANCE/0003-SYSTEM-SCORECARD-SPEC-V1.md",
]

ENFORCEMENT_MISSES = [
    "BRAIN/04-INTELLIGENCE/some-essay.md",
    "workspace/user/files/deck.html",
    "docs/README.md",
]


@pytest.mark.parametrize("path", ENFORCEMENT_HITS)
def test_is_enforcement_path_hits(mod, path):
    assert mod.is_enforcement_path(path) is True


@pytest.mark.parametrize("path", ENFORCEMENT_MISSES)
def test_is_enforcement_path_misses(mod, path):
    assert mod.is_enforcement_path(path) is False


# --- main() contract via fixture git repo ----------------------------------

def make_fixture_repo(tmp_path):
    repo = tmp_path / "fixture"
    repo.mkdir()
    env = {"GIT_CONFIG_NOSYSTEM": "1", "HOME": str(tmp_path)}
    def git(*args):
        subprocess.run(["git", *args], cwd=repo, check=True,
                       capture_output=True, env={**__import__("os").environ, **env})
    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    git("commit", "-q", "--allow-empty", "-m", "base")
    (repo / "IB-SMART-NOTE-TEST-001.md").write_text("# note only\n")
    git("add", ".")
    git("commit", "-q", "-m", "note only commit")
    (repo / "IB-SMART-NOTE-TEST-002.md").write_text("# note + test\n")
    (repo / "tests").mkdir(exist_ok=True)
    (repo / "tests" / "test_enforced_thing.py").write_text("def test_x(): pass\n")
    git("add", ".")
    git("commit", "-q", "-m", "note with enforcement")
    return repo


def run_main(mod, repo, monkeypatch, extra_args):
    monkeypatch.setattr(mod, "ROOT", repo)
    monkeypatch.setattr(sys, "argv", ["note_enforcement_check.py", "--base", "HEAD~2", *extra_args])
    return mod.main()


def test_json_contract_counts_notes_and_enforcement(mod, tmp_path, monkeypatch, capsys):
    repo = make_fixture_repo(tmp_path)
    rc = run_main(mod, repo, monkeypatch, ["--json"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["commits_with_notes"] == 2
    assert payload["commits_carrying_enforcement"] == 1
    assert payload["pct"] == 50.0
    flags = {r["enforced"] for r in payload["notes"]}
    assert flags == {True, False}


def test_never_fails_closed_even_when_nothing_enforced(mod, tmp_path, monkeypatch, capsys):
    """Fail-open by design: the tool reports; a refusing gate would be deleted."""
    repo = tmp_path / "fixture2"
    repo.mkdir()
    env = {"GIT_CONFIG_NOSYSTEM": "1", "HOME": str(tmp_path)}
    def git(*args):
        subprocess.run(["git", *args], cwd=repo, check=True,
                       capture_output=True, env={**__import__("os").environ, **env})
    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    git("commit", "-q", "--allow-empty", "-m", "base")
    (repo / "IB-SMART-NOTE-TEST-003.md").write_text("# prose only\n")
    git("add", ".")
    git("commit", "-q", "-m", "pure prose commit")
    monkeypatch.setattr(mod, "ROOT", repo)
    monkeypatch.setattr(sys, "argv", ["note_enforcement_check.py", "--base", "HEAD~1", "--json"])
    rc = mod.main()
    assert rc == 0  # reports 0%, does not fail
    payload = json.loads(capsys.readouterr().out)
    assert payload["pct"] == 0.0


def test_empty_range_reports_zero_without_error(mod, tmp_path, monkeypatch, capsys):
    repo = make_fixture_repo(tmp_path)
    monkeypatch.setattr(mod, "ROOT", repo)
    monkeypatch.setattr(sys, "argv", ["note_enforcement_check.py", "--base", "HEAD", "--json"])
    rc = mod.main()
    assert rc == 0
    assert "no commits between" in capsys.readouterr().err
