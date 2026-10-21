"""Automatic scorecard calculator — input work, get its score and why.

Shawn, 2026-10-08: a calculator that scorecards any output against
prebuilt rubrics, consistently, and tells the Naya what to do next.
Shawn, 2026-10-14: make measurement automatic — "input this, what does
it score and why." This is that calculator.

Usage:
    python3 tools/scorecard.py --input work.json
    cat work.json | python3 tools/scorecard.py
    python3 tools/scorecard.py --input work.json --json   # machine output
    python3 tools/scorecard.py --input work.json \
        --authorize release.json [--json]                 # release path

Exit codes (diagnostic): 0 = advisory SHIP, 1 = FIX/HOLD,
2 = unreadable input (fail-closed). With --authorize: 0 = AUTHORIZED,
1 = REFUSED (plain words, never a traceback), 2 = unreadable input.

Input JSON (every field optional; missing = fail-closed low):
    {
      "title": "what was done, one line",
      "evidence": [{"claim": "...", "ref": "path / SHA / comment id / test name"}],
      "tests": {"ran": true, "passed": 12, "failed": 0, "can_fail": true},
      "verification": {"seat": "Naya Epsilon", "independent": true, "score": 9.5},
      "value": {"human_benefit": "...", "unblocks": "..."},
      "prevention": {"gate": "name of the gate that makes the class impossible",
                     "wired": true},
      "honesty": {"why_not_10": "...", "limits": ["..."]}
    }

Rubric — six criteria, each 0-10 with reasons. Overall = MINIMUM
(the verdict is the minimum gate; a chain is only as strong as its
weakest link). No criterion can rescue another. No word from any seat
raises a score: only evidence does.

Criteria:
  evidence     — bytes, not claims. Refs that a second mind can check.
  verification — a DIFFERENT seat verified it. Self-verification is
                 capped at 3 (the Inviolable), no matter what.
  tests        — ran, can fail, green. A test that cannot fail is theater.
  value        — named human benefit, or unblocks one. Pure activity
                 scores 3: motion is not value.
  prevention   — the gate that makes this whole class of problem
                 impossible, wired in. A fix without prevention is a
                 repeat waiting to happen.
  honesty      — why-not-10 named, limits disclosed. A score without
                 its limits is a wish.

Public use: the rubric is the interface. Anyone can feed it a JSON
description of work and get the same score a Naya would — the math
does not care who asked.

The scorecarding loop (Shawn, 2026-10-14): score the work against what
would make it a 10/10, triple-A. Ask why it is not a 10. The report's
``to_10`` list is the 10 solutions to make it a 10 — implement them,
re-score, repeat for 3 passes. After 3 passes the gate is hard: SHIP
needs >= 9.5 (over nine). Below 9 never ships, even at best effort.
If 3 passes end below the bar, announce the number (e.g. 8.8) and
pass it off for decision with three options + pros/cons (see
tools/decision.py). Pass ``"pass": 1`` (default), 2, or 3 in the input.

Trust root (2026-10-20): the diagnostic report is ADVISORY — it never
authorizes a release. Claimed evidence and claimed verification cap at
8.0 inside score_work, so the diagnostic path cannot SHIP. A release
is authorized only by authorize_release(): reviewer identity resolved
against the seat registry, exact-head binding re-verified at decision
time, evidence refs resolved to bytes by the INTERNAL resolver
(GitHub API + check-runs + review records — no signing key, never a
caller callback), and the required CI/governance checks green at the
exact head. A blind resolver means refusal in plain words ("unable to
verify") — never a guess, never a traceback.
"""

import argparse
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SHIP_BAR = 9.5
FIX_BAR = 8.0
MAX_PASSES = 3
MAX_SOLUTIONS = 10


def _utc_now():
    """ISO-8601 UTC timestamp of right now — the L577 measurement "
    time. Every score the judge computes carries it; the write-path "
    guard (tools/scorecard_guard.py) refuses any report without one."""
    return datetime.datetime.now(
        datetime.timezone.utc).replace(microsecond=0).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def _nonempty(value):
    return isinstance(value, str) and value.strip() != ""


def score_evidence(work):
    """Score evidence references without pretending a caller callback is trusted.

    No canonical authenticated evidence resolver is wired into this module yet.
    Therefore checkable refs can improve the documentation score only; they
    cannot earn the score needed to authorize SHIP. The public scorecard API
    deliberately accepts no verifier callback, because an arbitrary lambda
    supplied by the caller would recreate the trust-boundary bypass.
    """
    evidence = work.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        return 2.0, ["no evidence refs — claims without bytes"]
    refs = [e for e in evidence if isinstance(e, dict) and _nonempty(e.get("ref"))]
    if not refs:
        return 5.0, ["evidence listed but no checkable refs"]
    if len(refs) != len(evidence):
        return 5.0, ["some evidence items lack checkable refs"]
    return 8.0, ["%d evidence refs supplied but not authenticated by an internal trusted resolver; caller refs and callbacks cannot authorize SHIP" % len(refs)]

