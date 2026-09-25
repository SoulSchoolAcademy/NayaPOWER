from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/assistant-cloudflare-hub-release.yml"

def test_cloudflare_production_release_is_manual_only():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in source
    assert "\n  push:" not in source

def test_cloudflare_release_requires_explicit_authorization_record():
    source = WORKFLOW.read_text(encoding="utf-8")
    required = [
        ".naya/control-plane/RELEASE-AUTHORIZATION.json",
        'auth.get("status") != "AUTHORIZED"',
        'auth.get("commit_sha") != expected_sha',
        'auth.get("target_environment") != "production"',
        'auth.get("deployment_surface") != "cloudflare"',
        'auth.get("approval") != "EXPLICIT_APPROVAL_GRANTED"',
        'auth.get("verification",{}).get("status") != "PRE_DEPLOYMENT_PASS"',
    ]
    for marker in required:
        assert marker in source, f"missing governed-release marker: {marker}"
