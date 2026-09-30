from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FUNCTION = ROOT / "supabase" / "functions" / "nayanet-verified-ai-action" / "index.ts"
WORKFLOW = ROOT / ".github" / "workflows" / "live-verified-ai-action-proof.yml"


def test_runtime_identity_is_short_lived_github_oidc_only():
    source = FUNCTION.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "token.actions.githubusercontent.com" in source
    assert "nayanet-runtime" in source
    assert "ACTIONS_ID_TOKEN_REQUEST_URL" in workflow
    assert "SUPABASE_USER_ACCESS_TOKEN" not in workflow
    assert "SUPABASE_USER_ACCESS_TOKEN" not in source
    assert "SUPABASE_USER_REFRESH_TOKEN" not in workflow


def test_runtime_is_bound_to_the_governed_workflow_on_main():
    source = FUNCTION.read_text(encoding="utf-8")
    assert ".github/workflows/live-verified-ai-action-proof.yml" in source
    assert "refs/heads/main" in source
    assert "WORKFLOW_BINDING_MISMATCH" in source
    assert "SoulSchoolAcademy/NayaPOWER" in source


def test_authority_is_resolved_from_durable_grant_not_from_request_evidence():
    source = FUNCTION.read_text(encoding="utf-8")
    assert "nayanet_authority_grants" in source
    assert 'grant.status === "ACTIVE"' in source
    assert "NAYA-NODE-0001-CONTINUITY" in source
    assert 'actions.includes(ACTION)' in source
    assert "grant.revoked_at" in source
    assert "grant.expires_at" in source


def test_independent_verification_rereads_authority_from_the_grants_table():
    source = FUNCTION.read_text(encoding="utf-8")
    verify = source.split('if (mode === "verify")')[1]
    assert "nayanet_authority_grants" in source
    assert "resolveAuthority(" in verify
    assert "grantIdPresented" in verify
    # The verifier must never decide authority from executor-writable evidence.
    assert "evidence.authority_status" not in verify


def test_independent_verification_is_owner_scoped():
    source = FUNCTION.read_text(encoding="utf-8")
    verifier = source.split('if (mode === "verify")')[1]
    assert 'from("nayanet_execution_receipts")' in verifier
    assert 'from("nayanet_execution_outcomes")' in verifier
    assert '.eq("id", id)' in verifier
    assert '.eq("user_id", OWNER_ID)' in verifier
    assert '.eq("project_id", "NayaNET")' in verifier


def test_executor_cannot_self_certify_its_own_outcome():
    source = FUNCTION.read_text(encoding="utf-8")
    assert "verified: false" in source
    execute = source.split('mode === "execute"')[1].split('mode === "verify"')[0]
    assert "verified: true" not in execute
    verify = source.split('mode === "verify"')[1]
    assert "verified: true" in verify
    assert "INDEPENDENT_RUNTIME" in verify


def test_observed_result_is_derived_from_canonical_block_not_asserted():
    source = FUNCTION.read_text(encoding="utf-8")
    assert "nayanet_intelligent_blocks" in source
    assert "IB-NAYA-NODE-0001-0001" in source
    assert "SHA-256" in source
    assert "canonical_digest" in source
    assert "canonicalDigest(" in source
    verify = source.split('if (mode === "verify")')[1]
    assert "expectedDigest" in verify


def test_idempotent_replay_requires_persisted_outcome():
    source = FUNCTION.read_text(encoding="utf-8")
    replay = source.split("if (idempotentReplay)", 1)[1].split("const {data: outcome", 1)[0]
    assert "if (!replayOutcome)" in replay
    assert "recoverOutcomeFromReceipt" in replay
    assert "IDEMPOTENT_REPLAY_OUTCOME_RECOVERED" in replay
    assert "PENDING_INDEPENDENT_RUNTIME_VERIFICATION" in replay


def test_consequential_action_requires_idempotency_key():
    source = FUNCTION.read_text(encoding="utf-8")
    execute = source.split('if (mode === "execute")', 1)[1].split('if (mode === "verify")', 1)[0]
    assert 'if (!idempotencyKey)' in execute
    assert '"IDEMPOTENCY_KEY_REQUIRED"' in execute


