from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "supabase/functions/nayanet-project-intelligence-bridge/index.ts"
MIGRATION = ROOT / "supabase/migrations/20260925040000_bind_bridge_owner_to_oidc_workflow_v1.sql"
BUILDER = ROOT / ".naya/runtime/project_intelligence_bridge.py"
WORKFLOW = ROOT / ".github/workflows/verify-project-intelligence-bridge.yml"


def test_bridge_requires_verified_workflow_claims():
    source = BRIDGE.read_text(encoding="utf-8")
    for marker in (
        "repository_owner!==REPOSITORY_OWNER",
        "OIDC_ACTOR_REQUIRED",
        "OIDC_SOURCE_SHA_REQUIRED",
        "OIDC_SUBJECT_NOT_AUTHORIZED",
        "WORKFLOW_REF_NOT_AUTHORIZED",
        "JOB_WORKFLOW_REF_NOT_AUTHORIZED",
        "WORKFLOW_NOT_ALLOWLISTED",
        "OIDC_WORKFLOW_CONTEXT_REQUIRED",
        "SOURCE_SHA_NOT_AUTHORIZED",
        "RUN_IDENTITY_NOT_AUTHORIZED",
        "OWNER_BINDING_REQUIRED",
        "OWNER_BINDING_INVALID",
        "nayanet_consume_bridge_owner_binding",
        "source_identity",
    ):
        assert marker in source
    assert source.index("OWNER_BINDING_REQUIRED") < source.index("getUserById")


def test_owner_binding_is_short_lived_workflow_scoped_and_service_role_consumed():
    source = MIGRATION.read_text(encoding="utf-8")
    for marker in (
        "nayanet_project_intelligence_bridge_owner_bindings",
        "nayanet_issue_bridge_owner_binding",
        "nayanet_consume_bridge_owner_binding",
        "BRIDGE_BINDING_EXPIRY_INVALID",
        "auth.role() <> 'service_role'",
        "OWNER_BINDING_INVALID_OR_EXPIRED",
        "revoke all on table public.nayanet_project_intelligence_bridge_owner_bindings from anon, authenticated",
        "grant execute on function public.nayanet_consume_bridge_owner_binding",
    ):
        assert marker in source


def test_sender_passes_binding_out_of_band_and_owner_token_is_masked():
    builder = BUILDER.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "nayanet_issue_bridge_owner_binding" in builder
    assert "X-Naya-Owner-Binding" in builder
    assert "NAYANET_OWNER_ACCESS_TOKEN" in builder
    assert "::add-mask::$owner_access_token" in workflow
    assert "NAYANET_OWNER_ACCESS_TOKEN" in workflow
