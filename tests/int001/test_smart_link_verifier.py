#!/usr/bin/env python3
"""INT-001 deterministic adversarial acceptance tests."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))
from smart_note_transaction import canonical_smart_note_path
from smart_link_verifier import classify_link_kind, classify_smart_link, receiver_link_correspondence

def run():
    hub = "/hub?ib=IB-001061"
    smart = "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/.naya/memory/smart-notes/2026/09/25/system/nayapower-daily-scorecard/IB-001061/smart-note.md"
    evidence = "https://github.com/SoulSchoolAcademy/NayaPOWER/commit/abc123"
    assert classify_link_kind(hub) == "HUB_DEEP_LINK"
    assert classify_link_kind(hub) != "SMART_LINK"
    assert classify_link_kind(smart) == "SMART_LINK"
    assert classify_link_kind(evidence) == "EVIDENCE_LINK"
    assert classify_link_kind("https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/README.md") == "UNKNOWN"

    original = canonical_smart_note_path("2026-09-25T23:56:53.224Z", "nayapower daily scorecard", "system", "IB-001061", ROOT / ".naya/memory/smart-notes")
    reclassified = canonical_smart_note_path("2026-10-02T12:00:00Z", "different topic", "another-category", "IB-001061", ROOT / ".naya/memory/smart-notes")
    assert original.name == "smart-note.md" and reclassified.name == "smart-note.md"
    assert original.parent.name == "IB-001061" and reclassified.parent.name == "IB-001061"
    assert original != reclassified
    assert original.parts[-2] == reclassified.parts[-2] == "IB-001061"

    note = ROOT / ".naya/memory/smart-notes/2026/09/25/system/nayapower-daily-scorecard/IB-001061/smart-note.md"
    receiver = {"intelligent_block_id": "IB-001061", "source_event_id": "62c2435f-4de2-4a63-9092-cdb39b034e2d", "canonical_receiver": "v7-smart-note-canonical"}
    assert receiver_link_correspondence(note, receiver, canonical_ref="main") is True
    assert receiver_link_correspondence(note, dict(receiver, intelligent_block_id="IB-001060"), canonical_ref="main") is False
    assert receiver_link_correspondence(note, dict(receiver, source_event_id="00000000-0000-0000-0000-000000000000"), canonical_ref="main") is False
    assert receiver_link_correspondence(note, dict(receiver, canonical_receiver="other-receiver"), canonical_ref="main") is False
    print("INT-001 adversarial D/F/receiver-link tests passed")

if __name__ == "__main__": run()