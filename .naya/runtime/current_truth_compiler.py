#!/usr/bin/env python3
"""Compile one cold-Naya current-truth packet from existing authoritative sources.

This is a derived, rebuildable projection. It creates no new persistence or
memory store and never overrides the control plane or live repository reality.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / ".naya/control-plane/STATE.json"
CURRENT_TRUTH = ROOT / "SUPERBRAIN/AI-BOOT/DISTILL-PROJECT-INTELLIGENCE-CURRENT-TRUTH.md"
BRAIN_MAP = ROOT / ".naya/memory/NAYAPOWER-BRAIN-MAP.md"
CONTRACT = ROOT / ".naya/codex/CANONICAL-SMART-NOTE-INTELLIGENT-BLOCK-SYSTEM-V1.md"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _git(*args: str) -> str | None:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _section(text: str, heading: str) -> str | None:
    marker = f"## {heading}"
    if marker not in text:
        return None
    value = text.split(marker, 1)[1]
    return value.split("\n## ", 1)[0].strip()


def compile_current_truth() -> dict[str, Any]:
    state = _read_json(STATE)
    current_truth = _read(CURRENT_TRUTH)
    observed_head = _git("rev-parse", "HEAD")
    observed_branch = _git("branch", "--show-current")

    unknown = list(state.get("unknown") or [])
    blocked = []
    if state.get("next_action", {}).get("status") == "BLOCKED":
        blocked.append(state["next_action"])
    blocked.extend(state.get("failures") or [])

    next_action = state.get("current_next_action") or state.get("single_next_action")
    if isinstance(next_action, str):
        next_action = {"action": next_action}

    packet = {
        "schema": "NAYAPOWER_CURRENT_TRUTH_PACKET_V1",
        "status": "DERIVED",
        "authority": {
            "human_director": "Shawn Vibert",
            "control_plane": ".naya/control-plane/",
            "live_repository": "git:HEAD",
            "protected_boundaries": state.get("protected_boundaries") or [],
            "operating_policy": state.get("operating_policy"),
            "hub_read_first": state.get("hub_readiness_inventory"),
            "note": "This packet never overrides live source, control plane, runtime evidence, or human authority.",
        },
        "repository_reality": {
            "branch": observed_branch,
            "head": observed_head,
            "head_source": "git:HEAD",
            "recorded_head_is_authoritative": False,
        },
        "identity": {
            "project": state.get("repository", "SoulSchoolAcademy/NayaPOWER"),
            "mission": state.get("mission"),
            "north_star": state.get("north_star"),
            "priority": state.get("priority"),
        },
        "current": {
            "block": state.get("current_block"),
            "block_status": state.get("current_block_status"),
            "frontier": state.get("current_frontier"),
            "today_mission": state.get("today_mission"),
        },
        "proven": {
            "latest_automation_observation": state.get("latest_automation_observation"),
            "current_state": state.get("known") or [],
        },
        "unknown": unknown,
        "blocked": blocked,
        "bottleneck": state.get("bottleneck"),
        "next": next_action,
        "canonical_sources": {
            "brain_map": str(BRAIN_MAP.relative_to(ROOT)),
            "current_truth": str(CURRENT_TRUTH.relative_to(ROOT)),
            "smart_note_ib_contract": str(CONTRACT.relative_to(ROOT)),
            "state": str(STATE.relative_to(ROOT)),
        },
        "current_truth_law": _section(current_truth, "CURRENT-TRUTH LAW"),
        "cold_naya_packet_definition": _section(current_truth, "COLD-NAYA PACKET"),
        "continuation_rule": _section(current_truth, "CONTINUATION"),
    }
    return packet


if __name__ == "__main__":
    print(json.dumps(compile_current_truth(), indent=2, ensure_ascii=False))
