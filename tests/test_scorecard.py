"""Tests for tools/scorecard.py — the automatic scorecard calculator.

Every test names a concrete work description and pins the score the
rubric must return. A test that cannot fail is theater; these can.
"""

import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, "tools")
from scorecard import (  # noqa: E402
    EvidenceResolver,
    ResolverBlind,
    authorize_release,
    score_work,
)


def good_work(**over):
    work = {
        "title": "Example good work",
        "evidence": [
            {"claim": "tests green", "ref": "tests/test_scorecard.py 12/12"},
            {"claim": "server tree matches", "ref": "tree 9d6af390"},
        ],
        "tests": {"ran": True, "passed": 12, "failed": 0, "can_fail": True},
        "verification": {"seat": "Naya Epsilon", "independent": True, "score": 9.5},
        "value": {"human_benefit": "a human gets a working checker",
                  "unblocks": "board-post rule becomes executable"},
        "prevention": {"gate": "receipt gate refuses field-missing posts", "wired": True},
        "honesty": {"why_not_10": "not yet run on a live PR",
                    "limits": ["one repo only"]},
    }
    work.update(over)
    return work


def test_caller_supplied_evidence_cannot_ship():
    report = score_work(good_work())
    assert report["criteria"]["evidence"]["score"] == 8.0
    assert "not authenticated" in report["criteria"]["evidence"]["reasons"][0]
    assert report["overall"] == 8.0
    assert report["verdict"] == "FIX"


def test_caller_cannot_inject_a_trusted_verifier():
    # A caller-controlled lambda must not be accepted as authenticated proof.
    with pytest.raises(TypeError):
        score_work(good_work(), evidence_verifier=lambda _item: True)


def test_forged_verified_flag_does_not_bypass_trust_boundary():
    forged = good_work(evidence=[
        {"claim": "tests green", "ref": "made-up://perfect", "verified": True},
        {"claim": "everything proven", "ref": "made-up://also-perfect", "verified": True},
    ])
    report = score_work(forged)
    assert report["criteria"]["evidence"]["score"] == 8.0
    assert report["verdict"] == "FIX"


def test_self_verification_capped_by_inviolable():
    report = score_work(good_work(
        verification={"seat": "Naya Verity", "independent": False, "score": 10.0}))
    assert report["criteria"]["verification"]["score"] == 3.0
    assert report["overall"] == 3.0
    assert report["verdict"] == "HOLD"


def test_no_evidence_means_no_bytes():
    report = score_work(good_work(evidence=[]))
    assert report["criteria"]["evidence"]["score"] == 2.0
    assert report["overall"] == 2.0


def test_evidence_without_refs_is_vague():
    report = score_work(good_work(evidence=[{"claim": "trust me"}]))
    assert report["criteria"]["evidence"]["score"] == 5.0


def test_activity_without_value_scores_3():
    report = score_work(good_work(value={}))
    assert report["criteria"]["value"]["score"] == 3.0
    assert report["overall"] == 3.0


def test_unblocks_without_human_benefit_scores_7():
    report = score_work(good_work(value={"unblocks": "the dock"}))
    assert report["criteria"]["value"]["score"] == 7.0


def test_red_tests_fail():
    report = score_work(good_work(
        tests={"ran": True, "passed": 10, "failed": 2, "can_fail": True}))
    assert report["criteria"]["tests"]["score"] == 5.0


def test_tests_that_cannot_fail_are_theater():
    report = score_work(good_work(
        tests={"ran": True, "passed": 12, "failed": 0, "can_fail": False}))
    assert report["criteria"]["tests"]["score"] == 5.0


def test_no_prevention_gate_means_class_can_recur():
    report = score_work(good_work(prevention={}))
    assert report["criteria"]["prevention"]["score"] == 4.0


def test_named_but_unwired_gate_scores_6():
    report = score_work(good_work(
        prevention={"gate": "a gate", "wired": False}))
    assert report["criteria"]["prevention"]["score"] == 6.0


def test_missing_honesty_scores_3():
    report = score_work(good_work(honesty={}))
    assert report["criteria"]["honesty"]["score"] == 3.0


def test_half_honest_scores_6():
    report = score_work(good_work(
        honesty={"why_not_10": "not yet live", "limits": []}))
    assert report["criteria"]["honesty"]["score"] == 6.0


