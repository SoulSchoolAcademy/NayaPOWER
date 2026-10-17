"""Tests for the L245 post-merge authority audit (B-25).

tools/authority_audit.py re-checks every first-parent main commit in the
window (merges, squash merges, direct pushes — a merges-only enumeration
would be fail-open on the exact class L245 exists for). Verdicts:
  PACKET_VALID        - authority check green on the exact merged head
  EXERCISED_AUTHORITY - the merge commit's author identity is the
                        director's own click: recorded, never flagged,
                        never reverted
  INVALID             - neither: revert PR proposed (dry-run here), venue
                        receipt planned
  SKIP                - the tool's own revert PR, or an already-open revert

Negative-control matrix (B-25 repair spec):
  invalid-authority post-merge (synthetic) -> revert planned, tree
      byte-identical to the pre-commit base (real temp git repo)
  lane merge with the LIVE merged_by distribution (org login) + no
      packet -> INVALID, revert planned (B-25 repair round, 2026-10-13:
      the old default fake used merged_by="SomeLane", a world that
      doesn't exist on the live repo)
  exercised authority (director merge-commit author identity) -> no
      revert, recorded not flagged
  packet valid                              -> no revert
  existing open revert PR                   -> skipped, never double-filed
      (PR path AND no-PR path — the dedup is hoisted above the fork)
  own revert PR (revert/* + marker)         -> skipped, no ping-pong
  commit naming no PR (direct push)         -> INVALID, authority unprovable
  direct push by the director               -> EXERCISED_AUTHORITY
  director identity matching is case/space-tolerant (casefold+strip)
  workflow without the authority job        -> audit refuses (exit 2), never
                                             reads absence as guilt
"""

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from authority_audit import (  # noqa: E402
    AUTHORITY_CHECK_NAME,
    DIRECTOR_AUTHOR_EMAIL,
    DIRECTOR_AUTHOR_NAME,
    GitHubClient,
    GitHubError,
    _is_director_commit,
    audit_commit,
    authority_job_present,
    build_revert,
)

MERGE_SHA = "5cc6d3aa34a951b2e184f1b96b057e2dcc4fee9d"
FIRST_PARENT = "d0d970a5451238e08cff35e2eba6c9aafa606b74"
HEAD_SHA = "ea762857554091a3f9a70f3f98b90d0ebbbc9a9d"

# Live `merged_by` distribution (B-25 repair round, 2026-10-13): the API
# reports the ORG login on merges of both classes — never a lane login.
LIVE_MERGED_BY = {"login": "SoulSchoolAcademy"}
# Lane merge-commit author identity (live evidence: Naya 4 review 5500983723).
LANE_AUTHOR_NAME = "Naya 5"
LANE_AUTHOR_EMAIL = "naya5@soulschool.academy"


def _commit(**over):
    d = {"sha": MERGE_SHA,
         "message": "Merge pull request #2508 from naya5/learn-artifacts-mechanization\n",
         "parents": [FIRST_PARENT, HEAD_SHA],
         "author_login": "SomeLane",
         "author_name": LANE_AUTHOR_NAME,
         "author_email": LANE_AUTHOR_EMAIL,
         "date": "2026-10-13T06:48:10Z"}
    d.update(over)
    return d


def _director_commit(**over):
    """A commit whose git author identity is the director's own merge."""
    d = _commit(author_login="ShawnDirector",
                author_name=DIRECTOR_AUTHOR_NAME,
                author_email=DIRECTOR_AUTHOR_EMAIL)
    d.update(over)
    return d


