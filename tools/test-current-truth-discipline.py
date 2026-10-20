#!/usr/bin/env python3
"""Byte-check discipline test for tools/current_truth_resolver.py.

Honest remedy for the w596 DUPLICATES verdict (Naya Beta, 2026-10-20):
the resolver DUPLICATES the 0014 discipline in code rather than reading the
0014 contract file. These tests PIN the discipline's behavior against the
live bytes, so any drift — or the future fix that wires the resolver to the
contract — is a test-visible, deliberate change, not silent rot.

Every test runs resolve() against the live repo files at ROOT and asserts
behavior driven by the live-evidence packet, never on the file contents:
the discipline is what's pinned, not the data.
"""

import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import current_truth_resolver as ctr  # noqa: E402

ROOT = TOOLS.parent
# Tip pinned at write time (2026-10-20 ~10:37Z). The tests pass repo_head
# explicitly so the git backend is never exercised by assertions.
TIP = "6dc986716456b59e1878840614960d7c51fe941a"


def _active_issue() -> int:
    brain = json.loads(
        (ROOT / "BRAIN" / "NAYAPOWER-BRAIN-INDEX.json").read_text(encoding="utf-8")
    )
    return int(brain["operations"]["active_issue"])


def _full_live(repo_head: str) -> dict:
    issue = _active_issue()
    return {
        "main_head": repo_head,
        "production_branch_head": repo_head,
        "issue_states": {str(issue): "OPEN"},
        "open_prs": [],
        "latest_successful_runtime_proof": {"head_sha": repo_head},
        "live_runtime_source": repo_head,
    }


def test_precedence_list_pinned():
    """The resolver's source-precedence ladder is pinned, in order."""
    result = ctr.resolve({}, repo_head=TIP)
    assert result["source_precedence"] == [
        "live_git_main",
        "live_runtime_or_deployment_evidence",
        "current_authority",
        "persisted_proof_receipts",
        "canonical_repository_contracts",
        "dated_projections",
    ]


def test_projection_only_discipline():
    """Projection-only authority marker is always present."""
    result = ctr.resolve({}, repo_head=TIP)
    assert result["projection_only"] is True
    assert "Derived projection only" in result["authority_note"]
    assert result["schema"] == "naya.current-truth-resolution.v1"


def test_fail_closed_on_checkout_conflict():
    """Checkout head != live main head -> CONFLICT (fail closed)."""
    live = _full_live(TIP)
    live["main_head"] = "0" * 40
    result = ctr.resolve(live, repo_head=TIP)
    assert result["status"] == "CONFLICT"
    codes = [c["code"] for c in result["hard_conflicts"]]
    assert "CHECKOUT_NOT_LIVE_MAIN" in codes


def test_unknowns_preserved_when_evidence_absent():
    """Absent live evidence -> explicit UNKNOWN keys, never silent defaults."""
    result = ctr.resolve({}, repo_head=TIP)
    assert result["status"] == "RESOLVED_WITH_UNKNOWNS"
    for key in (
        "LIVE_MAIN_HEAD",
        "ACTIVE_ISSUE_STATE",
        "LATEST_SUCCESSFUL_RUNTIME_PROOF_SOURCE",
        "LIVE_RUNTIME_SOURCE",
    ):
        assert key in result["unknowns"], f"UNKNOWN lost: {key}"


def test_full_evidence_has_no_hard_conflicts():
    """A fully-evidenced packet never produces a hard conflict."""
    result = ctr.resolve(_full_live(TIP), repo_head=TIP)
    assert result["hard_conflicts"] == []
    assert result["status"] in ("RESOLVED", "RESOLVED_WITH_UNKNOWNS")


def test_fail_on_conflict_exit_code(tmp_path, monkeypatch):
    """--fail-on-conflict exits 2 on hard conflicts (fail-closed CLI)."""
    live = _full_live(TIP)
    live["main_head"] = "0" * 40
    evidence = tmp_path / "live.json"
    evidence.write_text(json.dumps(live), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["current_truth_resolver.py", "--live-evidence", str(evidence), "--fail-on-conflict"],
    )
    # resolve() falls back to `git -C ROOT rev-parse HEAD`; the clone root
    # matches the resolver's ROOT so the call is valid here.
    assert ctr.main() == 2


def test_discipline_duplicated_not_read_from_0014():
    """Documents the w596 DUPLICATES verdict: the resolver hardcodes the
    discipline; it does NOT read the 0014 contract file. If the resolver is
    ever wired to the contract, THIS test is the one to update — that change
    must be deliberate, not drift."""
    src = (TOOLS / "current_truth_resolver.py").read_text(encoding="utf-8")
    assert "0014" not in src
    assert ".machine.json" not in src
    result = ctr.resolve({}, repo_head=TIP)
    # 'canonical_repository_contracts' is a precedence LABEL here, not a read.
    assert "canonical_repository_contracts" in result["source_precedence"]
