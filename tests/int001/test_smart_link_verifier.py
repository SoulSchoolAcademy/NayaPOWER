#!/usr/bin/env python3
"""INT-001 adversarial acceptance tests for vocabulary, identity, and receiver/link correspondence."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))

from smart_link_verifier import (  # noqa: E402
    build_smart_link,
    classify_link_kind,
    classify_smart_link,
    receiver_link_correspondence,
)


def run():
    # D — exact vocabulary: runtime Hub URLs are never Smart Links.
    hub = "/hub?ib=IB-001061"
    assert classify_link_kind(hub) == "HUB_DEEP_LINK"
    assert classify_link_kind(hub) != "SMART_LINK"
    assert classify_link_kind(
        "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/"
        ".naya/memory/smart-notes/2026/09/25/system/nayapower-daily-scorecard/"
        "IB-001061/smart-note.md"
    ) == "SMART_LINK"
    assert classify_link_kind(
        "https://github.com/SoulSchoolAcademy/NayaPOWER/commit/abc123"
    ) == "EVIDENCE_LINK"

    # F — identity preservation: reclassification/date changes move the projection
    # but preserve the receiver-issued IB identity.
    original = ROOT / ".naya/memory/smart-notes/2026/09/25/system/example/IB-001061/smart-note.md"
    reclassified = ROOT / ".naya/memory/smart-notes/2026/10/02/another-topic/IB-001061/smart-note.md"
    assert original.parent.name == "IB-001061"
    assert reclassified.parent.name == "IB-001061"
    assert original.parent.name == reclassified.parent.name
    assert classify_smart_link(reclassified, "IB-001061", True, True, "main") in {
        "MISSING", "VERIFIED"
    }

    # Receiver/link correspondence — the repository projection must join to the
    # receiver-issued identity and source event; a matching path alone is not enough.
    note = ROOT / ".naya/memory/smart-notes/2026/09/25/system/nayapower-daily-scorecard/IB-001061/smart-note.md"
    receiver = {
        "intelligent_block_id": "IB-001061",
        "source_event_id": "62c2435f-4de2-4a63-9092-cdb39b034e2d",
        "canonical_receiver": "v7-smart-note-canonical",
    }
    assert receiver_link_correspondence(
        note,
        receiver,
        canonical_ref="main",
    ) is True

    wrong_identity = dict(receiver, intelligent_block_id="IB-001060")
    assert receiver_link_correspondence(
        note,
        wrong_identity,
        canonical_ref="main",
    ) is False

    wrong_event = dict(receiver, source_event_id="00000000-0000-0000-0000-000000000000")
    assert receiver_link_correspondence(
        note,
        wrong_event,
        canonical_ref="main",
    ) is False

    print("INT-001 adversarial D/F/receiver-link tests passed")


if __name__ == "__main__":
    run()