class FakeAuditGitHub:
    def __init__(self, pr=None, authority_ok=False, existing_revert=None):
        self._pr = pr if pr is not None else {
            "number": 2508,
            "head": {"sha": HEAD_SHA, "ref": "naya5/learn-artifacts-mechanization"},
            "body": "some body",
            # The live `merged_by` distribution: the org login on merges of
            # BOTH classes (B-25 repair round, 2026-10-13). The old default
            # ("SomeLane") was a world that doesn't exist on the live repo.
            "merged_by": dict(LIVE_MERGED_BY),
        }
        self._authority_ok = authority_ok
        self._existing = existing_revert
        self.opened_prs = []
        self.venue_posts = []

    def get_pr(self, pr):
        return self._pr

    def authority_check_passed(self, head_sha):
        return self._authority_ok

    def find_open_revert_pr(self, sha):
        return self._existing

    def open_revert_pr(self, branch, title, body, base="main"):
        self.opened_prs.append({"branch": branch, "title": title,
                                "body": body, "base": base})
        return {"number": 2512}

    def post_venue_comment(self, venue, body):
        self.venue_posts.append({"venue": venue, "body": body})
        return {"id": 1}


def _git(args, cwd):
    out = subprocess.run(["git"] + args, capture_output=True, text=True,
                         cwd=str(cwd), timeout=60, check=False)
    assert out.returncode == 0, out.stderr[:300]
    return out.stdout.strip()


@pytest.fixture()
def temp_repo(tmp_path):
    """A real git repo: main with one merge commit, origin/main ref set,
    and a working `origin` remote (bare) so push works for real."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(["init", "-b", "main"], repo)
    _git(["config", "user.email", "test@example.com"], repo)
    _git(["config", "user.name", "Test"], repo)
    (repo / "a.txt").write_text("base\n")
    _git(["add", "a.txt"], repo)
    _git(["commit", "-m", "base"], repo)
    _git(["checkout", "-b", "feature"], repo)
    (repo / "b.txt").write_text("feature\n")
    _git(["add", "b.txt"], repo)
    _git(["commit", "-m", "feature work"], repo)
    _git(["checkout", "main"], repo)
    _git(["merge", "--no-ff", "-m",
          "Merge pull request #9999 from feature", "feature"], repo)
    merge_sha = _git(["rev-parse", "HEAD"], repo)
    first_parent = _git(["rev-parse", "HEAD^1"], repo)
    _git(["update-ref", "refs/remotes/origin/main", "main"], repo)
    origin = tmp_path / "origin.git"
    _git(["init", "--bare", str(origin)], tmp_path)
    _git(["remote", "add", "origin", str(origin)], repo)
    _git(["push", "origin", "main"], repo)
    return repo, merge_sha, first_parent


@pytest.fixture()
def repo_with_workflow(tmp_path):
    """A repo dir carrying the merge-consensus workflow (for the
    authority-job presence gate)."""
    wf_dir = tmp_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True)
    (wf_dir / "merge-consensus-gate.yml").write_text(
        "jobs:\n"
        "  consensus:\n"
        "    name: Team review + scorecard receipt\n"
        "  authority:\n"
        "    name: Verify merge authority\n")
    return tmp_path


# --- verdicts ---------------------------------------------------------------

def test_packet_valid_needs_no_revert(tmp_path):
    client = FakeAuditGitHub(authority_ok=True)
    v = audit_commit(client, _commit(), tmp_path, 2175, dry_run=True)
    assert v["verdict"] == "PACKET_VALID"
    assert v["authority_basis"] == "packet"
    assert client.opened_prs == []


def test_exercised_authority_recorded_never_reverted(tmp_path):
    """The director's own merge click: merge-COMMIT author identity is the
    discriminator — `merged_by` is the org login even here (live bytes)."""
    pr = {"number": 2508, "head": {"sha": HEAD_SHA, "ref": "naya5/x"},
          "body": "b", "merged_by": dict(LIVE_MERGED_BY)}
    client = FakeAuditGitHub(pr=pr, authority_ok=False)
    v = audit_commit(client, _director_commit(), tmp_path, 2175,
                     dry_run=True)
    assert v["verdict"] == "EXERCISED_AUTHORITY"
    assert v["authority_basis"] == "exercised"
    assert v["evidence_complete"] is False
    assert client.opened_prs == []
    assert client.venue_posts == []


def test_lane_merge_with_live_merged_by_is_invalid(temp_repo):
    """Naya 4's named regression test (review 5500983723): with the LIVE
    `merged_by` distribution (org login) and no authority packet, a lane
    merge MUST be INVALID with a revert planned — the old discriminator
    read this exact case as the director's own click."""
    repo, merge_sha, first_parent = temp_repo
    pr = {"number": 2508, "head": {"sha": HEAD_SHA, "ref": "naya5/x"},
          "body": "b", "merged_by": dict(LIVE_MERGED_BY)}
    client = FakeAuditGitHub(pr=pr, authority_ok=False)
    commit = {"sha": merge_sha,
              "message": "Merge pull request #2508 from naya5/x\n",
              "parents": [first_parent, "f" * 40],
              "author_login": "SomeLane",
              "author_name": LANE_AUTHOR_NAME,
              "author_email": LANE_AUTHOR_EMAIL,
              "date": "2026-10-13T06:48:10Z"}
    v = audit_commit(client, commit, repo, 2175, dry_run=True)
    assert v["verdict"] == "INVALID"
    assert v["authority_basis"] == "none"
    assert v["revert_pr"] is None  # dry-run: planned, not opened
    assert client.opened_prs == []


