#!/usr/bin/env python3
"""Canonical Current Naya Baton builder and validator.

The baton is a derived continuation artifact. STATE, BLOCKS, MAP and PROOF
remain the authoritative owners of their respective truths.
"""
from __future__ import annotations
import argparse, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PATHS = {
    "state": ROOT / ".naya/control-plane/STATE.json",
    "blocks": ROOT / ".naya/control-plane/BLOCKS.json",
    "map": ROOT / ".naya/control-plane/MAP.json",
    "proof": ROOT / ".naya/control-plane/PROOF.json",
    "baton": ROOT / ".naya/control-plane/BATON.json",
    "hub": ROOT / "NAYANET/HUB/index.html",
}

def live_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def build_baton() -> dict[str, Any]:
    state = load(PATHS["state"])
    blocks = load(PATHS["blocks"])
    map_data = load(PATHS["map"])
    proof = load(PATHS["proof"])
    active = blocks["active_block"]

    if state.get("repository") != "SoulSchoolAcademy/NayaPOWER":
        raise RuntimeError("CANONICAL_REPOSITORY_MISMATCH")
    if state.get("current_block") != active.get("id"):
        raise RuntimeError("STATE_BLOCK_ACTIVE_BLOCK_MISMATCH")
    if state.get("single_next_action") != active.get("next_action"):
        raise RuntimeError("STATE_BLOCK_NEXT_ACTION_MISMATCH")
    if state.get("next_action_count") != 1 or active.get("next_action_count") != 1:
        raise RuntimeError("ONE_NEXT_ACTION_LAW_NOT_SATISFIED")

    next_action = active["next_action"]
    acceptance = active.get("acceptance") or [active.get("completion", "Next action is executed and verified.")]
    mission = state["mission"]
    north_star = state.get("north_star")
    active_program = state.get("active_program", state.get("priority"))

    baton = {
        "$schema": "naya/control-plane/baton/v1",
        "status": "CANONICAL",
        "repository": state["repository"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_of_truth": {
            "identity": ".naya/control-plane/CANONICAL-IDENTITY-REGISTRY.json",
            "live_state": ".naya/control-plane/STATE.json",
            "active_block": ".naya/control-plane/BLOCKS.json",
            "mission_map": ".naya/control-plane/MAP.json",
            "proof": ".naya/control-plane/PROOF.json",
            "history": "NAYA/ACTIVITY/ and execution receipts",
        },
        "source_snapshot": {
            "live_head": live_head(),
            "state_status": state.get("status"),
            "map_status": map_data.get("status"),
            "proof_status": proof.get("status"),
            "state_block": state.get("current_block"),
            "block_next_action": next_action,
            "canonical_hub_source_sha": subprocess.check_output(["git","rev-parse","HEAD:NAYANET/HUB/index.html"],cwd=ROOT,text=True).strip(),
        },
        "current_state": {
            "rule": "Resolve live Git HEAD at execution time; STATE.json owns canonical operational current state.",
            "mission": mission,
            "north_star": north_star,
            "active_program": active_program,
            "active_block": active["id"],
            "active_block_status": active["status"],
        },
        "current_intelligence": {
            "canonical_source_map": "SUPERBRAIN/MASTER-NOTES/NAYAPOWER-CANONICAL-SOURCE-MAP.md",
            "continuous_flow": "SUPERBRAIN/MASTER-NOTES/SN-20260912-NAYAPOWER-CONTINUOUS-SMART-FLOW-AND-COLD-NAYA-RESTORE.md",
            "intelligent_block_protocol": "SUPERBRAIN/INTELLIGENT-BLOCK-PROTOCOL.md",
            "intelligence_distiller": "SUPERBRAIN/INTELLIGENCE-DISTILLER-PROTOCOL.md",
            "intelligence_organization": "SUPERBRAIN/INTELLIGENCE-ORGANIZATION-STANDARD.md",
        },
        "truth": {
            "proof_contract_status": proof.get("status"),
            "proof_authority": proof.get("proof_authority"),
            "separation_rules": proof.get("separation_rules", []),
            "proven": [
                "Control-plane current-state/active-block/mission-map/proof contracts exist.",
                "Continuous Smart Flow and cold-Naya operating directive is canonical.",
                "Next-action + handoff execution cycle exists and is machine-checkable.",
            ],
            "unknown": [
                "Universal automatic Smart Note -> Intelligent Block transformation across every meaningful Naya output.",
                "Universal automatic Intelligence -> Activity -> Control Plane synchronization.",
                "Universal lineage/Playback runtime behavior.",
                "Automatic successor-prompt generation from every meaningful output.",
                "Full intended-scope cold Naya independent continuation across all work.",
            ],
            "rule": "Evidence outranks assertion; UNKNOWN is not VERIFIED.",
        },
        "active_block": {
            "id": active["id"],
            "status": active["status"],
            "priority": active["priority"],
            "source": ".naya/control-plane/BLOCKS.json",
        },
        "next_action": {
            "count": 1,
            "status": "AUTHORIZED",
            "action": next_action,
            "source": ".naya/control-plane/BLOCKS.json",
            "reason": active.get("next_action_reason") or "The canonical active block exposes exactly one next action.",
            "acceptance": acceptance,
            "verification": "Independently observe the result, re-read canonical state, verify durable evidence, and leave exactly one successor action.",
        },
        "successor_prompt": {
            "rule": "Read the canonical baton and referenced control-plane sources before consequential execution.",
            "prompt": "Restore live NayaPOWER state from the canonical baton, reconcile it against STATE + BLOCKS + MAP + PROOF, execute only the one authorized next action, independently verify the result, record what changed and what remains unknown, rebuild the baton, and leave exactly one executable successor action.",
            "do_not": "Do not ask Shawn to reconstruct repository state that canonical sources provide. Do not create a competing next action. Do not convert UNKNOWN or recorded claims into proof.",
        },
        "playback": {
            "current_default": "Latest applicable canonical intelligence/state.",
            "lineage_sources": ["NAYA/ACTIVITY/", "execution receipts", ".naya/memory/events/", "SUPERBRAIN/INTELLIGENT-BLOCKS/"],
            "rule": "Replay history when needed; do not overwrite history merely because a newer state exists.",
        },
    }
    return baton

