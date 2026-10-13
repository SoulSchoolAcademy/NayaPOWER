#!/usr/bin/env python3
"""Merge-consensus gate: no merge without cross-seat review + scorecard receipt.

Shawn's doctrine: the protocol IS the authorization. No human click in the
pipeline. This gate is the authorization.

TIERED REVIEW (Shawn, 2026-10-13 — RATIFIED protocol amendment): review depth
matches blast radius.
  Tier 1 (mechanical): docs/text/data-only or test-only additions. Author
    attests "Tier: 1" in the PR body; the gate verifies the file allowlist
    and that no completed check on the head SHA has failed. No independent
    review. Post-merge 1-in-10 audit; failed audit -> author loses Tier 1
    privilege for 30 days (the audit mechanism is separate from this gate).
  Tier 2 (standard): default. One cross-seat review + scorecard >= 9.5.
  Tier 3 (critical): touches kernel/, BRAIN/01-GOVERNANCE/, auth/permissions,
    production workflows, or migrations — or any seat escalates. Two
    cross-seat reviews (different seats, both different from the author) +
    scorecard >= 9.5 + no failing checks.
Tier determination is mechanical: declared tier, file-path auto-escalation,
and TIER-ESCALATE comments; the highest wins. A declared tier lower than the
files require fails closed naming the offending files and the required tier.

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
review or score their own work.) Tier 3 additionally requires the two
reviewers to be different seats from each other.

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

# --- Tiered review (Shawn, 2026-10-13 — RATIFIED) ---
# Tier declaration: a line starting with "Tier: N" in the PR body. Default 2.
TIER_RE = re.compile(r"^\s*tier\s*:\s*([123])\b", re.I | re.M)
# Escalation: any seat comments TIER-ESCALATE (optionally with a tier number).
TIER_ESCALATE_RE = re.compile(r"tier-escalate\s*:?\s*([123])?", re.I)
# Score threshold for Tier 2/3 numeric scorecards (ratified policy: 9.5).
TIER23_MIN_SCORE = 9.5
# Tier 1 mechanical allowlist: these extensions are never executable content.
_TIER1_EXTS = (".md", ".txt", ".json")
# ...unless they live where bytes execute or govern: workflows run, the kernel
# boots, migrations mutate production.
_TIER1_CODE_DIRS = (".github/", "kernel/", "supabase/")
# Any changed file under these paths (or matching the auth pattern) forces
# Tier 3 no matter what the author declared.
_TIER3_PREFIXES = ("kernel/", "BRAIN/01-GOVERNANCE/", ".github/workflows/",
                   "supabase/migrations/")
_TIER3_AUTH_RE = re.compile(r"(^|/)(auth|permissions?|grants?)(/|_|\.|$)", re.I)
# Test-only additions: brand-new files on test paths, zero source changes.
_TEST_PATH_RE = re.compile(r"(^|/)(tests?|test)/|_test\.|test_|\.test\.", re.I)
# This gate's own check-run name (exact match — never a substring, so a
# maliciously named "my-consensus-check" cannot exclude itself from the
# Tier 1/3 CI-green verification).
_GATE_CHECK_NAME = "team review + scorecard receipt"

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


def _looks_like_scorecard(body, head_sha, min_score=TIER23_MIN_SCORE):
    """True if the comment is a scorecard receipt for this exact head SHA:
    it must name the head SHA, say 'scorecard' or 'verdict', and carry either
    a merge-approval phrase or a numeric score >= min_score. The exact-head
    rule is the security property — a receipt for an older head must not
    green-light a newer one — so it is never relaxed."""
    low = (body or "").lower()
    if "scorecard" not in low and "verdict" not in low:
        return False
    if head_sha not in (body or ""):
        return False
    approved = bool(re.search(r"merge\s*:\s*approved|merge\s+recommended",
                             low))
    score = _score_of(body)
    return approved or (score is not None and score >= min_score)


# --- Tier determination (Shawn, 2026-10-13 — RATIFIED) ---
# Mechanical, never judgment: declared tier, file-path auto-escalation, and
# TIER-ESCALATE comments; the highest wins. Mention-hardening applies exactly
# as for reviews — a quoted or negated "Tier: 1" is talk about the format,
# never the author's attestation.

def _declared_tier(pr_body):
    """Parse the author's 'Tier: N' attestation from the PR body. Default 2:
    a PR that does not attest Tier 1 gets full standard review. Quoted or
    negated mentions do not count."""
    cleaned = _MENTION_QUOTE_RE.sub(" ", pr_body or "")
    for m in TIER_RE.finditer(cleaned):
        line_start = cleaned.rfind("\n", 0, m.start()) + 1
        if _NEGATION_RE.search(cleaned[line_start:m.start()]):
            continue
        n = int(m.group(1))
        if 1 <= n <= 3:
            return n
    return 2


def _escalated_tier(comments):
    """Highest tier claimed by TIER-ESCALATE comments; 0 when none. A bare
    TIER-ESCALATE (no number) means Tier 3 — escalation fails toward safety,
    never toward leniency. Only upward: nothing here can lower a tier."""
    best = 0
    for c in comments:
        cleaned = _MENTION_QUOTE_RE.sub(" ", c.get("body") or "")
        for m in TIER_ESCALATE_RE.finditer(cleaned):
            line_start = cleaned.rfind("\n", 0, m.start()) + 1
            if _NEGATION_RE.search(cleaned[line_start:m.start()]):
                continue
            claimed = int(m.group(1)) if m.group(1) else 3
            best = max(best, claimed)
    return best


def _tier1_file_ok(f):
    """True if a single changed file is Tier-1 eligible: a mechanical
    extension outside code-execution dirs, or a brand-new file on a test
    path (test-only additions). Critical paths are never allowlisted here
    (defense in depth — auto-escalation should have caught them first)."""
    path = f.get("filename") or ""
    if path.startswith(_TIER3_PREFIXES):
        return False
    ext = "." + path.rsplit(".", 1)[-1].lower() if "." in path else ""
    if ext in _TIER1_EXTS and not path.startswith(_TIER1_CODE_DIRS):
        return True
    if (f.get("status") == "added" and _TEST_PATH_RE.search(path)
            and not path.startswith(_TIER3_PREFIXES)):
        return True
    return False


def determine_tier(pr_body, files, comments):
    """Return (tier, explanation). Highest of: declared tier (default 2),
    file-path auto-escalation to 3, comment escalation. Never lower than
    declared."""
    declared = _declared_tier(pr_body)
    auto = declared
    critical_hits = []
    for f in files:
        path = f.get("filename") or ""
        if path.startswith(_TIER3_PREFIXES) or _TIER3_AUTH_RE.search(path):
            auto = 3
            critical_hits.append(path)
    esc = _escalated_tier(comments)
    tier = max(declared, auto, esc)
    parts = [f"declared={declared}"]
    if critical_hits:
        shown = ", ".join(critical_hits[:5])
        more = f" (+{len(critical_hits) - 5} more)" if len(critical_hits) > 5 else ""
        parts.append(f"auto-escalated to 3 by critical path(s): {shown}{more}")
    if esc:
        parts.append(f"comment-escalated to {esc}")
    parts.append(f"final TIER {tier}")
    return tier, "; ".join(parts)


def _collect_reviewers(reviews, comments, pr_author_login, author_seat):
    """All reviewer seats distinct from the author (set). Native GitHub
    approvals from a different login count; seat-tagged review comments
    count when the seat differs from the author. Seats without tags collapse
    into one 'external reviewer' bucket — two untagged approvals do NOT
    count as two distinct seats (documented limitation; tag your seat)."""
    reviewers = set()
    for r in reviews:
        if (r.get("state") == "APPROVED"
                and (r.get("user") or {}).get("login", "").lower()
                != pr_author_login):
            reviewers.add(seat_of(r.get("body")) or "external reviewer")
    for c in comments:
        body = c.get("body") or ""
        if _looks_like_review(body):
            s = seat_of(body)
            if s and s != author_seat:
                reviewers.add(s)
    reviewers.discard(author_seat)
    return reviewers


def check_ci_green(token, repo, head_sha, tier):
    """Tier 1/3 'CI green' verification: no completed check on the head SHA
    — other than this gate itself — may have concluded failure, timed_out,
    cancelled, or action_required. Pending checks do not fail the gate:
    branch protection still blocks the actual merge until required checks
    pass, so there is no merge hole; this gate only refuses to bless a head
    with *known-red* CI."""
    try:
        result = api_get(f"/repos/{repo}/commits/{head_sha}/check-runs",
                         token)
    except GateAPIError as e:
        fail(f"TIER {tier}: unable to verify CI status: {e}")
    runs = result.get("check_runs", []) if isinstance(result, dict) else []
    bad = []
    for cr in runs:
        name = (cr.get("name") or "").strip().lower()
        if name == _GATE_CHECK_NAME:
            continue  # never deadlock on our own verdict
        if cr.get("status") == "completed" and cr.get("conclusion") in (
                "failure", "timed_out", "cancelled", "action_required"):
            bad.append(f"{cr.get('name')} ({cr.get('conclusion')})")
    if bad:
        fail(f"TIER {tier}: CI is not green on head {head_sha[:10]}: "
             f"{'; '.join(bad[:5])}. Fix the failures, then re-run this check.")
    print(f"TIER {tier}: CI verification passed "
          f"({len(runs)} check run(s), none failed).")


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
    pr_body = pr.get("body") or ""
    author_seat = author_seat_of(pr_body)
    if not author_seat:
        fail("PR body must declare the authoring seat ('Seat: Naya N'). "
             "Unattributed work cannot be reviewed. Add the declaration to "
             "the PR body and re-run.")

    reviews = api_get(f"/repos/{repo}/pulls/{pr_number}/reviews", token)
    comments = api_get(f"/repos/{repo}/issues/{pr_number}/comments", token)
    files = api_get(f"/repos/{repo}/pulls/{pr_number}/files", token)
    if not isinstance(files, list):
        files = []

    # --- Requirement 0: tier determination (mechanical; highest wins) ---
    tier, tier_expl = determine_tier(pr_body, files, comments)
    print(f"TIER DETERMINED: {tier} ({tier_expl})")

    # --- Tier 1: mechanical — allowlist + CI, no independent review ---
    if tier == 1:
        bad_files = [f.get("filename") for f in files
                     if not _tier1_file_ok(f)]
        if bad_files:
            shown = ", ".join(bad_files[:10])
            more = (f" (+{len(bad_files) - 10} more)"
                    if len(bad_files) > 10 else "")
            fail(f"TIER MISMATCH: declared Tier 1, but these files require a "
                 f"higher tier: {shown}{more}. Re-declare as Tier 2/3 or split "
                 f"the PR.")
        check_ci_green(token, repo, head_sha, tier)
        print(f"CONSENSUS GATE PASSED (Tier 1 mechanical): author {author_seat}, "
              f"{len(files)} allowlisted file(s); no independent review "
              f"required under the ratified tiered policy.")
        return

    # --- Tier 2/3: independent review(s) + scorecard ---
    reviewers = _collect_reviewers(reviews, comments, pr_author_login,
                                   author_seat)
    need = 2 if tier == 3 else 1
    if len(reviewers) < need:
        fail(f"TIER {tier}: need {need} review(s) from seats other than the "
             f"author ({author_seat}); have {len(reviewers)}. Post "
             f"'[NAYA M · REVIEW] APPROVED' (or an IV verdict comment with "
             f"your seat tag) as a PR comment, or submit a GitHub approving "
             f"review from a different account.")

    scorer_seat = None
    for c in comments:
        body = c.get("body") or ""
        if not _looks_like_scorecard(body, head_sha, TIER23_MIN_SCORE):
            continue
        s = seat_of(body)
        if s and s != author_seat:
            scorer_seat = s
            break
    if not scorer_seat:
        fail(f"TIER {tier}: no scorecard receipt naming head SHA {head_sha[:10]} "
             f"from a seat other than the author ({author_seat}), with score "
             f">= {TIER23_MIN_SCORE}. Post '## SCORECARD' with the exact head "
             f"SHA, a merge verdict or score >= {TIER23_MIN_SCORE}, and your "
             f"seat tag, as a PR comment.")

    if tier == 3:
        check_ci_green(token, repo, head_sha, tier)

    print(f"CONSENSUS GATE PASSED (Tier {tier}): author {author_seat}, "
          f"reviewer(s) {sorted(reviewers)}, scorer {scorer_seat}, "
          f"head {head_sha[:10]}.")


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
