"""Static guard: repo-native Team Naya comment writers use the governed seam."""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_repo_native_issue_comment_writers_are_governed():
    writers = []
    for path in REPO_ROOT.rglob("*.py"):
        if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "issues/{BOARD_ISSUE}/comments" in text or "issues/1354/comments" in text:
            writers.append(path)

    assert writers, "expected at least one repo-native Team Naya comment writer"
    for path in writers:
        source = path.read_text(encoding="utf-8", errors="ignore")
        assert "tools.team_naya_delivery" in source, (
            f"raw Team Naya comment writer bypasses governed delivery seam: {path}"
        )
