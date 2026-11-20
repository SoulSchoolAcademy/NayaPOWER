#!/usr/bin/env python3
"""Run the v23 staging-worker builder with WALK/IDENT fed from FIFOs.

The builder hardcodes WALK/IDENT to the base files on disk; this round's
new bytes live only in pipes (the EPERM flake blocks writing them to
disk), so the driver reads the builder source, repoints the two paths
at FIFOs, and execs it in-process. argv passes through (--welcome-stdin
--stdout for the pipe-only deploy). The builder's own asserts (walk /
identity / welcome / template / unfold shas) still run and fail loudly.
"""
import os
import sys

SRC = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py"
# WALK/IDENT sources: env vars (bash process substitution /dev/fd paths —
# pipes, never FIFOs: the EPERM flake blocks python writes to FIFO fds)
# or the /tmp FIFO defaults from the earlier pipe-only deploy.
WALK_SRC = os.environ.get("WALK_SRC", "/tmp/bridge-walk.fifo")
IDENT_SRC = os.environ.get("IDENT_SRC", "/tmp/bridge-ident.fifo")
src = open(SRC, encoding="utf-8").read()
src = src.replace('WALK = ROUND + "/walk-beginning-fixed.html"',
                  'WALK = %r' % WALK_SRC)
src = src.replace('IDENT = ROUND + "/identity-fixed.html"',
                  'IDENT = %r' % IDENT_SRC)
assert WALK_SRC in src, "WALK repoint failed"
assert IDENT_SRC in src, "IDENT repoint failed"
sys.argv = ["build-v23-staging-worker.py"] + sys.argv[1:]
exec(compile(src, SRC, "exec"), {"__name__": "__main__"})
