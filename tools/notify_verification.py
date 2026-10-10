#!/usr/bin/env python3
"""Verification notifications: keep the team feed (#2154) aware of PR verification.

Shawn: "there should be some kind of notification goes out for any agent
goes in to now verify that it's our score it."

Lifecycle events detected from issue_comment webhook payloads:
  1. ASSIGN    - a verifier is assigned to a PR ("assigned to verify")
  2. START     - a verifier begins work ("now verifying")
  3. REVIEW    - a [NAYA N - REVIEW] verdict lands (APPROVED / CHANGES REQUESTED)
  4. SCORECARD - a scorecard names the PR head SHA with a score

Each event posts exactly one notification comment to #2154.

Idempotency: every notification carries a marker <!-- vn:<key> -->.
Existing #2154 comments are scanned for the marker before posting;
a key is never notified twice.

Loop safety: any comment containing <!-- vn: is never treated as an
event (our own notifications can't re-trigger). The workflow also skips
marker-bearing comments. Notification text deliberately avoids the
consensus-gate trigger phrases ("[NAYA N - REVIEW]", "Seat: Naya N",
"## SCORECARD") so notifications can never false-pass the merge gate.

Notify-only. Never merges, never gates, never reviews. The
merge-consensus gate remains the sole authority for merges.

Env (workflow):
  GH_TOKEN          - GitHub token
  GITHUB_REPOSITORY - owner/repo
  ISSUE_NUMBER      - issue/PR number the comment landed on
  IS_PR             - "true" if the comment is on a pull request
  COMMENT_BODY      - the comment text

Local dry-run:
  python3 tools/notify_verification.py --dry-run --body-file /tmp/c.txt \\
      --issue 2201 --is-pr
  (prints detected events and the exact notification text; posts nothing)

Stdlib only.
"""
import json
import os
import re
import sys
import urllib.request

API = "https://api.github.com"
FEED_ISSUE = 2154
MARKER_PREFIX = "<!-- vn:"
UA = "naya-verify-notify/1.0"

SEAT_RE = re.compile(r"naya[\s\-]*([2345])\b", re.I)
REVIEW_RE = re.compile(r"\[NAYA\s*([2345])\s*[-\xb7.]\s*REVIEW\]", re.I)
SCORECARD_HEAD_RE = re.compile(r"\[NAYA\s*([2345])\s*[-\xb7.]\s*SCORECARD\]", re.I)
VERDICT_RE = re.compile(r"\b(APPROVED|CHANGES[_\s]REQUESTED)\b", re.I)
ASSIGN_RE = re.compile(r"assigned to verify", re.I)
START_RE = re.compile(r"\bnow verifying\b", re.I)
SCORECARD_RE = re.compile(r"##\s*SCORECARD|\bSCORECARD\b", re.I)
SCORE_RE = re.compile(r"score\s*[*_:=\s]*(\d+(?:\.\d+)?)", re.I)
PRNUM_RE = re.compile(r"(?:PR|pull request)\s*#?\s*(\d{3,5})", re.I)
SHA40_RE = re.compile(r"\b([0-9a-f]{40})\b")
SHA_CTX_RE = re.compile(r"(?:head(?:\s+sha)?|sha(?:\s+tested)?)\s*[:=]?\s*`?([0-9a-f]{7,40})`?", re.I)
PR_SECTION_RE = re.compile(r"^###\s+PR\s*#(\d+)\b([^\n]*)$", re.I | re.M)


