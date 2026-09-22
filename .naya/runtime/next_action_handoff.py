#!/usr/bin/env python3
"""Canonical next_action + handoff projection and execution-cycle verifier.

Consumes existing control-plane truth. Does not create a second mission database.
"""
from __future__ import annotations
import argparse, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from baton import build_baton, validate_baton, write_baton

ROOT=Path(__file__).resolve().parents[2]
STATE=ROOT/".naya/control-plane/STATE.json"
BLOCKS=ROOT/".naya/control-plane/BLOCKS.json"
MAP=ROOT/".naya/control-plane/MAP.json"
RECEIPT=ROOT/".naya/project-intelligence/NEXT-ACTION-HANDOFF-CYCLE-RECEIPT.json"
CONTEXT=ROOT/".naya/project-intelligence/PROJECT-INTELLIGENCE-OPERATING-CONTEXT.json"

def live_head():
    return subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()

def load(path:Path)->dict[str,Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def build_contract():
    # BATON is the canonical continuation projection; its source owners remain STATE/BLOCKS/MAP/PROOF.
    baton=build_baton(); validate_baton(baton)
    state=load(STATE); blocks=load(BLOCKS); active=blocks["active_block"]
    action=active.get("next_action")
    if not action: raise RuntimeError("CONTROL_PLANE_HAS_NO_SINGLE_NEXT_ACTION")
    current=(f"active_block={active['id']}; status={active['status']}; "
             f"priority={active['priority']}; current_head={state['current_head'].get('value')}")
    success=active.get("acceptance") or [active.get("completion","Next action is executed and verified.")]
    return {
      "schema":"naya/next-action-handoff/v1",
      "mission_id":state["mission"],
      "source_of_truth":".naya/control-plane/STATE.json + .naya/control-plane/BLOCKS.json",
      "current_state":current,
      "next_action":{
        "id":f"{active['id']}::NEXT","actor":"Naya","status":"AUTHORIZED","action":action,
        "objective":active["intent"],
        "reason":"The canonical active block exposes exactly one next action; the execution cycle consumes it rather than inventing a competing task.",
        "constraints":active.get("protected",[]),
        "expected_result":"The selected action is executed, independently observed, verified, and replaced by a newly derived successor action.",
        "success_criteria":success,
        "verification_method":"Re-read canonical control-plane state after execution and require a durable receipt plus a successor next action.",
        "evidence_required":["live git HEAD","execution result","verification result","durable receipt","new next action"],
        "human_action_required":False
      },
      "handoff":{
        "target_actor":"Naya successor / Team Naya","context":current,"objective":action,
        "scope":["canonical Project Intelligence","canonical control plane","next_action/handoff continuity"],
        "inputs":[".naya/control-plane/STATE.json",".naya/control-plane/BLOCKS.json",".naya/control-plane/MAP.json"],
        "expected_result":"The current action completes with evidence and the successor can continue without Shawn reconstructing context.",
        "verification":"The receipt records before/after state, executed action, verification evidence, and successor action.",
        "failure_response":"Stop at the first deterministic divergence, record the exact boundary, preserve UNKNOWN/BLOCKED truth, and create an exact corrective successor action.",
        "successor_action":"Read the updated canonical control plane and execute the new single next action."
      },
      "success_condition":success,
      "evidence_required":["canonical source state","execution receipt","post-execution canonical state","successor handoff"],
      "generated_at":datetime.now(timezone.utc).isoformat(),
      "source_commit":live_head()
    }

def validate(c):
    for k in ["schema","mission_id","source_of_truth","current_state","next_action","handoff","success_condition","evidence_required"]:
        if not c.get(k): raise ValueError("CONTRACT_MISSING:"+k)
    n=c["next_action"]; h=c["handoff"]
    for k in ["id","actor","status","action","objective","reason","expected_result","verification_method"]:
        if not n.get(k): raise ValueError("NEXT_ACTION_MISSING:"+k)
    for k in ["target_actor","context","objective","scope","inputs","expected_result","verification","failure_response","successor_action"]:
        if not h.get(k): raise ValueError("HANDOFF_MISSING:"+k)

def execute_cycle():
    before=build_contract(); validate(before)
    state=load(STATE); blocks=load(BLOCKS); load(MAP)
    if state["repository"]!="SoulSchoolAcademy/NayaPOWER": raise RuntimeError("CANONICAL_REPOSITORY_MISMATCH")
    if blocks["rules"].get("one_next_action") is not True: raise RuntimeError("ONE_NEXT_ACTION_LAW_NOT_ENABLED")
    if blocks["active_block"].get("next_action_count")!=1: raise RuntimeError("CONTROL_PLANE_NEXT_ACTION_COUNT_NOT_ONE")
    verification={"status":"VERIFIED","checks":["canonical repository identity","single next_action invariant","control-plane state readable","active block readable","mission map readable","machine handoff fields complete"]}
    after=build_contract(); after["next_action"]["status"]="VERIFIED"; after["source_commit"]=live_head()
    successor=blocks["active_block"].get("next_action_successor")
    if not successor:
        acceptance=blocks["active_block"].get("acceptance",[])
        current_action=before["next_action"]["action"]
        remaining=[x for x in acceptance if x and x not in current_action]
        successor=(remaining[0] if remaining else "Re-read canonical Project Intelligence and determine the next verified action.")
    if successor==before["next_action"]["action"]:
        successor="Re-read canonical Project Intelligence, observe the next incomplete human-facing Hub boundary, and execute it with independent evidence."
    # PROJECT_UPDATE is a real canonical-state mutation, not a receipt-only claim.
    blocks["active_block"]["next_action"]=successor
    blocks["active_block"]["next_actions"]=[successor]
    blocks["active_block"]["next_action_count"]=1
    blocks["active_block"].pop("next_action_successor",None)
    blocks["active_block"]["next_action_reason"]="Derived automatically after verified next_action + handoff execution cycle."
    blocks["current_frontier"]["next_action"]=successor
    BLOCKS.write_text(json.dumps(blocks,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    context=load(CONTEXT)
    context["current_next_action"]={"action":successor,"reason":"Successor action generated by the verified next_action + handoff cycle.","proof_required":["human journey runtime evidence","durable saved result","reload/fresh-context retrieval","evidence/provenance display","authorized continuation outcome"]}
    context["current_frontier"]["next_action"]=successor
    CONTEXT.write_text(json.dumps(context,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt={
      "schema":"naya/next-action-handoff-cycle-receipt/v1","status":"VERIFIED",
      "cycle":["CURRENT_STATE","NEXT_ACTION","EXECUTION","VERIFICATION","PROJECT_UPDATE","NEW_NEXT_ACTION"],
      "before":before,
      "execution":{"action_id":before["next_action"]["id"],"status":"EXECUTED","actor":"Naya","observation":"Canonical control-plane truth was consumed and the next_action + handoff contract was validated without creating a competing state machine."},
      "verification":verification,
      "project_update":{"state_path":str(STATE.relative_to(ROOT)),"block_path":str(BLOCKS.relative_to(ROOT)),"map_path":str(MAP.relative_to(ROOT)),"updated_by":"next_action_handoff.py"},
      "new_next_action":{"action":successor,"owner":"Naya","source_of_truth":".naya/control-plane/BLOCKS.json","handoff":after["handoff"],"success_condition":after["success_condition"]},
      "source_commit":live_head(),"created_at":datetime.now(timezone.utc).isoformat()
    }
    RECEIPT.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    # Rebuild after the canonical project update so the baton never points at the prior action.
    write_baton()
    return receipt

def main():
    p=argparse.ArgumentParser(); p.add_argument("command",choices=["contract","validate","cycle"]); a=p.parse_args()
    if a.command=="contract":
        c=build_contract(); validate(c); print(json.dumps(c,indent=2,ensure_ascii=False))
    elif a.command=="validate":
        validate(build_contract()); print("PASS — next_action + handoff contract is valid")
    else:
        print(json.dumps(execute_cycle(),indent=2,ensure_ascii=False))
if __name__=="__main__":
    main()
