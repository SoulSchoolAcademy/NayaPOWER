"""Conformance: the TS admission-contract port matches the Python canonical law
and is actually enforced at the CANDIDATE insert seam.

Style follows the repo's existing edge-function source-text tests
(e.g. test_checkpoint_provenance_diagnosis.py): the deployed seam is
TypeScript, so the test asserts on its source rather than executing Deno.
Behavioral authority remains the Python suite
(tests/test_learning_admission_contract.py).
"""
import re
from pathlib import Path

from kernel.protocol.learning_capture import ADMISSION_RULES

ROOT = Path(__file__).resolve().parent.parent
LEARN = ROOT / "supabase" / "functions" / "nayanet-learning-verify"
INDEX_TS = (LEARN / "index.ts").read_text(encoding="utf-8")
PORT_TS = (LEARN / "admission_contract.ts").read_text(encoding="utf-8")
RECEIVER_TS = (
    ROOT / "supabase" / "functions" / "v7-smart-note-canonical" / "index.ts"
).read_text(encoding="utf-8")


def test_port_carries_all_seven_rule_ids():
    for rule_id in ADMISSION_RULES:
        assert f'"{rule_id}"' in PORT_TS, f"TS port missing rule {rule_id}"


def test_port_rule_ids_match_python_canonical():
    ts_ids = re.findall(r'export const RULE_\w+ = "([a-z_]+)";', PORT_TS)
    assert ts_ids == list(ADMISSION_RULES), (
        "TS rule IDs drifted from the Python canonical ADMISSION_RULES: "
        f"ts={ts_ids} py={list(ADMISSION_RULES)}"
    )


def test_port_exports_check_admission():
    assert "export function checkAdmission" in PORT_TS


def test_index_imports_the_gate():
    assert 'from "./admission_contract.js"' in INDEX_TS
    assert "checkAdmission" in INDEX_TS


def test_gate_rejects_before_insert():
    assert "ADMISSION_CONTRACT_REJECTED" in INDEX_TS
    assert "failed_rules" in INDEX_TS
    check_pos = INDEX_TS.index("checkAdmission(")
    insert_pos = INDEX_TS.index('.from("learning_evidence").insert(candidate)')
    assert check_pos < insert_pos, "the gate must run BEFORE the CANDIDATE insert"


def test_rejection_returns_no_candidate():
    # The rejection branch returns before the insert line is reachable.
    reject_block = INDEX_TS.split("ADMISSION_CONTRACT_REJECTED")[0]
    tail = INDEX_TS[INDEX_TS.index("ADMISSION_CONTRACT_REJECTED"):]
    first_return_close = tail.index("}, 409)")
    between = tail[:first_return_close]
    assert ".insert(candidate)" not in between


def test_verdict_is_persisted_for_audit():
    assert "admission_verdict" in INDEX_TS
    assert "admission_design" in INDEX_TS


def test_receiver_path_is_not_gated():
    # The v7-smart-note-canonical Receiver lane must never be gated by this
    # contract (separate lane by law: the director/user path).
    assert "admission_contract" not in RECEIVER_TS
    assert "ADMISSION_CONTRACT_REJECTED" not in RECEIVER_TS
