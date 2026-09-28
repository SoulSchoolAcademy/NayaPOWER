import json
from pathlib import Path


def test_independent_learning_influence_receipt():
    r = json.loads(Path("learning-influence-receipt.json").read_text(encoding="utf-8"))
    assert r["schema"] == "NAYANET_LEARNING_INFLUENCE_RUNTIME_V1"
    assert r["status"] == "PASS"
    assert r["target_id"] == "NAYA-NODE-0001"
    assert r["learning_level"] == "E5_CAN_TEACH"
    assert r["source_event_id"] == "NAYA-NODE-0001-APPLY"
    assert r["behavioral_change"] is True
    assert r["control_verified_value"] < r["treatment_verified_value"]
    assert r["fresh_session_decision"] == "USE_VERIFIED_LEARNING_CONTEXT"
    assert r["influenced"] is True
    assert r["learning_id"] == r["evidence_id_from_decision"]
