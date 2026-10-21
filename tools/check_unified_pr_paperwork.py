#!/usr/bin/env python3
"""Single risk-tiered paperwork gate for PR evidence.

Substantive tests/spec checks remain separate. This gate only validates the
cross-seat scorecard/evidence paperwork and routes pure content PRs to the
canonical content door. It never changes repository protection settings.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import urllib.error

try:
    import check_merge_consensus as consensus
    import check_pr_receipt as receipt
    from pr_flow_tier import classify_tier
except ModuleNotFoundError:  # support import from repository tests
    from tools import check_merge_consensus as consensus
    from tools import check_pr_receipt as receipt
    from tools.pr_flow_tier import classify_tier


def _emit(code: int, message: str, cure: str) -> int:
    print(f"UNIFIED PAPERWORK GATE: {code}")
    print(f"Reason: {message}")
    print(f"One cure: {cure}")
    return 0 if code == "PASS" else 1


def _read_event() -> dict:
    path = os.environ.get("GITHUB_EVENT_PATH", "")
    if not path:
        raise RuntimeError("GITHUB_EVENT_PATH is missing")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _live_pr(event: dict, repo: str, token: str) -> tuple[dict, int]:
    number = os.environ.get("PR_NUMBER")
    if not number:
        issue = event.get("issue") or {}
        number = str(issue.get("number") or "")
    if not number:
        pr_event = event.get("pull_request") or {}
        number = str(pr_event.get("number") or "")
    if not number:
        raise RuntimeError("could not identify PR number from event")
    # Always refresh the live PR: event payloads and previous check runs can be stale.
    pr = consensus.api_get(f"/repos/{repo}/pulls/{number}", token)
    return pr, int(number)


def _scorecard_for_current_head(comments: list[dict], head: str,
                                author_seat: str, minimum: float) -> tuple[bool, str]:
    for comment in comments:
        body = comment.get("body") or ""
        low = body.lower()
        # Require a parsed head field, not a SHA mentioned anywhere in prose.
        # Seat is an explicit declaration; the repo currently does not
        # cryptographically bind declared seat labels to agent identities.
        if "scorecard" not in low and "verdict" not in low:
            continue
        if consensus.scorecard_head_of(body) != head.lower():
            continue
        seat = consensus.author_seat_of(body)
        if not seat or seat == author_seat:
            continue
        score = consensus._score_of(body)
        if score is not None and minimum <= score <= 10:
            return True, f"scorecard {score:g}/10 from different declared seat {seat} pins current head {head[:12]}"
    return False, f"no numeric scorecard >= {minimum:g}/10 from a different declared seat with an explicit head field pinned to current head {head[:12]}"


def _cross_seat_review(reviews: list[dict], comments: list[dict],
                       author_login: str, author_seat: str) -> tuple[bool, str]:
    for review in reviews:
        user = ((review.get("user") or {}).get("login") or "").lower()
        if review.get("state") == "APPROVED" and user and user != author_login.lower():
            return True, f"native GitHub approval from a different login ({user})"
    for comment in comments:
        body = comment.get("body") or ""
        seat = consensus.author_seat_of(body)
        if consensus._looks_like_review(body) and seat and seat != author_seat:
            return True, f"review receipt from different declared seat {seat}"
    return False, f"no accepted review from a different declared seat than author {author_seat}"


def run() -> int:
    event = _read_event()
    repo = os.environ.get("REPO") or os.environ.get("GITHUB_REPOSITORY") or ""
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    if not repo or not token:
        return _emit("ERROR — VERIFICATION_UNAVAILABLE",
                     "repository or read token is unavailable",
                     "restore the workflow's read-only GitHub token and re-run")

    try:
        pr, number = _live_pr(event, repo, token)
        head = ((pr.get("head") or {}).get("sha") or "").strip()
        title = pr.get("title") or ""
        body = pr.get("body") or ""
        if len(head) != 40 or any(ch not in "0123456789abcdef" for ch in head):
            return _emit("ERROR — VERIFICATION_UNAVAILABLE",
                         "GitHub did not return a valid current head SHA",
                         "retry after GitHub's PR API returns the current 40-character SHA")

        files = consensus.api_get(f"/repos/{repo}/pulls/{number}/files", token)
        paths = [item.get("filename", "") for item in files if item.get("filename")]
        expected_files = pr.get("changed_files")
        tier = classify_tier(title, paths, changed_files=files, expected_changed_files=expected_files)
        print(f"Tier: {tier['tier']} — {tier['reason']}")
        print(f"PR: #{number}; current head: {head}")

        if tier["tier"] == "C":
            return _emit(
                "BLOCKED — CONTENT_DOOR_NOT_PROVEN",
                "all changed paths appear to be mechanical content/index data, but the current canonical content door is not proven healthy: main's latest full test run reports missing Smart Note capture/registry entries and stale generated indexes",
                "repair the canonical capture → registry → index/sync path and make its schema, collision, registry-drift, and index-freshness checks green before routing note-only work through that door; do not substitute scorecard ceremony or merge a mega-PR to hide the content-door defect",
            )

        author_seat = consensus.author_seat_of(body)
        if not author_seat:
            return _emit("BLOCKED — AUTHOR_SEAT_MISSING",
                         "the PR body does not declare its authoring seat",
                         "add exactly one explicit 'Seat: Naya <seat>' declaration to the PR body")

        comments = consensus.api_get(f"/repos/{repo}/issues/{number}/comments", token)
        reviews = consensus.api_get(f"/repos/{repo}/pulls/{number}/reviews", token)
        author_login = ((pr.get("user") or {}).get("login") or "")
        review_ok, review_detail = _cross_seat_review(reviews, comments, author_login, author_seat)
        if not review_ok:
            return _emit("BLOCKED — DIFFERENT_SEAT_REVIEW_MISSING",
                         review_detail,
                         "have a non-author seat post a matcher-valid approval/review on this PR")

        minimum = 9.5 if tier["tier"] == "A" else 9.0
        ok, score_detail = _scorecard_for_current_head(comments, head, author_seat, minimum)
        if not ok:
            return _emit("BLOCKED — SCORECARD_MISSING_OR_STALE",
                         f"Tier {tier['tier']} requires {minimum:g}/10; {score_detail}",
                         f"post a numeric scorecard >= {minimum:g}/10 from a different declared seat with an explicit head field pinned to current SHA {head}")

        # The existing receipt checker is the source of truth for Evidence
        # heading and URL/SHA/path liveness; don't duplicate its parser.
        os.environ["PR_BODY"] = body
        receipt.URL_CHECK_RESULTS.clear()
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                receipt.main()
        except SystemExit:
            lines = [line.strip() for line in output.getvalue().splitlines() if line.strip()]
            reason = next((line for line in lines if "FAILED:" in line), "Evidence receipt did not pass")
            cure = next((line.replace("Fix: ", "") for line in lines if line.startswith("Fix: ")),
                        "add a ## Evidence section containing at least one live URL, existing commit SHA, or existing repository path and explain what it proves")
            states = [item.get("state") for item in receipt.URL_CHECK_RESULTS.values()]
            if "UNAVAILABLE" in states and "DEAD" not in states:
                details = "; ".join(
                    f"{url}: {item.get('detail')}"
                    for url, item in receipt.URL_CHECK_RESULTS.items()
                    if item.get("state") == "UNAVAILABLE"
                )
                return _emit("ERROR — VERIFICATION_UNAVAILABLE",
                             f"evidence URL check could not complete: {details}",
                             "retry when the URL host/network is reachable; do not change or replace the evidence unless a retry confirms it is dead")
            return _emit("BLOCKED — EVIDENCE_INVALID", reason, cure)

        print(f"UNIFIED PAPERWORK GATE: PASS — Tier {tier['tier']}; {score_detail}; evidence receipt resolves. Declared-seat separation is enforced by repository convention, not cryptographic actor binding.")
        return 0

    except (consensus.GateAPIError, urllib.error.URLError, TimeoutError) as exc:
        return _emit("ERROR — VERIFICATION_UNAVAILABLE",
                     f"GitHub/evidence verification unavailable: {type(exc).__name__}: {exc}",
                     "restore API/network availability and re-run; do not interpret this as a quality failure")
    except Exception as exc:
        return _emit("ERROR — VERIFICATION_UNAVAILABLE",
                     f"unexpected verification error: {type(exc).__name__}: {exc}",
                     "inspect the named integration error, repair the verifier, and re-run; do not bypass the gate")


if __name__ == "__main__":
    raise SystemExit(run())
