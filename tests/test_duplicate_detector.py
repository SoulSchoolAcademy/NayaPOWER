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
    assert data["version"] >= 1  # registry grows; pinning ==1 breaks every legitimate addition
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


# ---------------------------------------------------------------------------
# SP-009..SP-013 — drift_canary liveness/fairness seams (2026-10-11)
# Regression: a D22 liveness-qualifier rebuild got a false CLEAR before these
# entries existed (the builder caught it by manual seam search). These tests
# pin the fix: the same work description must now FLAG.
# ---------------------------------------------------------------------------

WORK_D22_NEAR_MISS = (
    "build a liveness-claim qualifier that judges whether claimed progress "
    "is genuine: safety vs liveness, activity vs progress, "
    "deadlock/livelock/starvation detection, waiting-state honesty, "
    "authority boundaries"
)
WORK_D23_PARAPHRASE = (
    "a well-founded measure that tells real progress from mere activity, "
    "counting only verified reductions in outstanding obligations"
)
WORK_D24_PARAPHRASE = (
    "prove fair scheduling without false progress: separate proofs for "
    "opportunity, service, and qualifying evidence"
)
WORK_D25_PARAPHRASE = (
    "when weak fairness is not enough — prevent starvation of work that "
    "flickers in and out of eligibility"
)
WORK_D26_PARAPHRASE = (
    "verify a liveness qualification by proving the three links separately "
    "with lasso classification over observations"
)
WORK_NEW_LIVENESS_ADJACENT = (
    "add voice playback to Intelligent Blocks so Naya reads answers aloud "
    "in her own voice on mobile"
)


def test_d22_near_miss_now_flags(entries):
    """The exact work description that false-CLEARed must FLAG SP-009."""
    flags, _ = verdict(WORK_D22_NEAR_MISS, entries)
    ids = [e["id"] for e, _ in flags]
    assert "SP-009" in ids
    canonicals = [e["canonical"] for e, _ in flags if e["id"] == "SP-009"]
    assert canonicals == ["drift_canary/liveness.py"]


def test_d23_paraphrase_flags(entries):
    flags, _ = verdict(WORK_D23_PARAPHRASE, entries)
    assert "SP-010" in [e["id"] for e, _ in flags]


def test_d24_paraphrase_flags(entries):
    flags, _ = verdict(WORK_D24_PARAPHRASE, entries)
    assert "SP-011" in [e["id"] for e, _ in flags]


def test_d25_paraphrase_flags(entries):
    flags, _ = verdict(WORK_D25_PARAPHRASE, entries)
    assert "SP-012" in [e["id"] for e, _ in flags]


def test_d26_paraphrase_flags(entries):
    flags, _ = verdict(WORK_D26_PARAPHRASE, entries)
    assert "SP-013" in [e["id"] for e, _ in flags]


def test_new_entries_do_not_overflag(entries):
    """Genuinely new work stays CLEAR after the registry grew 8 -> 13."""
    flags, advisories = verdict(WORK_NEW_LIVENESS_ADJACENT, entries)
    assert flags == []
    assert advisories == []


def test_new_entry_ids_unique_and_sequential(entries):
    ids = [e["id"] for e in entries]
    assert len(ids) == len(set(ids))
    for new_id in ("SP-009", "SP-010", "SP-011", "SP-012", "SP-013"):
        assert new_id in ids


def test_new_entries_point_at_real_files(entries):
    for e in entries:
        if e["id"] in ("SP-009", "SP-010", "SP-011", "SP-012", "SP-013"):
            assert (REPO_ROOT / e["canonical"]).is_file(), e["canonical"]
            assert "CODE-ONLY" in e["evidence"] or "extend this seam" in e["evidence"]
