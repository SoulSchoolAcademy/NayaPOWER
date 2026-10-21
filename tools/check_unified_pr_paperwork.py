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

import check_merge_consensus as consensus
import check_pr_receipt as receipt
from pr_flow_tier import classify_tier


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
        if not consensus._looks_like_scorecard(body, head):
            continue
        seat = consensus.seat_of(body)
        if not seat or seat == author_seat:
            continue
        score = consensus._score_of(body)
        if score is not None and score >= minimum:
            return True, f"independent scorecard {score:g}/10 from {seat} pins current head {head[:12]}"
    return False, f"no independent numeric scorecard >= {minimum:g}/10 pinned to current head {head[:12]}"


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
        tier = classify_tier(title, paths)
        print(f"Tier: {tier['tier']} — {tier['reason']}")
        print(f"PR: #{number}; current head: {head}")

        if tier["tier"] == "C":
            return _emit(
                "BLOCKED — ROUTE_TO_CONTENT_DOOR",
                "all changed paths appear to be mechanical content/index data; routine content must use the canonical sync/filing path, not a code-merge PR",
                "file through the canonical Smart Note/content door, pass schema + collision + provenance + deterministic-index checks, then record a post-landing spot-check; close this PR only after confirming the content is safely represented",
            )

        author_seat = consensus.author_seat_of(body)
        if not author_seat:
            return _emit("BLOCKED — AUTHOR_SEAT_MISSING",
                         "the PR body does not declare its authoring seat",
                         "add exactly one explicit 'Seat: Naya <seat>' declaration to the PR body")

        # Reuse the canonical matcher and API logic instead of creating a
        # second independent interpretation of seat/review receipt syntax.
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                consensus.run_gate(token, repo, str(number), head)
        except SystemExit:
            detail = output.getvalue().strip().splitlines()
            reason = detail[-1] if detail else "cross-seat review/scorecard matcher rejected the PR"
            if "no review from a seat" in reason.lower():
                return _emit("BLOCKED — DIFFERENT_SEAT_REVIEW_MISSING", reason,
                             "have a non-author seat post a matcher-valid approval/review on this PR")
            if "no scorecard receipt" in reason.lower():
                return _emit("BLOCKED — SCORECARD_MISSING_OR_STALE", reason,
                             "post a numeric scorecard from a different seat pinned to the exact current head SHA")
            return _emit("BLOCKED — CONSENSUS_RECEIPT_INVALID", reason,
                         "repair the specific missing field named above, then run the gate's local self-test before posting")

        comments = consensus.api_get(f"/repos/{repo}/issues/{number}/comments", token)
        minimum = 9.5 if tier["tier"] == "A" else 8.0
        ok, score_detail = _scorecard_for_current_head(comments, head, author_seat, minimum)
        if not ok:
            return _emit("BLOCKED — SCORE_BELOW_TIER_THRESHOLD",
                         f"Tier {tier['tier']} requires {minimum:g}/10; {score_detail}",
                         f"obtain an independent scorecard >= {minimum:g}/10 on the current head SHA {head}")

        # The existing receipt checker is the source of truth for Evidence
        # heading and URL/SHA/path liveness; don't duplicate its parser.
        os.environ["PR_BODY"] = body
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                receipt.main()
        except SystemExit:
            lines = [line.strip() for line in output.getvalue().splitlines() if line.strip()]
            reason = next((line for line in lines if "FAILED:" in line), "Evidence receipt did not pass")
            cure = next((line.replace("Fix: ", "") for line in lines if line.startswith("Fix: ")),
                        "add a ## Evidence section containing at least one live URL, existing commit SHA, or existing repository path and explain what it proves")
            return _emit("BLOCKED — EVIDENCE_INVALID", reason, cure)

        print(f"UNIFIED PAPERWORK GATE: PASS — Tier {tier['tier']}; {score_detail}; evidence receipt resolves.")
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
