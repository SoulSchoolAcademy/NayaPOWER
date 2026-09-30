#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "BRAIN/04-INTELLIGENCE/GRAPH/0003-GRAPH-RELATIONSHIP-CONTRACT-V2.json"
SEED_PATH = ROOT / "BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json"

def load_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def validate_edge(edge: dict[str, Any], contract: dict[str, Any] | None = None) -> list[str]:
    c = contract or load_contract()
    errors: list[str] = []
    if not edge.get("relationship_id"): errors.append("RELATIONSHIP_ID_REQUIRED")
    if not edge.get("source_id"): errors.append("SOURCE_ID_REQUIRED")
    if not edge.get("target_id"): errors.append("TARGET_ID_REQUIRED")
    if edge.get("relationship_type") not in c["allowed_relationship_types"]: errors.append("UNKNOWN_RELATIONSHIP_TYPE")

    scope = edge.get("owner_scope")
    if not isinstance(scope, dict) or not scope.get("owner_id") or not scope.get("visibility"):
        errors.append("OWNER_SCOPE_REQUIRED")
    elif scope.get("visibility") not in c["owner_scope_contract"]["allowed_visibility"]:
        errors.append("INVALID_VISIBILITY")
    elif scope.get("visibility") == "DERIVED_SHARED" and not edge.get("consent_ref"):
        errors.append("CROSS_OWNER_CONSENT_REQUIRED")

    if edge.get("epistemic_state") not in c["allowed_epistemic_states"]:
        errors.append("INVALID_EPISTEMIC_STATE")
    if edge.get("status") not in c["allowed_status"]:
        errors.append("INVALID_STATUS")

    provenance = edge.get("provenance")
    if not isinstance(provenance, list) or not provenance:
        errors.append("PROVENANCE_REQUIRED")
    evidence = edge.get("evidence_refs")
    if not isinstance(evidence, list):
        evidence = []
    if edge.get("epistemic_state") == "VERIFIED" and not evidence:
        errors.append("VERIFIED_EVIDENCE_REQUIRED")

    vf, vu = edge.get("valid_from"), edge.get("valid_until")
    if vf is not None and vu is not None and str(vf) > str(vu):
        errors.append("INVALID_TEMPORAL_INTERVAL")

    supersedes = edge.get("supersedes_relationship_id")
    if supersedes and supersedes == edge.get("relationship_id"):
        errors.append("INVALID_SUPERSESSION")

    applicability = edge.get("applicability")
    if not isinstance(applicability, dict):
        errors.append("INVALID_APPLICABILITY")
    else:
        state = applicability.get("state")
        if state not in c["applicability_contract"]["allowed_states"]:
            errors.append("INVALID_APPLICABILITY")
        if not isinstance(applicability.get("task_classes"), list) or not isinstance(applicability.get("limitations"), list):
            errors.append("INVALID_APPLICABILITY")

    reason_codes = edge.get("reason_codes")
    if not isinstance(reason_codes, list) or not reason_codes:
        errors.append("REASON_CODES_REQUIRED")
    return list(dict.fromkeys(errors))

def classify_v1_seed_upgrade_gaps(seed_path: Path = SEED_PATH) -> list[dict[str, Any]]:
    seed = json.loads(seed_path.read_text(encoding="utf-8"))
    required_v2 = [
        "owner_scope","evidence_refs","observed_at","valid_from","valid_until",
        "supersedes_relationship_id","consent_ref","applicability","reason_codes"
    ]
    rows = []
    for edge in seed.get("edges", []):
        missing = [k for k in required_v2 if k not in edge]
        rows.append({
            "relationship_id": edge.get("relationship_id"),
            "v1_epistemic_state": edge.get("epistemic_state"),
            "missing_v2_fields": missing,
            "classification": "V1_UPGRADE_REQUIRED" if missing else "V2_SHAPE_COMPLETE",
        })
    return rows

def main() -> int:
    contract = load_contract()
    report = {
        "schema": "naya.graph.relationship.v2.validation-report",
        "contract": str(CONTRACT_PATH.relative_to(ROOT)),
        "seed": str(SEED_PATH.relative_to(ROOT)),
        "seed_upgrade_inventory": classify_v1_seed_upgrade_gaps(),
        "authority_created": False,
        "runtime_claimed": False,
    }
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
