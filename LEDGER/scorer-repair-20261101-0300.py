#!/usr/bin/env python3
"""One-off repair (lane-scorer tick 2026-11-01 03:00 PST): split a concatenated
scores line so every score row parses line-by-line again. No scores changed,
only a missing newline restored. Run once; verify with a full re-parse."""
import json
from json import JSONDecoder
from pathlib import Path

p = Path("/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl")
lines = p.read_text().splitlines(keepends=True)
dec = JSONDecoder()
out = []
fixed = 0
for line in lines:
    s = line.strip()
    if not s:
        continue
    try:
        json.loads(s)
        out.append(s + "\n")
    except Exception:
        # Try to decode two concatenated objects from one line.
        objs = []
        rest = s
        ok = True
        while rest.strip():
            try:
                obj, idx = dec.raw_decode(rest)
            except Exception:
                ok = False
                break
            objs.append(obj)
            rest = rest[idx:].strip()
        if ok and len(objs) >= 2:
            for o in objs:
                out.append(json.dumps(o, ensure_ascii=False) + "\n")
            fixed += 1
            print("SPLIT into", len(objs), "rows:",
                  [(o.get("tick"), o.get("lane"), o.get("receipt")) for o in objs])
        else:
            print("UNFIXABLE, kept as-is:", s[:200])
            out.append(s + "\n")
p.write_text("".join(out))
print("lines before:", len(lines), "after:", len(out), "fixed lines:", fixed)
# Verify: full re-parse
bad = 0
rows = 0
for line in p.read_text().splitlines():
    rows += 1
    try:
        json.loads(line)
    except Exception:
        bad += 1
print("reparse rows:", rows, "bad:", bad)
