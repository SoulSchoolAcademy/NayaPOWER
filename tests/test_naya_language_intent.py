from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))

from naya_language_intent import interpret_naya_language


def test_node_aliases_resolve_to_one_semantic_intent():
    commands = [
        "smart node this",
        "naya node this",
        "smart note this",
        "note this",
        "remember this",
        "capture this",
        "document this",
    ]
    for command in commands:
        result = interpret_naya_language(command)
        assert result.intent == "CREATE_OR_UPDATE_NAYA_NODE"
        assert result.requires_clarification is False


def test_play_is_a_semantic_command_not_a_storage_command():
    result = interpret_naya_language("Naya, play")
    assert result.intent == "PLAY_INTELLIGENCE"
    assert result.requires_clarification is False


def test_materially_ambiguous_request_requires_clarification():
    result = interpret_naya_language("make it better")
    assert result.intent == "UNKNOWN"
    assert result.requires_clarification is True
    assert "Is this your intention?" in result.clarifying_question


def test_unknown_wording_does_not_get_invented_permissions():
    result = interpret_naya_language("publish this everywhere")
    assert result.intent == "UNKNOWN"
    assert result.requires_clarification is True
    assert result.authority_expansion is False
