#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "BRAIN/04-INTELLIGENCE/GRAPH/0004-GRAPH-SELECTOR-V2-ACCEPTANCE.json"

def evaluate(edge: dict[str, Any], task: dict[str, Any], allowed_types: list[str]) -> tuple[bool, str]:
    if edge.get("owner_id") != task.get("owner_id"):
        return False, "OWNER_MISMATCH"
    if edge.get("target_id") != task.get("target_id"):
        return False, "TARGET_MISMATCH"
    if edge.get("relationship_type") not in allowed_types:
        return False, "RELATIONSHIP_TYPE_NOT_ALLOWED"
    if edge.get("status") != "ACTIVE":
        return False, "STATUS_NOT_ACTIVE"
    if edge.get("epistemic_state") != "VERIFIED":
        return False, "EPISTEMIC_STATE_NOT_VERIFIED"
    if not edge.get("provenance"):
        return False, "PROVENANCE_REQUIRED"
    if not edge.get("evidence_refs"):
        return False, "EVIDENCE_REQUIRED"

    now = str(task.get("now") or "")
    valid_from = edge.get("valid_from")
    valid_until = edge.get("valid_until")
    if valid_from and now and str(valid_from) > now:
        return False, "TEMPORALLY_INVALID"
    if valid_until and now and str(valid_until) < now:
        return False, "TEMPORALLY_INVALID"

    if edge.get("visibility") == "DERIVED_SHARED" and not edge.get("consent_ref"):
        return False, "CONSENT_REQUIRED"

    app = edge.get("applicability") or {}
    if app.get("state") == "UNKNOWN":
        return False, "APPLICABILITY_UNKNOWN"
    if app.get("state") != "APPLICABLE":
        return False, "NOT_APPLICABLE"
    if task.get("task_class") not in (app.get("task_classes") or []):
        return False, "TASK_CLASS_MISMATCH"

    return True, "SELECTED"

def main() -> int:
    data=json.loads(FIXTURE.read_text(encoding="utf-8"))
    failures=[]
    for case in data["cases"]:
        selected, reason=evaluate(case["edge"], data["task"], data["allowed_relationship_types"])
        if selected != case["expect_selected"]:
            failures.append({"case":case["name"],"expected_selected":case["expect_selected"],"actual_selected":selected,"reason":reason})
        expected_reason=case.get("expect_reason")
        if expected_reason and reason != expected_reason:
            failures.append({"case":case["name"],"expected_reason":expected_reason,"actual_reason":reason})
    print(json.dumps({"schema":"naya.graph.selector.v2.acceptance-report","failures":failures,"passed":not failures},indent=2))
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
