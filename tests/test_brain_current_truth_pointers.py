import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRAIN_INDEX = ROOT / "BRAIN" / "NAYAPOWER-BRAIN-INDEX.json"


def _index():
    return json.loads(BRAIN_INDEX.read_text(encoding="utf-8"))


def test_brain_index_root_navigation_points_to_real_paths():
    index = _index()
    for key in ("canonical_root", "constitutional_root", "governance_root", "superbrain_spec"):
        path = ROOT / index[key]
        assert path.exists(), f"{key} points to missing path: {index[key]}"


def test_brain_index_source_corpus_count_matches_numbered_knowledge_concepts():
    index = _index()
    concepts = list((ROOT / "KNOWLEDGE").glob("NAYA POWER CONCEPT*.md"))
    assert index["source_corpus"]["concepts"] == len(concepts), (
        index["source_corpus"]["concepts"],
        len(concepts),
    )


def test_brain_index_operations_pointers_are_real_and_machine_plan_is_projection():
    index = _index()
    operations = index["operations"]
    for key in ("queue", "master_plan", "master_plan_machine_projection", "issue_944_reconciliation"):
        path = ROOT / operations[key]
        assert path.exists(), f"{key} points to missing path: {operations[key]}"

    machine = json.loads((ROOT / operations["master_plan_machine_projection"]).read_text(encoding="utf-8"))
    assert machine["projection_of"] == operations["master_plan"]
    assert machine["authority_note"].lower().find("not a second authority") >= 0


def test_brain_index_preserves_bounded_proof_semantics():
    proof = _index()["proof_boundary"]
    bounded = proof["bounded_production_proof"]
    assert bounded["issue"] == 913
    assert bounded["source_revision"] == "0dcff9b815039d20a7c4c06e05da3a8d9fab5ba4"
    assert proof["production_proof"] == "PROVEN_BOUNDED_EXACT_REVISION_NOT_INHERITED_BY_LATER_MAIN"
    assert proof["successor_behavioral_improvement"] == "PROVEN_BOUNDED_RELATED_HELDOUT_WITH_UNRELATED_REFUSAL"
    nine = proof["nine_node_behavioral_acceptance"]
    assert nine["status"] == "PRODUCTION_PROVEN_BOUNDED"
    assert nine["source_revision"] == "335bdd82568e8041d3f6921a9ee4c7bf28e2c99f"
    assert nine["proof_run"] == "36632211367"
    assert "universal" in nine["limitation"].lower()