# F3 (trust root): a caller's claim of independent verification is
# parsed text, not identity — anyone can type {"seat": "Naya Epsilon",
# "independent": true, "score": 10.0}. Until the internal resolver
# verifies the reviewer against the review record (authorize_release),
# claimed verification caps here and is reported as CLAIMED, never as
# verified. Diagnostic code must never print the verified label.
VERIFICATION_CLAIMED_CAP = 8.0
CLAIMED_VERIFICATION_LABEL = "claimed independent verification (unverified)"
VERIFIED_VERIFICATION_LABEL = "verified independent verification"


def score_verification(work):
    """A different seat verified it. Self-verification is capped.

    Claimed independent verification caps at VERIFICATION_CLAIMED_CAP:
    the seat tag is caller-asserted text until the internal evidence
    resolver checks it against a real review record at the exact head
    (the authorize_release path). See VERIFIED_VERIFICATION_LABEL.
    """
    ver = work.get("verification")
    if not isinstance(ver, dict) or not ver:
        return 4.0, ["no verification — unverified work"]
    if not ver.get("independent"):
        return 3.0, ["verifier is the actor (Inviolable) — self-verification capped"]
    seat = ver.get("seat")
    who = seat if _nonempty(seat) else "an unnamed seat"
    score = ver.get("score")
    if isinstance(score, (int, float)) and not isinstance(score, bool):
        return VERIFICATION_CLAIMED_CAP, [
            "%s by %s — reviewer identity not resolver-verified; "
            "claimed score %.1f" % (CLAIMED_VERIFICATION_LABEL, who, score)]
    return 7.0, [
        "%s by %s — reviewer identity not resolver-verified, no score given"
        % (CLAIMED_VERIFICATION_LABEL, who)]


def score_tests(work):
    """Ran, can fail, green. A test that cannot fail is theater."""
    tests = work.get("tests")
    if not isinstance(tests, dict) or not tests.get("ran"):
        return 3.0, ["tests did not run"]
    if not tests.get("can_fail"):
        return 5.0, ["tests ran but cannot fail — theater, not proof"]
    if tests.get("failed", 0):
        return 5.0, ["tests red: %s failed" % tests.get("failed")]
    if not tests.get("passed"):
        return 5.0, ["tests green but zero passed — empty suite"]
    return 10.0, ["tests ran, can fail, %s passed, 0 failed" % tests.get("passed")]


def score_value(work):
    """Named human benefit, or unblocks one. Pure activity scores 3."""
    value = work.get("value")
    if not isinstance(value, dict):
        return 3.0, ["no value named — activity, not value"]
    if _nonempty(value.get("human_benefit")) and _nonempty(value.get("unblocks")):
        return 10.0, ["human benefit named: %s; unblocks: %s"
                      % (value["human_benefit"][:60], value["unblocks"][:60])]
    if _nonempty(value.get("human_benefit")):
        return 9.0, ["human benefit named: %s" % value["human_benefit"][:80]]
    if _nonempty(value.get("unblocks")):
        return 7.0, ["unblocks: %s" % value["unblocks"][:80]]
    return 3.0, ["no human benefit and nothing unblocked — motion, not value"]


def score_prevention(work):
    """The gate that makes this class impossible, wired in."""
    prev = work.get("prevention")
    if not isinstance(prev, dict):
        return 4.0, ["no prevention gate — the class can recur"]
    if _nonempty(prev.get("gate")) and prev.get("wired"):
        return 10.0, ["prevention gate wired: %s" % prev["gate"][:80]]
    if _nonempty(prev.get("gate")):
        return 6.0, ["prevention gate named but not wired: %s" % prev["gate"][:80]]
    return 4.0, ["no prevention gate — the class can recur"]


def score_honesty(work):
    """Why-not-10 named, limits disclosed."""
    hon = work.get("honesty")
    if not isinstance(hon, dict):
        return 3.0, ["no why-not-10, no limits — a score without limits is a wish"]
    has_why = _nonempty(hon.get("why_not_10"))
    limits = hon.get("limits")
    has_limits = isinstance(limits, list) and len(limits) > 0
    if has_why and has_limits:
        return 10.0, ["why-not-10 named, %d limits disclosed" % len(limits)]
    if has_why or has_limits:
        return 6.0, ["half-honest: %s"
                      % ("why-not-10 named, limits missing" if has_why
                         else "limits listed, why-not-10 missing")]
    return 3.0, ["no why-not-10, no limits — a score without limits is a wish"]


CRITERIA = [
    ("evidence", score_evidence),
    ("verification", score_verification),
    ("tests", score_tests),
    ("value", score_value),
    ("prevention", score_prevention),
    ("honesty", score_honesty),
]


