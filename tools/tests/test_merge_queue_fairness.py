#!/usr/bin/env python3
"""Tests for the merge-queue fairness wiring — Naya 2 WIRE LANE.

Every test uses REAL asserts against the REAL EligibilityProver and
FairnessDebtLedger (the wiring, not mocks). Negative controls sabotage a
predicate / the ledger and assert the suite then FAILS -- proving the tests
are not theater. If sabotage does not break the test, the test is vacuous
and must be rewritten, never weakened.
"""

import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import merge_queue_fairness as mqf
from merge_queue_fairness import (
    scan_queue,
    merge_queue_registry,
    VERDICT_LEVELS,
)
from fairness_debt import FairnessDebtLedger

FIXED_NOW = datetime(2026, 10, 11, 5, 30, tzinfo=timezone.utc)


def _iso(dt):
    return dt.isoformat()


def _hours_ago(h):
    return _iso(FIXED_NOW - timedelta(hours=h))


def _evidence(head="abc123def456abc123def456abc123def456abcd",
              author="Naya 2",
              scorecard_seat="Naya 4",
              scorecard_verdict=9.2,
              scorecard_at=None,
              scorecard_head_matches=True,
              review_seat="Naya 4",
              review_at=None,
              review_head_matches=True,
              checks=None,
              checks_present=True,
              checks_completed_at=None,
              known_red=None,
              intent=True):
    if checks is None:
        checks = [
            {"name": "test", "status": "completed", "conclusion": "success",
             "completed_at": checks_completed_at or _hours_ago(50)},
            {"name": "delivery-gate", "status": "completed",
             "conclusion": "success",
             "completed_at": checks_completed_at or _hours_ago(50)},
        ]
    return {
        "pr_number": 9001,
        "head_sha": head,
        "author_seat": author,
        "scorecard": {
            "seat": scorecard_seat,
            "head_matches": scorecard_head_matches,
            "verdict": scorecard_verdict,
            "merge_approved": True,
            "at": scorecard_at or _hours_ago(50),
        },
        "review": {
            "seat": review_seat,
            "head_matches": review_head_matches,
            "at": review_at or _hours_ago(49),
        },
        "check_runs": checks,
        "checks_evidence_present": checks_present,
        "known_red_checks": known_red or {},
        "intent_recorded": intent,
    }


def _item(pr=9001, evidence=None, **kw):
    d = {"pr_number": pr, "head_sha": "abc123", "author_seat": "Naya 2",
         "intent_recorded": True, "blocked_by": [], "parked": None,
         "evidence": evidence or _evidence()}
    d.update(kw)
    return d


def _queue(items):
    return {"mission_state_ref": "test", "queue": items}


# ---------------------------------------------------------------------------
# Eligibility: the five requirements, evidence-only
# ---------------------------------------------------------------------------

def test_01_fully_ready_pr_is_eligible():
    v = scan_queue(_queue([_item()]), now=FIXED_NOW)[0]
    assert v.eligible is True
    assert v.missing == []
    assert v.verdict_level in VERDICT_LEVELS


def test_02_low_scorecard_is_ineligible_and_accrues_no_debt():
    # #2188's shape: verdict 8.44 < 9.0. Correctly unserved is not starvation.
    ev = _evidence(scorecard_verdict=8.44, scorecard_at=_hours_ago(24 * 20))
    v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
    assert v.eligible is False
    assert "scorecard_meets_floor" in v.missing
    assert v.debt == 0
    assert v.violated is False
    assert v.witness is None


def test_03_review_on_wrong_head_fails():
    ev = _evidence(review_head_matches=False)
    v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
    assert v.eligible is False
    assert "cross_seat_review" in v.missing


def test_04_same_seat_review_fails():
    ev = _evidence(review_seat="Naya 2")  # author is Naya 2
    v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
    assert v.eligible is False
    assert "cross_seat_review" in v.missing


def test_05_scheduler_claim_contradiction_is_named():
    # Scheduler (labels) claims ready; evidence lacks review. Evidence wins.
    ev = _evidence(review_head_matches=False)
    item = _item(evidence=ev, scheduler_claim=True)
    v = scan_queue(_queue([item]), now=FIXED_NOW)[0]
    assert v.eligible is False
    assert v.claim_contradicted is True


