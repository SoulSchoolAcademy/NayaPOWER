from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOUND = ROOT / "supabase/functions/nayanet-compound-intelligence/index.ts"
MIGRATION = ROOT / "supabase/migrations/20260925000000_enforce_independent_outcome_learning_promotion_v1.sql"
RUNTIME = ROOT / "NAYANET/HUB/public/assistant-runtime.js"
WORKFLOW = ROOT / ".github/workflows/verify-nayanet-compound-intelligence-12.yml"


def test_learning_verify_binds_promotion_to_independent_outcome():
    source = COMPOUND.read_text(encoding="utf-8")
    for marker in (
        'INDEPENDENT_OUTCOME_ID_REQUIRED',
        'nayanet_execution_outcomes',
        'OUTCOME_VERIFIER_MUST_BE_INDEPENDENT',
        'INDEPENDENT_OUTCOME_EVIDENCE_REQUIRED',
        'OUTCOME_RECEIPT_LINEAGE_MISMATCH',
        'LEARNING_ALREADY_PROMOTED_WITH_DIFFERENT_OUTCOME',
        'independent_outcome: true',
        '.eq("status", "CANDIDATE")',
    ):
        assert marker in source
    assert 'const observed = body.observed_value ?? evidence.observed_value;' not in source


def test_database_trigger_blocks_truthy_active_learning_without_outcome():
    source = MIGRATION.read_text(encoding="utf-8")
    for marker in (
        'INDEPENDENT_OUTCOME_REQUIRED_FOR_ACTIVE_LEARNING',
        'INDEPENDENT_OUTCOME_NOT_FOUND_OR_UNVERIFIED',
        'OUTCOME_VERIFIER_MUST_BE_INDEPENDENT',
        'INDEPENDENT_OUTCOME_RECEIPT_REQUIRED',
        'INDEPENDENT_OUTCOME_RECEIPT_MISMATCH',
        'nayanet_independent_outcome_learning_promotion',
        'before insert or update on public.learning_evidence',
    ):
        assert marker in source


def test_browser_learning_writer_stays_candidate_until_outcome_verified():
    source = RUNTIME.read_text(encoding="utf-8")
    assert "status:'CANDIDATE'" in source
    assert "status:'ACTIVE'" not in source


def test_compound_proof_distinguishes_deployment_parity_from_fail_closed_promotion():
    source = WORKFLOW.read_text(encoding="utf-8")
    for marker in (
        "INDEPENDENT_OUTCOME_ID_REQUIRED",
        "DEPLOYED_RUNTIME_PREDATES_INDEPENDENT_OUTCOME_BOUNDARY",
        "legacy_unbounded_promotion:true",
        "status:'BLOCKED'",
    ):
        assert marker in source
