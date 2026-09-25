from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/verify-human-smart-note-capture.yml"


def test_human_proof_binds_to_live_canonical_feed_surface():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "DEPLOYED_SOURCE_SHA: ${{ inputs.deployed_source_sha }}" in source
    assert "deployed_source_sha:\n        description: 'Source SHA known to be deployed at HUB_URL'\n        required: true" in source
    assert "page.locator('#blocks [" in source
    assert ".feedNav button[data-feed=\"activity\"]" in source
    assert "document.querySelectorAll('#blocks [data-event-id]')" in source
    assert "#naya-smart-feed-v2" not in source
