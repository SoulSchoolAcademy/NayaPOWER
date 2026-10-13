"""Tests for the L245 merge-authority packet assembler (B-25).

tools/assemble_merge_packet.py builds the DELEGATED-MERGE-AUTHORITY packet
from real PR data. Every GitHub read goes through the provider seam, so the
whole suite runs on fixtures with zero network.

Negative-control matrix (B-25 repair spec):
  valid packet on a real PR shape            -> PASS (exit 0)
  missing scorecard                         -> FAIL, exact reason
  score 8.5                                 -> FAIL, exact reason (below 9.0)
  self-validator ("naya5" vs "naya-5")      -> FAIL (identity normalization)
  CHANGES_REQUESTED                         -> FAIL (team_objections = 1)
  no approving review                       -> FAIL (validator unnamed)
  test check-run red                        -> FAIL (tests_green not true)
  no venue post                             -> FAIL (posted_to_1354 not true)
  API failure                               -> exit 2 "unable to verify"
"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from assemble_merge_packet import (  # noqa: E402
    DEFAULT_VENUE,
    GitHubError,
    _kernel_test_job_name,
    assemble,
)

HEAD = "ea762857554091a3f9a70f3f98b90d0ebbbc9a9d"
SHORT = HEAD[:8]


def _pr(**over):
    d = {
        "number": 2510,
        "head": {"sha": HEAD, "ref": "naya5/learn-artifacts-mechanization"},
        "base": {"ref": "main"},
        "user": {"login": "SomeUser"},
    }
    d.update(over)
    return d


def _scorecard_comment(**over):
    body = (
        "[NAYA KAPPA - REVIEW] APPROVED\n\n"
        "## SCORECARD\n\n"
        f"head: {HEAD}\n"
        "Seat: Naya Kappa\n"
        "verdict: 9.5\n\n"
        "## Evidence\n\n"
        "- live handles...\n\n"
        "value calculus run: the most intelligent thing wins.\n\n"
        "Post-merge report: sign-out on the venue after merge.\n"
    )
    d = {"id": 6139651754, "user": {"login": "Naya Kappa"}, "body": body}
    d.update(over)
    return d


def _venue_comment(**over):
    d = {"id": 6139900001,
         "user": {"login": "Naya 2"},
         "body": (f"build-signout: PR #2510 @ {SHORT} OPEN non-draft — "
                  f"FINAL 9.0/10 SHIPS, builder-scorer 3 rounds; "
                  f"venue sign-out posted")}
    d.update(over)
    return d


def _venue_signin_no_score(**over):
    d = {"id": 6139900002,
         "user": {"login": "Naya 2"},
         "body": (f"sign-in: working PR #2510 @ {SHORT} — "
                  f"scorecard to follow")}
    d.update(over)
    return d


class FakeGitHub:
    """Fixture provider. api_down=True makes every read raise."""

    def __init__(self, pr=None, reviews=None, comments=None,
                 check_runs=None, venue_comments=None, venue_by_number=None,
                 api_down=False):
        self._pr = pr if pr is not None else _pr()
        self._reviews = reviews if reviews is not None else [
            {"user": {"login": "Naya Kappa"}, "state": "APPROVED",
             "commit_id": HEAD}]
        self._comments = comments if comments is not None else [
            _scorecard_comment()]
        self._check_runs = check_runs if check_runs is not None else [
            {"name": "test", "conclusion": "success",
             "completed_at": "2026-10-13T06:13:04Z", "id": 1149000001},
            {"name": "guard", "conclusion": "success",
             "completed_at": "2026-10-13T06:13:05Z", "id": 1149000002},
        ]
        self._venue = (venue_comments if venue_comments is not None
                       else [_venue_comment()])
        self._venue_by_number = venue_by_number
        self._down = api_down

    def _maybe_down(self):
        if self._down:
            raise GitHubError("boom")

    def get_pr(self, pr):
        self._maybe_down()
        return self._pr

    def list_reviews(self, pr):
        self._maybe_down()
        return self._reviews

    def list_pr_comments(self, pr):
        self._maybe_down()
        return self._comments

    def list_check_runs(self, head_sha):
        self._maybe_down()
        return self._check_runs

    def list_venue_comments(self, venue):
        self._maybe_down()
        if self._venue_by_number is not None:
            return self._venue_by_number.get(venue, [])
        return self._venue


def _packet(**over):
    client = FakeGitHub(**over)
    # pin the kernel-test job name: unit tests exercise derivation logic,
    # not workflow-file resolution (covered by test_kernel_test_job_name_*)
    packet, evidence = assemble(client, 2510, DEFAULT_VENUE, test_job="test")
    return packet, evidence


# --- the happy path --------------------------------------------------------

def test_valid_pr_shape_assembles_passing_packet():
    packet, evidence = _packet()
    assert packet["target"] == "main"
    assert packet["branch"] == "naya5/learn-artifacts-mechanization"
    assert packet["seat"] == "naya5"
    assert packet["tests_green"] is True
    assert "1149000001" in packet["test_evidence"]
    assert packet["self_scorecard"] == {
        "score": 9.5, "evidence_backed": True, "value_calculus_run": True}
    assert packet["independent_validator"] == "Naya Kappa"
    assert packet["posted_to_1354"] is True
    assert packet["team_objections"] == 0
    assert packet["post_merge_report_planned"] is True
    # authorship is recorded: a fabricated self-scorecard is distinguishable
    assert evidence["scorecard_comment_author"] == "Naya Kappa"
    assert evidence["venue_comment_author"] == "Naya 2"
    assert evidence["validator_commit_id"] == HEAD
    assert evidence["stale_approvals_ignored"] == []
    # and the canonical check passes on it
    sys.path.insert(0, str(ROOT / "tools" / "protocol"))
    import merge_authority
    verdict = merge_authority.check(packet)
    assert verdict["pass"] is True, verdict["reasons"]


def test_seat_falls_back_to_author_login_without_slash():
    pr = _pr()
    pr["head"] = {"sha": HEAD, "ref": "hotfix-branch"}
    packet, _ = _packet(pr=pr)
    assert packet["seat"] == "SomeUser"


# --- negative controls: each missing condition fails with its reason -------

def _check(packet):
    sys.path.insert(0, str(ROOT / "tools" / "protocol"))
    import merge_authority
    return merge_authority.check(packet)


def test_missing_scorecard_fails_with_exact_reason():
    packet, _ = _packet(comments=[{"id": 1, "body": "lgtm"}])
    assert packet["self_scorecard"] is False
    verdict = _check(packet)
    assert verdict["pass"] is False
    assert any("self_scorecard missing" in r for r in verdict["reasons"])


def test_score_below_9_fails_with_exact_reason():
    comment = _scorecard_comment()
    comment["body"] = comment["body"].replace("verdict: 9.5", "verdict: 8.5")
    packet, _ = _packet(comments=[comment])
    assert packet["self_scorecard"]["score"] == 8.5
    verdict = _check(packet)
    assert verdict["pass"] is False
    assert any("8.5 < 9.0" in r for r in verdict["reasons"])


def test_self_validator_alias_fails_on_normalization():
    reviews = [{"user": {"login": "naya-5"}, "state": "APPROVED",
                "commit_id": HEAD}]
    packet, evidence = _packet(reviews=reviews)
    # "naya-5" normalizes to the seat "naya5": not an independent validator
    assert packet["independent_validator"] == ""
    verdict = _check(packet)
    assert verdict["pass"] is False
    assert any("independent_validator unnamed" in r
               for r in verdict["reasons"])


def test_changes_requested_counts_as_objection():
    reviews = [
        {"user": {"login": "Naya Kappa"}, "state": "APPROVED",
         "commit_id": HEAD},
        {"user": {"login": "Naya 4"}, "state": "CHANGES_REQUESTED",
         "commit_id": HEAD},
    ]
    packet, evidence = _packet(reviews=reviews)
    assert packet["team_objections"] == 1
    assert evidence["changes_requested_by"] == ["Naya 4"]
    verdict = _check(packet)
    assert verdict["pass"] is False
    assert any("team_objections = 1" in r for r in verdict["reasons"])


def test_no_approving_review_fails_validator_unnamed():
    packet, _ = _packet(reviews=[])
    assert packet["independent_validator"] == ""
    verdict = _check(packet)
    assert verdict["pass"] is False
    assert any("independent_validator unnamed" in r
               for r in verdict["reasons"])


def test_red_test_check_run_fails_tests_green():
    runs = [{"name": "test", "conclusion": "failure",
             "completed_at": "2026-10-13T06:13:04Z", "id": 1149000001}]
    packet, evidence = _packet(check_runs=runs)
    assert packet["tests_green"] is False
    assert evidence["check_run_failures"] == ["test"]
    verdict = _check(packet)
    assert verdict["pass"] is False
    assert any("tests_green is not true" in r for r in verdict["reasons"])


def test_missing_venue_post_fails_posted():
    packet, _ = _packet(venue_comments=[])
    assert packet["posted_to_1354"] is False
    verdict = _check(packet)
    assert verdict["pass"] is False
    assert any("posted_to_1354 is not true" in r for r in verdict["reasons"])


def test_legacy_venue_fallback_counts_law_letter_post():
    """Round-3 G2: a seat posting on the delegation's original venue (per
    LAW-A03's letter) is not misread as missing; evidence names the venue."""
    client = FakeGitHub(venue_by_number={2175: [], 1354: [_venue_comment()]})
    packet, evidence = assemble(client, 2510, DEFAULT_VENUE, test_job="test")
    assert packet["posted_to_1354"] is True
    assert evidence["venue_matched"] == 1354


