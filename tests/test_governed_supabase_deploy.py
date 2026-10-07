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
    assert "ACT_PROOF_WORKFLOW: live-verified-ai-action-proof.yml" in source
    assert "LEARNING_ACT_PROOF_WORKFLOW: live-act-proof.yml" in source
    assert "live-connect-proof.yml" in source
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
        "nayanet-causal-verify",
        "nayanet-learning-verify",
        "nayanet-law-runtime",
        "nayanet-act-runtime",
        "nayanet-know-runtime",
        "nayanet-prove-runtime",
        "nayanet-verified-ai-action",
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
    assert 'supabase/functions/nayanet-verified-ai-action/index.ts' in source
    assert '"attested_components":["nayanet-cold-runtime-proof","nayanet-verified-ai-action"]' in source
    assert '"parity_scope":"ATTESTED_COMPONENTS_ONLY"' in source
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
    assert 'gh workflow run "$PROOF_WORKFLOW" --repo "$GITHUB_REPOSITORY" --ref main -f source_sha="$GITHUB_SHA" -f producer_run_id="$producer_run_id"' in source
    assert 'gh run list --repo "$GITHUB_REPOSITORY" --workflow "$PROOF_WORKFLOW" --branch main --event workflow_dispatch' in source
    assert 'if [ "$proof_head" != "$GITHUB_SHA" ]; then' in source
    assert 'gh workflow run "$ACT_PROOF_WORKFLOW" --repo "$GITHUB_REPOSITORY" --ref main' in source
    assert 'gh run list --repo "$GITHUB_REPOSITORY" --workflow "$ACT_PROOF_WORKFLOW" --branch main --event workflow_dispatch' in source
    assert '"act_proof_conclusion":act_proof.get("conclusion")' in source
    assert 'gh workflow run "$LEARNING_ACT_PROOF_WORKFLOW" --repo "$GITHUB_REPOSITORY" --ref main -f expected_source_sha="$GITHUB_SHA"' in source
    assert 'gh run list --repo "$GITHUB_REPOSITORY" --workflow "$LEARNING_ACT_PROOF_WORKFLOW" --branch main --event workflow_dispatch' in source
    assert '"learning_act_proof_conclusion":learning_act_proof.get("conclusion")' in source
    assert 'if [ "$act_head" != "$GITHUB_SHA" ]; then' in source
    assert 'gh workflow run "$CONNECT_PROOF_WORKFLOW" --repo "$GITHUB_REPOSITORY" --ref main' in source
    assert 'gh run list --repo "$GITHUB_REPOSITORY" --workflow "$CONNECT_PROOF_WORKFLOW" --branch main --event workflow_dispatch' in source
    assert 'if [ "$connect_head" != "$GITHUB_SHA" ]; then' in source
    assert '"connect_proof_conclusion":connect_proof.get("conclusion")' in source
    assert '--event workflow_run' not in source


def test_runtime_proof_supports_explicit_exact_source_dispatch():
    proof = (ROOT / ".github" / "workflows" / "live-supabase-runtime-proof.yml").read_text(encoding="utf-8")
    assert "workflow_dispatch:" in proof
    assert "source_sha:" in proof
    assert "producer_run_id:" in proof
    assert "SOURCE_SHA:" in proof
    assert "PRODUCER_RUN_ID:" in proof
    assert "run-id: ${{ env.PRODUCER_RUN_ID }}" in proof
    assert "ref: ${{ env.SOURCE_SHA }}" in proof


def test_governed_promotion_polls_dispatched_runs_instead_of_blocking_on_gh_run_watch():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "gh run watch" not in source
    assert "gh run view" in source
    assert source.count("--jq .status") == 5
    assert source.count("--jq .conclusion") == 5
    assert '.status+":"+(.conclusion//"")' not in source


def test_manual_production_authorization_is_bound_to_exact_source_sha():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "source_sha:" in source
    assert 'description: "Exact 40-hex main SHA authorized by the Human Director"' in source
    assert "required: true" in source
    assert "AUTHORIZED_SOURCE_SHA" in source
    assert 'if [ "${#authorized_sha}" -ne 40 ]; then' in source
    assert 'case "$authorized_sha" in' in source
    assert '*[!0-9a-f]*|""' in source
    assert 'if [ "$authorized_sha" != "$GITHUB_SHA" ]; then' in source
    assert 'resolved_main="$(git rev-parse origin/main)"' in source
    assert 'if [ "$authorized_sha" != "$resolved_main" ]; then' in source
    assert "Re-authorize the exact current main SHA." in source


def test_sha_binding_happens_before_any_production_branch_mutation():
    source = WORKFLOW.read_text(encoding="utf-8")
    bind = source.index('authorized_sha="${{ inputs.source_sha }}"')
    build = source.index("- name: Build provenance-stamped production deployment commit")
    promote = source.index("- name: Promote provenance-stamped deployment commit to production branch")
    assert bind < build < promote


def test_durable_receipt_records_exact_human_authorized_source_sha():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert '"authorized_source_sha":' in source
    assert 'os.environ.get("AUTHORIZED_SOURCE_SHA")' in source
