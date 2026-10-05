"""TDD guard for the Universal Worker Protocol learning decision.

A completion claim must explicitly record either CAPTURE or justified NO_CAPTURE.
This is the smallest existing handoff/completion seam; it must not create a
second learning system.
"""

def _handoff(completion: str) -> str:
    return f"""
## Current known reality
main at abc123, measured, exit 0.

## Current P0
close the bounded worker task.

## Next three actions
1. execute
2. verify
3. handoff

## Permanent constraints
no merge, no production.

## First action
execute the bounded task.

## Handoff completion
{completion}
"""


def test_completion_requires_explicit_learning_decision():
    from tools.worker_handoff import check_handoff

    res = check_handoff(_handoff("DONE; commit abc123; tests 12/12."))
    assert not res.accepted
    assert any("learning decision" in v.lower() for v in res.violations)


def test_capture_learning_decision_is_accepted():
    from tools.worker_handoff import check_handoff

    res = check_handoff(
        _handoff("DONE; commit abc123; tests 12/12; learning decision: CAPTURE.")
    )
    assert res.accepted, res.violations


def test_no_capture_learning_decision_is_accepted():
    from tools.worker_handoff import check_handoff

    res = check_handoff(
        _handoff(
            "DONE; commit abc123; tests 12/12; "
            "learning decision: NO_CAPTURE — no reusable material lesson."
        )
    )
    assert res.accepted, res.violations
