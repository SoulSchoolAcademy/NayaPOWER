"""Real Team Naya handoff/sign-out execution seam proof."""


def _handoff():
    return """
## Current known reality
repeat-learning gate wired, seed is unresolved.

## Current P0
refuse premature completion.

## Next three actions
1. hold
2. repair
3. verify

## Permanent constraints
UNKNOWN/BLOCKED never PASS.

## First action
attempt the real handoff.

## Handoff completion
LEARNING_HOLD; test receipt recorded; learning decision: CAPTURE.
"""


def _sign_out(entry, evidence):
    return {
        "seat": "NAYA-4",
        "did": "deliver report",
        "evidence_links": [evidence],
        "score": 9.5,
        "proven": "real Team Naya handoff seam test",
        "unknown": "none",
        "blocked": "none",
        "next_action": "continue",
        "learning": {
            "topic": "delivery reports",
            "action": "deliver report",
            "ledger": [entry],
            "evidence_refs": [evidence],
            "authority_ref": "team-naya-test-authority",
            "timestamp": 1000,
        },
    }


def test_team_naya_execution_refuses_unresolved_repeat_with_hold_receipt():
    from tools.worker_handoff import execute_team_naya_handoff

    entry = {
        "id": "REAL-PATH-REPEAT-001",
        "directive_essence": "delivery reports must include evidence and learning receipt",
        "fix_status": "WIRED",
    }
    result = execute_team_naya_handoff(_handoff(), _sign_out(entry, "seed-real-001"))
    assert not result.passed
    assert result.decision == "LEARNING_HOLD"
    assert result.receipts[0].directive_id == "REAL-PATH-REPEAT-001"


def test_team_naya_execution_releases_after_verified_behavior_and_recurs_without_directive():
    from tools.worker_handoff import execute_team_naya_handoff

    entry = {
        "id": "REAL-PATH-REPEAT-001",
        "directive_essence": "delivery reports must include evidence and learning receipt",
        "fix_status": "VERIFIED",
    }
    result = execute_team_naya_handoff(_handoff(), _sign_out(entry, "behavior-real-002"))
    assert result.passed
    assert result.decision == "PASS"
    recurrence = execute_team_naya_handoff(_handoff(), _sign_out(entry, "recurrence-real-003"))
    assert recurrence.passed
    assert recurrence.decision == "PASS"
