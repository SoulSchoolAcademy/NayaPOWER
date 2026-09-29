from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FUNCTION = ROOT / "supabase" / "functions" / "nayanet-causal-verify" / "index.ts"
WORKFLOW = ROOT / ".github" / "workflows" / "live-cvo-runtime-proof.yml"


def test_cvo_runtime_requires_oidc_and_not_human_supabase_token():
    source = FUNCTION.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "token.actions.githubusercontent.com" in source
    assert "ACTIONS_ID_TOKEN_REQUEST_URL" in workflow
    assert "SUPABASE_USER_ACCESS_TOKEN" not in workflow
    assert "SUPABASE_USER_ACCESS_TOKEN" not in source
    assert "NAYA-NODE-0001-CONTINUITY" in source


def test_cvo_runtime_derives_action_and_outcome_from_persisted_receipts():
    source = FUNCTION.read_text(encoding="utf-8")
    assert "nayanet_execution_receipts" in source
    assert "nayanet_execution_outcomes" in source
    assert "NAYA-NODE-0001-COLD-BEHAVIOR" in source
    assert "TREATMENT_OUTCOME_EVIDENCE_INVALID" in source
    assert "causal.evidence?.treatment?.evidence?.provenance_present" in source
    assert "comparison_receipt_id" in source
    assert "NAYA-NODE-0001-TREATMENT" in source
    assert "NAYA-NODE-0001-BASELINE" in source
    assert "CONTROLLED_INTERVENTION" in source
    assert "NAYANET_CAUSAL_VERIFICATION_V1" in source
    assert "nayanet_intelligence_operations" not in source
    assert "nayanet_execution_receipts" in source


def test_cvo_runtime_persists_and_re_reads_verification():
    source = FUNCTION.read_text(encoding="utf-8")
    assert "causal_verification" in source
    assert "OUTCOME_VERIFIED" in source
    assert "independent_verification" in source
    assert "production_action_executed" in source


def test_cvo_runtime_has_bounded_independent_outcome_recovery():
    source = FUNCTION.read_text(encoding="utf-8")
    assert 'mode === "recover-learning-outcomes"' in source
    assert "LEARNING_OUTCOME_RECOVERY_PAIR_INVALID" in source
    assert "LEARNING_OUTCOME_RECOVERY_PARTIAL_STATE" in source
    assert "INDEPENDENT_RUNTIME_RECOMPUTATION_FROM_PERSISTED_CAUSAL_RECEIPTS" in source
    assert 'String(control.action).startsWith("NAYA-NODE-0001-CONTROL-")' in source
    assert 'String(treatment.action).startsWith("NAYA-NODE-0001-TREATMENT-")' in source
    assert 'taskId !== "NAYA-0001-PROVENANCE-HELDOUT-001"' in source
    assert 'controlEvidence.outcome?.provenance_preserved === false' in source
    assert 'treatmentEvidence.outcome?.provenance_preserved === true' in source
    assert '.from("nayanet_execution_outcomes").insert(rows)' in source
    assert '"CREATED_AND_REREAD"' in source
    assert '"REPLAYED_AND_REREAD"' in source


def test_outcome_recovery_cannot_create_authority_or_trust_executor_claim():
    source = FUNCTION.read_text(encoding="utf-8")
    recovery = source[source.index('if (mode === "recover-learning-outcomes")'):source.index('const {data:treatmentOutcome', source.index('if (mode === "recover-learning-outcomes")'))]
    assert "nayanet_issue_authority_grant" not in recovery
    assert "executor_claim_trusted:false" in recovery
    assert "verified: true" in recovery
    assert "verifier_token_jti" in recovery


def test_historical_outcome_recovery_is_manual_and_bounded_to_audited_pair():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "recover_historical_outcomes" in workflow
    assert "historical-outcome-recovery:" in workflow
    assert "github.event_name == 'workflow_dispatch'" in workflow
    assert '"mode":"recover-learning-outcomes"' in workflow
    assert "5b072812-699f-415d-b759-2ed509c36367" in workflow
    assert "109944fc-9868-45e3-a532-f40952aea3a1" in workflow
    assert "NAYANET_CAUSAL_OUTCOME_RECOVERY_V1" in workflow
    assert "executor_claim_trusted" in workflow
