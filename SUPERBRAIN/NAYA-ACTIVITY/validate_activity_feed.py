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

SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
TIMESTAMP_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2}T[^ ]+) — NAYA — (.+)$", re.MULTILINE)
REQUIRED_TERMS = [
    "WHAT I OBSERVED",
    "WHY I DID IT",
    "EVIDENCE",
    "WHY THIS IS NOT A 10",
    "NEXT BEST ACTION",
    "TAG → YOU'RE IT",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_day(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("# NayaPOWER — Naya-to-Naya Activity Feed"):
        fail(errors, f"{path}: missing canonical feed title")

    headings = TIMESTAMP_RE.findall(text)
    if not headings:
        fail(errors, f"{path}: no timestamped Naya events found")
        return

    timestamps: list[datetime] = []
    for raw, event in headings:
        try:
            timestamps.append(datetime.fromisoformat(raw))
        except ValueError:
            fail(errors, f"{path}: invalid timezone-aware timestamp: {raw}")
        if event.strip() in {"ACTION COMPLETE / DAILY STREAM INITIALIZED", "AAA RELAY CONTRACT"}:
            pass

    if timestamps != sorted(timestamps):
        fail(errors, f"{path}: event timestamps are not chronological")

    # Every completed-action or handoff block must carry the operational fields.
    starts = [m.start() for m in TIMESTAMP_RE.finditer(text)]
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(text)
        block = text[start:end]
        title = TIMESTAMP_RE.search(block).group(2)
        if "ACTION COMPLETE" in title or "HANDOFF" in title:
            for term in REQUIRED_TERMS:
                if term not in block:
                    fail(errors, f"{path}: {title}: missing required field/marker: {term}")

    # Evidence SHA claims must look like SHAs; do not require every entry to have one.
    for sha in SHA_RE.findall(text):
        if sha == "0" * 40:
            fail(errors, f"{path}: zero SHA is not valid evidence")

    if text.count("TAG → YOU'RE IT") < 1:
        fail(errors, f"{path}: no baton marker found")


def main() -> int:
    errors: list[str] = []

    if not PROTOCOL.exists():
        fail(errors, "missing NAYAPOWER-ACTIVITY-FEED-PROTOCOL.md")
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

    # The current board must point to the daily relay, not only describe a board.
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
    print("Chronology: valid")
    print("Required handoff fields: present")
    print("Current board relay pointers: present")
    print("Baton marker: present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
