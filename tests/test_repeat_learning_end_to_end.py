"""End-to-end Repeat Tracker seam proof.

This test exercises the actual sign-out validator against a seeded unresolved
lesson, captures the LEARNING_HOLD receipt, releases after later behavioral
verification, and repeats the same task without a new human directive.
"""

from tools.protocol_gates import check_sign_out
from kernel.protocol.repeat_learning_gate import release_learning_hold


def _sign_out(entry, evidence):
    return {
        "seat": "NAYA-4",
        "did": "deliver report",
        "evidence_links": [evidence],
        "score": 9.5,
        "proven": "e2e seam test",
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


def test_seeded_repeat_is_held_with_full_receipt():
    entry = {
        "id": "E2E-REPEAT-001",
        "directive_essence": "delivery reports must include evidence and learning receipt",
        "fix_status": "WIRED",
    }
    result = check_sign_out(_sign_out(entry, "seed-evidence-001"))
    assert not result.passed
    assert len(result.receipts) == 1
    receipt = result.receipts[0]
    assert receipt.decision == "LEARNING_HOLD"
    assert receipt.directive_id == "E2E-REPEAT-001"
    assert receipt.evidence_refs == ("seed-evidence-001",)
    assert receipt.authority_ref == "team-naya-test-authority"


def test_verified_behavior_releases_hold():
    entry = {
        "id": "E2E-REPEAT-001",
        "directive_essence": "delivery reports must include evidence and learning receipt",
        "fix_status": "VERIFIED",
    }
    result = release_learning_hold(
        entry=entry,
        later_behavioral_evidence=["behavior-receipt-002"],
        timestamp=2000,
    )
    assert result.passed
    assert result.decision == "PASS"


def test_same_situation_passes_without_new_human_directive():
    entry = {
        "id": "E2E-REPEAT-001",
        "directive_essence": "delivery reports must include evidence and learning receipt",
        "fix_status": "VERIFIED",
    }
    result = check_sign_out(_sign_out(entry, "behavior-receipt-002"))
    assert result.passed
    assert result.reasons == []
