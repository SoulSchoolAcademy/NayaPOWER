#!/usr/bin/env python3
"""Actions budget watch: early-warning gauge for the CI-minutes budget.

Sums workflow-run wall-clock minutes over the last 30 days (Linux 1x basis;
Windows/macOS runs are rare here — noted, not multiplied) and posts a burn
gauge to #1354 (single comment, updated in place via marker).

This is an approximation for trend-watching, not billing. The real meter is
GitHub Settings > Billing. If the projection crosses the monthly budget,
the team throttles PR churn before CI dies — because when CI minutes die,
work stops completely.

Stdlib only. Runs weekly via protocol-watchdog.yml.
"""
import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone

MARKER = "<!-- actions-budget-watch -->"
API = "https://api.github.com"
FEED_ISSUE = 1354
MONTHLY_BUDGET = 2500  # Shawn's number; Settings > Billing is the real meter


def rest(path):
    token = os.environ["GH_TOKEN"]
    req = urllib.request.Request(
        API + path,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "naya-budget-watch/1.0"})
    out = []
    while True:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
            out += d.get("workflow_runs", [])
            links = r.headers.get("Link", "")
        nxt = None
        for part in links.split(","):
            if 'rel="next"' in part:
                nxt = part.split(";")[0].strip().strip("<>")
        if not nxt or not nxt.startswith(API):
            break
        req = urllib.request.Request(
            nxt, headers={"Authorization": f"Bearer {token}",
                          "Accept": "application/vnd.github+json",
                          "User-Agent": "naya-budget-watch/1.0"})
        if len(out) >= 500:
            break
    return out


def post(owner, name, body):
    token = os.environ["GH_TOKEN"]
    def call(path, method="GET", data=None):
        req = urllib.request.Request(
            API + path, method=method,
            data=json.dumps(data).encode() if data is not None else None,
            headers={"Authorization": f"Bearer {token}",
                     "Accept": "application/vnd.github+json",
                     "User-Agent": "naya-budget-watch/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    comments = call(f"/repos/{owner}/{name}/issues/{FEED_ISSUE}/comments"
                    f"?per_page=100")
    mine = [c for c in comments if MARKER in (c.get("body") or "")]
    if mine:
        call(f"/repos/{owner}/{name}/issues/comments/{mine[0]['id']}",
             method="PATCH", data={"body": body})
    else:
        call(f"/repos/{owner}/{name}/issues/{FEED_ISSUE}/comments",
             method="POST", data={"body": body})


def main():
    try:
        owner, name = os.environ["GITHUB_REPOSITORY"].split("/")
    except KeyError:
        print("GITHUB_REPOSITORY missing; skipping.")
        return
    since = datetime.now(timezone.utc) - timedelta(days=30)
    try:
        runs = rest(f"/repos/{owner}/{name}/actions/runs"
                    f"?created=%3E{since.date().isoformat()}&per_page=100")
    except Exception as e:
        print(f"Could not list runs ({e}); skipping.")
        return

    minutes = 0.0
    counted = 0
    for r in runs:
        try:
            s = datetime.fromisoformat(r["run_started_at"].replace("Z", "+00:00"))
            e = datetime.fromisoformat(r["updated_at"].replace("Z", "+00:00"))
            minutes += max(0.0, (e - s).total_seconds() / 60)
            counted += 1
        except (KeyError, TypeError, ValueError):
            continue

    daily = minutes / 30
    projected = daily * 30
    pct = 100 * projected / MONTHLY_BUDGET
    status = "OK" if pct < 70 else ("WATCH" if pct < 100 else "OVER BUDGET")
    body = (MARKER + "\n## Actions budget watch\n"
            f"Last 30d: **{counted} runs, ~{minutes:.0f} CI minutes** "
            f"(~{daily:.0f}/day, Linux 1x basis).\n"
            f"Monthly budget: {MONTHLY_BUDGET} min. Projected burn: "
            f"~{projected:.0f} min (**{pct:.0f}%**) — **{status}**.\n")
    if status == "OVER BUDGET":
        body += ("\nProjected to EXCEED budget. Throttle now: batch changes, "
                 "fewer PRs, no ritual re-runs. When minutes die, CI dies, "
                 "work stops.")
    elif status == "WATCH":
        body += ("\nBurn is high. Every PR push costs minutes — make each one "
                 "count.")
    body += "\n_Approximation for trend-watching; the real meter is Settings > Billing._"
    try:
        post(owner, name, body)
        print(f"Posted budget gauge: {counted} runs, ~{minutes:.0f} min, {status}.")
    except Exception as e:
        print(f"Could not post gauge ({e}).")


if __name__ == "__main__":
    main()
