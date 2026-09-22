#!/usr/bin/env python3
"""P1 Cycle A: cold reconstruction baseline.

Frozen task:
Recover mission, active block, and exactly one canonical next action from
STATE + BLOCKS + MAP + PROOF without reading BATON.json or conversation history.

All measurements are local, directly observable process measurements.
"""
from __future__ import annotations
import hashlib, json, time
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCES=[
 ".naya/control-plane/STATE.json",
 ".naya/control-plane/BLOCKS.json",
 ".naya/control-plane/MAP.json",
 ".naya/control-plane/PROOF.json",
]
FROZEN_TASK="Recover mission, active block, and exactly one canonical next action from STATE + BLOCKS + MAP + PROOF without reading BATON.json or conversation history."
TASK_HASH=hashlib.sha256(FROZEN_TASK.encode()).hexdigest()

def main():
    start=time.perf_counter()
    reads=[]
    parsed={}
    for rel in SOURCES:
        p=ROOT/rel
        raw=p.read_bytes()
        reads.append({
            "path":rel,
            "bytes":len(raw),
            "chars":len(raw.decode("utf-8")),
            "sha256":hashlib.sha256(raw).hexdigest(),
        })
        parsed[rel]=json.loads(raw.decode("utf-8"))
    state=parsed[SOURCES[0]]
    blocks=parsed[SOURCES[1]]
    mp=parsed[SOURCES[2]]
    proof=parsed[SOURCES[3]]
    active=blocks["active_block"]
    assert state["repository"]=="SoulSchoolAcademy/NayaPOWER"
    assert mp["status"]=="CANONICAL"
    assert proof["status"]=="CANONICAL"
    assert state["current_block"]==active["id"]
    assert state["current_block_status"]==active["status"]
    assert state["single_next_action"]==active["next_action"]
    assert state["next_action_count"]==1
    assert active["next_action_count"]==1
    elapsed=round((time.perf_counter()-start)*1000,3)
    total_bytes=sum(x["bytes"] for x in reads)
    result={
      "schema":"naya/computation-efficiency-baseline/v1",
      "status":"MEASURED",
      "cycle":"A_BASELINE_COLD_RECONSTRUCTION",
      "frozen_task":FROZEN_TASK,
      "frozen_task_sha256":TASK_HASH,
      "conversation_memory":"EMPTY",
      "retained_task_specific_intelligence_used":False,
      "baton_read":False,
      "sources":reads,
      "resource_measurements":{
        "context_objects":{"value":len(reads),"state":"MEASURED"},
        "context_bytes":{"value":total_bytes,"state":"MEASURED"},
        "retrieval_calls":{"value":0,"state":"MEASURED","note":"No remote retrieval API; local canonical files were read directly."},
        "search_calls":{"value":0,"state":"MEASURED"},
        "tool_calls":{"value":0,"state":"MEASURED"},
        "model_calls":{"value":0,"state":"MEASURED"},
        "tokens":{"value":None,"state":"NOT_CLAIMED"},
        "wall_time_ms":{"value":elapsed,"state":"MEASURED"},
        "human_time_ms":{"value":None,"state":"UNKNOWN"},
        "retries":{"value":0,"state":"MEASURED"},
        "verification_calls":{"value":1,"state":"MEASURED"},
        "duplicate_context_objects":{"value":0,"state":"MEASURED"},
      },
      "reconstruction":{
        "mission":state["mission"],
        "active_block":active["id"],
        "active_block_status":active["status"],
        "next_action_count":1,
        "next_action":state["single_next_action"],
      },
      "verification":{
        "status":"VERIFIED",
        "checks":[
          "repository identity",
          "MAP canonical",
          "PROOF canonical",
          "STATE/BLOCK active block equality",
          "STATE/BLOCK exact next-action equality",
          "exactly-one-next-action invariant",
          "BATON not read"
        ]
      },
      "counterfactual":"NOT_APPLICABLE_FOR_CYCLE_A",
      "avoided_computation":"NOT_CLAIMED",
      "source_head":"RESOLVE_LIVE_GIT_HEAD_AT_EXECUTION",
      "created_at":datetime.now(timezone.utc).isoformat(),
    }
    out=ROOT/".naya/project-intelligence/COMPUTATION-EFFICIENCY-CYCLE-A-BASELINE.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=True))

if __name__=="__main__":
    main()
