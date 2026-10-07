from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACT_PROOF = ROOT / ".github" / "workflows" / "live-act-proof.yml"
DEPLOY = ROOT / ".github" / "workflows" / "governed-supabase-production-deploy.yml"
KNOW = ROOT / "supabase" / "functions" / "nayanet-know-runtime" / "index.ts"


def test_live_act_proof_exercises_two_phase_know_bound_path():
    source = ACT_PROOF.read_text(encoding="utf-8")
    assert "KNOW_RUNTIME:" in source
    assert '"mode":"retrieve"' in source
    assert '"mode":"plan"' in source
    assert '"retrieval_receipt_id":"$know_id"' in source
    assert 'printf \'{"mode":"execute","plan_receipt_id":"%s"}\'' in source
    assert '"mode":"inspect-plan"' in source
    assert 'TWO_PHASE_KNOW_CONNECT_BOUND' in source
    assert 'APPLY_BASELINE_WITHOUT_RETAINED_STEERING' in source
    assert 'PRESERVE_PROVENANCE_BEFORE_APPLY' in source
    assert 'executor_claim_trusted_as_verification' in source
    assert 'retrieval_creates_authority' in source


def test_live_act_proof_fails_closed_for_exact_source_parity_mismatch():
    source = ACT_PROOF.read_text(encoding="utf-8")
    assert "expected_source_sha:" in source
    assert "BLOCKED_BY_PRODUCTION_SOURCE" in source
    assert "BLOCKED_BY_RUNTIME_BLOB_MISMATCH" in source
    assert 'if [ -n "$expected" ]; then' in source
    assert "Exact-source ACT proof requested but production parity is not eligible" in source
    for path in (
        "supabase/functions/nayanet-law-runtime/index.ts",
        "supabase/functions/nayanet-act-runtime/index.ts",
        "supabase/functions/nayanet-act-runtime/act.ts",
        "supabase/functions/nayanet-know-runtime/index.ts",
        "supabase/functions/nayanet-know-runtime/know.ts",
        "supabase/functions/_shared/connect_selector.ts",
    ):
        assert path in source


def test_governed_promotion_preserves_verified_action_and_adds_registry_designated_act_proof():
    source = DEPLOY.read_text(encoding="utf-8")
    assert "ACT_PROOF_WORKFLOW: live-verified-ai-action-proof.yml" in source
    assert "LEARNING_ACT_PROOF_WORKFLOW: live-act-proof.yml" in source
    assert 'gh workflow run "$ACT_PROOF_WORKFLOW" --repo "$GITHUB_REPOSITORY" --ref main' in source
    assert 'gh workflow run "$LEARNING_ACT_PROOF_WORKFLOW" --repo "$GITHUB_REPOSITORY" --ref main -f expected_source_sha="$GITHUB_SHA"' in source
    assert '"act_proof_conclusion":act_proof.get("conclusion")' in source
    assert '"learning_act_proof_conclusion":learning_act_proof.get("conclusion")' in source


def test_know_runtime_allows_only_named_canonical_act_proof_identity():
    source = KNOW.read_text(encoding="utf-8")
    assert '".github/workflows/live-act-proof.yml"' in source
    assert 'expectedRefs.includes(workflowRef)' in source
    assert 'WORKFLOW_BINDING_MISMATCH' in source
