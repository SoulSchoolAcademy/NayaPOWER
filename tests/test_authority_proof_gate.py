from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = [
    ROOT / ".github/workflows/verify-p0-04-meaningful-output-promotion.yml",
    ROOT / ".github/workflows/verify-universal-meaningful-output-smart-feed-interaction.yml",
    ROOT / ".github/workflows/verify-smart-share-canonical.yml",
]

def test_authority_gate_precedes_browser_in_production_mutating_workflows():
    for path in WORKFLOWS:
        source = path.read_text(encoding="utf-8")
        gate = source.index("require-governed-authority-grant.mjs")
        assert gate < source.index("chromium.launch")
        assert "STREAM_E_AUTHORITY_GRANT_ID" in source

def test_authority_gate_emits_deterministic_error_codes():
    source = (ROOT / ".github/scripts/stream-e-authority-preflight.mjs").read_text(encoding="utf-8")
    assert "AUTHORITY_GRANT_REQUIRED" in source
    assert "AUTHORITY_GRANT_ID_INVALID" in source
    assert "authority_grant_id_present" in source