def test_live_venue_preferred_over_legacy():
    client = FakeGitHub(
        venue_by_number={2175: [_venue_comment()], 1354: [_venue_comment()]})
    packet, evidence = assemble(client, 2510, DEFAULT_VENUE, test_job="test")
    assert packet["posted_to_1354"] is True
    assert evidence["venue_matched"] == 2175


# --- kernel-test job name resolution (round-3 G3) ----------------------------

def _workflow_file(tmp_path, body):
    d = tmp_path / ".github" / "workflows"
    d.mkdir(parents=True)
    f = d / "kernel-tests.yml"
    f.write_text(body)
    return f


def test_kernel_test_job_name_no_name_field_uses_job_id(tmp_path):
    f = _workflow_file(tmp_path, "name: Kernel Tests\n\non: push\n\njobs:\n"
                                 "  test:\n    runs-on: ubuntu-latest\n")
    assert _kernel_test_job_name(f) == "test"


def test_kernel_test_job_name_prefers_name_field(tmp_path):
    f = _workflow_file(tmp_path, "jobs:\n  test:\n    name: Kernel Test Suite\n"
                                 "    runs-on: ubuntu-latest\n")
    assert _kernel_test_job_name(f) == "Kernel Test Suite"


def test_kernel_test_job_name_missing_file_fails_closed(tmp_path):
    with pytest.raises(GitHubError):
        _kernel_test_job_name(tmp_path / "nope.yml")


