#!/usr/bin/env python3
"""Run the v23 staging-worker builder (FIX #2 copy) with WALK/IDENT fed
from pipes and UNFOLD from the recovered 842cae53 bytes.

The builder hardcodes WALK/IDENT/UNFOLD to files on disk; this round's
walk/identity bytes live only in pipes (the EPERM flake blocks writing
them to disk), and the on-disk unfold was overwritten by the agreement
merge round (faea2190) while this round's builder still asserts the
presentation unfold 842cae53 — so the driver reads the builder source,
repoints the three paths, and execs it in-process. argv passes through
(--welcome-stdin --stdout for the pipe-only deploy). The builder's own
asserts (walk / identity / welcome / template / unfold shas) still run
and fail loudly.
"""
import os
import sys

FIX2 = "/home/hatch/workspace/team-nitro/bridge-presentation-fix2-20261117"
SRC = FIX2 + "/build-v23-staging-worker.py"
# WALK/IDENT sources: env vars (bash process substitution /dev/fd paths —
# pipes, never FIFOs: the EPERM flake blocks python writes to FIFO fds)
# or the /tmp FIFO defaults from the earlier pipe-only deploy.
WALK_SRC = os.environ.get("WALK_SRC", "/tmp/bridge-walk.fifo")
IDENT_SRC = os.environ.get("IDENT_SRC", "/tmp/bridge-ident.fifo")
UNFOLD_SRC = os.environ.get("UNFOLD_SRC", FIX2 + "/unfold-842cae53.html")
src = open(SRC, encoding="utf-8").read()
src = src.replace('WALK = ROUND + "/walk-beginning-fixed.html"',
                  'WALK = %r' % WALK_SRC)
src = src.replace('IDENT = ROUND + "/identity-fixed.html"',
                  'IDENT = %r' % IDENT_SRC)
src = src.replace('UNFOLD = "/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html"',
                  'UNFOLD = %r' % UNFOLD_SRC)
assert WALK_SRC in src, "WALK repoint failed"
assert IDENT_SRC in src, "IDENT repoint failed"
assert UNFOLD_SRC in src, "UNFOLD repoint failed"
sys.argv = ["build-v23-staging-worker.py"] + sys.argv[1:]
exec(compile(src, SRC, "exec"), {"__name__": "__main__"})
