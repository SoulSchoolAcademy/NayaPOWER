#!/usr/bin/env python3
"""Receipt gate: a PR without live evidence is not done.

Reads the PR body from PR_BODY. Requires a `## Evidence` section containing
at least one VERIFIED artifact handle:
  - URL (http/https)      -> must resolve (status < 400)
  - 40-char git SHA       -> must exist in this repo (git cat-file -e)
  - repo path             -> must exist at HEAD (backtick-quoted or bare)

Exit 0 = receipt valid. Exit 1 = FAIL with a plain-words reason.
Exit 2 = UNKNOWN (a transient failure — rate limit, host 5xx, network
blip — stopped verification; re-run, not a FAIL). Genuine failures still
fail loudly. Never a traceback: every failure mode is classified first.
Stdlib only. No network except the URL liveness checks.
"""
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

TIMEOUT = 15

# URL liveness retry tuning: a host under load answers 429/5xx, or the
# network blips once. A dead link must FAIL loudly; a transient blip must
# say UNKNOWN. Classify, retry the transient, then decide.
_URL_MAX_ATTEMPTS = 3
_URL_BACKOFF_BASE_S = 1

_UA = {"User-Agent": "naya-receipt-gate/1.1"}


def fail(msg):
    print(f"RECEIPT GATE FAILED: {msg}")
    print("Fix: add a `## Evidence` section to the PR body with at least one")
    print("live artifact handle — a link that resolves, a commit SHA that exists,")
    print("or a repo path that exists — plus one line saying what it proves.")
    sys.exit(1)


def unknown(msg):
    print(f"RECEIPT GATE UNKNOWN: {msg}")
    print("This is NOT a fail — a transient failure (rate limit, host")
    print("error, network blip) stopped verification. Re-run the check.")
    sys.exit(2)


def _retry_after(headers):
    try:
        ra = headers.get("Retry-After") if headers else None
        return int(ra) if ra else None
    except (TypeError, ValueError):
        return None


def _classify_http_status(code, headers):
    """Classify an HTTP status from a URL liveness probe.

    Returns ('live'|'dead'|'transient'|'head_unsupported', detail). 429,
    rate-limited 403s, and 5xx are transient — the host is under load, not
    the link dead. 405/501 and plain 403 on a HEAD probe usually mean the
    host rejects HEAD — fall through to GET before judging. Other 4xx mean
    the handle does not resolve.
    """
    if code < 400:
        return "live", f"HTTP {code}"
    if code == 429 or (code == 403 and _retry_after(headers) is not None):
        return "transient", f"HTTP {code} (rate-limited)"
    if code in (405, 501) or code == 403:
        return "head_unsupported", f"HTTP {code}"
    if 500 <= code < 600:
        return "transient", f"HTTP {code}"
    return "dead", f"HTTP {code}"


def _probe_once(url, method):
    """One liveness probe. Returns ('live'|'dead'|'transient'|
    'head_unsupported', detail). Never raises."""
    req = urllib.request.Request(url, method=method, headers=_UA)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            if method == "GET":
                r.read(1)  # headers + first byte only; no full download
            return _classify_http_status(r.status, r.headers)
    except urllib.error.HTTPError as e:
        return _classify_http_status(e.code, e.headers)
    except Exception as e:
        # URLError, TimeoutError, ssl errors: the network blipped, not the
        # evidence. Transient by definition.
        return "transient", f"{type(e).__name__}: {e}"


def probe_url(url):
    """Classify one URL handle: ('live'|'dead'|'transient', detail).

    Transient failures (429, 5xx, network errors) are retried with backoff;
    only a transient that survives every attempt is reported as transient.
    A URL that is genuinely gone (404/410, refused GET) is 'dead'. Never
    raises, never a traceback.
    """
    last = ("transient", "no probe attempted")
    for attempt in range(1, _URL_MAX_ATTEMPTS + 1):
        kind, detail = _probe_once(url, "HEAD")
        if kind == "head_unsupported":
            # The host rejects HEAD probes; GET is the real verdict.
            kind, detail = _probe_once(url, "GET")
        if kind == "live":
            return "live", detail
        if kind == "dead":
            return "dead", detail
        last = ("transient", detail)
        if attempt < _URL_MAX_ATTEMPTS:
            wait = _URL_BACKOFF_BASE_S * (2 ** (attempt - 1))
            print(f"receipt: transient ({detail}) on {url} — retrying in "
                  f"{wait}s (attempt {attempt}/{_URL_MAX_ATTEMPTS})",
                  file=sys.stderr)
            time.sleep(wait)
    return last


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
    unknown_handles = []
    for u in dict.fromkeys(urls):
        if "localhost" in u or "127.0.0.1" in u:
            continue
        kind, detail = probe_url(u)
        handle = f"url:{u}"
        if kind == "live":
            verified.append(handle)
        elif kind == "dead":
            dead.append(f"{handle} ({detail})")
        else:
            unknown_handles.append(f"{handle} ({detail})")
    for s in dict.fromkeys(shas):
        (verified if git_exists(s) else dead).append(f"sha:{s[:8]}")
    for p in dict.fromkeys(paths):
        p = p.strip()
        (verified if path_exists(p) else dead).append(f"path:{p}")

    # Transients are reported loudly even when another handle decides the
    # verdict — a transient is never silently folded into a FAIL or a PASS.
    if unknown_handles:
        print(f"RECEIPT GATE: {len(unknown_handles)} handle(s) unverifiable "
              f"(transient): {', '.join(unknown_handles[:5])}",
              file=sys.stderr)
    if dead:
        fail(f"{len(dead)} dead artifact handle(s): {', '.join(dead[:5])}. "
             "Evidence that does not resolve is not evidence.")
    if unknown_handles:
        unknown(f"{len(unknown_handles)} artifact handle(s) could not be "
                f"verified (transient failure): "
                f"{', '.join(unknown_handles[:5])} — re-run, not a FAIL.")
    if not verified:
        fail("`## Evidence` exists but contains no verifiable artifact handle "
             "(live URL, existing SHA, or existing repo path).")
    print(f"Receipt OK: {len(verified)} live handle(s): "
          f"{', '.join(verified[:5])}")


if __name__ == "__main__":
    main()