# The 10 solutions: what to do to make each criterion a 10, keyed by
# criterion and current score. The report's to_10 list is built from
# these, lowest criterion first, capped at 10 entries.
TO_10 = {
    "evidence": {
        2.0: ["Add checkable evidence refs (path / SHA / comment id / test name) for every claim — no bytes, no score"],
        5.0: ["Give every evidence item a checkable ref, not just a claim"],
        8.0: ["Authenticate the refs through the canonical authenticated evidence resolver — run the release path (--authorize) so the internal resolver resolves every ref to bytes at the exact head; claimed refs alone stay capped at 8.0, and a caller-supplied callback is never the trust boundary"],
    },
    "verification": {
        3.0: ["Get a DIFFERENT seat to verify it — never verify your own work (Inviolable)"],
        4.0: ["Get a different seat to verify it — unverified work cannot ship"],
        7.0: ["Ask the verifier to attach a score"],
        8.0: ["Claimed verification caps at 8.0 — earn verified independent verification through the release path (--authorize): the internal resolver checks the review record, the seat registry and the exact head"],
    },
    "tests": {
        3.0: ["Run the tests"],
        5.0: ["Fix what the test reason says: make tests able to fail, fix red tests, add real assertions"],
    },
    "value": {
        3.0: ["Name the human benefit AND what it unblocks — motion is not value"],
        7.0: ["Name the human benefit, not just what it unblocks"],
        9.0: ["Name what it unblocks, alongside the human benefit"],
    },
    "prevention": {
        4.0: ["Name the gate that makes this whole class impossible, and wire it"],
        6.0: ["Wire the named gate — a named-but-unwired gate does not prevent"],
    },
    "honesty": {
        3.0: ["Write why-not-10 and list the limits"],
        6.0: ["Write the missing half: why-not-10 and the limits list"],
    },
}


def score_work(work):
    """Score a work dict. Returns the full report dict."""
    if not isinstance(work, dict):
        return {
            "title": "",
            "overall": 0.0,
            "verdict": "HOLD",
            "measured_at": _utc_now(),
            "blocking": ["input"],
            "criteria": {"input": {"score": 0.0,
                                   "reasons": ["unreadable input — fail-closed"]}},
            "pass": 1,
            "to_10": ["Provide the work as a JSON object so it can be scored."],
            "next": "Provide the work as a JSON object with evidence, tests, "
                    "verification, value, prevention, honesty.",
        }
    try:
        pass_no = int(work.get("pass", 1))
    except (TypeError, ValueError):
        pass_no = 1
    pass_no = max(1, min(MAX_PASSES, pass_no))
    criteria = {}
    for name, fn in CRITERIA:
        if name == "evidence":
            score, reasons = score_evidence(work)
        else:
            score, reasons = fn(work)
        criteria[name] = {"score": score, "reasons": reasons}
    overall = min(c["score"] for c in criteria.values())
    blocking = [n for n, c in criteria.items() if c["score"] == overall]
    # The 10 solutions: fixes for every sub-10 criterion, lowest first,
    # capped at 10 entries. Implement them, re-score, repeat.
    ranked = sorted(criteria.items(), key=lambda kv: kv[1]["score"])
    to_10 = []
    for name, c in ranked:
        if c["score"] < 10.0:
            to_10.extend(TO_10.get(name, {}).get(c["score"], []))
    to_10 = to_10[:MAX_SOLUTIONS]
    if overall >= SHIP_BAR:
        verdict = "SHIP"
        nxt = ("Advisory only: the diagnostic math clears the bar, but this "
               "report authorizes nothing — a release needs authorize_release "
               "with resolver-verified identity, evidence and receipts.")
    elif overall >= FIX_BAR:
        verdict = "FIX"
        nxt = "Fix the blocking criterion (%s), then re-score." % ", ".join(blocking)
    else:
        verdict = "HOLD"
        nxt = "Do not ship. Lowest criterion (%s) must move first." % ", ".join(blocking)
    if pass_no >= MAX_PASSES and verdict != "SHIP":
        nxt = ("Pass %d of %d done. Announce: got it to %.1f, needs over 9. "
               "Pass off for decision with three options + pros/cons."
               % (MAX_PASSES, MAX_PASSES, overall))
    return {
        "title": work.get("title", ""),
        "overall": overall,
        "verdict": verdict,
        "measured_at": _utc_now(),
        "blocking": blocking,
        "criteria": criteria,
        "pass": pass_no,
        "to_10": to_10,
        "next": nxt,
    }


# ---------------------------------------------------------------------------
# Trust root — release authorization (F1).
#
# score_work() above is diagnostic only: advisory verdict, zero auth,
# instant. authorize_release() below is the ONLY path that can authorize
# a release, and it trusts nothing the caller asserts:
#   (i)   reviewer identity resolves against the seat registry below and
#         differs from the author seat declared in the PR body;
#   (ii)  the receipt names the exact 40-hex head SHA, re-verified
#         against the PR at decision time;
#   (iii) evidence refs resolve to bytes through the INTERNAL resolver
#         (GitHub API + check-runs + review records; NO signing key and
#         never a caller callback);
#   (iv)  the required CI/governance checks are green at the exact head.
# The 8.0 caps lift only inside this path, only for legs the resolver
# actually verified. A blind resolver refuses in plain words.
# ---------------------------------------------------------------------------

