#!/usr/bin/env python3
"""Hub build-identity sentinel — first watcher for the public Hub.

WHY THIS EXISTS
---------------
On 2026-10-22 the GitHub auto-deploy (deploy-hub-cloudflare.yml, created
2026-10-21 via PR #2738) fired on PR #2961's merge and overwrote the live
Hub at nayanet.live with the repo's stale `HUB/app` monolith. Every step
reported SUCCESS — the deploy's health check only asserts HTTP 200, and a
wrong-but-live build returns 200. The site served an October-2-era shell
(10 baked note cards, no Smart Factory room, no Smart Note wall) for ~25
minutes and the DIRECTOR found it by eye. The hub-sync watcher that used
to re-assert the true build had died silently days earlier; silence was
the failure mode twice over.

This sentinel abolishes both failure modes:

* It verifies BUILD IDENTITY, not liveness. It fetches the public home
  page and one room page over HTTPS and evaluates identity markers from
  `hub_build_expectations.json` — the true build's room registry, its
  current design tokens, the baked Smart Note wall counted two
  independent ways, the shell's size class, and the absence of the stale
  monolith's signature wiring. HTTP 200 with the wrong build is a
  DIVERGED verdict, not a pass.
* It is alive by construction. Every run writes its verdict and
  timestamp to a state file, whatever the verdict. A supervisor running
  `check-state` alarms when that file goes stale — a dead sentinel is an
  alarm condition, never a silent pass. (The dead watcher is exactly
  what let the 2026-10-22 overwrite stick.)

The sentinel OBSERVES the public site only. It never touches publishing
or deploy machinery: on DIVERGED, the runbook (hub_build_sentinel.md)
routes the alarm to the humans/lanes who own the build.

USAGE
-----
    python3 tools/hub_build_sentinel.py check [--base-url URL]
        [--expectations PATH] [--state PATH] [--timeout 30] [--json]
    python3 tools/hub_build_sentinel.py check --home-file F --room-file F
        (offline evaluation of captured pages — tests, incident replay)
    python3 tools/hub_build_sentinel.py check-state [--state PATH]
        [--max-age 600]

Exit codes (check): 0 MATCH · 1 DIVERGED · 2 usage/config error ·
3 UNREACHABLE (a fetch failed — distinct from a wrong build).
Exit codes (check-state): 0 fresh · 1 stale/missing/unreadable · 2 usage.
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent
DEFAULT_EXPECTATIONS = TOOL_DIR / "hub_build_expectations.json"
STATE_ENV_VAR = "HUB_SENTINEL_STATE"
DEFAULT_STATE = (
    Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
    / "nayapower"
    / "hub-build-sentinel.state.json"
)
DEFAULT_MAX_AGE = 600  # seconds — 2x the recommended 5-minute interval

EXIT_MATCH = 0
EXIT_DIVERGED = 1
EXIT_USAGE = 2
EXIT_UNREACHABLE = 3

VERDICT_MATCH = "MATCH"
VERDICT_DIVERGED = "DIVERGED"
VERDICT_UNREACHABLE = "UNREACHABLE"


def iso(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def now_epoch() -> float:
    return datetime.now(timezone.utc).timestamp()


# ---------------------------------------------------------------------------
# fetching
# ---------------------------------------------------------------------------


class FetchError(Exception):
    """A page could not be fetched at all — UNREACHABLE, never DIVERGED."""


# Every transport failure the fetch path can raise while moving bytes.
# http.client.HTTPException (IncompleteRead, RemoteDisconnected, ...) is
# NOT an OSError subclass: leaving it out of the caught tuple is what
# crashed this sentinel on 10 straight hourly runs on 2026-10-25 (L671) —
# the process died on a traceback, emitted no verdict, and never advanced
# its state file, so a human had to re-verify the Hub by hand every hour.
TRANSPORT_ERRORS = (
    http.client.HTTPException,
    urllib.error.URLError,
    urllib.error.HTTPError,
    ConnectionError,
    TimeoutError,
    OSError,
)

READ_CHUNK = 256 * 1024  # drain granularity for response bodies
RESUME_LIMIT = 10  # Range-resume rounds before a truncated fetch gives up
FETCH_ATTEMPTS = 3  # whole-fetch attempts (fresh body), with backoff


def _request(url: str, start: int = 0) -> urllib.request.Request:
    headers = {
        "User-Agent": "hub-build-sentinel/1.0 (build-identity check)",
        "Accept-Encoding": "identity",
    }
    if start:
        headers["Range"] = f"bytes={start}-"
    return urllib.request.Request(url, headers=headers)


def _promised_total(resp, start: int) -> int | None:
    """The total body length the server promised, if it promised one:
    the total in a 206 Content-Range, else Content-Length. None when the
    server promised nothing (chunked transfer) — then only a clean EOF
    or a later Content-Range can prove the body complete."""
    content_range = resp.headers.get("Content-Range") or ""
    if "/" in content_range:
        total = content_range.rsplit("/", 1)[1].strip()
        if total.isdigit():
            return int(total)
    length = resp.headers.get("Content-Length")
    if length is not None and str(length).isdigit():
        return start + int(length) if resp.status == 206 else int(length)
    return None


def _drain(resp, body: bytearray) -> None:
    """Append a response body to `body`, reading in chunks. A transport
    failure propagates with everything read so far already appended —
    IncompleteRead's partial bytes included — so the caller can resume
    from len(body) instead of starting over."""
    while True:
        try:
            chunk = resp.read(READ_CHUNK)
        except http.client.IncompleteRead as exc:
            body += exc.partial
            raise
        if not chunk:
            return
        body += chunk


def _fetch_resumable(url: str, timeout: float) -> bytes:
    """Fetch `url`, resuming truncated transfers with Range requests.

    The live Hub shell is ~5.4 MB and the connection serving it drops
    mid-body often enough that one unbounded read() crashed this
    sentinel for 10 straight hourly runs (IncompleteRead, 2026-10-25).
    Bytes already received are kept; the next request asks only for the
    remainder. A body is returned ONLY when it is complete — a truncated
    page must never reach evaluate(), where it would read as a wrong
    build and cry DIVERGED at a healthy Hub.
    """
    body = bytearray()
    total: int | None = None
    resumes = 0
    while True:
        start = len(body)
        failure: Exception | None = None
        try:
            with urllib.request.urlopen(_request(url, start), timeout=timeout) as resp:
                if resp.status not in (200, 206):
                    raise FetchError(f"{url}: HTTP {resp.status}")
                if resp.status == 200 and start:
                    # The server ignored the Range header and is sending a
                    # fresh full body — restart from it, never append to it.
                    body = bytearray()
                    start = 0
                promised = _promised_total(resp, start)
                if promised is not None:
                    total = promised
                _drain(resp, body)
        except FetchError:
            raise
        except TRANSPORT_ERRORS as exc:
            if not body and resumes == 0:
                # Nothing was ever received — not a truncation to resume;
                # let fetch_url's retry layer handle it with backoff.
                raise FetchError(f"{url}: {exc}") from exc
            failure = exc
        if failure is None and (total is None or len(body) >= total):
            return bytes(body)
        # Truncated: the connection dropped mid-body, or closed cleanly
        # short of the promised total. Resume from the bytes we hold.
        resumes += 1
        if resumes > RESUME_LIMIT:
            held = f"{len(body)} of {total}" if total is not None else f"{len(body)}"
            raise FetchError(
                f"{url}: body still truncated ({held} bytes) after {RESUME_LIMIT} resumes"
            ) from failure
        time.sleep(0.2)


def _fetch_via_curl(url: str, timeout: float) -> bytes:
    """Last-resort fetch via the curl binary, when one is on PATH.

    Measured 2026-10-25 in the sandbox this sentinel runs in: the egress
    proxy truncates THIS process's TLS flows mid-body — a dozen urllib
    attempts at the 5.4 MB shell (plain reads, chunked reads, read1,
    gzip, ALPN variants) delivered 0.26–3.2 MB before the connection
    died, and the origin ignores Range (200 full body), so resumption
    cannot converge either. curl is a different TLS client, the proxy
    lets it through, and it completed every attempt. The bytes are the
    same served bytes whichever client carries them — evaluation is
    untouched — and curl exits non-zero on a truncated transfer, so
    this path never returns a partial body.
    """
    exe = shutil.which("curl")
    if exe is None:
        raise FetchError(f"{url}: no curl binary on PATH for the fallback fetch")
    try:
        proc = subprocess.run(
            [
                exe, "-fsSL", "--max-redirs", "5",
                "--max-time", str(max(1, int(timeout))),
                "-A", "hub-build-sentinel/1.0 (build-identity check)",
                "-H", "Accept-Encoding: identity",
                url,
            ],
            capture_output=True,
            timeout=timeout + 5,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise FetchError(f"{url}: curl fallback could not run: {exc}") from exc
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", errors="replace").strip()[:200]
        raise FetchError(f"{url}: curl fallback failed (exit {proc.returncode}): {err}")
    return proc.stdout


def fetch_url(url: str, timeout: float) -> bytes:
    """Fetch `url` completely, or raise FetchError. Never raises a raw
    transport exception and never returns partial bytes: every failure
    mode lands in FetchError, which run_check turns into the UNREACHABLE
    verdict + a state-file advance (the L671 floor)."""
    last: Exception | None = None
    for attempt in range(FETCH_ATTEMPTS):
        try:
            return _fetch_resumable(url, timeout)
        except FetchError as exc:
            last = exc
            break  # a truncation/HTTP verdict will not heal by re-reading
        except TRANSPORT_ERRORS as exc:  # _fetch_resumable converts these; belt and braces
            last = exc
        if attempt + 1 < FETCH_ATTEMPTS:
            time.sleep(0.5 * (2**attempt))
    # The stdlib transport is exhausted. One last-resort attempt via
    # curl (see _fetch_via_curl for the measured reason) before the
    # page is declared unreachable.
    try:
        return _fetch_via_curl(url, timeout)
    except FetchError as curl_exc:
        raise FetchError(f"{last} | curl fallback also failed: {curl_exc}") from curl_exc


# ---------------------------------------------------------------------------
# evaluation (pure — no network; the tests drive this directly)
# ---------------------------------------------------------------------------


def evaluate_check(check: dict, pages: dict[str, bytes]) -> dict:
    """Evaluate one expectation check against decoded page bodies.

    `pages` maps "home"/"room" to raw bytes. Returns a result dict with
    id, kind, page, ok, and a human-readable detail string.
    """
    page = check["page"]
    body = pages[page]
    text = body.decode("utf-8", errors="replace")
    kind = check["kind"]
    detail = ""
    ok = False

    if kind == "contains":
        found = text.count(check["needle"])
        ok = found >= check.get("min_count", 1)
        detail = f"found {found}x, need >= {check.get('min_count', 1)}x: {check['needle']!r}"
    elif kind == "count":
        found = text.count(check["needle"])
        ok = found >= check["min_count"]
        detail = f"count {found}, need >= {check['min_count']}: {check['needle']!r}"
    elif kind == "unique_regex_count":
        found = len(set(re.findall(check["pattern"], text)))
        ok = found >= check["min_count"]
        detail = f"unique matches {found}, need >= {check['min_count']}: /{check['pattern']}/"
    elif kind == "min_bytes":
        ok = len(body) >= check["min_bytes"]
        detail = f"{len(body)} bytes, need >= {check['min_bytes']}"
    elif kind == "forbidden":
        found = text.count(check["needle"])
        ok = found == 0
        detail = f"found {found}x, need 0x: {check['needle']!r}"
    elif kind == "distinct_from_home":
        ok = body != pages["home"]
        detail = "room bytes differ from home bytes" if ok else "room bytes IDENTICAL to home bytes (fallback shell)"
    else:
        detail = f"unknown check kind: {kind!r}"
        ok = False

    return {"id": check["id"], "kind": kind, "page": page, "ok": ok, "detail": detail}


def classify_suspect(expectations: dict, pages: dict[str, bytes], results: list[dict]) -> str:
    """Name the suspected build when the verdict is DIVERGED."""
    home_text = pages["home"].decode("utf-8", errors="replace")
    sig = expectations.get("stale_signature", {})
    needles = sig.get("needles", [])
    sig_present = bool(needles) and all(n in home_text for n in needles)
    wall_failed = any(
        (not r["ok"]) and r["id"].startswith("note_wall") for r in results
    )
    forbidden_failed = any((not r["ok"]) and r["kind"] == "forbidden" for r in results)
    if sig_present and wall_failed:
        return sig.get("label", "stale-signature build")
    if sig_present or forbidden_failed:
        return "repo-monolith-derived / hybrid build (stale signature elements present)"
    return "unknown build (no known signature matched)"


def evaluate(expectations: dict, pages: dict[str, bytes]) -> dict:
    """Evaluate all checks. Returns verdict, per-check results, suspect."""
    results = [evaluate_check(c, pages) for c in expectations["checks"]]
    failed = [r for r in results if not r["ok"]]
    if failed:
        verdict = VERDICT_DIVERGED
        suspect = classify_suspect(expectations, pages, results)
    else:
        verdict = VERDICT_MATCH
        suspect = None
    return {"verdict": verdict, "results": results, "failed": failed, "suspected_build": suspect}


# ---------------------------------------------------------------------------
# state file — liveness by construction
# ---------------------------------------------------------------------------


def write_state(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def check_state(path: Path, max_age: float) -> tuple[int, str]:
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
        ts = float(record["ts_epoch"])
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return 1, f"ALARM: sentinel state missing or unreadable at {path} ({exc}) — the sentinel is presumed DEAD"
    age = now_epoch() - ts
    if age > max_age:
        return 1, (
            f"ALARM: sentinel state is {age:.0f}s old (max {max_age:.0f}s) — "
            f"last verdict {record.get('verdict')} at {record.get('ts_iso')} — the sentinel is presumed DEAD"
        )
    return 0, f"sentinel alive: state {age:.0f}s old, last verdict {record.get('verdict')} at {record.get('ts_iso')}"


# ---------------------------------------------------------------------------
# check command
# ---------------------------------------------------------------------------


def load_expectations(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"error: cannot read expectations file {path}: {exc}")
    for key in ("base_url", "pages", "checks"):
        if key not in data:
            raise SystemExit(f"error: expectations file {path} is missing key {key!r}")
    return data


def _record_unreachable(state_path: Path, base_url: str, detail: str) -> int:
    """The L671 floor: a failed fetch still emits the structured
    UNREACHABLE verdict AND advances the state file. A run that produces
    neither a verdict nor a state advance is the exact failure mode this
    sentinel exists to abolish — it must be impossible, not unlikely."""
    ts = now_epoch()
    record = {
        "tool": "hub_build_sentinel",
        "ts_epoch": ts,
        "ts_iso": iso(ts),
        "verdict": VERDICT_UNREACHABLE,
        "base_url": base_url,
        "detail": detail,
    }
    write_state(state_path, record)
    print(f"HUB BUILD SENTINEL — {record['ts_iso']}")
    print(f"VERDICT: UNREACHABLE — {detail}")
    print("(a fetch failure is not a wrong build; the sentinel itself ran and recorded this state)")
    return EXIT_UNREACHABLE


def run_check(args: argparse.Namespace) -> int:
    expectations = load_expectations(Path(args.expectations))
    base_url = (args.base_url or expectations["base_url"]).rstrip("/")
    pages_spec = expectations["pages"]

    if args.home_file:
        # Offline evaluation: captured pages, no network.
        try:
            pages = {"home": Path(args.home_file).read_bytes()}
            pages["room"] = Path(args.room_file).read_bytes() if args.room_file else pages["home"]
        except OSError as exc:
            print(f"error: cannot read captured page: {exc}")
            return EXIT_USAGE
        source = f"files:{args.home_file}"
    else:
        pages = {}
        source = base_url
        try:
            for name in ("home", "room"):
                url = base_url + pages_spec[name]
                pages[name] = fetch_url(url, timeout=args.timeout)
        except FetchError as exc:
            return _record_unreachable(Path(args.state), base_url, str(exc))
        except Exception as exc:
            # fetch_url converts every transport failure to FetchError, so
            # reaching here means something unforeseen. The L671 floor
            # still holds: verdict + state advance, never a bare traceback.
            return _record_unreachable(
                Path(args.state), base_url, f"unexpected fetch failure: {exc!r}"
            )

    outcome = evaluate(expectations, pages)
    ts = now_epoch()
    record = {
        "tool": "hub_build_sentinel",
        "ts_epoch": ts,
        "ts_iso": iso(ts),
        "verdict": outcome["verdict"],
        "base_url": base_url,
        "source": source,
        "suspected_build": outcome["suspected_build"],
        "pages": {
            name: {"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}
            for name, body in pages.items()
        },
        "checks": outcome["results"],
    }
    write_state(Path(args.state), record)

    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    else:
        print(f"HUB BUILD SENTINEL — {record['ts_iso']} — source {source}")
        for name, body in pages.items():
            print(f"  {name}: {pages_spec[name]} — {len(body)} bytes, sha256 {record['pages'][name]['sha256'][:16]}…")
        for r in outcome["results"]:
            print(f"  [{'PASS' if r['ok'] else 'FAIL'}] {r['id']} ({r['page']}): {r['detail']}")
        print(f"VERDICT: {outcome['verdict']}", end="")
        if outcome["suspected_build"]:
            print(f" — suspected build: {outcome['suspected_build']}", end="")
        print()
    return EXIT_MATCH if outcome["verdict"] == VERDICT_MATCH else EXIT_DIVERGED


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Hub build-identity sentinel (see module docstring).")
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="fetch the public Hub and verify build identity")
    p_check.add_argument("--base-url", default=None, help="override expectations base_url")
    p_check.add_argument("--expectations", default=str(DEFAULT_EXPECTATIONS))
    p_check.add_argument("--state", default=os.environ.get(STATE_ENV_VAR, str(DEFAULT_STATE)))
    p_check.add_argument("--timeout", type=float, default=30.0)
    p_check.add_argument("--json", action="store_true", help="print the full state record as JSON")
    p_check.add_argument("--home-file", default=None, help="offline: captured home page HTML")
    p_check.add_argument("--room-file", default=None, help="offline: captured room page HTML")

    p_state = sub.add_parser("check-state", help="alarm if the sentinel's own state file is stale")
    p_state.add_argument("--state", default=os.environ.get(STATE_ENV_VAR, str(DEFAULT_STATE)))
    p_state.add_argument("--max-age", type=float, default=DEFAULT_MAX_AGE)

    args = parser.parse_args(argv)
    if args.command == "check":
        return run_check(args)
    if args.command == "check-state":
        code, message = check_state(Path(args.state), args.max_age)
        print(message)
        return code
    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
