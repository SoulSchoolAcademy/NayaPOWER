"""Trigger-chain jurisdiction gate — pytest enforcement (GOVERN wave 31).

Runs on the real operating path: kernel-tests.yml executes `pytest -q` on
every PR and every push to main. A BLOCK here is a red CI check, which the
merge protocol treats as a hard stop.

The #2020/#2152 bypass class: jurisdiction analysis followed the FILE LIST,
not the TRIGGER CHAIN. A benign-looking change (one capture JSON) merged
under low jurisdiction while its chain — .naya/capture/** push-to-main ->
live-intelligence-commit-proof (mints OIDC, invokes LIVE runtime) ->
live-supabase-runtime-proof — executed production-consequential actions.

L215 proof directions are exercised by T1 (GREEN, clean tree), T2 (RED,
planted violation), T3 (negative control), T4 (manifest anti-drift), T5
(authorization marker both directions).
"""

import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from trigger_chain_jurisdiction import (  # noqa: E402
    AUTH_MARKER_PATH,
    MANIFEST_PATH,
    change_specific_chains,
    emit_manifest,
    jurisdiction_for,
    load_workflows,
    repo_root,
    validate_auth_marker,
    verdict,
)


def root():
    # repo root via git (works in CI checkouts and worktrees); the script's
    # own fallback handles non-git trees.
    return repo_root(None)


@pytest.fixture(scope="module")
def workflows():
    return load_workflows(root())


@pytest.fixture(scope="module")
def manifest_disk():
    with open(os.path.join(root(), MANIFEST_PATH)) as f:
        return json.load(f)


def valid_marker(tmp_path=None):
    return {
        "version": 1,
        "authorized_paths": [".naya/capture/**"],
        "board_receipt": (
            "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354"
            "#issuecomment-6120000000"
        ),
        "authorized_by": "Shawn Vibert",
        "authorized_at": "2026-10-12T10:00:00Z",
        "scope_note": "test fixture only",
    }


# T1 — GREEN control: a change with no production chain passes.
def test_clean_tree_change_passes(workflows):
    code, report = verdict(["HUB/app/index.html", "BRAIN/05-MEMORY/x.md"],
                           workflows, None)
    assert code == 0, report
    assert report["verdict"] == "PASS"
    assert report["production_links"] == []


# T2 — RED direction: the #2020 shape blocks without authorization.
def test_capture_change_blocks_without_marker(workflows):
    code, report = verdict([".naya/capture/some-lesson.json"], workflows, None)
    assert code == 1, report
    assert report["verdict"] == "BLOCK"
    assert "live-intelligence-commit-proof.yml" in report["production_links"]
    # the full chain is named: root + workflow_run descendant
    assert "live-supabase-runtime-proof.yml" in report["production_links"]
    assert AUTH_MARKER_PATH in report["reason"]


