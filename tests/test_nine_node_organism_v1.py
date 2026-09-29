import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_nine_node_organism_contract_has_all_nodes_and_envelope():
    p=ROOT/"BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json"
    j=json.loads(p.read_text())
    assert j["order"]==["SELF","LAW","ACT","KNOW","PROVE","CONNECT","VERIFY","LEARN","EVOLVE"]
    required=set(j["universal_envelope"]["required_fields"])
    for name,node in j["nodes"].items():
        assert required.issubset(node.keys()), (name, required-set(node.keys()))
    assert j["nodes"]["LAW"]["non_responsibilities"][0]=="execute action"

def test_smart_door_registry_separates_capability_from_authority():
    j=json.loads((ROOT/"BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json").read_text())
    ids={d["door_id"] for d in j["doors"]}
    assert {"DOOR-GITHUB","DOOR-MCP","DOOR-AI","DOOR-DATA","DOOR-EMAIL","DOOR-CALENDAR","DOOR-VOICE","DOOR-WEB","DOOR-NAYA"}.issubset(ids)
    c=json.loads((ROOT/"BRAIN/10-INTERFACES/0001-SMART-DOOR-CONTRACT-V1.json").read_text())
    assert any("does not create authority" in x for x in c["laws"])

def test_law_runtime_decides_and_receipts_but_never_executes():
    src=(ROOT/"supabase/functions/nayanet-law-runtime/index.ts").read_text()
    assert 'action:"law_authority_decision"' in src
    assert "evaluateLaw" in src
    assert "LAW_DECIDES_ONLY_DOES_NOT_EXECUTE" in src
    assert "nayanet_intelligence_commit_runtime" not in src

def test_organism_source_map_resolves_existing_seams_without_claiming_universal_binding():
    j=json.loads((ROOT/"BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json").read_text())
    assert j["source_assessment"]["universal_binding"] == "NOT_PROVEN"
    assert "not a mandatory linear execution schedule" in j["order_semantics"]
    edges=json.loads((ROOT/"BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json").read_text())["edges"]
    for name,node in j["nodes"].items():
        binding=node["source_binding"]
        refs=binding["contract_refs"]+[binding["semantic_schema"]]+binding["runtime_sources"]+binding["test_sources"]+binding["workflow_refs"]
        for ref in refs:
            assert (ROOT/ref).is_file(), (name,ref)
        assert binding["gap"] and binding["transition_contract"]
        assert "NOT_PROVEN" in binding["schema_conformance"]
        expected={e["relationship_id"] for e in edges if node["node_id"] in (e["source_id"],e["target_id"])}
        assert set(node["relationships"]) == expected
