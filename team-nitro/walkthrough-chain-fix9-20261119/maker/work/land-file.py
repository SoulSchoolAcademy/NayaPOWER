#!/usr/bin/env python3
"""FIX9 land-file loop (2026-11-19): hold local-file bytes in memory and
spawn FRESH single-attempt node writers until the target verifies.
(Same sticky-EPERM lesson as restore-loop2.py: one process retrying
never lands; fresh processes do.) Usage:
python3 land-file.py <src_path> <want_sha> <out_path>
"""
import hashlib, subprocess, sys, time

SRC, WANT_SHA, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
WRITER = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix9-20261119/maker/work/writer9.js"

with open(SRC, "rb") as f:
    raw = f.read()
assert hashlib.sha256(raw).hexdigest() == WANT_SHA, "source sha mismatch"
print("source %s: %d B sha %s (held in memory)" % (SRC, len(raw), WANT_SHA[:12]), flush=True)
for n in range(1, 121):
    r = subprocess.run(["node", WRITER, OUT, "1"], input=raw,
                       capture_output=True, timeout=60)
    try:
        with open(OUT, "rb") as f:
            back = f.read()
        if hashlib.sha256(back).hexdigest() == WANT_SHA:
            print("LANDED on try %d: %s %d B sha %s" % (n, OUT, len(back), WANT_SHA[:12]), flush=True)
            sys.exit(0)
    except Exception:
        pass
    if n % 10 == 0:
        print("try %d: not yet" % n, flush=True)
    time.sleep(1)
print("NOT LANDED after 120 fresh tries", flush=True)
sys.exit(1)
