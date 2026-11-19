#!/usr/bin/env python3
"""FIX9 restore loop v2 (2026-11-19): the EPERM is STICKY per process —
once a process takes one EPERM, its later writes keep failing even when
the window opens. A retry loop inside one process therefore never
lands. The fix is fresh single-attempt writers: fetch the filed blob
once, hold the bytes in memory, and spawn a FRESH node writer (1
attempt) per try until the file verifies. Usage:
python3 restore-loop2.py <blob> <want_sha> <want_bytes> <out_path>
"""
import base64, hashlib, importlib.util, subprocess, sys, time

SPEC = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(st)

BLOB, WANT_SHA, WANT_BYTES, OUT = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
WRITER = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix9-20261119/maker/work/writer9.js"

_, d = st.gh("GET", "/repos/%s/git/blobs/%s" % (st.REPO, BLOB))
raw = base64.b64decode("".join(d["content"].split()))
assert len(raw) == WANT_BYTES and hashlib.sha256(raw).hexdigest() == WANT_SHA, "blob mismatch"
print("blob %s: %d B sha %s (held in memory)" % (BLOB[:8], len(raw), WANT_SHA[:12]), flush=True)
for n in range(1, 121):
    r = subprocess.run(["node", WRITER, OUT, "1"], input=raw,
                       capture_output=True, timeout=60)
    try:
        back = st.read_bytes(OUT)
        if len(back) == WANT_BYTES and hashlib.sha256(back).hexdigest() == WANT_SHA:
            print("LANDED on try %d: %s %d B sha %s" % (n, OUT, len(back), WANT_SHA[:12]), flush=True)
            sys.exit(0)
    except Exception:
        pass
    if n % 10 == 0:
        print("try %d: not yet (%s)" % (n, r.stderr.decode("utf-8", "replace").strip().splitlines()[-1] if r.stderr else "?"), flush=True)
    time.sleep(1)
print("NOT LANDED after 120 fresh tries", flush=True)
sys.exit(1)