def test_kernel_test_job_name_ambiguous_multi_job_fails_closed(tmp_path):
    body = "jobs:\n  lint:\n    runs-on: ubuntu-latest\n  build:\n    runs-on: ubuntu-latest\n"
    with pytest.raises(GitHubError):
        _kernel_test_job_name(_workflow_file(tmp_path, body))


def test_kernel_test_job_name_single_job_used(tmp_path):
    f = _workflow_file(tmp_path, "jobs:\n  kernel:\n    runs-on: ubuntu-latest\n")
    assert _kernel_test_job_name(f) == "kernel"


# --- packet machine schema (round-3 G10) -----------------------------------

SCHEMA = json.loads(
    (Path(__file__).resolve().parent.parent
     / "tools" / "authority_packet.schema.json").read_text())


def _conforms(packet):
    """Structural conformance to authority_packet.schema.json without a
    jsonschema dependency (the test env's venv lacks it): required keys
    present, no extra keys, scalar types match."""
    required = SCHEMA["required"]
    assert set(packet.keys()) == set(required), (  # additionalProperties: false
        f"packet keys {sorted(packet.keys())} != schema required "
        f"{sorted(required)}")
    type_map = {"string": str, "boolean": bool, "integer": int}
    for key, spec in SCHEMA["properties"].items():
        types = spec["type"] if isinstance(spec["type"], list) else [spec["type"]]
        if key == "self_scorecard":
            continue  # union validated below
        assert isinstance(packet[key], tuple(type_map[t] for t in types)), (
            key, type(packet[key]))
    sc = packet["self_scorecard"]
    assert sc is False or isinstance(sc, dict)
    if isinstance(sc, dict):
        assert set(sc.keys()) == {
            "score", "evidence_backed", "value_calculus_run"}, sc.keys()
        assert isinstance(sc["score"], (int, float))
        assert isinstance(sc["evidence_backed"], bool)
        assert isinstance(sc["value_calculus_run"], bool)


