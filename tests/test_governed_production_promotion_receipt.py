from pathlib import Path

WORKFLOW = Path(".github/workflows/governed-supabase-production-deploy.yml")

def test_child_polling_selects_only_exact_authorized_head_dispatch():
    source = WORKFLOW.read_text(encoding="utf-8")
    producer = source[source.index("Dispatch canonical fresh-intelligence producer"):source.index("Dispatch canonical end-to-end runtime proof")]
    proof = source[source.index("Dispatch canonical end-to-end runtime proof"):source.index("Write durable production promotion receipt")]
    for section in (producer, proof):
        assert 'r.get("headSha")==os.environ["GITHUB_SHA"]' in section
        assert 'r.get("event")=="workflow_dispatch"' in section
        assert 'max(matches,key=lambda r:r["createdAt"])' in section

def test_parent_receipt_requires_successful_deployment_and_both_child_proofs():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "production-promotion-receipt.json" in source
    assert 'receipt["machine_deployment"]["supabase_check_conclusion"]=="success"' in source
    assert 'receipt["canonical_proof"]["producer_conclusion"]=="success"' in source
    assert 'receipt["canonical_proof"]["runtime_proof_conclusion"]=="success"' in source
