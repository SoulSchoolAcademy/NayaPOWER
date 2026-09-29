import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "BRAIN" / "04-INTELLIGENCE" / "SMART-NODE-PROTOCOL-V1.json"


def _manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_smart_node_is_alias_over_existing_intelligent_block_boundary():
    m = _manifest()
    assert m["status"] == "CANONICAL"
    assert m["canonical_machine_target"] == "INTELLIGENT_BLOCK"
    assert m["creates_new_object_type"] is False
    assert m["creates_new_kernel_node"] is False
    assert m["authority_inheritance"] is False


def test_proactive_capture_cannot_self_verify_or_widen_authority():
    m = _manifest()
    a = m["auto_capture"]
    assert a["enabled_as_candidate"] is True
    assert a["maximum_auto_truth_state"] == "CANDIDATE"
    assert a["requires_existing_write_authority"] is True
    assert a["may_widen_privacy"] is False
    assert a["may_self_promote"] is False


def test_cold_naya_loop_ends_in_handoff_and_preserves_verification():
    m = _manifest()
    loop = m["cold_naya_loop"]
    assert loop[0] == "VERIFY_CURRENT_MAIN"
    assert "ESTABLISH_AUTHORITY_AND_SCOPE" in loop
    assert "VERIFY" in loop
    assert "CAPTURE_NEW_DURABLE_INTELLIGENCE_IF_WARRANTED" in loop
    assert loop[-1] == "HANDOFF"


def test_proof_ladder_does_not_collapse_structure_into_compounding():
    m = _manifest()
    assert m["proof_ladder"] == [
        "STRUCTURED",
        "RETRIEVABLE",
        "APPLICABLE",
        "BEHAVIORALLY_USED",
        "OUTCOME_VERIFIED",
        "LEARNED",
        "COMPOUNDING",
    ]