def test_invalid_merge_plans_revert_in_dry_run(temp_repo):
    repo, merge_sha, first_parent = temp_repo
    client = FakeAuditGitHub(authority_ok=False)
    commit = {"sha": merge_sha,
              "message": "Merge pull request #9999 from feature\n",
              "parents": [first_parent, "f" * 40],
              "author_login": "SomeLane",
              "author_name": LANE_AUTHOR_NAME,
              "author_email": LANE_AUTHOR_EMAIL,
              "date": "2026-10-13T06:48:10Z"}
    v = audit_commit(client, commit, repo, 2175, dry_run=True)
    assert v["verdict"] == "INVALID"
    assert v["authority_basis"] == "none"
    assert v["tree_verified"] is True
    assert v["revert_pr"] is None  # dry-run: planned, not opened
    assert client.opened_prs == []


def test_invalid_merge_opens_revert_pr_live(temp_repo):
    repo, merge_sha, first_parent = temp_repo
    client = FakeAuditGitHub(authority_ok=False)
    commit = {"sha": merge_sha,
              "message": "Merge pull request #9999 from feature\n",
              "parents": [first_parent, "f" * 40],
              "author_login": "SomeLane",
              "author_name": LANE_AUTHOR_NAME,
              "author_email": LANE_AUTHOR_EMAIL,
              "date": "2026-10-13T06:48:10Z"}
    v = audit_commit(client, commit, repo, 2175, dry_run=False)
    assert v["verdict"] == "INVALID"
    assert v["revert_pr"] == 2512
    assert len(client.opened_prs) == 1
    opened = client.opened_prs[0]
    assert opened["branch"] == f"revert/{merge_sha[:8]}"
    assert opened["base"] == "main"
    assert "L245-REVERT-FOR:" in opened["body"]
    assert "never auto-merge" in opened["body"]
    assert "re-invocation lane" in opened["body"]
    assert len(client.venue_posts) == 1
    assert "INVALID" in client.venue_posts[0]["body"]


def test_existing_revert_pr_skips_never_double_files(tmp_path):
    client = FakeAuditGitHub(
        authority_ok=False,
        existing_revert={"number": 2500, "title": "Revert ... (L245)"})
    v = audit_commit(client, _commit(), tmp_path, 2175, dry_run=False)
    assert v["verdict"] == "SKIP"
    assert client.opened_prs == []


