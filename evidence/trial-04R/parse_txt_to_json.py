#!/usr/bin/env python3
"""PIN: the named producer of answers_raw_04r.json (trial-04R).

Parses the .txt answer sheets in answer_sheets/ into the canonical JSON.
Byte-proven: output of this script == the committed answers_raw_04r.json
(sha256-proven, see TRIAL-04R-RECEIPT.md lineage; diff must be empty).

Method:
- Sheet order: COLD arm then BRIDGE arm, per arm_assignment.txt.
- Agents with no sheet file (T4R-A19.MISSING.txt is not a sheet) are excluded
  per the preregistration missing-agent rule.
- Line format: `Q<n>: <answer>` -> value is the full text after `Q<n>:`
  stripped; `[source: ...]` tags are retained verbatim in the value.
- Encoding: json.dump default (ensure_ascii=True, indent=2, no trailing newline).

Usage: python3 parse_txt_to_json.py [--check]  # --check exits 0 iff byte-identical
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SHEETS = os.path.join(BASE, "answer_sheets")
OUT = os.path.join(BASE, "answers_raw_04r.json")


def arm_order():
    # arm_assignment.txt lists BRIDGE then COLD; the canonical JSON is COLD first.
    by_arm = {}
    for line in open(os.path.join(BASE, "arm_assignment.txt"), encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        arm, agents = line.split(":", 1)
        by_arm[arm.strip()] = agents.split()
    return by_arm["COLD"] + by_arm["BRIDGE"]


def parse_sheet(path):
    out = {}
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            m = re.match(r"^(Q\d+):\s*(.*)$", line)
            if not m:
                continue
            q, val = m.group(1), m.group(2)
            # the value is the FULL answer text, source tags included —
            # the canonical JSON retains `[source: ...]` verbatim.
            out[q] = val.strip()
    return out


def build():
    data = {}
    for agent in arm_order():
        p = os.path.join(SHEETS, agent + ".txt")
        if not os.path.exists(p):
            print("skip (no sheet): %s" % agent)
            continue
        data[agent] = parse_sheet(p)
    return json.dumps(data, indent=2, ensure_ascii=True)


def main():
    want = build()
    if "--check" in sys.argv:
        have = open(OUT, encoding="utf-8").read()
        if want == have:
            print("BYTE-IDENTICAL: parse reproduces answers_raw_04r.json")
            return 0
        print("DIFFERS: output != committed answers_raw_04r.json")
        return 1
    open(OUT, "w", encoding="utf-8").write(want)
    print("wrote", OUT)


if __name__ == "__main__":
    sys.exit(main())