def test_06_failing_check_blocks_eligibility():
    checks = [
        {"name": "test", "status": "completed", "conclusion": "failure",
         "completed_at": _hours_ago(50)},
    ]
    ev = _evidence(checks=checks)
    v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
    assert v.eligible is False
    assert "checks_green_on_head" in v.missing


def test_07_documented_known_red_is_excused():
    # The receipt-gate depth-1 bug shape: failing, but documented in evidence.
    checks = [
        {"name": "test", "status": "completed", "conclusion": "success",
         "completed_at": _hours_ago(50)},
        {"name": "Receipt gate (evidence or it didn't happen)",
         "status": "completed", "conclusion": "failure",
         "completed_at": _hours_ago(50)},
    ]
    known = {"Receipt gate (evidence or it didn't happen)":
             "depth-1 bug fixed by #2188; per mission state"}
    ev = _evidence(checks=checks, known_red=known)
    v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
    assert v.eligible is True
    assert "checks_green_on_head" not in v.missing


def test_08_checks_still_running_fails_closed():
    checks = [
        {"name": "test", "status": "in_progress", "conclusion": None,
         "completed_at": None},
    ]
    ev = _evidence(checks=checks)
    v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
    assert v.eligible is False
    assert "checks_green_on_head" in v.missing


def test_09_missing_intent_blocks_eligibility():
    ev = _evidence(intent=False)
    v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
    assert v.eligible is False
    assert "merge_intent_recorded" in v.missing


# ---------------------------------------------------------------------------
# Debt: starvation produces a falsifiable witness
# ---------------------------------------------------------------------------

def test_10_starved_eligible_pr_produces_witness():
    # Ready 5 days ago, still open: debt 5 > bound 3 -> VIOLATION.
    ev = _evidence(scorecard_at=_hours_ago(24 * 5), review_at=_hours_ago(24 * 5),
                   checks_completed_at=_hours_ago(24 * 5))
    v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
    assert v.eligible is True
    assert v.ready_since is not None
    assert v.debt == 5
    assert v.bound == 3
    assert v.violated is True
    assert v.witness is not None
    assert v.witness.item_id == "PR-9001"
    assert v.witness.debt == 5 and v.witness.bound == 3
    assert "PR-9001" in v.witness.describe()


def test_11_recently_ready_pr_accrues_no_violation():
    # Ready 30h ago: 1 complete window, debt 1 <= bound 3.
    ev = _evidence(scorecard_at=_hours_ago(30), review_at=_hours_ago(29))
    v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
    assert v.eligible is True
    assert v.debt == 1
    assert v.violated is False
    assert v.witness is None


def test_12_partial_window_never_accrues():
    # Ready 20h ago: 0 complete windows. A false alarm is worse than a late one.
    ev = _evidence(scorecard_at=_hours_ago(20), review_at=_hours_ago(19))
    v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
    assert v.debt == 0
    assert v.violated is False


def test_13_blocked_pr_accrues_no_debt():
    # #2201's shape: eligible but queued behind #2188. Legitimate, not starvation.
    ev = _evidence(scorecard_at=_hours_ago(24 * 10),
                   review_at=_hours_ago(24 * 10 - 1),
                   checks_completed_at=_hours_ago(24 * 10))
    item = _item(evidence=ev, blocked_by=[9004])
    v = scan_queue(_queue([item]), now=FIXED_NOW)[0]
    assert v.eligible is True
    assert v.debt == 0
    assert v.violated is False
    assert v.deferred_reason is not None and "9004" in v.deferred_reason


def test_14_parked_pr_accrues_no_debt():
    # Awaiting Shawn's word: the human gate, not starvation.
    ev = _evidence(scorecard_at=_hours_ago(24 * 10),
                   review_at=_hours_ago(24 * 10 - 1),
                   checks_completed_at=_hours_ago(24 * 10))
    item = _item(evidence=ev, parked={"reason": "awaiting Shawn's word"})
    v = scan_queue(_queue([item]), now=FIXED_NOW)[0]
    assert v.eligible is True
    assert v.debt == 0
    assert v.violated is False
    assert "parked" in (v.deferred_reason or "")


