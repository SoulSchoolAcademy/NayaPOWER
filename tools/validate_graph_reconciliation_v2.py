#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/"BRAIN/04-INTELLIGENCE/GRAPH/0005-GRAPH-RECONCILIATION-V2-ACCEPTANCE.json"
NOW="2026-09-30T03:00:00Z"
CONFLICT_TYPES={"CONTRADICTS","INVALIDATES"}

def current_for_task(edge:dict[str,Any], task_class:str)->tuple[bool,str]:
    if edge.get("status")!="ACTIVE":
        return False,"STATUS_NOT_ACTIVE"
    if edge.get("epistemic_state")!="VERIFIED":
        return False,"EPISTEMIC_STATE_NOT_VERIFIED"
    if not edge.get("provenance") or not edge.get("evidence_refs"):
        return False,"EVIDENCE_REQUIRED"
    vf=edge.get("valid_from")
    vu=edge.get("valid_until")
    if vf and str(vf)>NOW:
        return False,"FUTURE_EFFECTIVE"
    if vu and str(vu)<NOW:
        return False,"EXPIRED"
    app=edge.get("applicability") or {}
    if app.get("state")!="APPLICABLE":
        return False,"NOT_APPLICABLE"
    if task_class not in (app.get("task_classes") or []):
        return False,"TASK_CLASS_MISMATCH"
    return True,"CURRENT"

def reconcile(edges:list[dict[str,Any]], task_class:str)->dict[str,Any]:
    selected=[]
    excluded=[]
    current=[]
    by_id={e["relationship_id"]:e for e in edges}
    for edge in edges:
        ok,reason=current_for_task(edge,task_class)
        if ok:
            current.append(edge)
        else:
            excluded.append(edge["relationship_id"])
    superseded_ids={e.get("supersedes_relationship_id") for e in current if e.get("supersedes_relationship_id")}
    if superseded_ids:
        excluded.extend([rid for rid in superseded_ids if rid in by_id and rid not in excluded])
        current=[e for e in current if e["relationship_id"] not in superseded_ids]

    conflict_edges=[e for e in current if e.get("relationship_type") in CONFLICT_TYPES]
    non_conflict=[e for e in current if e.get("relationship_type") not in CONFLICT_TYPES]
    unresolved = bool(conflict_edges and non_conflict and not any(e.get("supersedes_relationship_id") for e in conflict_edges))
    if unresolved:
        return {"status":"UNRESOLVED_CONFLICT","selected":[],"excluded":sorted(set(excluded))}

    selected=[e["relationship_id"] for e in current]
    if not selected:
        return {"status":"NO_APPLICABLE_CONTEXT","selected":[],"excluded":sorted(set(excluded))}
    return {"status":"RESOLVED","selected":selected,"excluded":sorted(set(excluded))}

def main()->int:
    data=json.loads(FIXTURE.read_text(encoding="utf-8"))
    failures=[]
    for case in data["cases"]:
        got=reconcile(case["edges"],case["task_class"])
        if got["status"]!=case["expect_status"] or sorted(got["selected"])!=sorted(case["expect_selected"]) or sorted(got["excluded"])!=sorted(case["expect_excluded"]):
            failures.append({"case":case["name"],"expected":{"status":case["expect_status"],"selected":case["expect_selected"],"excluded":case["expect_excluded"]},"actual":got})
    print(json.dumps({"schema":"naya.graph.reconciliation.v2.acceptance-report","passed":not failures,"failures":failures},indent=2))
    return 1 if failures else 0

if __name__=="__main__":
    raise SystemExit(main())