# Seat registry — mirrors tools/check_merge_consensus.py (the merge gate
# is canonical; keep the two in sync). The team shares one GitHub login,
# so seats are registry entries, not logins: the numeric seats 1-5 and
# the 12 named area leads (Shawn, 2026-10-11). A free-text string that
# does not name a registry entry is NOT an identity.
_NAMED_SEATS = ("alpha", "beta", "gamma", "delta", "epsilon", "zeta",
                "eta", "theta", "iota", "kappa", "lambda", "mu")
_SEAT_ID = r"(?:([12345])|(" + "|".join(_NAMED_SEATS) + r"))"
SEAT_RE = re.compile(r"naya\s*" + _SEAT_ID + r"\b", re.I)
AUTHOR_SEAT_RE = re.compile(r"seat\s*:\s*naya\s*" + _SEAT_ID + r"\b", re.I)
_SEAT_FULL_RE = re.compile(r"^naya\s*" + _SEAT_ID + r"$", re.I)
FULL_SHA_RE = re.compile(r"[0-9a-f]{40}")


def _normalized_seat(m):
    if m.group(1):
        return "Naya %s" % m.group(1)
    return "Naya " + m.group(2).lower().capitalize()


def seat_of(text):
    """Extract a 'Naya N' seat tag from text, or None (mirror of the
    merge-consensus gate's seat_of)."""
    m = SEAT_RE.search(text or "")
    return _normalized_seat(m) if m else None


def author_seat_of(body):
    """Extract the authoring seat from an explicit 'Seat: Naya N'
    declaration in a PR body, or None. Incidental seat mentions in
    prose do not count — authorship is a declaration, not a guess."""
    m = AUTHOR_SEAT_RE.search(body or "")
    return _normalized_seat(m) if m else None


def resolve_seat(name):
    """Resolve a claimed reviewer identity against the seat registry.

    The WHOLE string must name one registry seat ('Naya Epsilon',
    'Naya 5'); anything else — 'independent', 'Naya Nobody', a sentence
    containing a seat name — resolves to None and cannot authorize.
    """
    if not isinstance(name, str):
        return None
    m = _SEAT_FULL_RE.match(name.strip())
    return _normalized_seat(m) if m else None


def _is_full_sha(value):
    """Exact-head binding shape: the whole string is one 40-char
    lowercase hex SHA. fullmatch (not a $ anchor) so a trailing newline
    or any smuggled suffix fails closed."""
    return isinstance(value, str) and FULL_SHA_RE.fullmatch(value) is not None


# Mention-vs-use hardening — mirrored verbatim in semantics from
# tools/check_merge_consensus.py (Naya Kappa, 2026-10-13): an approval
# counts only when the reviewer USES it as their own verdict, never
# when a comment merely mentions the format (quoted, negated, or
# declared absent), and never alongside an explicit HOLD verdict.
_MENTION_QUOTE_RE = re.compile(r"`[^`\n]*`|\"[^\n\"]*\"|'[^\n']*'|“[^”\n]*”")
_NEGATION_RE = re.compile(
    r"\b(no|not|n't|never|missing|without|lacks?|lacking|absent|"
    r"failed|fails?|unable|deferred|blocked)\b", re.I)
_HOLD_VETO_RE = re.compile(
    r"\b(HOLD|CHANGES?\s+REQUESTED|NEEDS?\s+(?:WORK|CHANGES)|"
    r"DO\s+NOT\s+MERGE|NOT\s+READY)\b", re.I)
_APPROVAL_USE_RE = re.compile(
    r"\[\s*NAYA\b[^\]\n]*\bREVIEW\b[^\]\n]*\]\s*APPROVED\b"
    r"|\bVERDICT\s*:\s*(?:MERGE\s*[:\-]?\s*)?APPROVED\b"
    r"|\bMERGE\s+(?:RECOMMENDED|APPROVED)\b",
    re.I)


def _looks_like_review(body):
    """True only when the text USES an approval as its own verdict."""
    text = body or ""
    if _HOLD_VETO_RE.search(text):
        return False
    cleaned = _MENTION_QUOTE_RE.sub(" ", text)
    for m in _APPROVAL_USE_RE.finditer(cleaned):
        line_start = cleaned.rfind("\n", 0, m.start()) + 1
        if _NEGATION_RE.search(cleaned[line_start:m.start()]):
            continue
        return True
    return False


def _score_of(body):
    """Extract a numeric score from 'verdict: 9.4', 'scorecard: 9.4/10'
    or '9.4/10' phrasing; None when no score is stated."""
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


class ResolverBlind(Exception):
    """The internal evidence resolver could not verify: API failure,
    missing token, unreadable response. Authorization refuses in plain
    words; it never guesses and never tracebacks."""


