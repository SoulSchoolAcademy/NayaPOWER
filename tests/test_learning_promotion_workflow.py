from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "live-learning-influence-proof.yml"


def test_learning_promotion_uses_existing_verifier_and_verified_causal_evidence():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "learning-promotion" in source
    assert "nayanet-learning-verify" in source
    assert "SUPABASE_USER_ACCESS_TOKEN" in source
    assert '"evidence_refs"' in source
    assert "f91fc48a-3d34-41aa-b51e-17b4ce89a3e2" in source
    assert "treatment_receipt_id" not in source
    assert "independent-learning-influence-verification" in source


def test_learning_promotion_does_not_directly_mutate_learning_state():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "update public.learning_evidence" not in source
    assert "status: ACTIVE" not in source
