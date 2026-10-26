#!/usr/bin/env python3
"""Mission-state freshness watch: is canonical mission state being published?

The one canonical mission state lives on the live/mission-state branch
(ruling 2026-10-26, board comment 6409001863 — the Option C snapshot at
BRAIN/CURRENT-MISSION-STATE.md on the retired naya/mission-state branch is
no longer canonical). The watch tracks STATE-CORE.json, published there by
the state-core tick (single writer, ~15 min cadence). If that file's last
commit is older than STALE_MINUTES, canonical state may have stopped
publishing — post an alert to #3066, the live coordination board (single
comment, updated in place via marker).
(Alert history: originally #1354, then #2793; #2793 was archived
2026-10-25 and its successor is #3066.)

Report-only. Never writes mission state itself.
Stdlib only. Runs via mission-state-watch.yml (every 45 min).
"""
import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone

MARKER = "<!-- mission-state-watch -->"
API = "https://api.github.com"
FEED_ISSUE = 3066
STATE_BRANCH = "live/mission-state"
STATE_PATH = "STATE-CORE.json"
STALE_MINUTES = 90


def rest(path, method="GET", data=None):
    token = os.environ["GH_TOKEN"]
    req = urllib.request.Request(
        API + path, method=method,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "naya-mission-watch/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    try:
        owner, name = os.environ["GITHUB_REPOSITORY"].split("/")
    except KeyError:
        print("GITHUB_REPOSITORY missing; skipping.")
        return
    try:
        commits = rest(f"/repos/{owner}/{name}/commits"
                       f"?path={STATE_PATH}&sha={STATE_BRANCH}&per_page=1")
    except Exception as e:
        print(f"Could not read state history ({e}); skipping.")
        return
    if not commits:
        alert = (f"Mission state missing: no commits for {STATE_PATH} on "
                 f"{STATE_BRANCH}. The canonical state publisher is not "
                 f"publishing state.")
    else:
        try:
            dt = datetime.fromisoformat(
                commits[0]["commit"]["committer"]["date"].replace("Z", "+00:00"))
        except (KeyError, TypeError, ValueError):
            print("Could not parse state date; skipping.")
            return
        age = datetime.now(timezone.utc) - dt
        if age <= timedelta(minutes=STALE_MINUTES):
            print(f"Mission state fresh ({age.total_seconds()/60:.0f} min old).")
            return
        alert = (f"Mission state STALE: {STATE_PATH} on {STATE_BRANCH} "
                 f"last published "
                 f"{age.total_seconds()/60:.0f} min ago "
                 f"(>{STALE_MINUTES} min). The state-core publisher may "
                 f"be down — workers are tuning into old orders.")

    body = MARKER + "\n## Mission-state watch\n" + alert
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
        print("Posted staleness alert.")
    except Exception as e:
        print(f"Could not post alert ({e}).")


if __name__ == "__main__":
    main()
