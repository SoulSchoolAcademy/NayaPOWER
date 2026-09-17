#!/usr/bin/env python3
"""Build the Primary Intelligence System feed consumed by the Intelligent Hub.

Sources:
- legacy/canonical SMART FEED CONTENT
- canonical SUPERBRAIN/SMART-NOTES calendar
- optional in-transaction Smart Note objects

The output is a projection, not a competing source of truth.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "SMART FEED CONTENT"
SMART_NOTES_ROOT = ROOT / "SUPERBRAIN" / "SMART-NOTES"
OUT = ROOT / "NAYANET" / "HUB" / "public" / "intelligence" / "pis-feed.json"

NOTE_RE = re.compile(r"(?:^|\n)🧠\s*NAYA POWER\s*[—-]\s*SMART NOTE\s+(\d+)\s*\n")
SEC_RE = re.compile(r"(?:^|\n)\s*(?:#+\s*)?(\d+)\.\s+([^\n]+)\s*\n", re.M)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)
META_RE = re.compile(r"^\*\*(.+?):\*\*\s*(.+?)\s*$", re.M)


def clean(s: str) -> str:
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def para(s: str, limit: int = 1800) -> str:
    for p in re.split(r"\n\s*\n", clean(s)):
        p = p.strip()
        if p and not re.match(r"^(?:\d+\.|#+)", p):
            return p[:limit]
    return clean(s)[:limit]


def sections(s: str) -> dict[int, str]:
    matches = list(SEC_RE.finditer(s))
    return {int(x.group(1)): clean(s[x.end():matches[i + 1].start() if i + 1 < len(matches) else len(s)]) for i, x in enumerate(matches)}


def when() -> str:
    try:
        x = subprocess.check_output(["git", "log", "-1", "--format=%cI", "--", "SMART FEED CONTENT"], cwd=ROOT, text=True).strip()
        if x:
            return x
    except Exception:
        pass
    return datetime.now(timezone.utc).isoformat()


def legacy_events(text: str, ts: str) -> list[dict[str, Any]]:
    matches = list(NOTE_RE.finditer(text))
    events = []
    for i, m in enumerate(matches):
        body = text[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)].strip()
        sec = sections(body)
        subject = re.search(r"(?:\*\*\s*)?Subject ID:\s*([^\n]+)", body, re.I)
        number = int(m.group(1))
        eid = subject.group(1).strip() if subject else f"NAYA-POWER-{number:02d}"
        title = re.sub(r"^What (?:Is|Are)\s+", "", body.splitlines()[0].strip())
        nutshell, human, child, grandma = para(sec.get(1, "")) or title, para(sec.get(2, "")), para(sec.get(3, "")), para(sec.get(4, ""))
        naya, machine, lesson, meaning = para(sec.get(5, "")), para(sec.get(6, "")), para(sec.get(7, "")), para(sec.get(8, ""))
        links, action, value = para(sec.get(9, "")), para(sec.get(10, "")), para(sec.get(11, ""))
        events.append({
            "event_id": eid, "user_id": "canonical", "created_at": ts, "updated_at": ts,
            "source": {"type": "smart_note", "label": title},
            "human_input": {"raw": human or nutshell, "captured_at": ts},
            "context": {"topic": title, "tags": ["Smart Note", "Naya Power", "Intelligent Feed"], "canonical_path": f"SMART FEED CONTENT#NAYA-POWER-{number:02d}"},
            "naya_interpretation": {"observation": nutshell, "interpretation": naya, "recommendation": action, "uncertainty": "Source uncertainty is preserved; projection does not invent certainty."},
            "machine_evidence": {"items": ["Canonical source: SMART FEED CONTENT", "PIS projection generated from canonical Smart Feed content."], "verification_state": "source-projection-generated"},
            "weaver_synthesis": {"summary": nutshell, "relationships": []},
            "lesson": {"text": lesson, "retained": True}, "meaning": {"text": meaning, "significance": "Canonical Smart Note meaning"},
            "action": {"text": action, "status": "from-source"}, "whats_in_it_for_you": value,
            "relationships": {"event_ids": [], "connection_ids": [], "space_ids": []}, "privacy": {"visibility": "source-defined", "consent_state": "source-defined"},
            "trust": {"level": "source-projection", "evidence_ids": []}, "status": "active",
            "perspectives": [
                {"label": "HUMAN", "body": human or nutshell, "tone": "human"}, {"label": "CHILD", "body": child, "tone": "child"},
                {"label": "GRANDMA", "body": grandma, "tone": "grandma"}, {"label": "NAYA", "body": naya, "tone": "naya"},
                {"label": "MACHINE", "body": machine, "tone": "machine"}, {"label": "WEAVER", "body": links, "tone": "weaver"},
            ],
            "pis": {"source_ref": f"SMART FEED CONTENT#NAYA-POWER-{number:02d}", "projection_version": "3.0", "timestamp_precision": "source-commit"},
        })
    return events


def parse_canonical_note(path: Path, root: Path = ROOT) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("# SMART NOTE"):
        return None
    headings = list(HEADING_RE.finditer(text))
    sec: dict[str, str] = {}
    for i, match in enumerate(headings):
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        sec[clean(match.group(1)).upper()] = clean(text[match.end():end])
    meta = {m.group(1).strip().lower(): clean(m.group(2)) for m in META_RE.finditer(text)}
    sid_match = re.search(r"\*\*Smart Note ID:\*\*\s*`([^`]+)`", text)
    if not sid_match:
        return None
    rel = str(path.relative_to(root)).replace("\\", "/")
    eid = sid_match.group(1)
    topic = text.splitlines()[0].replace("# SMART NOTE —", "").replace("# SMART NOTE -", "").strip()
    evidence = [re.sub(r"^-\s*", "", x).strip() for x in sec.get("EVIDENCE / SMART LINKS", "").splitlines() if x.strip().startswith("-")]
    return {
        "event_id": eid, "user_id": "canonical", "created_at": meta.get("timestamp", when()), "updated_at": meta.get("timestamp", when()),
        "source": {"type": "smart_note", "label": topic}, "human_input": {"raw": sec.get("HUMAN NOTE", sec.get("IN A NUTSHELL", "")), "captured_at": meta.get("timestamp", when())},
        "context": {"topic": topic, "tags": ["canonical", "smart-note", "naya-language"], "canonical_path": rel},
        "naya_interpretation": {"observation": sec.get("IN A NUTSHELL", ""), "interpretation": sec.get("NAYA NOTE", ""), "recommendation": sec.get("HOW TO USE IT", ""), "uncertainty": "Projection is derived from the canonical Smart Note; truth status remains governed by its evidence."},
        "machine_evidence": {"items": evidence + [f"CANONICAL_SMART_NOTE:{rel}"], "verification_state": "RECORDED"},
        "weaver_synthesis": {"summary": sec.get("WHY IT MATTERS", topic), "relationships": []},
        "lesson": {"text": sec.get("LEARNING LESSON / ADAPTIVE LEARNING", ""), "retained": True},
        "meaning": {"text": sec.get("WHY IT MATTERS", ""), "significance": sec.get("WHY IT MATTERS", "")},
        "action": {"text": sec.get("ONE NEXT ACTION", ""), "status": "canonical"}, "whats_in_it_for_you": sec.get("WHAT'S IN IT FOR ME / YOU / US", ""),
        "relationships": {"event_ids": [], "connection_ids": [], "space_ids": []}, "privacy": {"visibility": "source-defined", "consent_state": "source-defined"},
        "trust": {"level": "recorded", "evidence_ids": evidence}, "status": meta.get("status", "CANONICAL"),
        "perspectives": [
            {"label": "HUMAN", "body": sec.get("HUMAN NOTE", ""), "tone": "human"}, {"label": "CHILD", "body": sec.get("CHILD / DERIVED NOTE", ""), "tone": "child"},
            {"label": "GRAMMAR", "body": sec.get("GRAMMAR NOTE", ""), "tone": "machine"}, {"label": "NAYA", "body": sec.get("NAYA NOTE", ""), "tone": "naya"},
            {"label": "MACHINE", "body": sec.get("MACHINE NOTE", ""), "tone": "machine"}, {"label": "LEARNING", "body": sec.get("LEARNING LESSON / ADAPTIVE LEARNING", ""), "tone": "learning"},
        ],
        "pis": {"source_ref": rel, "projection_version": "3.0", "timestamp_precision": "canonical-smart-note"},
    }


def canonical_note_events(root: Path = SMART_NOTES_ROOT) -> list[dict[str, Any]]:
    if not root.exists():
        return []
    events = []
    repo_root = root.parents[2]
    for path in sorted(root.rglob("*.md")):
        event = parse_canonical_note(path, repo_root)
        if event:
            events.append(event)
    return events


def build_projection(*, extra_notes: Iterable[dict[str, Any]] | None = None, source_root: Path = ROOT, output: Path = OUT) -> dict[str, Any]:
    source_root = Path(source_root)
    source = source_root / "SMART FEED CONTENT"
    legacy = legacy_events(source.read_text(encoding="utf-8"), when()) if source.exists() else []
    notes = canonical_note_events(source_root / "SUPERBRAIN" / "SMART-NOTES")
    merged: dict[str, dict[str, Any]] = {e["event_id"]: e for e in legacy}
    for event in notes + list(extra_notes or []):
        merged[event["event_id"]] = event
    events = sorted(merged.values(), key=lambda e: (e.get("created_at", ""), e["event_id"]), reverse=True)
    payload = {"schema_version": "PIS-3.0", "generated_at": datetime.now(timezone.utc).isoformat(), "source": "github:canonical-smart-notes+smart-feed", "event_count": len(events), "events": events}
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"status": "REBUILT", "event_count": len(events), "output": str(output), "events": events}


def main() -> None:
    result = build_projection()
    print(f"PIS_FEED_BUILT events={result['event_count']} source=canonical-smart-notes+smart-feed")


if __name__ == "__main__":
    main()