# T2b — RED direction via the CLI on a real planted violation (L215 live).
def test_cli_blocks_planted_violation_live(tmp_path):
    paths_file = tmp_path / "paths.txt"
    paths_file.write_text(".naya/capture/planted-violation.json\n")
    proc = subprocess.run(
        [sys.executable,
         os.path.join(root(), "tools", "trigger_chain_jurisdiction.py"),
         "--tree", root(), "--paths-file", str(paths_file)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "BLOCK" in proc.stdout
    assert "live-intelligence-commit-proof" in proc.stdout


# T3 — negative control: standing-pipeline-only changes never need a marker.
@pytest.mark.parametrize("path", [
    "HUB/app/index.html",
    "BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/x.md",  # BRAIN/** -> resolver only
    "tools/some_helper.py",
    "README.md",
])
def test_non_production_paths_pass(workflows, path):
    code, report = verdict([path], workflows, None)
    assert code == 0, (path, report)


# T3b — the marker file itself is not a trigger (no self-trigger loop).
def test_marker_file_itself_has_no_chain(workflows):
    code, report = verdict([AUTH_MARKER_PATH], workflows, None)
    assert code == 0, report
    assert report["direct_triggers"] == {}


# T4 — manifest anti-drift + curation discipline: regeneration from LIVE
# bytes == checked-in manifest, and every entry carries a human review date
# against its exact bytes (a byte change resets reviewed_at to None, forcing
# explicit re-curation — re-emitting alone cannot clear it).
def test_manifest_matches_live_bytes(workflows, manifest_disk):
    import trigger_chain_jurisdiction as tcj
    fresh = tcj.emit_manifest(workflows, manifest_disk)
    assert fresh["workflows"] == manifest_disk["workflows"], (
        "manifest drifted from live workflow bytes — re-curate the changed "
        "workflow's production classification and re-emit with "
        "`python tools/trigger_chain_jurisdiction.py --emit-manifest`"
    )


def test_every_entry_reviewed_against_its_bytes(manifest_disk):
    unreviewed = [f for f, w in manifest_disk["workflows"].items()
                  if not w.get("reviewed_at")]
    assert unreviewed == [], (
        f"entries without human review against current bytes: {unreviewed} — "
        "review the classification, update evidence, set reviewed_at"
    )


# T4b — every push-to-main workflow is curated (fail closed).
def test_no_unclassified_push_main_workflows(workflows):
    import trigger_chain_jurisdiction as tcj
    unclassified = [
        fname for fname, wf in workflows.items()
        if wf["push_main"] and tcj.CURATED.get(fname) is None
    ]
    assert unclassified == [], (
        f"unclassified push-to-main workflows (fail closed): {unclassified}"
    )


# T5a — valid marker covering the chained paths passes.
def test_valid_marker_passes(workflows):
    code, report = verdict([".naya/capture/x.json"], workflows, valid_marker())
    assert code == 0, report
    assert report["verdict"] == "PASS"
    assert "merge seat must still verify" in report["reason"]


# T5b — marker that does not cover the chained paths blocks.
def test_non_covering_marker_blocks(workflows):
    marker = valid_marker()
    marker["authorized_paths"] = ["BRAIN/**"]
    code, report = verdict([".naya/capture/x.json"], workflows, marker)
    assert code == 1, report
    assert "do not cover" in report["reason"]


# T5c — malformed marker blocks (missing receipt).
def test_malformed_marker_blocks(workflows):
    marker = valid_marker()
    del marker["board_receipt"]
    code, report = verdict([".naya/capture/x.json"], workflows, marker)
    assert code == 1, report


# T5d — marker unit validation: bad receipt URL rejected.
def test_marker_receipt_url_must_be_this_repo():
    ok, reasons = validate_auth_marker(
        {**valid_marker(), "board_receipt": "https://example.com/evil"},
        [".naya/capture/x.json"],
    )
    assert not ok and reasons


# T6 — change-specificity: every-push (unfiltered) triggers are the standing
# pipeline and cannot create a production chain by themselves.
def test_unfiltered_push_triggers_are_not_change_specific(workflows):
    unfiltered = [f for f, w in workflows.items()
                  if w["push_main"] and w["push_paths"] is None]
    assert unfiltered, "expected standing-pipeline workflows to exist"
    hits = change_specific_chains(["any/random/path.txt"], workflows)
    assert hits == {}, hits


# T7 — the CI wiring exists and invokes the gate (it must not silently rot).
def test_ci_wiring_workflow_exists():
    import trigger_chain_jurisdiction as tcj
    wf_path = os.path.join(root(), ".github", "workflows",
                           "trigger-chain-jurisdiction.yml")
    assert os.path.exists(wf_path), "wiring workflow file missing"
    body = open(wf_path).read()
    assert "trigger_chain_jurisdiction.py" in body
    assert "pull_request" in body and "push" in body
    assert "--pr-author" in body


# T8 — end-to-end CLI on a real temp git repo via --base-ref/--head-ref.
def test_cli_end_to_end_on_temp_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1",
               GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    def git(*a):
        subprocess.run(["git", "-C", str(repo), *a], check=True, env=env,
                       capture_output=True)
    git("init", "-q")
    # minimal workflow tree: one path-filtered production-shaped trigger.
    # (Uses the REAL script against a synthetic repo.)
    (repo / ".github" / "workflows").mkdir(parents=True)
    (repo / ".github" / "workflows" / "demo-prod.yml").write_text(
        "name: Demo Prod\non:\n  push:\n    branches: [main]\n"
        "    paths: ['cap/**']\njobs:\n  j:\n    runs-on: ubuntu-latest\n"
        "    steps:\n      - run: curl $ACTIONS_ID_TOKEN_REQUEST_URL\n")
    git("add", "-A")
    git("commit", "-qm", "base")
    base = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True,
                          env=env).stdout.strip()
    (repo / "cap").mkdir()
    (repo / "cap" / "x.json").write_text("{}")
    git("add", "-A")
    git("commit", "-qm", "change")
    # unclassified workflow -> BLOCK (fail closed), even though synthetic
    proc = subprocess.run(
        [sys.executable,
         os.path.join(root(), "tools", "trigger_chain_jurisdiction.py"),
         "--tree", str(repo), "--base-ref", base, "--head-ref", "HEAD"],
        capture_output=True, text=True)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "unclassified" in proc.stdout.lower() or "BLOCK" in proc.stdout


# T9 — descendants() matches the curated chain (curation prose is tested).
def test_descendants_match_curated_chain(workflows):
    roots = ["live-intelligence-commit-proof.yml"]
    got = set()
    import trigger_chain_jurisdiction as tcj
    got = set(tcj.descendants(roots, workflows))
    assert got == {"live-supabase-runtime-proof.yml"}, got


# T10 — class-level anti-drift: a STANDING-PIPELINE (unfiltered push-to-main)
# production-consequential workflow must carry a standing_ratification record.
# workflow_run-only production workflows inherit authorization from their
# change-specific chain root, so they are out of scope here.
def test_no_unratified_standing_production_workflows(workflows):
    import trigger_chain_jurisdiction as tcj
    bad = [f for f, w in workflows.items()
           if w["push_main"] and w["push_paths"] is None
           and tcj.CURATED.get(f, (False, None, None))[0] is True
           and not (tcj.CURATED.get(f, (False, None, None))[2] or {}).get("basis")]
    assert bad == [], (
        f"standing-pipeline production workflows without ratification record: "
        f"{bad}"
    )


def test_standing_ratifications_are_explicit(manifest_disk):
    for fname, w in manifest_disk["workflows"].items():
        if not (w.get("production_consequential")
                and w.get("push_main")
                and w.get("push_path_filters") is None):
            continue  # not standing-pipeline production: N/A
        sr = w.get("standing_ratification")
        assert isinstance(sr, dict) and sr.get("status") in (
            "RATIFIED", "PLACEMENT_ONLY"), (
            f"{fname}: standing production workflow needs an explicit "
            f"standing_ratification (RATIFIED or PLACEMENT_ONLY)")
        assert sr.get("basis"), f"{fname}: ratification basis is empty"


# T5e — self-authorization is rejected when the PR author is known.
def test_self_authorization_blocked(workflows):
    marker = valid_marker()
    marker["authorized_by"] = "some-seat"
    code, report = verdict([".naya/capture/x.json"], workflows, marker,
                           pr_author="some-seat")
    assert code == 1, report
    assert "self-authorization" in report["reason"]


def test_different_author_passes(workflows):
    code, report = verdict([".naya/capture/x.json"], workflows,
                           valid_marker(), pr_author="some-seat")
    assert code == 0, report


# Parser regression tests — fail-open shapes must model as push-to-main.
def test_push_without_branches_means_all_branches(tmp_path):
    import trigger_chain_jurisdiction as tcj
    wfdir = tmp_path / ".github" / "workflows"
    wfdir.mkdir(parents=True)
    (wfdir / "x.yml").write_text(
        "name: X\non:\n  push:\n    paths: ['a/**']\n"
        "jobs:\n  j:\n    runs-on: ubuntu-latest\n    steps: []\n")
    wf = tcj.load_workflows(str(tmp_path))
    assert wf["x.yml"]["push_main"] is True


def test_scalar_branches_wrapped(tmp_path):
    import trigger_chain_jurisdiction as tcj
    wfdir = tmp_path / ".github" / "workflows"
    wfdir.mkdir(parents=True)
    (wfdir / "x.yml").write_text(
        "name: X\non:\n  push:\n    branches: main\n"
        "jobs:\n  j:\n    runs-on: ubuntu-latest\n    steps: []\n")
    wf = tcj.load_workflows(str(tmp_path))
    assert wf["x.yml"]["push_main"] is True


def test_branches_ignore_honored(tmp_path):
    import trigger_chain_jurisdiction as tcj
    wfdir = tmp_path / ".github" / "workflows"
    wfdir.mkdir(parents=True)
    (wfdir / "x.yml").write_text(
        "name: X\non:\n  push:\n    branches: ['**']\n    branches-ignore: ['main']\n"
        "jobs:\n  j:\n    runs-on: ubuntu-latest\n    steps: []\n")
    wf = tcj.load_workflows(str(tmp_path))
    assert wf["x.yml"]["push_main"] is False


def test_scalar_paths_wrapped(tmp_path):
    import trigger_chain_jurisdiction as tcj
    wfdir = tmp_path / ".github" / "workflows"
    wfdir.mkdir(parents=True)
    (wfdir / "x.yml").write_text(
        "name: X\non:\n  push:\n    branches: [main]\n    paths: cap/exact.json\n"
        "jobs:\n  j:\n    runs-on: ubuntu-latest\n    steps: []\n")
    wf = tcj.load_workflows(str(tmp_path))
    assert wf["x.yml"]["push_paths"] == ["cap/exact.json"]
    hits = tcj.change_specific_chains(["cap/exact.json"], wf)
    assert hits == {"cap/exact.json": ["x.yml"]}, hits


# Glob unit tests — GitHub semantics incl. character classes.
@pytest.mark.parametrize("pattern,path,expected", [
    (".naya/capture/**", ".naya/capture/x.json", True),
    (".naya/capture/**", ".naya/capture/a/b.json", True),
    ("*.md", "README.md", True),
    ("*.md", "docs/README.md", True),  # basename-only matches at any depth
    ("docs/*.md", "docs/a/b.md", False),  # * does not cross /
    ("file[0-9].txt", "file5.txt", True),
    ("file[0-9].txt", "filex.txt", False),
    ("file[!0-9].txt", "filex.txt", True),
    ("file[!0-9].txt", "file5.txt", False),
    ("file?.txt", "file5.txt", True),
    ("main", "main", True),  # branch glob
    ("**", "main", True),
])
def test_github_glob_semantics(pattern, path, expected):
    import trigger_chain_jurisdiction as tcj
    assert bool(tcj.github_glob_to_regex(pattern).match(path)) is expected

