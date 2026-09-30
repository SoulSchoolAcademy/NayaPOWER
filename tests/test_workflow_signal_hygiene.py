from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / ".github" / "workflows" / "live-verified-ai-action-proof.yml"
PROMOTION = ROOT / ".github" / "workflows" / "governed-supabase-production-deploy.yml"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_live_proof_preflights_parity_before_behavior():
    text = _text(LIVE)
    assert "  preflight:" in text
    assert 'status="BLOCKED_BY_PARITY"' in text
    assert "production_stamped_source_revision" in text
    assert "behavioral_proof_executed" in text
    for job in ("authorized-action", "authority-absent-refusal", "concurrent-idempotency-proof"):
        pattern = rf"  {re.escape(job)}:\n    needs: preflight\n    if: needs\.preflight\.outputs\.eligible == 'true'"
        assert re.search(pattern, text), f"{job} must be gated by parity preflight"


def test_blocked_parity_is_not_relabelled_as_passed_behavior():
    text = _text(LIVE)
    assert '"behavioral_proof_executed":False' in text
    assert "behavior jobs skipped without converting BLOCKED into FAILED" in text


def test_standing_policy_denial_is_non_mutating_blocked_state():
    text = _text(PROMOTION)
    assert "id: standing_policy" in text
    assert 'echo "allowed=false" >> "$GITHUB_OUTPUT"' in text
    assert "Automatic production promotion: BLOCKED" in text
    assert "No production mutation attempted" in text
    assert 'raise SystemExit(f"FAIL CLOSED: machine policy evaluator denied the automatic promotion' not in text


def test_every_mutating_promotion_step_is_gated_after_policy_denial():
    text = _text(PROMOTION)
    names = (
        "Build provenance-stamped production deployment commit",
        "Promote provenance-stamped deployment commit to production branch",
        "Wait for a new Supabase GitHub Integration deployment check",
        "Revalidate authorized source and deployment ownership before producer",
        "Dispatch canonical fresh-intelligence producer after deployment",
        "Dispatch canonical end-to-end runtime proof after producer",
        "Dispatch canonical ACT proof after deployment",
        "Write durable production promotion receipt",
    )
    condition = "if: github.event_name == 'workflow_dispatch' || steps.standing_policy.outputs.allowed == 'true'"
    for name in names:
        pattern = rf"- name: {re.escape(name)}\n        {re.escape(condition)}"
        assert re.search(pattern, text), f"{name} must not run after a standing-policy denial"


def test_explicit_wrong_sha_still_fails_closed():
    text = _text(PROMOTION)
    assert "authorized source_sha $authorized_sha does not equal workflow source $GITHUB_SHA" in text
    assert "main moved to $resolved_main after authorization of $authorized_sha" in text
    assert "exit 1" in text
