from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/verify-live-smart-note-receiver.yml"


def test_live_receiver_proof_uses_the_canonical_real_feed_card():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert source.count("#blocks [data-real-smart-note][data-event-id=") >= 5
    assert "pageA.locator('[data-event-id=" not in source
    assert "freshPage.locator('[data-event-id=" not in source
    assert source.count("&stream=personal&receiver_proof=") >= 2
    assert "data-intelligent-block-schema" in source
