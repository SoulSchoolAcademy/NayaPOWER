from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "live-supabase-runtime-proof.yml"


def test_learning_promotion_uses_existing_oidc_bound_verifier_and_causal_evidence():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "learning-promotion" in source
    assert "nayanet-learning-verify" in source
    assert "SUPABASE_USER_ACCESS_TOKEN" not in source
    assert "oidc.jwt" in source
    assert "ACTIONS_ID_TOKEN_REQUEST_TOKEN" in source
    assert '"evidence_refs"' in source
    assert "f91fc48a-3d34-41aa-b51e-17b4ce89a3e2" in source
    assert "independent-learning-influence-verification" in source
    assert "needs: independent-learning-influence-verification" in source


def test_learning_promotion_does_not_relax_runtime_oidc_binding_or_mutate_sql_directly():
    influence = (ROOT / ".github" / "workflows" / "live-learning-influence-proof.yml").read_text(encoding="utf-8")
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "SUPABASE_USER_ACCESS_TOKEN" not in influence
    assert "update public.learning_evidence" not in source
    assert "status: ACTIVE" not in source


def test_learning_verifier_is_machine_authenticated_by_governed_oidc_not_user_session():
    source = (ROOT / "supabase" / "functions" / "nayanet-learning-verify" / "index.ts").read_text(encoding="utf-8")
    assert "createRemoteJWKSet" in source
    assert "jwtVerify" in source
    assert 'audience: AUDIENCE' in source
    assert 'payload.workflow_ref !== workflowRef' in source
    assert 'payload.repository !== REPOSITORY' in source
    assert 'payload.ref !== REF' in source
    assert 'auth.getUser' not in source
    assert 'SUPABASE_USER_ACCESS_TOKEN' not in source
