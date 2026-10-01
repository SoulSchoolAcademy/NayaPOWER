"""Adversarial tests for the SELF organ machine contract (self-machine-contract).

The contract's job is to make SELF machine-checkable: a state claim is
honored only when the evidence its gate requires is present. Identity is
established, never inferred; continuity is bound, never assumed; successor
packets transfer intelligence, never authority; missing or corrupt
continuity fails closed. UNKNOWN != PASS.
"""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "validate_self_machine_contract",
    ROOT / "tools" / "validate_self_machine_contract.py",
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
failures = _mod.failures
STAGES = _mod.STAGES

FIXTURE = ROOT / "BRAIN/03-KERNEL/NODES/SELF/0003-SELF-MACHINE-CONTRACT-V1.json"


def valid_record_at(stage, record_id="SELF-TEST-001"):
    idx = STAGES.index(stage)
    return {
        "record_id": record_id,
        "loop_stage": stage,
        "stage_history": STAGES[: idx + 1],
        "identity_attestation": {
            "actor_id": "naya-2",
            "system_id": "NayaPOWER",
            "role": "naya",
        },
        "mission_source": "canonical constitution / human-director directive",
        "objective": "test objective",
        "continuity_binding": {"checkpoint_id": "CHK-" + "a1" * 12},
        "known_unknown_boundary": {"known": ["k1"], "unknown": ["u1"], "blocked": []},
        "experience_preserved": True,
        "experience_ref": "observed outcome retained",
        "audit_trail": ["changed x because y"],
        "checkpoint_id": "CHK-" + "b2" * 12,
        "successor_packet": {
            "schema": "naya.self.successor.v2",
            "predecessor_id": "naya-1",
            "system_id": "NayaPOWER",
            "authority_transferred": False,
        },
        "inherited_intelligence": ["lesson from predecessor"],
        "proof_ref": "boot receipt verified",
    }


@pytest.fixture()
def contract():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def contract_with(contract, records):
    data = copy.deepcopy(contract)
    data["records"] = records
    return data


def test_real_contract_file_validates_green(contract):
    assert failures(contract) == []


def test_loop_order_mismatch_rejected(contract):
    data = copy.deepcopy(contract)
    data["loop_stages"] = list(reversed(STAGES))
    fails = failures(data)
    assert any("LOOP_ORDER_MISMATCH" in f for f in fails)


def test_stage_skip_rejected(contract):
    rec = valid_record_at("ESTABLISH")
    rec["loop_stage"] = "REMEMBER"
    rec["stage_history"] = ["ESTABLISH", "REMEMBER"]
    fails = failures(contract_with(contract, [rec]))
    assert any("STAGE_HISTORY_INVALID" in f for f in fails)


def test_backward_transition_rejected(contract):
    rec = valid_record_at("PRESERVE")
    rec["loop_stage"] = "REMEMBER"
    fails = failures(contract_with(contract, [rec]))
    assert any("STAGE_HISTORY_INVALID" in f for f in fails)


def test_status_canonical_rejected(contract):
    data = copy.deepcopy(contract)
    data["status"] = "CANONICAL"
    fails = failures(data)
    assert any("STATUS_NOT_PROPOSED_CANONICAL" in f for f in fails)


def test_as_of_must_be_pinned_sha(contract):
    data = copy.deepcopy(contract)
    data["as_of"] = "main"
    fails = failures(data)
    assert any("AS_OF_NOT_PINNED_SHA" in f for f in fails)


def test_establish_without_attestation_rejected(contract):
    rec = valid_record_at("ESTABLISH")
    del rec["identity_attestation"]
    fails = failures(contract_with(contract, [rec]))
    assert any("ESTABLISH_EVIDENCE_MISSING" in f for f in fails)


def test_fabricated_identity_rejected(contract):
    rec = valid_record_at("ESTABLISH")
    rec["identity_attestation"]["actor_id"] = "   "
    fails = failures(contract_with(contract, [rec]))
    assert any("IDENTITY_MISSING" in f for f in fails)


def test_identity_never_inferred_from_display_name(contract):
    rec = valid_record_at("ESTABLISH")
    rec["identity_attestation"]["role"] = "superuser"
    fails = failures(contract_with(contract, [rec]))
    assert any("ROLE_INVALID" in f for f in fails)