def validate_baton(baton: dict[str, Any]) -> None:
    state = load(PATHS["state"])
    blocks = load(PATHS["blocks"])
    map_data = load(PATHS["map"])
    proof = load(PATHS["proof"])
    active = blocks["active_block"]

    assert baton.get("status") == "CANONICAL", "BATON_NOT_CANONICAL"
    assert baton.get("repository") == state.get("repository") == "SoulSchoolAcademy/NayaPOWER", "BATON_REPOSITORY_MISMATCH"
    assert baton.get("source_of_truth", {}).get("live_state") == ".naya/control-plane/STATE.json"
    assert baton.get("source_of_truth", {}).get("active_block") == ".naya/control-plane/BLOCKS.json"
    assert baton.get("source_of_truth", {}).get("mission_map") == ".naya/control-plane/MAP.json"
    assert baton.get("source_of_truth", {}).get("proof") == ".naya/control-plane/PROOF.json"
    assert map_data.get("status") == "CANONICAL", "MAP_NOT_CANONICAL"
    assert proof.get("status") == "CANONICAL", "PROOF_NOT_CANONICAL"

    assert baton["current_state"]["mission"] == state["mission"], "BATON_MISSION_MISMATCH"
    assert baton["current_state"]["active_block"] == active["id"] == state["current_block"], "BATON_ACTIVE_BLOCK_MISMATCH"
    assert baton["current_state"]["active_block_status"] == active["status"] == state["current_block_status"], "BATON_ACTIVE_BLOCK_STATUS_MISMATCH"

    assert baton["active_block"]["id"] == active["id"], "BATON_BLOCK_ID_MISMATCH"
    assert baton["active_block"]["status"] == active["status"], "BATON_BLOCK_STATUS_MISMATCH"
    assert baton["active_block"]["priority"] == active["priority"], "BATON_BLOCK_PRIORITY_MISMATCH"

    n = baton["next_action"]
    assert n["count"] == 1, "BATON_NEXT_ACTION_COUNT_NOT_ONE"
    assert n["action"] == active["next_action"] == state["single_next_action"], "BATON_NEXT_ACTION_MISMATCH"
    assert n["source"] == ".naya/control-plane/BLOCKS.json", "BATON_NEXT_ACTION_SOURCE_MISMATCH"
    assert baton["source_snapshot"]["proof_status"] == proof.get("status"), "BATON_PROOF_STATUS_MISMATCH"
    assert baton["source_snapshot"].get("canonical_hub_source_sha") == subprocess.check_output(["git","rev-parse","HEAD:NAYANET/HUB/index.html"],cwd=ROOT,text=True).strip(), "BATON_HUB_SOURCE_MISMATCH"

def write_baton() -> dict[str, Any]:
    baton = build_baton()
    validate_baton(baton)
    PATHS["baton"].write_text(json.dumps(baton, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return baton

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["build", "validate", "build-and-validate"])
    args = p.parse_args()
    if args.command == "build":
        baton = write_baton()
        print(json.dumps({"status": "PASS", "operation": "BATON_BUILT", "live_head": baton["source_snapshot"]["live_head"], "next_action": baton["next_action"]["action"]}, indent=2))
    elif args.command == "validate":
        baton = load(PATHS["baton"])
        validate_baton(baton)
        print(json.dumps({"status": "PASS", "operation": "BATON_VALID", "next_action": baton["next_action"]["action"]}, indent=2))
    else:
        baton = write_baton()
        print(json.dumps({"status": "PASS", "operation": "BATON_BUILT_AND_VALIDATED", "live_head": baton["source_snapshot"]["live_head"], "next_action": baton["next_action"]["action"]}, indent=2))

if __name__ == "__main__":
    main()