def test_overall_is_minimum_not_average():
    # Five criteria at 10, one at 4 → overall 4, not ~9.
    report = score_work(good_work(prevention={}))
    assert report["overall"] == 4.0
    assert report["blocking"] == ["prevention"]


def test_unreadable_input_fail_closed():
    report = score_work(None)
    assert report["overall"] == 0.0
    assert report["verdict"] == "HOLD"


def test_cli_cannot_ship_without_trusted_evidence_verifier():
    payload = json.dumps(good_work())
    out = subprocess.run(
        [sys.executable, "tools/scorecard.py", "--json"],
        input=payload, capture_output=True, text=True)
    assert out.returncode == 1
    report = json.loads(out.stdout)
    assert report["verdict"] == "FIX"
    assert report["overall"] == 8.0
    assert "not authenticated" in report["criteria"]["evidence"]["reasons"][0]


def test_cli_hold_exit_1():
    payload = json.dumps(good_work(value={}))
    out = subprocess.run(
        [sys.executable, "tools/scorecard.py"],
        input=payload, capture_output=True, text=True)
    assert out.returncode == 1
    assert "HOLD" in out.stdout


def test_cli_unreadable_exit_2():
    out = subprocess.run(
        [sys.executable, "tools/scorecard.py"],
        input="not json", capture_output=True, text=True)
    assert out.returncode == 2


def test_to_10_lists_solutions_for_gaps():
    report = score_work(good_work(value={}))
    assert report["to_10"]
    assert any("human benefit" in fix for fix in report["to_10"])


def test_unverified_refs_generate_trusted_verifier_remediation():
    report = score_work(good_work())
    assert any("canonical authenticated evidence resolver" in fix for fix in report["to_10"])


def test_to_10_capped_at_10():
    worst = good_work(evidence=[], tests={"ran": False, "passed": 0,
                                           "failed": 0, "can_fail": False},
                      verification={}, value={}, prevention={}, honesty={})
    assert len(score_work(worst)["to_10"]) <= 10


def test_pass_3_hold_announces_and_passes_off():
    report = score_work(good_work(value={}, **{"pass": 3}))
    assert report["verdict"] == "HOLD"
    assert "Announce" in report["next"]
    assert "Pass off" in report["next"]


def test_pass_3_fix_announces():
    report = score_work(good_work(value={"human_benefit": "x"}, **{"pass": 3}))
    assert report["overall"] == 8.0
    assert report["verdict"] == "FIX"
    assert "Announce" in report["next"]



def test_malformed_evidence_item_prevents_perfect_evidence_score():
    work = good_work(evidence=[
        {"claim": "tests green", "ref": "tests/test_scorecard.py 12/12"},
        {"claim": "missing ref"},
    ])
    report = score_work(work)
    assert report["criteria"]["evidence"]["score"] == 5.0
    assert report["verdict"] == "HOLD"


def test_single_reference_cannot_score_10_without_internal_resolver():
    report = score_work(
        good_work(evidence=[{"claim": "tests green", "ref": "tests/test_scorecard.py 12/12"}]))
    assert report["criteria"]["evidence"]["score"] == 8.0
    assert report["verdict"] == "FIX"


# ---------------------------------------------------------------------------
# Trust-root regression battery (F2) — the falsifier, pinned forever.
# The original falsifier (commit 411ea53370): any two caller-supplied
# refs earned evidence 10.0, and a fully fabricated JSON SHIPped. Its
# residual form: score_verification returned 10.0 on a caller-asserted
# {"seat": ..., "independent": true, "score": 10.0}. These tests pin
# every door shut: diagnostic claims cap at 8.0 and say "claimed";
# authorization verifies identity, head, bytes and receipts through
# the internal resolver — or refuses in plain words.
# ---------------------------------------------------------------------------

AUTH_HEAD = "0123456789abcdef" * 2 + "01234567"
AUTH_TREE = "f" * 40


