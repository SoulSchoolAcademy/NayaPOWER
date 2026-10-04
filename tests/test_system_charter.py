from pathlib import Path

import pytest

from kernel.system_charter import (
    CharterContractError,
    charter_is_governing,
    compile_node_directive,
    load_system_charter,
    simulate_ratification,
)

NODES = ("SELF","LAW","ACT","KNOW","PROVE","CONNECT","VERIFY","LEARN","EVOLVE")


def test_ratified_charter_is_active_and_governing():
    doc = load_system_charter()
    assert doc["status"] == "RATIFIED_ACTIVE"
    assert doc["authority"]["ratified"] is True
    assert doc["activation"]["runtime_enabled"] is True
    assert charter_is_governing(doc) is True
    directive = compile_node_directive(doc, "SELF")
    assert directive["governing"] is True


def test_exact_twelve_laws_cover_exact_nine_nodes():
    doc = load_system_charter()
    assert [law["id"] for law in doc["laws"]] == list(range(1, 13))
    assert set(doc["node_bindings"]) == set(NODES)
    assert set(node for law in doc["laws"] for node in law["nodes"]) == set(NODES)


def test_each_node_compiles_from_ratified_charter_without_new_node_or_engine():
    doc = load_system_charter()
    for node in NODES:
        directive = compile_node_directive(doc, node)
        assert directive["governing"] is True
        assert directive["node"] == node
        assert directive["objective"]["decision_system"] == "NAYA-DECISION-VALUE-CALCULUS-V2.1"
        assert directive["must"]
        assert directive["must_not"]


def test_hard_stops_precede_act_and_authority_cannot_be_created_by_value():
    doc = load_system_charter()
    hard = next(law for law in doc["laws"] if law["id"] == 2)
    authority = next(law for law in doc["laws"] if law["id"] == 7)
    assert set(hard["nodes"]) == {"LAW","ACT"}
    assert "regardless of score" in hard["machine_rule"]
    assert "value" in authority["machine_rule"].lower()
    assert "never create authority" in authority["machine_rule"].lower()
    assert "allow score to override hard gate" in doc["node_bindings"]["LAW"]["must_not"]


def test_learning_requires_verify_and_cold_successor_continuity():
    doc = load_system_charter()
    learning = next(law for law in doc["laws"] if law["id"] == 9)
    assert {"VERIFY","LEARN","EVOLVE"}.issubset(set(learning["nodes"]))
    assert "behavioral delta" in doc["node_bindings"]["LEARN"]["must"][0]
    assert "authority must be freshly resolved" in next(
        law["machine_rule"] for law in doc["laws"] if law["id"] == 10
    )


def test_active_charter_fails_closed_if_ratification_binding_is_removed():
    import copy
    doc = copy.deepcopy(load_system_charter())
    doc["authority"]["ratification_receipt"] = None
    with pytest.raises(CharterContractError, match="SYSTEM_CHARTER_CANNOT_ACTIVATE_WITHOUT_RATIFICATION"):
        compile_node_directive(doc, "LAW", require_governing=False)


def test_machine_contract_pins_exact_ratified_charter_and_receipt():
    doc = load_system_charter()
    source = doc["sources"]["ratified_charter"]
    assert source["source_branch"] == "brain-build/system-charter-20261004"
    assert source["ratified_head_sha"] == "ea9bd18c6abe8778f04c5775f5ff539dbd4abd79"
    assert source["receipt_blob_sha"] == "ac77b25769fa46fd93c7fc7fc125161be9676164"
    expected = {
        "MANIFESTO.md": "641bfe3fa6f762ee4b7a0cd99cafba3d08fd19f9",
        "MANIFESTO.ai.md": "f9ec135cccdeff5d86334bd20426cfeb995462c2",
        "MANIFESTO.machine.json": "00569ed1a645fa1792d5f914faeeb3e77b26b93c",
        "CONSTITUTION/0003-CONSTITUTIONAL-CODE-V1.md": "8536a0ed253859b4ddcd1d6c98628c24a188164b",
        "MISSION-CONTRACT-V1.md": "3e899f99ff1b01d56e8220a155ea20f525dd4634",
        "SYSTEMS-CONTRACT-V1.md": "91c0cc8d07e4924498f38b8a4ef06ba3de970f2b",
    }
    assert {x["path"]: x["blob_sha"] for x in source["documents"]} == expected
    receipt = (Path(__file__).resolve().parents[1] / source["receipt_path"]).read_text(encoding="utf-8")
    assert source["ratified_head_sha"] in receipt
    for blob_sha in expected.values():
        assert blob_sha in receipt
