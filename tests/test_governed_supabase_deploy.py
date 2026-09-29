from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "governed-supabase-production-deploy.yml"
CONFIG = ROOT / "supabase" / "config.toml"\nRUNTIME_PROOF = ROOT / ".github" / "workflows" / "live-supabase-runtime-proof.yml"


def test_governed_promotion_keeps_manual_human_gate_and_canonical_proof():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "inputs.confirm" in source
    assert "DEPLOY" in source
    assert "PRODUCTION_BRANCH: production" in source
    assert "live-intelligence-commit-proof.yml" in source
    assert "live-supabase-runtime-proof.yml" in source
    assert "production-promotion-receipt.json" in source


def test_governed_promotion_uses_native_integration_instead_of_cli_deploy():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "supabase functions deploy" not in source
    assert "SUPABASE_NATIVE_GITHUB_INTEGRATION" in source
    assert "supabase-production-check.json" in source


def test_governed_promotion_preserves_existing_runtime_set_in_source_config():
    source = CONFIG.read_text(encoding="utf-8")
    for function_name in (
        "nayanet-cold-runtime-proof",
        "nayanet-intelligence-commit-runtime",
        "nayanet-causal-learning-experiment",
        "nayanet-learning-verify",
    ):
        assert f"[functions.{function_name}]" in source


def test_native_production_deployment_is_provenance_stamped_before_supabase_deploys():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert 'const DEPLOYED_SOURCE_REVISION = "UNSTAMPED";' in source
    assert "deployment-sha.txt" in source
    assert "DEPLOYMENT_SHA=" in source
    assert 'commits/$DEPLOYMENT_SHA/check-runs' in source
    assert '"deployment_commit_sha":os.environ["DEPLOYMENT_SHA"]' in source
    assert '"deployed_source_revision":os.environ["GITHUB_SHA"]' in source
    assert 'json.dump({"content":base64.b64encode(payload).decode("ascii"),"encoding":"base64"}, sys.stdout)' in source
    assert 'open("deployment-blob-request.json","w")' not in source


def test_governed_promotion_serializes_authority_bearing_execution():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "concurrency:" in source
    assert "group: governed-production-promotion" in source
    assert "cancel-in-progress: false" in source


def test_governed_promotion_revalidates_authorized_source_and_deployment_before_producer():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "Revalidate authorized source and deployment ownership before producer" in source
    assert 'test "$(git rev-parse origin/main)" = "$GITHUB_SHA"' in source
    assert 'test "$production_now" = "$DEPLOYMENT_SHA"' in source
    assert 'if [ "$producer_head" != "$GITHUB_SHA" ]; then' in source
    assert 'gh run cancel "$run_id"' in source
    assert "main moved after producer dispatch; refusing to continue." in source


def test_governed_promotion_dispatches_runtime_proof_directly():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert 'gh workflow run "$PROOF_WORKFLOW" --repo "$GITHUB_REPOSITORY" --ref main' in source
    assert 'gh run list --repo "$GITHUB_REPOSITORY" --workflow "$PROOF_WORKFLOW" --branch main --event workflow_dispatch' in source
    assert 'if [ "$proof_head" != "$GITHUB_SHA" ]; then' in source
    assert '--event workflow_run' not in source


def test_runtime_proof_keeps_workflow_run_and_adds_manual_dispatch_trigger():
    source = RUNTIME_PROOF.read_text(encoding="utf-8")
    assert "workflow_run:" in source
    assert "workflow_dispatch:" in source
