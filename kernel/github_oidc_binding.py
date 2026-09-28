from dataclasses import dataclass

CANONICAL_ISSUER = "https://token.actions.githubusercontent.com"
CANONICAL_AUDIENCE = "nayanet-runtime"
CANONICAL_REPOSITORY = "SoulSchoolAcademy/NayaPOWER"
CANONICAL_WORKFLOW = ".github/workflows/live-supabase-runtime-proof.yml"
CANONICAL_REF = "refs/heads/main"
CANONICAL_NAYA_ID = "NAYA-NODE-0001"
CANONICAL_OWNER_ID = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f"

@dataclass(frozen=True)
class GitHubRuntimeAuthorization:
    authorized: bool
    reason: str
    naya_id: str | None = None
    owner_id: str | None = None

def authorize_github_runtime(claims: dict) -> GitHubRuntimeAuthorization:
    if claims.get("iss") != CANONICAL_ISSUER:
        return GitHubRuntimeAuthorization(False, "ISSUER_MISMATCH")
    if claims.get("aud") != CANONICAL_AUDIENCE:
        return GitHubRuntimeAuthorization(False, "AUDIENCE_MISMATCH")
    if claims.get("repository") != CANONICAL_REPOSITORY:
        return GitHubRuntimeAuthorization(False, "REPOSITORY_BINDING_MISMATCH")
    expected = f"{CANONICAL_REPOSITORY}/{CANONICAL_WORKFLOW}@{CANONICAL_REF}"
    if claims.get("workflow_ref") != expected:
        return GitHubRuntimeAuthorization(False, "WORKFLOW_BINDING_MISMATCH")
    if claims.get("ref") != CANONICAL_REF:
        return GitHubRuntimeAuthorization(False, "REF_BINDING_MISMATCH")
    return GitHubRuntimeAuthorization(True, "CANONICAL_GITHUB_RUNTIME", CANONICAL_NAYA_ID, CANONICAL_OWNER_ID)
