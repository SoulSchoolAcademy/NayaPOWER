#!/usr/bin/env python3
"""Host-boundary regression: clear Smart Note capture must route to execution."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chatgpt_host_adapter import build_smart_note_capture_request


def test_chatgpt_host_builds_canonical_capture_request_from_plain_language():
    result = build_smart_note_capture_request(
        "SMART NOTE THIS",
        title="The NayaPOWER method",
        content="SYNERGIZE → OPTIMIZE → MAXIMIZE → EQUALIZE → ORGANIZE → DISTILL",
    )
    assert result["intent"]["operation"] == "CREATE"
    assert result["intent"]["canonical_receiver"] == "v7-smart-note-canonical"
    assert result["execution"]["mode"] == "CANONICAL_SMART_NOTE_CAPTURE"
    assert result["execution"]["human_note"]["title"] == "The NayaPOWER method"
    assert result["execution"]["required_outputs"] == [
        "intelligent_block_id",
        "verified_smart_link",
        "completion_receipt",
    ]
    assert result["execution"]["on_missing_evidence"] == "BLOCKED_NOT_EXPLANATION"


def test_chatgpt_host_does_not_turn_a_smart_note_question_into_creation():
    result = build_smart_note_capture_request("What is a Smart Note?", title="x", content="y")
    assert result["execution"]["mode"] == "NO_CANONICAL_CAPTURE"
    assert result["intent"]["operation"] == "NONE"


if __name__ == "__main__":
    test_chatgpt_host_builds_canonical_capture_request_from_plain_language()
    test_chatgpt_host_does_not_turn_a_smart_note_question_into_creation()
    print("PASS 2/2 ChatGPT Smart Note host-routing tests")
