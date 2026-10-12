#!/usr/bin/env python3
"""Reproduction of the 2026-10-12 09:45Z seatless-sign-out defect (defect 4)
on REAL lane-feed data.

Defect: a seatless sign-out falls into the "names no matching seat" fallback,
which closes the EARLIEST open claim instead of the signer's own
most-recent open claim — the opposite of the defect-3 rule and of
Kappa §7 ("earliest wins, later claimant owes a stand-down").

Real instance (lane alpha, issue #1713):
  sign-in  6121713676  09:42:32Z  Naya Alpha (LEARN) — compound observation
  sign-in  6121747521  09:44:49Z  [SIGN-IN] learn-convergence-builder run
  sign-out 6121753742  09:45:14Z  [SIGN-OUT] learn-convergence-builder run
    (seatless: bracketed header holds only the role marker "SIGN-OUT",
    which normalize_seat strips to None)

Net effect: Alpha's compound-observation claim 6121713676 was closed by a
sign-out from the exercise's session; the exercise's own claim 6121747521
stayed open.

Usage: python3 repro_20261012_1115.py <path-to-lane_state.py>
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


now = datetime(2026, 10, 12, 11, 10, tzinfo=timezone.utc)
comments = [load("6121713676"), load("6121747521"), load("6121753742")]
res = ls.determine_state(comments, now=now, lease_minutes=120)

print("evidence lines mentioning the sign-out:")
for e in res["evidence"]:
    if "6121753742" in e:
        print("  ", e)

mis_closed = any("sign-out 6121753742" in e and "closes sign-in 6121713676" in e
                 for e in res["evidence"])
closed_own = any("sign-out 6121753742" in e and "closes sign-in 6121747521" in e
                 for e in res["evidence"])

if mis_closed:
    print("REPRODUCED: seatless sign-out 6121753742 mis-closed the EARLIEST "
          "open claim 6121713676 (Alpha) instead of the signer's own "
          "most-recent open claim 6121747521")
    print("state:", res["state"], "| occupant sign-in:",
          res["occupant"]["sign_in_id"] if res["occupant"] else None)
    sys.exit(0)
if closed_own:
    print("FIXED: seatless sign-out 6121753742 closed the signer's own "
          "most-recent open claim 6121747521; Alpha's 6121713676 stays open")
    print("state:", res["state"], "| occupant sign-in:",
          res["occupant"]["sign_in_id"] if res["occupant"] else None)
    sys.exit(1)
print("UNEXPECTED outcome — neither close line found")
print(json.dumps(res, indent=2, default=str)[:2000])
sys.exit(2)
