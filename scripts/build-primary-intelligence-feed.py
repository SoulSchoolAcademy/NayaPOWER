#!/usr/bin/env python3
"""Build the Primary Intelligence System projection consumed by the NayaNET Hub.

Canonical source: timestamped Smart Notes under .naya/.
Output: NAYANET/HUB/public/intelligence/pis-feed.json.

This is a projection builder, not a second source of truth. Each event retains
its canonical Smart Note path and stable event identity so the Hub can verify
that it is rendering the same intelligence event.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".naya"
OUTPUT = ROOT / "NAYANET" / "HUB" / "public" / "intelligence" / "pis-feed.json"

SECTION_RE = re.compile(r"^## (\d+)\.\s+(.+?)\s*$", re.MULTILINE)
DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")
SUBJECT_RE = re.compile(r"\*\*Subject ID:\*\*\s*([^\n]+)")


def sections(text: str) -> dict[int, str]:
    matches = list(SECTION_RE.finditer(text))
    result: dict[int, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[int(match.group(1))] = text[start:end].strip()
    return result


def clean_markdown(value: str) -> str:
    value = re.sub(r"^\s*>\s?", "", value, flags=re.MULTILINE)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def first_paragraph(value: str) -> str:
    value = clean_markdown(value)
    for part in re.split(r"\n\s*\n", value):
        part = part.strip()
        if part and not part.startswith("#"):
            return part
    return value[:800].strip()


def first_line(value: str) -> str:
    value = clean_markdown(value)
    for line in value.splitlines():
        line = line.strip(" -\t")
        if line:
            return line[:1000]
    return ""


def event_time(path: Path, text: str) -> str:
    match = DATE_RE.search(path.name) or DATE_RE.search(text[:1200])
    date = match.group(1) if match else "1970-01-01"
    # Prefer the canonical Git commit timestamp when available; otherwise keep
    # a deterministic day-level timestamp rather than inventing a time.
    try:
        committed = subprocess.check_output(
            ["git", "log", "-1", "--format=%cI", "--", str(path.relative_to(ROOT))],
            cwd=ROOT,
            text=True,
        ).strip()
        if committed:
            return committed
    except Exception:
        pass
    return f"{date}T00:00:00+00:00"


def event_id(path: Path, text: str) -> str:
    subject = SUBJECT_RE.search(text)
    if subject:
        return subject.group(1).strip().lower().replace(" ", "-")
    return path.stem.lower()


def make_event(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    sec = sections(text)
    title_match = re.search(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else path.stem
    when = event_time(path, text)
    raw = first_paragraph(sec.get(2, "")) or title
    child = first_paragraph(sec.get(3, ""))
    grandma = first_paragraph(sec.get(4, ""))
    naya = first_paragraph(sec.get(5, ""))
    machine = first_paragraph(sec.get(6, ""))
    lesson = first_paragraph(sec.get(7, ""))
    meaning = first_paragraph(sec.get(8, ""))
    connections = first_paragraph(sec.get(9, ""))
    action = first_paragraph(sec.get(10, ""))
    nutshell = first_paragraph(sec.get(1, "")) or raw
    perspectives = [
        {"label": "HUMAN", "body": raw, "tone": "human"},
        {"label": "CHILD", "body": child, "tone": "child"},
        {"label": "GRANDMA", "body": grandma, "tone": "grandma"},
        {"label": "NAYA", "body": naya, "tone": "naya"},
        {"label": "MACHINE", "body": machine, "tone": "machine"},
        {"label": "WEAVER", "body": connections, "tone": "weaver"},
    ]
    return {
        "event_id": event_id(path, text),
        "user_id": "canonical",
        "created_at": when,
        "updated_at": when,
        "source": {"type": "smart_note", "label": title},
        "human_input": {"raw": raw, "captured_at": when},
        "context": {
            "topic": title,
            "tags": ["Smart Note", "PIS", "Naya Power"],
            "canonical_path": str(path.relative_to(ROOT)).replace("\\", "/"),
        },
        "naya_interpretation": {
            "observation": nutshell,
            "interpretation": naya,
            "recommendation": action,
            "uncertainty": "Not stated in the source projection." if not naya else "Source uncertainty is preserved in the canonical Smart Note where present.",
        },
        "machine_evidence": {
            "items": [f"Canonical Smart Note: {path.relative_to(ROOT)}", "PIS projection generated from canonical GitHub Smart Note source."],
            "verification_state": "source-projection-generated",
        },
        "weaver_synthesis": {"summary": nutshell, "relationships": []},
        "lesson": {"text": lesson, "retained": True},
        "meaning": {"text": meaning, "significance": "Canonical Smart Note meaning"},
        "action": {"text": action, "status": "from-source"},
        "relationships": {"event_ids": [], "connection_ids": [], "space_ids": []},
        "privacy": {"visibility": "source-defined", "consent_state": "source-defined"},
        "trust": {"level": "source-projection", "evidence_ids": []},
        "status": "active",
        "perspectives": perspectives,
        "pis": {
            "source_ref": str(path.relative_to(ROOT)).replace("\\", "/"),
            "projection_version": "1.0",
            "timestamp_precision": "commit-or-day",
        },
    }


def main() -> None:
    notes = sorted(SOURCE.glob("*SMART-NOTE.md"), key=lambda p: p.name, reverse=True)
    events = [make_event(path) for path in notes]
    payload = {
        "schema_version": "PIS-1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": ".naya/*SMART-NOTE.md",
        "event_count": len(events),
        "events": events,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PIS_FEED_BUILT events={len(events)} output={OUTPUT}")


if __name__ == "__main__":
    main()
