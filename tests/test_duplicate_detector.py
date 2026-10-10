"""Tests for tools/duplicate_detector.py — Operating Code V2, Gate 7.

Covers: paraphrase recall, genuinely-new work, partial overlap, adversarial
decoys, self-match invariant, and registry failure modes (UNKNOWN != CLEAR).
"""

import json
import sys
from pathlib import Path

import pytest

from tools import duplicate_detector as detector

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = REPO_ROOT / "tools" / "solved_problem_registry.json"

WORK_PARAPHRASE_SP001 = (
    "before building, check the open PRs and the newest board comments "
    "for a conflicting claim on the same repair"
)
WORK_PARTIAL_SP002 = (
    "a gate that fails PRs containing dead code or duplicate symbol names"
)
WORK_PARAPHRASE_SP006 = "an activation gate for cold starts"
WORK_NEW = (
    "add voice playback to Intelligent Blocks so Naya reads answers aloud "
    "in her own voice on mobile"
)
WORK_VAGUE = (
    "tell me if a problem was already solved before I start coding"
)
WORK_DECOY = "build a dashboard showing PR cycle-time metrics for the team"


@pytest.fixture()
def entries():
    return detector.load_registry(REGISTRY)


def verdict(work, entries):
    flags, advisories = detector.scan(work, entries)
    return flags, advisories


def test_paraphrase_of_solved_problem_flags(entries):
    """SP-001 reworded without registry keywords still flags."""
    flags, _ = verdict(WORK_PARAPHRASE_SP001, entries)
    ids = [e["id"] for e, _ in flags]
    assert "SP-001" in ids


def test_partial_overlap_flags(entries):
    """Rebuilding one gate of a five-gate mechanism flags for review."""
    flags, _ = verdict(WORK_PARTIAL_SP002, entries)
    ids = [e["id"] for e, _ in flags]
    assert "SP-002" in ids


def test_reworded_gate_still_flags(entries):
    flags, _ = verdict(WORK_PARAPHRASE_SP006, entries)
    ids = [e["id"] for e, _ in flags]
    assert "SP-006" in ids


def test_genuinely_new_work_is_clear(entries):
    flags, advisories = verdict(WORK_NEW, entries)
    assert flags == []
    assert advisories == []


def test_vague_work_does_not_flag(entries):
    """'Tell me if it's solved' names no specific problem — no flag."""
    flags, _ = verdict(WORK_VAGUE, entries)
    assert flags == []


def test_decoy_vocabulary_does_not_flag(entries):
    """Generic shared words (PR, dashboard) must not reach the flag bar."""
    flags, _ = verdict(WORK_DECOY, entries)
    assert flags == []


def test_self_match_invariant(entries):
    """Every entry's own problem prose flags itself — the registry
    describes what it claims to describe."""
    for entry in entries:
        flags, _ = detector.scan(detector.entry_text(entry), entries)
        ids = [e["id"] for e, _ in flags]
        assert entry["id"] in ids, f"{entry['id']} does not flag its own prose"


def test_registry_schema_and_files_exist():
    data = json.loads(REGISTRY.read_text())
    assert data["version"] == 1
    problems = data["problems"]
    assert len(problems) >= 5
    ids = [p["id"] for p in problems]
    assert len(ids) == len(set(ids)), "duplicate entry ids"
    for p in problems:
        assert detector.REQUIRED_ENTRY_KEYS <= set(p), f"{p.get('id')} missing keys"
        canonical = REPO_ROOT / p["canonical"]
        assert canonical.exists(), f"{p['id']} canonical path missing: {p['canonical']}"


def test_missing_registry_is_environment_failure(tmp_path, capsys):
    code = detector.main(["--work", WORK_NEW, "--registry", str(tmp_path / "nope.json")])
    assert code == 3
    assert "ENVIRONMENT FAILURE" in capsys.readouterr().out


def test_corrupt_registry_is_environment_failure(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    code = detector.main(["--work", WORK_NEW, "--registry", str(bad)])
    assert code == 3


def test_registry_entry_missing_key_fails(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"problems": [{"id": "SP-999", "problem": "x" * 30}]}))
    with pytest.raises(RuntimeError, match="REGISTRY_SCHEMA"):
        detector.load_registry(bad)


def test_flag_exit_code(tmp_path, capsys):
    code = detector.main(["--work", WORK_PARAPHRASE_SP001, "--registry", str(REGISTRY)])
    assert code == 2
    out = capsys.readouterr().out
    assert "VERDICT: FLAG" in out
    assert "SP-001" in out


def test_clear_exit_code(capsys):
    code = detector.main(["--work", WORK_NEW, "--registry", str(REGISTRY)])
    assert code == 0
    assert "VERDICT: CLEAR" in capsys.readouterr().out


def test_default_registry_resolves_from_any_cwd(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    code = detector.main(["--work", WORK_NEW])
    assert code == 0  # default registry found next to the module
