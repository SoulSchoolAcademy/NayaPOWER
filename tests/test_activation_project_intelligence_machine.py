"""Machine contract for the Activation Naya project-intelligence read model.

This fixture is a read-only projection. It cannot grant LAW authority, create
a Smart Note, advance truth-state, or certify a learning outcome. Tests are
guardrails for published claims and source continuity, not runtime learning proof.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / ".naya/project-intelligence/activation-naya.machine.json"

def load():
    assert P.is_file(), "project intelligence missing"
    return json.loads(P.read_text(encoding="utf-8"))

def test_machine_project_shape_and_single_truth():
    d = load()
    assert d["schema"] == "naya.project-intelligence.activation.v1"
    assert d["record_type"] == "NON_AUTHORITATIVE_PROJECT_PROJECTION_CANDIDATE"
    assert d["project_id"] == "activation-naya"
    assert d["project_state"] == "NOT_FULLY_ACTIVATED"
    assert d["information_architecture"]["project_view_is"] == "read_model_or_materialized_projection_not_Source_Of_Truth"
    assert set(d["source_policy"]["no_second"]) == {"Brain", "authority_model", "registry_writer", "Hub_shell", "learning_pipeline"}

def test_machine_nine_nodes_one_organism():
    d = load()
    roles = d["node_contract"]["roles"]
    expected = ["SELF","LAW","ACT","KNOW","PROVE","CONNECT","VERIFY","LEARN","EVOLVE"]
    assert d["node_contract"]["canonical_order"] == expected
    assert [r["id"] for r in roles] == expected
    assert all(r["owns"] and r["emits"] and r["must_not"] for r in roles)

def test_machine_source_dedup_and_sha_evidence():
    corpus = load()["sources"]["uploaded_pdf_corpus"]
    assert corpus["raw_pdf_count"] == 9
    assert corpus["unique_documents"] == len(corpus["documents"]) == 8
    names = [s["key"] for s in corpus["documents"]]
    assert len(names) == len(set(names))
    for s in corpus["documents"]:
        assert s["pages"] > 0
        assert len(s["sha256"]) == 64
        int(s["sha256"], 16)
        assert s["role"]

def test_candidate_never_falsely_promoted_or_claimed_learned():
    d = load()
    t11 = d["runtime_snapshot"]["T11"]
    assert t11["smart_note_id"] == "SN-782"
    assert t11["truth_state"] == "CANDIDATE"
    assert t11["lifecycle_state"] == "CANDIDATE"
    assert t11["scope"] == "PRIVATE"
    assert t11["smart_link_status"] == "ACTIVE_AUTH_GATED"
    assert t11["learning_proven"] is False
    assert t11["cold_retrieval_job"].startswith("FAILURE")
    assert all(g["result"] == "NOT_PROVEN" for g in d["acceptance"]["checks"])
    assert d["runtime_snapshot"]["score"]["current_earned_value"] is None

def test_machine_separates_verified_reported_and_disputed():
    d = load()
    v = d["runtime_snapshot"]
    assert len(v["facts_verified"]) >= 5
    assert all(x["state"] == "VERIFIED_GITHUB" and x["refs"] for x in v["facts_verified"])
    assert all(x["source"] and x["validation"] for x in v["source_reported_claims"])
    assert len(v["disputed_and_resolution_required"]) >= 5
    assert all(x["resolution"] and len(x["positions"]) >= 2 for x in v["disputed_and_resolution_required"])

def test_machine_interfaces_refusals_and_next_step():
    d = load()
    stages = d["pipeline"]["stages"]
    assert len(stages) == 12
    assert len({x["id"] for x in stages}) == len(stages)
    assert all(x["input"] and x["output"] and x["refusal"] for x in stages)
    assert len(d["acceptance"]["checks"]) == 8
    assert d["work"]["single_next_action_id"] == d["work"]["ordered_actions"][0]["id"]
    assert d["machine_interface"]["on_unauthorized"] == "DENY_NO_PRIVATE_PROJECTION"
    assert d["machine_interface"]["on_stale"] == "STALE_REFRESH_REQUIRED"
    assert d["refresh"]["mode"] == "event_driven"
    assert d["refresh"]["no_manual_counter_edits"] is True
    assert d["work"]["pending_consensus"]

def test_machine_sha_pins_and_runtime_proof_reference():
    d = load()
    assert len(d["source_main_sha"]) == 40
    assert d["runtime_snapshot"]["T11"]["receiver_workflow_run"] == 37980089547
    assert d["sources"]["canonical_refs"]["SMART-NOTE-CONTRACT"] == "NAYA-ACTIVATION/SMART-NOTE-OPERATING-CONTRACT-V1.md"
    assert "git" in d["sources"]["canonical_refs"]["PR-2050"]


def test_multi_lesson_retrieval_audit_is_not_conflated_with_blind_learning():
    d = load()
    a = d["runtime_snapshot"]["retrieval_diagnostic"]
    b = d["runtime_snapshot"]["team_reported_blind_battery"]
    assert a["schema"] == "naya.lesson-exam.repository-audit.v1"
    assert a["total_scenarios"] == 43
    assert a["retrieved_expected_id"] + a["selected_different_id"] + a["id_collision"] == 43
    assert a["state"] == "GITHUB_REPRODUCED_DIAGNOSTIC_NOT_CAUSAL_LEARNING"
    assert a["act_control_treatment_wrong_lesson"] == "NOT_RUN"
    assert b["state"] == "TEAM_REPORTED_NOT_INDEPENDENTLY_REPLAYED_IN_THIS_LANE"
    assert b["reported_numerator"] == 14 and b["reported_denominator"] == 14
    assert b["reported_average_score"] == 9.93
    assert d["runtime_snapshot"]["T11"]["learning_proven"] is False
    assert d["work"]["single_next_action_id"] in {a["id"] for a in d["work"]["ordered_actions"]}
