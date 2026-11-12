"""Declared behavior change extraction (Lesson Law, SN-0815) — learning loop v1.

The extractor in tools/smart_note_v2.py turns the prose declaration in a
lesson note into a structured row {lesson_id, trigger, old_behavior,
new_behavior, verify_by} so a sampler can test whether the change held.
These tests pin: the two real note shapes (dedicated section; quoted
declaration inside another section), the negative control (no section ->
no row, no crash), the placeholder guard (the law's illustrative
"we do X instead of Y" is never data), explicit VERIFY_BY precedence, and
the three notes filed 2026-10-21 as living fixtures.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.smart_note_v2 import (
    declared_change_row,
    parse_declared_change,
    scan_declared_changes,
)

ROOT = Path(__file__).resolve().parents[1]

SECTION_NOTE = """# A Test Lesson

**ID:** IB-SMART-NOTE-20261022-sn9999-a-test-lesson
**Created:** 2026-10-22 01:00 UTC
**Category:** LEARNING / test

## IN A NUTSHELL

A test.

## THE DECLARED BEHAVIOR CHANGE

From tonight, when the widget jams, I clear it and log the jam in the
shared register before I report the shift done, instead of clearing it
quietly and moving on.

## WHAT IT ALL MEANS

Tests matter.
"""

QUOTED_NOTE = """# The Law Note Shape

**ID:** IB-SMART-NOTE-20261022-sn9998-the-law-note-shape
**Created:** 2026-10-22 01:00 UTC
**Category:** SYSTEM / governance

## IN A NUTSHELL

A lesson held in one seat's head, or left in a chat scroll, is not
learned by the team.

## NAYA

The standard arrives. THE DECLARED BEHAVIOR CHANGE (Director, chat,
2026-10-22 ~01:00Z — the North Star of this note): "From now on, every
lesson any Naya learns is filed as a titled Smart Note in the system,
and every lesson note declares the behavior change that results —
'from now on, we do X instead of Y.' A lesson without a declared
behavior change is not counted as learned."

## MACHINE

Rules: (1) TRIGGER: any seat learns a lesson (from a win, a failure)
-> a Smart Note filing is owed by that seat.
"""

NO_DECLARATION_NOTE = """# An Ordinary Note

**ID:** IB-SMART-NOTE-20261022-sn9997-an-ordinary-note
**Created:** 2026-10-22 01:00 UTC
**Category:** SYSTEM / misc

## IN A NUTSHELL

Nothing about lessons here. This note documents a config value.
"""


def test_section_shape_parses_all_fields():
    dc = parse_declared_change(SECTION_NOTE, created="2026-10-22", lesson_id="SN-9999")
    assert dc is not None
    assert dc["trigger"] == "when the widget jams"
    assert "clear it and log the jam in the shared register" in dc["new_behavior"]
    assert dc["old_behavior"] == "clearing it quietly and moving on"
    assert dc["verify_by"] == "2026-10-29"  # created + 7d sampler cadence
    assert dc["verify_by_source"].startswith("derived:")


def test_negative_control_no_section_no_row():
    assert parse_declared_change(NO_DECLARATION_NOTE, created="2026-10-22") is None
    assert declared_change_row(NO_DECLARATION_NOTE, note_path="SN-9997/x.md") is None


def test_empty_section_is_no_row():
    text = SECTION_NOTE.replace(
        "From tonight, when the widget jams, I clear it and log the jam in the\n"
        "shared register before I report the shift done, instead of clearing it\n"
        "quietly and moving on.", "")
    assert parse_declared_change(text, created="2026-10-22") is None


def test_quoted_marker_shape_and_placeholder_guard():
    row = declared_change_row(QUOTED_NOTE, note_path="BRAIN/x/SN-9998/note.md")
    assert row is not None
    dc = row["declared_change"]
    assert dc["trigger"] == "any seat learns a lesson (from a win, a failure)"
    # The illustrative placeholder inside the quote is form, not data:
    assert "we do X" not in (dc["new_behavior"] or "")
    assert (dc["old_behavior"] or "") != "Y"
    assert "held in one seat's head" in (dc["old_behavior"] or "")
    assert "is filed as a titled Smart Note" in dc["new_behavior"]


def test_explicit_verify_by_wins_over_derived():
    text = SECTION_NOTE + "\nVERIFY_BY: 2026-12-01\n"
    dc = parse_declared_change(text, created="2026-10-22")
    assert dc["verify_by"] == "2026-12-01"
    assert dc["verify_by_source"] == "explicit"


def test_tonights_three_notes_are_rows():
    rows = {r["lesson_id"]: r for r in scan_declared_changes()}
    for sn in ("SN-0815", "SN-0816", "SN-1787"):
        assert sn in rows, f"{sn} missing from declared-change scan"
        dc = rows[sn]["declared_change"]
        assert dc["trigger"], sn
        assert dc["new_behavior"], sn
        assert dc["old_behavior"], sn
        assert dc["verify_by"] == "2026-10-28", sn
    assert rows["SN-0816"]["declared_change"]["old_behavior"] == "reach for a benign story"
    assert rows["SN-1787"]["extraction"]["method"] == "quoted-marker"
