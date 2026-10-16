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
  - PR body must declare:  Seat: Naya N   (a numeric seat, e.g. "Naya 2",
    or one of the 12 named seats — Alpha..Mu, e.g. "Seat: Naya Epsilon")
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

A transient API failure (rate limit, 5xx, network error) that survives all
retries is NOT a failure of consensus: it exits 2 with a plain-words
"CONSENSUS GATE UNKNOWN" line — re-run, not a FAIL. Genuine problems
(permission denied, missing review, missing scorecard) exit 1.

Exit 0 = consensus present (or gate not applicable). Exit 1 = FAIL with a
plain-words reason. Exit 2 = UNKNOWN (transient API failure — re-run).
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
# The 12 named area leads (Shawn, 2026-10-11): Alpha, Beta, Gamma, Delta,
# Epsilon, Zeta, Eta, Theta, Iota, Kappa, Lambda, Mu. Named seats sign as
# "Naya <Title>" (e.g. "Naya Epsilon"); the legacy numeric seats 1-5 keep
# working exactly as before. One shared id pattern so the author-declaration
# rule and the review/scorecard rules recognize exactly the same seats.
_NAMED_SEATS = ("alpha", "beta", "gamma", "delta", "epsilon", "zeta",
                "eta", "theta", "iota", "kappa", "lambda", "mu")
_SEAT_ID = r"(?:([12345])|(" + "|".join(_NAMED_SEATS) + r"))"
SEAT_RE = re.compile(r"naya\s*" + _SEAT_ID + r"\b", re.I)
# The authoring seat must be an EXPLICIT declaration ("Seat: Naya N"), never
# an incidental mention: PR bodies routinely discuss other seats ("the Naya 1
# judge", "needs Naya 2/3/4 review"), and the first incidental match would
# misattribute authorship (caught by dogfooding on PR #2373, whose body
# mentions Naya 1 before declaring Seat: Naya 5).
AUTHOR_SEAT_RE = re.compile(r"seat\s*:\s*naya\s*" + _SEAT_ID + r"\b", re.I)

# The seat-receipt convention (Seat: Naya N in the PR body, tagged review and
# scorecard comments) was introduced by PR #2352, merged 2026-10-11 16:30:13Z.
# PRs opened before this instant predate the convention.
SEAT_CONVENTION_CUTOFF = "2026-10-11T16:30:00Z"

# Retry tuning: GitHub answers 403 (secondary rate limit) or 429 when the API
# is under pressure — common during merge bursts when dozens of workflow runs
# share one GITHUB_TOKEN. 5xx and plain network errors are transient too.
# Each page fetch gets up to 5 attempts. A 403/429 that carries a Retry-After
# header (or a rate-limit message), a 5xx, or a network error is transient:
# honor the header (capped), else exponential backoff. A 403 whose body
# says "Resource not accessible" is a permission problem: fail fast, retries
# cannot help.
_API_MAX_ATTEMPTS = 5
_API_BACKOFF_BASE_S = 1
_API_MAX_WAIT_S = 120


class GateAPIError(Exception):
    """A GitHub API failure, classified for a clean fail-closed message."""


class TransientAPIError(GateAPIError):
    """A transient GitHub API failure (rate limit, 5xx, network error) that
    survived every retry. The gate is UNKNOWN, not FAILED: re-run the check.
    Subclasses GateAPIError so existing fail-closed handling still catches
    it; main() checks for it first to print the distinct UNKNOWN verdict."""


def fail(msg):
    print(f"CONSENSUS GATE FAILED: {msg}")
    sys.exit(1)


