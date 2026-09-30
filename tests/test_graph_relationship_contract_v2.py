import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("graph_v2", ROOT / "tools" / "validate_graph_relationship_v2.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def edge():
    return {
        "relationship_id": "REL-1",
        "source_id": "IB-A",
        "target_id": "IB-B",
        "relationship_type": "SUPPORTS",
        "owner_scope": {"owner_id": "owner-a", "visibility": "PRIVATE"},
        "epistemic_state": "VERIFIED",
        "status": "ACTIVE",
        "provenance": ["event-1"],
        "evidence_refs": ["evidence-1"],
        "created_at": "2026-09-30T00:00:00Z",
        "observed_at": "2026-09-30T00:00:00Z",
        "valid_from": "2026-09-30T00:00:00Z",
        "valid_until": None,
        "supersedes_relationship_id": None,
        "consent_ref": None,
        "applicability": {"state": "APPLICABLE", "task_classes": ["provenance_sensitive"], "limitations": ["bounded"]},
        "reason_codes": ["EVIDENCE_SUPPORTED"],
    }

def test_valid_edge_passes():
    assert mod.validate_edge(edge()) == []

def test_unknown_type_fails_closed():
    x=edge(); x["relationship_type"]="MAGICALLY_AUTHORIZES"
    assert "UNKNOWN_RELATIONSHIP_TYPE" in mod.validate_edge(x)

def test_missing_provenance_fails_closed():
    x=edge(); x["provenance"]=[]
    assert "PROVENANCE_REQUIRED" in mod.validate_edge(x)

def test_verified_requires_evidence():
    x=edge(); x["evidence_refs"]=[]
    assert "VERIFIED_EVIDENCE_REQUIRED" in mod.validate_edge(x)

def test_cross_owner_shared_requires_consent():
    x=edge(); x["owner_scope"]["visibility"]="DERIVED_SHARED"; x["consent_ref"]=None
    assert "CROSS_OWNER_CONSENT_REQUIRED" in mod.validate_edge(x)

def test_invalid_temporal_interval_fails():
    x=edge(); x["valid_from"]="2026-10-02T00:00:00Z"; x["valid_until"]="2026-10-01T00:00:00Z"
    assert "INVALID_TEMPORAL_INTERVAL" in mod.validate_edge(x)

def test_self_supersession_fails():
    x=edge(); x["supersedes_relationship_id"]="REL-1"
    assert "INVALID_SUPERSESSION" in mod.validate_edge(x)

def test_applicability_is_required_and_bounded():
    x=edge(); x["applicability"]={"state":"MAYBE","task_classes":[],"limitations":[]}
    assert "INVALID_APPLICABILITY" in mod.validate_edge(x)

def test_v1_seed_is_classified_not_silently_promoted():
    rows=mod.classify_v1_seed_upgrade_gaps()
    assert rows
    assert all(r["classification"]=="V1_UPGRADE_REQUIRED" for r in rows)
    assert all("owner_scope" in r["missing_v2_fields"] for r in rows)
    assert all("applicability" in r["missing_v2_fields"] for r in rows)

def test_contract_never_grants_authority():
    c=mod.load_contract()
    assert c["authority_boundary"]["graph_grants_authority"] is False
    assert "retrieved=>authorized" in c["authority_boundary"]["forbidden_inference"]
