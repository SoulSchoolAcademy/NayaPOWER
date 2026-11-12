#!/usr/bin/env python3
"""cli.py — friction + watchers over a JSONL ledger stream.

Usage:
    python3 cli.py [--input stream.jsonl] [--output out.json]

Input:  one ledger-shaped entry per line (JSONL). With no --input, stdin.
Output: one JSON document:

    {
      "actors":          {actor: {"balance", "level", "level_name", "tier"}},
      "alerts":          [watcher alert dicts, sorted by (watcher, actor)],
      "friction_events": [friction_transition event dicts, in walk order],
      "friction_profile": "friction-profile-v1",
      "points_profile":   "points-profile-v1"
    }

Deterministic: the same input bytes produce byte-identical output bytes
(all mappings key-sorted, all lists in canonical order). Pure stdlib; no
side effects beyond writing the output document. Ships dark — a wiring
step (WIRING.md) decides what consumes this in production.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import balance as _balance
import friction as _friction
import watchers as _watchers


def render(entries):
    """The full output document (as text) for a list of entry dicts."""
    entries = list(entries)
    projection = _balance.project(entries)
    tier_states, events = _friction.evaluate(entries)
    alerts = _watchers.run_watchers(entries)
    actors = {}
    for actor in sorted(projection, key=str):
        proj = projection[actor]
        actors[actor] = {
            "balance": proj["balance"],
            "level": proj["level"],
            "level_name": proj["level_name"],
            "tier": tier_states[actor]["tier"],
        }
    doc = {
        "actors": actors,
        "alerts": alerts,
        "friction_events": events,
        "friction_profile": _friction.FRICTION_PROFILE_ID,
        "points_profile": _balance.POINTS_PROFILE_ID,
    }
    return json.dumps(doc, indent=2, sort_keys=True) + "\n"


def _read_entries(stream):
    entries = []
    for line in stream:
        line = line.strip()
        if line:
            entries.append(json.loads(line))
    return entries


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="JSONL input file (default: stdin)")
    parser.add_argument("--output", help="output file (default: stdout)")
    args = parser.parse_args(argv)
    if args.input:
        with open(args.input, "r", encoding="utf-8") as fh:
            entries = _read_entries(fh)
    else:
        entries = _read_entries(sys.stdin)
    text = render(entries)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