def test_15_missing_timestamps_widen_bound_no_false_witness():
    # Eligible but ready_since unprovable: bound widens, nothing accrues.
    ev = _evidence()
    ev["scorecard"] = dict(ev["scorecard"], at=None)
    v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
    assert v.eligible is True
    assert v.ready_since is None
    assert v.widenings == 1
    assert v.bound == 6  # 3 * 2^1
    assert v.debt == 0
    assert v.violated is False
    assert v.verdict_level == "FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS"


def test_16_all_verdicts_name_a_d26_level():
    items = [
        _item(pr=9001),  # eligible, recent
        _item(pr=9002, evidence=_evidence(scorecard_verdict=8.0)),  # ineligible
        _item(pr=9003, evidence=_evidence(scorecard_at=_hours_ago(24 * 9),
                                         review_at=_hours_ago(24 * 9 - 1)),
              blocked_by=[9001]),  # blocked
    ]
    for v in scan_queue(_queue(items), now=FIXED_NOW):
        assert v.verdict_level in VERDICT_LEVELS, v.pr_number


# ---------------------------------------------------------------------------
# Negative controls -- sabotage must break the suite (no theater)
# ---------------------------------------------------------------------------

def test_nc1_sabotaged_floor_always_true_must_create_witness():
    """Sabotage scorecard_meets_floor to always-True: the 8.44 PR must then
    become eligible AND, with 20 days ready, produce a witness. If it does
    not, the floor predicate is not actually gating."""
    reg = merge_queue_registry()
    orig = reg._predicates["scorecard_meets_floor"]
    reg._predicates["scorecard_meets_floor"] = lambda ev: (True, "sabotaged")
    try:
        import merge_queue_fairness as m
        orig_fn = m.merge_queue_registry
        m.merge_queue_registry = lambda: reg
        try:
            ev = _evidence(scorecard_verdict=8.44,
                           scorecard_at=_hours_ago(24 * 20),
                           review_at=_hours_ago(24 * 20 - 1),
                           checks_completed_at=_hours_ago(24 * 20))
            v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
        finally:
            m.merge_queue_registry = orig_fn
    finally:
        reg._predicates["scorecard_meets_floor"] = orig
    assert v.eligible is True, "sabotage did not take effect -- test is broken"
    assert v.violated is True, (
        "SABOTAGE NOT DETECTED: always-true floor did not produce a witness; "
        "the floor predicate may not be gating")


def test_nc2_broken_ledger_must_suppress_witness():
    """Sabotage the debt ledger to never accrue: the starved PR must then
    produce NO witness. Proves the witness depends on real accrual."""
    orig_record = FairnessDebtLedger.record_window

    def no_accrue(self, window_id, eligible, serviced, evidence_present=True):
        self._window_log.append({"window_id": window_id, "sabotaged": True})

    FairnessDebtLedger.record_window = no_accrue
    try:
        ev = _evidence(scorecard_at=_hours_ago(24 * 5),
                       review_at=_hours_ago(24 * 5 - 1),
                       checks_completed_at=_hours_ago(24 * 5))
        v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
    finally:
        FairnessDebtLedger.record_window = orig_record
    assert v.violated is False, (
        "SABOTAGE NOT DETECTED: witness fired without any debt accrual; "
        "the witness may not depend on the ledger")


def test_nc3_sabotaged_review_always_false_must_block():
    """Sabotage cross_seat_review to always-False: a fully-ready PR must
    become ineligible. Proves the review predicate is load-bearing."""
    reg = merge_queue_registry()
    orig = reg._predicates["cross_seat_review"]
    reg._predicates["cross_seat_review"] = lambda ev: (False, "sabotaged")
    try:
        import merge_queue_fairness as m
        orig_fn = m.merge_queue_registry
        m.merge_queue_registry = lambda: reg
        try:
            v = scan_queue(_queue([_item()]), now=FIXED_NOW)[0]
        finally:
            m.merge_queue_registry = orig_fn
    finally:
        reg._predicates["cross_seat_review"] = orig
    assert v.eligible is False, (
        "SABOTAGE NOT DETECTED: always-false review did not block eligibility")


