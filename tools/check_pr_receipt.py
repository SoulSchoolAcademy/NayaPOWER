#!/usr/bin/env python3
"""Receipt gate: a PR without live evidence is not done.

Reads the PR body from PR_BODY. Requires a `## Evidence` section containing
at least one VERIFIED artifact handle:
  - URL (http/https)      -> must resolve (status < 400)
  - 40-char git SHA       -> must exist in this repo (git cat-file -e)
  - repo path             -> must exist at HEAD (backtick-quoted or bare)

TRAP (do not regress): a backticked BRANCH name (e.g. `naya5/foo`) is parsed
as a repo path and will fail as a dead handle — a branch name is not a path.
Workers must cite the branch head's 40-char SHA or the PR URL instead.

Exit 0 = receipt valid. Exit 1 = fail with a plain-words reason.
Stdlib only. No network except the URL liveness checks.
"""
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

TIMEOUT = 15
# Detailed outcomes let the unified gate distinguish dead evidence from a
# temporary network outage. The legacy boolean contract remains unchanged.
URL_CHECK_RESULTS = {}


def fail(msg):
    print(f"RECEIPT GATE FAILED: {msg}")
    print("Fix: add a `## Evidence` section to the PR body with at least one")
    print("live artifact handle — a link that resolves, a commit SHA that exists,")
    print("or a repo path that exists — plus one line saying what it proves.")
    sys.exit(1)


def check_url(url):
    """Return the legacy boolean while recording LIVE/DEAD/UNAVAILABLE.

    HEAD-rejecting hosts are retried with GET. A confirmed 4xx is dead
    evidence; 5xx and transport failures are verification outages, not proof
    that the artifact itself is invalid.
    """
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "naya-receipt-gate/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            if r.status < 400:
                URL_CHECK_RESULTS[url] = {"state": "LIVE", "detail": f"HEAD {r.status}"}
                return True
    except Exception:
        pass

    # Some hosts reject HEAD; retry with GET (read only one byte).
    req = urllib.request.Request(url, method="GET",
                                 headers={"User-Agent": "naya-receipt-gate/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            r.read(1)
            if r.status < 400:
                URL_CHECK_RESULTS[url] = {"state": "LIVE", "detail": f"GET {r.status}"}
                return True
            if r.status >= 500:
                URL_CHECK_RESULTS[url] = {"state": "UNAVAILABLE", "detail": f"GET {r.status}"}
            else:
                URL_CHECK_RESULTS[url] = {"state": "DEAD", "detail": f"GET {r.status}"}
            return False
    except urllib.error.HTTPError as exc:
        state = "UNAVAILABLE" if exc.code >= 500 or exc.code in {401, 403, 408, 425, 429} else "DEAD"
        URL_CHECK_RESULTS[url] = {"state": state, "detail": f"GET HTTP {exc.code}"}
        return False
    except Exception as exc:
        URL_CHECK_RESULTS[url] = {"state": "UNAVAILABLE", "detail": f"{type(exc).__name__}: {exc}"}
        return False


def git_exists(sha):
    return subprocess.run(["git", "cat-file", "-e", sha],
                          capture_output=True).returncode == 0


def path_exists(path):
    return subprocess.run(["git", "cat-file", "-e", f"HEAD:{path}"],
                          capture_output=True).returncode == 0


def main():
    URL_CHECK_RESULTS.clear()
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

    # Parse-time pre-check (prevention, not just diagnosis): a backticked
    # handle shaped like a branch path that does NOT exist at HEAD is the
    # trap in disguise — it was parsed as a repo path and can only fail
    # downstream as dead. Fire here, with the trap named.
    # Fires ONLY on otherwise-dead handles: real paths resolve via
    # path_exists and skip this check, so no passing evidence becomes failing.
    branch_like = [p for p in dict.fromkeys(paths)
                   if re.fullmatch(r"[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]+)+",
                                   p.strip())
                   and not path_exists(p.strip())]
    if branch_like:
        fail("TRAP: branch-like backticked handle(s) in `## Evidence`: "
             + ", ".join(f"path:{p.strip()}" for p in branch_like[:5])
             + ". TRAP: a backticked branch name (e.g. `naya5/foo`) is parsed "
             "as a repo path and will fail here — a branch name is not a path. "
             "Do not backtick branch names in ## Evidence; cite the branch "
             "head's 40-char SHA or the PR URL instead.")

    verified = []
    dead = []
    unavailable = []
    for u in dict.fromkeys(urls):
        if "localhost" in u or "127.0.0.1" in u:
            continue
        check_url(u)
        state = URL_CHECK_RESULTS.get(u, {}).get("state", "DEAD")
        if state == "LIVE":
            verified.append(f"url:{u}")
        elif state == "UNAVAILABLE":
            unavailable.append(f"url:{u}")
        else:
            dead.append(f"url:{u}")
    for s in dict.fromkeys(shas):
        (verified if git_exists(s) else dead).append(f"sha:{s[:8]}")
    for p in dict.fromkeys(paths):
        p = p.strip()
        (verified if path_exists(p) else dead).append(f"path:{p}")

    if dead:
        fail(f"{len(dead)} dead artifact handle(s): {', '.join(dead[:5])}. "
             "Evidence that does not resolve is not evidence. "
             "TRAP: a backticked branch name (e.g. `naya5/foo`) is parsed as a "
             "repo path and will fail here — a branch name is not a path. "
             "Do not backtick branch names in ## Evidence; cite the branch "
             "head's 40-char SHA or the PR URL instead.")
    if unavailable:
        print("RECEIPT GATE: ERROR — VERIFICATION_UNAVAILABLE")
        print(f"MISSING: live verification for {len(unavailable)} evidence URL(s): {', '.join(unavailable[:5])}")
        print("CURE: retry the evidence check when the host/network or authorization is available; do not relabel an unverified URL as dead. (owner: Gate maintainer)")
        raise SystemExit(2)
    if not verified:
        fail("`## Evidence` exists but contains no verifiable artifact handle "
             "(live URL, existing SHA, or existing repo path).")
    print(f"Receipt OK: {len(verified)} live handle(s): "
          f"{', '.join(verified[:5])}")


if __name__ == "__main__":
    main()
