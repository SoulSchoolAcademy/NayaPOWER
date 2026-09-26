#!/usr/bin/env python3
"""INT-001 machine-checkable Smart Link acceptance tests."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))

from smart_note_transaction import canonical_smart_note_path  # noqa: E402
from smart_link_verifier import classify_smart_link, build_smart_link, classify_link_kind, receiver_link_correspondence, validate_smart_note_structure  # noqa: E402


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

    # Structural acceptance — required 15-section Smart Note order.
    for real_note in (
        ROOT / ".naya/memory/smart-notes/2026/09/25/system/"
        "canonical-memory-receiver/IB-001019/smart-note.md",
        ROOT / ".naya/memory/smart-notes/2026/09/25/system/"
        "canonical-memory-organization/IB-001024/smart-note.md",
    ):
        assert validate_smart_note_structure(real_note.read_text(encoding="utf-8")) == (True, [])
    malformed = "\n".join([
        "# SMART NOTE",
        "## IN A NUTSHELL", "x", "## DATE / TIME", "x", "## WHAT", "x",
        "## WHY IT MATTERS", "x", "## HUMAN", "x", "## CHILD", "x",
        "## GRANDMA", "x", "## NAYA", "x", "## MACHINE", "x",
        "## WHAT WE LEARNED", "x", "## CONNECTIONS", "x",
        "## WHAT'S IN IT FOR YOU / US", "x", "## HOW TO APPLY", "x",
        "## WHAT IT ULTIMATELY MEANS", "x", "## NEXT ACTION", "x",
    ])
    ok, errors = validate_smart_note_structure(malformed)
    assert ok is False
    assert errors
    assert "section order" in " ".join(errors).lower()
    valid_synthetic = "\n".join(["# SMART NOTE"] + [f"## {section}\ncontent" for section in (
        "IN A NUTSHELL", "DATE / TIME", "WHAT", "WHY IT MATTERS", "HUMAN",
        "CHILD", "GRANDMA", "NAYA", "MACHINE", "WHAT WE LEARNED",
        "CONNECTIONS", "HOW TO APPLY", "WHAT IT ULTIMATELY MEANS",
        "WHAT'S IN IT FOR YOU / US", "NEXT ACTION",
    )])
    n_a_note = valid_synthetic.replace("## HOW TO APPLY\ncontent", "## HOW TO APPLY\nN/A", 1)
    ok, errors = validate_smart_note_structure(n_a_note)
    assert ok is True
    assert errors == []

    # D — exact vocabulary: Hub Deep Link, Smart Link, and Evidence Link cannot collapse.
    hub = "/hub?ib=IB-001061"
    smart = (
        "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/"
        ".naya/memory/smart-notes/2026/09/25/system/"
        "nayapower-daily-scorecard/IB-001061/smart-note.md"
    )
    evidence = "https://github.com/SoulSchoolAcademy/NayaPOWER/commit/abc123"
    assert classify_link_kind(hub) == "HUB_DEEP_LINK"
    assert classify_link_kind(hub) != "SMART_LINK"
    assert classify_link_kind(smart) == "SMART_LINK"
    assert classify_link_kind(evidence) == "EVIDENCE_LINK"
    assert classify_link_kind(
        "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/README.md"
    ) == "UNKNOWN"

    # F — classification/date changes move the projection but preserve the same IB.
    original_path = canonical_smart_note_path(
        "2026-09-25T23:56:53.224Z",
        "nayapower daily scorecard",
        "system",
        "IB-001061",
        ROOT / ".naya/memory/smart-notes",
    )
    reclassified_path = canonical_smart_note_path(
        "2026-10-02T12:00:00Z",
        "different topic",
        "another-category",
        "IB-001061",
        ROOT / ".naya/memory/smart-notes",
    )
    assert original_path.name == reclassified_path.name == "smart-note.md"
    assert original_path.parent.name == reclassified_path.parent.name == "IB-001061"
    assert original_path != reclassified_path
    assert original_path.parts[-2] == reclassified_path.parts[-2] == "IB-001061"

    # Receiver/link correspondence — path match alone is insufficient.
    note = ROOT / ".naya/memory/smart-notes/2026/09/25/system/nayapower-daily-scorecard/IB-001061/smart-note.md"
    receiver = {
        "intelligent_block_id": "IB-001061",
        "source_event_id": "62c2435f-4de2-4a63-9092-cdb39b034e2d",
        "canonical_receiver": "v7-smart-note-canonical",
    }
    assert receiver_link_correspondence(note, receiver, canonical_ref="main") is True
    assert receiver_link_correspondence(
        note, dict(receiver, intelligent_block_id="IB-001060"), canonical_ref="main"
    ) is False
    assert receiver_link_correspondence(
        note,
        dict(receiver, source_event_id="00000000-0000-0000-0000-000000000000"),
        canonical_ref="main",
    ) is False
    assert receiver_link_correspondence(
        note, dict(receiver, canonical_receiver="other-receiver"), canonical_ref="main"
    ) is False

    print("INT-001 acceptance tests passed + adversarial D/F/receiver-link cases")



if __name__ == "__main__":
    run()
