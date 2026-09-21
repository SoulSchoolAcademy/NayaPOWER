#!/usr/bin/env python3
"""NayaPOWER Project Intelligence Context v1.

Project Intelligence is a rebuildable projection over canonical repository truth.
It is not a second project database and never upgrades evidence.

Design:
  CANONICAL SOURCES + CONTROL PLANE + PIS/LEARNING + EVIDENCE
      -> DISTILLED PROJECT INTELLIGENCE CONTEXT
      -> COLD NAYA / TEAM HANDOFF / NEXT ACTION

The projection answers the questions a fresh Naya must answer before acting:
identity, mission, vision, purpose, goals, requirements, constraints,
constitution, architecture, authority, canonical sources, current state,
verified, failed, unknown, decisions, dependencies, learning, open loops,
definition of done, next action, proof target, and handoff.

Distillation means value-preserving compression: remove redundancy and noise,
never remove a fact merely because it is inconvenient or long. Evidence,
uncertainty, provenance, privacy, and causal relationships survive the
projection.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / ".naya" / "control-plane"
PROJECT_PATH = ROOT / ".naya" / "projects" / "CURRENT-PROJECT.md"
ONE_SHOT = ROOT / "NAYAPOWER-ONE-SHOT.md"
MACHINE_CONTRACT = ROOT / ".naya" / "one-shot" / "NAYAPOWER-MACHINE-CONTRACT.json"
SYSTEM_MAP = ROOT / ".naya" / "one-shot" / "NAYAPOWER-SYSTEM-MAP.mmd"
START_HERE = ROOT / "SUPERBRAIN" / "AI-BOOT" / "START-HERE.md"
EVENT_DIR = ROOT / "MASTER-NOTES" / "INTELLIGENCE-EVENTS"
PIS_DIR = ROOT / ".naya" / "memory" / "notes"
LEARNING_DIR = ROOT / "MASTER-NOTES" / "ADAPTIVE-LEARNING"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def bullets(value: str) -> list[str]:
    return [
        re.sub(r"^\s*[-*]\s+", "", line).strip()
        for line in value.splitlines()
        if re.match(r"^\s*[-*]\s+", line)
    ]


def load_events() -> list[dict[str, Any]]:
    if not EVENT_DIR.exists():
        return []
    events = []
    for path in sorted(EVENT_DIR.rglob("*.json")):
        try:
            event = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        if isinstance(event, dict) and str(event.get("event_id", "")).startswith("SE-"):
            events.append(event)
    return events


def event_project(event: dict[str, Any]) -> str:
    return str(event.get("project_id") or event.get("project") or "").strip()


def current_project_events(events: list[dict[str, Any]], project: str) -> list[dict[str, Any]]:
    wanted = re.sub(r"[^a-z0-9]+", "-", project.lower()).strip("-")
    return [
        e for e in events
        if re.sub(r"[^a-z0-9]+", "-", event_project(e).lower()).strip("-") == wanted
    ]


def event_state(event: dict[str, Any]) -> str:
    explicit = str(event.get("evidence_state") or "").strip().upper()
    if explicit:
        return explicit
    verification = event.get("verification")
    if isinstance(verification, dict) and str(verification.get("status", "")).upper() == "VERIFIED":
        return "VERIFIED"
    return "UNKNOWN"


def collect_event_state(events: list[dict[str, Any]], states: set[str]) -> list[dict[str, Any]]:
    return [
        {
            "event_id": e.get("event_id"),
            "title": e.get("title", ""),
            "lesson": e.get("lesson", ""),
            "evidence_state": event_state(e),
            "actual_outcome": e.get("actual_outcome", ""),
            "next_action": e.get("next_action", ""),
            "source": e.get("source", []),
        }
        for e in events
        if event_state(e) in states
    ]


def load_learning(project: str) -> list[dict[str, Any]]:
    if not LEARNING_DIR.exists():
        return []
    wanted = re.sub(r"[^a-z0-9]+", "-", project.lower()).strip("-")
    out = []
    for path in sorted(LEARNING_DIR.glob("LRN-*.json")):
        item = read_json(path)
        if not item:
            continue
        candidate = str(item.get("project", "")).strip()
        normalized = re.sub(r"[^a-z0-9]+", "-", candidate.lower()).strip("-")
        if normalized == wanted:
            out.append(item)
    return out


def project_identity(state: dict[str, Any], project_text: str, events: list[dict[str, Any]]) -> dict[str, Any]:
    repo = str(state.get("repository") or "SoulSchoolAcademy/NayaPOWER")
    name = "NayaPOWER"
    title = project_text.splitlines()[0].lstrip("# ").strip() if project_text else name
    bound = current_project_events(events, repo) or current_project_events(events, name)
    return {
        "name": name,
        "repository": repo,
        "title": title,
        "scope": "NayaPOWER Superbrain / NayaNET operating system and its governed human-facing Hub",
        "canonical_project_binding": "repository identity + canonical project-linked Intelligence Events when present",
        "canonical_event_count": len(bound),
        "status": "BOUND" if bound else "RECONSTRUCTED_FROM_CANONICAL_PROJECT_SOURCES",
    }


def architecture(machine: dict[str, Any], system_map: str) -> dict[str, Any]:
    return {
        "model": [
            "HUMAN — vision, intent, authority, destination",
            "NAYA — governed intelligence and execution partner",
            "NayaPOWER — Superbrain / control substrate",
            "DISTILL — value-preserving selection of what matters for the current decision",
            "CANONICAL EVENT — durable occurrence and provenance",
            "EVIDENCE / RECEIPT — proof of what happened",
            "PIS / RELATIONSHIPS / INDEX — primary intelligence and connections",
            "LEARNING — verified experience promoted into reusable intelligence",
            "RETRIEVAL — restore relevant intelligence into the next context",
            "AUTHORIZED DECISION — authority/consent/scope/revocation/expiry/RLS gate",
            "EXECUTION — governed action",
            "VERIFICATION — independent evidence",
            "UPDATED STATE — current truth changes after verified execution",
            "COMPOUNDING — verified learning improves future decisions",
            "NayaNET HUB — visual brain / human operating surface; projection, not source of truth",
        ],
        "canonical_loop": [
            "EXPERIENCE",
            "CAPTURE",
            "CONNECT",
            "DISTILL",
            "UNDERSTAND",
            "ACT",
            "VERIFY",
            "LEARN",
            "COMPOUND",
            "REDISTILL",
        ],
        "system_map_source": ".naya/one-shot/NAYAPOWER-SYSTEM-MAP.mmd",
        "machine_contract_source": ".naya/one-shot/NAYAPOWER-MACHINE-CONTRACT.json",
        "system_map_present": bool(system_map),
        "engine": machine.get("engine", []),
        "human_surface": machine.get("human_surface", []),
    }


def build_project_intelligence() -> dict[str, Any]:
    state = read_json(CONTROL / "STATE.json")
    control_map = read_json(CONTROL / "MAP.json")
    blocks = read_json(CONTROL / "BLOCKS.json")
    proof = read_json(CONTROL / "PROOF.json")
    machine = read_json(MACHINE_CONTRACT)
    project_text = read_text(PROJECT_PATH)
    one_shot_text = read_text(ONE_SHOT)
    system_map = read_text(SYSTEM_MAP)
    events = load_events()
    active = blocks.get("active_block", {}) if isinstance(blocks.get("active_block"), dict) else {}
    learning = load_learning("NayaPOWER")

    mission = str(state.get("mission") or control_map.get("mission") or "").strip()
    north_star = str(state.get("north_star") or control_map.get("north_star") or "").strip()
    purpose = (
        "Make useful intelligence persistent, retrievable, verifiable, actionable, "
        "and compounding so humans can accomplish extraordinary things without becoming "
        "AI project managers."
    )

    current_state = {
        "operational_status": state.get("status"),
        "priority": state.get("priority"),
        "active_block": active.get("id"),
        "active_block_status": active.get("status"),
        "current_head_source": state.get("current_head", {}).get("source"),
        "recorded_head_is_not_authoritative": state.get("current_head", {}).get("recorded_head_is_not_authoritative"),
        "bottleneck": state.get("bottleneck"),
        "next_action": active.get("next_action") or state.get("single_next_action"),
        "target_state": active.get("target_state"),
    }

    goals = [
        "Make the canonical NAYANET/HUB/index.html human-facing Hub operational through the existing governed Naya engine.",
        "Preserve one canonical intelligence/event substrate while exposing many authorized views.",
        "Turn verified experience into durable learning that can influence later decisions without granting authority.",
        "Enable cold-Naya restoration, responsible continuation, verification, learning, and successor handoff without conversational archaeology.",
        "Maximize verified human value per unit of effort while preserving agency, truth, privacy, safety, and trust.",
    ]

    requirements = [
        "One canonical source of truth; derived indexes/projections must be rebuildable.",
        "Project Intelligence must be reconstructable from canonical sources rather than maintained as an independent mutable database.",
        "Every consequential action must pass the existing authority, consent, scope, revocation, expiry, RLS, and fail-closed boundaries.",
        "Evidence state must remain explicit: UNKNOWN is never success.",
        "The current frontier must expose exactly one highest-value responsible next action.",
        "Verified execution must leave durable evidence and successor-ready context.",
        "The Hub must remain the human-facing visual brain and must not become a competing intelligence authority.",
    ]

    constraints = list(state.get("protected_boundaries", []))
    if not constraints:
        constraints = list(control_map.get("protected", []))

    constitution = {
        "core_laws": [
            "CAPABILITY DOES NOT CREATE AUTHORITY.",
            "UNKNOWN ≠ VERIFIED.",
            "BLOCKED ≠ PASS.",
            "RECORDED ≠ CURRENT.",
            "IMPLEMENTED ≠ VERIFIED.",
            "VERIFIED ≠ PRODUCTION-PROVEN.",
            "ONE CANONICAL EVENT → MANY AUTHORIZED VIEWS.",
            "NO SECOND INTELLIGENCE STORE.",
            "HUMAN OWNS THE DESTINATION; NAYA NAVIGATES REALITY.",
            "THE SYSTEM MUST NOT DEPEND ON A NAYA REMEMBERING TO REMEMBER.",
        ],
        "source": "NAYAPOWER-ONE-SHOT.md + control-plane sources",
    }

    authority = {
        "human": "Director / owner of destination and authority.",
        "naya": "Governed intelligence / execution partner.",
        "github": "Durable engineering/source context and execution record.",
        "superbrain": "NayaPOWER is the governed intelligence/control substrate.",
        "hub": "NayaNET Hub is the human-facing projection/action surface, not source of truth.",
        "truth_owners": control_map.get("truth_owners", {}),
    }

    canonical_sources = {
        "control_plane": [
            ".naya/control-plane/CANONICAL-IDENTITY-REGISTRY.json",
            ".naya/control-plane/MAP.json",
            ".naya/control-plane/STATE.json",
            ".naya/control-plane/BLOCKS.json",
            ".naya/control-plane/PROOF.json",
        ],
        "architecture": [
            "NAYAPOWER-ONE-SHOT.md",
            ".naya/one-shot/NAYAPOWER-MACHINE-CONTRACT.json",
            ".naya/one-shot/NAYAPOWER-SYSTEM-MAP.mmd",
            "SUPERBRAIN/AI-BOOT/START-HERE.md",
        ],
        "project": [".naya/projects/CURRENT-PROJECT.md"],
        "intelligence": [
            "MASTER-NOTES/INTELLIGENCE-EVENTS/",
            ".naya/memory/notes/",
            ".naya/memory/INDEX.json",
            "MASTER-NOTES/ADAPTIVE-LEARNING/",
        ],
        "human_surface": ["NAYANET/HUB/index.html"],
        "evidence": [
            ".naya/control-plane/PROOF.json",
            ".naya/receipts/",
            "GitHub Actions artifacts and execution receipts",
        ],
    }

    vision = (
        "A network where human and AI intelligence is persistent, connected, verified, "
        "distilled, and compounded so people become more capable and wiser rather than "
        "merely accumulating more information."
    )

    decisions = [
        "NayaPOWER is the Superbrain/control substrate; NayaNET Hub is the visual human operating surface.",
        "Project Intelligence is a rebuildable projection over existing canonical intelligence, not a second project database.",
        "GitHub is the durable engineering/source context; runtime systems provide governed operational state and persistence where applicable.",
        "Distillation is value-preserving: remove redundancy/noise, not valuable truth, uncertainty, provenance, or causal context.",
        "The current human-facing Hub source remains NAYANET/HUB/index.html.",
    ]

    dependencies = {
        "upstream": [
            "Human intent / authority",
            "Canonical project sources and Intelligence Events",
            "Control-plane truth and governance",
        ],
        "intelligence": [
            "PIS / Smart Notes",
            "relationships and indexes",
            "execution receipts / evidence",
            "Adaptive Learning",
        ],
        "downstream": [
            "Cold Naya restore",
            "Team Naya handoff",
            "Next-action selection",
            "Authorized execution",
            "Hub projections",
        ],
    }

    verified = collect_event_state(events, {"VERIFIED", "RUNTIME-PROVEN", "PRODUCTION-PROVEN"})
    verified_state = state.get("verified_evidence", {}).get("known", [])
    if not verified_state and isinstance(state.get("known"), list):
        verified_state = state.get("known", [])
    if isinstance(verified_state, list):
        verified = [{"source": ".naya/control-plane/STATE.json", "statement": str(item)} for item in verified_state] + verified
    failed = collect_event_state(events, {"FAILED", "BLOCKED"})
    failures_state = state.get("failures", [])
    if isinstance(failures_state, list):
        failed = [{"source": ".naya/control-plane/STATE.json", "statement": str(item)} for item in failures_state] + failed
    unknown = collect_event_state(events, {"UNKNOWN"})
    learning_summary = [
        {
            "learning_event_id": item.get("learning_event_id"),
            "lesson": item.get("lesson"),
            "evidence_state": item.get("evidence_state"),
            "learning_state": item.get("learning_state"),
            "recommendation": item.get("recommendation", ""),
        }
        for item in learning[-25:]
    ]

    proof_current = proof.get("current_evidence", {})
    proof_statuses = {}
    if isinstance(proof_current, dict):
        for key, value in proof_current.items():
            if isinstance(value, dict) and "status" in value:
                proof_statuses[key] = value.get("status")

    open_loops = list(state.get("unknown", []))
    if active.get("next_action"):
        open_loops = list(dict.fromkeys(open_loops + [active["next_action"]]))

    project = project_identity(state, project_text, events)

    result = {
        "schema": "naya/project-intelligence-context/v1",
        "status": "REBUILDABLE_DERIVED_PROJECTION",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "distillation_rule": (
            "Preserve maximum decision-relevant value per unit of context. "
            "Compression may remove redundancy and noise, never evidence, uncertainty, "
            "provenance, authority boundaries, causal relationships, or material failures."
        ),
        "identity": project,
        "mission": mission,
        "vision": vision,
        "purpose": purpose,
        "north_star": north_star,
        "goals": goals,
        "requirements": requirements,
        "constraints": constraints,
        "constitution": constitution,
        "architecture": architecture(machine, system_map),
        "authority": authority,
        "canonical_sources": canonical_sources,
        "current_state": current_state,
        "verified": verified,
        "failed": failed,
        "unknown": unknown,
        "decisions": decisions,
        "dependencies": dependencies,
        "learning": {
            "definition": "Verified experience that can improve future decisions without silently changing authority.",
            "recent_project_learning": learning_summary,
            "count": len(learning),
        },
        "open_loops": open_loops,
        "definition_of_done": active.get("target_state") or control_map.get("execution_map", {}).get("definition_of_done"),
        "next_action": active.get("next_action") or state.get("single_next_action"),
        "proof_target": active.get("target_state") or state.get("single_next_action"),
        "team_handoff": {
            "sender": "Current Naya",
            "receiver": "Next Naya",
            "mission": mission,
            "context": "Restore this Project Intelligence Context from canonical sources before acting.",
            "current_state": current_state,
            "what_is_verified": verified,
            "what_is_unknown": state.get("unknown", []),
            "protected": constraints,
            "assignment": active.get("next_action") or state.get("single_next_action"),
            "authority_check": "Capability does not create authority; verify actor, scope, action, consent, revocation, expiry and RLS before consequential execution.",
            "proof_required": active.get("target_state") or "claim-appropriate evidence",
            "successor_rule": "Do not ask the human to reconstruct repository history when canonical evidence can answer it.",
        },
        "source_lineage": {
            "control_plane": {
                "STATE": ".naya/control-plane/STATE.json",
                "MAP": ".naya/control-plane/MAP.json",
                "BLOCKS": ".naya/control-plane/BLOCKS.json",
                "PROOF": ".naya/control-plane/PROOF.json",
            },
            "project_source": ".naya/projects/CURRENT-PROJECT.md",
            "architecture_sources": ["NAYAPOWER-ONE-SHOT.md", ".naya/one-shot/NAYAPOWER-MACHINE-CONTRACT.json"],
            "event_count": len(events),
            "pis_note_count": len(list(PIS_DIR.glob("*.json"))) if PIS_DIR.exists() else 0,
            "learning_count": len(learning),
        },
        "cold_restore_answers": {
            "WHAT": project["title"],
            "WHY": mission,
            "WHERE": f"Repository: {project['repository']}; active block: {current_state['active_block']}",
            "AUTHORITY": authority["human"],
            "PROTECTED": constraints,
            "CURRENT_STATE": current_state,
            "CURRENT_GAP": state.get("unknown", []),
            "NEXT_ACTION": active.get("next_action") or state.get("single_next_action"),
            "PROOF": active.get("target_state") or "claim-appropriate evidence",
            "HANDOFF": "team_handoff",
        },
        "source_health": {
            "project_source_present": bool(project_text),
            "one_shot_present": bool(one_shot_text),
            "machine_contract_present": bool(machine),
            "system_map_present": bool(system_map),
            "start_here_present": bool(read_text(START_HERE)),
            "control_plane_present": all(bool(read_json(CONTROL / name)) for name in ("STATE.json", "MAP.json", "BLOCKS.json", "PROOF.json")),
        },
    }
    return result


if __name__ == "__main__":
    print(json.dumps(build_project_intelligence(), indent=2, ensure_ascii=False))
