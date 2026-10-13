#!/usr/bin/env python3
"""Merge-consensus gate: no merge without cross-seat review + scorecard receipt.

Shawn's doctrine: the protocol IS the authorization. No human click in the
pipeline. This gate is the authorization.

Reads from env:
  GH_TOKEN      - GitHub token (workflow secrets.GITHUB_TOKEN)
  REPO          - owner/repo
  PR_NUMBER     - pull request number
  HEAD_SHA      - PR head SHA under test

Seat identity: the team shares one GitHub account, so GitHub logins cannot
distinguish seats. Seats are identified by signed tags instead:
  - PR body must declare:  Seat: Naya N
  - Reviewer posts a comment:  [NAYA M · REVIEW] ... APPROVED ...
    (the team's IV sign-out verdict format — "## VERDICT: MERGE RECOMMENDED"
    with a seat tag — is also accepted as a review)
  - Scorecard receipt:  ## SCORECARD ... head: <sha> ... Seat: Naya K ...
    (the team's "Honest scorecard: 9.4/10" format is also accepted,
    provided it names the exact head SHA and a seat tag)
Author seat, reviewer seat, and scorer seat: reviewer and scorer may be the
same seat, but BOTH must differ from the author seat. (The author cannot
review or score their own work.)

Native GitHub APPROVED reviews from a *different login* than the PR author
also satisfy the review requirement (future-proof for distinct seat accounts).

Scope: the seat-receipt convention started 2026-10-11T16:30:00Z (PR #2352).
PRs opened before that cannot carry seat tags, so the gate SKIPS them with a
clear message instead of failing on a convention that did not exist yet.

Fail-closed, never a traceback: API or unexpected errors exit 1 through
fail() with plain words ("unable to verify consensus: ..."), never a stack
trace. A permanently-red check with a stack trace trains everyone to ignore
red; an honest "unable to verify, re-run may resolve" does not.

Exit 0 = consensus present (or gate not applicable). Exit 1 = fail with a
plain-words reason.
Stdlib only.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

API = "https://api.github.com"
SEAT_RE = re.compile(r"naya\s*([12345])\b", re.I)
# The authoring seat must be an EXPLICIT declaration ("Seat: Naya N"), never
# an incidental mention: PR bodies routinely discuss other seats ("the Naya 1
# judge", "needs Naya 2/3/4 review"), and the first incidental match would
# misattribute authorship (caught by dogfooding on PR #2373, whose body
# mentions Naya 1 before declaring Seat: Naya 5).
AUTHOR_SEAT_RE = re.compile(r"seat\s*:\s*naya\s*([12345])\b", re.I)

# The seat-receipt convention (Seat: Naya N in the PR body, tagged review and
# scorecard comments) was introduced by PR #2352, merged 2026-10-11 16:30:13Z.
# PRs opened before this instant predate the convention.
SEAT_CONVENTION_CUTOFF = "2026-10-11T16:30:00Z"

# Retry tuning: GitHub answers 403 (secondary rate limit) or 429 when the API
# is under pressure — common during merge bursts when dozens of workflow runs
# share one GITHUB_TOKEN. Each page fetch gets up to 5 attempts. A 403/429
# that carries a Retry-After header (or a rate-limit message) is a transient
# limit: honor the header (capped), else exponential backoff. A 403 whose body
# says "Resource not accessible" is a permission problem: fail fast, retries
# cannot help.
_API_MAX_ATTEMPTS = 5
_API_BACKOFF_BASE_S = 1
_API_MAX_WAIT_S = 120


class GateAPIError(Exception):
    """A GitHub API failure, classified for a clean fail-closed message."""


def fail(msg):
    print(f"CONSENSUS GATE FAILED: {msg}")
    sys.exit(1)


def _classify_http_error(e):
    """Classify an HTTPError as ('rate_limit'|'permission'|'error', detail,
    retry_after_seconds_or_None). Reads the response body for GitHub's
    message; never raises."""
    try:
        raw = e.read() or b""
    except Exception:
        raw = b""
    try:
        body_text = raw.decode("utf-8", "replace")
    except Exception:
        body_text = ""
    try:
        msg = json.loads(body_text).get("message", "") if body_text else ""
    except Exception:
        msg = body_text[:200]
    retry_after = None
    try:
        ra = e.headers.get("Retry-After") if e.headers else None
        retry_after = int(ra) if ra else None
    except (TypeError, ValueError):
        retry_after = None
    low = f"{msg} {body_text}".lower()
    if e.code == 429 or (e.code == 403
                         and ("rate limit" in low or retry_after is not None)):
        return "rate_limit", msg or "rate limited", retry_after
    if e.code == 403 and "resource not accessible" in low:
        return "permission", msg or "forbidden", None
    return "error", msg or f"HTTP {e.code}", None


def _fetch_page(url, headers):
    """GET one page. Transient rate limits (403/429) are retried with the
    server's Retry-After (capped) or exponential backoff; permission 403s and
    other failures become GateAPIError immediately. Returns
    (parsed_json, link_header). Never leaks a traceback to the caller."""
    attempt = 0
    while True:
        attempt += 1
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.load(r)
                link = r.headers.get("Link", "")
            return data, link
        except urllib.error.HTTPError as e:
            kind, detail, retry_after = _classify_http_error(e)
            if kind == "rate_limit" and attempt < _API_MAX_ATTEMPTS:
                wait = retry_after if retry_after else \
                    _API_BACKOFF_BASE_S * (2 ** (attempt - 1))
                wait = max(1, min(wait, _API_MAX_WAIT_S))
                print(f"api_get: rate-limited (HTTP {e.code}), waiting {wait}s "
                      f"(attempt {attempt}/{_API_MAX_ATTEMPTS})",
                      file=sys.stderr)
                time.sleep(wait)
                continue
            if kind == "rate_limit":
                raise GateAPIError(
                    f"GitHub API rate-limited after {_API_MAX_ATTEMPTS} "
                    f"attempts ({detail}). Re-run the check; merge bursts "
                    f"exhaust the shared token quota.")
            if kind == "permission":
                raise GateAPIError(
                    f"GitHub API denied access (HTTP 403): {detail}. The "
                    f"workflow's GITHUB_TOKEN lacks permission for this "
                    f"endpoint; retrying will not help.")
            raise GateAPIError(f"GitHub API error (HTTP {e.code}): {detail}")


def api_get(path, token):
    # Follow pagination: list endpoints return up to 30 items per page by
    # default, so gate-invisible reviews/scorecards on busy PRs (>30 comments)
    # would silently fail the gate. Single-object endpoints return a dict
    # and are returned as-is.
    sep = "&" if "?" in path else "?"
    url = API + path + sep + "per_page=100"
    headers = {"Authorization": f"Bearer {token}",
               "Accept": "application/vnd.github+json",
               "User-Agent": "naya-consensus-gate/2.1"}
    items = None
    while url:
        data, link = _fetch_page(url, headers)
        if isinstance(data, list):
            items = (items or []) + data
        else:
            return data
        url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                url = part.split(";")[0].strip().strip("<>")
                break
    return items if items is not None else []


def seat_of(text):
    """Extract 'Naya N' seat tag from text, or None."""
    m = SEAT_RE.search(text or "")
    return f"Naya {m.group(1)}" if m else None


def author_seat_of(body):
    """Extract the authoring seat from an explicit 'Seat: Naya N'
    declaration in the PR body, or None. Incidental seat mentions in prose
    do not count — authorship is a declaration, not a guess."""
    m = AUTHOR_SEAT_RE.search(body or "")
    return f"Naya {m.group(1)}" if m else None


def _looks_like_review(body):
    """True if the comment reads as an approving review: either the tagged
    review incantation, or the team's IV sign-out verdict format."""
    up = (body or "").upper()
    if "[NAYA" in up and "REVIEW" in up and "APPROVED" in up:
        return True
    return "VERDICT" in up and ("MERGE RECOMMENDED" in up or "APPROVED" in up)


