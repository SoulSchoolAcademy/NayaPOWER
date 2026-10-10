"""Review-only regression suite for candidate compounding and Smart App reuse."""
import hashlib
import json
from pathlib import Path

from kernel.value_calculus import (
    ACT, ASK, NEEDS_AUTHORITY, Candidate, PVEstimate, QualityProfile, RiskPolicy,
    gate_candidate,
)
from tools.qualify_reusable_smart_app import preflight_reuse, rank_repair_options

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / ".naya/specifications/NAYA-COMPOUNDING-SMART-APP-REUSE-V1.candidate.json"
CONTENT = b"approved-release-bytes-v1"


def valid_package():
    return {
        "artifact_id": "SMART-APP-DEMO-001",
        "version": "1.0.0",
        "content_sha256": hashlib.sha256(CONTENT).hexdigest(),
        "owner_scope": "PRIVATE",
        "source_main_sha": "a" * 40,
        "canonical_refs": ["HUB/NAYANET-SMART-APP-ROOMS-V1.json"],
        "human_job": "Use a qualified and bounded component rather than rebuild it",
        "required_capabilities": ["read_template"],
        "applicability": ["permitted_same_project"],
        "non_applicability": ["untrusted_external_project"],
        "authority_ref": "law-receipt:for-independent-check",
        "provenance_refs": ["content-receipt:example"],
        "independent_proof_refs": ["verify-receipt:example"],
        "negative_test_refs": ["test:wrong_scope"],
        "observed_quality": {"verification": "VERIFIED_PASS"},
        "quality_profile_ref": "NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md",
        "rollback_ref": "snapshot:previous_version",
        "cold_successor_probe": "run:independent_cold_reuse",
        "outcome_metric": "measured_correct_reuse_vs_rebuild",
        "supersedes": None,
    }


def test_no_competing_authority_and_all_existing_contracts_referenced():
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    assert spec["state"] == "CANDIDATE_FOR_PEER_REVIEW_NOT_RATIFIED"
    assert spec["pipeline"][0]["step"] == "DEFINE"
    assert spec["pipeline"][-1]["step"] == "MEASURE"
    assert len(spec["pipeline"]) == 9
    assert "NO_SECOND_BRAIN" in spec["invariants"]
    assert "NO_SECOND_VALUE_CALCULATOR" in spec["invariants"]
    assert "NEW_VERSION_FOR_CHANGED_BYTES" in spec["invariants"]
    assert "GRADUATION_REQUIRES_COLD_SUCCESSOR_REUSE" in spec["invariants"]
    for path in spec["governed_dependencies"].values():
        assert (ROOT / path).is_file(), path


def test_valid_locally_consistent_candidate_is_never_auto_published():
    result = preflight_reuse(valid_package(), CONTENT)
    assert result["status"] == "REVIEWABLE_NOT_AUTHORIZED"
    assert result["errors"] == []
    assert result["publishing_authorized"] is False
    assert result["independent_proof_verified_here"] is False


def test_hash_mismatch_fails_closed():
    result = preflight_reuse(valid_package(), b"modified-unverified-release")
    assert result["status"] == "NOT_READY"
    assert "CONTENT_HASH_MISMATCH" in result["errors"]


def test_missing_provenance_cannot_be_accepted():
    p = valid_package()
    p["independent_proof_refs"] = []
    r = preflight_reuse(p, CONTENT)
    assert r["status"] == "NOT_READY"
    assert "REQUIRED_REFERENCES_MISSING:independent_proof_refs" in r["errors"]


def test_unknown_authority_field_never_authorizes_release():
    p = valid_package()
    p["authority_ref"] = "unverified-claim"
    result = preflight_reuse(p, CONTENT)
    assert result["publishing_authorized"] is False
    assert result["next_gate"] == "EXTERNAL_VERIFIER_AND_LAW_AUTHORITY_CHECK"


def test_invalid_scope_is_rejected():
    p = valid_package()
    p["owner_scope"] = "ANYONE_WITH_URL"
    assert "SCOPE_INVALID" in preflight_reuse(p, CONTENT)["errors"]


def test_same_version_changed_bytes_refused():
    prior = valid_package()
    candidate = valid_package()
    new_bytes = b"changed-v1"
    candidate["content_sha256"] = hashlib.sha256(new_bytes).hexdigest()
    r = preflight_reuse(candidate, new_bytes, prior_release=prior)
    assert "SAME_VERSION_CHANGED_BYTES" in r["errors"]


def test_source_only_quality_is_not_independent_outcome():
    p = valid_package()
    p["observed_quality"] = {"verification": "PASS_PENDING_WINDOW"}
    assert "INDEPENDENT_OUTCOME_UNPROVEN" in preflight_reuse(p, CONTENT)["errors"]


def test_missing_cold_successor_probe_blocks_candidate():
    p = valid_package()
    p["cold_successor_probe"] = ""
    assert "FIELD_EMPTY:cold_successor_probe" in preflight_reuse(p, CONTENT)["errors"]


def test_default_ranker_is_canonical_calculus_not_an_ad_hoc_score():
    profile = QualityProfile(profile_id="check", version="2.1", objective="responsible reuse")
    pv = PVEstimate(8, 0, 1, 0.2, {k:0.95 for k in ("B","H","C","R")}, 2)
    dims = {k:9.5 for k in ("objective_fit","evidence_sufficiency","applicability","robustness","reversibility","blast_containment","simplicity")}
    conf = {k:0.95 for k in dims}
    base = Candidate("baseline",dims,conf,pv,authorized=True,is_baseline=True,lawful=True,rights_safe=True,privacy_safe=True,safety_safe=True)
    forbidden = Candidate("forbidden",dims,conf,PVEstimate(100,0,0,0,{k:0.99 for k in ("B","H","C","R")},3),authorized=False,lawful=False,rights_safe=True,privacy_safe=True,safety_safe=True)
    result = rank_repair_options([base, forbidden], "baseline", profile)
    bad_row = next(x for x in result["rows"] if x["candidate_id"]=="forbidden")
    assert bad_row["gate"] != "ADMISSIBLE"
    assert result["decision"] != ACT


def test_non_string_scope_fails_closed_instead_of_crashing():
    p = valid_package()
    p["owner_scope"] = ["PRIVATE"]
    result = preflight_reuse(p, CONTENT)
    assert result["status"] == "NOT_READY"
    assert "SCOPE_INVALID" in result["errors"]