def test_packet_conforms_to_machine_schema():
    packet, _ = _packet()
    _conforms(packet)


def test_packet_conforms_with_jsonschema_when_available():
    jsonschema = pytest.importorskip("jsonschema")
    packet, _ = _packet()
    jsonschema.validate(packet, SCHEMA)


# --- live-API replay (round-3 G5) ------------------------------------------

FIXTURES = (Path(__file__).resolve().parent / "fixtures" / "b25")


def _fixture_bytes(name):
    return (FIXTURES / name).read_bytes()


def _replay_run(cmd, **kwargs):
    """Stub at the exec boundary: serve captured real API payloads.
    Everything above this line — _api's arg building, JSON parsing,
    _paged's pagination, the derivation logic — is production code."""
    assert cmd[1] == "api"
    full = cmd[2]
    prefix = "repos/SoulSchoolAcademy/NayaPOWER/"
    assert full.startswith(prefix), full
    path = full[len(prefix):]
    base, _, query = path.partition("?")

    def page_file(stem, default_ext="json"):
        params = dict(p.split("=", 1) for p in query.split("&") if "=" in p)
        page = params.get("page", "1")
        f = FIXTURES / f"{stem}_p{page}.{default_ext}"
        return f.read_bytes() if f.exists() else b"[]"

    if base == "pulls/2510":
        body = _fixture_bytes("pr_2510.json")
    elif base == "pulls/2510/reviews":
        body = page_file("reviews_2510")
    elif base == "issues/2510/comments":
        body = page_file("pr_comments_2510")
    elif base.startswith("commits/") and base.endswith("/check-runs"):
        body = _fixture_bytes("check_runs_head.json")
    elif base == "issues/2175/comments":
        body = page_file("venue_2175")
    elif base == "issues/1354/comments":
        body = b"[]"  # not reached in this replay (live venue hit first)
    else:
        raise AssertionError(f"unexpected API path in replay: {path}")

    class Done:
        returncode = 0
        stdout = body.decode("utf-8")
        stderr = ""

    return Done()


def test_live_api_replay_through_real_client(monkeypatch):
    """The round-2 scorer's G5: the GitHubClient seam was mocked in every
    test. Here the REAL client parses REAL captured payloads — only the
    subprocess exec is stubbed. Must reproduce the live smoke run's
    findings exactly."""
    import subprocess as _sp
    import assemble_merge_packet as amp
    monkeypatch.setattr(_sp, "run", _replay_run)
    client = amp.GitHubClient("SoulSchoolAcademy/NayaPOWER")
    packet, evidence = amp.assemble(client, 2510, amp.DEFAULT_VENUE,
                                    test_job="test")
    # live smoke findings, 2026-10-13 ~07:05Z on PR #2510 @ 58a619df:
    assert packet["posted_to_1354"] is True  # B-37 sign-out on #2175 p17
    assert evidence["venue_matched"] == 2175
    assert packet["tests_green"] is False  # 2 real failing check-runs
    assert packet["independent_validator"] == ""  # no independent validator
    assert evidence["head_sha"] == (
        "58a619dfe3c6da291f339e579dd30ff862c191fd")
    assert packet["seat"] == "naya2"  # seat via branch prefix
    _conforms(packet)  # schema twin holds on real shapes too


