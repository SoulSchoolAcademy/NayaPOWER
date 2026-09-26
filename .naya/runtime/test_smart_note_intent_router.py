#!/usr/bin/env python3
"""Regression gate for the canonical Smart Note conversational intent boundary.

This test exists because a clear Smart Note capture request must be treated as
an executable canonical operation, not as a request for explanation.

The router does not create persistence or allocate an IB. It only determines
the required operation and the evidence contract that the execution layer must
satisfy.
"""
from __future__ import annotations

import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent
sys.path.insert(0, str(RUNTIME))

from smart_note_intent_router import resolve_smart_note_intent


def test_explicit_smart_note_capture_is_an_action_not_a_question():
    result = resolve_smart_note_intent("SMART NOTE THIS")
    assert result["intent"] == "CANONICAL_SMART_NOTE_CAPTURE"
    assert result["operation"] == "CREATE"
    assert result["canonical_receiver"] == "v7-smart-note-canonical"
    assert result["requires_clarification"] is False
    assert result["required_evidence"] == [
        "receiver_persistence",
        "intelligent_block_id",
        "repository_projection",
        "verified_smart_link",
    ]


def test_capture_variants_resolve_to_the_same_canonical_operation():
    phrases = [
        "make this a smart note",
        "capture this as a smart note",
        "save this as a smart note",
        "turn this into a smart note",
        "smart note this please",
    ]
    for phrase in phrases:
        result = resolve_smart_note_intent(phrase)
        assert result["intent"] == "CANONICAL_SMART_NOTE_CAPTURE"
        assert result["operation"] == "CREATE"
        assert result["requires_clarification"] is False


def test_questions_and_lookup_requests_do_not_trigger_creation():
    for phrase in (
        "what is a smart note?",
        "show me my smart note",
        "find the smart note",
        "where is the smart link?",
    ):
        result = resolve_smart_note_intent(phrase)
        assert result["intent"] != "CANONICAL_SMART_NOTE_CAPTURE"
        assert result["operation"] == "NONE"


def test_capture_result_cannot_be_complete_without_smart_link():
    result = resolve_smart_note_intent("SMART NOTE THIS")
    assert result["completion_rule"] == "NO_SMART_LINK_NO_COMPLETION"
    assert result["smart_link_type"] == "DIRECT_GITHUB_SMART_NOTE"


if __name__ == "__main__":
    tests = [
        test_explicit_smart_note_capture_is_an_action_not_a_question,
        test_capture_variants_resolve_to_the_same_canonical_operation,
        test_questions_and_lookup_requests_do_not_trigger_creation,
        test_capture_result_cannot_be_complete_without_smart_link,
    ]
    for test in tests:
        test()
    print(f"PASS {len(tests)}/{len(tests)} Smart Note intent regression tests")
