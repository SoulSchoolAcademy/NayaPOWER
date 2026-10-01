"""Adversarial tests for the SUCCESSION handoff-verification spec (#864, thicken-domains).

The handoff verifier's job is to make the 08-SUCCESSION pipeline
machine-checkable: a stage claim is honored only when the evidence that
stage's gate requires is present. A section that is neither present nor
explicitly named as a gap is a fabrication risk, not an assumption;
proof-less intelligence is UNVERIFIED, never VERIFIED; a package never
manufactures authority; a continuity receipt that FAILs or that verifies
against the wrong canonical revision can never produce a transfer;
stale packages are rejected as stale. UNKNOWN != PASS.
"""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "validate_successor_handoff",
    ROOT / "tools" / "validate_successor_handoff.py",
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
failures = _mod.failures
STAGES = _mod.STAGES
SECTIONS = _mod.SECTIONS

FIXTURE = ROOT / "BRAIN/08-SUCCESSION/0002-SUCCESSOR-HANDOFF-VERIFICATION-V1.json"
BASIS_SHA = "507d34213333a38708912d343537985e619938ac"


def valid_record_at(stage, record_id="SHV-TEST-001"):
    idx = STAGES.index(stage)
    sections = {s: f"test content for {s}" for s in SECTIONS}
    rec = {
        "record_id": record_id,
        "stage": stage,
        "stage_history": STAGES[: idx + 1],
        "outcome": "ACTIVE",
        "sections": sections,
        "source_manifest": {s: f"canonical source for {s}" for s in SECTIONS},
        "self_describing": True,
        "gaps": [],
        "intelligence_items": [
            {
                "key": "test intelligence",
                "proof_state": "VERIFIED",
                "verification_ref": "test verification",
            }
        ],
        "authority_check": {
            "manufactures_authority": False,
            "note": "no authority created",
        },
        "fallback_mode": "FULL",
        "package_basis_sha": BASIS_SHA,
        "verification_receipt": None,
        "transfer_decision": None,
        "rejection_reason": None,
        "staleness_note": None,
    }
    if idx >= STAGES.index("CONTINUITY_VERIFY"):
        rec["verification_receipt"] = {
            "verified_against_sha": BASIS_SHA,
            "checks": ["section sources traced", "authority bound"],
            "result": "PASS",
            "verifier": "test verifier",
        }
    if stage == "TRANSFER":
        rec["outcome"] = "TRANSFERRED"
        rec["transfer_decision"] = {
            "outcome": "TRANSFERRED",
            "declared_at": "2026-10-01T00:00:00Z",
            "note": "test transfer",
        }
    return rec


@pytest.fixture()
def handoff():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def handoff_with(handoff, records):
    data = copy.deepcopy(handoff)
    data["records"] = records
    return data


def test_real_handoff_file_validates_green(handoff):
    assert failures(handoff) == []


def test_stage_skip_rejected(handoff):
    rec = valid_record_at("ASSEMBLE")
    rec["stage"] = "CONTINUITY_VERIFY"
    rec["stage_history"] = ["ASSEMBLE", "CONTINUITY_VERIFY"]
    fails = failures(handoff_with(handoff, [rec]))
    assert any("STAGE_HISTORY_INVALID" in f for f in fails)


def test_backward_transition_rejected(handoff):
    # A record that was at CONTINUITY_VERIFY cannot re-appear at ASSEMBLE:
    # the frozen history no longer matches the claimed stage.
    rec = valid_record_at("CONTINUITY_VERIFY")
    rec["stage"] = "ASSEMBLE"
    fails = failures(handoff_with(handoff, [rec]))
    assert any("STAGE_HISTORY_INVALID" in f for f in fails)


def test_unknown_stage_rejected(handoff):
    rec = valid_record_at("ASSEMBLE")
    rec["stage"] = "HANDOFF"
    fails = failures(handoff_with(handoff, [rec]))
    assert any("STAGE_INVALID" in f for f in fails)


def test_fractional_stage_rejected(handoff):
    rec = valid_record_at("AUTHORITY_BOUND")
    rec["stage"] = "AUTHORITY_BOUND.5"
    rec["stage_history"] = STAGES[: STAGES.index("AUTHORITY_BOUND") + 1]
    fails = failures(handoff_with(handoff, [rec]))
    assert any("STAGE_INVALID" in f for f in fails)


def test_terminal_outcome_before_transfer_rejected(handoff):
    rec = valid_record_at("COMPLETENESS_CHECK")
    rec["outcome"] = "TRANSFERRED"
    fails = failures(handoff_with(handoff, [rec]))
    assert any("OUTCOME_PREMATURE" in f for f in fails)


