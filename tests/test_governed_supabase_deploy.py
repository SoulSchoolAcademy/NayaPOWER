from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "governed-supabase-production-deploy.yml"


def test_governed_deploy_includes_learning_verifier_under_manual_gate():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert 'description: "Type DEPLOY to authorize a production Edge Function deployment"' in source
    assert 'test "${{ inputs.confirm }}" = "DEPLOY"' in source
    assert "supabase functions deploy nayanet-learning-verify --use-api" in source
    assert 'gh workflow run "$PROOF_WORKFLOW"' in source


def test_governed_deploy_preserves_existing_runtime_set():
    source = WORKFLOW.read_text(encoding="utf-8")
    for function_name in (
        "nayanet-cold-runtime-proof",
        "nayanet-intelligence-commit-runtime",
        "nayanet-causal-learning-experiment",
        "nayanet-learning-verify",
    ):
        assert f"supabase functions deploy {function_name} --use-api" in source
