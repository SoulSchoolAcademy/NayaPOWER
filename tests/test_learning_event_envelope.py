"""Tests for tools/learning_event_envelope.py — the canonical learning-event
envelope (issue #2244, requirement 3).

These tests exercise the real seams: deterministic idempotent issuance,
the enforced lifecycle, and the named-rejection gates. Negative controls
are first-class: a broken gate must FAIL, not silently pass.
"""

import json

import pytest

from tools.learning_event_envelope import (
    EVENT_TYPES,
    LEDGER_SCHEMA,
    LIFECYCLE,
    SCHEMA,
    SEVERITIES,
    EnvelopeError,
    EventNotFound,
    derive_event_id,
    get_event,
    issue_event,
    list_events,
    load_ledger,
    transition,
    validate_issue_fields,
)

SHA = "a" * 40


def _fields(**over):
    base = {
        "event_type": "failure",
        "severity": "HIGH",
        "title": "promotion wait-step died on skipped check",
        "source_artifact": "tools/learning_event_envelope.py",
        "source_sha": SHA,
        "expected": "wait step tolerates skipped placeholder checks",
        "actual": "wait step failed fast on skipped == failed",
        "owner": "naya-2",
        "impacted_teams": ["learn", "verify"],
        "next_action": "record event, share in specialty feed",
    }
    base.update(over)
    return base


@pytest.fixture()
def ledger(tmp_path):
    return tmp_path / "events.json"


# ---------------------------------------------------------------- issuance


def test_issue_minimal_valid(ledger):
    env, dup = issue_event(_fields(), ledger_path=ledger, issued_by="naya-2")
    assert dup is False
    assert env["schema"] == SCHEMA
    assert env["event_id"].startswith("evt-")
    assert env["lifecycle_state"] == "DETECTED"
    assert env["lesson_status"] == "PROPOSED"
    assert env["severity"] == "HIGH"
    assert env["impacted_teams"] == ["learn", "verify"]  # normalised + sorted
    assert len(env["history"]) == 1 and env["history"][0]["action"] == "ISSUED"
    # ledger persisted
    data = json.loads(ledger.read_text())
    assert data["schema"] == LEDGER_SCHEMA
    assert data["events"][env["event_id"]]["event_id"] == env["event_id"]


def test_issue_is_idempotent_same_failure_one_event(ledger):
    # #2244 acceptance: a material failure creates EXACTLY ONE idempotent event.
    env1, dup1 = issue_event(_fields(), ledger_path=ledger)
    env2, dup2 = issue_event(_fields(), ledger_path=ledger)
    assert dup1 is False and dup2 is True
    assert env1["event_id"] == env2["event_id"]
    ledger_data = load_ledger(ledger)
    assert len(ledger_data["events"]) == 1
    assert ledger_data["issued_count"] == 1
    # non-identity fields (next_action) do not fork the event
    env3, dup3 = issue_event(_fields(next_action="a different next step"), ledger_path=ledger)
    assert dup3 is True and env3["event_id"] == env1["event_id"]


def test_issue_different_failure_different_event(ledger):
    env1, _ = issue_event(_fields(), ledger_path=ledger)
    env2, dup2 = issue_event(_fields(actual="a materially different actual"), ledger_path=ledger)
    assert dup2 is False
    assert env1["event_id"] != env2["event_id"]
    assert len(load_ledger(ledger)["events"]) == 2


def test_issue_missing_required_field_rejected(ledger):
    fields = _fields()
    del fields["expected"]
    with pytest.raises(EnvelopeError, match="MISSING_FIELDS"):
        issue_event(fields, ledger_path=ledger)


def test_issue_bad_severity_rejected(ledger):
    with pytest.raises(EnvelopeError, match="BAD_SEVERITY"):
        issue_event(_fields(severity="CRITICAL!!"), ledger_path=ledger)


def test_issue_bad_event_type_rejected(ledger):
    with pytest.raises(EnvelopeError, match="BAD_EVENT_TYPE"):
        issue_event(_fields(event_type="vibe"), ledger_path=ledger)