def _score_of(body):
    """Extract a numeric score from 'verdict: 9.4', 'scorecard: 9.4/10', or
    '9.4/10' phrasing; None when no score is stated."""
    for pat in (r"verdict:\s*(\d+(?:\.\d+)?)",
                r"scorecard:\s*(\d+(?:\.\d+)?)",
                r"(\d+(?:\.\d+)?)\s*/\s*10"):
        m = re.search(pat, body or "", re.I)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                continue
    return None


def _looks_like_scorecard(body, head_sha):
    """True if the comment is a scorecard receipt for this exact head SHA:
    it must name the head SHA, say 'scorecard' or 'verdict', and carry either
    a merge-approval phrase or a numeric score >= 9.0. The exact-head rule is
    the security property — a receipt for an older head must not green-light
    a newer one — so it is never relaxed."""
    low = (body or "").lower()
    if "scorecard" not in low and "verdict" not in low:
        return False
    if head_sha not in (body or ""):
        return False
    approved = bool(re.search(r"merge\s*:\s*approved|merge\s+recommended",
                             low))
    score = _score_of(body)
    return approved or (score is not None and score >= 9.0)


def run_gate(token, repo, pr_number, head_sha):
    pr = api_get(f"/repos/{repo}/pulls/{pr_number}", token)
    pr_created = pr.get("created_at") or ""
    # The seat-receipt convention did not exist when a pre-cutoff PR was
    # opened; enforcing it retroactively is a stale assertion. Merge under
    # the protocol in force at the time; the human merge lane owns it.
    # (When created_at is unknown, enforce rather than skip: fail closed.)
    if pr_created and pr_created < SEAT_CONVENTION_CUTOFF:
        print(f"CONSENSUS GATE SKIPPED: PR #{pr_number} opened {pr_created}, "
              f"before the seat-receipt convention ({SEAT_CONVENTION_CUTOFF}).")
        return

    pr_author_login = (pr["user"]["login"] or "").lower()
    author_seat = author_seat_of(pr.get("body"))
    if not author_seat:
        fail("PR body must declare the authoring seat ('Seat: Naya N'). "
             "Unattributed work cannot be reviewed. Add the declaration to "
             "the PR body and re-run.")

    # --- Requirement 1: cross-seat review ---
    reviews = api_get(f"/repos/{repo}/pulls/{pr_number}/reviews", token)
    comments = api_get(f"/repos/{repo}/issues/{pr_number}/comments", token)

    reviewer_seat = None
    # Path A: native GitHub approval from a different login.
    for r in reviews:
        if (r.get("state") == "APPROVED"
                and (r["user"]["login"] or "").lower() != pr_author_login):
            reviewer_seat = seat_of(r.get("body")) or "external reviewer"
            break
    # Path B: seat-tagged review comment (incantation or IV verdict format)
    # from a different seat.
    if not reviewer_seat:
        for c in comments:
            body = c.get("body") or ""
            if _looks_like_review(body):
                s = seat_of(body)
                if s and s != author_seat:
                    reviewer_seat = s
                    break
    if not reviewer_seat:
        fail(f"no review from a seat other than the author ({author_seat}). "
             f"Post '[NAYA M · REVIEW] APPROVED' (or an IV verdict comment "
             f"with your seat tag) as a PR comment, or submit a GitHub "
             f"approving review from a different account.")

    # --- Requirement 2: scorecard receipt naming this exact head SHA ---
    scorer_seat = None
    for c in comments:
        body = c.get("body") or ""
        if not _looks_like_scorecard(body, head_sha):
            continue
        s = seat_of(body)
        if s and s != author_seat:
            scorer_seat = s
            break
    if not scorer_seat:
        fail(f"no scorecard receipt naming head SHA {head_sha[:10]} from a seat "
             f"other than the author ({author_seat}). Post '## SCORECARD' (or "
             f"'Honest scorecard: <score>/10') with the exact head SHA, a "
             f"merge verdict or score >= 9.0, and your seat tag, as a PR "
             f"comment.")

    print(f"CONSENSUS GATE PASSED: author {author_seat}, "
          f"reviewer {reviewer_seat}, scorer {scorer_seat}, head {head_sha[:10]}.")


def main():
    token = os.environ.get("GH_TOKEN") or ""
    repo = os.environ.get("REPO") or ""
    pr_number = os.environ.get("PR_NUMBER") or ""
    head_sha = os.environ.get("HEAD_SHA") or ""
    if not (token and repo and pr_number and head_sha):
        fail("missing GH_TOKEN/REPO/PR_NUMBER/HEAD_SHA in environment.")
    try:
        run_gate(token, repo, pr_number, head_sha)
    except GateAPIError as e:
        # Fail closed (unverified consensus == no consensus) but say so
        # plainly: a transient API error is not a missing review.
        fail(f"unable to verify consensus: {e}")
    except Exception as e:  # never a traceback on the check
        fail(f"unable to verify consensus: unexpected "
             f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