def test_invented_mission_rejected(contract):
    rec = valid_record_at("ESTABLISH")
    rec["mission_source"] = ""
    fails = failures(contract_with(contract, [rec]))
    assert any("ESTABLISH_EVIDENCE_MISSING" in f for f in fails)


def test_operation_without_objective_rejected(contract):
    rec = valid_record_at("ESTABLISH")
    rec["objective"] = ""
    fails = failures(contract_with(contract, [rec]))
    assert any("OBJECTIVE_MISSING" in f for f in fails)


def test_restore_without_continuity_binding_rejected(contract):
    rec = valid_record_at("RESTORE")
    del rec["continuity_binding"]
    fails = failures(contract_with(contract, [rec]))
    assert any("RESTORE_EVIDENCE_MISSING" in f for f in fails)


def test_assumed_continuity_rejected(contract):
    # A checkpoint that is not content-addressed is not a binding.
    rec = valid_record_at("RESTORE")
    rec["continuity_binding"] = {"checkpoint_id": "latest"}
    fails = failures(contract_with(contract, [rec]))
    assert any("CONTINUITY_UNBOUND" in f for f in fails)


def test_understand_boundary_must_be_explicit(contract):
    rec = valid_record_at("UNDERSTAND")
    del rec["known_unknown_boundary"]["blocked"]
    fails = failures(contract_with(contract, [rec]))
    assert any("BOUNDARY_NOT_EXPLICIT" in f for f in fails)


def test_checkpoint_must_be_content_addressed(contract):
    rec = valid_record_at("PRESERVE")
    rec["checkpoint_id"] = "CHK-notahash"
    fails = failures(contract_with(contract, [rec]))
    assert any("CHECKPOINT_NOT_CONTENT_ADDRESSED" in f for f in fails)


def test_handoff_with_authority_transfer_rejected(contract):
    # Successor packets transfer intelligence, never authority.
    rec = valid_record_at("HAND_OFF")
    rec["successor_packet"]["authority_transferred"] = True
    fails = failures(contract_with(contract, [rec]))
    assert any("AUTHORITY_CLAIM_REJECTED" in f for f in fails)


def test_handoff_packet_schema_mismatch_rejected(contract):
    rec = valid_record_at("HAND_OFF")
    rec["successor_packet"]["schema"] = "naya.self.successor.v9"
    fails = failures(contract_with(contract, [rec]))
    assert any("SUCCESSOR_PACKET_SCHEMA_MISMATCH" in f for f in fails)


def test_continue_without_proof_ref_rejected(contract):
    rec = valid_record_at("CONTINUE")
    rec["proof_ref"] = ""
    fails = failures(contract_with(contract, [rec]))
    assert any("CONTINUE_EVIDENCE_MISSING" in f for f in fails)


def test_duplicate_record_id_rejected(contract):
    rec = valid_record_at("ESTABLISH", record_id="DUP")
    fails = failures(contract_with(contract, [copy.deepcopy(rec), rec]))
    assert any("RECORD_ID_DUPLICATE" in f for f in fails)


def test_transition_to_unknown_state_rejected(contract):
    data = copy.deepcopy(contract)
    data["state_machine"]["legal_transitions"].append(
        {"from": "READY", "to": "ASCENDED", "on": "nothing"}
    )
    fails = failures(data)
    assert any("TRANSITION_UNKNOWN_STATE" in f for f in fails)


def test_invariants_must_be_twelve(contract):
    data = copy.deepcopy(contract)
    data["invariants"] = data["invariants"][:11]
    fails = failures(data)
    assert any("INVARIANTS_NOT_TWELVE" in f for f in fails)


def test_roles_must_match_schema(contract):
    data = copy.deepcopy(contract)
    data["roles"] = ["naya", "human", "agent", "service", "admin"]
    fails = failures(data)
    assert any("ROLES_MISMATCH" in f for f in fails)


def test_error_codes_must_bind_executor_vocabulary(contract):
    data = copy.deepcopy(contract)
    data["merged_executor_vocabulary"]["error_codes"] = []
    fails = failures(data)
    assert any("ERROR_CODES_MISSING" in f for f in fails)


def test_missing_required_section_rejected(contract):
    data = copy.deepcopy(contract)
    del data["fail_closed_law"]
    fails = failures(data)
    assert any("REQUIRED_SECTIONS_MISSING" in f for f in fails)


def test_empty_records_list_is_valid(contract):
    # An empty records list is honest: no invented worked examples.
    assert failures(contract_with(contract, [])) == []
