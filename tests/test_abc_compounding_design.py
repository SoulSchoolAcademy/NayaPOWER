"""Adversarial tests for the A->B->C compounding proof design validator.

Evidence law applies: a green validator proves the DESIGN is well-formed.
It proves nothing about production behavior. Only a live gated run with
receipts proves compounding.
"""
import copy
import json
import re
import subprocess
import sys
from pathlib import Path

import importlib.util

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load_validator():
    # Loaded via importlib from its file path rather than a static top-level
    # import: tools/ carries no package marker, and a static
    # `from validate_abc_compounding_design import ...` is indistinguishable
    # to tests/test_ci_declares_test_dependencies.py from a third-party
    # import the CI workflow does not install.
    path = ROOT / "tools" / "validate_abc_compounding_design.py"
    spec = importlib.util.spec_from_file_location("validate_abc_compounding_design", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_val = _load_validator()
DESIGN_PATH = _val.DESIGN_PATH
check_precondition_gate = _val.check_precondition_gate
validate_design = _val.validate_design


@pytest.fixture
def design():
    return json.loads(DESIGN_PATH.read_text(encoding="utf-8"))


def test_valid_design_passes(design):
    assert validate_design(design) == []


def test_missing_a_stage_fails(design):
    d = copy.deepcopy(design)
    d["generation_a"]["stages"].remove("independent_verifier_confirms_result")
    errs = validate_design(d)
    assert any(e.startswith("MISSING_STAGE:generation_a:") for e in errs)


def test_stage_order_violation_fails(design):
    d = copy.deepcopy(design)
    st = d["generation_b"]["stages"]
    # move verification-after-action before reconstruction: forward-only violation
    st.insert(0, st.pop(st.index("produce_distinct_verified_refinement_from_own_result")))
    errs = validate_design(d)
    assert any(e.startswith("STAGE_ORDER_VIOLATION:generation_b") for e in errs)


def test_missing_negative_control_fails(design):
    d = copy.deepcopy(design)
    d["negative_controls"] = [c for c in d["negative_controls"]
                              if c["id"] != "chain_halt_on_no_b_improvement"]
    errs = validate_design(d)
    assert any("NEGATIVE_CONTROLS_INCOMPLETE" in e for e in errs)
    assert any("CHAIN_HALT_RULE_MISSING" in e for e in errs)


def test_negative_control_without_rule_fails(design):
    d = copy.deepcopy(design)
    d["negative_controls"][0] = {"id": "unrelated_task"}
    errs = validate_design(d)
    assert any("NEGATIVE_CONTROL_NO_RULE" in e for e in errs)


def test_incomplete_evidence_chain_fails(design):
    d = copy.deepcopy(design)
    d["evidence_chain_links"].remove("b_independent_verification")
    d["evidence_chain_links"].remove("c_retrieval_receipt")
    errs = validate_design(d)
    assert any("EVIDENCE_CHAIN_INCOMPLETE" in e for e in errs)


def test_authority_boundary_must_be_false(design):
    d = copy.deepcopy(design)
    d["authority_boundary"]["graph_grants_authority"] = True
    assert any("AUTHORITY_BOUNDARY" in e for e in validate_design(d))
    d2 = copy.deepcopy(design)
    del d2["authority_boundary"]
    assert any("AUTHORITY_BOUNDARY" in e for e in validate_design(d2))


def test_no_authority_inheritance_rule_required(design):
    d = copy.deepcopy(design)
    d["authority_boundary"]["rule"] = "Some generic statement about graphs."
    assert any("NO_AUTHORITY_INHERITANCE_RULE_MISSING" in e for e in validate_design(d))


def test_epistemic_state_outside_contract_fails(design):
    d = copy.deepcopy(design)
    d["epistemic_states_allowed"].append("ABSOLUTELY_CERTAIN")
    assert any("EPISTEMIC_STATE_OUTSIDE_CONTRACT_V2" in e for e in validate_design(d))


def test_relationship_type_outside_contract_fails(design):
    d = copy.deepcopy(design)
    d["relationship_types_allowed"].append("MAGICALLY_CAUSES")
    assert any("RELATIONSHIP_TYPE_OUTSIDE_CONTRACT_V2" in e for e in validate_design(d))


def test_precondition_met_without_evidence_fails(design):
    d = copy.deepcopy(design)
    p = d["required_preconditions"][0]
    p["met"] = True
    p["evidence"] = None
    assert any("PRECONDITION_MET_WITHOUT_EVIDENCE" in e for e in validate_design(d))


def test_unmet_precondition_without_blocker_fails(design):
    d = copy.deepcopy(design)
    p = next(x for x in d["required_preconditions"] if not x["met"])
    del p["blocker"]
    assert any("UNMET_PRECONDITION_NO_BLOCKER_RECORDED" in e for e in validate_design(d))


def test_baseline_not_pre_registered_fails(design):
    d = copy.deepcopy(design)
    del d["measurement_protocol"]["baseline"]
    assert any("BASELINE_NOT_PRE_REGISTERED" in e for e in validate_design(d))


def test_metrics_missing_fails(design):
    d = copy.deepcopy(design)
    d["measurement_protocol"]["metrics"] = []
    assert any("MEASUREMENT_METRICS_MISSING" in e for e in validate_design(d))


def test_success_definition_must_name_improvement_vs_baseline(design):
    d = copy.deepcopy(design)
    d["measurement_protocol"]["success_definition"] = "The chain looks good."
    assert any("SUCCESS_DEFINITION_MISSING_BASELINE_IMPROVEMENT" in e for e in validate_design(d))


def test_design_may_not_self_claim_proof(design):
    d = copy.deepcopy(design)
    d["status"] = "VERIFIED"
    assert any("DESIGN_MAY_NOT_SELF_CLAIM_PROOF" in e for e in validate_design(d))


def test_as_of_sha_must_be_valid(design):
    d = copy.deepcopy(design)
    d["as_of"] = "not-a-sha"
    assert any("AS_OF_SHA_INVALID" in e for e in validate_design(d))


def test_live_gate_refuses_while_preconditions_unmet(design):
    # Canonical design (current main reality): two preconditions unmet -> REFUSED.
    allowed, reasons = check_precondition_gate(design)
    assert allowed is False
    assert any("LIVE_RUN_REFUSED" in r for r in reasons)
    assert any("graph-v2-persistence-migration" in r for r in reasons)
    assert any("v2-selector-wired-and-proven" in r for r in reasons)


def test_gate_allows_only_when_all_met_with_evidence(design):
    d = copy.deepcopy(design)
    for p in d["required_preconditions"]:
        p["met"] = True
        p["evidence"] = "evidence://run/12345678"
    assert validate_design(d) == []
    allowed, reasons = check_precondition_gate(d)
    assert allowed is True
    assert any("LIVE_RUN_ALLOWED" in r for r in reasons)


def test_forged_precondition_report_fails_validation(design):
    d = copy.deepcopy(design)
    p = next(x for x in d["required_preconditions"] if not x["met"])
    p["met"] = True  # claim met...
    p["evidence"] = None  # ...but no evidence pointer
    errs = validate_design(d)
    assert any("PRECONDITION_MET_WITHOUT_EVIDENCE" in e for e in errs)
    allowed, _ = check_precondition_gate(d)
    assert allowed is False


def test_validator_cli_reports_refused_exit_code():
    r = subprocess.run([sys.executable, str(ROOT / "tools/validate_abc_compounding_design.py"),
                        "--preconditions", str(DESIGN_PATH)],
                       capture_output=True, text=True, cwd=str(ROOT))
    assert r.returncode == 2  # design valid, live gate REFUSED
    assert "DESIGN_VALID" in r.stdout
    assert "LIVE_RUN_REFUSED" in r.stdout


def test_design_pins_exact_main_sha(design):
    # The design must pin the EXACT main SHA it was authored against: 40 hex
    # chars, not an abbreviation. It is intentionally NOT compared to current
    # HEAD — on a PR branch HEAD is the branch head while the pin predates the
    # branch commit by construction, so an equality check can never pass there
    # (it only passed pre-commit when HEAD was still the base). Resolvability
    # via git is not asserted either: CI checks out a shallow clone, so the
    # pinned commit may not be present locally.
    sha = design["as_of"]
    assert isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{40}", sha), \
        f"as_of must pin the exact 40-char main SHA, got {sha!r}"


def test_graph_contract_v2_vocab_alignment(design):
    contract = json.loads((ROOT / "BRAIN/04-INTELLIGENCE/GRAPH/0003-GRAPH-RELATIONSHIP-CONTRACT-V2.json")
                          .read_text(encoding="utf-8"))
    assert set(design["epistemic_states_allowed"]).issubset(set(contract["allowed_epistemic_states"]))
    assert set(design["relationship_types_allowed"]).issubset(set(contract["allowed_relationship_types"]))
    assert contract["authority_boundary"]["graph_grants_authority"] is False
