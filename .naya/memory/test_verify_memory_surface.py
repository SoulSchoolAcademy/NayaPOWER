from pathlib import Path
import sys
import json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/".naya/memory"))
import verify_memory_surface
def test_canonical_memory_surface():
    errors = verify_memory_surface.verify()
    assert errors
    assert all("retrieval boundary remains UNKNOWN" in error for error in errors if "authorization metadata incomplete" in error)

def test_retrieval_manifest_names_canonical_ib_store():
    import json
    manifest = json.loads((ROOT / ".naya/memory/RETRIEVAL-MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["canonical_primary_store"] == ".naya/memory/smart-notes/"
    assert manifest["canonical_registry"] == ".naya/memory/smart-notes/REGISTRY.json"
    assert manifest["event_lineage_store"] == ".naya/memory/events/"

def test_legacy_v2_schema_is_quarantined():
    assert not (ROOT / ".naya/memory/note.schema.json").exists()
    assert (ROOT / ".naya/memory/archive/legacy-pre-2026-09-25/note.schema.v2-legacy.json").exists()


def test_cold_restore_uses_canonical_ib_runtime():
    restore = (ROOT / ".naya" / "runtime" / "restore_context.py").read_text(encoding="utf-8")
    assert "from smart_notes_v3 import" in restore
    assert "memory_runtime" not in restore
    assert "retrieve_canonical_ibs(" in restore

def test_active_memory_surface_cannot_reintroduce_local_ib_allocation_or_legacy_registry():
    active_files = [
        path for path in (ROOT / ".naya" / "memory").iterdir()
        if path.is_file() and path.name not in {"verify_memory_surface.py", "test_verify_memory_surface.py"}
    ]
    forbidden = ("_allocate_ib_id", "identity_cursor", "IB-ID-REGISTRY.json")
    violations = []
    for path in active_files:
        body = path.read_text(encoding="utf-8")
        for token in forbidden:
            if token in body:
                violations.append(f"{path.name}:{token}")
    assert not violations, "active memory surface contains forbidden identity authority: " + ", ".join(violations)


def test_canonical_registry_declares_live_receiver_identity_authority():
    registry = json.loads((ROOT / ".naya" / "memory" / "smart-notes" / "REGISTRY.json").read_text(encoding="utf-8"))
    assert registry["identity_authority"] == "live canonical receiver only"
    assert "identity_cursor" not in registry



def test_canonical_registry_missing_authorization_metadata_is_not_green():
    errors = verify_memory_surface.verify()
    assert any('authorization metadata incomplete' in error for error in errors)