def _classify_http_error(e):
    """Classify an HTTPError as ('transient'|'permission'|'error', detail,
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
        return "transient", "rate-limited: " + (msg or f"HTTP {e.code}"), \
            retry_after
    if 500 <= e.code < 600:
        return "transient", "server error: " + (msg or f"HTTP {e.code}"), \
            retry_after
    if e.code == 403 and "resource not accessible" in low:
        return "permission", msg or "forbidden", None
    return "error", msg or f"HTTP {e.code}", None


def _transient_wait(attempt, retry_after, what):
    """Sleep before the next retry of a transient failure, logging the
    wait to stderr."""
    wait = retry_after if retry_after else \
        _API_BACKOFF_BASE_S * (2 ** (attempt - 1))
    wait = max(1, min(wait, _API_MAX_WAIT_S))
    print(f"api_get: {what}, waiting {wait}s "
          f"(attempt {attempt}/{_API_MAX_ATTEMPTS})", file=sys.stderr)
    time.sleep(wait)


def _fetch_page(url, headers):
    """GET one page. Transient failures (rate-limited 403/429, 5xx, network
    errors) are retried with the server's Retry-After (capped) or exponential
    backoff; on exhaustion they become TransientAPIError (UNKNOWN verdict).
    Permission 403s and other failures become GateAPIError immediately.
    Returns (parsed_json, link_header). Never leaks a traceback to the
    caller."""
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
            if kind == "transient" and attempt < _API_MAX_ATTEMPTS:
                _transient_wait(attempt, retry_after,
                                f"{detail} (HTTP {e.code})")
                continue
            if kind == "transient":
                raise TransientAPIError(
                    f"GitHub API still failing after {_API_MAX_ATTEMPTS} "
                    f"attempts ({detail}). Re-run the check; merge bursts "
                    f"exhaust the shared token quota.")
            if kind == "permission":
                raise GateAPIError(
                    f"GitHub API denied access (HTTP 403): {detail}. The "
                    f"workflow's GITHUB_TOKEN lacks permission for this "
                    f"endpoint; retrying will not help.")
            raise GateAPIError(f"GitHub API error (HTTP {e.code}): {detail}")
        except OSError as e:
            # Network blip, DNS failure, refused connection, timeout, reset:
            # the network moved, not the verdict. (Catches URLError and its
            # bare-OSError cousins like TimeoutError/ConnectionResetError.)
            # Retry, then UNKNOWN.
            detail = f"network error: {e}"
            if attempt < _API_MAX_ATTEMPTS:
                _transient_wait(attempt, None, detail)
                continue
            raise TransientAPIError(
                f"GitHub API unreachable after {_API_MAX_ATTEMPTS} attempts "
                f"({detail}). Re-run the check.")


def api_get(path, token):
    # Full drain: concatenates every page (single-object endpoints return
    # the dict as-is). Kept for callers that need the whole list. The gate's
    # own verdict scans prefer _api_pages with early exit (below).
    items = None
    for data in _api_pages(path, token):
        if isinstance(data, list):
            items = (items or []) + data
        else:
            return data
    return items if items is not None else []


def _api_pages(path, token):
    """Yield one parsed page at a time, following Link: rel="next".

    Single-object endpoints yield their dict once, then stop. Callers with
    existential scans (first hit in page order decides) break out early
    instead of draining every page — same verdict, fewer API calls.
    """
    # List endpoints return up to 30 items per page by default, so
    # gate-invisible reviews/scorecards on busy PRs (>30 comments) would
    # silently fail the gate without per_page=100 + page following.
    sep = "&" if "?" in path else "?"
    url = API + path + sep + "per_page=100"
    headers = {"Authorization": f"Bearer {token}",
               "Accept": "application/vnd.github+json",
               "User-Agent": "naya-consensus-gate/2.1"}
    while url:
        data, link = _fetch_page(url, headers)
        yield data
        url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                url = part.split(";")[0].strip().strip("<>")
                break


def _normalized_seat(m):
    """Normalize a SEAT_RE/AUTHOR_SEAT_RE match to 'Naya <Title>' form:
    numeric seats stay as-is ('Naya 5'); named seats are title-cased
    ('naya epsilon' -> 'Naya Epsilon')."""
    if m.group(1):
        return f"Naya {m.group(1)}"
    return "Naya " + m.group(2).lower().capitalize()


def seat_of(text):
    """Extract 'Naya N' seat tag from text, or None."""
    m = SEAT_RE.search(text or "")
    return _normalized_seat(m) if m else None


def author_seat_of(body):
    """Extract the authoring seat from an explicit 'Seat: Naya N'
    declaration in the PR body, or None. Incidental seat mentions in prose
    do not count — authorship is a declaration, not a guess."""
    m = AUTHOR_SEAT_RE.search(body or "")
    return _normalized_seat(m) if m else None


# --- mention-vs-use hardening (Naya Kappa, 2026-10-13) ---
# An approval keyword counts only when the commenter USES it as their own
# verdict declaration. MENTION contexts never count:
#   (a) the incantation/keywords are quoted (`...`, "...", '...', “…”)
#       — the comment is talking ABOUT the format, not using it;
#   (b) a negation/absence marker (no/not/missing/without/...) sits between
#       the line start and the keyword — the comment says the approval is
#       MISSING, not that it is GIVEN;
#   (c) the comment carries an explicit non-approval verdict (HOLD, CHANGES
#       REQUESTED, NEEDS WORK, DO NOT MERGE, NOT READY) — fail closed: a
#       comment that declares HOLD cannot also be a review approval.
# Convention this encodes: a review declaration is plain text, e.g.
# "[NAYA DELTA · REVIEW] APPROVED" or "VERDICT: MERGE RECOMMENDED".
# A quoted incantation is a mention of the format, never the approval.
_MENTION_QUOTE_RE = re.compile(r"`[^`\n]*`|\"[^\n\"]*\"|'[^\n']*'|“[^”\n]*”")
_NEGATION_RE = re.compile(
    r"\b(no|not|n't|never|missing|without|lacks?|lacking|absent|"
    r"failed|fails?|unable|deferred|blocked)\b", re.I)
_HOLD_VETO_RE = re.compile(
    r"\b(HOLD|CHANGES?\s+REQUESTED|NEEDS?\s+(?:WORK|CHANGES)|"
    r"DO\s+NOT\s+MERGE|NOT\s+READY)\b", re.I)
_APPROVAL_USE_RE = re.compile(
    r"\[\s*NAYA\b[^\]\n]*\bREVIEW\b[^\]\n]*\]\s*APPROVED\b"   # [NAYA X · REVIEW] APPROVED
    r"|\bVERDICT\s*:\s*(?:MERGE\s*[:\-]?\s*)?APPROVED\b"      # VERDICT: APPROVED / VERDICT: merge APPROVED
    r"|\bMERGE\s+(?:RECOMMENDED|APPROVED)\b",                 # MERGE RECOMMENDED / MERGE APPROVED
    re.I)


def _looks_like_review(body):
    """True only when the comment USES an approval keyword as its own
    verdict declaration — never when it merely MENTIONS one (quoted,
    negated, or declared absent), and never when the comment also carries
    an explicit HOLD / non-approval verdict (fail closed)."""
    text = body or ""
    if _HOLD_VETO_RE.search(text):
        return False
    cleaned = _MENTION_QUOTE_RE.sub(" ", text)
    for m in _APPROVAL_USE_RE.finditer(cleaned):
        line_start = cleaned.rfind("\n", 0, m.start()) + 1
        if _NEGATION_RE.search(cleaned[line_start:m.start()]):
            continue  # mention: the approval is described as missing
        return True
    return False


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
    # The PR object is a single-object endpoint: exactly one page.
    pr = next(_api_pages(f"/repos/{repo}/pulls/{pr_number}", token))
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
    # Pages are consumed lazily and fetching stops the moment both an
    # approving non-author review AND a valid scorecard receipt are found.
    # Both scans are existential — the first hit in page order decides —
    # so an unfetched later page can never change the verdict; stopping
    # early only saves API calls (common case: ~2 calls, not full
    # pagination of both endpoints).
    reviewer_seat = None
    for page in _api_pages(f"/repos/{repo}/pulls/{pr_number}/reviews", token):
        # Path A: native GitHub approval from a different login.
        for r in page:
            if (r.get("state") == "APPROVED"
                    and (r["user"]["login"] or "").lower() != pr_author_login):
                reviewer_seat = seat_of(r.get("body")) or "external reviewer"
                break
        if reviewer_seat:
            break

    # --- Requirement 2: scorecard receipt naming this exact head SHA ---
    # (scanned on the same comment pages as Path B, stopping when both
    # the reviewer and the scorer are known)
    scorer_seat = None
    for page in _api_pages(f"/repos/{repo}/issues/{pr_number}/comments",
                           token):
        for c in page:
            body = c.get("body") or ""
            # Path B: seat-tagged review comment (incantation or IV verdict
            # format) from a different seat — only if Path A found nothing.
            if reviewer_seat is None and _looks_like_review(body):
                s = seat_of(body)
                if s and s != author_seat:
                    reviewer_seat = s
            if scorer_seat is None and _looks_like_scorecard(body, head_sha):
                s = seat_of(body)
                if s and s != author_seat:
                    scorer_seat = s
            if reviewer_seat and scorer_seat:
                break
        if reviewer_seat and scorer_seat:
            break
    if not reviewer_seat:
        fail(f"no review from a seat other than the author ({author_seat}). "
             f"Post '[NAYA M · REVIEW] APPROVED' (or an IV verdict comment "
             f"with your seat tag) as a PR comment, or submit a GitHub "
             f"approving review from a different account.")
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
    except TransientAPIError as e:
        # A transient API failure is not a verdict about consensus. The gate
        # is UNKNOWN: exit 2 (non-zero, but distinct from FAIL's 1) so the
        # log line says UNKNOWN and the fix is a re-run, not an investigation.
        print(f"CONSENSUS GATE UNKNOWN: transient API failure — re-run, "
              f"not a FAIL: {e}")
        sys.exit(2)
    except GateAPIError as e:
        # Fail closed (unverified consensus == no consensus) but say so
        # plainly: a transient API error is not a missing review.
        fail(f"unable to verify consensus: {e}")
    except Exception as e:  # never a traceback on the check
        fail(f"unable to verify consensus: unexpected "
             f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
