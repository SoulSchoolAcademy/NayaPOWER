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
    assert entry["smart_link_status"] == "ACTIVE"
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
    assert entry["projection_status"] == "GITHUB_BRAIN_PUBLISHED"
    assert entry["smart_link"].startswith("https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/BRAIN/05-MEMORY/SMART-NOTES/")
    assert entry["smart_note_id"] == "SN-001"
    assert entry["canonical_brain_path"].endswith("/SN-001/IB-SMART-NOTE-20260929-b8f141805fa0d7ae.md")

def test_human_smart_note_projection_lives_in_brain_memory_hierarchy():
    entry_path = ROOT / "BRAIN/05-MEMORY/SMART-NOTES/2026/09/29/SYSTEM-INTELLIGENCE/SMART-NOTE-SYSTEM/OFFICIAL-SMART-NOTE-FORMAT/SN-001/IB-SMART-NOTE-20260929-b8f141805fa0d7ae.md"
    assert entry_path.exists()
    text = entry_path.read_text()
    for section in [
        "IN A NUTSHELL", "HUMAN NOTE", "CHILD NOTE", "GRANDMA NOTE", "NAYA NOTE",
        "MACHINE NOTE", "LEARNING LESSON", "WHAT IT MEANS", "WHAT'S IN IT FOR YOU",
        "HOW TO APPLY / HOW TO USE", "HOW IT CONNECTS", "PROOF / PROVENANCE", "TRUTH BOUNDARY"
    ]:
        assert section in text
    assert "IB-SMART-NOTE-20260929-b8f141805fa0d7ae" in text

def test_projection_generator_targets_brain_and_preserves_private_default():
    assert "BRAIN_SMART_NOTE_ROOT" in mod.__dict__
    assert str(mod.BRAIN_SMART_NOTE_ROOT).endswith("BRAIN/05-MEMORY/SMART-NOTES")
    private_capture = {
        "source": {"captured_at": "2026-09-29"},
        "category": "SYSTEM_INTELLIGENCE",
        "topic": "SMART_NOTE_SYSTEM",
        "subtopic": "OFFICIAL_FORMAT",
        "projection": {}
    }
    p = mod.projection_path(private_capture, "IB-TEST")
    assert "BRAIN/05-MEMORY/SMART-NOTES/2026/09/29" in str(p).replace("\\", "/")
    assert "/SN-" in str(p).replace("\\", "/")

def test_sn002_is_registered_to_live_canonical_runtime():
    reg = json.loads((ROOT / ".naya/memory/smart-notes/index.json").read_text())
    entry = next(e for e in reg["entries"] if e.get("smart_note_id") == "SN-002")
    assert entry["intelligent_block_id"] == "IB-SMART-NOTE-20260929-sn002-smart-note-node-flow"
    assert entry["provenance"]["receipt_id"] == "102d900e-1dc0-44ce-bde4-9d8d668f4d60"
    assert entry["proven_relationship"]["source_id"] == "NAYA-KERNEL-KNOW"
    assert entry["proven_relationship"]["relationship_type"] == "PRODUCES"
    assert entry["proof_boundary"]["universal_nine_node_binding"] == "NOT_PROVEN"

def test_sequence_policy_advances_after_sn002():
    reg = json.loads((ROOT / ".naya/memory/smart-notes/index.json").read_text())
    assert reg["sequence_policy"]["next_sequence"] == 4
    assert mod.allocate_smart_note_id({"source":{"captured_at":"2026-09-29"}}, "IB-NEW") == "SN-004"


def test_projection_workflow_publishes_active_verified_public_projection():
    workflow = (ROOT / ".github/workflows/live-intelligence-commit-proof.yml").read_text()
    assert 'e.get("smart_link_status") in {"ACTIVE", "READY"}' in workflow
    assert 'e.get("smart_link_status")=="READY"' not in workflow


def test_projection_workflow_does_not_allocate_intelligent_block_identity():
    workflow = (ROOT / ".github/workflows/live-intelligence-commit-proof.yml").read_text()
    assert 'ib="IB-SMART-NOTE-"+capture["capture_id"]' not in workflow
    assert '"intelligent_block_id"' in workflow


def test_projection_workflow_stages_brain_projection_and_registry():
    workflow = (ROOT / ".github/workflows/live-intelligence-commit-proof.yml").read_text()
    assert "git add BRAIN/05-MEMORY/SMART-NOTES .naya/memory/smart-notes" in workflow


def test_sequence_policy_advances_past_sn003():
    reg = json.loads((ROOT / ".naya/memory/smart-notes/index.json").read_text())
    assert reg["sequence_policy"]["next_sequence"] == 4
    assert mod.allocate_smart_note_id({"source":{"captured_at":"2026-09-29"}}, "IB-NEW") == "SN-004"
