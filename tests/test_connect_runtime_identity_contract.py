from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
WORKFLOW = REPO / ".github" / "workflows" / "live-supabase-runtime-proof.yml"
FUNCTION = REPO / "supabase" / "functions" / "nayanet-cold-runtime-proof" / "index.ts"


def test_live_connect_runtime_uses_oidc_not_human_supabase_token():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "id-token: write" in workflow
    assert "SUPABASE_USER_ACCESS_TOKEN" not in workflow
    assert "ACTIONS_ID_TOKEN_REQUEST_URL" in workflow
    assert "${COLD_RUNTIME_FUNCTION}?mode=connect" in workflow


def test_connect_runtime_resolves_durable_owner_binding_server_side():
    source = FUNCTION.read_text(encoding="utf-8")
    assert 'payload.repository !== REPOSITORY' in source
    assert 'const WORKFLOWS = new Set([' in source
    assert '".github/workflows/live-supabase-runtime-proof.yml"' in source
    assert '".github/workflows/live-learn-proof.yml"' in source
    assert 'const workflowRefMismatch = !expectedRefs.includes(workflowRef)' in source
    assert 'mode === "connect"' in source
    assert "nayanet_brain_relationships" in source
    assert "nayanet_authority_grants" in source
    assert "owner_id=eq." in source
    assert "SUPABASE_USER_ACCESS_TOKEN" not in source


def test_connect_runtime_keeps_consequential_actions_fail_closed_without_authority():
    source = FUNCTION.read_text(encoding="utf-8")
    assert 'blocked_by: "LAW"' in source
    assert 'executed: false' in source
    assert 'consequential: true' in source
