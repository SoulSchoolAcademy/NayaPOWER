#!/usr/bin/env python3
"""checkpoint-watch.py — Machine 2 of the Ultimate Operating System.

Reads the team-pulse ledger and reports, per watched lane, how long it has
been silent. A lane is HEALTHY (<30 min since movement), SILENT (30-60 min),
or ESCALATE (>60 min). Exits 1 if any watched lane is SILENT or ESCALATE —
silence is caught by the machine, not by Shawn asking.

It also verifies each watched lane's checkpoint file exists on disk
(--checkpoint id=path, repeatable). A missing checkpoint file is itself a
defect: the work does not exist until it is written down.

Usage:
  python3 checkpoint-watch.py --ledger <team-pulse-waiting.json> \
      --watch nitro:dashboard-fix4,nitro:personal-verify3,nitro:pricing-fix1,nitro:hub-fix \
      --checkpoint nitro:dashboard-fix4=~/workspace/team-nitro/dashboard/defectfix-v7/builder/FIX-PASS-4.md \
      --checkpoint nitro:personal-verify3=~/workspace/team-nitro/personal/whoiam-removal/verifier-2/PERSONAL-VERIFY-3.md

Exit codes: 0 = every watched lane healthy and checkpointed.
            1 = a watched lane is silent, escalating, or its checkpoint is missing.
            2 = the ledger cannot be read (the watch itself is broken).
"""
import argparse
import datetime
import json
import os
import sys


def parse_time(value):
    if not value:
        return None
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=datetime.timezone.utc)
    except ValueError:
        return None


def main():
    parser = argparse.ArgumentParser(description="Watch the lanes for silence.")
    parser.add_argument("--ledger", required=True,
                        help="Path to team-pulse-waiting.json")
    parser.add_argument("--watch", required=True,
                        help="Comma-separated lane ids to watch")
    parser.add_argument("--checkpoint", action="append", default=[],
                        help="id=path pair; the lane's checkpoint file must exist")
    args = parser.parse_args()

    try:
        with open(os.path.expanduser(args.ledger)) as f:
            ledger = json.load(f)
    except (OSError, ValueError) as exc:
        print("WATCH BROKEN: cannot read ledger: %s" % exc, file=sys.stderr)
        return 2

    now = datetime.datetime.now(datetime.timezone.utc)
    items = {item.get("id"): item for item in ledger.get("items", [])}
    checkpoints = {}
    for pair in args.checkpoint:
        if "=" in pair:
            lane_id, path = pair.split("=", 1)
            checkpoints[lane_id.strip()] = os.path.expanduser(path.strip())

    watched = [lane.strip() for lane in args.watch.split(",") if lane.strip()]
    bad = 0
    for lane_id in watched:
        item = items.get(lane_id)
        if item is None:
            print("%s: NOT ON THE BOARD — no ledger entry" % lane_id)
            bad += 1
            continue
        moved = parse_time(item.get("movement_utc"))
        if moved is None:
            print("%s: NO MOVEMENT RECORDED — cannot tell if it is alive" % lane_id)
            bad += 1
            continue
        silent = int((now - moved).total_seconds() // 60)
        if silent < 30:
            status = "HEALTHY"
        elif silent < 60:
            status = "SILENT"
            bad += 1
        else:
            status = "ESCALATE"
            bad += 1
        line = "%s: %s — silent %d min (last movement %s)" % (
            lane_id, status, silent, item.get("movement_utc"))
        checkpoint = checkpoints.get(lane_id)
        if checkpoint:
            if os.path.isfile(checkpoint):
                line += " — checkpoint present"
            else:
                line += " — CHECKPOINT MISSING: %s" % checkpoint
                bad += 1
        print(line)

    stale = 0
    for item in ledger.get("items", []):
        moved = parse_time(item.get("movement_utc"))
        if moved and (now - moved).total_seconds() > 30 * 60:
            stale += 1
    print("ledger: %d open items, %d silent over 30 min (not all are active lanes)"
          % (len(ledger.get("items", [])), stale))

    if bad:
        print("WATCH: %d watched lane(s) need attention" % bad)
        return 1
    print("WATCH: all watched lanes healthy and checkpointed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
