"""Contract: the learning-influence live proof must use a short-lived Naya runtime
identity, never a human session.

Coder 2, 2026-09-28 — REPAIRED, and the repair deliberately does NOT weaken it.

WHAT WAS WRONG
The previous version asserted the literal string
`nayanet-cold-runtime-proof?mode=learning-influence` appears in the workflow.
It does not, and never did not-dangerously: the workflow defines

    RUNTIME_FUNCTION: https://<project>.supabase.co/functions/v1/nayanet-cold-runtime-proof

and then invokes

    "${RUNTIME_FUNCTION}?mode=learning-influence"

That composes to exactly the canonical endpoint. The runtime behaviour was
correct the whole time; only the string-matching assertion was brittle, and it
broke on an unrelated refactor that hoisted the URL into a variable. Main was
RED for that reason.

Fixing this by editing the workflow to inline the URL would have made a test
pass by changing the artifact under test. That is backwards, and it would also
have destroyed the readability of the workflow.

So the assertion now checks the SEMANTIC property instead: it resolves the
endpoint the workflow itself defines, and proves that the composed request targets
the canonical function in learning-influence mode, authenticated by a
short-lived OIDC token, with no human or publishable credential anywhere.

The security assertions are preserved verbatim and one was ADDED.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "live-learning-influence-proof.yml"

CANONICAL_FUNCTION = "nayanet-cold-runtime-proof"


def _source() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def _resolved_function() -> str:
    """Resolve the function URL the workflow actually calls, however it is written."""
    source = _source()
    env = re.search(r"RUNTIME_FUNCTION:\s*(\S+)", source)
    assert env, "workflow no longer defines RUNTIME_FUNCTION; the endpoint contract must be updated deliberately"
    url = env.group(1)
    assert url.startswith("https://"), f"RUNTIME_FUNCTION must be an https endpoint, got {url!r}"
    return url


def test_learning_influence_runtime_uses_short_lived_naya_identity_not_human_session():
    source = _source()
    assert "id-token: write" in source
    assert "ACTIONS_ID_TOKEN_REQUEST_URL" in source
    assert "audience=nayanet-runtime" in source
    assert "SUPABASE_USER_ACCESS_TOKEN" not in source
    assert "SUPABASE_USER_REFRESH_TOKEN" not in source
    assert "SUPABASE_PUBLISHABLE_KEY" not in source

    # The semantic replacement for the old literal-string assertion: the composed
    # request must target the canonical runtime in learning-influence mode.
    url = _resolved_function()
    assert url.rstrip("/").endswith(f"/functions/v1/{CANONICAL_FUNCTION}"), (
        f"learning-influence proof must target the canonical runtime {CANONICAL_FUNCTION}, got {url!r}"
    )
    assert f'${{RUNTIME_FUNCTION}}?mode=learning-influence' in source, (
        "the workflow must invoke the canonical runtime in learning-influence mode"
    )

    # ADDED: the request must be authenticated by the minted short-lived OIDC
    # token, not by any other bearer value.
    assert '"Authorization: Bearer $(cat "$RUNNER_TEMP/oidc.jwt")"' in source, (
        "the runtime call must authenticate with the short-lived OIDC token, not a human session"
    )


def test_learning_influence_keeps_independent_verification_on_fresh_runtime():
    source = _source()
    assert "independent-verification" in source
    assert "executor_claim_trusted" in source
    assert "independent_verification" in source
