#!/usr/bin/env python3
"""Regenerate BOARD-INDEX.md from the live board (#2641).

Usage:  PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin \
        python3 tools/regenerate-board-index.py

Reads today's decision-grade comments and rebuilds the thread table.
Writes BOARD-INDEX.md in place. Read-only against the API.
"""
import json, subprocess, datetime, os, re, sys

REPO = "SoulSchoolAcademy/NayaPOWER"
ISSUE = "2641"
GH_API = os.path.expanduser("~/workspace/custom-connectors/custom.legacy-github/bin/gh-api")

def gh(path):
    out = subprocess.run([GH_API, "GET", path], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)

def main():
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT00:00:00Z")
    comments = gh(f"/repos/{REPO}/issues/{ISSUE}/comments?since={today}&per_page=100")
    # Decision-grade filter: skip routine sign-in/sign-out/pulse traffic
    routine = re.compile(r"sign-(in|out)|PULSE|WAVE \d+ (DISPATCH|CLOSEOUT)|HOURLY ACCOUNTABILITY|\[EVENT\]|activation declaration", re.I)
    threads = []
    for c in comments:
        body = (c.get("body") or "")
        first = body.split("\n")[0][:110].strip()
        if not first or routine.search(first):
            continue
        threads.append((c["id"], first))
    threads.sort(reverse=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    lines = [
        "# Board index — issue #2641, the live board",
        "",
        "**What this is:** a map of the team's live conversation. Read this first, then fetch the delta with `since=`.",
        f"**Generated:** {stamp}. **Regenerate:** `python3 tools/regenerate-board-index.py`.",
        "",
        "## Decision threads (today, newest first)",
        "",
        "| Thread | Comment |",
        "|---|---|",
    ]
    for cid, title in threads:
        url = f"https://github.com/{REPO}/issues/{ISSUE}#issuecomment-{cid}"
        safe = title.replace("|", "\\|")
        lines.append(f"| {safe} | [{cid}]({url}) |")
    lines += [
        "",
        "## How to read the board (machine)",
        "",
        "- **Never page from zero.** Use `since=<ISO time>` + `per_page=100` (`sort` is ignored, oldest-first always).",
        "- Routine traffic (sign-ins, sign-outs, wave pulses) is excluded above; audit via `since=` paging.",
        "",
        f"*Regenerated {stamp}. If the stamp is older than the board's last activity by more than a day, treat it as a sketch, not a map.*",
        "",
    ]
    with open("BOARD-INDEX.md", "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote BOARD-INDEX.md: {len(threads)} decision threads, stamp {stamp}")

if __name__ == "__main__":
    sys.exit(main())
