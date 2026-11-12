#!/usr/bin/env python3
"""Duplicate-work watch (advisory): warn when another open PR touches the same files.

Compares this PR's changed files against other open PRs to main. If overlap
is found, posts (or skips, if already posted) a single comment naming the
overlapping PRs. NEVER fails the build — information, not bureaucracy.

Stdlib only. Uses GH_TOKEN (the Actions token is fine: 1,000/hr/repo).
"""
import json
import os
import subprocess
import sys
import urllib.request

MARKER = "<!-- overlap-watch -->"
API = "https://api.github.com"


def api(path, method="GET", data=None):
    token = os.environ["GH_TOKEN"]
    req = urllib.request.Request(
        API + path, method=method,
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "User-Agent": "naya-overlap-watch/1.0"})
    out = []
    while True:
        with urllib.request.urlopen(req, timeout=30) as r:
            page = json.load(r)
            out += page if isinstance(page, list) else [page]
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
                          "User-Agent": "naya-overlap-watch/1.0"})
    return out


def main():
    try:
        repo = os.environ["GITHUB_REPOSITORY"]
        pr_num = int(os.environ["PR_NUMBER"])
        base = os.environ.get("BASE_SHA", "")
        head = os.environ.get("HEAD_SHA", "")
    except (KeyError, ValueError) as e:
        print(f"Missing env: {e}; skipping.")
        return

    mine = set()
    if base and head:
        out = subprocess.run(["git", "diff", "--name-only", f"{base}...{head}"],
                             capture_output=True, text=True)
        mine = set(out.stdout.split())
    if not mine:
        print("No changed files; nothing to compare.")
        return

    try:
        prs = api(f"/repos/{repo}/pulls?state=open&base=main&per_page=30")
    except Exception as e:
        print(f"Could not list PRs ({e}); advisory skipped.")
        return

    hits = []
    for pr in prs:
        n = pr["number"]
        if n == pr_num:
            continue
        try:
            files = api(f"/repos/{repo}/pulls/{n}/files?per_page=100")
        except Exception:
            continue
        theirs = {f["filename"] for f in files}
        common = mine & theirs
        if common:
            hits.append((n, pr.get("title", ""), sorted(common)[:8]))

    if not hits:
        print("No overlapping open PRs.")
        return

    try:
        comments = api(f"/repos/{repo}/issues/{pr_num}/comments?per_page=100")
    except Exception as e:
        print(f"Could not read comments ({e}); skipping post.")
        return
    if any(MARKER in (c.get("body") or "") for c in comments):
        print("Overlap warning already posted; skipping.")
        return

    lines = [MARKER, "## Duplicate-work watch",
             "These open PRs touch the same files as this one — check you are "
             "not solving the same problem twice:", ""]
    for n, title, files in hits:
        lines.append(f"- #{n} {title} — `{', '.join(files)}`"
                     + (f" (+{len(files)} more)" if len(files) == 8 else ""))
    try:
        api(f"/repos/{repo}/issues/{pr_num}/comments", method="POST",
            data={"body": "\n".join(lines)})
        print(f"Posted overlap warning for {len(hits)} PR(s).")
    except Exception as e:
        print(f"Could not post comment ({e}).")


if __name__ == "__main__":
    main()
