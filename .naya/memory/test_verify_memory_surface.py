from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/".naya/memory"))
import verify_memory_surface
def test_canonical_memory_surface():
    assert verify_memory_surface.verify()==[]

def test_retrieval_manifest_names_canonical_ib_store():
    import json
    manifest = json.loads((ROOT / ".naya/memory/RETRIEVAL-MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["canonical_primary_store"] == ".naya/memory/smart-notes/"
    assert manifest["canonical_registry"] == ".naya/memory/smart-notes/REGISTRY.json"
    assert manifest["event_lineage_store"] == ".naya/memory/events/"

def test_legacy_v2_schema_is_quarantined():
    assert not (ROOT / ".naya/memory/note.schema.json").exists()
    assert (ROOT / ".naya/memory/archive/legacy-pre-2026-09-25/note.schema.v2-legacy.json").exists()