def test_issue_bad_sha_rejected(ledger):
    with pytest.raises(EnvelopeError, match="BAD_SOURCE_SHA"):
        issue_event(_fields(source_sha="not-a-sha"), ledger_path=ledger)


def test_issue_empty_teams_rejected(ledger):
    with pytest.raises(EnvelopeError, match="EMPTY_IMPACTED_TEAMS"):
        issue_event(_fields(impacted_teams=[]), ledger_path=ledger)


def test_event_id_deterministic(ledger):
    # Same identity fields -> same ID regardless of issuance order or extras.
    id1 = derive_event_id(validate_issue_fields(_fields()))
    id2 = derive_event_id(validate_issue_fields(_fields(impacted_teams="verify, learn")))
    assert id1 == id2


def test_severity_order_and_types_sane():
    assert SEVERITIES == ("INFO", "NOTICE", "WARNING", "HIGH", "CRITICAL")
    for t in ("failure", "lesson", "blocker", "breakthrough", "material"):
        assert t in EVENT_TYPES


# ---------------------------------------------------------------- lifecycle


def _issued(ledger):
    env, _ = issue_event(_fields(), ledger_path=ledger, issued_by="naya-2")
    return env["event_id"]


def test_share_requires_feed_url(ledger):
    eid = _issued(ledger)
    with pytest.raises(EnvelopeError, match="MISSING_FEED_URL"):
        transition(eid, "SHARED", actor="naya-2", ledger_path=ledger)
    env = transition(eid, "SHARED", actor="naya-2", ledger_path=ledger,
                     feed_url="https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2235")
    assert env["lifecycle_state"] == "SHARED"
    assert env["specialty_feed_url"].endswith("/2235")


def test_illegal_transition_rejected(ledger):
    eid = _issued(ledger)
    # DETECTED -> RESOLVED skips the chain: must fail, loudly.
    with pytest.raises(EnvelopeError, match="ILLEGAL_TRANSITION"):
        transition(eid, "RESOLVED", actor="naya-2", ledger_path=ledger,
                   smart_note_id="SN-0001", smart_note_link="https://x",
                   regression_evidence="PR #1")


def test_unknown_event_rejected(ledger):
    with pytest.raises(EventNotFound, match="UNKNOWN_EVENT"):
        transition("evt-deadbeefdeadbeefdead", "SHARED", actor="naya-2", ledger_path=ledger)
    with pytest.raises(EventNotFound, match="UNKNOWN_EVENT"):
        get_event("evt-deadbeefdeadbeefdead", ledger_path=ledger)


def test_bad_target_state_rejected(ledger):
    eid = _issued(ledger)
    with pytest.raises(EnvelopeError, match="BAD_STATE"):
        transition(eid, "ARCHIVED", actor="naya-2", ledger_path=ledger)


def test_missing_actor_rejected(ledger):
    eid = _issued(ledger)
    with pytest.raises(EnvelopeError, match="MISSING_ACTOR"):
        transition(eid, "SHARED", actor="  ", ledger_path=ledger,
                   feed_url="https://github.com/x/issues/1")


def test_resolved_requires_note_or_explicit_no_lesson(ledger):
    eid = _issued(ledger)
    transition(eid, "SHARED", actor="naya-2", ledger_path=ledger,
               feed_url="https://github.com/x/issues/1")
    transition(eid, "ACKNOWLEDGED", actor="naya-4", ledger_path=ledger)
    # No note and no reason: rejected.
    with pytest.raises(EnvelopeError, match="MISSING_RESOLUTION"):
        transition(eid, "RESOLVED", actor="naya-4", ledger_path=ledger,
                   regression_evidence="PR #9")
    # Note without link: rejected.
    with pytest.raises(EnvelopeError, match="MISSING_NOTE_LINK"):
        transition(eid, "RESOLVED", actor="naya-4", ledger_path=ledger,
                   smart_note_id="SN-0001", regression_evidence="PR #9")
    # Explicit no-lesson path: accepted, status records the reason.
    env = transition(eid, "RESOLVED", actor="naya-4", ledger_path=ledger,
                     no_lesson_reason="one-off environment flake, no reusable lesson")
    assert env["lifecycle_state"] == "RESOLVED"
    assert env["lesson_status"] == "NONE_WITH_REASON"