def test_transfer_without_terminal_outcome_rejected(handoff):
    rec = valid_record_at("TRANSFER")
    rec["outcome"] = "ACTIVE"
    rec["transfer_decision"]["outcome"] = "ACTIVE"
    fails = failures(handoff_with(handoff, [rec]))
    assert any("OUTCOME_MISSING" in f for f in fails)


def test_section_neither_present_nor_gapped_rejected(handoff):
    # An empty section with no named gap is a fabrication risk, not an
    # innocent omission.
    rec = valid_record_at("COMPLETENESS_CHECK")
    rec["sections"]["proof"] = None
    fails = failures(handoff_with(handoff, [rec]))
    assert any("SECTION_UNGAPPED_MISSING" in f for f in fails)


def test_explicit_gap_accepted(handoff):
    # The honest path: empty content + an explicit named gap passes the
    # completeness gate (the worked example in the fixture does this for
    # recent_outcomes).
    rec = valid_record_at("COMPLETENESS_CHECK")
    rec["sections"]["proof"] = None
    rec["gaps"] = [{"section": "proof", "reason": "proof records absent; see gap"}]
    fails = failures(handoff_with(handoff, [rec]))
    assert not any("SECTION_UNGAPPED_MISSING" in f for f in fails)
    assert not any("GAP_CONTENT_CONFLICT" in f for f in fails)


def test_gap_with_content_rejected(handoff):
    rec = valid_record_at("COMPLETENESS_CHECK")
    rec["gaps"] = [{"section": "proof", "reason": "listed as gap anyway"}]
    fails = failures(handoff_with(handoff, [rec]))
    assert any("GAP_CONTENT_CONFLICT" in f for f in fails)


def test_gap_without_reason_rejected(handoff):
    rec = valid_record_at("COMPLETENESS_CHECK")
    rec["sections"]["proof"] = None
    rec["gaps"] = [{"section": "proof", "reason": "   "}]
    fails = failures(handoff_with(handoff, [rec]))
    assert any("GAP_REASON_MISSING" in f for f in fails)


def test_source_manifest_incomplete_rejected(handoff):
    rec = valid_record_at("ASSEMBLE")
    del rec["source_manifest"]["identity"]
    fails = failures(handoff_with(handoff, [rec]))
    assert any("SOURCE_MANIFEST_INCOMPLETE" in f for f in fails)


def test_not_self_describing_rejected(handoff):
    rec = valid_record_at("ASSEMBLE")
    rec["self_describing"] = False
    fails = failures(handoff_with(handoff, [rec]))
    assert any("SELF_DESCRIBING_REQUIRED" in f for f in fails)


def test_authority_manufacture_rejected(handoff):
    # A successor package never manufactures authority: this is a hard
    # rejection, not a handoff record.
    rec = valid_record_at("AUTHORITY_BOUND")
    rec["authority_check"]["manufactures_authority"] = True
    fails = failures(handoff_with(handoff, [rec]))
    assert any("AUTHORITY_CLAIM_REJECTED" in f for f in fails)


def test_missing_authority_context_without_readonly_rejected(handoff):
    # Contract failure state: "authority context missing -> successor operates
    # in read-only mode". Missing context with FULL fallback fails closed.
    rec = valid_record_at("AUTHORITY_BOUND")
    rec["sections"]["authority_context"] = None
    rec["gaps"] = [
        {"section": "authority_context", "reason": "no authority context present"}
    ]
    fails = failures(handoff_with(handoff, [rec]))
    assert any("AUTHORITY_CONTEXT_MISSING_NO_FALLBACK" in f for f in fails)


def test_readonly_with_full_context_rejected(handoff):
    rec = valid_record_at("AUTHORITY_BOUND")
    rec["fallback_mode"] = "READ_ONLY"
    fails = failures(handoff_with(handoff, [rec]))
    assert any("FALLBACK_CONTRADICTS_CONTEXT" in f for f in fails)


def test_readonly_transfer_path_valid(handoff):
    # The full degraded path: no authority context, explicit gap, READ_ONLY
    # fallback, PASS receipt, TRANSFERRED_READ_ONLY verdict.
    rec = valid_record_at("TRANSFER")
    rec["sections"]["authority_context"] = None
    rec["gaps"] = [
        {
            "section": "authority_context",
            "reason": "authority context absent; successor is read-only",
        }
    ]
    rec["source_manifest"]["authority_context"] = "consulted export; absent — see gap"
    rec["fallback_mode"] = "READ_ONLY"
    rec["outcome"] = "TRANSFERRED_READ_ONLY"
    rec["transfer_decision"]["outcome"] = "TRANSFERRED_READ_ONLY"
    rec["transfer_decision"]["note"] = "read-only transfer; no actions permitted"
    fails = failures(handoff_with(handoff, [rec]))
    assert fails == []


