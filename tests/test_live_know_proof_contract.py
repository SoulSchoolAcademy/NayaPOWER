from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/live-know-proof.yml"

def test_live_know_proof_does_not_hardcode_historical_selected_block():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert 'selected_block_id"]=="IB-NAYA-NODE-0001-0001"' not in text
    assert 'positive_selected_block_id' in text
    assert 'selected_epistemic_state' in text
    assert 'provenance_preservation' in text
    assert 'retrieval_creates_authority' in text
