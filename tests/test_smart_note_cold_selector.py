from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "live-intelligence-commit-proof.yml"
REGISTRY = ROOT / ".naya" / "memory" / "smart-notes" / "index.json"


def test_cold_successor_uses_stable_smart_note_identity_not_stale_topic_alias():
    wf = WORKFLOW.read_text(encoding="utf-8")
    assert 'e.get("smart_note_id")=="SN-001"' in wf
    assert 'e.get("topic")=="SMART_NOTE_UNIVERSAL_CAPTURE"' not in wf
    assert 'IB-SMART-NOTE-20260929-b8f141805fa0d7ae' in wf


def test_registry_contains_exact_sn001_machine_identity():
    import json
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    matches = [e for e in reg["entries"] if e.get("smart_note_id") == "SN-001"]
    assert len(matches) == 1
    assert matches[0]["intelligent_block_id"] == "IB-SMART-NOTE-20260929-b8f141805fa0d7ae"
