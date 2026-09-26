#!/usr/bin/env python3
"""INT-001 machine-checkable Smart Link acceptance tests."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))

from smart_link_verifier import classify_smart_link, build_smart_link  # noqa: E402


def run():
    for ib, path in (
        (
            "IB-001019",
            ROOT / ".naya/memory/smart-notes/2026/09/25/system/"
            "canonical-memory-receiver/IB-001019/smart-note.md",
        ),
        (
            "IB-001024",
            ROOT / ".naya/memory/smart-notes/2026/09/25/system/"
            "canonical-memory-organization/IB-001024/smart-note.md",
        ),
    ):
        assert classify_smart_link(path, ib, True, True, "main") == "VERIFIED"

    note = ROOT / ".naya/memory/smart-notes/2026/09/25/system/nayapower-daily-scorecard/IB-001061/smart-note.md"
    assert classify_smart_link(note, "IB-001061", True, True, "main") == "VERIFIED"
    assert build_smart_link(note, "main") == (
        "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/"
        ".naya/memory/smart-notes/2026/09/25/system/"
        "nayapower-daily-scorecard/IB-001061/smart-note.md"
    )

    missing = ROOT / ".naya/memory/smart-notes/2026/09/25/system/not-present/IB-999999/smart-note.md"
    assert classify_smart_link(missing, "IB-999999", True, True, "main") == "MISSING"

    pending = ROOT / ".naya/memory/smart-notes/2026/09/25/system/not-present/IB-888888/smart-note.md"
    assert classify_smart_link(pending, "IB-888888", True, False, "main") == "PENDING"

    conflicted = ROOT / "tests/fixtures/int001-conflicted-smart-note.md"
    assert classify_smart_link(conflicted, "IB-001061", True, True, "main") == "CONFLICTED"

    assert classify_smart_link(missing, "IB-777777", False, False, "main") == "UNKNOWN"

    print("INT-001 acceptance tests passed")


if __name__ == "__main__":
    run()
