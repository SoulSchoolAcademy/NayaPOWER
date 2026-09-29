import json
from pathlib import Path

import tools.current_truth_resolver as ctr


def _live(main, *, issues=None, proof=None, runtime=None):
    return {
        "main_head": main,
        "production_branch_head": "prod-sha",
        "issue_states": issues or {"978": "CLOSED", "975": "CLOSED", "810": "OPEN"},
        "latest_successful_runtime_proof": proof,
        "live_runtime_source": runtime,
    }


def test_resolver_reports_current_main_not_latest_proven_source(monkeypatch):
    main = "a" * 40
    proven = "b" * 40
    result = ctr.resolve(
        _live(
            main,
            proof={"run_id": 123, "head_sha": proven, "conclusion": "success"},
            runtime=proven,
        ),
        repo_head=main,
    )
    assert result["status"] == "RESOLVED_WITH_UNKNOWNS"
    assert result["proof"]["current_main_is_latest_proven_source"] is False
    assert result["proof"]["source_runtime_parity"] == "MISMATCH"
    codes = {x["code"] for x in result["warnings"]}
    assert "CURRENT_MAIN_NOT_LATEST_PROVEN_SOURCE" in codes
    assert "SOURCE_RUNTIME_PARITY_MISMATCH" in codes


def test_resolver_accepts_reconciled_closed_historical_issues_with_open_frontier():
    main = "a" * 40
    result = ctr.resolve(
        _live(main, issues={"978": "CLOSED", "975": "CLOSED", "810": "OPEN"}, proof={"head_sha": main}, runtime=main),
        repo_head=main,
    )
    assert result["status"] != "CONFLICT"
    assert result["active_work"]["active_issue"] == 810
    assert result["active_work"]["active_issue_state"] == "OPEN"


def test_resolver_fails_closed_when_current_active_issue_is_closed():
    main = "a" * 40
    result = ctr.resolve(
        _live(main, issues={"978": "CLOSED", "975": "CLOSED", "810": "CLOSED"}, proof={"head_sha": main}, runtime=main),
        repo_head=main,
    )
    assert result["status"] == "CONFLICT"
    assert any(x["code"] == "ACTIVE_ISSUE_NOT_OPEN" for x in result["hard_conflicts"])


def test_resolver_preserves_unknown_runtime_instead_of_inventing_parity():
    main = "a" * 40
    result = ctr.resolve(
        _live(main, proof={"head_sha": main}, runtime=None),
        repo_head=main,
    )
    assert result["proof"]["source_runtime_parity"] == "UNKNOWN"
    assert "LIVE_RUNTIME_SOURCE" in result["unknowns"]
    assert result["proof"]["current_main_is_latest_proven_source"] is True


def test_resolver_rejects_non_main_checkout():
    repo_head = "a" * 40
    main = "b" * 40
    result = ctr.resolve(_live(main), repo_head=repo_head)
    assert result["status"] == "CONFLICT"
    assert any(x["code"] == "CHECKOUT_NOT_LIVE_MAIN" for x in result["hard_conflicts"])


def test_resolver_is_projection_not_second_authority():
    main = "a" * 40
    result = ctr.resolve(_live(main), repo_head=main)
    assert result["projection_only"] is True
    assert "not a second authority" in result["authority_note"].lower()


def test_workflow_collects_live_github_state_and_uploads_resolution():
    root = Path(__file__).resolve().parents[1]
    wf = (root / ".github" / "workflows" / "current-truth-resolver.yml").read_text()
    assert "permissions:" in wf
    assert "actions: read" in wf
    assert "issues: read" in wf
    assert '"gh", "api"' in wf
    assert '"gh", "run", "list"' in wf
    assert "current-truth-resolution.json" in wf
    assert "--fail-on-conflict" in wf
