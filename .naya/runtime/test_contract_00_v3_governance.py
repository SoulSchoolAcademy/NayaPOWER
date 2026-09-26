"""Contract 00 V3 self-governance acceptance tests.

These tests prove the constitutional artifacts are structurally reachable and
that critical governance rules cannot silently disappear from the candidate.
They intentionally do not claim runtime/production enforcement where none is
registered.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / ".naya/contracts/00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md"
SCHEMA = ROOT / ".naya/contracts/schemas/CONTRACT-00-GOVERNANCE-V3.schema.json"
ENFORCEMENT = ROOT / ".naya/contracts/CONTRACT-00-ENFORCEMENT-REGISTRY-V3.json"
PROCEDURE = ROOT / ".naya/contracts/CONTRACT-00-DECISION-PROCEDURE-V3.json"
REGISTRY = ROOT / ".naya/control-plane/CANONICAL-CONTRACT-REGISTRY.md"


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_contract_00_machine_chain_is_reachable():
    assert CONTRACT.exists()
    assert SCHEMA.exists()
    assert ENFORCEMENT.exists()
    assert PROCEDURE.exists()
    assert REGISTRY.exists()


def test_contract_00_identity_and_candidate_state_are_explicit():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Contract ID:** CC-000" in text
    assert "3.0-CANDIDATE" in text
    assert "V3 CANDIDATE UNDER REVIEW" in text


def test_contract_00_required_governance_sections_exist():
    text = CONTRACT.read_text(encoding="utf-8")
    required = [
        "## 41. Constitutional Core",
        "## 42. Canonical Contract Governance Layer",
        "## 43. Deterministic Constitutional Decision Procedure",
        "## 44. Action Proportionality",
        "## 45. Enforcement Registry",
        "## 46. Trust Boundary",
        "## 47. Constitutional Self-Governance",
        "## 48. Constitutional Amendment and Emergency Repair",
        "## 49. Constitutional Reachability",
        "## 50. Contract 00 Acceptance Status",
        "## 51. Specialized Contract Governance Freeze",
        "## 52. Constitutional Completion Record",
    ]
    for section in required:
        assert section in text


def test_decision_procedure_is_fail_closed_and_ordered():
    procedure = _json(PROCEDURE)
    expected = [
        "IDENTIFY", "RESTORE", "DISCOVER", "RESOLVE_AUTHORITY",
        "CHECK_SCOPE", "CHECK_CONFLICT", "CLASSIFY_ACTION",
        "DEFINE_SUCCESS_AND_PROOF", "CHECK_ENFORCEMENT",
        "EXECUTE_OR_REFUSE", "OBSERVE", "VERIFY", "RECORD_EVIDENCE",
        "UPDATE_CANONICAL_STATE", "LEAVE_SUCCESSOR_STATE",
    ]
    assert procedure["steps"] == expected
    assert set(procedure["fail_closed_states"]) == {"UNKNOWN", "BLOCKED", "CONFLICTED"}


def test_enforcement_registry_does_not_fake_full_enforcement():
    registry = _json(ENFORCEMENT)
    assert registry["contract_id"] == "CC-000"
    assert registry["status"] == "CANDIDATE"
    statuses = {rule["status"] for rule in registry["rules"]}
    assert "UNENFORCED" in statuses or "PARTIALLY_ENFORCED" in statuses
    for rule in registry["rules"]:
        if rule["status"] == "ENFORCED":
            assert rule["evidence"], f"ENFORCED rule lacks evidence: {rule['rule_id']}"


def test_registry_points_to_cc000_and_blocks_premature_full_governance():
    text = REGISTRY.read_text(encoding="utf-8")
    assert "### CC-000: NayaNET Constitutional Contract Law" in text
    assert ".naya/contracts/00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md" in text
    assert "CONTRACT 00 V3 GOVERNANCE GATE" in text
    assert "must not be treated as operationally ratified" in text


def test_critical_truth_and_anti_guessing_rules_survive_mutation_probe():
    text = CONTRACT.read_text(encoding="utf-8")
    critical = [
        "UNKNOWN ≠ PASS",
        "CAPABILITY DOES NOT CREATE AUTHORITY",
        "Naya MUST NOT",
        "Claim strength MUST NOT exceed evidence strength",
        "If any mandatory step cannot be established",
    ]
    for rule in critical:
        assert rule in text

    mutated = text.replace("UNKNOWN ≠ PASS", "UNKNOWN = PASS", 1)
    assert "UNKNOWN ≠ PASS" not in mutated
    assert "UNKNOWN = PASS" in mutated


if __name__ == "__main__":
    tests = [
        test_contract_00_machine_chain_is_reachable,
        test_contract_00_v3_canonicality_and_human_ratification_rules,
        test_contract_00_v3_proactive_execution_and_no_permission_loop_are_explicit,
        test_contract_00_v3_ratification_cannot_be_inferred,
        test_contract_00_identity_and_candidate_state_are_explicit,
        test_contract_00_required_governance_sections_exist,
        test_decision_procedure_is_fail_closed_and_ordered,
        test_enforcement_registry_does_not_fake_full_enforcement,
        test_registry_points_to_cc000_and_blocks_premature_full_governance,
        test_critical_truth_and_anti_guessing_rules_survive_mutation_probe,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS Contract 00 V3 self-governance suite: {len(tests)} tests")


def test_contract_00_v3_canonicality_and_human_ratification_rules():
    schema = _json(ROOT / ".naya/contracts/schemas/CONTRACT-00-GOVERNANCE-V3.schema.json")
    assert schema["canonicality"]["max_in_force_constitutional_claimants"] == 1
    assert schema["canonicality"]["unmapped_in_force_constitutional_claimants_before_ratification"] == 0
    assert schema["properties"]["ratification"]["properties"]["human_only"]["const"] is True
    assert schema["properties"]["ratification"]["properties"]["machine_cannot_ratify"]["const"] is True


def test_contract_00_v3_proactive_execution_and_no_permission_loop_are_explicit():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Naya MUST take ownership of advancing the highest-value safe next action" in text
    assert "MUST NOT wait for a human to restate a next step" in text
    assert "MUST NOT use proactive ownership to expand authority" in text


def test_contract_00_v3_ratification_cannot_be_inferred():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "AI self-declaration is never ratification" in text
    assert "MUST NOT by itself change a contract from CANDIDATE/PROPOSED to RATIFIED or ACTIVE" in text
    assert "No automated gate may convert CANDIDATE into RATIFIED" in text