class FakeResolver(EvidenceResolver):
    """Canned-facts resolver for the authorization battery. `blind`
    simulates a total API failure (the GATE_BLIND class)."""

    def __init__(self, facts=None, paths=None, checks=None, record=None,
                 blind=False):
        self._facts = facts if facts is not None else {
            "head_sha": AUTH_HEAD, "tree_sha": AUTH_TREE,
            "author_seat": "Naya 5"}
        self._paths = paths if paths is not None else {"tests/test_scorecard.py"}
        self._checks = checks if checks is not None else {
            "scorecard-tests": "success", "test": "success"}
        self._record = record if record is not None else {
            "found": True, "score": 9.6}
        self._blind = blind

    def _fail_if_blind(self):
        if self._blind:
            raise ResolverBlind("simulated API failure (blind resolver)")

    def pr_facts(self, repo, pr_number):
        self._fail_if_blind()
        return dict(self._facts)

    def path_exists_at(self, repo, path, sha):
        self._fail_if_blind()
        return path in self._paths

    def check_state(self, repo, sha, names):
        self._fail_if_blind()
        return {name: self._checks.get(name, "missing") for name in names}

    def review_record(self, repo, pr_number, reviewer_seat):
        self._fail_if_blind()
        return dict(self._record)


def good_authorization(**over):
    authorization = {
        "repo": "SoulSchoolAcademy/NayaPOWER",
        "pr_number": 2585,
        "reviewer_seat": "Naya Epsilon",
        "head_sha": AUTH_HEAD,
        "evidence_refs": ["tests/test_scorecard.py 26 passed", AUTH_TREE],
        "required_checks": ["scorecard-tests", "test"],
    }
    authorization.update(over)
    return authorization


def test_claimed_verification_caps_at_8_and_says_claimed():
    # F3: the residual lie, pinned. good_work claims independent
    # verification at 9.5 from "Naya Epsilon" — parsed text, believed
    # by nobody: capped at 8.0 and labeled claimed, never verified.
    report = score_work(good_work())
    criterion = report["criteria"]["verification"]
    assert criterion["score"] == 8.0
    assert criterion["reasons"][0].startswith(
        "claimed independent verification (unverified)")


def test_authorize_release_happy_path_lifts_only_verified_caps():
    decision = authorize_release(
        score_work(good_work()), good_authorization(),
        resolver=FakeResolver())
    assert decision["authorized"] is True
    assert decision["verdict"] == "AUTHORIZED"
    assert decision["evidence"]["score"] == 10.0
    assert decision["verification"] == "verified independent verification"
    assert decision["verification_score"] == 10.0
    assert decision["overall"] == 10.0


def test_fabricated_full_input_never_ships_and_never_authorizes():
    # F2(a): every leg fake, including the spoofed seat and the
    # caller-set "verified": true flags (the original falsifier's
    # exact shape, plus its verification residual).
    fake = {
        "title": "fabricated everything",
        "evidence": [
            {"claim": "tests green", "ref": "made-up://perfect",
             "verified": True},
            {"claim": "everything proven", "ref": "made-up://also-perfect",
             "verified": True},
        ],
        "tests": {"ran": True, "passed": 9999, "failed": 0, "can_fail": True},
        "verification": {"seat": "Naya Epsilon", "independent": True,
                         "score": 10.0},
        "value": {"human_benefit": "benefit", "unblocks": "work"},
        "prevention": {"gate": "gate", "wired": True},
        "honesty": {"why_not_10": "none", "limits": ["none"]},
    }
    report = score_work(fake)
    assert report["verdict"] != "SHIP"
    assert report["criteria"]["evidence"]["score"] == 8.0
    assert report["criteria"]["verification"]["score"] == 8.0
    assert report["criteria"]["verification"]["reasons"][0].startswith(
        "claimed independent verification (unverified)")
    decision = authorize_release(
        report,
        good_authorization(
            evidence_refs=["made-up://perfect", "made-up://also-perfect"]),
        resolver=FakeResolver(paths=set(),
                              record={"found": False, "score": None}))
    assert decision["authorized"] is False
    assert decision["verdict"] == "REFUSED"


def test_authorize_rejects_a_callback_as_resolver():
    # F2(b): the trust boundary cannot be injected. A bare callable is
    # not the internal resolver — same rule as score_work's removed
    # evidence_verifier parameter.
    with pytest.raises(TypeError):
        authorize_release(score_work(good_work()), good_authorization(),
                          resolver=lambda *a, **k: True)