def test_full_lifecycle_walk(ledger):
    eid = _issued(ledger)
    transition(eid, "SHARED", actor="naya-2", ledger_path=ledger,
               feed_url="https://github.com/x/issues/2235")
    transition(eid, "ACKNOWLEDGED", actor="naya-4", ledger_path=ledger)
    env = transition(eid, "RESOLVED", actor="naya-4", ledger_path=ledger,
                     smart_note_id="SN-0800",
                     smart_note_link="https://github.com/x/blob/main/BRAIN/SN-0800.md",
                     regression_evidence="PR #2300 green")
    assert env["lifecycle_state"] == "RESOLVED"
    assert env["lesson_status"] == "PROPOSED"  # not verified until behavior proof
    # PRESERVED without a note must fail — use a no-lesson event instead.
    eid2 = issue_event(_fields(title="one-off flake"), ledger_path=ledger)[0]["event_id"]
    for to, kw in (("SHARED", {"feed_url": "https://github.com/x/issues/1"}),
                   ("ACKNOWLEDGED", {})):
        transition(eid2, to, actor="naya-2", ledger_path=ledger, **kw)
    transition(eid2, "RESOLVED", actor="naya-2", ledger_path=ledger,
               no_lesson_reason="no reusable lesson")
    with pytest.raises(EnvelopeError, match="MISSING_NOTE_AT_PRESERVE"):
        transition(eid2, "PRESERVED", actor="naya-2", ledger_path=ledger)
    # The noted event continues to the end.
    transition(eid, "PRESERVED", actor="naya-4", ledger_path=ledger)
    with pytest.raises(EnvelopeError, match="MISSING_REUSE_EVIDENCE"):
        transition(eid, "REUSED", actor="naya-4", ledger_path=ledger)
    transition(eid, "REUSED", actor="naya-4", ledger_path=ledger,
               reuse_evidence="cold successor applied SN-0800 on held-out task 2026-10-11")
    with pytest.raises(EnvelopeError, match="MISSING_BEHAVIOR_PROOF"):
        transition(eid, "BEHAVIORALLY_VERIFIED", actor="naya-1", ledger_path=ledger)
    env = transition(eid, "BEHAVIORALLY_VERIFIED", actor="naya-1", ledger_path=ledger,
                     behavior_proof="independent receipt 6106000000: control/treatment delta observed")
    assert env["lifecycle_state"] == "BEHAVIORALLY_VERIFIED"
    assert env["lesson_status"] == "VERIFIED"
    # Terminal: nothing leaves BEHAVIORALLY_VERIFIED.
    with pytest.raises(EnvelopeError, match="ILLEGAL_TRANSITION"):
        transition(eid, "SHARED", actor="naya-2", ledger_path=ledger,
                   feed_url="https://github.com/x/issues/1")
    # History recorded every step: ISSUED + 6 transitions.
    assert len(env["history"]) == 7
    assert [h["to"] for h in env["history"][1:]] == list(LIFECYCLE[1:])


def test_list_filters_by_state(ledger):
    eid1 = _issued(ledger)
    env2, _ = issue_event(_fields(title="second event"), ledger_path=ledger)
    transition(eid1, "SHARED", actor="naya-2", ledger_path=ledger,
               feed_url="https://github.com/x/issues/1")
    assert [e["event_id"] for e in list_events(ledger, state="SHARED")] == [eid1]
    assert len(list_events(ledger)) == 2
    assert env2["event_id"] in [e["event_id"] for e in list_events(ledger, state="DETECTED")]


def test_ledger_round_trip(ledger):
    env, _ = issue_event(_fields(), ledger_path=ledger)
    reloaded = get_event(env["event_id"], ledger_path=ledger)
    assert reloaded == env
