from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "live-intelligence-commit-proof.yml"


def test_cold_successor_selects_current_capture_by_exact_content_hash():
    wf = WORKFLOW.read_text(encoding="utf-8")
    assert 'name: smart-note-lineage' in wf
    assert 'expected=json.load(open("smart-note-expected.json"))' in wf
    assert 'e.get("content_hash")==expected["content_hash"]' in wf
    assert 'exact_current_capture_retrieved' in wf
    assert 'e.get("smart_note_id")=="SN-001"' not in wf
    assert 'IB-SMART-NOTE-20260929-b8f141805fa0d7ae' not in wf


def test_cold_successor_behavior_preserves_truth_and_distillation_boundaries():
    wf = WORKFLOW.read_text(encoding="utf-8")
    assert '"promote_to_verified":False' in wf
    assert '"raw_transcript_is_canonical":False' in wf
    assert 'machine.get("automatic_truth_ceiling")=="CANDIDATE"' in wf
    assert 'machine.get("raw_source_separate_from_distillation") is True' in wf
