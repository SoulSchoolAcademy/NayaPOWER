import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "KNOWLEDGE"
INDEX = KNOWLEDGE / "NAYAPOWER-INDEX-V1.json"
SMART_NODE_MANIFEST = ROOT / "BRAIN" / "04-INTELLIGENCE" / "SMART-NODE-PROTOCOL-V1.json"


def test_every_numbered_concept_file_is_in_machine_index():
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    indexed = {entry["path"] for entry in index["files"]}
    concepts = {
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in KNOWLEDGE.glob("NAYA POWER CONCEPT*.md")
    }
    assert concepts <= indexed, f"Unindexed KNOWLEDGE concepts: {sorted(concepts - indexed)}"


def test_smart_node_terminology_matches_canonical_operating_protocol():
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    manifest = json.loads(SMART_NODE_MANIFEST.read_text(encoding="utf-8"))
    term = index["terminology"]["canonical"]["Smart Node"]
    assert manifest["status"] == "CANONICAL"
    assert manifest["canonical_machine_target"] == "INTELLIGENT_BLOCK"
    assert "human operating command" in term.lower()
    assert "Smart Node" not in index["terminology"].get("historical", {})
