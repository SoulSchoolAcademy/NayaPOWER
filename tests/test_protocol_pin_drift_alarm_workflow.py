"""Contract tests for the automatic protocol pin drift caller.

The detector's behavioral tests live in test_protocol_pin_drift_alarm.py.
These tests protect the wiring: a real main change invokes the detector,
only explicit clean state is healthy, and alerts are idempotent/non-blocking.
"""
from pathlib import Path

WORKFLOW = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "workflows"
    / "automatic-protocol-pin-drift-alarm.yml"
)


def test_drift_alarm_is_wired_to_protocol_and_pin_changes():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert 'branches: ["main"]' in text
    assert '"PROTOCOL.md"' in text
    assert '"tools/protocol_pin.py"' in text
    assert "workflow_dispatch:" in text


def test_only_explicit_clean_readable_result_counts_as_healthy():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert 'healthy = rc == 0 and payload.get("alarm") is False' in text
    assert "drift or unreadable pin; fail closed" in text
    assert 'if steps.drift.outputs.alarm == \'true\'' in text


def test_alarm_is_idempotent_and_does_not_repin_or_block_work():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "<!-- NAYA-PROTOCOL-PIN-DRIFT-ALARM -->" in text
    assert "github.rest.issues.updateComment" in text
    assert "github.rest.issues.createComment" in text
    assert "never silently re-pins law" in text
    assert "never blocks ordinary work" in text
    assert "Required-check" not in text


def test_workflow_preserves_diagnostic_text_in_single_line_output():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert 'detail=\\{safe\\}' not in text  # guard against regex-escaped output templates
    assert 'f"detail={safe}\\n"' in text
    assert 'safe = detail.replace("\\r", " ").replace("\\n", " ")' in text
