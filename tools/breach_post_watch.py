#!/usr/bin/env python3
"""Breach-post watch: the L244 watchdog has live machinery now.

L244 — "Normalization of deviance is not authorization": when standing
instructions require a breach post, it must be posted. Until this script,
no machinery in the tree detected a required-but-missing breach post
(the #2423 relay merge-watch skip was caught by a human, not a gate).

This extends the protocol-watchdog lane (one watcher, never a second):
it scans merges to main in the last WINDOW_DAYS for the machine-readable
breach-post catalog, checks the venue issue (#2175, the coordination
board) for a matching post marker, and POSTS the breach flag itself when
the post is missing.

BEHAVIOR TABLE
-------------
Trigger                 Signal                                            Key
invalid-authority       a revert PR naming invalid merge authority, or   invalid-authority:<N>
                        a merged PR carrying an invalid-authority
                        adjudication in title/body/comments
protocol-breach         a PR merged to main with no literal               protocol-breach:<N>
                        `## Evidence` section in its body and no
                        recorded exception (the normalization-of-
                        deviance class: ~17 prior silent merges)
silent-override         a main-branch commit in the window not           silent-override:<sha7>
                        attributable to any merged PR (direct push)

Rules:
  - Event WITH a matching post marker  -> silent (no flag).
  - Event WITHOUT a marker             -> FLAG; the flag comment carries
    the marker, so the next run stays silent (idempotent).
  - API failure                        -> plain words "unable to verify"
    on stdout and exit 1. Never a silent green.
  - Report-only: never merges, never reverts, never blocks, never edits
    PRs. The flag IS the breach post the standing instruction required.

Known limitations (fail-safe direction, report-only cost):
  - Rebase-merged PRs leave intermediate main commits with no `(#N)`
    marker; if the repo ever rebase-merges, those read as silent-override.
  - Exception text past a PR's first 100 comments is missed -> false
    flag (a human closes it; the marker then silences future runs).

A post marker for key K is the literal string `breach-post:<K>`
anywhere in a #2175 comment body.

Stdlib only. Runs via protocol-watchdog.yml (breach-posts job).
"""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://api.github.com"
VENUE_ISSUE = 2175
WINDOW_DAYS = 7
MARKER = "<!-- breach-post-watch -->"

EVIDENCE_RE = re.compile(r"^##\s+evidence\s*$", re.MULTILINE | re.IGNORECASE)
# Exception suppression needs BOTH halves (L22: no exception without his
# explicit real-numbered word; L23: his click authorizes nothing). A bare
# "9.5-bar exception" with no attribution, or a bare "Shawn's word" with no
# explicit real number, is precisely the #2325 fraud pattern — it must FLAG.
# The evidence (the real number) must sit near the attribution (±80 chars),
# so distant unrelated numbers cannot launder a claim.
_EXCEPTION_AUTHORITY_RES = [
    re.compile(r"shawn'?s (explicit )?(word|exception|approval)", re.I),
    re.compile(r"director'?s (explicit )?word", re.I),
    re.compile(r"approved by shawn", re.I),
    re.compile(r"shawn explicitly approved", re.I),
]
_EXCEPTION_EVIDENCE_RES = [
    re.compile(r"\b9\.\d+\b"),
    re.compile(r"9\.5[\s-]*bar[\s-]*exception", re.I),
]
_EXCEPTION_WINDOW = 80
_NEGATION_RE = re.compile(r"\b(not|no|never|without|isn'?t|aren'?t|wasn'?t)"
                          r"\b[^.\n]{0,40}", re.I)
INVALID_AUTHORITY_RES = [
    re.compile(r"invalid[-\s_]?delegated[-\s_]?merge[-\s_]?authority", re.I),
    re.compile(r"invalid[-\s_]?merge[-\s_]?authority", re.I),
    re.compile(r"law verdict[^.\n]{0,80}0/5 gates", re.I),
]
REVERT_TITLE_RE = re.compile(r"^revert\s+#?(\d+)", re.I)
PR_REF_RES = [
    re.compile(r"^Merge pull request #\d+", re.I),
    re.compile(r"\(#\d+\)"),
]
MARKER_KEY_RE = re.compile(r"breach-post:([a-z0-9][a-z0-9\-:]*)")


# --- pure core (testable without the network) ------------------------------

def has_evidence_section(body):
    return bool(EVIDENCE_RE.search(body or ""))


def has_exception(body, comments_text=""):
    text = _NEGATION_RE.sub("", (body or "") + "\n" + (comments_text or ""))
    for rx in _EXCEPTION_AUTHORITY_RES:
        for m in rx.finditer(text):
            window = text[max(0, m.start() - _EXCEPTION_WINDOW):
                          m.end() + _EXCEPTION_WINDOW]
            if any(ev.search(window) for ev in _EXCEPTION_EVIDENCE_RES):
                return True
    return False


def invalid_authority_hit(title, body, comments_text=""):
    text = " ".join([title or "", body or "", comments_text or ""])
    return any(rx.search(text) for rx in INVALID_AUTHORITY_RES)


