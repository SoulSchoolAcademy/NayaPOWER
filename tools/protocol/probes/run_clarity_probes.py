#!/usr/bin/env python3
"""Clarity probe runner for the Two-Layer Law plain-diction wall.

Runs every probe in clarity_probes.json through two_layer.check and prints
the live verdict table. Exit 0 iff every probe behaves per its intent:
HONOR and BOUND probes PASS, ATTACK probes FAIL.

    python3 tools/protocol/probes/run_clarity_probes.py [--json]

The BEFORE column (Flesch era) is pinned in clarity_probe_evidence.md from
the live pre-rewrite run; this runner reproduces the AFTER column.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools" / "protocol"))

from checks import two_layer  # noqa: E402

EXPECTED = {"HONOR": True, "ATTACK": False, "BOUND": True}


def run() -> list[dict]:
    corpus = json.loads((HERE / "clarity_probes.json").read_text())
    tech = corpus["technical"]
    rows = []
    for p in corpus["probes"]:
        rec = {
            "report_type": "deliverable_report",
            "title": p["id"],
            "technical": tech,
            "plain_human": p["plain_human"],
        }
        r = two_layer.check(rec)
        d = r["details"]
        want = EXPECTED[p["intent"]]
        rows.append({
            "id": p["id"],
            "intent": p["intent"],
            "label": p["label"],
            "want_pass": want,
            "got_pass": r["pass"],
            "ok": r["pass"] is want,
            "abstraction": d.get("plain_abstraction"),
            "hits": d.get("abstraction_hits", []),
        })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="Run clarity probes")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    rows = run()
    if args.json:
        print(json.dumps(rows, indent=1))
        return 0 if all(r["ok"] for r in rows) else 1
    print(f"{'ID':4} {'INTENT':7} {'WANT':6} {'GOT':6} {'OK?':5} "
          f"{'abstr.':>6}  hits")
    for r in rows:
        hits = ",".join(r["hits"][:6]) if r["hits"] else "-"
        print(f"{r['id']:4} {r['intent']:7} {str(r['want_pass']):6} "
              f"{str(r['got_pass']):6} {str(r['ok']):5} "
              f"{r['abstraction']:>6.3f}  {hits}")
    n_ok = sum(r["ok"] for r in rows)
    print(f"\n{n_ok}/{len(rows)} probes behave per intent")
    return 0 if n_ok == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
