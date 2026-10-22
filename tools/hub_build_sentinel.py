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
import json
import os
import re
import sys
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


def fetch_url(url: str, timeout: float) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "hub-build-sentinel/1.0 (build-identity check)",
            "Accept-Encoding": "identity",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                raise FetchError(f"{url}: HTTP {resp.status}")
            return resp.read()
    except FetchError:
        raise
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
        raise FetchError(f"{url}: {exc}") from exc


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
            record = {
                "tool": "hub_build_sentinel",
                "ts_epoch": now_epoch(),
                "ts_iso": iso(now_epoch()),
                "verdict": VERDICT_UNREACHABLE,
                "base_url": base_url,
                "detail": str(exc),
            }
            write_state(Path(args.state), record)
            print(f"HUB BUILD SENTINEL — {record['ts_iso']}")
            print(f"VERDICT: UNREACHABLE — {exc}")
            print("(a fetch failure is not a wrong build; the sentinel itself ran and recorded this state)")
            return EXIT_UNREACHABLE

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