def revert_target(title, body):
    """Return the original PR number if this is an invalid-authority revert."""
    m = REVERT_TITLE_RE.match((title or "").strip())
    if m and re.search(r"invalid", (title or "") + " " + (body or ""), re.I):
        return int(m.group(1))
    return None


def classify_pr(pr):
    """Return a list of breach events for one merged PR dict.

    pr keys: number, title, body, merged_at, merge_commit_sha,
             author, comments_text.
    Each event: {"key", "kind", "detail"}.
    """
    events = []
    n = pr["number"]
    title, body = pr.get("title") or "", pr.get("body") or ""
    comments_text = pr.get("comments_text") or ""

    target = revert_target(title, body)
    if target is not None:
        events.append({
            "key": f"invalid-authority:{target}",
            "kind": "invalid-authority",
            "detail": (f"PR #{n} reverts #{target} as an invalid-authority "
                       f"merge (title: {title[:80]!r})."),
        })
    if target is None and invalid_authority_hit(title, body, comments_text):
        # (A revert PR's own adjudication text describes its target, which
        # is already flagged above — no second event for the revert itself.)
        events.append({
            "key": f"invalid-authority:{n}",
            "kind": "invalid-authority",
            "detail": (f"PR #{n} carries an invalid-authority adjudication "
                       f"(title: {title[:80]!r})."),
        })
    if not has_evidence_section(body) and not has_exception(body, comments_text):
        events.append({
            "key": f"protocol-breach:{n}",
            "kind": "protocol-breach",
            "detail": (f"PR #{n} {title[:80]!r} merged without a "
                       f"`## Evidence` section and no recorded exception."),
        })
    return events


def commit_attributable_to_pr(message, oid, pr_merge_oids):
    if oid in pr_merge_oids:
        return True
    return any(rx.search(message or "") for rx in PR_REF_RES)


def classify_commit(commit, pr_merge_oids):
    """Return a silent-override event for a direct push, else None.

    commit keys: oid, message.
    """
    oid = commit["oid"]
    if commit_attributable_to_pr(commit.get("message"), oid, pr_merge_oids):
        return None
    return {
        "key": f"silent-override:{oid[:12]}",
        "kind": "silent-override",
        "detail": (f"Commit {oid[:12]} on main is not attributable to any "
                   f"merged PR (direct push; message: "
                   f"{(commit.get('message') or '')[:80]!r})."),
    }


def extract_marker_keys(comment_bodies):
    keys = set()
    for b in comment_bodies:
        keys.update(MARKER_KEY_RE.findall(b or ""))
    return keys


def scan(events, posted_keys):
    """Split events into (flagged, clear) by posted markers."""
    flagged, clear = [], []
    for ev in events:
        (clear if ev["key"] in posted_keys else flagged).append(ev)
    # de-dupe identical keys, keep first
    seen, uniq = set(), []
    for ev in flagged:
        if ev["key"] not in seen:
            seen.add(ev["key"])
            uniq.append(ev)
    return uniq, clear


def render_body(flagged, clear, window_days, scanned_merges, scanned_commits):
    lines = [
        MARKER,
        "## Breach-post watch (L244)",
        f"Scanned {scanned_merges} PR merges + {scanned_commits} main commits "
        f"in the last {window_days} days. "
        f"{len(flagged)} missing breach post(s) flagged, "
        f"{len(clear)} event(s) already on file.",
        "",
        "Report-only: this job never merges, never reverts, never blocks, "
        "never edits PRs. A flagged line carries its post marker; the next "
        "run stays silent once the marker exists.",
    ]
    if flagged:
        lines += ["", "### Missing breach posts"]
        for ev in flagged:
            lines.append(
                f"- <!-- breach-post:{ev['key']} --> **{ev['kind']}** — "
                f"{ev['detail']}")
    else:
        lines += ["", "All clear — every required breach post is on file."]
    return "\n".join(lines) + "\n"


# --- live half ---------------------------------------------------------------

