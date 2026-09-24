#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const cp = path.join(root, ".naya", "control-plane");
function readJson(name) { return JSON.parse(fs.readFileSync(path.join(cp, name), "utf8")); }
function liveGit() {
  const head = (process.env.CURRENT_TRUTH_HEAD || execFileSync("git", ["rev-parse", "HEAD"], {encoding:"utf8"})).trim();
  const branch = (process.env.CURRENT_TRUTH_BRANCH || execFileSync("git", ["branch", "--show-current"], {encoding:"utf8"})).trim();
  return {head, branch};
}
function first(...values) { return values.find(v => typeof v === "string" && v.trim()) || null; }
function distinct(values) { return [...new Set(values.filter(Boolean))]; }
function collectSignals(value, prefix="") {
  const out=[]; if (!value || typeof value !== "object") return out;
  for (const [k,v] of Object.entries(value)) {
    const key=prefix ? prefix+"."+k : k;
    if (typeof v === "string" && /(UNKNOWN|BLOCKED|FAILED|STALE|OPEN_PENDING|MISSING|REQUIRES)/i.test(v)) out.push([key,v]);
    else if (Array.isArray(v)) for (const item of v) if (typeof item === "string" && /(UNKNOWN|BLOCKED|FAILED|STALE|OPEN_PENDING|MISSING|REQUIRES)/i.test(item)) out.push([key,item]);
    else if (v && typeof v === "object") out.push(...collectSignals(v,key));
  }
  return out;
}
function render() {
  const MAP=readJson("MAP.json"), STATE=readJson("STATE.json"), BLOCKS=readJson("BLOCKS.json"), PROOF=readJson("PROOF.json"), BATON=readJson("BATON.json");
  const git=liveGit();
  const nextActions=distinct([
    MAP.execution_map?.next_action, MAP.current_frontier?.next_action, MAP.next_action,
    STATE.single_next_action, STATE.next_action?.action,
    BLOCKS.active_block?.next_action, BLOCKS.current_frontier?.next_action,
    BATON.next_action?.action, BATON.current_frontier?.next_action, PROOF.next_action?.action
  ]);
  const currentNext=first(BLOCKS.active_block?.next_action, STATE.single_next_action, MAP.execution_map?.next_action, BATON.next_action?.action, PROOF.next_action?.action);
  const hub=first(MAP.authority?.canonical_hub_path, MAP.intelligent_hub_pre_execution?.canonical_hub, STATE.hub_pre_execution_gate?.canonical_hub);
  const mission=first(MAP.mission, STATE.mission);
  const northStar=first(MAP.north_star, STATE.north_star);
  const activeBlock=first(BLOCKS.active_block?.id, STATE.current_block, MAP.execution_map?.active_block);
  const activeStatus=first(BLOCKS.active_block?.status, STATE.current_block_status);
  const signals=collectSignals({STATE,MAP,BLOCKS,PROOF,BATON}).slice(0,20);
  const lines=[
    `# NayaPOWER - CURRENT TRUTH`,``,
    `> Generated from the canonical control plane at build time. This file is a derived cold-boot aid; it never overrides the constitution, control plane, or live runtime evidence.`,``,
    `- **Live branch:** \`${git.branch || "DETACHED"}\``,
    `- **Live HEAD:** \`${git.head}\``,
    `- **Current truth source:** \`git:HEAD + .naya/control-plane/{MAP,STATE,BLOCKS,PROOF,BATON}.json\``,``,
    `## Who We Are`,``,`NayaPOWER is the governed intelligence operating system for Naya/NayaNET.`,``,
    `## What We Are Building`,``,mission || "UNKNOWN",``,
    `## North Star`,``,northStar || "UNKNOWN",``,
    `## Current Architecture`,``,
    `- **Canonical Hub:** \`${hub || "UNKNOWN"}\``,
    `- **Constitution:** \`${MAP.authority?.governing_standard || "UNKNOWN"}\``,
    `- **Control plane:** \`${MAP.authority?.current_state || ".naya/control-plane/STATE.json"}\``,
    `- **Proof authority:** \`${MAP.truth_owners?.proof_contract || ".naya/control-plane/PROOF.json"}\``,``,
    `## Current State`,``,
    `- **Active block:** ${activeBlock || "UNKNOWN"}`,
    `- **Block status:** ${activeStatus || "UNKNOWN"}`,
    `- **Live repository HEAD:** \`${git.head}\``,
    `- **Recorded control-plane HEAD:** \`${STATE.current_head?.observed_head || "NONE"}\``,
    `- **Recorded HEAD authoritative:** ${STATE.current_head?.recorded_head_is_not_authoritative === false ? "yes" : "no"}`,
    ``,`## Proven`,``,
    `- Control-plane truth sources are explicitly separated by role: MAP / STATE / BLOCKS / PROOF / BATON.`,
    `- Proof contract distinguishes IMPLEMENTED from VERIFIED and VERIFIED from PRODUCTION_PROVEN.`,
    `- Canonical Hub is declared as \`${hub || "UNKNOWN"}\`.`,``,
    `## Unknown / Blocked / Stale Signals`,``,
  ];
  if (signals.length) for (const [k,v] of signals) lines.push(`- **${k}:** ${v.replace(/\n/g," ")}`);
  else lines.push(`- None detected by the compiler's conservative signal scan.`);
  lines.push(``,`## Current Authority`,``,
    `- **Constitution:** \`${MAP.authority?.governing_standard || "UNKNOWN"}\``,
    `- **Current state:** \`${MAP.authority?.current_state || "UNKNOWN"}\``,
    `- **Active block:** \`${activeBlock || "UNKNOWN"}\``,``,
    `## Current Mission / Next Action`,``,
    `- **Single next action:** ${currentNext || "UNKNOWN"}`,
    `- **Next-action conflict:** ${nextActions.length > 1 ? "DETECTED - multiple distinct control-plane next actions exist; do not treat this artifact as resolved authority." : "NOT DETECTED by the canonical surfaces inspected."}`,
    ``,`## Compiler Integrity`,``,
    `- This artifact is derived, not authoritative.`,
    `- Live git identity is resolved at generation time.`,
    `- Historical recorded HEAD values are shown for reconciliation, never substituted for live HEAD.`,
    `- If the compiler detects conflicting next actions, it reports the conflict rather than guessing.`,
    `- The compiler must never turn UNKNOWN, BLOCKED, or STALE into VERIFIED.`,``,
  );
  return lines.join("\n");
}
const output=render();
const target=path.join(root,"CURRENT-TRUTH.md");
if (process.argv.includes("--check")) {
  const existing=fs.existsSync(target)?fs.readFileSync(target,"utf8"):null;
  if (existing!==output) { console.error("CURRENT_TRUTH_STALE"); process.exit(2); }
  console.log("CURRENT_TRUTH_FRESH");
} else {
  fs.writeFileSync(target,output,"utf8");
  console.log("CURRENT_TRUTH_GENERATED");
}