# ---------------------------------------------------------------------------
# CLI: exit codes are the contract (0 clean / 1 violation / 2 fail-closed)
# ---------------------------------------------------------------------------

def _write_queue(tmp_path, queue):
    p = tmp_path / "q.json"
    p.write_text(json.dumps(queue))
    return str(p)


def _run_cli(*args):
    cmd = [sys.executable,
           os.path.join(os.path.dirname(__file__), "..", "merge_queue_fairness.py"),
           *args]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60)


def test_cli_clean_queue_exits_0(tmp_path):
    ev = _evidence(scorecard_at=_hours_ago(30), review_at=_hours_ago(29))
    qp = _write_queue(tmp_path, _queue([_item(evidence=ev)]))
    r = _run_cli("--queue", qp, "--now", _iso(FIXED_NOW))
    assert r.returncode == 0, r.stderr
    assert "0 violations" in r.stdout


def test_cli_starved_queue_exits_1_with_witness(tmp_path):
    ev = _evidence(scorecard_at=_hours_ago(24 * 5),
                   review_at=_hours_ago(24 * 5 - 1),
                   checks_completed_at=_hours_ago(24 * 5))
    qp = _write_queue(tmp_path, _queue([_item(evidence=ev)]))
    r = _run_cli("--queue", qp, "--now", _iso(FIXED_NOW), "--json")
    assert r.returncode == 1, r.stderr
    out = json.loads(r.stdout)
    assert out["verdicts"][0]["violated"] is True
    assert out["verdicts"][0]["witness"]["item_id"] == "PR-9001"


