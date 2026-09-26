from pathlib import Path


def test_github_dispatch_bridge_has_single_projection_selector():
    source = (Path(__file__).resolve().parents[1] / "NAYANET" / "EXECUTION-BRIDGE" / "nayanet-github-dispatch" / "index.ts").read_text(encoding="utf-8")
    marker = 'const isProjection=operation==="project_smart_note";'
    assert source.count(marker) == 1, "duplicate projection selector causes the Edge Function to fail at startup"


def test_projection_workflow_detects_untracked_projection_for_commit():
    workflow = (Path(__file__).resolve().parents[1] / ".github" / "workflows" / "project-canonical-smart-note.yml").read_text(encoding="utf-8")
    commit_step = workflow.split("- name: Commit deterministic projection", 1)[1].split("- name: Byte-for-byte verification from main", 1)[0]
    assert "git ls-files --error-unmatch" in commit_step, "commit step must distinguish tracked projections from newly created untracked projections"
    assert "git diff --cached --quiet" in commit_step, "commit step must detect staged changes before deciding no commit is required"
    assert "git show \"$FETCH_HEAD:$TARGET\"" in workflow, "final verification must read the artifact from the freshly fetched main commit"
    assert "relative_path=path.resolve().relative_to(repo_root).as_posix()" in workflow, "projection-path must be repository-relative for Git object verification"
    assert "git cat-file -e \"$FETCH_HEAD:$TARGET\"" in workflow, "final verification must prove the projection exists in freshly fetched main"