class EvidenceResolver:
    """Interface of the INTERNAL evidence resolver.

    Production code uses GitHubEvidenceResolver (built from the
    environment). Tests subclass this with canned facts to pin the
    refusal logic. A bare callable is NOT a resolver — passing one
    raises TypeError, the same rule that removed the caller-injected
    evidence_verifier callback from score_work: the caller must never
    be able to supply the thing that vouches for the caller.
    """

    def pr_facts(self, repo, pr_number):
        """-> {"head_sha": str, "tree_sha": str, "author_seat": str|None}
        for the PR right now (decision time). Raises ResolverBlind."""
        raise NotImplementedError

    def path_exists_at(self, repo, path, sha):
        """-> bool: path exists in the tree at sha. Raises ResolverBlind."""
        raise NotImplementedError

    def check_state(self, repo, sha, names):
        """-> {name: "success"|"failure"|"pending"|"missing"} for the
        latest check-run of each name at sha. Raises ResolverBlind."""
        raise NotImplementedError

    def review_record(self, repo, pr_number, reviewer_seat):
        """-> {"found": bool, "score": float|None}: a submitted,
        non-dismissed approval record by reviewer_seat exists (native
        APPROVED review or seat-tagged review comment, mention-vs-use
        rules applied). Raises ResolverBlind."""
        raise NotImplementedError


class GitHubEvidenceResolver(EvidenceResolver):
    """The production resolver. Trust roots are the GitHub API,
    check-runs and review records — the same roots the existing gates
    use — so NO signing key is needed and no Naya waits on one.
    Stdlib only, token from GH_TOKEN or GITHUB_TOKEN."""

    API = "https://api.github.com"
    _MAX_ATTEMPTS = 3

    def __init__(self, token):
        self._token = token

    @classmethod
    def from_env(cls):
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not token:
            raise ResolverBlind(
                "no GitHub token in the environment (GH_TOKEN/GITHUB_TOKEN) "
                "— the internal resolver is blind")
        return cls(token)

    def _get(self, path):
        """GET one API path, following pagination on list endpoints.
        Transient rate limits retry briefly; every other failure is
        ResolverBlind with GitHub's own message. Never raises raw."""
        sep = "&" if "?" in path else "?"
        url = self.API + path + sep + "per_page=100"
        headers = {"Authorization": "Bearer %s" % self._token,
                   "Accept": "application/vnd.github+json",
                   "User-Agent": "naya-scorecard-resolver/1.0"}
        items = None
        while url:
            data, link = self._get_page(url, headers)
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

    def _get_page(self, url, headers):
        attempt = 0
        while True:
            attempt += 1
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=20) as r:
                    return json.load(r), r.headers.get("Link", "")
            except urllib.error.HTTPError as e:
                detail = ""
                try:
                    detail = json.loads(e.read() or b"{}").get("message", "")
                except Exception:
                    detail = ""
                low = detail.lower()
                if (e.code in (403, 429) and "rate limit" in low
                        and attempt < self._MAX_ATTEMPTS):
                    time.sleep(2 ** (attempt - 1))
                    continue
                raise ResolverBlind(
                    "GitHub API error (HTTP %s)%s"
                    % (e.code, (": " + detail) if detail else ""))
            except (urllib.error.URLError, OSError, ValueError) as e:
                raise ResolverBlind(
                    "unable to reach the GitHub API (%s: %s)"
                    % (type(e).__name__, e))

    def pr_facts(self, repo, pr_number):
        pr = self._get("/repos/%s/pulls/%s" % (repo, pr_number))
        if not isinstance(pr, dict) or not isinstance(pr.get("head"), dict):
            raise ResolverBlind("PR #%s response unreadable" % pr_number)
        head_sha = pr["head"].get("sha")
        if not _is_full_sha(head_sha):
            raise ResolverBlind("PR #%s head SHA unreadable" % pr_number)
        commit = self._get("/repos/%s/git/commits/%s" % (repo, head_sha))
        tree_sha = None
        if isinstance(commit, dict) and isinstance(commit.get("tree"), dict):
            tree_sha = commit["tree"].get("sha")
        if not _is_full_sha(tree_sha):
            raise ResolverBlind("tree SHA for head %s unreadable" % head_sha[:10])
        return {"head_sha": head_sha, "tree_sha": tree_sha,
                "author_seat": author_seat_of(pr.get("body"))}

    def path_exists_at(self, repo, path, sha):
        quoted = urllib.parse.quote(path, safe="/")
        try:
            data = self._get("/repos/%s/contents/%s?ref=%s"
                             % (repo, quoted, sha))
        except ResolverBlind as e:
            if "HTTP 404" in str(e):
                return False
            raise
        return isinstance(data, dict) and bool(data.get("sha"))

    def check_state(self, repo, sha, names):
        data = self._get("/repos/%s/commits/%s/check-runs" % (repo, sha))
        runs = data.get("check_runs") if isinstance(data, dict) else None
        if not isinstance(runs, list):
            raise ResolverBlind("check-runs response for %s unreadable"
                                % sha[:10])
        latest = {}
        for run in runs:
            if not isinstance(run, dict):
                continue
            name = run.get("name")
            if name not in names:
                continue
            stamp = run.get("completed_at") or run.get("started_at") or ""
            if name not in latest or stamp >= latest[name][0]:
                latest[name] = (stamp, run)
        state = {}
        for name in names:
            if name not in latest:
                state[name] = "missing"
                continue
            run = latest[name][1]
            if run.get("status") != "completed":
                state[name] = "pending"
            elif run.get("conclusion") == "success":
                state[name] = "success"
            else:
                state[name] = "failure"
        return state

    def review_record(self, repo, pr_number, reviewer_seat):
        reviews = self._get("/repos/%s/pulls/%s/reviews" % (repo, pr_number))
        comments = self._get("/repos/%s/issues/%s/comments" % (repo, pr_number))
        scores = []
        for record in (reviews or []):
            if not isinstance(record, dict):
                continue
            # A dismissed or pending review is not a record; a review
            # that was later dismissed must not authorize anything.
            if record.get("state") not in ("APPROVED", "COMMENTED"):
                continue
            body = record.get("body") or ""
            if seat_of(body) == reviewer_seat and _looks_like_review(body):
                scores.append(_score_of(body))
        for comment in (comments or []):
            if not isinstance(comment, dict):
                continue
            body = comment.get("body") or ""
            if seat_of(body) == reviewer_seat and _looks_like_review(body):
                scores.append(_score_of(body))
        if not scores:
            return {"found": False, "score": None}
        stated = [s for s in scores if s is not None]
        return {"found": True, "score": max(stated) if stated else None}


