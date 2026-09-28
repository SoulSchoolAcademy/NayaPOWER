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
    assert "comparison_receipt_id" in source
    assert "NAYA-NODE-0001-TREATMENT" in source
    assert "NAYA-NODE-0001-BASELINE" in source
    assert "retained_intelligence_used !== true" in source
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
