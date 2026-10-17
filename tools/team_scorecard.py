#!/usr/bin/env python3
"""Team accountability scorecard — the math on performance.

Runs weekly (protocol-watchdog.yml). Measures the team on GitHub data, no
self-reporting:

  - PRs opened / merged / closed-unmerged (last 7 days)
  - First-time-right % = merged / (merged + closed_unmerged + reverts)
  - Avg hours from open to merge
  - Reverts merged
  - Stale-branch count (from the branch list)

Writes BRAIN/SCORECARD.md to the naya/mission-state branch (no CI burn)
and posts a summary to #1354. Numbers only — no adjectives. If the math
is bad, the math is bad; that is the point.

Stdlib only.
"""
import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone

MARKER = "<!-- team-scorecard -->"
API = "https://api.github.com"
FEED_ISSUE = 1354
STATE_BRANCH = "naya/mission-state"
SCORECARD_PATH = "BRAIN/SCORECARD.md"
WINDOW_DAYS = 7


def rest(path, method="GET", data=None):
    token = os.environ["GH_TOKEN"]
    req = urllib.request.Request(
        API + path, method=method,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "naya-scorecard/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def paged(path):
    token = os.environ["GH_TOKEN"]
    out = []
    url = API + path
    while url:
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "naya-scorecard/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
            out += d if isinstance(d, list) else [d]
            links = r.headers.get("Link", "")
        url = None
        for part in links.split(","):
            if 'rel="next"' in part:
                url = part.split(";")[0].strip().strip("<>")
        if url and len(out) >= 400:
            break
    return out


def main():
    try:
        owner, name = os.environ["GITHUB_REPOSITORY"].split("/")
    except KeyError:
        print("GITHUB_REPOSITORY missing; skipping.")
        return
    since = datetime.now(timezone.utc) - timedelta(days=WINDOW_DAYS)
    week = since.date().isoformat()

    try:
        prs = paged(f"/repos/{owner}/{name}/pulls?state=all&per_page=100")
    except Exception as e:
        print(f"Could not list PRs ({e}); skipping.")
        return
    prs = [p for p in prs
           if p.get("created_at", "")[:10] >= week]

    opened = len(prs)
    merged = sum(1 for p in prs if p.get("merged_at"))
    closed_unmerged = sum(1 for p in prs
                          if p.get("state") == "closed" and not p.get("merged_at"))
    reverts = sum(1 for p in prs
                  if p.get("merged_at")
                  and (p.get("title") or "").lower().startswith("revert"))
    ftr = (100.0 * merged / max(1, merged + closed_unmerged + reverts))

    hours = []
    for p in prs:
        if p.get("merged_at"):
            try:
                s = datetime.fromisoformat(p["created_at"].replace("Z", "+00:00"))
                e = datetime.fromisoformat(p["merged_at"].replace("Z", "+00:00"))
                hours.append((e - s).total_seconds() / 3600)
            except (TypeError, ValueError):
                pass
    avg_h = sum(hours) / len(hours) if hours else 0.0

    body = (MARKER + f"\n## Team scorecard — last {WINDOW_DAYS} days\n"
            f"- PRs opened: **{opened}** · merged: **{merged}** · "
            f"closed unmerged: **{closed_unmerged}** · reverts: **{reverts}**\n"
            f"- **First-time-right: {ftr:.0f}%** "
            f"(merged ÷ (merged + unmerged + reverts))\n"
            f"- Avg open→merge: **{avg_h:.1f}h**\n")
    if ftr < 70:
        body += ("\nFirst-time-right below 70% — the team is reworking more than "
                 "shipping. Find the top failure mode and kill it.")
    elif ftr >= 90:
        body += "\nFirst-time-right at 90%+ — the machine is healthy. Hold the bar."

    # Write the scorecard file to the live branch.
    try:
        cur = rest(f"/repos/{owner}/{name}/contents/{SCORECARD_PATH}"
                   f"?ref={STATE_BRANCH}")
        sha = cur.get("sha")
    except Exception:
        sha = None
    import base64
    full = ("# TEAM SCORECARD\n"
            f"> Week of {week} · generated mechanically, no self-reporting.\n\n"
            + body.replace(MARKER + "\n", "") +
            "\n_First-time-right = merged ÷ (merged + closed-unmerged + reverts)._\n")
    payload = {"message": f"Scorecard week of {week}",
               "content": base64.b64encode(full.encode()).decode(),
               "branch": STATE_BRANCH}
    if sha:
        payload["sha"] = sha
    try:
        rest(f"/repos/{owner}/{name}/contents/{SCORECARD_PATH}",
             method="PUT", data=payload)
        print("Wrote", SCORECARD_PATH)
    except Exception as e:
        print(f"Could not write scorecard ({e}).")

    # Post summary to the feed.
    try:
        comments = rest(f"/repos/{owner}/{name}/issues/{FEED_ISSUE}/comments"
                        f"?per_page=100")
        mine = [c for c in comments if MARKER in (c.get("body") or "")]
        if mine:
            rest(f"/repos/{owner}/{name}/issues/comments/{mine[0]['id']}",
                 method="PATCH", data={"body": body})
        else:
            rest(f"/repos/{owner}/{name}/issues/{FEED_ISSUE}/comments",
                 method="POST", data={"body": body})
        print(f"Posted scorecard: {opened} opened, {merged} merged, FTR {ftr:.0f}%.")
    except Exception as e:
        print(f"Could not post scorecard ({e}).")


if __name__ == "__main__":
    main()
