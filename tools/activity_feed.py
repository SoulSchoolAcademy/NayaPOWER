#!/usr/bin/env python3
"""Update ACTIVITY-FEED.md from recent repo events.

Reads the watermark (last successful run) from the feed file header,
queries commits / PRs / workflow runs since then, prepends new entries
(newest first), caps the feed, and writes the new watermark.

Only stdlib + `gh` CLI. Safe to run on a schedule; no-ops when empty.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = "SoulSchoolAcademy/NayaPOWER"
FEED = Path("ACTIVITY-FEED.md")
MAX_ENTRIES = 200
OWN_COMMIT_MARK = "[skip ci] activity-feed"
OWN_WORKFLOW = "activity-feed.yml"


def gh(*args: str):
    out = subprocess.run(
        ["gh", "api", *args], capture_output=True, text=True, check=True
    ).stdout
    return json.loads(out or "null")


def parse_watermark() -> dt.datetime:
    if not FEED.exists():
        return dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=1)
    m = re.search(r"<!-- watermark: ([^>]+) -->", FEED.read_text())
    if not m:
        return dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=1)
    return dt.datetime.fromisoformat(m.group(1).replace("Z", "+00:00"))


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def collect(since: dt.datetime):
    since_s = since.strftime("%Y-%m-%dT%H:%M:%SZ")
    entries: list[tuple[str, str]] = []  # (timestamp, markdown line)

    # Commits to main
    try:
        commits = gh(f"repos/{REPO}/commits", "--paginate",
                     "-f", "sha=main", "-f", f"since={since_s}", "-f", "per_page=100") or []
        for c in commits:
            msg = (c["commit"]["message"] or "").splitlines()[0][:100]
            if OWN_COMMIT_MARK in msg:
                continue
            ts = c["commit"]["author"]["date"]
            author = (c["author"] or {}).get("login") or c["commit"]["author"]["name"]
            entries.append((ts, f"- \U0001f4dd `{c['sha'][:8]}` {msg} — {author}"))
    except Exception as e:
        print(f"commits query failed: {e}", file=sys.stderr)

    # PRs updated recently
    try:
        pulls = gh(f"repos/{REPO}/pulls", "-f", "state=all",
                   "-f", "sort=updated", "-f", "direction=desc",
                   "-f", "per_page=50") or []
        for p in pulls:
            if p["updated_at"] < since_s:
                break
            ts = p["updated_at"]
            state = "merged \U0001f38c" if p.get("merged_at") else p["state"]
            entries.append((ts, f"- \U0001f500 PR #{p['number']} {state}: {p['title'][:100]}"))
    except Exception as e:
        print(f"pulls query failed: {e}", file=sys.stderr)

    # Workflow runs completed recently
    try:
        runs = (gh(f"repos/{REPO}/actions/runs", "-f", "per_page=50")
                .get("workflow_runs", []))
        for r in runs:
            if r["updated_at"] < since_s or r["status"] != "completed":
                continue
            if r["path"].endswith(OWN_WORKFLOW):
                continue
            icon = {"success": "\u2705", "failure": "\u274c"}.get(r["conclusion"], "\u26aa")
            entries.append((ts := r["updated_at"],
                            f"- {icon} `{r['name'][:40]}` {r['conclusion']} on `{r['head_branch'][:30]}`@{r['head_sha'][:8]}"))
    except Exception as e:
        print(f"runs query failed: {e}", file=sys.stderr)

    entries.sort(key=lambda e: e[0], reverse=True)
    return entries


def main() -> int:
    since = parse_watermark()
    now_s = iso_now()
    entries = collect(since)
    print(f"found {len(entries)} new events since {since}")

    header = (
        "# NayaPOWER Activity Feed\n"
        f"<!-- watermark: {now_s} -->\n"
        "*Auto-updated every 15 minutes. Mirrored by the Hub's Smart Feed room.*\n"
    )
    old_lines: list[str] = []
    if FEED.exists():
        text = FEED.read_text()
        # keep everything after the first three header lines
        parts = text.split("\n", 3)
        old_lines = parts[3].splitlines() if len(parts) > 3 else []

    new_block = [f"\n## {now_s[:13]}:00 UTC"]
    for _, line in entries:
        new_block.append(line)

    # merge: new entries first, then old, cap at MAX_ENTRIES bullets
    bullets: list[str] = []
    for line in new_block + old_lines:
        if line.startswith("- "):
            if len(bullets) >= MAX_ENTRIES:
                break
            bullets.append(line)
        elif line.startswith("## "):
            # keep section headers only if they still have bullets under them
            bullets.append(line)
    # drop trailing headers with no bullets beneath
    cleaned: list[str] = []
    pending_header = None
    for line in bullets:
        if line.startswith("## "):
            pending_header = line
        else:
            if pending_header:
                cleaned.append(pending_header)
                pending_header = None
            cleaned.append(line)

    FEED.write_text(header + "\n".join(cleaned) + "\n")
    print(f"wrote {len([l for l in cleaned if l.startswith('- ')])} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
