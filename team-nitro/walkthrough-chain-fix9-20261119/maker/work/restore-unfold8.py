#!/usr/bin/env python3
"""FIX9 restore (2026-11-19): the local fix-8 unfold working copy was
truncated to 0 bytes by a failed truncate-first write (EPERM flake).
Restore it from its FILED blob de7970d2 (131,797 B, sha256 11130770),
fetched via the git blob API and piped to the safe temp+verify+replace
writer. Python never writes a file itself. Usage:
python3 restore-unfold8.py
"""
import base64, hashlib, importlib.util, subprocess, sys

SPEC = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(st)

BLOB = "de7970d2c6cf577ca64b9404aff332031b953bfd"
WANT_SHA = "11130770398575ba407da0f9acca254d946c03daa76852cfebc1763bd76bff32"
WANT_BYTES = 131797
OUT = "/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html"
WRITER = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix9-20261119/maker/work/writer9.js"

_, d = st.gh("GET", "/repos/%s/git/blobs/%s" % (st.REPO, BLOB))
raw = base64.b64decode("".join(d["content"].split()))
print("blob %s: %d B sha %s" % (BLOB[:8], len(raw), hashlib.sha256(raw).hexdigest()[:12]), flush=True)
assert len(raw) == WANT_BYTES and hashlib.sha256(raw).hexdigest() == WANT_SHA, "blob is not the fix-8 unfold"
r = subprocess.run(["node", WRITER, OUT, "40"], input=raw, capture_output=True, timeout=300)
print(r.stderr.decode("utf-8", "replace"), flush=True)
assert r.returncode == 0, "writer failed"
back = st.read_bytes(OUT)
assert len(back) == WANT_BYTES and hashlib.sha256(back).hexdigest() == WANT_SHA, "restore verify failed"
print("RESTORED: %s %d B sha %s" % (OUT, len(back), hashlib.sha256(back).hexdigest()[:12]), flush=True)
