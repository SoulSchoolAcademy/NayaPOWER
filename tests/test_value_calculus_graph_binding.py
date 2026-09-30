import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODES = ["SELF","LAW","ACT","KNOW","PROVE","CONNECT","VERIFY","LEARN","EVOLVE"]
CALCULUS_ID = "NAYA-DECISION-VALUE-CALCULUS-V2.1"
GRAPH = ROOT / "BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json"
ORGANISM = ROOT / "BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json"
OBJECT = ROOT / "BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-DECISION-VALUE-CALCULUS-V2.1.json"
PROTOCOL = ROOT / "BRAIN/04-INTELLIGENCE/0005-SMART-NODE-INTELLIGENT-BLOCK-PROTOCOL-V1.md"
MASTER = ROOT / "BRAIN/04-INTELLIGENCE/MASTER-INDEX.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_value_calculus_is_one_shared_intelligent_object_not_tenth_node():
    obj = load(OBJECT)
    organism = load(ORGANISM)
    assert obj["object_id"] == CALCULUS_ID
    assert obj["object_type"] == "DECISION_SYSTEM"
    assert organism["order"] == NODES
    assert CALCULUS_ID not in organism["order"]
    assert set(organism["shared_decision_calculus"]["node_roles"]) == set(NODES)

def test_graph_has_exactly_one_calculus_edge_to_each_nine_node():
    graph = load(GRAPH)
    edges = [e for e in graph["edges"] if e["source_id"] == CALCULUS_ID]
    assert len(edges) == 9
    assert {e["target_id"] for e in edges} == {f"NAYA-KERNEL-{n}" for n in NODES}
    assert all(e["type"] == "APPLIES_TO" for e in edges)
    assert all(e["status"] == "ACTIVE" for e in edges)
    assert all(e["epistemic_state"] == "VERIFIED" for e in edges)

def test_each_node_rereads_same_calculus_edge_and_role():
    for n in NODES:
        node = load(ROOT / f"BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-KERNEL-{n}.json")
        assert node["machine_view"]["decision_calculus"] == CALCULUS_ID
        assert node["machine_view"]["decision_calculus_role"]
        rels = [r for r in node["relationships"] if r["relationship_id"] == f"REL-VALUE-CALCULUS-{n}"]
        assert len(rels) == 1
        rel = rels[0]
        assert rel["direction"] == "IN"
        assert rel["type"] == "APPLIES_TO"
        assert rel["source_object_id"] == CALCULUS_ID
        assert rel["target_object_id"] == f"NAYA-KERNEL-{n}"

def test_protocol_and_master_index_expose_executable_calculus():
    protocol = PROTOCOL.read_text(encoding="utf-8")
    master = load(MASTER)
    assert "## 23. Decision Value Calculus V2.1" in protocol
    assert "ACT | READ_MORE | ASK | REFUSE" in protocol
    assert master["decision_calculus"]["object_id"] == CALCULUS_ID
    assert master["decision_calculus"]["executable"] == "kernel/value_calculus.py"
    assert master["decision_calculus"]["applies_to_nodes"] == NODES

def test_graph_binding_does_not_claim_runtime_behavioral_proof():
    obj = load(OBJECT)
    assert obj["proof"]["graph_binding_status"] == "SOURCE_GRAPH_BINDING"
    assert obj["proof"]["production_status"] == "NOT_PRODUCTION_PROVEN"
    assert "do not prove live graph traversal" in obj["proof"]["limitation"].lower()
