from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / ".github" / "workflows" / "live-intelligence-commit-proof.yml"
CONSUMER = ROOT / ".github" / "workflows" / "live-supabase-runtime-proof.yml"


def test_live_runtime_proof_consumes_the_actual_producer_lineage_artifact():
    producer = PRODUCER.read_text(encoding="utf-8")
    consumer = CONSUMER.read_text(encoding="utf-8")
    assert "name: smart-note-lineage" in producer
    assert "name: smart-note-lineage" in consumer
    assert "name: fresh-lesson-lineage" not in consumer
    assert "fresh-lesson-lineage-ids.json" in producer
    assert "fresh-lineage/fresh-lesson-lineage-ids.json" in consumer