def rest(path, token, method="GET", data=None):
    req = urllib.request.Request(
        API + path, method=method,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def feed_comments(token, repo, pages=3):
    """Recent comments on the team feed #2154 (newest last per page)."""
    out = []
    for page in range(1, pages + 1):
        batch = rest(
            f"/repos/{repo}/issues/{FEED_ISSUE}/comments"
            f"?per_page=100&page={page}", token)
        if not batch:
            break
        out.extend(batch)
    return out


def seat_of(text):
    m = SEAT_RE.search(text or "")
    return f"Naya {m.group(1)}" if m else None


def extract_sha(text):
    m = SHA_CTX_RE.search(text or "")
    if m:
        return m.group(1)
    m = SHA40_RE.search(text or "")
    return m.group(1) if m else None


def extract_score(text):
    m = SCORE_RE.search(text or "")
    return m.group(1) if m else None


def short(sha):
    return sha[:7] if sha else "unknown-sha"


def parse_scorecard_sections(body):
    """Split a scorecard into per-PR sections.

    Returns [{pr, verdict, sha, score}]. Handles both the independent
    format ('### PR #2201 (LIVE-3, SN-0809) - APPROVED' + '**Head SHA:**'
    + '**Score:** 9.2/10') and looser author formats (best effort).
    """
    sections = []
    matches = list(PR_SECTION_RE.finditer(body or ""))
    for i, m in enumerate(matches):
        pr = m.group(1)
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        chunk = body[m.start():end]
        verdict_m = VERDICT_RE.search(m.group(2) + " " + chunk[:200])
        verdict = verdict_m.group(1).upper().replace(" ", "_") if verdict_m else None
        sections.append({
            "pr": pr,
            "verdict": verdict,
            "sha": extract_sha(chunk),
            "score": extract_score(chunk),
        })
    return sections


def detect_events(body, issue_number, is_pr):
    """Return a list of event dicts detected in the comment body."""
    events = []
    if not body or MARKER_PREFIX in body:
        return events  # our own notification; never an event

    if is_pr:
        pr = str(issue_number)
        is_assignment = bool(ASSIGN_RE.search(body))
        if is_assignment:
            seat = seat_of(body) or "Naya ?"
            sha = extract_sha(body)
            events.append({
                "type": "assign", "pr": pr, "seat": seat, "sha": sha,
                "key": f"assign:{pr}:{sha or 'nosha'}",
            })
            # An assignment comment is never a review: its recipe text may
            # mention "[NAYA N · REVIEW]" / "APPROVED" as instructions for
            # the future review. Skip review detection to avoid a false
            # completion event.
        else:
            if START_RE.search(body):
                seat = seat_of(body) or "Naya ?"
                sha = extract_sha(body)
                events.append({
                    "type": "start", "pr": pr, "seat": seat, "sha": sha,
                    "key": f"start:{pr}:{sha or 'nosha'}:{seat.replace(' ', '')}",
                })
            rm = REVIEW_RE.search(body)
            if rm:
                verdict_m = VERDICT_RE.search(body)
                if verdict_m:  # verdict-less reviews (author notes) are not events
                    seat = f"Naya {rm.group(1)}"
                    verdict = verdict_m.group(1).upper().replace(" ", "_")
                    sha = extract_sha(body)
                    events.append({
                        "type": "review", "pr": pr, "seat": seat,
                        "verdict": verdict, "sha": sha,
                        "score": extract_score(body),
                        "key": f"review:{pr}:{sha or 'nosha'}:{verdict}:{seat.replace(' ', '')}",
                    })

    # Scorecards live on the team feed (#2154) but we detect them anywhere
    # except inside our own notifications.
    if SCORECARD_RE.search(body) or SCORECARD_HEAD_RE.search(body):
        for sec in parse_scorecard_sections(body):
            if not sec["verdict"] and not sec["score"]:
                continue
            scorer_m = SCORECARD_HEAD_RE.search(body)
            scorer = f"Naya {scorer_m.group(1)}" if scorer_m else (seat_of(body) or "Naya ?")
            events.append({
                "type": "scorecard", "pr": sec["pr"], "seat": scorer,
                "verdict": sec["verdict"], "sha": sec["sha"],
                "score": sec["score"],
                "key": f"score:{sec['pr']}:{sec['sha'] or 'nosha'}:{scorer.replace(' ', '')}",
            })
    return events


def render(event, score_lookup=None):
    """Build (marker, body) for an event notification."""
    t = event["type"]
    if t == "assign":
        key = event["key"]
        body = (f"{MARKER_PREFIX}{key}-->\n"
                f"🔍 **Verification assigned** — {event['seat']} → "
                f"PR #{event['pr']} (head `{short(event['sha'])}`)")
    elif t == "start":
        key = event["key"]
        body = (f"{MARKER_PREFIX}{key}-->\n"
                f"🔍 {event['seat']} **started verification** of "
                f"PR #{event['pr']} (head `{short(event['sha'])}`)")
    elif t == "review":
        key = event["key"]
        emoji = "✅" if event["verdict"] == "APPROVED" else "🔁"
        score = event["score"]
        if not score and score_lookup:
            score = score_lookup(event["pr"], event["sha"])
        score_line = f"Score: {score}/10" if score else "Score: pending"
        body = (f"{MARKER_PREFIX}{key}-->\n"
                f"{emoji} {event['seat']} **verified** PR #{event['pr']} "
                f"(head `{short(event['sha'])}`): **{event['verdict']}**\n"
                f"{score_line}")
    elif t == "scorecard":
        key = event["key"]
        verdict = f": **{event['verdict']}**" if event["verdict"] else ""
        score = f"**{event['score']}/10**" if event["score"] else "no score parsed"
        body = (f"{MARKER_PREFIX}{key}-->\n"
                f"📊 Scorecard from {event['seat']} for PR #{event['pr']} "
                f"(head `{short(event['sha'])}`){verdict} — {score}")
    else:
        raise ValueError(t)
    return key, body


def already_notified(comments, key):
    marker = f"{MARKER_PREFIX}{key}-->"
    return any(marker in (c.get("body") or "") for c in comments)


def find_review_comment(comments, pr, sha):
    """Find our review notification for a PR+SHA to patch its score line."""
    prefix = f"{MARKER_PREFIX}review:{pr}:{sha}:" if sha else None
    for c in comments:
        b = c.get("body") or ""
        if prefix and b.startswith(prefix):
            return c
        if not sha and f"{MARKER_PREFIX}review:{pr}:nosha:" in b:
            return c
    return None


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args

    def arg(name):
        return args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else None

    if dry_run:
        body_file = arg("--body-file")
        body = open(body_file).read() if body_file else (arg("--body") or "")
        issue_number = arg("--issue") or "0"
        is_pr = (arg("--is-pr") or "true").lower() == "true"
        print(f"--- dry run: issue #{issue_number} (is_pr={is_pr}) ---")
        events = detect_events(body, issue_number, is_pr)
        if not events:
            print("no events detected")
            return
        for e in events:
            key, text = render(e)
            print(f"[{e['type']}] key={key}")
            print(text)
            print("-" * 50)
        return

    token = os.environ.get("GH_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    issue_number = os.environ.get("ISSUE_NUMBER", "")
    is_pr = os.environ.get("IS_PR", "").lower() == "true"
    body = os.environ.get("COMMENT_BODY", "")
    if not (token and repo and issue_number):
        print("missing GH_TOKEN/GITHUB_REPOSITORY/ISSUE_NUMBER; skipping.")
        return

    events = detect_events(body, issue_number, is_pr)
    if not events:
        print("no verification events detected; nothing to do.")
        return

    comments = feed_comments(token, repo)

    def score_lookup(pr, sha):
        # A scorecard for the same PR+SHA may already be on the feed.
        for c in comments:
            b = c.get("body") or ""
            if MARKER_PREFIX in b:
                continue
            for sec in parse_scorecard_sections(b):
                if sec["pr"] == str(pr) and sec["score"]:
                    if not sha or not sec["sha"] or sec["sha"].startswith(sha[:7]) or sha.startswith(sec["sha"][:7]):
                        return sec["score"]
        return None

    for event in events:
        key, text = render(event, score_lookup)
        if already_notified(comments, key):
            print(f"already notified: {key}")
            continue

        if event["type"] == "scorecard" and event["score"]:
            # Fold the score into the existing review notification when present.
            rc = find_review_comment(comments, event["pr"], event["sha"])
            if rc and "Score: pending" in (rc.get("body") or ""):
                new_body = rc["body"].replace(
                    "Score: pending", f"Score: {event['score']}/10", 1)
                rest(f"/repos/{repo}/issues/comments/{rc['id']}",
                     token, method="PATCH", data={"body": new_body})
                print(f"patched review notification with score: {key}")
                continue

        rest(f"/repos/{repo}/issues/{FEED_ISSUE}/comments",
             token, method="POST", data={"body": text})
        print(f"notified: {key}")


if __name__ == "__main__":
    main()
