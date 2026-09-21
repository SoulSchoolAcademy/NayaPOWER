#!/usr/bin/env python3
"""Fail-closed temporal truth fixture validator."""
from datetime import datetime,timezone
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
F=ROOT/".naya/project-intelligence/temporal-truth-fixtures.json"
def d(s): return datetime.fromisoformat(s.replace("Z","+00:00"))
def classify(case):
    now=d(case["as_of"])
    current=[]
    for c in case["claims"]:
        start=d(c["valid_from"])
        end=d(c["valid_until"]) if c.get("valid_until") else None
        if end and end < now: continue
        if start <= now: current.append(c)
    if not current: return "STALE"
    if len({c["assertion"] for c in current})>1: return "CONFLICTED"
    return "CURRENT"
data=json.loads(F.read_text())
for case in data["cases"]:
    got=classify(case)
    if got!=case["expected"]: raise SystemExit(f"TEMPORAL_TRUTH=RED FIRST_DIVERGENCE={case['id']} expected={case['expected']} got={got}")
print(json.dumps({"status":"GREEN","cases":len(data["cases"]),"states":["CURRENT","STALE","CONFLICTED"],"rule":"validity is evaluated against explicit as_of; assertion/observation time cannot masquerade as event validity"},indent=2))