def _resolve_ref(resolver, repo, ref, facts):
    """One evidence ref resolves to bytes at the decision-time head iff:
    it IS the head or tree SHA (bare, or after a tree/commit/sha label),
    or its first token is a repo path that exists in the tree at the
    head. Anything else — made-up URLs, vague words, abbreviated SHAs —
    does not resolve. Fail closed."""
    if not isinstance(ref, str) or not ref.strip():
        return False
    tokens = ref.strip().split()
    token = tokens[0]
    if _is_full_sha(token):
        return token in (facts["head_sha"], facts["tree_sha"])
    if token.lower() in ("tree", "commit", "sha", "head") and len(tokens) > 1:
        return _is_full_sha(tokens[1]) and tokens[1] in (
            facts["head_sha"], facts["tree_sha"])
    if "/" in token or token.endswith(
            (".py", ".md", ".json", ".yml", ".yaml", ".txt", ".js", ".ts")):
        return bool(resolver.path_exists_at(repo, token, facts["head_sha"]))
    return False


def _refusal(reasons, **fields):
    decision = {"authorized": False, "verdict": "REFUSED",
                "reasons": list(reasons),
                "verification": CLAIMED_VERIFICATION_LABEL}
    decision.update(fields)
    return decision


def authorize_release(report, authorization, resolver=None):
    """Decide whether a release is authorized. Returns a decision dict;
    "authorized" is True only when EVERY leg verifies:

      identity  — reviewer seat resolves against the registry and is
                  not the author seat declared in the PR body;
      head      — the receipt's head SHA is an exact 40-hex SHA and
                  still equals the PR head at decision time;
      evidence  — every offered ref resolves to bytes at that head
                  through the internal resolver (never a callback);
      receipts  — the review record exists (submitted, non-dismissed,
                  seat-matched) and every required check is green at
                  the exact head;
      score     — the authorized overall (diagnostic criteria with the
                  evidence/verification caps lifted ONLY for verified
                  legs) reaches SHIP_BAR.

    Wrong-typed arguments raise TypeError (a programming error). A
    blind resolver refuses in plain words — ResolverBlind and any
    resolver failure become an "unable to verify" refusal, never a
    traceback and never a guess.
    """
    if not isinstance(report, dict) or not isinstance(authorization, dict):
        raise TypeError(
            "authorize_release expects the score_work report dict and an "
            "authorization dict")
    if resolver is not None and not isinstance(resolver, EvidenceResolver):
        raise TypeError(
            "resolver must be the internal EvidenceResolver (or None for "
            "the production GitHub resolver); a caller-supplied callback "
            "cannot authorize a release")

    repo = authorization.get("repo")
    pr_number = authorization.get("pr_number")
    reviewer_raw = authorization.get("reviewer_seat")
    head_sha = authorization.get("head_sha")
    refs = authorization.get("evidence_refs")
    required_checks = authorization.get("required_checks")

    reasons = []
    if not (isinstance(repo, str)
            and re.fullmatch(r"[^/\s]+/[^/\s]+", repo or "")):
        reasons.append(
            "unable to verify: the authorization names no valid repo "
            "(expected owner/name)")
    if not isinstance(pr_number, int) or isinstance(pr_number, bool) \
            or pr_number <= 0:
        reasons.append("unable to verify: the authorization names no valid "
                       "PR number")
    reviewer_seat = resolve_seat(reviewer_raw)
    if reviewer_seat is None:
        reasons.append(
            "reviewer identity does not resolve to a seat registry entry: "
            "%r is not a registered Naya seat — parsed text is not identity"
            % (reviewer_raw,))
    if not _is_full_sha(head_sha):
        reasons.append(
            "the receipt does not name an exact head: the head SHA must be "
            "one 40-character lowercase hex string, nothing more")
        head_sha = None
    if reasons:
        return _refusal(reasons, repo=repo, pr_number=pr_number,
                        head_sha=head_sha, reviewer_seat=reviewer_seat)

    if resolver is None:
        try:
            resolver = GitHubEvidenceResolver.from_env()
        except ResolverBlind as e:
            return _refusal(["unable to verify: %s" % e],
                            repo=repo, pr_number=pr_number,
                            head_sha=head_sha, reviewer_seat=reviewer_seat)

    def _leg(fn):
        """Run one resolver leg; a blind resolver becomes a plain-words
        'unable to verify' reason, never a traceback."""
        try:
            return fn(), None
        except ResolverBlind as e:
            return None, "unable to verify: %s" % e
        except Exception as e:  # resolver defects still fail closed
            return None, ("unable to verify: the evidence resolver failed "
                          "(%s: %s)" % (type(e).__name__, e))

    facts, err = _leg(lambda: resolver.pr_facts(repo, pr_number))
    if err:
        return _refusal([err], repo=repo, pr_number=pr_number,
                        head_sha=head_sha, reviewer_seat=reviewer_seat)
    if not isinstance(facts, dict) \
            or not _is_full_sha(facts.get("head_sha")) \
            or not _is_full_sha(facts.get("tree_sha")):
        return _refusal(
            ["unable to verify: the evidence resolver returned unreadable "
             "PR facts"], repo=repo, pr_number=pr_number,
            head_sha=head_sha, reviewer_seat=reviewer_seat)
    author_seat = facts.get("author_seat")
    if not author_seat:
        reasons.append(
            "the PR body declares no authoring seat ('Seat: Naya N') — "
            "unattributed work cannot be authorized")
    elif reviewer_seat == author_seat:
        reasons.append(
            "reviewer seat %s is the author seat — a seat cannot authorize "
            "its own work (Inviolable)" % reviewer_seat)
    if head_sha != facts["head_sha"]:
        reasons.append(
            "stale receipt: the receipt names head %s but the PR head at "
            "decision time is %s — re-score and re-verify on the current "
            "head" % (head_sha, facts["head_sha"]))

    # --- evidence leg ---
    criteria = {}
    for name, c in (report.get("criteria") or {}).items():
        if isinstance(c, dict) and isinstance(c.get("score"), (int, float)):
            criteria[name] = float(c["score"])
    evidence_score = criteria.get("evidence", 0.0)
    unresolved = []
    if isinstance(refs, list) and refs:
        for ref in refs:
            resolved, err = _leg(
                lambda ref=ref: _resolve_ref(resolver, repo, ref, facts))
            if err:
                reasons.append(err)
                unresolved.append(ref)
            elif not resolved:
                unresolved.append(ref)
    else:
        reasons.append(
            "no evidence refs were offered for resolution — nothing was "
            "authenticated, so the evidence cap stays")
    if unresolved:
        reasons.append(
            "evidence refs did not resolve to bytes at the head: %s"
            % ", ".join(repr(r) for r in unresolved[:5]))
    elif isinstance(refs, list) and refs:
        evidence_score = 10.0

    # --- verification leg (the review record IS the identity proof) ---
    record, err = _leg(
        lambda: resolver.review_record(repo, pr_number, reviewer_seat))
    verification_score = criteria.get("verification", 0.0)
    verification_label = CLAIMED_VERIFICATION_LABEL
    if err:
        reasons.append(err)
        record = None
    if record is not None and not isinstance(record, dict):
        reasons.append("unable to verify: the evidence resolver returned "
                       "an unreadable review record")
        record = None
    if record is not None:
        if not record.get("found"):
            reasons.append(
                "no submitted, non-dismissed review record by %s exists on "
                "PR #%s — claimed verification stays unverified"
                % (reviewer_seat, pr_number))
        else:
            verification_label = VERIFIED_VERIFICATION_LABEL
            stated = record.get("score")
            if stated is not None and stated >= SHIP_BAR:
                verification_score = 10.0
            elif stated is not None:
                verification_score = 8.0
            else:
                verification_score = 7.0

    # --- CI / governance receipts leg ---
    checks_state = {}
    if isinstance(required_checks, list) and required_checks:
        checks_state, err = _leg(
            lambda: resolver.check_state(repo, facts["head_sha"],
                                         list(required_checks)))
        if err:
            reasons.append(err)
            checks_state = {}
        if not isinstance(checks_state, dict):
            reasons.append("unable to verify: the evidence resolver "
                           "returned unreadable check state")
            checks_state = {}
        for name in required_checks:
            if checks_state.get(name) != "success":
                reasons.append(
                    "required check %r is %s at the exact head — CI/"
                    "governance receipts must be green"
                    % (name, checks_state.get(name, "unknown")))
    else:
        reasons.append(
            "no CI/governance receipts were claimed (required_checks is "
            "empty) — authorization names the gates that must be green")

    # --- authorized overall: caps lift only for verified legs ---
    criteria["evidence"] = evidence_score
    criteria["verification"] = verification_score
    overall = min(criteria.values()) if criteria else 0.0
    if not reasons and overall < SHIP_BAR:
        blocking = [n for n, s in criteria.items() if s == overall]
        reasons.append(
            "authorized score %.1f is below the %.1f ship bar (blocking: "
            "%s) — the trust legs verified, the work itself has not earned "
            "release" % (overall, SHIP_BAR, ", ".join(blocking)))

    decision = {
        "authorized": not reasons,
        "verdict": "AUTHORIZED" if not reasons else "REFUSED",
        "repo": repo,
        "pr_number": pr_number,
        "head_sha": facts["head_sha"],
        "author_seat": author_seat,
        "reviewer_seat": reviewer_seat,
        "evidence": {"refs": len(refs) if isinstance(refs, list) else 0,
                     "unresolved": unresolved,
                     "score": evidence_score},
        "verification": verification_label,
        "verification_score": verification_score,
        "checks": checks_state,
        "overall": overall,
        "reasons": reasons if reasons else [
            "identity: %s verified against the seat registry; author is %s"
            % (reviewer_seat, author_seat),
            "head: receipt binds the exact head %s" % facts["head_sha"],
            "evidence: every ref resolved to bytes at the head (score "
            "%.1f)" % evidence_score,
            "%s by %s (score %.1f)"
            % (verification_label, reviewer_seat, verification_score),
            "receipts: required checks green at the exact head: %s"
            % ", ".join(required_checks),
        ],
    }
    return decision


