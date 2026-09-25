from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/verify-smart-share-canonical.yml"

def test_smart_share_proof_is_manual_and_fail_closed():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "branches: [main]" not in source
    assert "workflow_dispatch:" in source
    assert "ALLOW_LEGACY_SMART_SHARE_DIAGNOSTIC" in source
    assert "LEGACY_SMART_SHARE_DIAGNOSTIC_BLOCKED" in source
    assert source.index("ALLOW_LEGACY_SMART_SHARE_DIAGNOSTIC") < source.index("chromium.launch")
