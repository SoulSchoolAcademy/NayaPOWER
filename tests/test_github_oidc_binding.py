from kernel.github_oidc_binding import authorize_github_runtime

def test_authorizes_only_the_canonical_naya_proof_workflow():
    claims = {
        "iss": "https://token.actions.githubusercontent.com",
        "aud": "nayanet-runtime",
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "workflow_ref": "SoulSchoolAcademy/NayaPOWER/.github/workflows/live-supabase-runtime-proof.yml@refs/heads/main",
        "ref": "refs/heads/main",
    }
    result = authorize_github_runtime(claims)
    assert result.authorized is True
    assert result.naya_id == "NAYA-NODE-0001"
    assert result.owner_id == "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f"

def test_rejects_a_different_workflow_as_not_naya_runtime():
    claims = {
        "iss": "https://token.actions.githubusercontent.com",
        "aud": "nayanet-runtime",
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "workflow_ref": "SoulSchoolAcademy/NayaPOWER/.github/workflows/other.yml@refs/heads/main",
        "ref": "refs/heads/main",
    }
    result = authorize_github_runtime(claims)
    assert result.authorized is False
    assert result.reason == "WORKFLOW_BINDING_MISMATCH"

def test_token_rotation_is_irrelevant_to_naya_identity():
    base = {
        "iss": "https://token.actions.githubusercontent.com", "aud": "nayanet-runtime",
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "workflow_ref": "SoulSchoolAcademy/NayaPOWER/.github/workflows/live-supabase-runtime-proof.yml@refs/heads/main",
        "ref": "refs/heads/main",
    }
    before = authorize_github_runtime({**base, "jti": "token-a"})
    after = authorize_github_runtime({**base, "jti": "token-b"})
    assert before.naya_id == after.naya_id == "NAYA-NODE-0001"
    assert before.owner_id == after.owner_id == "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f"
