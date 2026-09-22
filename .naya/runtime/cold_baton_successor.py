#!/usr/bin/env python3
"""Cold-successor proof for the canonical Current Naya Baton.

The consumer restores continuation from BATON.json with conversation memory
explicitly empty. Canonical STATE/BLOCKS/MAP/PROOF are used only to reconcile
the derived baton, never as conversational history.
"""
from __future__ import annotations
import hashlib, json, subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BATON=ROOT/".naya/control-plane/BATON.json"
STATE=ROOT/".naya/control-plane/STATE.json"
BLOCKS=ROOT/".naya/control-plane/BLOCKS.json"
MAP=ROOT/".naya/control-plane/MAP.json"
PROOF=ROOT/".naya/control-plane/PROOF.json"
RECEIPT=ROOT/".naya/project-intelligence/BATON-COLD-SUCCESSOR-PROOF.json"

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def head(): return subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()

def main():
    baton=load(BATON)
    state=load(STATE); blocks=load(BLOCKS); map_data=load(MAP); proof=load(PROOF)
    active=blocks["active_block"]

    assert baton["status"]=="CANONICAL", "BATON_NOT_CANONICAL"
    assert baton["repository"]==state["repository"]=="SoulSchoolAcademy/NayaPOWER", "REPOSITORY_MISMATCH"
    assert baton["source_of_truth"]["live_state"]==".naya/control-plane/STATE.json"
    assert baton["source_of_truth"]["active_block"]==".naya/control-plane/BLOCKS.json"
    assert baton["source_of_truth"]["mission_map"]==".naya/control-plane/MAP.json"
    assert baton["source_of_truth"]["proof"]==".naya/control-plane/PROOF.json"
    assert map_data["status"]=="CANONICAL" and proof["status"]=="CANONICAL", "SOURCE_AUTHORITY_INVALID"

    recovered_state={
        "mission":baton["current_state"]["mission"],
        "north_star":baton["current_state"]["north_star"],
        "active_program":baton["current_state"]["active_program"],
        "active_block":baton["current_state"]["active_block"],
        "active_block_status":baton["current_state"]["active_block_status"],
    }
    source_state={
        "mission":state["mission"],
        "north_star":state["north_star"],
        "active_program":state.get("active_program",state.get("priority")),
        "active_block":state["current_block"],
        "active_block_status":state["current_block_status"],
    }
    assert recovered_state==source_state, "COLD_STATE_RECONSTRUCTION_MISMATCH"

    recovered_action=baton["next_action"]["action"]
    assert baton["next_action"]["count"]==1, "COLD_BATON_NEXT_ACTION_COUNT_NOT_ONE"
    assert recovered_action==state["single_next_action"]==active["next_action"], "COLD_EXACT_NEXT_ACTION_MISMATCH"

    successor_prompt=baton["successor_prompt"]["prompt"]
    assert successor_prompt and baton["successor_prompt"]["do_not"], "SUCCESSOR_PROMPT_INCOMPLETE"

    receipt={
      "schema":"naya/baton-cold-successor-proof/v1",
      "status":"PROVEN",
      "claim_scope":"BATON -> COLD NAYA -> EXACT CURRENT STATE -> EXACT ONE NEXT ACTION",
      "conversation_memory":"EMPTY",
      "conversational_archaeology":False,
      "archaeology_sources_used":[],
      "baton_source":".naya/control-plane/BATON.json",
      "source_authorities_used_for_reconciliation":[
        ".naya/control-plane/STATE.json",
        ".naya/control-plane/BLOCKS.json",
        ".naya/control-plane/MAP.json",
        ".naya/control-plane/PROOF.json"
      ],
      "live_head":head(),
      "recovered_current_state":recovered_state,
      "recovered_one_next_action":{
        "count":1,
        "status":baton["next_action"]["status"],
        "action":recovered_action,
        "source":baton["next_action"]["source"],
      },
      "exact_match_checks":{
        "mission":recovered_state["mission"]==source_state["mission"],
        "active_block":recovered_state["active_block"]==active["id"],
        "active_block_status":recovered_state["active_block_status"]==active["status"],
        "next_action":recovered_action==state["single_next_action"],
        "next_action_count":baton["next_action"]["count"]==1,
        "map_canonical":map_data["status"]=="CANONICAL",
        "proof_canonical":proof["status"]=="CANONICAL",
      },
      "successor_prompt":successor_prompt,
      "interpretation":"A fresh successor can recover the current mission/state and exactly one authorized next action from the canonical baton without conversational history. This proof does not claim that an external LLM independently executed the action.",
      "baton_sha256":hashlib.sha256(BATON.read_bytes()).hexdigest(),
      "created_at":datetime.now(timezone.utc).isoformat()
    }
    RECEIPT.parent.mkdir(parents=True,exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2,ensure_ascii=False))

if __name__=="__main__": main()