def _req(path, method="GET", data=None, graphql=False):
    token = os.environ["GH_TOKEN"]
    body = json.dumps(data).encode() if data is not None else None
    headers = {"Authorization": f"Bearer {token}",
               "User-Agent": "naya-breach-watch/1.0"}
    if graphql:
        headers["Content-Type"] = "application/json"
    else:
        headers["Accept"] = "application/vnd.github+json"
    req = urllib.request.Request(API + path, method=method, data=body,
                                 headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def gql(query, variables):
    return _req("/graphql", method="POST",
                data={"query": query, "variables": variables}, graphql=True)


MERGED_PRS_Q = """
query($q:String!, $cursor:String) {
  search(query:$q, type:ISSUE, first:100, after:$cursor) {
    pageInfo { hasNextPage endCursor }
    nodes { ... on PullRequest {
      number title body mergedAt
      author { login }
      baseRefName
      mergeCommit { oid }
      comments(first:100) { nodes { body } }
    } }
  }
}"""

MAIN_COMMITS_Q = """
query($owner:String!, $name:String!, $since:GitTimestamp!, $cursor:String) {
  repository(owner:$owner, name:$name) {
    object(expression:"main") { ... on Commit {
      history(first:100, since:$since, after:$cursor) {
        pageInfo { hasNextPage endCursor }
        nodes { oid message committedDate }
      } } } } }"""


def _norm_ts(ts):
    return (ts or "").replace("Z", "+00:00")


def fetch_merged_prs(owner, name, since_iso):
    q = (f"repo:{owner}/{name} is:pr is:merged "
         f"merged:>={since_iso[:10]} base:main")
    prs, cursor = [], None
    while True:
        d = gql(MERGED_PRS_Q, {"q": q, "cursor": cursor})
        nodes = d["data"]["search"]["nodes"]
        for n in nodes:
            if n.get("baseRefName") != "main" or not n.get("mergedAt"):
                continue
            # the search qualifier is date-truncated; post-filter to the
            # exact window (fail-safe direction would be over-covering,
            # but the report header claims the window — keep it honest)
            if _norm_ts(n["mergedAt"]) < since_iso:
                continue
            comments = n.get("comments", {}).get("nodes", [])
            prs.append({
                "number": n["number"],
                "title": n.get("title") or "",
                "body": n.get("body") or "",
                "merged_at": n["mergedAt"],
                "merge_commit_sha": (n.get("mergeCommit") or {}).get("oid"),
                "author": ((n.get("author") or {}).get("login") or ""),
                "comments_text": "\n".join(
                    c.get("body") or "" for c in comments),
            })
        page = d["data"]["search"]["pageInfo"]
        if not page["hasNextPage"]:
            break
        cursor = page["endCursor"]
    return prs


def fetch_main_commits(owner, name, since_iso):
    commits, cursor = [], None
    while True:
        d = gql(MAIN_COMMITS_Q, {"owner": owner, "name": name,
                                 "since": since_iso, "cursor": cursor})
        hist = d["data"]["repository"]["object"]["history"]
        for c in hist["nodes"]:
            commits.append({"oid": c["oid"], "message": c.get("message") or "",
                            "date": c.get("committedDate")})
        if not hist["pageInfo"]["hasNextPage"]:
            break
        cursor = hist["pageInfo"]["endCursor"]
    return commits


def fetch_posted_keys(owner, name):
    keys, page = set(), 1
    while True:
        comments = _req(f"/repos/{owner}/{name}/issues/{VENUE_ISSUE}"
                        f"/comments?per_page=100&page={page}")
        if not comments:
            break
        keys.update(extract_marker_keys(c.get("body") for c in comments))
        if len(comments) < 100:
            break
        page += 1
    return keys


def find_marker_comment(owner, name):
    """Find the watchdog's own report comment, searching all pages.

    #2175 turns over dozens of comments per hour; the report comment
    is almost never on the first page. A first-page-only search would
    POST a duplicate every run.
    """
    page = 1
    while True:
        comments = _req(f"/repos/{owner}/{name}/issues/{VENUE_ISSUE}"
                        f"/comments?per_page=100&page={page}")
        if not comments:
            return None
        for c in comments:
            if MARKER in (c.get("body") or ""):
                return c["id"]
        if len(comments) < 100:
            return None
        page += 1


def upsert_report(owner, name, body):
    cid = find_marker_comment(owner, name)
    if cid:
        _req(f"/repos/{owner}/{name}/issues/comments/{cid}",
             method="PATCH", data={"body": body})
        print(f"Updated breach-post report (comment {cid}).")
    else:
        _req(f"/repos/{owner}/{name}/issues/{VENUE_ISSUE}/comments",
             method="POST", data={"body": body})
        print("Posted breach-post report.")


def fail_closed(reason):
    print(f"BREACH-POST WATCH: unable to verify — {reason}")
    sys.exit(1)


def main():
    try:
        owner, name = os.environ["GITHUB_REPOSITORY"].split("/")
    except KeyError:
        fail_closed("GITHUB_REPOSITORY missing.")
    since = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)
    since_iso = since.isoformat()

    try:
        prs = fetch_merged_prs(owner, name, since_iso)
        commits = fetch_main_commits(owner, name, since_iso)
        posted = fetch_posted_keys(owner, name)
    except Exception as e:
        fail_closed(f"GitHub API error: {e}")

    events = []
    for pr in prs:
        events.extend(classify_pr(pr))
    pr_merge_oids = {p["merge_commit_sha"] for p in prs
                     if p.get("merge_commit_sha")}
    for c in commits:
        ev = classify_commit(c, pr_merge_oids)
        if ev:
            events.append(ev)

    flagged, clear = scan(events, posted)
    body = render_body(flagged, clear, WINDOW_DAYS, len(prs), len(commits))
    try:
        upsert_report(owner, name, body)
    except Exception as e:
        fail_closed(f"could not post the report: {e}")
    print(f"Done: {len(flagged)} flagged, {len(clear)} already on file.")


if __name__ == "__main__":
    main()
