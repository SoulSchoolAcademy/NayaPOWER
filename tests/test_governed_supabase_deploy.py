from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "governed-supabase-production-deploy.yml"
CONFIG = ROOT / "supabase" / "config.toml"


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


def test_governed_promotion_serializes_authority_bearing_production_writes():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "concurrency:" in source
    assert "group: nayapower-governed-production-promotion" in source
    assert "cancel-in-progress: false" in source


def test_governed_promotion_refuses_moved_authorized_source_before_producer_dispatch():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert 'git fetch origin main' in source
    assert 'current_main="$(git rev-parse origin/main)"' in source
    assert 'if [ "$current_main" != "$GITHUB_SHA" ]; then' in source
    assert "AUTHORIZED_SOURCE_MOVED" in source


def test_governed_promotion_refuses_moved_production_deployment_before_producer_dispatch():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert 'current_production="$(gh api "repos/$GITHUB_REPOSITORY/git/ref/heads/$PRODUCTION_BRANCH" --jq .object.sha)"' in source
    assert 'if [ "$current_production" != "$DEPLOYMENT_SHA" ]; then' in source
    assert "PRODUCTION_DEPLOYMENT_MOVED" in source
