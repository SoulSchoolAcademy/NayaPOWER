#!/usr/bin/env python3
"""Mission-state freshness watch: is the director alive?

The canonical mission snapshot lives at BRAIN/CURRENT-MISSION-STATE.md on the
naya/mission-state branch, refreshed by the director ~every 30 min. If the
snapshot's last-verified time is older than STALE_MINUTES, the director may be
down — post an alert to #1354 (single comment, updated in place via marker).

Report-only. Never writes the snapshot itself.
Stdlib only. Runs via protocol-watchdog.yml (add a schedule entry or call it
from the existing weekly job — recommended: every 30 min alongside the ticks).
"""
import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone

MARKER = "<!-- mission-state-watch -->"
API = "https://api.github.com"
FEED_ISSUE = 1354
STATE_BRANCH = "naya/mission-state"
STATE_PATH = "BRAIN/CURRENT-MISSION-STATE.md"
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
        print(f"Could not read snapshot history ({e}); skipping.")
        return
    if not commits:
        alert = (f"Mission snapshot missing: no commits for {STATE_PATH} on "
                 f"{STATE_BRANCH}. The director is not publishing state.")
    else:
        try:
            dt = datetime.fromisoformat(
                commits[0]["commit"]["committer"]["date"].replace("Z", "+00:00"))
        except (KeyError, TypeError, ValueError):
            print("Could not parse snapshot date; skipping.")
            return
        age = datetime.now(timezone.utc) - dt
        if age <= timedelta(minutes=STALE_MINUTES):
            print(f"Mission snapshot fresh ({age.total_seconds()/60:.0f} min old).")
            return
        alert = (f"Mission snapshot STALE: last verified "
                 f"{age.total_seconds()/60:.0f} min ago "
                 f"(>{STALE_MINUTES} min). The director may be down — "
                 f"workers are tuning into old orders.")

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
