import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "SELF": ["NAYA-KERNEL-LAW", "NAYA-KERNEL-KNOW"],
    "LAW": ["NAYA-KERNEL-ACT"],
    "ACT": ["NAYA-KERNEL-VERIFY"],
    "KNOW": ["NAYA-KERNEL-PROVE", "NAYA-KERNEL-CONNECT"],
    "PROVE": ["NAYA-KERNEL-VERIFY"],
    "CONNECT": ["NAYA-KERNEL-VERIFY"],
    "VERIFY": ["NAYA-KERNEL-LEARN"],
    "LEARN": ["NAYA-KERNEL-EVOLVE"],
    "EVOLVE": ["NAYA-KERNEL-SELF"],
}

EXPECTED_ROUTES = [
    "SELF->LAW",
    "SELF->KNOW",
    "LAW->ACT",
    "ACT->VERIFY",
    "KNOW->PROVE",
    "KNOW->CONNECT",
    "PROVE->VERIFY",
    "CONNECT->VERIFY",
    "VERIFY->LEARN",
    "LEARN->EVOLVE",
    "EVOLVE->SELF",
]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_organism_declares_exact_minimum_runtime_routes():
    organism = load("BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json")
    assert organism["required_runtime_routes"] == EXPECTED_ROUTES
    for node, targets in EXPECTED.items():
        assert organism["nodes"][node]["runtime_handoffs"] == targets


def test_node_objects_match_runtime_route_contract():
    for node, targets in EXPECTED.items():
        obj = load(f"BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-KERNEL-{node}.json")
        assert obj["machine_view"]["runtime_handoffs"] == targets
        assert "semantic/display neighbor only" in obj["machine_view"]["neighbor_handoff_semantics"]


def test_graph_seed_contains_every_required_runtime_route():
    graph = load("BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json")
    pairs = {(edge["source_id"], edge["target_id"]) for edge in graph["edges"]}
    for route in EXPECTED_ROUTES:
        source, target = route.split("->")
        assert (f"NAYA-KERNEL-{source}", f"NAYA-KERNEL-{target}") in pairs, route


def test_know_to_prove_direction_is_consistent_everywhere():
    graph = load("BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json")
    edge = next(e for e in graph["edges"] if e["relationship_id"] == "REL-KERNEL-KNOW-PROVE")
    assert edge["source_id"] == "NAYA-KERNEL-KNOW"
    assert edge["target_id"] == "NAYA-KERNEL-PROVE"

    know = load("BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-KERNEL-KNOW.json")
    prove = load("BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-KERNEL-PROVE.json")
    krel = next(r for r in know["relationships"] if r["relationship_id"] == "REL-KERNEL-KNOW-PROVE")
    prel = next(r for r in prove["relationships"] if r["relationship_id"] == "REL-KERNEL-KNOW-PROVE")

    assert krel["direction"] == "OUT"
    assert krel["source_object_id"] == "NAYA-KERNEL-KNOW"
    assert krel["target_object_id"] == "NAYA-KERNEL-PROVE"

    assert prel["direction"] == "IN"
    assert prel["source_object_id"] == "NAYA-KERNEL-KNOW"
    assert prel["target_object_id"] == "NAYA-KERNEL-PROVE"


def test_seed_edge_semantics_do_not_invert_governance_or_data_flow():
    graph = load("BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json")
    by_id = {e["relationship_id"]: e for e in graph["edges"]}

    # SELF supplies identity/mission/current-state context; it does not govern LAW.
    assert by_id["REL-KERNEL-SELF-LAW"]["type"] == "CONTEXTUALIZES"

    # ACT can produce execution observations/events consumed by intelligence;
    # the edge must not read as KNOW owning/using ACT authority.
    assert by_id["REL-KERNEL-ACT-KNOW"]["type"] == "PRODUCES"