def test_cli_malformed_input_exits_2(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{not json")
    r = _run_cli("--queue", str(p))
    assert r.returncode == 2
    assert "SCAN ERROR" in r.stderr


def test_cli_missing_file_exits_2(tmp_path):
    r = _run_cli("--queue", str(tmp_path / "nope.json"))
    assert r.returncode == 2


# ---------------------------------------------------------------------------
# Latest-run-per-check semantics (regression: found live on #2188/#2201)
# ---------------------------------------------------------------------------

def test_17_old_failure_superseded_by_rerun_is_eligible():
    # GitHub semantics: the LATEST run per check name decides. A stale
    # failing run must not condemn the head.
    checks = [
        {"name": "test", "status": "completed", "conclusion": "failure",
         "completed_at": _hours_ago(60)},
        {"name": "test", "status": "completed", "conclusion": "success",
         "completed_at": _hours_ago(50)},
    ]
    ev = _evidence(checks=checks, checks_completed_at=_hours_ago(50))
    v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
    assert v.eligible is True
    assert "checks_green_on_head" not in v.missing


def test_18_latest_run_failing_still_blocks():
    checks = [
        {"name": "test", "status": "completed", "conclusion": "success",
         "completed_at": _hours_ago(60)},
        {"name": "test", "status": "completed", "conclusion": "failure",
         "completed_at": _hours_ago(50)},
    ]
    ev = _evidence(checks=checks, checks_completed_at=_hours_ago(50))
    v = scan_queue(_queue([_item(evidence=ev)]), now=FIXED_NOW)[0]
    assert v.eligible is False
    assert "checks_green_on_head" in v.missing


# ---------------------------------------------------------------------------
# Snapshot: live-format anchoring + fail loud on empty parse (L216)
# ---------------------------------------------------------------------------

import snapshot_merge_queue as smq

# Faithful miniature of the live #2154 "Right now (in order)" format
# (2026-10-11): numbered PR items + arrow-chain merge order + Parked section.
LIVE_SHAPE_BODY = """# CURRENT MISSION STATE — live

## Right now (in order)
1. **Tip `57e935c1` — red pending one merge.** Morning merge order: **#2293 → #2270 → #2188 (his word) → #2201 queues.**
2. **PR #2270 (Zero Value Law) — MERGE-READY, sequencing after #2293.**
3. **PR #2188 (receipt-gate fix) — VERIFICATION-COMPLETE, needs Shawn's word.** The gate re-ran on the review → FAILURE (stale).
4. **PR #2201 (spec/aer-live-3) — CONSENSUS-GREEN, queued behind #2188.**
5. **PR #2296 — MERGE-READY.** NO MERGE — Shawn pulls the trigger. **#2280 vs #2293 — recommend close-unmerged (his call).** #2279 + #2283 — merge-protocol conditions pending (his word). #2102 SUPERSEDED — recommend close-unmerged. PR #2231 (draft: failure-learning gate).

## Parked — Shawn's word only
- #2293 / #2270 merges (his word — morning order above). #2188 merge (8.44 < 9.0).
"""


def test_19_live_shape_parses_queue_with_annotations():
    chains = smq.extract_queue_chains(LIVE_SHAPE_BODY)
    prs = [p for p, _ in chains]
    assert prs == [2293, 2270, 2188, 2201, 2296, 2280, 2279, 2283, 2102, 2231], prs
    by_pr = dict(chains)
    assert "sequencing after #2293" in by_pr[2270]
    assert "his word" in by_pr[2188].lower()
    assert "queued behind #2188" in by_pr[2201]
    assert "pulls the trigger" in by_pr[2296]
    assert "close-unmerged" in by_pr[2280]      # subject of the "vs" clause
    assert "close-unmerged" not in by_pr[2293]  # comparison baseline untouched
    assert "SUPERSEDED" in by_pr[2102]
    assert "draft" in by_pr[2231].lower()
    # Prose arrows without PR refs ("review → FAILURE") contribute nothing.
    assert 2154 not in prs
    # The Parked section names its own (line granularity, like the old pass).
    assert smq.parked_from_parked_section(LIVE_SHAPE_BODY) == {2293, 2270, 2188}


def test_20_missing_section_fails_loud_not_silent(tmp_path, monkeypatch, capsys):
    # A #2154 body with no "Right now" section: the snapshot must exit 2 and
    # write NO file -- nothing downstream may scan an empty queue green.
    monkeypatch.setenv("GH_TOKEN", "test-token")
    monkeypatch.setattr(smq, "api_get", lambda path, token: {
        "body": "# CURRENT MISSION STATE\n## North Star\nNothing queued here.\n",
        "updated_at": "2026-10-11T06:13:19Z"})
    out = tmp_path / "q.json"
    rc = smq.main(["--out", str(out), "--mission-state", "2154"])
    assert rc == 2
    assert "queue parsed empty from #2154" in capsys.readouterr().err
    assert not out.exists()


def test_21_section_without_refs_fails_loud(tmp_path, monkeypatch, capsys):
    # Section present but zero PR refs: still an alarm, not a clean scan.
    monkeypatch.setenv("GH_TOKEN", "test-token")
    monkeypatch.setattr(smq, "api_get", lambda path, token: {
        "body": ("# CURRENT MISSION STATE\n## Right now (in order)\n"
                 "Nothing to merge today.\n\n## Parked\nNone.\n"),
        "updated_at": "2026-10-11T06:13:19Z"})
    out = tmp_path / "q.json"
    rc = smq.main(["--out", str(out), "--mission-state", "2154"])
    assert rc == 2
    assert "queue parsed empty from #2154" in capsys.readouterr().err
    assert not out.exists()


def test_22_lead_keeps_own_clause_subordinate_signals_do_not_leak():
    # Regression from the live proof: item 5's lead #2296 is MERGE-READY but
    # its item text mentions #2280/#2102 terminal subordinates. The lead's
    # annotation must be its own clause only -- "close-unmerged" belongs to
    # the subordinates, never to the lead.
    body = ("# MISSION\n## Right now (in order)\n"
            "5. **PR #2296 — MERGE-READY.** NO MERGE — Shawn pulls the trigger. "
            "**#2280 vs #2293 — recommend close-unmerged (his call).** "
            "#2102 SUPERSEDED — recommend close-unmerged.\n"
            "\n## Parked\nNone.\n")
    chains = smq.extract_queue_chains(body)
    by_pr = dict(chains)
    assert [p for p, _ in chains] == [2296, 2280, 2102]
    assert "pulls the trigger" in by_pr[2296]
    assert "close-unmerged" not in by_pr[2296]
    assert not smq.TERMINAL_RE.search(by_pr[2296])
    assert smq.TERMINAL_RE.search(by_pr[2280])
    assert smq.TERMINAL_RE.search(by_pr[2102])
