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


def test_dispatch_fallback_persists_expected_content_for_cold_successor():
    wf = WORKFLOW.read_text(encoding="utf-8")
    fallback = wf[wf.index("          else:\n              lesson_key="):]
    fallback = fallback[:fallback.index("          pathlib.Path(\"lesson-request.json\")")]
    assert 'lesson_content="Preserve provenance before applying retained intelligence."' in fallback
    assert 'digest=hashlib.sha256(lesson_content.encode()).hexdigest()' in fallback
    assert 'pathlib.Path("smart-note-expected.json").write_text' in fallback
    assert '"expected_content":lesson_content' in fallback
    assert '"content_hash":digest' in fallback


def test_dispatch_cold_successor_uses_persisted_lineage_when_no_projection_exists():
    wf = WORKFLOW.read_text(encoding="utf-8")
    marker = '          capture_path=open("capture-path.txt").read().strip()'
    start = wf.index(marker)
    end = wf.index('          python - <<\'PY\'', start)
    block = wf[start:end]
    assert 'if capture_path:' in block
    assert 'fresh-lesson-lineage-ids.json' in block
    assert 'intelligent_block_id' in block
    assert 'reg["entries"]' in block


def test_cold_successor_runtime_reread_has_bounded_empty_body_retry():
    wf = WORKFLOW.read_text(encoding="utf-8")
    start = wf.index('          for attempt in 1 2 3; do', wf.index('cold-verify-request.json'))
    end = wf.index('          python - <<\'PY\'', start)
    block = wf[start:end]
    assert 'for attempt in 1 2 3; do' in block
    assert 'cold-runtime-reread.json' in block
    assert 'if [[ -s cold-runtime-reread.json ]]' in block
    assert 'sleep 2' in block
    assert 'exit 1' in block



def test_cold_successor_uses_verify_contract_runtime_and_pinned_source():
    # The cold-successor job POSTs {"mode":"verify", <lineage ids>} and consumes
    # {checks, persisted}. Only nayanet-intelligence-commit-runtime honors the
    # body-"verify" contract; nayanet-cold-runtime-proof is hard-bound to
    # live-supabase-runtime-proof.yml (WORKFLOW_BINDING_MISMATCH) and has no
    # body-"verify" mode (UNSUPPORTED_MODE). See self-build-loop cycle 2026-09-30.
    wf = WORKFLOW.read_text(encoding="utf-8")
    start = wf.index("  cold-successor-held-out:")
    end = wf.index("  independent-behavior-verification:", start)
    block = wf[start:end]
    assert "ref: ${{ env.SOURCE_SHA }}" in block
    assert '"$RUNTIME_FUNCTION"' in block
    assert '"$COLD_RUNTIME_FUNCTION"' not in block