def test_scorecard_without_evidence_section_not_evidence_backed():
    comment = _scorecard_comment()
    comment["body"] = comment["body"].replace("## Evidence\n\n", "")
    packet, _ = _packet(comments=[comment])
    assert packet["self_scorecard"]["evidence_backed"] is False
    verdict = _check(packet)
    assert verdict["pass"] is False
    assert any("evidence_backed is not true" in r for r in verdict["reasons"])


def test_scorecard_naming_other_head_does_not_count():
    comment = _scorecard_comment()
    comment["body"] = comment["body"].replace(HEAD, "0" * 40)
    packet, _ = _packet(comments=[comment])
    assert packet["self_scorecard"] is False


def test_stale_approval_on_old_head_does_not_validate():
    old_head = "0" * 40
    reviews = [{"user": {"login": "Naya Kappa"}, "state": "APPROVED",
                "commit_id": old_head}]
    packet, evidence = _packet(reviews=reviews)
    # the approval is stale: not counted as an independent validator
    assert packet["independent_validator"] == ""
    assert evidence["stale_approvals_ignored"] == ["Naya Kappa"]
    verdict = _check(packet)
    assert verdict["pass"] is False
    assert any("independent_validator unnamed" in r
               for r in verdict["reasons"])


def test_venue_signin_without_score_does_not_count_as_posted():
    # "scorecard to follow" names the PR and the head but carries no
    # scorecard verdict: intent only, not intent+scorecard+validation
    packet, _ = _packet(venue_comments=[_venue_signin_no_score()])
    assert packet["posted_to_1354"] is False
    verdict = _check(packet)
    assert verdict["pass"] is False
    assert any("posted_to_1354 is not true" in r for r in verdict["reasons"])


def test_pr_tag_does_not_match_longer_number():
    comment = _venue_comment()
    comment["body"] = comment["body"].replace("#2510", "#25101")
    packet, _ = _packet(venue_comments=[comment])
    assert packet["posted_to_1354"] is False


def test_cancelled_check_run_fails_tests_green():
    runs = [
        {"name": "test", "conclusion": "success",
         "completed_at": "2026-10-13T06:13:04Z", "id": 1149000001},
        {"name": "guard", "conclusion": "cancelled",
         "completed_at": "2026-10-13T06:13:05Z", "id": 1149000002},
    ]
    packet, evidence = _packet(check_runs=runs)
    assert packet["tests_green"] is False
    assert evidence["check_run_failures"] == ["guard"]
    verdict = _check(packet)
    assert verdict["pass"] is False
    assert any("tests_green is not true" in r for r in verdict["reasons"])


def test_in_progress_check_run_fails_tests_green():
    runs = [
        {"name": "test", "conclusion": "success",
         "completed_at": "2026-10-13T06:13:04Z", "id": 1149000001},
        {"name": "guard", "conclusion": None,
         "completed_at": "2026-10-13T06:13:05Z", "id": 1149000002},
    ]
    packet, _ = _packet(check_runs=runs)
    assert packet["tests_green"] is False


# --- fail-closed on API failure --------------------------------------------

def test_api_failure_raises_for_fail_closed_exit_2():
    client = FakeGitHub(api_down=True)
    with pytest.raises(GitHubError):
        assemble(client, 2510, DEFAULT_VENUE)


def test_packet_is_json_serializable():
    packet, evidence = _packet()
    json.dumps({"packet": packet, "evidence": evidence})
