"""Production Team Naya delivery writer must be gated before posting."""


def _handoff(done_line="evidence receipt; learning decision: CAPTURE."):
    return f"""## Current known reality
current production delivery.
## Current P0
route all delivery through the governed writer.
## Next three actions
1. validate
2. post
3. verify
## Permanent constraints
UNKNOWN/BLOCKED never PASS.
## First action
run governed delivery.
## Handoff completion
{done_line}
"""


def _sign_out(status="VERIFIED"):
    return {
        "seat": "NAYA-4",
        "did": "deliver Team Naya report",
        "evidence_links": ["delivery-evidence-001"],
        "score": 9.5,
        "proven": "delivery writer test",
        "unknown": "none",
        "blocked": "none",
        "next_action": "continue",
        "learning": {
            "topic": "Team Naya delivery",
            "action": "deliver Team Naya report",
            "ledger": [{
                "id": "DELIVERY-REPEAT-001",
                "directive_essence": "Team Naya deliveries must pass learning enforcement",
                "fix_status": status,
            }],
            "evidence_refs": ["delivery-evidence-001"],
            "authority_ref": "team-naya-test-authority",
            "timestamp": 1000,
        },
    }


def test_production_writer_refuses_unresolved_delivery_before_post():
    from tools.team_naya_delivery import deliver_team_naya_comment

    posted = []
    result = deliver_team_naya_comment(
        _handoff(), _sign_out("WIRED"), lambda body: posted.append(body)
    )
    assert not result.passed
    assert result.decision == "LEARNING_HOLD"
    assert posted == []


def test_production_writer_posts_only_after_verified_release():
    from tools.team_naya_delivery import deliver_team_naya_comment

    posted = []
    result = deliver_team_naya_comment(
        _handoff(), _sign_out("VERIFIED"), lambda body: posted.append(body)
    )
    assert result.passed
    assert result.decision == "PASS"
    assert len(posted) == 1


def test_production_writer_recurrence_passes_without_new_human_directive():
    from tools.team_naya_delivery import deliver_team_naya_comment

    posted = []
    result = deliver_team_naya_comment(
        _handoff(), _sign_out("VERIFIED"), lambda body: posted.append(body)
    )
    assert result.passed
    assert result.decision == "PASS"
    assert len(posted) == 1
