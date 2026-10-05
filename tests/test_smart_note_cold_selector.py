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



def test_cold_successor_uses_canonical_lineage_verifier_and_pinned_source():
    wf = WORKFLOW.read_text(encoding="utf-8")
    start = wf.index("  cold-successor-held-out:")
    end = wf.index("  independent-behavior-verification:", start)
    block = wf[start:end]
    assert "ref: ${{ env.SOURCE_SHA }}" in block
    assert '--data-binary @cold-verify-request.json "$RUNTIME_FUNCTION"' in block
    assert "COLD_RUNTIME_FUNCTION" not in wf

    runtime = (ROOT / "supabase/functions/nayanet-intelligence-commit-runtime/index.ts").read_text(encoding="utf-8")
    assert '".github/workflows/live-intelligence-commit-proof.yml"' in runtime
    assert 'if (mode === "verify")' in runtime

def test_batch_cold_successor_distinguishes_active_from_superseded_lifecycle():
    import json

    wf = WORKFLOW.read_text(encoding="utf-8")
    start = wf.index('          capture=json.load(open(expected["capture_path"]))')
    end = wf.index('          PY\n            done', start)
    block = wf[start:end]

    assert 'lifecycle_state=str(capture.get("lifecycle_state","ACTIVE")).upper()' in block
    assert 'if lifecycle_state=="ACTIVE":' in block
    assert 'assert machine.get("raw_source_separate_from_distillation") is True' in block
    assert 'assert machine.get("automatic_truth_ceiling")=="CANDIDATE"' in block
    assert 'else:' in block
    assert 'from tools.sn002_conformance import check_dir' in block
    assert 'resolve_runtime_connections(successor_doc,reg)' in block
    assert '"relationship_type":"SUPERSEDES"' in block
    assert 'superseded_excluded_from_active_retrieval' in block
    assert 'active=sn.retrieve(capture["title"])' in block

    r1 = json.loads((ROOT / ".naya/capture/SMART-NOTE-20261005-sn0355-nonstop-loop.json").read_text(encoding="utf-8"))
    r2 = json.loads((ROOT / ".naya/capture/SMART-NOTE-20261005-sn0355-nonstop-loop-r2.json").read_text(encoding="utf-8"))
    assert r1["lifecycle_state"] == "SUPERSEDED"
    assert "raw_source_separate_from_distillation" not in r1["intelligence"]["machine_view"]
    assert r1["superseded_by_capture_id"] == r2["capture_id"]
    assert r2["lifecycle_state"] == "ACTIVE"
    assert r2["intelligence"]["machine_view"]["raw_source_separate_from_distillation"] is True
    assert r2["intelligence"]["machine_view"]["automatic_truth_ceiling"] == "CANDIDATE"
    assert any(
        (edge.get("type") or edge.get("relationship_type")) == "SUPERSEDES"
        and str(edge.get("target") or edge.get("target_block_id", "")).startswith("SN-346")
        for edge in r2["intelligence"]["connections"]
    )


def test_dispatch_replay_is_verify_only_and_cannot_create_missing_runtime_objects():
    wf = WORKFLOW.read_text(encoding="utf-8")
    assert "replay_capture_paths:" in wf
    assert "VERIFY_ONLY_REPLAY_INVALID_PATH" in wf
    assert "VERIFY_ONLY_REPLAY_MISSING_PATH" in wf
    assert wf.count("VERIFY_ONLY_REPLAY_REQUIRES_EXISTING_CANONICAL_HASH") == 2
    assert "replay-mode.txt" in wf
    start = wf.index("  independent-behavior-verification:")
    block = wf[start:]
    assert 'if lifecycle=="ACTIVE":' in block
    assert 'elif lifecycle=="SUPERSEDED":' in block
    assert '"NOT_APPLICABLE_HISTORICAL_OBJECT"' in block

def test_independent_behavior_job_downloads_lineage_batch_metadata():
    wf = WORKFLOW.read_text(encoding="utf-8")
    start = wf.index("  independent-behavior-verification:")
    block = wf[start:]
    assert "name: smart-note-lineage" in block
    assert "name: smart-note-cold-successor-proof" in block
    assert 'count="$(cat capture-count.txt)"' in block
    assert 'man=json.load(open("batch-manifest.json"))' in block
