from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "live-learning-influence-proof.yml"


def test_learning_promotion_uses_existing_verifier_and_verified_causal_evidence():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "learning-promotion" in source
    assert "nayanet-learning-verify" in source
    assert "SUPABASE_USER_ACCESS_TOKEN" in source
    assert '"evidence_refs"' in source
    assert "CVO-NAYA-NODE-0001-FRESH-LEARNING-2026-09-28" in source
    assert "f91fc48a-3d34-41aa-b51e-17b4ce89a3e2" in source
    assert "f079f1e7-272d-467f-b776-a456de98a704" in source
    assert "8a7875eb-9d4b-44eb-af4c-c3f696fa46da" in source


def test_learning_promotion_does_not_directly_mutate_learning_state():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "update public.learning_evidence" not in source
    assert "status: ACTIVE" not in source
