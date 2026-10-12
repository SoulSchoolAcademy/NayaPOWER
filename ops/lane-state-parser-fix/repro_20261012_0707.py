#!/usr/bin/env python3
"""Reproduction of the 2026-10-12 07:07Z defect on REAL lane-feed data.

Defect: determine_state() closes the EARLIEST open claim with a matching
seat instead of the signer's most-recent open claim.

Real instance (lane gamma, issue #1715):
  sign-in  6117761106  04:28:54Z  Naya Mu (Human Value) instrument build
  sign-in  6118180575  05:13:30Z  NAYA 5 freshness worker
  sign-out 6118197320  05:15:18Z  NAYA 5 freshness worker — closes ITS OWN
                                  sign-in, but the referee closed 6117761106.

Usage: python3 repro_20261012_0707.py <path-to-lane_state.py>
Exit 0 = reproduction confirmed (bug present); exit 1 = fixed.
"""
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[1])))
import importlib.util
spec = importlib.util.spec_from_file_location("lane_state_under_test",
                                              os.path.abspath(sys.argv[1]))
ls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ls)

HERE = os.path.dirname(os.path.abspath(__file__))


def load(cid):
    d = json.load(open(os.path.join(HERE, f"fixture-{cid}.json")))
    return {"id": d["id"], "created_at": d["created_at"],
            "body": d["body"] or ""}


now = datetime(2026, 10, 12, 8, 0, tzinfo=timezone.utc)
comments = [load("6117761106"), load("6118180575"), load("6118197320")]
res = ls.determine_state(comments, now=now, lease_minutes=120)

print("evidence lines mentioning the sign-out:")
for e in res["evidence"]:
    if "6118197320" in e:
        print("  ", e)

closed_own = any("sign-out 6118197320" in e and "closes sign-in 6118180575" in e
                 for e in res["evidence"])
mis_closed = any("sign-out 6118197320" in e and "closes sign-in 6117761106" in e
                 for e in res["evidence"])

if mis_closed:
    print("REPRODUCED: sign-out 6118197320 mis-closed 6117761106 "
          "(earliest seat match) instead of the signer's own 6118180575")
    print("state:", res["state"], "| occupant:", res["occupant"]["sign_in_id"])
    sys.exit(0)
if closed_own:
    print("FIXED: sign-out 6118197320 closed the signer's own most-recent "
          "open claim 6118180575")
    print("state:", res["state"], "| occupant sign-in:",
          res["occupant"]["sign_in_id"] if res["occupant"] else None)
    sys.exit(1)
print("UNEXPECTED outcome — neither close line found")
print(json.dumps(res, indent=2, default=str)[:2000])
sys.exit(2)