def test_resolver_not_found_keeps_evidence_capped_and_refuses():
    # F2(c): refs that resolve to nothing keep evidence at the
    # diagnostic cap, and authorization refuses.
    decision = authorize_release(
        score_work(good_work()), good_authorization(),
        resolver=FakeResolver(paths=set()))
    assert decision["authorized"] is False
    assert decision["evidence"]["score"] == 8.0
    assert decision["evidence"]["unresolved"] == [
        "tests/test_scorecard.py 26 passed"]
    assert any("did not resolve" in r for r in decision["reasons"])


def test_reviewer_who_is_the_author_cannot_authorize():
    # F2(d): reviewer seat == the PR body's declared author seat.
    decision = authorize_release(
        score_work(good_work()),
        good_authorization(reviewer_seat="Naya 5"),
        resolver=FakeResolver())
    assert decision["authorized"] is False
    assert any("author seat" in r for r in decision["reasons"])


def test_unregistered_reviewer_identity_refused():
    # Parsed text is not identity: only registry seats resolve.
    for bogus in ("Naya Nobody", "independent", "the reviewer"):
        decision = authorize_release(
            score_work(good_work()),
            good_authorization(reviewer_seat=bogus),
            resolver=FakeResolver())
        assert decision["authorized"] is False
        assert any("seat registry" in r for r in decision["reasons"])


def test_stale_head_sha_refused():
    # F2(e): the receipt names a head the PR no longer has.
    decision = authorize_release(
        score_work(good_work()),
        good_authorization(head_sha="b" * 40),
        resolver=FakeResolver())
    assert decision["authorized"] is False
    assert any("stale receipt" in r for r in decision["reasons"])


def test_newline_smuggled_head_sha_refused():
    # F2(e), binding shape: a trailing newline must not smuggle a
    # second line past the exact-head check (fullmatch, not $).
    decision = authorize_release(
        score_work(good_work()),
        good_authorization(head_sha=AUTH_HEAD + "\n"),
        resolver=FakeResolver())
    assert decision["authorized"] is False
    assert any("exact head" in r for r in decision["reasons"])


def test_blind_resolver_refuses_in_plain_words():
    # F2(f): a blind resolver (API failure) refuses with "unable to
    # verify" — and authorize_release returns, never raises.
    decision = authorize_release(
        score_work(good_work()), good_authorization(),
        resolver=FakeResolver(blind=True))
    assert decision["authorized"] is False
    assert decision["verdict"] == "REFUSED"
    assert any("unable to verify" in r for r in decision["reasons"])


def test_authorize_release_refuses_red_required_check():
    decision = authorize_release(
        score_work(good_work()), good_authorization(),
        resolver=FakeResolver(
            checks={"scorecard-tests": "success", "test": "failure"}))
    assert decision["authorized"] is False
    assert any("required check 'test' is failure" in r
               for r in decision["reasons"])


def test_authorize_release_refuses_work_below_the_bar():
    # The trust legs can all verify and the work can still not earn
    # release: value 3.0 blocks at the ship bar.
    decision = authorize_release(
        score_work(good_work(value={})), good_authorization(),
        resolver=FakeResolver())
    assert decision["authorized"] is False
    assert any("below the" in r and "ship bar" in r
               for r in decision["reasons"])


def test_cli_authorize_blind_refuses_without_traceback(tmp_path):
    # F2(f) at the CLI seam: no token in the environment means the
    # production resolver is blind — plain-words refusal, exit 1,
    # and stderr carries no traceback a tired Naya would learn to
    # ignore.
    work_file = tmp_path / "work.json"
    work_file.write_text(json.dumps(good_work()))
    auth_file = tmp_path / "auth.json"
    auth_file.write_text(json.dumps(good_authorization()))
    env = {k: v for k, v in os.environ.items()
           if k not in ("GH_TOKEN", "GITHUB_TOKEN")}
    out = subprocess.run(
        [sys.executable, "tools/scorecard.py",
         "--input", str(work_file), "--authorize", str(auth_file),
         "--json"],
        capture_output=True, text=True, env=env)
    assert out.returncode == 1
    assert "Traceback" not in out.stderr
    payload = json.loads(out.stdout)
    assert payload["authorization"]["authorized"] is False
    assert payload["authorization"]["verdict"] == "REFUSED"
    assert any("unable to verify" in r
               for r in payload["authorization"]["reasons"])