def test_verified_intelligence_without_ref_rejected(handoff):
    rec = valid_record_at("COMPLETENESS_CHECK")
    rec["intelligence_items"] = [
        {"key": "claimed intel", "proof_state": "VERIFIED", "verification_ref": None}
    ]
    fails = failures(handoff_with(handoff, [rec]))
    assert any("VERIFIED_WITHOUT_REF" in f for f in fails)


def test_unverified_intelligence_marking_accepted(handoff):
    # Intelligence without proof records is UNVERIFIED — explicit and honest.
    rec = valid_record_at("COMPLETENESS_CHECK")
    rec["intelligence_items"] = [
        {"key": "unproven intel", "proof_state": "UNVERIFIED", "verification_ref": None}
    ]
    fails = failures(handoff_with(handoff, [rec]))
    assert not any("INTELLIGENCE" in f for f in fails)
    assert not any("VERIFIED" in f for f in fails)


def test_stale_receipt_basis_rejected(handoff):
    # The receipt verifies against a different revision than the package's
    # declared basis: the package is STALE, never transferred.
    rec = valid_record_at("CONTINUITY_VERIFY")
    rec["verification_receipt"]["verified_against_sha"] = "0" * 40
    fails = failures(handoff_with(handoff, [rec]))
    assert any("STALE_BASIS_MISMATCH" in f for f in fails)


def test_failed_continuity_cannot_transfer(handoff):
    # Contract failure state: "continuity verification fails -> halt".
    # A FAIL receipt recorded honestly can never yield TRANSFERRED.
    rec = valid_record_at("TRANSFER")
    rec["verification_receipt"]["result"] = "FAIL"
    fails = failures(handoff_with(handoff, [rec]))
    assert any("TRANSFER_WITHOUT_PASS" in f for f in fails)


def test_failed_continuity_can_reject(handoff):
    # The honest terminal path for a failed verification: REJECTED with a
    # reason (halt; alert the human director).
    rec = valid_record_at("TRANSFER")
    rec["verification_receipt"]["result"] = "FAIL"
    rec["outcome"] = "REJECTED"
    rec["transfer_decision"]["outcome"] = "REJECTED"
    rec["transfer_decision"]["note"] = "continuity verification failed; halting"
    rec["rejection_reason"] = "continuity verification failed; human director alerted"
    fails = failures(handoff_with(handoff, [rec]))
    assert fails == []


def test_stale_outcome_without_note_rejected(handoff):
    rec = valid_record_at("TRANSFER")
    rec["verification_receipt"]["verified_against_sha"] = "0" * 40
    rec["outcome"] = "STALE"
    rec["transfer_decision"]["outcome"] = "STALE"
    rec["staleness_note"] = None
    fails = failures(handoff_with(handoff, [rec]))
    assert any("STALE_NOTE_MISSING" in f for f in fails)


def test_rejected_without_reason_rejected(handoff):
    rec = valid_record_at("TRANSFER")
    rec["verification_receipt"]["result"] = "FAIL"
    rec["outcome"] = "REJECTED"
    rec["transfer_decision"]["outcome"] = "REJECTED"
    rec["rejection_reason"] = None
    fails = failures(handoff_with(handoff, [rec]))
    assert any("REJECTION_REASON_MISSING" in f for f in fails)


def test_decision_outcome_mismatch_rejected(handoff):
    rec = valid_record_at("TRANSFER")
    rec["transfer_decision"]["outcome"] = "REJECTED"
    fails = failures(handoff_with(handoff, [rec]))
    assert any("DECISION_OUTCOME_MISMATCH" in f for f in fails)


def test_duplicate_record_id_rejected(handoff):
    recs = [
        valid_record_at("ASSEMBLE", "SHV-DUP"),
        valid_record_at("COMPLETENESS_CHECK", "SHV-DUP"),
    ]
    fails = failures(handoff_with(handoff, recs))
    assert any("RECORD_ID_DUPLICATE" in f for f in fails)


def test_canonical_status_without_ratification_rejected(handoff):
    data = handoff_with(handoff, [valid_record_at("ASSEMBLE")])
    data["status"] = "CANONICAL"
    fails = failures(data)
    assert any("STATUS_NOT_PROPOSED_CANONICAL" in f for f in fails)


def test_as_of_must_be_pinned_sha(handoff):
    data = handoff_with(handoff, [valid_record_at("ASSEMBLE")])
    data["as_of"] = "main"
    fails = failures(data)
    assert any("AS_OF_NOT_PINNED_SHA" in f for f in fails)


def test_schema_mismatch_rejected(handoff):
    data = handoff_with(handoff, [valid_record_at("ASSEMBLE")])
    data["schema"] = "naya.other.v1"
    fails = failures(data)
    assert any("SCHEMA_MISMATCH" in f for f in fails)
