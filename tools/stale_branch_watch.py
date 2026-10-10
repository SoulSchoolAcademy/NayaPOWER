#!/usr/bin/env python3
"""Stale-branch watch: report-only. Never deletes.

Uses GraphQL to bulk-fetch every branch head's commit date (~10 calls for
~1,000 branches instead of ~1,000 REST calls). Branches with no commit in
STALE_DAYS and no open PR are reported to #1354 (single comment, updated in
place via marker). Deletion is NEVER automatic — destructive actions are
Shawn's gate.

Stdlib only. Runs weekly via protocol-watchdog.yml.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

MARKER = "<!-- stale-branch-watch -->"
API = "https://api.github.com"
STALE_DAYS = 45
FEED_ISSUE = 1354


def gql(query, variables):
    token = os.environ["GH_TOKEN"]
    req = urllib.request.Request(
        API + "/graphql", method="POST",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json",
                 "User-Agent": "naya-stale-watch/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def rest(path, method="GET", data=None):
    token = os.environ["GH_TOKEN"]
    req = urllib.request.Request(
        API + path, method=method,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "naya-stale-watch/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


BRANCH_Q = """
query($owner:String!, $name:String!, $cursor:String) {
  repository(owner:$owner, name:$name) {
    refs(refPrefix:"refs/heads/", first:100, after:$cursor) {
      pageInfo { hasNextPage endCursor }
      nodes { name target { ... on Commit { committedDate oid } } }
  }
}"""


def main():
    try:
        owner, name = os.environ["GITHUB_REPOSITORY"].split("/")
    except KeyError:
        print("GITHUB_REPOSITORY missing; skipping.")
        return
    cutoff = datetime.now(timezone.utc) - timedelta(days=STALE_DAYS)

    branches = []
    cursor = None
    while True:
        try:
            d = gql(BRANCH_Q, {"owner": owner, "name": name, "cursor": cursor})
        except Exception as e:
            print(f"GraphQL failed ({e}); skipping.")
            return
        refs = d["data"]["repository"]["refs"]
        branches += refs["nodes"]
        if not refs["pageInfo"]["hasNextPage"]:
            break
        cursor = refs["pageInfo"]["endCursor"]

    try:
        open_prs = rest(f"/repos/{owner}/{name}/pulls?state=open&per_page=100")
        active_heads = {pr["head"]["ref"] for pr in open_prs}
    except Exception:
        active_heads = set()

    stale = []
    for b in branches:
        ref = b["name"]
        if ref == "main" or ref in active_heads:
            continue
        try:
            dt = datetime.fromisoformat(
                b["target"]["committedDate"].replace("Z", "+00:00"))
        except (KeyError, TypeError):
            continue
        if dt < cutoff:
            stale.append((ref, dt.date().isoformat()))

    stale.sort(key=lambda x: x[1])
    body = (MARKER + "\n## Stale-branch watch\n"
            f"{len(branches)} branches scanned, {len(stale)} stale "
            f"(no commit in {STALE_DAYS}d, no open PR).\n"
            "Report-only: nothing deleted. Claim or close them before they rot.\n")
    if stale:
        body += "\n" + "\n".join(f"- `{r}` — last commit {d}"
                                 for r, d in stale[:40])
        if len(stale) > 40:
            body += f"\n- …and {len(stale) - 40} more"
    else:
        body += "\nAll clear — no stale branches."

    try:
        comments = rest(f"/repos/{owner}/{name}/issues/{FEED_ISSUE}/comments"
                        f"?per_page=100")
        mine = [c for c in comments if MARKER in (c.get("body") or "")]
        if mine:
            cid = mine[0]["id"]
            rest(f"/repos/{owner}/{name}/issues/comments/{cid}",
                 method="PATCH", data={"body": body})
            print(f"Updated stale-branch report ({len(stale)} stale).")
        else:
            rest(f"/repos/{owner}/{name}/issues/{FEED_ISSUE}/comments",
                 method="POST", data={"body": body})
            print(f"Posted stale-branch report ({len(stale)} stale).")
    except Exception as e:
        print(f"Could not post report ({e}).")


if __name__ == "__main__":
    main()
