#!/usr/bin/env python3
"""Receipt gate: a PR without live evidence is not done.

Reads the PR body from PR_BODY. Requires a `## Evidence` section containing
at least one VERIFIED artifact handle:
  - URL (http/https)      -> must resolve (status < 400)
  - 40-char git SHA       -> must exist in this repo (git cat-file -e)
  - repo path             -> must exist at HEAD (backtick-quoted or bare)

Exit 0 = receipt valid. Exit 1 = fail with a plain-words reason.
Stdlib only. No network except the URL liveness checks.
"""
import os
import re
import subprocess
import sys
import urllib.request

TIMEOUT = 15


def fail(msg):
    print(f"RECEIPT GATE FAILED: {msg}")
    print("Fix: add a `## Evidence` section to the PR body with at least one")
    print("live artifact handle — a link that resolves, a commit SHA that exists,")
    print("or a repo path that exists — plus one line saying what it proves.")
    sys.exit(1)


def check_url(url):
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "naya-receipt-gate/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status < 400
    except Exception:
        # Some hosts reject HEAD; retry with GET (headers only read).
        try:
            req = urllib.request.Request(url, method="GET",
                                         headers={"User-Agent": "naya-receipt-gate/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                r.read(1)
                return r.status < 400
        except Exception:
            return False


def git_exists(sha):
    return subprocess.run(["git", "cat-file", "-e", sha],
                          capture_output=True).returncode == 0


def path_exists(path):
    return subprocess.run(["git", "cat-file", "-e", f"HEAD:{path}"],
                          capture_output=True).returncode == 0


def main():
    body = os.environ.get("PR_BODY") or ""
    m = re.search(r"^##\s+evidence\s*$", body, re.IGNORECASE | re.MULTILINE)
    if not m:
        fail("no `## Evidence` section in the PR body.")
    section = body[m.end():]
    # Cut at the next ## heading.
    nxt = re.search(r"^##\s+", section, re.MULTILINE)
    if nxt:
        section = section[:nxt.start()]

    urls = re.findall(r"https?://[^\s\)>\]]+", section)
    shas = re.findall(r"\b[0-9a-f]{40}\b", section)
    paths = [p for p in re.findall(r"`([^`]+)`", section)
             if "/" in p or p.endswith((".md", ".py", ".yml", ".yaml", ".json"))]

    verified = []
    dead = []
    for u in dict.fromkeys(urls):
        if "localhost" in u or "127.0.0.1" in u:
            continue
        (verified if check_url(u) else dead).append(f"url:{u}")
    for s in dict.fromkeys(shas):
        (verified if git_exists(s) else dead).append(f"sha:{s[:8]}")
    for p in dict.fromkeys(paths):
        p = p.strip()
        (verified if path_exists(p) else dead).append(f"path:{p}")

    if dead:
        fail(f"{len(dead)} dead artifact handle(s): {', '.join(dead[:5])}. "
             "Evidence that does not resolve is not evidence.")
    if not verified:
        fail("`## Evidence` exists but contains no verifiable artifact handle "
             "(live URL, existing SHA, or existing repo path).")
    print(f"Receipt OK: {len(verified)} live handle(s): "
          f"{', '.join(verified[:5])}")


if __name__ == "__main__":
    main()
