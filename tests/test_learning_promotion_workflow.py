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
    assert "workflow_run" in source
    assert "Live Intelligence Commit Proof" in source
    assert "github.event.workflow_run.id" in source
    assert "fresh-lesson-lineage" in source
    assert "fresh-lesson-lineage-ids.json" in source
    assert "IB-NAYA-FLOW-LESSON-3049c1cc637d41469f626c734f856c3c" not in source
    assert "independent-learning-influence-verification" in source
    assert "needs: independent-learning-influence-verification" in source
    assert "EXACT_LESSON_ALREADY_LEARNED" not in source
    assert "5c5331c3-8b36-47d9-bf94-846806de90fb" not in source


def test_learning_promotion_does_not_relax_runtime_oidc_binding_or_mutate_sql_directly():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "SUPABASE_USER_ACCESS_TOKEN" not in source
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
    # #2077 (WO3 admission gate): candidate status is now gate-determined via
    # admittedStatus (defaults to "CANDIDATE", may be "NOT_VERIFIED").
    assert 'status: admittedStatus' in source
    assert 'let admittedStatus = "CANDIDATE"' in source
    assert 'mode === "candidate"' in source


def test_learning_candidate_bridge_is_idempotent_and_does_not_promote():
    source = (ROOT / "supabase" / "functions" / "nayanet-learning-verify" / "index.ts").read_text(encoding="utf-8")
    assert 'created: false' in source
    assert 'eq("status", "CANDIDATE")' in source
    assert 'status: "ACTIVE"' in source


def test_learning_proof_consumes_same_head_fresh_commit_artifact_instead_of_fixed_block():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert 'workflows: ["Live Intelligence Commit Proof"]' in source
    assert "actions: read" in source
    assert "run-id: ${{ env.PRODUCER_RUN_ID }}" in source
    assert "github-token: ${{ secrets.GITHUB_TOKEN }}" in source
    assert 'open("fresh-lineage/fresh-lesson-lineage-ids.json")' in source
    assert 'fresh_block_id=ids["intelligent_block_id"]' in source
    assert '"checkpoint_id":ids["checkpoint_id"]' in source
    assert 'open("fresh-block-id.txt","w").write(fresh_block_id)' in source


def test_reused_candidate_rebinds_top_level_source_event_to_fresh_event():
    source = (ROOT / "supabase" / "functions" / "nayanet-learning-verify" / "index.ts").read_text(encoding="utf-8")
    # A reused same-claim CANDIDATE must not mix an old top-level event with
    # fresh embedded Event → Block → Lineage provenance.
    assert 'update({ source_event_id: event.id, observed_value: repairedObserved })' in source


def test_governed_production_promotion_separates_authorization_from_authentication():
    deploy = (ROOT / ".github" / "workflows" / "governed-supabase-production-deploy.yml").read_text(encoding="utf-8")
    forbidden = "SUPABASE_" + "ACCESS_TOKEN"
    assert "inputs.confirm" in deploy
    assert "DEPLOY" in deploy
    assert forbidden not in deploy
    assert "supabase functions deploy" not in deploy
    assert "SUPABASE_NATIVE_GITHUB_INTEGRATION" in deploy
    assert "PRODUCTION_BRANCH: production" in deploy


def test_governed_production_promotion_requires_new_supabase_deployment_evidence():
    deploy = (ROOT / ".github" / "workflows" / "governed-supabase-production-deploy.yml").read_text(encoding="utf-8")
    assert "supabase-check-ids-before.json" in deploy
    assert "supabase-production-check.json" in deploy
    assert "No successful NEW Supabase GitHub Integration check appeared" in deploy
    assert "live-intelligence-commit-proof.yml" in deploy
    assert "live-supabase-runtime-proof.yml" in deploy
    assert "production-promotion-receipt.json" in deploy


def test_supabase_config_declares_governed_runtime_functions_for_native_integration():
    config = (ROOT / "supabase" / "config.toml").read_text(encoding="utf-8")
    expected = {
        "nayanet-cold-runtime-proof",
        "nayanet-intelligence-commit-runtime",
        "nayanet-causal-learning-experiment",
        "nayanet-causal-verify",
        "nayanet-learning-verify",
        "nayanet-law-runtime",
        "nayanet-act-runtime",
        "nayanet-know-runtime",
        "nayanet-prove-runtime",
        "nayanet-verified-ai-action",
    }
    declared = {
        line[len("[functions."):-1]
        for line in config.splitlines()
        if line.startswith("[functions.") and line.endswith("]")
    }
    assert declared == expected
    assert config.count("verify_jwt = false") == len(expected)


def test_runtime_proof_can_be_dispatched_with_exact_producer_context():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in source
    assert "source_sha:" in source
    assert "producer_run_id:" in source
    assert "github.event_name == 'workflow_run'" in source
    assert "SOURCE_SHA:" in source
    assert "PRODUCER_RUN_ID:" in source


def test_learning_promotion_makes_http_failures_observable_and_retries_one_fresh_oidc_token_on_403():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert 'promotion_status="learning-promotion.http-status"' in source
    assert 'promotion_headers="learning-promotion.headers"' in source
    assert 'promotion_attempts=0' in source
    assert 'curl -sS -X POST' in source
    assert '-D "$promotion_headers"' in source
    assert '-o "$promotion_body"' in source
    assert '-w "%{http_code}"' in source
    assert 'PROMOTION_FINAL_HTTP_STATUS=$status' in source
    assert 'PROMOTION_RESPONSE_BODY:' in source
    assert 'PROMOTION_403_RETRYING_WITH_FRESH_OIDC_TOKEN' in source
    assert 'token="$(mint_runtime_token)"' in source
    assert 'post_promotion "$token"' in source
    assert 'if [[ ! "$status" =~ ^2[0-9][0-9]$ ]]; then' in source
    assert 'exit 1' in source


def test_learning_promotion_no_longer_uses_opaque_fail_fast_curl():
    source = WORKFLOW.read_text(encoding="utf-8")
    start = source.index("  learning-promotion:")
    end = source.index("  independent-retained-learning-reread:", start)
    promotion = source[start:end]
    assert 'curl -fsS -X POST             -H "Authorization: Bearer $(cat "$RUNNER_TEMP/oidc.jwt")"' not in promotion
    assert 'learning-promotion.json >' not in promotion


def test_learning_promotion_retry_is_bounded_to_a_single_403_recovery_attempt():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert source.count('post_promotion "$(cat "$RUNNER_TEMP/oidc.jwt")"') == 1
    assert source.count('post_promotion "$token"') == 1
    assert source.count('if [ "$status" = "403" ]; then') == 1
    assert source.count('mint_runtime_token()') == 1


def test_learning_lock_in_law_binds_node_scope_to_the_persisted_learning_target():
    source = (ROOT / "supabase" / "functions" / "nayanet-learning-verify" / "index.ts").read_text(encoding="utf-8")
    assert 'const learningTargetId = String((learning as any).target_id || "").trim();' in source
    assert 'matches(scope.target, learningTargetId)' in source
    assert 'resolveLearningLockInLaw(admin, ownerId, intelligentBlockId, learningTargetId)' in source
    assert 'LEARNING_AUTHORITY_TARGET' not in source
