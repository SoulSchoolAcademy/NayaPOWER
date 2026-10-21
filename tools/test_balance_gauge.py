#!/usr/bin/env python3
"""Fixture tests for tools/balance_gauge.py (Balanced Machine §6).

Includes the negative control: a PR failing a CONTENT check must NOT
count as paperwork-blocked, even when a paperwork check also fails.
Run: python3 -m pytest tools/test_balance_gauge.py -q
"""
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import balance_gauge as bg  # noqa: E402

UTC = timezone.utc
TIP_FAILING = {"test", "promote-and-prove", "resolve-current-truth"}


def run(name, conclusion="failure", status="completed", started="2026-10-21T00:00:00Z", rid=1):
    return {"name": name, "conclusion": conclusion, "status": status,
            "started_at": started, "id": rid}


# --- paperwork-block rate -------------------------------------------------

def attr(head_failing, base_failing=TIP_FAILING):
    """Attributable set for a PR whose merge-base carries the tip reds."""
    return bg.attributable_failures(head_failing, base_failing)


def test_negative_control_content_failure_is_not_paperwork_blocked():
    # PR fails a paperwork gate AND a content check (completeness, not a
    # base red): the content failure is attributable => NOT paperwork-only.
    failing = attr({"Team review + scorecard receipt", "completeness"})
    assert bg.paperwork_blocked(failing) is False


def test_content_only_failure_is_not_paperwork_blocked():
    assert bg.paperwork_blocked(attr({"completeness"})) is False
    assert bg.paperwork_blocked(attr({"spec-integrity"})) is False


def test_paperwork_only_plus_inherited_base_reds_is_blocked():
    failing = attr({"Team review + scorecard receipt",
                    "Receipt gate (evidence or it didn't happen)", "test"})
    assert bg.paperwork_blocked(failing) is True


def test_receipt_pin_alone_is_blocked():
    assert bg.paperwork_blocked(attr({"Receipt pin — exact head SHA"})) is True


def test_no_failures_is_not_blocked():
    assert bg.paperwork_blocked(attr(set())) is False
    assert bg.paperwork_blocked(attr({"test"})) is False  # inherited only


def test_attributable_failures_subtracts_base_reds():
    assert bg.attributable_failures({"a", "b"}, {"a"}) == {"b"}
    assert bg.attributable_failures(set(), {"a"}) == set()


def test_absent_paperwork_checks_count_as_blocked():
    # Paperwork checks never ran at the head (expected-pending): the gate
    # is the blocker even with zero failing checks (audit: #2810/#2812).
    runs = [run("test", "success")]
    assert bg.paperwork_blocked(attr(set()), runs) is True


def test_satisfied_paperwork_is_not_blocked():
    runs = [run("Team review + scorecard receipt", "success"),
            run("Receipt gate (evidence or it didn't happen)", "success"),
            run("Receipt pin — exact head SHA", "success"),
            run("test", "success")]
    assert bg.paperwork_blocked(attr(set()), runs) is False


def test_pending_paperwork_counts_but_pending_content_does_not_disqualify():
    runs = [run("Team review + scorecard receipt", "failure"),
            run("Receipt gate (evidence or it didn't happen)", "success"),
            run("Receipt pin — exact head SHA", "success"),
            run("test", None, status="in_progress")]
    failing = attr({"Team review + scorecard receipt"})
    assert bg.paperwork_blocked(failing, runs) is True


def test_dirty_or_draft_is_never_paperwork_blocked():
    failing = attr({"Team review + scorecard receipt"})
    assert bg.paperwork_blocked(failing, [], mergeable_state="dirty") is False
    assert bg.paperwork_blocked(failing, [], draft=True) is False


def test_resolve_tip_failing_uses_ancestor_when_tip_pending():
    tip_runs = [run("test", None, status="in_progress"),
                run("build", "success")]
    parent_runs = [run("test", "failure"), run("build", "success")]
    assert bg.resolve_tip_failing([tip_runs, parent_runs]) == {"test"}
    # A name green at the tip stays green even if red at the parent.
    tip_green = [run("test", "success")]
    assert bg.resolve_tip_failing([tip_green, parent_runs]) == set()


def test_latest_per_name_wins():
    runs = [run("test", "success", started="2026-10-21T00:00:00Z", rid=1),
            run("test", "failure", started="2026-10-21T01:00:00Z", rid=2)]
    assert bg.failing_names(runs) == {"test"}
    runs.reverse()
    assert bg.failing_names(runs) == {"test"}
    ok = [run("test", "failure", started="2026-10-21T00:00:00Z", rid=1),
          run("test", "success", started="2026-10-21T01:00:00Z", rid=2)]
    assert bg.failing_names(ok) == set()


