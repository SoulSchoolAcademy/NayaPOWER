#!/usr/bin/env python3
"""Regression tests for the next Superbrain intelligence layer."""
from __future__ import annotations
import json,tempfile
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/".naya"/"runtime")); sys.path.insert(0,str(ROOT/".naya"/"memory"))
from canonical_event_store import create_or_replay
from entity_resolution import decide,apply_decision
from contradiction_supersession import apply_supersession
from outbox import transition,success_receipt
import superbrain_health,retrieval_benchmark
BASE={"event_id":"SE-20260825-210000-intelligence-test","effective_at":"2026-08-25T21:00:00+00:00","created_at":"2026-08-25T21:00:00+00:00","title":"Intelligence test","subject":"Superbrain","type":"execution-milestone","event_type":"execution-milestone","project":"Naya Power Superbrain","project_context":{"project_id":"PRJ-NAYAPOWER-SUPERBRAIN","current_daily_project":"Naya Power Superbrain","current_objective":"test intelligence-layer integrity"},"source":{"id":"source-1"},"status":"CANONICAL","representations":{"naya":{"id":"SN-20260825-210000-naya","canonical_event_id":"SE-20260825-210000-intelligence-test","summary":"AI view","lessons":["idempotency matters"],"next_best_actions":["test again"]},"shawn":{"id":"SN-20260825-210000-shawn","canonical_event_id":"SE-20260825-210000-intelligence-test","summary":"Human view","lessons":["history matters"],"next_best_actions":["verify"]}},"verification":{"status":"VERIFIED","receipt":"RCPT-test"},"receipt":{"receipt_id":"RCPT-test"},"delivery":{"state":"VERIFIED"},"continuity":{"learning_status":"LEARNED"},"next_execution":{"path":".naya/handoffs/NEXT-EXECUTION-20260825-SUPERBRAIN-CONTRACT-ENFORCEMENT.md"}}
def test_idempotency():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)/"events"; idx=Path(tmp)/"idempotency.json"; first=create_or_replay(BASE,root,idx); second=create_or_replay(BASE,root,idx)
        assert first["status"]=="CREATED" and second["status"]=="REPLAY" and len(list(root.rglob("*.json")))==1
        changed=json.loads(json.dumps(BASE)); changed["representations"]["naya"]["summary"]="changed"; assert create_or_replay(changed,root,idx)["status"]=="CONFLICT"
def test_resolution_and_supersession():
    incoming=json.loads(json.dumps(BASE)); incoming["event_id"]="SE-20260825-210001-intelligence-test"; incoming["representations"]["naya"]["canonical_event_id"]=incoming["event_id"]; incoming["representations"]["shawn"]["canonical_event_id"]=incoming["event_id"]; result=decide(BASE,incoming); assert result["action"] in {"UPDATE","REVIEW","CREATE"}; assert apply_decision(BASE,incoming,"SUPERSEDE")["preserve_history"] is True
    old,new=apply_supersession(BASE,incoming,{"source":"test-evidence","status":"VERIFIED"}); assert old["status"]=="SUPERSEDED" and incoming["event_id"] in old["relationships"]["superseded_by"] and old["event_id"] in new["relationships"]["supersedes"]
def test_outbox():
    assert transition("PENDING","ATTEMPTED")["valid"] and transition("ATTEMPTED","FAILED")["valid"] and transition("FAILED","RETRY")["valid"] and transition("RETRY","ATTEMPTED")["valid"]
    try: transition("PENDING","DELIVERED")
    except ValueError: pass
    else: raise AssertionError("invalid direct delivery must fail")
    assert success_receipt("A-1","DELIVERED")["delivery_state"]=="DELIVERED"
def test_health_and_baseline():
    health=superbrain_health.report(); assert "canonical_event_count" in health and "receipt_completeness" in health and "meaningful_execution_metrics" in health
    baseline=retrieval_benchmark.run(); assert baseline["semantic_vector_engine"] is False
def main():
    test_idempotency();test_resolution_and_supersession();test_outbox();test_health_and_baseline();print("PASS — intelligence-layer, idempotency, resolution, supersession, outbox, health, and retrieval-baseline tests GREEN")
if __name__=="__main__": main()
