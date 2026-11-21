"""Regression tests for tools/doc_completeness_check.py.

Covers the changed-only scoping of the governance-triple check
(self-build cycle 253): in --changed-only mode only laws whose files
changed are checked, so pre-existing governance debt can no longer red
the gate on an unrelated capture-only push. Full mode is unchanged.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"

# The two laws whose pre-existing debt reds the gate at pin aa6610dd:
# 0038 has only .human.md (2 failures); DAILY-LAW-REGISTRY has
# .human.md + .machine.json (1 failure).
DEBT_LAWS = {
    "0038-WHAT-NAYA-STANDS-FOR": [".human.md"],
    "DAILY-LAW-REGISTRY": [".human.md", ".machine.json"],
}


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "doc_completeness_check_under_test",
        TOOLS_DIR / "doc_completeness_check.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def checker():
    return load_checker()


def _gov_dir(tmp_path, laws):
    gov = tmp_path / "BRAIN" / "01-GOVERNANCE"
    gov.mkdir(parents=True)
    for base, suffixes in laws.items():
        for suffix in suffixes:
            p = gov / (base + suffix)
            p.write_text("{}" if suffix == ".machine.json" else "# law\n",
                         encoding="utf-8")
    return gov


def test_full_mode_reports_all_debt(checker, tmp_path):
    """Unchanged behavior: full mode checks every law triple."""
    gov = _gov_dir(tmp_path, DEBT_LAWS)
    failures, warnings, checked = checker.check_law_triple(gov)
    assert checked == 2
    assert len(failures) == 3
    assert any("0038-WHAT-NAYA-STANDS-FOR: AI form missing" in f for f in failures)
    assert any("0038-WHAT-NAYA-STANDS-FOR: machine form missing" in f for f in failures)
    assert any("DAILY-LAW-REGISTRY: AI form missing" in f for f in failures)


def test_changed_only_scopes_to_changed_laws(checker, tmp_path):
    """Only the changed law's triple is checked; other debt is not blocking."""
    gov = _gov_dir(tmp_path, DEBT_LAWS)
    failures, _warnings, checked = checker.check_law_triple(
        gov, only_bases={"0038-what-naya-stands-for"})
    assert checked == 1
    assert len(failures) == 2
    assert all("0038-WHAT-NAYA-STANDS-FOR" in f for f in failures)
    assert not any("DAILY-LAW-REGISTRY" in f for f in failures)


def test_changed_only_empty_scope_checks_nothing(checker, tmp_path):
    """No governance files changed -> the triple check is skipped entirely."""
    gov = _gov_dir(tmp_path, DEBT_LAWS)
    failures, warnings, checked = checker.check_law_triple(gov, only_bases=set())
    assert (failures, warnings, checked) == ([], [], 0)


def test_law_base_of(checker):
    assert checker.law_base_of("0038-WHAT-NAYA-STANDS-FOR.ai.md") == \
        "0038-WHAT-NAYA-STANDS-FOR"
    assert checker.law_base_of("DAILY-LAW-REGISTRY.human.md") == "DAILY-LAW-REGISTRY"
    assert checker.law_base_of("DAILY-LAW-REGISTRY.machine.json") == \
        "DAILY-LAW-REGISTRY"
    assert checker.law_base_of("0038-WHAT-NAYA-STANDS-FOR.md") == \
        "0038-WHAT-NAYA-STANDS-FOR"
    assert checker.law_base_of("README.md") == "README"
    assert checker.law_base_of("notes.txt") is None


def test_main_changed_only_empty_diff_exits_zero(checker, tmp_path, monkeypatch, capsys):
    """The CI push condition at pin aa6610dd: empty diff, pre-existing debt
    present — the gate must now pass instead of exiting 1."""
    gov = _gov_dir(tmp_path, DEBT_LAWS)
    root = tmp_path / "repo"
    root.mkdir()
    monkeypatch.setattr(checker, "ROOT", root)
    monkeypatch.setattr(checker, "CAPTURE_DIR", root / ".naya" / "capture")
    monkeypatch.setattr(checker, "GOV_DIR", gov)
    monkeypatch.setattr(checker, "changed_files", lambda: [])
    monkeypatch.setattr(sys, "argv", ["doc_completeness_check.py", "--changed-only"])
    assert checker.main() == 0
    out = capsys.readouterr().out
    assert "Checked 0 Smart Notes + 0 governance triples." in out
    assert "FAIL:" not in out


def test_main_changed_only_changed_law_still_fails(checker, tmp_path, monkeypatch, capsys):
    """A changed law with an incomplete triple still fails — the scope fix
    does not weaken the gate for the law that actually changed."""
    gov = _gov_dir(tmp_path, DEBT_LAWS)
    root = tmp_path / "repo"
    root.mkdir()
    monkeypatch.setattr(checker, "ROOT", root)
    monkeypatch.setattr(checker, "CAPTURE_DIR", root / ".naya" / "capture")
    monkeypatch.setattr(checker, "GOV_DIR", gov)
    monkeypatch.setattr(
        checker, "changed_files",
        lambda: [gov / "0038-WHAT-NAYA-STANDS-FOR.human.md"])
    monkeypatch.setattr(sys, "argv", ["doc_completeness_check.py", "--changed-only"])
    assert checker.main() == 1
    out = capsys.readouterr().out
    assert "Checked 0 Smart Notes + 1 governance triples." in out
    assert "0038-WHAT-NAYA-STANDS-FOR: AI form missing" in out
    assert "DAILY-LAW-REGISTRY" not in out
