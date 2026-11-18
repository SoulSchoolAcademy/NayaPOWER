#!/usr/bin/env python3
"""FIX2 builder CORS patch: insert the OPTIONS preflight branch into the
embedded worker source inside build-v23-staging-worker.py.
The worker source in the builder is a Python string with literal \\n
escapes, so the match is built with chr(92) + 'n' explicitly."""
import hashlib, os, sys, time

BS = chr(92)
P = os.path.expanduser("~/workspace/team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py")
old = ("async fetch(req, env) {\n    const u = new URL(req.url);\n    const p = u.pathname;\n\n    // ---- same-origin claim: write name + alias, read the row back ----")
new = ("async fetch(req, env) {\n    const u = new URL(req.url);\n    const p = u.pathname;\n\n    // ---- FIX2 (2026-11-18, eye item 4): CORS preflight for /api/* - the identity page calls /api/claim from the proof host too (absolute API base), and a POST with Content-Type: application/json preflights. Without this the browser blocks the claim before it is sent, so the proof-host claim never goes through. ----\n    if (req.method === \"OPTIONS\" && p.startsWith(\"/api/\")) { return new Response(null, { status: 204, headers: JSONH }); }\n\n    // ---- same-origin claim: write name + alias, read the row back ----")

def read_bytes(p):
    with open(p, "rb") as f:
        return f.read()

def write_resilient(path, data, attempts=30):
    tmp = path + ".tmpfix2"
    for n in range(attempts):
        try:
            with open(tmp, "wb") as f:
                for i in range(0, len(data), 8192):
                    f.write(data[i:i + 8192])
                f.flush()
                os.fsync(f.fileno())
            got = read_bytes(tmp)
            if len(got) == len(data) and hashlib.sha256(got).hexdigest() == hashlib.sha256(data).hexdigest():
                os.replace(tmp, path)
                got2 = read_bytes(path)
                assert len(got2) == len(data) and hashlib.sha256(got2).hexdigest() == hashlib.sha256(data).hexdigest()
                return True
        except Exception as e:
            print("retry %d: %r" % (n, e), flush=True)
        time.sleep(2)
    return False

data = read_bytes(P)
txt = data.decode("utf-8")
print("JSONH CORS present:", "access-control-allow-origin" in txt, flush=True)
print("OPTIONS branch present:", 'req.method === "OPTIONS"' in txt, flush=True)
assert txt.count(old) == 1, "old fetch-handler head not found exactly once: %d" % txt.count(old)
assert 'req.method === "OPTIONS"' not in txt, "OPTIONS branch already present"
txt2 = txt.replace(old, new, 1)
assert txt2.count("OPTIONS") == 2, "OPTIONS count wrong after patch"
ok = write_resilient(P, txt2.encode("utf-8"))
print("patched:", ok, "new bytes:", len(txt2.encode("utf-8")), flush=True)
if not ok:
    sys.exit(1)
print("sha:", hashlib.sha256(read_bytes(P)).hexdigest()[:16], flush=True)
