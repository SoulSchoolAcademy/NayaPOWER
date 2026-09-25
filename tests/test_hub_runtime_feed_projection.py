from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "NAYANET/HUB/index.html"

def test_canonical_hub_exposes_live_runtime_feed_projection():
    source = HUB.read_text(encoding="utf-8")
    for marker in [
        "NayaRuntimeFeedProjection",
        "smartFeed({stream:'personal'",
        "data-runtime-event-id",
        "data-event-id",
        "PROJECT_INTELLIGENCE_BRIDGE",
    ]:
        assert marker in source, f"missing live runtime feed projection marker: {marker}"

def test_runtime_feed_projection_preserves_owner_scoped_runtime_identity():
    source = HUB.read_text(encoding="utf-8")
    assert "stream:'personal'" in source
    assert "data-source-ref" in source
    assert "data-receipt-id" in source
    assert "data-packet-id" in source
