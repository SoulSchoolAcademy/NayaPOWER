"""The merge-consensus workflow must be able to read workflow runs.

The PR-scoped merge-authority verifier queries actions/workflows/.../runs.
Without the explicit Actions read permission, GitHub returns 403 and the
check exits 2 (unable to verify) instead of rendering a structured verdict.
"""
from pathlib import Path
import re

REPO = Path(__file__).resolve().parents[1]
WORKFLOW = REPO / ".github" / "workflows" / "merge-consensus-gate.yml"


def test_merge_consensus_workflow_grants_only_required_actions_read():
    text = WORKFLOW.read_text(encoding="utf-8")
    match = re.search(
        r"(?ms)^permissions:\s*\n(?P<body>(?:^[ \t]+[^\n]*\n)+)",
        text,
    )
    assert match, "workflow must declare an explicit least-privilege permissions block"
    permissions = match.group("body")
    assert re.search(r"(?m)^\s+actions:\s*read\s*$", permissions), (
        "merge-authority verifier calls the Actions API; grant actions: read "
        "inside the workflow's explicit permissions block"
    )
    assert not re.search(r"(?m)^\s+actions:\s*write\s*$", permissions), (
        "the merge-authority verifier is read-only; actions: write is excessive"
    )
