from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "live-supabase-runtime-proof.yml"


def _workflow() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_live_generalization_chain_reuses_existing_runtime_and_learning_pipeline():
    raw = _workflow()
    for job in (
        "active-learning-generalization:",
        "independent-active-learning-generalization:",
        "cold-successor-generalization:",
        "cold-successor-generalization-verification:",
    ):
        assert job in raw

    assert "?mode=learning-generalization" in raw
    # The independent verifier request must explicitly select the existing verifier
    # mode; the workflow builds this JSON via Python json.dump rather than a second
    # verification service or pipeline.
    assert '"mode":"verify-generalization"' in raw.replace(" ", "")
    assert '"mode":"candidate"' in raw.replace(" ", "")
    assert "nayanet-causal-learning-experiment" in raw
    assert "nayanet-learning-verify" in raw


def test_live_generalization_chain_requires_active_learning_and_current_runtime_parity_gate():
    raw = _workflow()
    generalization_block = raw.split("  active-learning-generalization:", 1)[1].split("\n  independent-active-learning-generalization:", 1)[0]
    assert "independent-retained-learning-reread" in generalization_block
    assert "live-connect" in generalization_block
    assert 'r["learning_status"] == "ACTIVE"' in generalization_block
    assert 'r["deployed_source_revision"] == os.environ["SOURCE_SHA"]' in generalization_block


def test_live_generalization_chain_contains_related_and_unrelated_tasks():
    raw = _workflow()
    assert "NAYA-0001-PROVENANCE-HELDOUT-002" in raw
    assert "NAYA-0001-UNRELATED-ARITHMETIC-001" in raw
    assert 'r["result"]["related_heldout_improved"] is True' in raw
    assert 'r["result"]["unrelated_negative_transfer_refused"] is True' in raw


def test_independent_generalization_verifier_must_bite():
    raw = _workflow()
    block = raw.split("  independent-active-learning-generalization:", 1)[1].split("\n  cold-successor-generalization:", 1)[0]
    assert '"mode":"verify-generalization"' in block.replace(" ", "")
    assert 'v["independent_verification"] is True' in block
    assert 'v["executor_claim_trusted"] is False' in block
    assert 'v["recomputed"]["related_causal_supported"] is True' in block
    assert 'v["recomputed"]["negative_transfer_refused"] is True' in block
    assert 'v["recomputed"]["unrelated_behavior_delta"] is False' in block
    assert 'v["token_jti"] != e.get("token_jti")' in block


def test_cold_successor_generalization_preserves_non_inheritance_and_refusal():
    raw = _workflow()
    block = raw.split("  cold-successor-generalization:", 1)[1].split("\n  cold-successor-generalization-verification:", 1)[0]
    assert "mode=cold-successor&learning_id=" in block
    assert "related_task_id=" in block
    assert "task_id=${related_task_id}" in block
    assert "NAYA-0001-PROVENANCE-HELDOUT-002" in block
    assert "NAYA-0001-ACTIVE-INTELLIGENCE-HELDOUT-002" in block
    assert "task_id=NAYA-0001-UNRELATED-ARITHMETIC-001" in block
    assert 'x["authority_boundary"]["authority_inherited"] is False' in block
    assert 'x["authority_boundary"]["successor_grant_count"] == 0' in block
    assert 'x["authority_boundary"]["executed"] is False' in block
    assert 'u["use"]["correct_refusal"] is True' in block


def test_successor_verifier_recomputes_both_task_contexts_independently():
    raw = _workflow()
    block = raw.split("  cold-successor-generalization-verification:", 1)[1].split("\n  cold-successor:", 1)[0]
    assert "mode=cold-successor-verify" in block
    assert 'v["executor_claim_trusted"] is False' in block
    assert 'v["recomputed"]["successor_grant_count"] == 0' in block
    assert 'vu["recomputed"]["correct_refusal"] is True' in block
    normalized = block.replace(" ", "")
    assert '"independent_verification":vr["independent_verification"]andvu["independent_verification"]' in normalized
    assert '"independent_verification_basis":{' in normalized
    assert '"verifier_mode":"AUTHORITATIVE_REREAD_AND_RECOMPUTATION"' in normalized