def test_pending_run_is_not_a_failure():
    assert bg.failing_names([run("test", None, status="in_progress")]) == set()


# --- tier classifier (audit-lane rules) ------------------------------------

def F(name, status="modified"):
    return {"filename": name, "status": status}


def test_tier_a_governance_and_workflows():
    assert bg.classify_tier([F("BRAIN/01-GOVERNANCE/0031-X.md")]) == "A"
    assert bg.classify_tier([F(".github/workflows/ci.yml")]) == "A"
    assert bg.classify_tier([F("tools/check_merge_consensus.py")]) == "A"
    assert bg.classify_tier([F("kernel/x.py"), F("AGENTS.md")]) == "A"


def test_tier_a_mass_deletion():
    files = [F(f"old/f{i}.py", "removed") for i in range(11)]
    assert bg.classify_tier(files) == "A"


def test_tier_c_note_and_index_and_doc():
    assert bg.classify_tier([F("BRAIN/05-MEMORY/SMART-NOTES/2026/10/21/SN-1.md")]) == "C"
    assert bg.classify_tier([F("BRAIN/NAYAPOWER-BRAIN-INDEX.json")]) == "C"
    assert bg.classify_tier([F("docs/some-guide.md")]) == "C"


def test_note_about_protocols_stays_c():
    # Content trees are excluded from keyword triggers (tier-audit.md):
    # a Smart Note *about* protocols is content, not law.
    assert bg.classify_tier(
        [F("BRAIN/05-MEMORY/SMART-NOTES/2026/10/21/SN-9-PROTOCOL-note.md")]) == "C"


def test_tier_b_mixed_code():
    assert bg.classify_tier([F("tools/some_tool.py")]) == "B"
    assert bg.classify_tier([F("tools/some_tool.py"), F("docs/x.md")]) == "B"


# --- time-to-merge median ---------------------------------------------------

def test_median():
    assert bg.median([]) is None
    assert bg.median([3.0]) == 3.0
    assert bg.median([1.0, 3.0, 2.0]) == 2.0
    assert bg.median([1.0, 2.0, 3.0, 4.0]) == 2.5


# --- escape proxy ------------------------------------------------------------

def _dt(day, hour=0):
    return datetime(2026, 10, day, hour, tzinfo=UTC)


def test_escape_proxy_matches_fix_reference_within_7d():
    merged = [{"number": 100, "merged_at": _dt(10)}]
    cands = [{"number": 101, "title": "fix: regression from #100", "body": "",
              "created_at": _dt(12)}]
    assert bg.escape_candidates(merged, cands) == {100}


def test_escape_proxy_rejects_stale_and_unrelated():
    merged = [{"number": 100, "merged_at": _dt(1)}]
    late = [{"number": 101, "title": "fix: late follow-up #100", "body": "",
             "created_at": _dt(20)}]
    assert bg.escape_candidates(merged, late) == set()
    plain = [{"number": 102, "title": "docs: mention #100", "body": "see #100",
              "created_at": _dt(2)}]
    assert bg.escape_candidates(merged, plain) == set()
    noref = [{"number": 103, "title": "fix: something else", "body": "",
              "created_at": _dt(2)}]
    assert bg.escape_candidates(merged, noref) == set()


def test_escape_proxy_revert_in_body_reference():
    merged = [{"number": 7, "merged_at": _dt(10, 6)}]
    cands = [{"number": 8, "title": "revert: bad merge", "body": "reverts #7",
              "created_at": _dt(10, 12)}]
    assert bg.escape_candidates(merged, cands) == {7}


# --- feed freshness ------------------------------------------------------------

def test_feed_newest_picks_max_created_at():
    html = ('{"created_at":"2026-10-21T10:00:00+00:00"}'
            '{"created_at":"2026-10-21T12:30:00+00:00"}'
            '{"created_at":"2026-10-20T09:00:00+00:00"}')
    newest, count = bg.feed_newest(html)
    assert count == 3
    assert newest == datetime(2026, 10, 21, 12, 30, tzinfo=UTC)


def test_feed_newest_empty():
    assert bg.feed_newest("<html>no notes</html>") == (None, 0)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"{len(fns)} tests passed")