def test_refusal_persists_receipt_and_creates_no_outcome():
    source = FUNCTION.read_text(encoding="utf-8")
    refusal = source.split("if (!authorityDecision.allowed)")[1].split("const grant = authorityDecision.grant")[0]
    assert '"BLOCKED"' in refusal
    assert "NAYA-NODE-0001-VERIFIED-AI-ACTION-REFUSAL" in refusal
    assert "nayanet_execution_outcomes" not in refusal
    assert "AUTHORITY_ABSENT" in refusal


def test_verifier_proves_refusal_had_no_outcome_and_no_mutation():
    source = FUNCTION.read_text(encoding="utf-8")
    assert "refusal_outcome_absent" in source
    assert "unauthorized_outcome_exists" in source
    assert "refusal_receipt_present" in source
    assert "receipt_mutated_after_refusal" in source


def test_workflow_uses_three_separate_fresh_runtimes():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert workflow.count("ACTIONS_ID_TOKEN_REQUEST_URL") >= 3
    for job in ("authorized-action:", "authority-absent-refusal:", "independent-verification:"):
        assert job in workflow
    assert "id-token: write" in workflow
    assert "contents: read" in workflow


def test_concurrent_duplicate_requests_have_an_atomic_idempotency_claim():
    source = FUNCTION.read_text(encoding="utf-8")
    migration_dir = ROOT / "supabase" / "migrations"
    migrations = "\n".join(p.read_text(encoding="utf-8") for p in migration_dir.glob("*.sql"))
    assert "idempotency_key" in source
    assert "idempotency_key" in migrations
    assert "unique" in migrations.lower()
    assert "nayanet_execution_receipts" in migrations
    assert "23505" in source
    assert "IDEMPOTENCY_KEY_REUSE_CONFLICT" in source
    assert "IDEMPOTENT_REPLAY_OUTCOME_RECOVERED" in source
    # The idempotency key must be persisted at the receipt boundary, not only encoded in prose.
    assert "idempotency_key: idempotencyKey" in source
    # A concurrent loser must resolve the already-claimed receipt rather than execute again.
    execute = source.split('if (mode === "execute")', 1)[1].split('if (mode === "verify")', 1)[0]
    assert "idempotentReplay" in execute
    assert "IDEMPOTENT_REPLAY_OUTCOME_MISSING" in execute


def test_idempotency_key_is_bound_to_exact_request_context():
    source = FUNCTION.read_text(encoding="utf-8")
    execute = source.split('if (mode === "execute")', 1)[1].split('if (mode === "verify")', 1)[0]
    assert "idempotency_request_fingerprint" in execute
    assert "IDEMPOTENCY_KEY_REUSE_CONFLICT" in execute
    assert 'status: "BLOCKED"' in execute
    assert "idempotentReplay" in execute
    # A reused key must be compared with the persisted original request context before replay.
    assert "persistedFingerprint" in execute
    assert "requestFingerprint" in execute


def test_idempotent_replay_recovers_missing_outcome_from_bound_receipt():
    source = FUNCTION.read_text(encoding="utf-8")
    execute = source.split('if (mode === "execute")', 1)[1].split('if (mode === "verify")', 1)[0]
    assert "recoverOutcomeFromReceipt" in execute
    assert "IDEMPOTENT_REPLAY_OUTCOME_RECOVERED" in execute
    assert "idempotency_request_fingerprint" in execute
    assert "PENDING_INDEPENDENT_RUNTIME_VERIFICATION" in execute
    # Recovery must use the existing canonical outcome table, not invent a second recovery ledger.
    assert execute.count('from("nayanet_execution_outcomes")') >= 2


def test_no_service_role_or_owner_bypass_is_exposed_to_the_runtime():
    source = FUNCTION.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "SUPABASE_SERVICE_ROLE_KEY" not in workflow
    assert "SUPABASE_SERVICE_ROLE_KEY" in source
    assert "SUPABASE_ACCESS_TOKEN" not in workflow