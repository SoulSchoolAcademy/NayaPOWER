import json
from pathlib import Path

import tools.current_truth_resolver as ctr


def _live(main, *, issues=None, proof=None, runtime=None):
    return {
        "main_head": main,
        "production_branch_head": "prod-sha",
        "issue_states": issues or {"66": "OPEN", "978": "CLOSED", "975": "CLOSED", "810": "CLOSED"},
        "latest_successful_runtime_proof": proof,
        "live_runtime_source": runtime,
        "open_prs": [{"number": 1053, "title": "Current truth", "head_sha": "pr-head", "draft": False, "merge_state": "CLEAN"}],
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


def test_resolver_fails_closed_when_active_issue_is_closed():
    main = "a" * 40
    result = ctr.resolve(
        _live(main, issues={"66": "CLOSED"}, proof={"head_sha": main}, runtime=main),
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
    assert "set +e" in wf
    assert 'status=$?' in wf
    assert 'exit "$status"' in wf
    assert "if: always()" in wf


def test_control_plane_points_to_open_current_truth_frontier():
    root = Path(__file__).resolve().parents[1]
    brain = json.loads((root / "BRAIN" / "NAYAPOWER-BRAIN-INDEX.json").read_text())
    ops = json.loads((root / "BRAIN" / "90-OPERATIONS" / "0003-ULTIMATE-MASTER-EXECUTION-PLAN-V1.json").read_text())
    assert brain["operations"]["active_issue"] == 66
    assert ops["current_state"]["issue_978"].startswith("CLOSED")
    assert ops["current_state"]["issue_975"].startswith("CLOSED")
    assert ops["current_state"]["issue_810"].startswith("CLOSED")
    assert ops["top_10"][0]["id"] == "#66"


def test_generated_markdown_continuation_brief_contains_operational_handoff():
    main = "a" * 40
    result = ctr.resolve(
        _live(main, proof={"run_id": 123, "head_sha": main, "conclusion": "success"}, runtime=None),
        repo_head=main,
    )
    md = ctr.render_markdown(result)
    assert "# NayaPOWER Current Truth" in md
    assert f"`{main}`" in md
    assert "**Active issue:** #66 (OPEN)" in md
    assert "## One next action" in md
    assert "## Warnings / unknowns" in md
    assert "LIVE_RUNTIME_SOURCE" in md
    assert "## Max-10" in md
    assert "Projection only" in md


def test_workflow_publishes_and_uploads_generated_continuation_brief():
    root = Path(__file__).resolve().parents[1]
    wf = (root / ".github" / "workflows" / "current-truth-resolver.yml").read_text()
    assert "--markdown-output current-truth-brief.md" in wf
    assert "current-truth-brief.md" in wf
    assert "GITHUB_STEP_SUMMARY" in wf


def test_resolver_carries_live_open_pr_frontier():
    main = "a" * 40
    result = ctr.resolve(_live(main, proof={"head_sha": main}, runtime=main), repo_head=main)
    prs = result["active_work"]["open_prs"]
    assert prs[0]["number"] == 1053
    assert prs[0]["head_sha"] == "pr-head"
    md = ctr.render_markdown(result)
    assert "## Open pull requests" in md
    assert "#1053 Current truth" in md
    assert "`pr-head`" in md


def test_workflow_collects_live_open_pull_requests():
    root = Path(__file__).resolve().parents[1]
    wf = (root / ".github" / "workflows" / "current-truth-resolver.yml").read_text()
    assert "pull-requests: read" in wf
    assert '"gh", "pr", "list"' in wf
    assert '"number,title,headRefOid,isDraft,mergeStateStatus,updatedAt"' in wf
    assert '"open_prs": open_prs' in wf
