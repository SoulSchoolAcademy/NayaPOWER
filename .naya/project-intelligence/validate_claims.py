#!/usr/bin/env python3
"""Fail-closed validator for the NayaNET first-class claim contract."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SCHEMA=ROOT/".naya/project-intelligence/claim.schema.json"
FIXTURES=ROOT/".naya/project-intelligence/claims/fixtures.json"
GREEN={"VERIFIED","RUNTIME_PROVEN","PRODUCTION_PROVEN"}
NON_GREEN={"UNKNOWN","CONFLICTED","STALE","BLOCKED","FAILED","SUPERSEDED"}
TRUTH={"DOCUMENTED","IMPLEMENTED","VERIFIED","RUNTIME_PROVEN","PRODUCTION_PROVEN","UNKNOWN","CONFLICTED","STALE","BLOCKED","FAILED","SUPERSEDED"}

def fail(msg): raise AssertionError(msg)

def dt(v):
    try: return datetime.fromisoformat(v.replace("Z","+00:00"))
    except Exception: fail("invalid ISO-8601 timestamp")

def validate(c):
    for k in ["claim_id","subject","assertion","source","scope","time","truth_state","evidence","supersession","confidence","limitations"]:
        if k not in c: fail("missing required field: "+k)
    if not c["claim_id"].startswith("CLM-"): fail("claim_id must use CLM- namespace")
    if c["scope"].get("project")!="NAYANET": fail("claim scope must bind to NAYANET")
    if c["truth_state"] not in TRUTH: fail("invalid truth_state")
    if not isinstance(c["evidence"],list) or not c["evidence"]: fail("every claim requires at least one evidence item")
    for e in c["evidence"]:
        for k in ("evidence_id","kind","ref","supports"):
            if not e.get(k): fail("evidence missing "+k)
    for k in ("asserted_at","observed_at","valid_from"): dt(c["time"][k])
    if c["time"].get("valid_until") is not None: dt(c["time"]["valid_until"])
    if not 0 <= c["confidence"] <= 1: fail("confidence outside 0..1")
    if c["truth_state"] in GREEN and not c["limitations"]: fail("green claims require explicit limitations")
    if c["truth_state"] in {"UNKNOWN","STALE","CONFLICTED","BLOCKED","FAILED"} and c["confidence"]>=1:
        fail("uncertain truth state cannot carry absolute confidence")
    return True

def main():
    schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
    if schema.get("$id")!="nayanet/project-intelligence/claim/v1": fail("wrong schema identity")
    data=json.loads(FIXTURES.read_text(encoding="utf-8"))
    for c in data["valid"]: validate(c)
    for item in data["invalid"]:
        try: validate(item["claim"])
        except AssertionError: continue
        fail("invalid fixture accepted: "+item["case"])
    print(json.dumps({
      "status":"GREEN",
      "schema":schema["$id"],
      "valid_fixtures":len(data["valid"]),
      "invalid_fixtures_rejected":len(data["invalid"]),
      "non_green_promotion_guard":"GREEN"
    },indent=2))

if __name__=="__main__":
    try: main()
    except AssertionError as e:
        print("CLAIMS_CONTRACT=RED")
        print("FIRST_DIVERGENCE="+str(e))
        raise SystemExit(1)
