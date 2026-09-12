#!/usr/bin/env python3
"""Deterministic integrity validator for the NayaPOWER daily Activity Feed."""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DAILY = ROOT / "DAILY"
PROTOCOL = ROOT / "NAYAPOWER-ACTIVITY-FEED-PROTOCOL.md"
BOARD = ROOT / "00-NAYAPOWER-CURRENT-ACTIVITY-BOARD.md"
HANDOFF_CONTRACT = ROOT / "NAYA-COMPLETE-HANDOFF-CONTRACT.md"

SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
TIMESTAMP_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2}T[^ ]+) — NAYA — (.+)$", re.MULTILINE)
NEXT_ACTION_RE = re.compile(r"^(?:\*\*NEXT BEST ACTION:\*\*|## NEXT BEST ACTION\s*$)", re.MULTILINE)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_day(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("# NayaPOWER — Naya-to-Naya Activity Feed"):
        fail(errors, f"{path}: missing canonical feed title")

    matches = list(TIMESTAMP_RE.finditer(text))
    if not matches:
        fail(errors, f"{path}: no timestamped Naya events found")
        return

    timestamps: list[datetime] = []
    for match in matches:
        raw = match.group(1)
        try:
            parsed = datetime.fromisoformat(raw)
            if parsed.tzinfo is None:
                fail(errors, f"{path}: timestamp is missing timezone: {raw}")
            timestamps.append(parsed)
        except ValueError:
            fail(errors, f"{path}: invalid timestamp: {raw}")

    chronology_warning = False
    if len(timestamps) == len(matches) and timestamps != sorted(timestamps):
        chronology_warning = True

    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.start():end]
        title = match.group(2)

        is_historical_bootstrap = title == "ACTION COMPLETE / DAILY STREAM INITIALIZED"

        if "ACTION COMPLETE" in title and not is_historical_bootstrap:
            required = [
                "What I did",
                "Why",
                "Current state",
                "Verification status",
                "WHY THIS IS NOT A 10",
                "NEXT BEST ACTION",
                "TAG → YOU'RE IT",
            ]
            for term in required:
                if term not in block:
                    fail(errors, f"{path}: {title}: missing required field: {term}")

        if "HANDOFF" in title:
            required = [
                "NEXT BEST ACTION",
                "Protected boundaries",
                "WHY THIS IS NOT A 10",
                "TAG → YOU'RE IT",
            ]
            for term in required:
                if term not in block:
                    fail(errors, f"{path}: {title}: missing required field: {term}")
            handoff_markers = [
                "### NEXT NAYA EXECUTION PROMPT",
                "### NEXT NAYA EXECUTION PROMPT — EXECUTE NOW",
                "### NEXT NAYA TORCH",
                "### NEXT NAYA — READY TO RUN",
                "## EXECUTION INSTRUCTION FOR NEXT NAYA",
            ]
            if not any(marker in block for marker in handoff_markers):
                fail(errors, f"{path}: {title}: missing complete successor prompt/torch")

    latest = matches[-1]
    latest_block = text[latest.start():]
    successor_markers = [
        "### NEXT NAYA EXECUTION PROMPT",
        "### NEXT NAYA EXECUTION PROMPT — EXECUTE NOW",
        "### NEXT NAYA TORCH",
        "### NEXT NAYA — READY TO RUN",
        "## EXECUTION INSTRUCTION FOR NEXT NAYA",
    ]
    if not any(marker in latest_block for marker in successor_markers):
        fail(errors, f"{path}: latest event is missing a complete successor prompt/torch")

    latest_required = [
        "CURRENT STATE",
        "WHY THIS MATTERS",
        "WHAT HAS BEEN DONE",
        "WHAT THE EVIDENCE PROVES",
        "WHAT REMAINS UNKNOWN",
        "CURRENT SCORE / QUALITY GATE",
        "NEXT BEST ACTION",
        "EXECUTION INSTRUCTION FOR NEXT NAYA",
        "HANDOFF / CONTINUATION",
        "WHY THIS IS NOT A 10",
        "TAG → YOU'RE IT",
    ]
    for term in latest_required:
        if term not in latest_block:
            fail(errors, f"{path}: latest event missing complete-handoff field: {term}")

    next_action_count = len(NEXT_ACTION_RE.findall(latest_block))
    if next_action_count != 1:
        fail(
            errors,
            f"{path}: latest event must contain exactly one next-action field; found {next_action_count}",
        )

    for sha in SHA_RE.findall(text):
        if sha == "0" * 40:
            fail(errors, f"{path}: zero SHA is not valid evidence")

    if text.count("TAG → YOU'RE IT") < 1:
        fail(errors, f"{path}: no baton marker found")

    if chronology_warning:
        print(f"WARNING: {path}: event timestamps are not chronological; historical order preserved and textual append order is authoritative")


def main() -> int:
    errors: list[str] = []

    if not PROTOCOL.exists():
        fail(errors, "missing NAYAPOWER-ACTIVITY-FEED-PROTOCOL.md")
    if not HANDOFF_CONTRACT.exists():
        fail(errors, "missing NAYA-COMPLETE-HANDOFF-CONTRACT.md")
    if not BOARD.exists():
        fail(errors, "missing 00-NAYAPOWER-CURRENT-ACTIVITY-BOARD.md")
    if not DAILY.exists():
        fail(errors, "missing DAILY activity directory")
    else:
        days = sorted(DAILY.glob("*.md"))
        if not days:
            fail(errors, "DAILY contains no day feed files")
        for day in days:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}\.md", day.name):
                fail(errors, f"invalid daily feed filename: {day.name}")
            validate_day(day, errors)

    if BOARD.exists():
        board = BOARD.read_text(encoding="utf-8")
        for marker in ["FIRST-CLASS ACTIVITY FEED", "DAILY/", "TAG → YOU'RE IT"]:
            if marker not in board:
                fail(errors, f"current board missing relay marker: {marker}")

    if errors:
        print("ACTIVITY_FEED=RED")
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("ACTIVITY_FEED=GREEN")
    print("Daily feeds: valid")
    print("Chronology: warning-only for preserved historical anomalies")
    print("Required action/handoff fields: present")
    print("Latest event: complete successor contract present")
    print("Latest event: exactly one next-action field present")
    print("Current board relay pointers: present")
    print("Baton marker: present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
