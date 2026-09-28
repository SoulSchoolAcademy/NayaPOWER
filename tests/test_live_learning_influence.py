from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "live-learning-influence-proof.yml"


def test_learning_influence_runtime_uses_short_lived_naya_identity_not_human_session():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "id-token: write" in source
    assert "ACTIONS_ID_TOKEN_REQUEST_URL" in source
    assert "audience=nayanet-runtime" in source
    # The endpoint is composed from a shell variable, so assert the semantics
    # rather than one contiguous literal. Requiring the literal previously made
    # this contract test fail purely because the URL was correctly extracted
    # into RUNTIME_FUNCTION. The rule is unchanged: the cold runtime proof must
    # be invoked in learning-influence mode, over short-lived OIDC identity.
    assert "nayanet-cold-runtime-proof" in source
    assert "mode=learning-influence" in source
    assert "SUPABASE_USER_ACCESS_TOKEN" not in source
    assert "SUPABASE_USER_REFRESH_TOKEN" not in source
    assert "SUPABASE_PUBLISHABLE_KEY" not in source


def test_learning_influence_keeps_independent_verification_on_fresh_runtime():
    source = WORKFLOW.read_text(encoding="utf-8")
    assert "independent-verification" in source
    assert "executor_claim_trusted" in source
    assert "independent_verification" in source
