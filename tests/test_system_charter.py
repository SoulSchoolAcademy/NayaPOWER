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


def test_candidate_charter_is_machine_valid_but_non_governing():
    doc = load_system_charter()
    assert doc["status"] == "CANDIDATE_NON_GOVERNING"
    assert charter_is_governing(doc) is False
    with pytest.raises(CharterContractError, match="SYSTEM_CHARTER_NOT_RATIFIED_ACTIVE"):
        compile_node_directive(doc, "SELF")


def test_exact_twelve_laws_cover_exact_nine_nodes():
    doc = load_system_charter()
    assert [law["id"] for law in doc["laws"]] == list(range(1, 13))
    assert set(doc["node_bindings"]) == set(NODES)
    assert set(node for law in doc["laws"] for node in law["nodes"]) == set(NODES)


def test_each_node_compiles_after_ratification_without_new_node_or_engine():
    doc = simulate_ratification(load_system_charter())
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
    assert "never create authority" in doc["node_bindings"]["LAW"]["must_not"][1]


def test_learning_requires_verify_and_cold_successor_continuity():
    doc = load_system_charter()
    learning = next(law for law in doc["laws"] if law["id"] == 9)
    assert {"VERIFY","LEARN","EVOLVE"}.issubset(set(learning["nodes"]))
    assert "behavioral delta" in doc["node_bindings"]["LEARN"]["must"][0]
    assert "authority must be freshly resolved" in next(
        law["machine_rule"] for law in doc["laws"] if law["id"] == 10
    )


def test_candidate_cannot_activate_by_flipping_runtime_flag_only():
    doc = load_system_charter()
    doc["activation"]["runtime_enabled"] = True
    with pytest.raises(CharterContractError, match="SYSTEM_CHARTER_CANNOT_ACTIVATE_WITHOUT_RATIFICATION"):
        compile_node_directive(doc, "LAW", require_governing=False)


def test_machine_contract_pins_naya2_charter_sources():
    doc = load_system_charter()
    source = doc["sources"]["candidate_charter"]
    assert source["branch"] == "brain-build/system-charter-20261004"
    assert source["head_sha"] == "0ed85ad91da10212fe57bc64af302a21a0d889fa"
    paths = {x["path"] for x in source["documents"]}
    assert paths == {
        "MANIFESTO.md",
        "CONSTITUTION/0003-CONSTITUTIONAL-CODE-V1.md",
        "MISSION-CONTRACT-V1.md",
        "SYSTEMS-CONTRACT-V1.md",
    }
