#!/usr/bin/env python3
"""Machine-readable Superbrain health metrics with meaningful-execution scope."""
from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
MEMORY=ROOT/".naya"/"memory"; EVENTS=MEMORY/"events"
sys.path.insert(0,str(MEMORY)); sys.path.insert(0,str(ROOT/".naya"/"runtime"))
import smart_notes_v3 as brain
from continuity_enforcement import is_meaningful_execution, load_policy

def completeness(rows, fn): return round(sum(1 for e in rows if fn(e))/len(rows),4) if rows else 1.0

def report()->dict:
    loaded=[]
    raw=brain.load_events()
    for p,e in raw:
        if not e.get("__parse_error__"): loaded.append((p,e))
    ids={e.get("event_id") for _,e in loaded}
    parse_errors=sum(1 for _,e in raw if e.get("__parse_error__"))
    relationships=orphan=0
    for _,e in loaded:
        rel=brain.relationship_map(e)
        for key in ("related","depends_on","supersedes","superseded_by","source_events"):
            vals=brain.normalize_targets(rel.get(key,[]))
            relationships+=len(vals); orphan+=sum(1 for target in vals if target not in ids and not str(target).startswith("EXT:"))
    policy=load_policy()
    meaningful=[e for _,e in loaded if is_meaningful_execution(e,policy)]
    receipt=lambda e: bool((e.get("receipt") or {}).get("receipt_id") or (e.get("verification") or {}).get("receipt") or (e.get("verification") or {}).get("receipt_url"))
    delivery=lambda e: bool((e.get("delivery") or {}).get("state") or (e.get("verification") or {}).get("feed_status"))
    verified=lambda e: (e.get("verification") or {}).get("status")=="VERIFIED"
    all_receipt=completeness([e for _,e in loaded],receipt); all_delivery=completeness([e for _,e in loaded],delivery)
    meaningful_metrics={"count":len(meaningful),"verification_completeness":completeness(meaningful,verified),"receipt_completeness":completeness(meaningful,receipt),"delivery_state_completeness":completeness(meaningful,delivery)}
    return {"schema_version":2,"status":"GREEN" if parse_errors==0 and orphan==0 else "RED","canonical_event_count":len(ids),"parse_error_count":parse_errors,"relationship_reference_count":relationships,"orphan_relationship_count":orphan,"verified_event_count":sum(1 for _,e in loaded if verified(e)),"receipt_completeness":all_receipt,"delivery_state_completeness":all_delivery,"all_event_metrics":{"receipt_completeness":all_receipt,"delivery_state_completeness":all_delivery},"meaningful_execution_metrics":meaningful_metrics,"derived_indexes":{"index_exists":(EVENTS/"INDEX.json").exists(),"validation_report_exists":(MEMORY/"VALIDATION-REPORT.json").exists(),"relationship_graph_exists":(MEMORY/"RELATIONSHIP-GRAPH.json").exists()},"note":"Overall health does not equate non-meaningful historical events with completed executions; continuity completeness is measured separately for meaningful executions."}
if __name__=="__main__": print(json.dumps(report(),indent=2,ensure_ascii=False))