def test_existing_revert_pr_skips_on_no_pr_path(temp_repo):
    """The dedup guarantee ("never double-filed") must hold on the no-PR
    path too — before the hoist, a direct-push INVALID opened a FRESH
    revert PR on every audit run, contradicting the module docstring."""
    repo, _, _ = temp_repo
    (repo / "e.txt").write_text("direct\n")
    _git(["add", "e.txt"], repo)
    _git(["commit", "-m", "direct push to main"], repo)
    sha = _git(["rev-parse", "HEAD"], repo)
    parent = _git(["rev-parse", "HEAD^"], repo)
    _git(["push", "origin", "main"], repo)
    client = FakeAuditGitHub(
        authority_ok=False,
        existing_revert={"number": 2501, "title": "Revert ... (L245)"})
    commit = {"sha": sha, "message": "direct push to main\n",
              "parents": [parent], "author_login": None,
              "author_name": LANE_AUTHOR_NAME,
              "author_email": LANE_AUTHOR_EMAIL,
              "date": "2026-10-13T06:48:10Z"}
    v = audit_commit(client, commit, repo, 2175, dry_run=False)
    assert v["verdict"] == "SKIP", v
    assert "already open" in v["reason"]
    assert "pr" not in v  # no-PR record carries no PR field
    assert client.opened_prs == []


def test_director_identity_matching_is_case_and_space_tolerant():
    """Display names are not case-stable: these must all read as the
    director, never fail closed into INVALID against his own merge."""
    assert _is_director_commit(DIRECTOR_AUTHOR_NAME,
                              DIRECTOR_AUTHOR_EMAIL) is True
    assert _is_director_commit("shawn vibert",
                              DIRECTOR_AUTHOR_EMAIL) is True
    assert _is_director_commit("SHAWN VIBERT",
                              DIRECTOR_AUTHOR_EMAIL) is True
    assert _is_director_commit("  Shawn Vibert ",
                              " HumanMaximusCodex@Gmail.Com ") is True
    assert _is_director_commit("someone else",
                              DIRECTOR_AUTHOR_EMAIL) is False
    assert _is_director_commit(DIRECTOR_AUTHOR_NAME,
                              "wrong@example.com") is False
    assert _is_director_commit("", "") is False


def test_own_revert_pr_skipped_no_ping_pong(tmp_path):
    pr = {"number": 2512,
          "head": {"sha": HEAD_SHA, "ref": "revert/5cc6d3aa"},
          "body": "<!-- L245-REVERT-FOR: 5cc6d3aa34a951b2e184f1b96b057e2dcc4fee9d -->\n...",
          "merged_by": {"login": "SomeLane"}}
    client = FakeAuditGitHub(pr=pr, authority_ok=False)
    commit = _commit(
        message="Merge pull request #2512 from revert/5cc6d3aa\n")
    v = audit_commit(client, commit, tmp_path, 2175, dry_run=False)
    assert v["verdict"] == "SKIP"
    assert "own L245 revert PR" in v["reason"]
    assert client.opened_prs == []


def test_squash_merge_names_pr_and_audits(tmp_path):
    pr = {"number": 1348, "head": {"sha": HEAD_SHA, "ref": "naya4/x"},
          "body": "b", "merged_by": {"login": "SomeLane"}}
    client = FakeAuditGitHub(pr=pr, authority_ok=True)
    commit = _commit(
        message="some title (#1348)\n",
        parents=["a" * 40])  # single parent: squash
    v = audit_commit(client, commit, tmp_path, 2175, dry_run=True)
    assert v["verdict"] == "PACKET_VALID"
    assert v["pr"] == 1348


def test_squash_merge_with_body_still_names_pr(tmp_path):
    """Round-3 G1: the real-world squash shape carries a body (this team's
    pre-submit rule requires ## Evidence on every PR). The old end-anchored
    regex missed it -> spurious INVALID -> spurious revert PR."""
    pr = {"number": 1348, "head": {"sha": HEAD_SHA, "ref": "naya4/x"},
          "body": "b", "merged_by": {"login": "SomeLane"}}
    client = FakeAuditGitHub(pr=pr, authority_ok=True)
    commit = _commit(
        message=("some title (#1348)\n"
                 "\n"
                 "## Evidence\n"
                 "\n"
                 "- handle one\n"
                 "\n"
                 "Co-authored-by: Someone <someone@example.com>\n"),
        parents=["a" * 40])  # single parent: squash
    v = audit_commit(client, commit, tmp_path, 2175, dry_run=True)
    assert v["verdict"] == "PACKET_VALID", v
    assert v["pr"] == 1348


