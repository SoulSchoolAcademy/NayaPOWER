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
