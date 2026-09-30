"""Contract: the learning-influence live proof must use a short-lived Naya runtime
identity, never a human session.

PROVENANCE OF THIS FILE - read before "fixing" it
--------------------------------------------------
This assertion was brittle: it required the literal string
`nayanet-cold-runtime-proof?mode=learning-influence` to appear in the workflow.
It does not, because the workflow correctly hoists the URL into
RUNTIME_FUNCTION and composes `"${RUNTIME_FUNCTION}?mode=learning-influence"`.
The runtime behaviour was correct throughout; only the string match was wrong,
and it broke on an unrelated refactor, leaving `main` RED.

**Two coders fixed this independently and concurrently.** The version now on
`main` asserts the endpoint by checking the canonical function name and the mode
separately - simple and robust to refactors. That fix is the base here.

Kept from my version, because each adds something the main version does not:
  * RUNTIME_FUNCTION is resolved and validated: it must be an https URL that
    actually ends in /functions/v1/<canonical function>. Checking the string
    "nayanet-cold-runtime-proof" appears somewhere in the file does not prove the
    workflow CALLS it.
  * the runtime call must authenticate with the minted short-lived OIDC token,
    not merely avoid three named credentials.

Dropped from my version: the literal `"${RUNTIME_FUNCTION}?mode=learning-influence"`
check. It was brittle in exactly the way the original assertion was - it couples
the test to a variable name - and the two assertions above already cover it.
Being cleverer than the shared fix here was not worth the fragility.

No security assertion was weakened. Two were strengthened.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "live-supabase-runtime-proof.yml"

CANONICAL_FUNCTION = "nayanet-cold-runtime-proof"


def _source() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def _resolved_function() -> str:
    """Resolve the function URL the workflow actually calls, however it is written."""
    source = _source()
    env = re.search(r"RUNTIME_FUNCTION:\s*(\S+)", source)
    assert env, (
        "workflow no longer defines RUNTIME_FUNCTION; the endpoint contract must be updated deliberately"
    )
    url = env.group(1)
    assert url.startswith("https://"), f"RUNTIME_FUNCTION must be an https endpoint, got {url!r}"
    return url


def test_learning_influence_runtime_uses_short_lived_naya_identity_not_human_session():
    source = _source()
    assert "id-token: write" in source
    assert "ACTIONS_ID_TOKEN_REQUEST_URL" in source
    assert "audience=nayanet-runtime" in source

    # From main: the endpoint is composed from a shell variable, so assert the
    # semantics rather than one contiguous literal. The rule is unchanged: the
    # cold runtime proof must be invoked in learning-influence mode, over
    # short-lived OIDC identity.
    assert CANONICAL_FUNCTION in source
    assert "mode=learning-influence" in source

    assert "SUPABASE_USER_ACCESS_TOKEN" not in source
    assert "SUPABASE_USER_REFRESH_TOKEN" not in source
    assert "SUPABASE_PUBLISHABLE_KEY" not in source

    # Additionally, the endpoint the workflow resolves must really be the
    # canonical function - not merely a file that mentions its name.
    url = _resolved_function()
    assert url.rstrip("/").endswith(f"/functions/v1/{CANONICAL_FUNCTION}"), (
        f"learning-influence proof must target the canonical runtime {CANONICAL_FUNCTION}, got {url!r}"
    )

    # Additionally, the request must be authenticated by the minted short-lived
    # OIDC token, not by any other bearer value.
    assert '"Authorization: Bearer $(cat "$RUNNER_TEMP/oidc.jwt")"' in source, (
        "the runtime call must authenticate with the short-lived OIDC token, not a human session"
    )


def test_learning_influence_keeps_independent_verification_on_fresh_runtime():
    source = _source()
    assert "independent-verification" in source
    assert "executor_claim_trusted" in source
    assert "independent_verification" in source


def test_live_proof_python_heredocs_compile():
    """Catch syntax errors in Python embedded in the executed workflow steps."""
    import yaml

    workflow = yaml.safe_load(_source())
    checked = 0
    failures = []
    for job_id, job in workflow["jobs"].items():
        for step in job.get("steps", []):
            lines = step.get("run", "").splitlines()
            index = 0
            while index < len(lines):
                match = re.search(r"\bpython(?:3)?\s+-\s+<<'([A-Za-z_]\w*)'", lines[index])
                if not match:
                    index += 1
                    continue
                delimiter = match.group(1)
                end = next((i for i in range(index + 1, len(lines))
                            if lines[i].strip() == delimiter), len(lines))
                # Bash also terminates a heredoc at the end of its run script.
                checked += 1
                try:
                    compile("\n".join(lines[index + 1:end]), f"{job_id}:{step.get('name')}", "exec")
                except SyntaxError as error:
                    failures.append(str(error))
                index = end + 1
    assert checked > 0, "No Python heredocs checked"
    assert not failures, failures
