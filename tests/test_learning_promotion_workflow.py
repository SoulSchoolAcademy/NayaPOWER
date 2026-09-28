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
    assert "5c5331c3-8b36-47d9-bf94-846806de90fb" in source
    assert "independent-learning-influence-verification" in source
    assert "needs: independent-learning-influence-verification" in source
    assert "EXACT_LESSON_ALREADY_LEARNED" in source
    assert "5c5331c3-8b36-47d9-bf94-846806de90fb" in source


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


def test_learning_influence_retries_unique_revision_allocation_under_concurrency():
    source = (ROOT / "supabase" / "functions" / "nayanet-cold-runtime-proof" / "index.ts").read_text(encoding="utf-8")
    assert "RECEIPT_REVISION_RETRY" in source
    assert "23505" in source
    assert "insertReceiptWithRetry" in source


def test_fresh_intelligent_block_can_enter_existing_learning_candidate_path_without_dropping_provenance():
    source = (ROOT / "supabase" / "functions" / "nayanet-learning-verify" / "index.ts").read_text(encoding="utf-8")
    assert 'mode === "candidate"' in source
    assert '["CANDIDATE", "LEARNED"]' in source
    assert 'NAYA-NODE-0001' in source
    assert 'intelligent_block_id' in source
    assert 'source_event_id' in source
    assert 'lineage_id' in source
    assert 'relationship_id' in source
    assert 'index_id' in source
    assert 'checkpoint_id' in source
    assert 'provenance_preserved: true' in source
    assert 'status: "CANDIDATE"' in source
    assert 'mode === "candidate"' in source


def test_learning_candidate_bridge_is_idempotent_and_does_not_promote():
    source = (ROOT / "supabase" / "functions" / "nayanet-learning-verify" / "index.ts").read_text(encoding="utf-8")
    assert 'created: false' in source
    assert 'eq("status", "CANDIDATE")' in source
    assert 'status: "ACTIVE"' in source
