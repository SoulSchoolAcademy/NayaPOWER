from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/assistant-cloudflare-hub-release.yml"


def test_canonical_hub_production_release_is_not_push_triggered():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "  push:" not in source, "production Hub release must not auto-deploy on push"
    assert "  workflow_dispatch:" in source, "production Hub release must require explicit dispatch"
    assert source.count("  workflow_dispatch:") == 1


def test_canonical_release_requires_explicit_approval_binding():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert 'test "${APPROVAL}" = "EXPLICIT_APPROVAL_GRANTED"' in source
    assert 'test -n "${REASON}"' in source
