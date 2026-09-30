from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "governed-supabase-production-deploy.yml"


def test_blocked_summary_does_not_execute_reason_as_shell_command():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert 'echo "- reason: `$reason`"' not in workflow
    assert "printf -- '- reason: `%s`\\n' \"$reason\"" in workflow
    assert 'echo "- source: `$GITHUB_SHA`"' not in workflow
    assert "printf -- '- source: `%s`\\n' \"$GITHUB_SHA\"" in workflow
