#!/usr/bin/env python3
"""Human-readable calendar projections for governed Naya continuity records.

Machine events remain authoritative in .naya/memory/events. This module only
projects verified events into the human-readable calendar trees:

  NAYAPOWER/ACTIVITY/YYYY/MM/DD/YYYY-MM-DDTHH-MM-SSZ__TOPIC.md
  NAYA-TEAM/YYYY/MM/DD/YYYY-MM-DDTHH-MM-SSZ__TOPIC.md

It deliberately does not create Smart Notes: Smart Notes have their own
contract and writer. This separation prevents three systems from becoming one
ambiguous feed.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ACTIVITY_ROOT = ROOT / "NAYAPOWER" / "ACTIVITY"
TEAM_ROOT = ROOT / "NAYA-TEAM"


def _utc_parts(stamp: str | None = None) -> tuple[datetime, str]:
    dt = datetime.fromisoformat((stamp or datetime.now(timezone.utc).isoformat()).replace("Z", "+00:00")).astimezone(timezone.utc)
    return dt, f"{dt:%Y-%m-%dT%H-%M-%SZ}"


def safe_topic(topic: str) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "-", str(topic).strip()).strip("-").upper()
    return token[:100] or "UNTITLED"


def calendar_record_path(root: Path, stamp: str, topic: str) -> Path:
    dt, filename_stamp = _utc_parts(stamp)
    return root / f"{dt:%Y}" / f"{dt:%m}" / f"{dt:%d}" / f"{filename_stamp}__{safe_topic(topic)}.md"


def _ensure_day_index(day_dir: Path, title: str, record: Path) -> None:
    day_dir.mkdir(parents=True, exist_ok=True)
    index = day_dir / "INDEX.md"
    link = record.name
    if index.exists():
        body = index.read_text(encoding="utf-8")
        if link in body:
            return
        body = body.rstrip() + f"\n- [{title}](./{link})\n"
    else:
        body = f"# {day_dir.parent.name}/{day_dir.name}\n\n## Records\n\n- [{title}](./{link})\n"
    index.write_text(body, encoding="utf-8")


def project_event(event: dict[str, Any], *, activity_root: Path | None = None, team_root: Path | None = None) -> dict[str, str]:
    stamp = str(event.get("effective_at") or event.get("created_at") or datetime.now(timezone.utc).isoformat())
    topic = str(event.get("subject") or event.get("title") or event.get("event_id") or "Naya Activity")
    dt, filename_stamp = _utc_parts(stamp)
    activity_root = Path(activity_root) if activity_root else ACTIVITY_ROOT
    team_root = Path(team_root) if team_root else TEAM_ROOT

    activity_path = calendar_record_path(activity_root, stamp, topic)
    team_path = calendar_record_path(team_root, stamp, topic)
    activity_path.parent.mkdir(parents=True, exist_ok=True)
    team_path.parent.mkdir(parents=True, exist_ok=True)

    execution = event.get("execution") or {}
    continuity = event.get("continuity") or {}
    handoff = continuity.get("handoff") or {}
    verification = event.get("verification") or {}
    evidence = verification.get("evidence") or event.get("evidence_ids") or []
    evidence_lines = "\n".join(f"- `{x}`" for x in evidence) or "- None supplied"

    activity_body = f"""# Activity — {topic}\n\n**Timestamp:** {stamp}\n**Event ID:** `{event.get('event_id', '')}`\n**Status:** `{event.get('status', 'UNKNOWN')}`\n**Actor:** `{execution.get('actor_id', 'unknown')}`\n\n## What happened\n\n{event.get('activity_feed_projection', {}).get('summary', event.get('summary', ''))}\n\n## Execution binding\n\n- Claim: `{execution.get('claim_id', '')}`\n- Action: `{execution.get('action_id', '')}`\n- Decision: `{execution.get('decision_id', '')}`\n- Authority: `{execution.get('authority_id', '')}`\n- Run: `{execution.get('run_id', '')}`\n- Session: `{execution.get('session_id', '')}`\n\n## Verification evidence\n\n{evidence_lines}\n\n## Continuity\n\n- Next Action: **{handoff.get('next_action', '')}**\n- Successor: **{handoff.get('successor', '')}**\n\n## Machine authority\n\nThe machine-readable canonical event remains authoritative under `.naya/memory/events/`. This file is the human-readable Activity projection.\n"""

    team_body = f"""# NAYA-TEAM — {topic}\n\n**Timestamp:** {stamp}\n**Event ID:** `{event.get('event_id', '')}`\n**Source:** Activity event projection\n\n## Why this matters to the next Naya\n\nThis record is the cross-Naya continuity projection of a verified governed execution. It exists so a successor can understand what happened without reconstructing the predecessor's private conversation.\n\n## What happened\n\n{event.get('activity_feed_projection', {}).get('summary', event.get('summary', ''))}\n\n## Current state\n\n`{continuity.get('execution_state', 'UNKNOWN')}`\n\n## Evidence\n\n{evidence_lines}\n\n## Exactly ONE Next Action\n\n**{handoff.get('next_action', '')}**\n\n## Successor\n\n**{handoff.get('successor', '')}**\n\n## Separation\n\nThis is a NAYA-TEAM continuity record, not a Smart Note and not the canonical machine event.\n"""

    for path, body, title, root in (
        (activity_path, activity_body, topic, activity_root),
        (team_path, team_body, topic, team_root),
    ):
        if path.exists():
            existing = path.read_text(encoding="utf-8")
            if existing != body:
                raise ValueError(f"projection conflict: {path}")
        else:
            path.write_text(body, encoding="utf-8")
        _ensure_day_index(path.parent, title, path)

    return {"activity_path": str(activity_path), "team_path": str(team_path), "timestamp": filename_stamp}


__all__ = ["project_event", "calendar_record_path", "safe_topic", "ACTIVITY_ROOT", "TEAM_ROOT"]
