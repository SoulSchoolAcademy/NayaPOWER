from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_receiver_is_the_only_application_ingress():
    receiver = (ROOT / "supabase/functions/v7-smart-note-canonical/index.ts").read_text(encoding="utf-8")
    runtime = (ROOT / "NAYANET/HUB/public/assistant-runtime.js").read_text(encoding="utf-8")

    assert "v7_create_smart_note" in receiver
    assert "v7-smart-note-canonical" in runtime
    assert "fetch(URL+'/functions/v1/v7-smart-note-canonical'" in runtime

    # Application code must consume the receiver's returned identity rather than
    # manufacture the canonical IB-XXXXXX identity locally.
    assert not re.search(r"IB-[0-9]{6}", receiver)
    assert not re.search(r"nextval\(['\"]nayanet_smart_note_ib_identity_seq", runtime)


def test_database_boundary_does_not_allocate_repository_ib_identity_locally():
    migrations = sorted((ROOT / "supabase/migrations").glob("*.sql"))
    matching = []
    for path in migrations:
        text = path.read_text(encoding="utf-8")
        if "nayanet_intelligent_blocks" in text and "nayanet_upsert_intelligent_block_from_smart_note" in text:
            matching.append((path.name, text))

    assert matching, "canonical Intelligent Block persistence boundary is not declared in migrations"
    for _, text in matching:
        assert "nextval('nayanet_smart_note_ib_identity_seq'" not in text
        assert not re.search(r"['"]IB-[0-9]{6}['"]", text)


def test_repository_registry_contains_only_canonical_ib_projection_records():
    registry = json.loads(
        (ROOT / ".naya/memory/smart-notes/REGISTRY.json").read_text(encoding="utf-8")
    )
    assert registry["status"] == "CANONICAL"
    assert registry["identity_authority"] == "live canonical receiver only"
    ids = [entry["intelligent_block_id"] for entry in registry["entries"]]
    assert len(ids) == len(set(ids))
    for entry in registry["entries"]:
        assert re.fullmatch(r"IB-[0-9]{6}", entry["intelligent_block_id"])
        projection = ROOT / entry["path"]
        assert projection.is_file()
        assert entry["path"].endswith("/smart-note.md")


def test_canonical_smart_note_contract_and_retrieval_manifest_agree():
    contract = (ROOT / ".naya/codex/CANONICAL-SMART-NOTE-INTELLIGENT-BLOCK-SYSTEM-V1.md").read_text(encoding="utf-8")
    manifest = json.loads(
        (ROOT / ".naya/memory/RETRIEVAL-MANIFEST.json").read_text(encoding="utf-8")
    )
    assert "Smart Note" in contract and "Intelligent Block (IB)" in contract
    assert "IB-000001" in contract
    assert manifest["identity_authority"] == "live canonical receiver v7-smart-note-canonical"
    assert manifest["canonical_registry"] == ".naya/memory/smart-notes/REGISTRY.json"
