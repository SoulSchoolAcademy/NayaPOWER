#!/usr/bin/env python3
"""
Drink-First Gate — machine enforcement of the Drink-First Law
(Shawn, 2026-10-09, RATIFIED: "before you serve me you must drink the water.
Either do your job right and send me what's right, or don't send me anything
at all. If it's not useful, it's useless.")

No Naya serves Shawn or his people unactivated. Unactivated work doesn't ship,
ever. This gate is the enforcement primitive: it takes an activation receipt
(JSON, schema naya.activation.receipt.v1) and the live main tip SHA (resolved
by the caller from the refs API — the gate never touches the network, so its
verdicts are deterministic) and fails closed.

Verdicts
--------
  PASS               receipt is ACTIVATED, cites the live tip, and is fresh
  FAIL-UNACTIVATED   status != "ACTIVATED"
  FAIL-TIP-MOVED     receipt's main_sha != live tip (SN-0493: a decision
                     expires when the tip moves)
  FAIL-STALE         receipt older than the freshness window (default 4h)
  FAIL-CITATION      --require-citation set and the work product does not cite
                     the receipt's main_sha
  FAIL-SCHEMA        receipt unreadable or missing required fields

Required receipt fields (superset of NAYA-ACTIVATION/ACTIVATION-RECEIPT-TEMPLATE.json):
  schema == "naya.activation.receipt.v1"
  status == "ACTIVATED"
  main_sha             tip the receipt was written against (candidate extension)
  timestamp            ISO-8601 UTC of activation (candidate extension)
  activation_protocol  non-empty string
  loaded               non-empty list naming what was drunk
                       (e.g. ["constitution","design-doctrine","smart-blocks"])

Usage
-----
  python3 drink_first_gate.py --receipt receipt.json --live-tip <sha>
  python3 drink_first_gate.py --receipt receipt.json --live-tip <sha> --max-age-hours 4 --json
  python3 drink_first_gate.py --receipt receipt.json --live-tip <sha> \
      --product work.html --require-citation

Exit codes: 0 = PASS, 1 = FAIL (any FAIL-* verdict), 2 = tool error.

The gate is deliberately dumb: it proves the worker activated against the live
tip recently. It does NOT prove the work is good — pair it with the domain
gate (e.g. design-compliance-check.py) at the same pre-delivery point. A gate
that passes unusable work is not a valid gate.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone

SCHEMA = "naya.activation.receipt.v1"
DEFAULT_MAX_AGE_HOURS = 4


def _parse_ts(raw):
    """Parse an ISO-8601 timestamp; return aware datetime or None."""
    if not isinstance(raw, str) or not raw:
        return None
    text = raw.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def check(receipt, live_tip, max_age_hours=DEFAULT_MAX_AGE_HOURS,
          product_text=None, require_citation=False, now=None):
    """Return (verdict, detail). Pure function — no I/O, no network."""
    now = now or datetime.now(timezone.utc)

    if not isinstance(receipt, dict):
        return "FAIL-SCHEMA", "receipt is not a JSON object"
    if receipt.get("schema") != SCHEMA:
        return "FAIL-SCHEMA", "schema != %r" % SCHEMA
    if receipt.get("status") != "ACTIVATED":
        return ("FAIL-UNACTIVATED",
                "status is %r, not ACTIVATED" % (receipt.get("status"),))

    main_sha = receipt.get("main_sha")
    if not isinstance(main_sha, str) or len(main_sha) < 7:
        return "FAIL-SCHEMA", "missing or invalid main_sha"
    if not isinstance(live_tip, str) or not live_tip:
        raise ValueError("live_tip is required")
    if main_sha != live_tip and not live_tip.startswith(main_sha) \
            and not main_sha.startswith(live_tip):
        return ("FAIL-TIP-MOVED",
                "receipt cites %s, live tip is %s" % (main_sha, live_tip))

    ts = _parse_ts(receipt.get("timestamp"))
    if ts is None:
        return "FAIL-SCHEMA", "missing or unparseable timestamp"
    age = now - ts
    if age > timedelta(hours=max_age_hours):
        return ("FAIL-STALE",
                "receipt age %s exceeds %sh freshness window"
                % (age, max_age_hours))
    if age < timedelta(0):
        return "FAIL-SCHEMA", "timestamp is in the future"

    if not receipt.get("activation_protocol"):
        return "FAIL-SCHEMA", "missing activation_protocol"
    loaded = receipt.get("loaded")
    if not isinstance(loaded, list) or not loaded:
        return "FAIL-SCHEMA", "loaded must be a non-empty list"

    if require_citation:
        if product_text is None:
            return "FAIL-CITATION", "require-citation set but no product text given"
        if main_sha not in product_text:
            return ("FAIL-CITATION",
                    "product does not cite the receipt's main_sha %s" % main_sha)

    return ("PASS",
            "activated against live tip %s, age %s, %d items loaded"
            % (main_sha, age, len(loaded)))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Drink-First Gate: fail closed on unactivated work.")
    ap.add_argument("--receipt", required=True, help="activation receipt JSON path")
    ap.add_argument("--live-tip", required=True, help="live main tip SHA (caller resolves via refs API)")
    ap.add_argument("--max-age-hours", type=float, default=DEFAULT_MAX_AGE_HOURS)
    ap.add_argument("--product", default=None, help="work product path to check for receipt citation")
    ap.add_argument("--require-citation", action="store_true")
    ap.add_argument("--json", action="store_true", help="emit verdict as JSON")
    args = ap.parse_args(argv)

    try:
        with open(args.receipt, encoding="utf-8") as f:
            receipt = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return _emit("TOOL-ERROR", str(e), args, 2)

    product_text = None
    if args.product:
        try:
            with open(args.product, encoding="utf-8") as f:
                product_text = f.read()
        except OSError as e:
            return _emit("TOOL-ERROR", str(e), args, 2)

    try:
        verdict, detail = check(receipt, args.live_tip, args.max_age_hours,
                                product_text, args.require_citation)
    except ValueError as e:
        return _emit("TOOL-ERROR", str(e), args, 2)

    return _emit(verdict, detail, args, 0 if verdict == "PASS" else 1)


def _emit(verdict, detail, args, code):
    if args.json:
        print(json.dumps({"verdict": verdict, "detail": detail}))
    else:
        print("%s: %s" % (verdict, detail))
    return code


if __name__ == "__main__":
    sys.exit(main())
