from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEARN = ROOT / "supabase" / "functions" / "nayanet-learning-verify" / "index.ts"
PROMOTION = ROOT / ".github" / "workflows" / "governed-supabase-production-deploy.yml"
PRODUCER = ROOT / ".github" / "workflows" / "live-intelligence-commit-proof.yml"


def test_historical_checkpoint_reconstructs_from_immutable_commit_receipt():
    source = LEARN.read_text(encoding="utf-8")
    assert "IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT" in source
    assert 'commitReceipt?.action === "intelligence_commit"' in source
    for field in (
        "checkpoint_id", "event_row_id", "intelligent_block_id",
        "lineage_id", "relationship_id", "index_id"
    ):
        assert field in source
    assert "immutable_receipt_reconstruction: false" in source


def test_historical_learning_does_not_clobber_current_mutable_checkpoint():
    source = LEARN.read_text(encoding="utf-8")
    assert 'const historicalCheckpoint = (observed as any).checkpoint_provenance === "IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT"' in source
    assert "if (!historicalCheckpoint)" in source
    assert '"LEARNED_VIA_IMMUTABLE_RECEIPT"' in source
    assert "historical_receipt_lock_in" in source


def test_promotion_dispatches_required_exact_producer_source_sha():
    workflow = PROMOTION.read_text(encoding="utf-8")
    assert 'gh workflow run "$PRODUCER_WORKFLOW" --repo "$GITHUB_REPOSITORY" --ref main -f expected_source_sha="$GITHUB_SHA"' in workflow


def test_cold_successor_can_reconstruct_expected_payload_from_capture():
    workflow = PRODUCER.read_text(encoding="utf-8")
    assert 'except FileNotFoundError:' in workflow
    assert 'capture_path=open("capture-path.txt").read().strip()' in workflow
    assert 'hashlib.sha256(distilled.encode()).hexdigest()' in workflow


def test_historical_promotion_records_lock_in_on_original_commit_receipt():
    source = LEARN.read_text(encoding="utf-8")
    assert 'historicalCommitReceiptId = String((observed as any).commit_receipt_id || "")' in source
    assert 'historical_checkpoint_provenance: "IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT"' in source
    assert "historical_commit_receipt: historicalCommitReceipt" in source


def test_sn015_graph_applicability_is_predeclared():
    source = LEARN.read_text(encoding="utf-8")
    assert "active_intelligence_sensitive" in source
    assert "Persistence and retrieval never create verification or authority" in source


def test_runtime_generalizes_active_intelligence_without_forcing_provenance_task():
    runtime = (ROOT / "supabase/functions/nayanet-cold-runtime-proof/index.ts").read_text(encoding="utf-8")
    assert "NAYA-0001-ACTIVE-INTELLIGENCE-HELDOUT-002" in runtime
    assert "COLD-NAYA-GRAPH-ACTIVE-INTELLIGENCE-001" in runtime
    assert "REQUIRE_TRUTH_AND_AUTHORITY_BOUNDARIES_BEFORE_APPLY" in runtime
    assert "active_intelligence_discipline" in runtime


def test_independent_causal_verifier_knows_active_intelligence_tasks():
    verifier = (ROOT / "supabase/functions/nayanet-causal-learning-experiment/index.ts").read_text(encoding="utf-8")
    assert "NAYA-0001-ACTIVE-INTELLIGENCE-HELDOUT-001" in verifier
    assert "NAYA-0001-ACTIVE-INTELLIGENCE-HELDOUT-002" in verifier
    assert "active_intelligence_discipline" in verifier
    assert "related_outcome_delta:{metric:relatedMetric,value:relatedOutcomeDelta}" in verifier


def test_runtime_workflow_selects_graph_and_successor_tasks_from_actual_learning():
    workflow = (ROOT / ".github/workflows/live-supabase-runtime-proof.yml").read_text(encoding="utf-8")
    assert "graph-task-id.txt" in workflow
    assert "related-task-id.txt" in workflow
    assert "NAYA-0001-ACTIVE-INTELLIGENCE-HELDOUT-002" in workflow
    assert "COLD-NAYA-GRAPH-ACTIVE-INTELLIGENCE-001" in workflow