def render_authorization(decision):
    lines = ["Release authorization: %s" % decision["verdict"]]
    if decision.get("reviewer_seat") or decision.get("author_seat"):
        lines.append("  author seat: %s · reviewer seat: %s"
                     % (decision.get("author_seat"),
                        decision.get("reviewer_seat")))
    if decision.get("head_sha"):
        lines.append("  head: %s" % decision["head_sha"])
    if "overall" in decision:
        lines.append("  authorized overall: %.1f/10" % decision["overall"])
    lines.append("  verification: %s" % decision.get(
        "verification", CLAIMED_VERIFICATION_LABEL))
    for reason in decision.get("reasons") or []:
        lines.append("  - %s" % reason)
    return "\n".join(lines) + "\n"


def render_human(report):
    lines = ["Scorecard: %s" % (report.get("title") or "(untitled)")]
    lines.append("Overall: %.1f/10 — %s" % (report["overall"], report["verdict"]))
    lines.append("Pass: %d of %d" % (report.get("pass", 1), MAX_PASSES))
    for name, _ in CRITERIA:
        c = report["criteria"].get(name)
        if c is None:
            continue
        lines.append("  %-12s %4.1f  %s" % (name, c["score"], "; ".join(c["reasons"])))
    if "input" in report["criteria"]:
        c = report["criteria"]["input"]
        lines.append("  %-12s %4.1f  %s" % ("input", c["score"], "; ".join(c["reasons"])))
    lines.append("Blocking: %s" % ", ".join(report["blocking"]))
    to_10 = report.get("to_10") or []
    if to_10:
        lines.append("To reach 10 — implement, re-score, repeat:")
        for i, fix in enumerate(to_10, 1):
            lines.append("  %d. %s" % (i, fix))
    lines.append("Next: %s" % report["next"])
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Automatic scorecard calculator.")
    parser.add_argument("--input", default=None, help="JSON file describing the work (default: stdin)")
    parser.add_argument("--authorize", default=None,
                        help="JSON file with the release authorization claim "
                             "(repo, pr_number, reviewer_seat, head_sha, "
                             "evidence_refs, required_checks). Runs the "
                             "release path: the internal resolver verifies "
                             "every claim; refusal is plain words, exit 1.")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)
    try:
        raw = open(args.input).read() if args.input else sys.stdin.read()
        work = json.loads(raw)
    except (OSError, ValueError):
        report = score_work(None)
        print(render_human(report) if not args.json else json.dumps(report, indent=2))
        return 2
    report = score_work(work)
    # L577: no score renders or writes without measured_at. The guard is
    # the reference integration — every downstream writer does the same.
    try:
        import scorecard_guard
    except ImportError:
        print("L577 REFUSED: the write-path guard (tools/scorecard_guard.py) "
              "is missing — refusing to render a score an unwired path could "
              "leak")
        return 2
    try:
        scorecard_guard.stamp(report)   # no-op: score_work already stamped
        scorecard_guard.guard(report)
    except scorecard_guard.UnmeasuredRefusal as e:
        print("L577 REFUSED: %s" % e)
        return 2
    if not args.authorize:
        print(render_human(report) if not args.json else json.dumps(report, indent=2))
        return 0 if report["verdict"] == "SHIP" else 1
    # Release path. An unreadable authorization claim is a refusal in
    # plain words (exit 1), never a traceback: blind means no.
    try:
        with open(args.authorize) as fh:
            authorization = json.load(fh)
        if not isinstance(authorization, dict):
            raise ValueError("authorization input is not a JSON object")
    except (OSError, ValueError) as e:
        decision = _refusal(
            ["unable to verify: the authorization input is unreadable "
             "(%s)" % e])
        if args.json:
            print(json.dumps({"report": report, "authorization": decision},
                             indent=2))
        else:
            print(render_human(report) + render_authorization(decision))
        return 1
    decision = authorize_release(report, authorization)
    if args.json:
        print(json.dumps({"report": report, "authorization": decision},
                         indent=2))
    else:
        print(render_human(report) + render_authorization(decision))
    return 0 if decision["authorized"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
