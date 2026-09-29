from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "governed-supabase-production-deploy.yml"


def test_governed_deploy_includes_learning_verifier_under_manual_gate():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert 'description: "Type DEPLOY to authorize a production Edge Function deployment"' in source
    assert 'test "${{ inputs.confirm }}" = "DEPLOY"' in source
    assert '"nayanet-learning-verify"' in source
    assert 'gh workflow run "$PROOF_WORKFLOW"' in source


def test_governed_deploy_preserves_existing_runtime_set_in_broker_request():
    source = WORKFLOW.read_text(encoding="utf-8")
    for function_name in (
        "nayanet-cold-runtime-proof",
        "nayanet-intelligence-commit-runtime",
        "nayanet-causal-learning-experiment",
        "nayanet-learning-verify",
    ):
        assert f'"{function_name}"' in source


def test_governed_deploy_uses_oidc_broker_not_recurring_human_supabase_token():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "id-token: write" in source
    assert "ACTIONS_ID_TOKEN_REQUEST_TOKEN" in source
    assert "audience=nayanet-production-deploy" in source
    assert "NAYANET_DEPLOYMENT_BROKER_URL" in source
    assert "SUPABASE_ACCESS_TOKEN" not in source
    assert "SUPABASE_USER_ACCESS_TOKEN" not in source
    assert "supabase functions deploy" not in source


def test_deployment_authorization_is_distinct_from_machine_authentication():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert 'test "${{ inputs.confirm }}" = "DEPLOY"' in source
    assert '"human_authorization":"DEPLOY"' in source
    assert '"source_revision":os.environ["GITHUB_SHA"]' in source
    assert '"functions":[' in source
    assert 'response.get("runtime_identity") == "github-actions-oidc"' in source
