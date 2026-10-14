#!/usr/bin/env python3
"""Receipt gate: a PR without RELEVANT evidence is not done.

Reads the PR body from PR_BODY. Requires a `## Evidence` section containing
at least one BOUND artifact handle - a handle tied to THIS PR's change set:
  - URL (http/https) -> must resolve (status < 400) AND live under the
                       repo/board domain (github.com/SoulSchoolAcademy/NayaPOWER)
  - 40-char git SHA  -> must be a commit IN this PR: an ancestor of HEAD_SHA
                       that is NOT an ancestor of BASE_SHA (via merge-base)
  - repo path        -> must be in this PR's diff (BASE_SHA...HEAD_SHA)
                       and exist at HEAD_SHA (backtick-quoted or bare)

Plus one prose line saying what the evidence proves (the fail text's promise,
now enforced - liveness without a claim is not evidence either).

Binding context: HEAD_SHA / BASE_SHA env vars, or --head / --base flags.
Without them relevance cannot be verified and the gate REFUSES (fail closed):
it never passes what it cannot justify. (Lane 9, t0710 - the bullseye A/B
proved the old liveness-only check passed example.com links, unrelated SHAs,
and untouched paths with "Receipt OK".)

Exit 0 = receipt valid. Exit 1 = fail with a plain-words reason.
Stdlib only. No network except the URL liveness checks.
"""
import argparse
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

TIMEOUT = 15
REPO_DOMAINS = ("github.com", "www.github.com")
REPO_PATH_PREFIX = "/soulschoolacademy/nayapower/"


def fail(msg):
    print(f"RECEIPT GATE FAILED: {msg}")
    print("Fix: add a `## Evidence` section to the PR body with at least one")
    print("artifact handle BOUND to this PR's change set - a repo/board link")
    print("that resolves, a commit SHA from this PR, or a repo path this PR")
    print("touched - plus one line saying what it proves.")
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


def url_bound(url):
    """A URL is bound iff it points at the repo/board domain."""
    try:
        parts = urllib.parse.urlparse(url)
    except Exception:
        return False
    return (parts.netloc.lower() in REPO_DOMAINS
            and parts.path.lower().startswith(REPO_PATH_PREFIX))


def git_exists(sha):
    return subprocess.run(["git", "cat-file", "-e", sha],
                          capture_output=True).returncode == 0


def sha_bound(sha, head, base):
    """A SHA is bound iff it is a commit in this PR: an ancestor of HEAD_SHA
    that is not an ancestor of BASE_SHA. Returns None if the SHA is dead
    (not in the repo at all)."""
    if not git_exists(sha):
        return None
    in_head = subprocess.run(["git", "merge-base", "--is-ancestor", sha, head],
                             capture_output=True).returncode == 0
    if not in_head:
        return False
    in_base = subprocess.run(["git", "merge-base", "--is-ancestor", sha, base],
                             capture_output=True).returncode == 0
    return not in_base


def pr_diff_paths(head, base):
    p = subprocess.run(["git", "diff", "--name-only", f"{base}...{head}"],
                       capture_output=True, text=True)
    if p.returncode != 0:
        fail(f"cannot compute the PR diff ({base[:8]}...{head[:8]}): "
             f"{p.stderr.strip()[:200]}")
    return set(p.stdout.splitlines())


def path_exists_at(path, head):
    return subprocess.run(["git", "cat-file", "-e", f"{head}:{path}"],
                          capture_output=True).returncode == 0


def has_prose_line(section):
    """At least one line saying what the evidence proves: strip every handle
    token, then require a surviving line with >= 4 word tokens."""
    text = re.sub(r"https?://[^\s\)>\]]+", " ", section)
    text = re.sub(r"\b[0-9a-f]{40}\b", " ", text)
    text = re.sub(r"`[^`]+`", " ", text)
    for line in text.splitlines():
        words = re.findall(r"[A-Za-z]{2,}", line)
        if len(words) >= 4:
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--head", default=os.environ.get("HEAD_SHA") or "")
    ap.add_argument("--base", default=os.environ.get("BASE_SHA") or "")
    args = ap.parse_args()
    head, base = args.head.strip(), args.base.strip()

    body = os.environ.get("PR_BODY") or ""
    # t0702-lane8 root cause: the old ^##\s+evidence\s*$ rejected real
    # headings like "## Evidence (verified at action time)". Word boundary now.
    m = re.search(r"^##\s+evidence\b", body, re.IGNORECASE | re.MULTILINE)
    if not m:
        fail("no `## Evidence` section in the PR body.")
    section = body[m.end():]
    # Cut at the next ## heading.
    nxt = re.search(r"^##\s+", section, re.MULTILINE)
    if nxt:
        section = section[:nxt.start()]

    if not head or not base:
        fail("no PR binding context (HEAD_SHA/BASE_SHA env or --head/--base). "
             "Relevance cannot be verified without the PR's change set - refusing.")
    if not git_exists(head) or not git_exists(base):
        fail(f"binding context not in this repo (head {head[:8]}, "
             f"base {base[:8]}) - refusing.")

    urls = re.findall(r"https?://[^\s\)>\]]+", section)
    shas = re.findall(r"\b[0-9a-f]{40}\b", section)
    paths = [p for p in re.findall(r"`([^`]+)`", section)
             if "/" in p or p.endswith((".md", ".py", ".yml", ".yaml", ".json"))]

    bound, unbound, dead = [], [], []
    for u in dict.fromkeys(urls):
        if "localhost" in u or "127.0.0.1" in u:
            continue
        if not check_url(u):
            dead.append(f"url:{u}")
        elif url_bound(u):
            bound.append(f"url:{u}")
        else:
            unbound.append(f"url:{u} (not repo/board domain)")
    for s in dict.fromkeys(shas):
        verdict = sha_bound(s, head, base)
        if verdict is None:
            dead.append(f"sha:{s[:8]}")
        elif verdict:
            bound.append(f"sha:{s[:8]}")
        else:
            unbound.append(f"sha:{s[:8]} (not a commit in this PR)")
    diff_paths = pr_diff_paths(head, base)
    for p in dict.fromkeys(paths):
        p = p.strip()
        if not path_exists_at(p, head):
            dead.append(f"path:{p}")
        elif p in diff_paths:
            bound.append(f"path:{p}")
        else:
            unbound.append(f"path:{p} (not touched by this PR)")

    if dead:
        fail(f"{len(dead)} dead artifact handle(s): {', '.join(dead[:5])}. "
             "Evidence that does not resolve is not evidence.")
    if not bound:
        detail = f" Unbound handles: {', '.join(unbound[:5])}." if unbound else ""
        fail("`## Evidence` has no artifact handle bound to this PR's "
             f"change set ({base[:8]}...{head[:8]}).{detail}")
    if not has_prose_line(section):
        fail("`## Evidence` has bound handles but no prose line saying what "
             "they prove.")

    print(f"Receipt OK: {len(bound)} bound handle(s): "
          f"{', '.join(bound[:5])}")
    if unbound:
        print(f"Note: {len(unbound)} live but unbound handle(s) not counted: "
              f"{', '.join(unbound[:5])}")


if __name__ == "__main__":
    main()
