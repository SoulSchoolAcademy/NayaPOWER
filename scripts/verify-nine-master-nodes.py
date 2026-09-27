#!/usr/bin/env python3
"""Dependency-free static conformance gate for the NayaPOWER nine-node kernel."""
from __future__ import annotations
import json, sys
from pathlib import Path

NODE_IDS=[f"MN-{i:02d}" for i in range(1,10)]
NODE_KEYS=["SELF","LAW","ACT","KNOW","PROVE","CONNECT","VERIFY","LEARN","EVOLVE"]
CONTRACTS={f"{i:02d}" for i in range(27)}
TRANSITIONS={
 ("PROPOSED","ACTIVE"),("PROPOSED","CONFLICTED"),("ACTIVE","CONFLICTED"),
 ("ACTIVE","SUPERSEDED"),("ACTIVE","RETIRED"),("CONFLICTED","ACTIVE"),
 ("CONFLICTED","SUPERSEDED"),("SUPERSEDED","RETIRED")
}
INPUTS={"identity","intent","state","context","authority","intelligence","evidence","relationships"}
OUTPUTS={"understanding","decision_context","action_context","evidence_context","learning_context","successor_context"}

def fail(msg:str)->int:
    print("FAIL:",msg,file=sys.stderr); return 1

def main()->int:
    if len(sys.argv)!=2: return fail("usage: verify-nine-master-nodes.py PATH")
    try: d=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except Exception as e: return fail(f"invalid JSON: {e}")
    nodes=d.get("nodes")
    if not isinstance(nodes,list) or len(nodes)!=9: return fail("kernel must contain exactly 9 nodes")
    ids=[n.get("id") for n in nodes]; keys=[n.get("key") for n in nodes]; nums=[n.get("node_no") for n in nodes]
    if ids!=NODE_IDS: return fail("kernel node IDs/order must be MN-01..MN-09")
    if keys!=NODE_KEYS: return fail("kernel node keys/order are invalid")
    if nums!=list(range(1,10)): return fail("node_no values must be 1..9")
    owner=d.get("contract_primary_ownership")
    if not isinstance(owner,dict) or set(owner)!=CONTRACTS: return fail("primary ownership must cover exactly contracts 00-26")
    declared={}
    for n in nodes:
        for c in n.get("primary_contracts",[]):
            if c in declared: return fail(f"contract {c} has multiple primary owners")
            declared[c]=n["id"]
    if declared!=owner: return fail("node primary_contracts do not match primary ownership")
    triads=d.get("triads",[])
    if len(triads)!=3 or sorted(x for t in triads for x in t.get("nodes",[]))!=NODE_IDS: return fail("triads must partition the nine Nodes")
    if d.get("runtime_flow")!=NODE_IDS+["MN-01"]: return fail("runtime flow must traverse MN-01..MN-09 and return to MN-01")
    if set(d.get("required_input_fields",[]))!=INPUTS: return fail("required input envelope changed")
    if set(d.get("required_output_fields",[]))!=OUTPUTS: return fail("required output envelope changed")
    mn=" ".join(d.get("global_invariants",{}).get("must_not",[])).lower()
    for phrase in ("self-authorize","self-ratify","competing canonical intelligence store"):
        if phrase not in mn: return fail(f"missing forbidden invariant: {phrase}")
    sm=d.get("state_machine",{})
    if sm.get("states")!=["PROPOSED","ACTIVE","CONFLICTED","SUPERSEDED","RETIRED"]: return fail("state machine states changed")
    if {tuple(x) for x in sm.get("allowed_transitions",[])}!=TRANSITIONS: return fail("state machine transitions changed")
    if [g.get("id") for g in d.get("kernel_gates",[])]!=["K1","K2","K3","K4","K5","K6"]: return fail("kernel gates K1-K6 are required")
    print("PASS: nine Master Node kernel is structurally and normatively valid")
    return 0
if __name__=="__main__": raise SystemExit(main())
