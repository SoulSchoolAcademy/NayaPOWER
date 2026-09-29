import json
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("smart_note_v2", ROOT / "tools" / "smart_note_v2.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_general_capture_discovery_is_not_filename_hardcoded():
    assert mod.changed_capture(["README.md", ".naya/capture/ANY-NAME.json"]) == ".naya/capture/ANY-NAME.json"

def test_capture_discovery_fails_closed_on_batch():
    try:
        mod.changed_capture([".naya/capture/a.json", ".naya/capture/b.json"])
    except SystemExit as e:
        assert "BATCH_NOT_YET_SUPPORTED" in str(e)
    else:
        raise AssertionError("expected fail-closed batch rejection")

def test_machine_registry_contains_exact_private_block_pointer():
    reg = json.loads((ROOT / ".naya/memory/smart-notes/index.json").read_text())
    entry = next(e for e in reg["entries"] if e["intelligent_block_id"] == "IB-SMART-NOTE-20260929-b8f141805fa0d7ae")
    assert entry["scope"] == "PRIVATE"
    assert entry["smart_link_status"] == "PENDING_PRIVATE_PROJECTION"
    assert entry["provenance"]["receipt_id"] == "faa4345a-aacd-43f2-ab2f-a991b9681979"

def test_nia_language_has_primary_command_and_safe_ceiling():
    nia = json.loads((ROOT / "BRAIN/00-SPEC/NIA-LANGUAGE-INTENT-V1.json").read_text())
    assert nia["primary_capture_command"] == "Smart Note this"
    assert nia["primary_capture_intent"] == "CAPTURE_DURABLE_INTELLIGENCE"
    assert nia["maximum_automatic_capture_state"] == "CANDIDATE"
    assert nia["safety"]["may_grant_authority"] is False

def test_historical_checkpoint_binding_uses_object_local_receipt_semantics():
    reg = json.loads((ROOT / ".naya/memory/smart-notes/index.json").read_text())
    entry = next(e for e in reg["entries"] if e["intelligent_block_id"] == "IB-SMART-NOTE-20260929-b8f141805fa0d7ae")
    assert entry["provenance"]["checkpoint_semantics"] == "MUTABLE_PROJECT_STATE_POINTER"
    assert entry["provenance"]["historical_checkpoint_binding"] == "EXECUTION_RECEIPT_EVIDENCE"
    workflow = (ROOT / ".github/workflows/live-intelligence-commit-proof.yml").read_text()
    assert "RECEIPT_OBJECT_LOCAL_SNAPSHOT" in workflow

def test_smart_note_command_is_standing_authority_for_same_note_lifecycle():
    nia = (ROOT / "BRAIN/00-SPEC/0006-NIA-LANGUAGE-INTENT-CONTRACT-V1.md").read_text()
    assert "No second `DEPLOY` confirmation is required" in nia
    assert "One command, one complete Smart Note lifecycle" in nia
    assert "does **not** authorize unrelated product releases" in nia

def test_registered_smart_link_is_active_and_exact():
    reg = json.loads((ROOT / ".naya/memory/smart-notes/index.json").read_text())
    entry = next(e for e in reg["entries"] if e["intelligent_block_id"] == "IB-SMART-NOTE-20260929-b8f141805fa0d7ae")
    assert entry["smart_link_status"] == "ACTIVE"
    assert entry["projection_status"] == "LIVE_PRIVATE_VIEWER"
    assert entry["smart_link"].endswith("nayanet-smart-note-viewer?ib=IB-SMART-NOTE-20260929-b8f141805fa0d7ae")
    assert entry["canonical_brain_path"].endswith("/IB-SMART-NOTE-20260929-b8f141805fa0d7ae/smart-note.md")
