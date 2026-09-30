from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "live-intelligence-commit-proof.yml"


def test_producer_runtime_failure_preserves_http_status_and_response_body():
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "curl -sS -w \"%{http_code}\"" in workflow
    assert '-o fresh-lesson-receipt.json' in workflow
    assert 'echo "runtime HTTP status: $http_code"' in workflow
    assert "cat fresh-lesson-receipt.json" in workflow
    assert 'RUNTIME_POST_FAILED status=$http_code' in workflow


def test_producer_keeps_fail_closed_semantics_after_observation():
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert '[ "$http_code" = "200" ]' in workflow
    assert "exit 1" in workflow
    assert "fresh-lesson-receipt.json" in workflow
