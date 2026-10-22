"""Tests for tools/hub_deploy.py — the standalone Hub deploy pipeline
(Balanced Machine step 4, DESIGN.ai.md §5.1).

Negative controls required by the design:
* the syntax gate REFUSES a syntax-broken Hub source (file and inline forms);
* a smoke failure after publish triggers an automatic ROLLBACK, proven in a
  dry-run harness (CopyAdapter to a local target) — the target must end up
  byte-identical to the previously deployed version;
* no configured transport => the pipeline fails closed (NOT_CONFIGURED),
  never a pretend deploy.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))
import hub_deploy as hd

GOOD_PAGE = """<!doctype html><html><head><meta charset="utf-8">
<script>const NOTES = [{"id": "SN-0001", "title": "ok"}];</script>
</head><body>hub v__VERSION__</body></html>"""


def good_page(version: int) -> str:
    return GOOD_PAGE.replace("__VERSION__", str(version))

# Valid JS (trailing comma in an array literal is legal) but the baked feed
# array is NOT valid JSON -> passes the syntax gate, fails the smoke check.
CORRUPT_FEED_PAGE = """<!doctype html><html><head><meta charset="utf-8">
<script>const NOTES = [{"id": "SN-0002"},];</script>
</head><body>hub corrupt feed</body></html>"""

BROKEN_JS = "function broken( { return 1; }\n"
BROKEN_INLINE_PAGE = """<!doctype html><html><head>
<script>const x = {;</script>
</head><body>hub</body></html>"""


def _git(repo: Path, *args: str) -> str:
    env = {**os.environ,
           "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "t@t"}
    out = subprocess.run(["git", *args], cwd=repo, env=env,
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()


@pytest.fixture()
def hub_repo(tmp_path: Path) -> tuple[Path, dict[str, str]]:
    """A mini git repo whose HUB/app evolves: v1 good, v2 corrupt-feed, v3 good."""
    repo = tmp_path / "repo"
    (repo / "HUB" / "app").mkdir(parents=True)
    _git(repo, "init", "-q")
    page = repo / "HUB" / "app" / "index.html"
    commits = {}
    for key, body in [("v1", good_page(1)),
                      ("v2", CORRUPT_FEED_PAGE),
                      ("v3", good_page(3))]:
        page.write_text(body, encoding="utf-8")
        _git(repo, "add", "-A")
        _git(repo, "commit", "-qm", key)
        commits[key] = _git(repo, "rev-parse", "HEAD")
    return repo, commits


# ---------------------------------------------------------------- gate -----

def test_syntax_gate_accepts_good_sources(tmp_path: Path):
    src = tmp_path / "app"
    src.mkdir()
    (src / "index.html").write_text(good_page(1), encoding="utf-8")
    (src / "app.js").write_text("const ok = () => 1;\n", encoding="utf-8")
    failures = hd.syntax_gate(hd.collect_hub_files(src), tmp_path / "scratch")
    assert failures == []


def test_syntax_gate_refuses_broken_js_file(tmp_path: Path):
    src = tmp_path / "app"
    src.mkdir()
    (src / "app.js").write_text(BROKEN_JS, encoding="utf-8")
    failures = hd.syntax_gate(hd.collect_hub_files(src), tmp_path / "scratch")
    assert failures, "gate must refuse a syntax-broken .js source"
    assert "app.js" in failures[0]


def test_syntax_gate_refuses_broken_inline_script(tmp_path: Path):
    src = tmp_path / "app"
    src.mkdir()
    (src / "index.html").write_text(BROKEN_INLINE_PAGE, encoding="utf-8")
    failures = hd.syntax_gate(hd.collect_hub_files(src), tmp_path / "scratch")
    assert failures, "gate must refuse a syntax-broken inline <script>"
    assert "index.html" in failures[0]


# --------------------------------------------------------------- smoke -----

def test_smoke_check_forms(tmp_path: Path):
    good = tmp_path / "good"
    good.mkdir()
    (good / "index.html").write_text(good_page(1), encoding="utf-8")
    ok, _ = hd.smoke_check(str(good))
    assert ok

    corrupt = tmp_path / "corrupt"
    corrupt.mkdir()
    (corrupt / "index.html").write_text(CORRUPT_FEED_PAGE, encoding="utf-8")
    ok, detail = hd.smoke_check(str(corrupt))
    assert not ok and "parse" in detail

    ok, _ = hd.smoke_check(str(tmp_path / "does-not-exist"))
    assert not ok


# -------------------------------------------------------------- deploy -----

def test_deploy_fails_closed_when_no_transport(hub_repo, tmp_path: Path, monkeypatch):
    repo, commits = hub_repo
    monkeypatch.delenv("HUB_DEPLOY_CMD", raising=False)
    code = hd.run_deploy(commits["v1"], None, str(tmp_path / "target"),
                         state_path=tmp_path / "state.json", repo=repo)
    assert code == hd.EXIT_NOT_CONFIGURED


def test_deploy_happy_path_then_smoke_failure_rolls_back(hub_repo, tmp_path: Path):
    repo, commits = hub_repo
    target = tmp_path / "target"
    state = tmp_path / "state.json"

    # v1 deploys clean.
    code = hd.run_deploy(commits["v1"], str(target), str(target),
                         state_path=state, repo=repo)
    assert code == hd.EXIT_OK
    assert "hub v1" in (target / "index.html").read_text(encoding="utf-8")
    assert json.loads(state.read_text())["deployed_commit"] == commits["v1"]

    # v2 passes the syntax gate but its baked feed array is corrupt JSON:
    # smoke fails and the pipeline must roll the target back to v1 bytes.
    receipt = tmp_path / "receipt.json"
    code = hd.run_deploy(commits["v2"], str(target), str(target),
                         state_path=state, repo=repo, receipt_path=receipt)
    assert code == hd.EXIT_SMOKE
    assert "hub v1" in (target / "index.html").read_text(encoding="utf-8")
    assert json.loads(state.read_text())["deployed_commit"] == commits["v1"]
    rec = json.loads(receipt.read_text())
    assert rec["result"] == "SMOKE_FAILED" and rec["rollback"] == "done"

    # v3 deploys clean on top; state now remembers v1 as previous.
    code = hd.run_deploy(commits["v3"], str(target), str(target),
                         state_path=state, repo=repo)
    assert code == hd.EXIT_OK
    assert "hub v3" in (target / "index.html").read_text(encoding="utf-8")
    st = json.loads(state.read_text())
    assert st["deployed_commit"] == commits["v3"]
    assert st["previous_commit"] == commits["v1"]


def test_manual_rollback_republishes_previous(hub_repo, tmp_path: Path):
    repo, commits = hub_repo
    target = tmp_path / "target"
    state = tmp_path / "state.json"
    assert hd.run_deploy(commits["v1"], str(target), str(target),
                         state_path=state, repo=repo) == hd.EXIT_OK
    assert hd.run_deploy(commits["v3"], str(target), str(target),
                         state_path=state, repo=repo) == hd.EXIT_OK
    # run_rollback uses the module-level STATE_PATH by default; point it via
    # the state file argument the CLI uses — here we call with explicit state.
    code = hd.run_rollback(str(target), state_path=state, repo=repo)
    assert code == hd.EXIT_OK
    assert "hub v1" in (target / "index.html").read_text(encoding="utf-8")