def test_direct_push_without_pr_is_invalid(temp_repo):
    repo, _, _ = temp_repo
    (repo / "e.txt").write_text("direct\n")
    _git(["add", "e.txt"], repo)
    _git(["commit", "-m", "direct push to main"], repo)
    sha = _git(["rev-parse", "HEAD"], repo)
    parent = _git(["rev-parse", "HEAD^"], repo)
    _git(["push", "origin", "main"], repo)  # G8: build_revert fetches origin/main
    client = FakeAuditGitHub(authority_ok=False)
    commit = {"sha": sha, "message": "direct push to main\n",
              "parents": [parent], "author_login": "SomeLane",
              "author_name": LANE_AUTHOR_NAME,
              "author_email": LANE_AUTHOR_EMAIL,
              "date": "2026-10-13T06:48:10Z"}
    v = audit_commit(client, commit, repo, 2175, dry_run=True)
    assert v["verdict"] == "INVALID"
    assert "no PR" in v["reason"]
    assert client.opened_prs == []  # dry-run


def test_direct_push_by_director_is_exercised_authority(tmp_path):
    client = FakeAuditGitHub(authority_ok=False)
    commit = _director_commit(message="direct push to main\n",
                              parents=["a" * 40])
    v = audit_commit(client, commit, tmp_path, 2175, dry_run=True)
    assert v["verdict"] == "EXERCISED_AUTHORITY"
    assert client.opened_prs == []


# --- the tree-verified revert, on real git bytes -----------------------------

def test_revert_restores_pre_merge_tip_byte_identical(temp_repo):
    repo, merge_sha, first_parent = temp_repo
    revert = build_revert(repo, merge_sha, first_parent, is_merge=True)
    assert revert["tree_verified"] is True
    assert revert["diff_stat"] == ""
    tree_files = _git(
        ["ls-tree", "-r", "--name-only", revert["revert_head"]], repo)
    assert "b.txt" not in tree_files.splitlines()
    assert "a.txt" in tree_files.splitlines()


def test_single_commit_revert_restores_parent_tree(temp_repo):
    repo, merge_sha, first_parent = temp_repo
    # single commit on main (squash-shaped): revert == inverse of the commit
    (repo / "d.txt").write_text("single\n")
    _git(["add", "d.txt"], repo)
    _git(["commit", "-m", "single change (#1234)"], repo)
    single_sha = _git(["rev-parse", "HEAD"], repo)
    parent = _git(["rev-parse", "HEAD^"], repo)
    _git(["push", "origin", "main"], repo)  # G8: build_revert fetches origin/main
    revert = build_revert(repo, single_sha, parent, is_merge=False)
    assert revert["tree_verified"] is True
    assert revert["diff_stat"] == ""


def test_revert_reports_dirty_tree_when_later_merges_touch_other_files(
        temp_repo):
    repo, merge_sha, first_parent = temp_repo
    (repo / "c.txt").write_text("later\n")
    _git(["add", "c.txt"], repo)
    _git(["commit", "-m", "later"], repo)
    _git(["push", "origin", "main"], repo)  # G8: build_revert fetches origin/main
    revert = build_revert(repo, merge_sha, first_parent, is_merge=True)
    assert revert["conflict"] is False
    assert revert["tree_verified"] is False
    assert "c.txt" in revert["diff_stat"]


def test_revert_conflict_aborts_clean_and_reports(temp_repo):
    repo, merge_sha, first_parent = temp_repo
    (repo / "b.txt").write_text("later change\n")
    _git(["add", "b.txt"], repo)
    _git(["commit", "-m", "later"], repo)
    _git(["push", "origin", "main"], repo)  # G8: build_revert fetches origin/main
    revert = build_revert(repo, merge_sha, first_parent, is_merge=True)
    assert revert["conflict"] is True
    assert revert["tree_verified"] is False
    assert revert["revert_head"] is None
    # repo left clean: no half-applied revert state, back on main
    assert _git(["status", "--porcelain"], repo) == ""
    assert _git(["rev-parse", "--abbrev-ref", "HEAD"], repo) == "main"


