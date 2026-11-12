#!/usr/bin/env python3
"""Hub-sync heartbeat writer + liveness checker — Balanced Machine step 4
(DESIGN.ai.md §5.1).

WHY THIS EXISTS
---------------
On 2026-10-21 the hub-sync watcher died silently when its VM was replaced.
Nothing alarmed; the live Hub wall sat at 1 card for hours. Silence was the
failure mode. This tool abolishes it:

* The watcher calls ``beat`` every successful cycle — it writes a small
  timestamped heartbeat artifact (default ``HUB/sync-heartbeat.json``).
* A checker (this tool's ``check``, run on the director-pass cadence or by
  the ``hub-sync-liveness`` workflow) alarms when the newest heartbeat is
  older than --max-age seconds (default 600 = the design's 10 minutes /
  30 missed 20-second cycles). A missing or unreadable heartbeat is an
  alarm too — never a pass.

The alarm is a board post to the live board (#2793) via the gh-api wrapper
the lanes already use, or plain stdout when --post is not given.

USAGE
-----
    python3 tools/hub_sync_heartbeat.py beat [--file PATH] [--detail TEXT]
    python3 tools/hub_sync_heartbeat.py check [--file PATH | --ref REF | --url URL]
                                              [--max-age 600] [--post]

Exit codes (check): 0 fresh · 1 STALE/missing (alarm) · 2 usage error.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HEARTBEAT = REPO_ROOT / "HUB" / "sync-heartbeat.json"
HEARTBEAT_REPO_PATH = "HUB/sync-heartbeat.json"
DEFAULT_MAX_AGE = 600  # seconds — DESIGN.ai.md §5.1: 10 minutes / 30 missed cycles
BOARD_ISSUE = 2793
REPO_SLUG = "SoulSchoolAcademy/NayaPOWER"
DEFAULT_GH_API = Path.home() / "workspace" / "naya" / "bin" / "gh-api"


def now_epoch() -> float:
    return datetime.now(timezone.utc).timestamp()


def iso(epoch: float) -> str:
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------
# beat
# --------------------------------------------------------------------------

def beat(path: Path, detail: str = "", watcher: str = "hub-sync",
         epoch: float | None = None) -> dict:
    ts = now_epoch() if epoch is None else epoch
    payload = {
        "watcher": watcher,
        "ts_epoch": ts,
        "ts_utc": iso(ts),
        "cycle_ok": True,
        "detail": detail,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)  # atomic — a checker never reads a torn heartbeat
    return payload


# --------------------------------------------------------------------------
# check
# --------------------------------------------------------------------------

def load_heartbeat(file: Path | None, ref: str | None, url: str | None) -> tuple[dict | None, str]:
    """Return (payload, source description) or (None, why-unreadable)."""
    try:
        if url:
            req = urllib.request.Request(url, headers={"User-Agent": "hub-sync-liveness/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8")), f"url {url}"
        if ref:
            proc = subprocess.run(
                ["git", "show", f"{ref}:{HEARTBEAT_REPO_PATH}"],
                cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
            )
            if proc.returncode != 0:
                return None, f"no heartbeat at ref {ref} ({proc.stderr.strip()[:160]})"
            return json.loads(proc.stdout), f"git ref {ref}:{HEARTBEAT_REPO_PATH}"
        path = file or DEFAULT_HEARTBEAT
        if not path.is_file():
            return None, f"heartbeat file missing: {path}"
        return json.loads(path.read_text(encoding="utf-8")), f"file {path}"
    except (json.JSONDecodeError, ValueError) as exc:
        return None, f"heartbeat unreadable: {exc}"
    except Exception as exc:
        return None, f"heartbeat source failed: {exc}"


def evaluate(payload: dict | None, why: str, max_age: int,
             epoch: float | None = None) -> tuple[bool, str]:
    """(fresh, message). Missing/unreadable/stale all alarm — silence is the
    failure mode this tool exists to abolish."""
    now = now_epoch() if epoch is None else epoch
    if payload is None:
        return False, f"HUB-SYNC LIVENESS ALARM: no heartbeat readable ({why}). " \
                      f"The sync watcher may be down — silence is the failure mode."
    ts = payload.get("ts_epoch")
    if not isinstance(ts, (int, float)):
        return False, f"HUB-SYNC LIVENESS ALARM: heartbeat carries no numeric ts_epoch ({why})."
    age = now - float(ts)
    if age > max_age:
        return False, (f"HUB-SYNC LIVENESS ALARM: last successful sync cycle was "
                       f"{iso(float(ts))} — {int(age)}s ago, over the {max_age}s limit "
                       f"({why}). The Hub wall may be frozen; check the watcher.")
    return True, f"hub-sync heartbeat fresh: {int(age)}s old (limit {max_age}s, {why})."


def post_alarm(message: str, body_dir: Path) -> tuple[bool, str]:
    gh_api = Path(os.environ.get("GH_API", str(DEFAULT_GH_API)))
    if not gh_api.is_file():
        return False, f"gh-api wrapper not found at {gh_api} — alarm NOT posted"
    body_dir.mkdir(parents=True, exist_ok=True)
    body_file = body_dir / "hub-sync-liveness-alarm.json"
    body_file.write_text(json.dumps({"body": message}), encoding="utf-8")
    proc = subprocess.run(
        [str(gh_api), "POST",
         f"/repos/{REPO_SLUG}/${'issues'}/{BOARD_ISSUE}/comments",
         "--body-file", str(body_file)],
        capture_output=True, text=True, timeout=60,
    )
    if proc.returncode != 0:
        return False, f"alarm post failed: {(proc.stderr or proc.stdout)[:300]}"
    try:
        comment_id = json.loads(proc.stdout).get("id")
    except (json.JSONDecodeError, ValueError):
        comment_id = "?"
    return True, f"alarm posted to #{BOARD_ISSUE} (comment {comment_id})"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_beat = sub.add_parser("beat", help="write a heartbeat (watcher calls this each cycle)")
    p_beat.add_argument("--file", default=None)
    p_beat.add_argument("--detail", default="")
    p_beat.add_argument("--watcher", default="hub-sync")

    p_check = sub.add_parser("check", help="alarm if the newest heartbeat is stale")
    src = p_check.add_mutually_exclusive_group()
    src.add_argument("--file", default=None)
    src.add_argument("--ref", default=None, help="git ref holding HUB/sync-heartbeat.json")
    src.add_argument("--url", default=None, help="URL serving the heartbeat JSON")
    p_check.add_argument("--max-age", type=int, default=DEFAULT_MAX_AGE)
    p_check.add_argument("--post", action="store_true",
                         help=f"post the alarm to board #{BOARD_ISSUE} via gh-api")
    p_check.add_argument("--body-dir", default=None,
                         help="dir for the alarm body file (default: heartbeat dir)")

    args = parser.parse_args(argv)

    if args.cmd == "beat":
        path = Path(args.file) if args.file else DEFAULT_HEARTBEAT
        payload = beat(path, detail=args.detail, watcher=args.watcher)
        print(f"heartbeat written: {path} @ {payload['ts_utc']}")
        return 0

    if args.cmd == "check":
        payload, why = load_heartbeat(
            Path(args.file) if args.file else None, args.ref, args.url)
        fresh, message = evaluate(payload, why, args.max_age)
        print(message)
        if fresh:
            return 0
        if args.post:
            body_dir = Path(args.body_dir) if args.body_dir else (
                Path(args.file).parent if args.file else DEFAULT_HEARTBEAT.parent)
            posted, detail = post_alarm(message, body_dir)
            print(detail)
            if not posted:
                return 2
        return 1

    return 2


if __name__ == "__main__":
    sys.exit(main())
