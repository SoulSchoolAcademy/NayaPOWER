#!/usr/bin/env python3
"""Read-only proof of the NayaNET Hub's *served* Smart Note feed.

A source commit or a successful deploy is not a proof of live publication.
This probe compares the public feed with the intended artifact, including
content hashes, and optionally enforces the latest note's age. No credentials,
private data, or database access are required.

Usage:
  python tools/prove_hub_feed.py --expected-file HUB/app/feed-live.json
  python tools/prove_hub_feed.py --expected-file HUB/app/feed-live.json --max-age-hours 48
  python tools/prove_hub_feed.py --url file:///path/to/fixture.json

Default: fetch the public URL, check basic integrity; --expected-file adds
release parity. The output contains aggregate diagnostics only, not note bodies.
Exit 0=PASS, 1=FAIL, 2=ERROR (not established). Never promote ERROR to PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PUBLIC_URL = "https://nayanet.app/feed-live.json"


def parse_feed(raw: bytes) -> dict:
    """Validate the canonical feed envelope without returning private content."""
    try:
        envelope = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"not valid JSON: {type(exc).__name__}") from exc
    if not isinstance(envelope, dict):
        raise ValueError("feed is not a JSON object")
    notes = envelope.get("notes")
    if not isinstance(notes, list) or not notes:
        raise ValueError("notes must be a nonempty list")
    reported = envelope.get("count")
    if isinstance(reported, bool) or not isinstance(reported, int) or reported != len(notes):
        raise ValueError(f"count metadata mismatch: declared={reported!r}, actual={len(notes)}")
    ids = []
    newest = None
    for i, note in enumerate(notes):
        if not isinstance(note, dict) or not isinstance(note.get("id"), str) or not note["id"].strip():
            raise ValueError(f"card #{i} has no stable id")
        ids.append(note["id"].strip())
        stamp = note.get("created_at") or note.get("created")
        if stamp:
            try:
                dt = datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    raise ValueError("time zone missing")
                dt = dt.astimezone(timezone.utc)
                newest = max(dt, newest) if newest else dt
            except (ValueError, TypeError) as exc:
                raise ValueError(f"card #{i} has invalid timestamp") from exc
    if len(ids) != len(set(ids)):
        raise ValueError(f"duplicate card id(s): {len(ids) - len(set(ids))}")
    return {"count": len(ids), "ids": frozenset(ids), "newest": newest,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "generated_from": envelope.get("generated_from")}


def inspect(live: bytes, expected: bytes | None = None,
            *, max_age_hours: float | None = None,
            required_ids: tuple[str, ...] = (),
            now: datetime | None = None) -> dict:
    """Fail closed: inspect delivered bytes, not repository or UI assertions."""
    try:
        obs = parse_feed(live)
    except ValueError as exc:
        return {"status": "FAIL", "reason": str(exc)}
    out = {"status": "PASS", "count": obs["count"],
           "sha256": obs["sha256"], "generated_from": obs["generated_from"],
           "newest_created_at": obs["newest"].isoformat() if obs["newest"] else None}
    failures = []
    missing = sorted(set(required_ids) - obs["ids"])
    if missing:
        failures.append(f"{len(missing)} required ids not served: {missing[:10]}")
    if expected is not None:
        try:
            want = parse_feed(expected)
        except ValueError as exc:
            return {"status": "ERROR", "reason": f"invalid expected artifact: {exc}"}
        out["expected_count"] = want["count"]
        out["expected_sha256"] = want["sha256"]
        out["missing_count"] = len(want["ids"] - obs["ids"])
        out["unexpected_count"] = len(obs["ids"] - want["ids"])
        if want["ids"] != obs["ids"]:
            failures.append("published card ids differ from checked-in artifact")
        if want["sha256"] != obs["sha256"]:
            failures.append("served bytes differ from checked-in artifact")
    if max_age_hours is not None:
        if obs["newest"] is None:
            failures.append("no parseable note creation timestamp")
        else:
            ref = now or datetime.now(timezone.utc)
            age_hours = (ref.astimezone(timezone.utc) - obs["newest"]).total_seconds() / 3600
            out["newest_age_hours"] = round(age_hours, 2)
            if age_hours > max_age_hours or age_hours < -1:
                failures.append(f"newest note age {age_hours:.2f}h outside 0..{max_age_hours}h (1h clock skew allowed)")
    if failures:
        out["status"] = "FAIL"
        out["reasons"] = failures
    return out


def read_live(url: str, timeout: float = 20.0) -> bytes:
    req = Request(url, headers={"User-Agent": "NayaNET-feed-proof/1.0", "Accept": "application/json"})
    with urlopen(req, timeout=timeout) as res:
        if res.status not in (200, None):
            raise OSError(f"HTTP {res.status}")
        if res.headers.get("Content-Type", "").lower().split(";")[0].strip() not in (
            "application/json", "application/octet-stream", "text/plain"):
            raise OSError("response is not a JSON asset")
        return res.read(64 * 1024 * 1024 + 1)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=PUBLIC_URL)
    parser.add_argument("--expected-file", type=Path)
    parser.add_argument("--max-age-hours", type=float)
    parser.add_argument("--require-id", action="append", default=[])
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args(argv)
    try:
        if args.timeout <= 0 or args.max_age_hours is not None and args.max_age_hours <= 0:
            raise ValueError("timeout and max-age-hours must be positive")
        raw = read_live(args.url, args.timeout)
        if len(raw) > 64 * 1024 * 1024:
            raise ValueError("feed exceeds 64 MiB limit")
        expected = args.expected_file.read_bytes() if args.expected_file else None
        result = inspect(raw, expected, max_age_hours=args.max_age_hours,
                         required_ids=tuple(args.require_id))
        result["source"] = args.url
        result["expected_file"] = str(args.expected_file) if args.expected_file else None
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["status"] == "PASS" else 1 if result["status"] == "FAIL" else 2
    except (OSError, URLError, HTTPError, ValueError) as exc:
        print(json.dumps({"status": "ERROR", "source": args.url,
                          "reason": f"{type(exc).__name__}: {exc}"}, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