# --- the audit refuses to run blind ------------------------------------------

def test_authority_job_present_when_workflow_defines_it(repo_with_workflow):
    assert authority_job_present(repo_with_workflow) is True


def test_authority_job_absent_when_workflow_missing_job(tmp_path):
    wf_dir = tmp_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True)
    (wf_dir / "merge-consensus-gate.yml").write_text(
        "jobs:\n  consensus:\n    name: Team review + scorecard receipt\n")
    assert authority_job_present(tmp_path) is False


def test_authority_job_absent_when_workflow_file_missing(tmp_path):
    assert authority_job_present(tmp_path) is False


def test_real_workflow_defines_the_authority_job():
    wf = ROOT / ".github" / "workflows" / "merge-consensus-gate.yml"
    assert authority_job_present(ROOT) is True, (
        f"{wf} must define a job named exactly {AUTHORITY_CHECK_NAME!r}: "
        f"the audit looks up that check-run name on merged heads")
    # and the name matches the audit's lookup constant, parsed not asserted
    data = yaml.safe_load(wf.read_text())
    names = [j.get("name") for j in data["jobs"].values()
             if isinstance(j, dict)]
    assert AUTHORITY_CHECK_NAME in names


# --- first-parent walk: branch heads are never audited ----------------------

def _canned_commit(sha, parents, date, login="A",
                   name="Lane Author", email="lane@example.com"):
    return {"sha": sha,
            "parents": [{"sha": p} for p in parents],
            "commit": {"committer": {"date": date},
                       "author": {"name": name, "email": email}},
            "author": {"login": login}}


def test_list_main_commits_walks_first_parent_only():
    canned = {
        "tip": _canned_commit("tip", ["mid", "branchhead"],
                             "2026-10-13T07:00:00Z"),
        "mid": _canned_commit("mid", ["old"], "2026-10-13T06:00:00Z",
                              login="B", name="Mid Author",
                              email="mid@example.com"),
        "old": _canned_commit("old", [], "2026-10-13T05:00:00Z",
                              login="C"),
    }
    client = GitHubClient("o/r")

    def fake_api(path, method="GET", body=None):
        if path == "git/refs/heads/main":
            return {"object": {"sha": "tip"}}
        assert path.startswith("commits/")
        return canned[path.split("/")[1]]

    client._api = fake_api
    since = datetime(2026, 10, 13, 4, 0, tzinfo=timezone.utc)
    got = client.list_main_commits(since)
    # branchhead (second parent) never appears: it was never a main tip
    assert [c["sha"] for c in got] == ["tip", "mid", "old"]
    assert got[1]["author_login"] == "B"
    # the exercised-authority identity fields are captured, not just the
    # linked login (B-25 repair round, 2026-10-13)
    assert got[1]["author_name"] == "Mid Author"
    assert got[1]["author_email"] == "mid@example.com"


def test_list_main_commits_stops_at_window_edge():
    canned = {
        "tip": _canned_commit("tip", ["old"], "2026-10-13T07:00:00Z"),
        "old": _canned_commit("old", [], "2026-10-13T01:00:00Z"),
    }
    client = GitHubClient("o/r")

    def fake_api(path, method="GET", body=None):
        if path == "git/refs/heads/main":
            return {"object": {"sha": "tip"}}
        return canned[path.split("/")[1]]

    client._api = fake_api
    since = datetime(2026, 10, 13, 4, 0, tzinfo=timezone.utc)
    got = client.list_main_commits(since)
    assert [c["sha"] for c in got] == ["tip"]


# --- revert that fails without starting is an error, not a conflict --------

def test_revert_of_missing_sha_raises_not_conflict(temp_repo):
    repo, _, _ = temp_repo
    with pytest.raises(GitHubError, match="failed without starting"):
        build_revert(repo, "0" * 40, "f" * 40, is_merge=False)
    # repo left on main, clean — no half-applied state
    assert _git(["rev-parse", "--abbrev-ref", "HEAD"], repo) == "main"
    assert _git(["status", "--porcelain"], repo) == ""

