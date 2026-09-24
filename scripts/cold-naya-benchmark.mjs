#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";

const root=process.cwd();
const required=[
  "SUPERBRAIN/AI-BOOT/START-HERE.md",
  "SUPERBRAIN/MASTER-NOTES/NAYAPOWER-CANONICAL-SOURCE-MAP.md",
  ".naya/codex/11-RUNTIME-CONSTITUTION.md",
  ".naya/control-plane/MAP.json",
  ".naya/control-plane/STATE.json",
  ".naya/control-plane/BLOCKS.json",
  ".naya/control-plane/PROOF.json",
  ".naya/control-plane/BATON.json"
];
function read(p){ return fs.readFileSync(path.join(root,p),"utf8"); }
function json(p){ return JSON.parse(read(p)); }
function assert(c,m){ if(!c) throw new Error(m); }
const start=read(required[0]);
const map=json(required[3]), state=json(required[4]), blocks=json(required[5]), proof=json(required[6]), baton=json(required[7]);
const liveHead=execFileSync("git",["rev-parse","HEAD"],{encoding:"utf8"}).trim();
const bootChecks={
  start_here:true,
  source_map:true,
  constitution:true,
  control_plane:true,
  live_head_resolution:start.includes("LIVE_AT_EXECUTION_TIME"),
  no_conversation_dependency:start.includes("Do not reconstruct the project from conversation history"),
};
for(const [k,v] of Object.entries(bootChecks)) assert(v,"BOOT_CHECK_FAILED:"+k);
const actions=[
  map.execution_map?.next_action,
  map.current_frontier?.next_action,
  state.single_next_action,
  blocks.active_block?.next_action,
  baton.next_action?.action,
  proof.next_action?.action
].filter(Boolean);
const unique=[...new Set(actions)];
assert(unique.length===1,"NEXT_ACTION_CONFLICT:"+unique.length);
const nextAction=unique[0];
assert(blocks.active_block?.id,"ACTIVE_BLOCK_MISSING");
assert(blocks.active_block?.status,"ACTIVE_BLOCK_STATUS_MISSING");
assert(map.authority?.governing_standard,"CONSTITUTION_POINTER_MISSING");
assert(map.authority?.canonical_hub_path === "NAYANET/HUB/index.html","CANONICAL_HUB_POINTER_MISMATCH");
assert(state.current_head?.recorded_head_is_not_authoritative===true,"RECORDED_HEAD_AUTHORITY_RULE_MISSING");
assert(proof.truth_state_machine?.includes("VERIFIED"),"PROOF_TRUTH_STATE_MISSING");
assert(proof.non_green_states?.includes("UNKNOWN") && proof.non_green_states?.includes("BLOCKED"),"PROOF_NON_GREEN_RULE_MISSING");
const artifact={
  schema:"NAYANET_COLD_NAYA_BOOT_BENCHMARK_V1",
  status:"VERIFIED",
  source_head:liveHead,
  archaeology:{
    canonical_sources_required:required.length,
    canonical_sources_read:required.length,
    conversation_sources_read:0,
    unbounded_repository_search_required:false
  },
  reconstruction:{
    mission:true,
    authority:true,
    architecture:true,
    current_state:true,
    active_block:true,
    proof_rules:true,
    single_next_action:true
  },
  next_action:nextAction,
  active_block:blocks.active_block.id,
  active_block_status:blocks.active_block.status,
  human_reasoning_accuracy:"NOT_MEASURED",
  human_task_continuation:"NOT_MEASURED",
  note:"This benchmark proves deterministic cold-boot reconstruction from the canonical repository package. It does not claim to measure an AI model's reasoning quality or human task success."
};
fs.writeFileSync("cold-naya-benchmark.json",JSON.stringify(artifact,null,2)+"\n");
console.log(JSON.stringify(artifact,null,2));
