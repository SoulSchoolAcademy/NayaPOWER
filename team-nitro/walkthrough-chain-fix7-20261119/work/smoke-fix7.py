#!/usr/bin/env python3
"""FIX7 smoke test (in-memory only, no disk writes): extract base from the
worker embed, transform to fix-7 bytes, build the worker twice via the
builder with UNFOLD_RAW in env, verify embeds + markers, print worker sha.
Proves the chain before build-fix7.py / stage-fix7.py are written."""
import hashlib, json, subprocess, sys

WORK = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix7-20261119/work"
PROBE = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix7-20261119/probe2"
BUILDER = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py"
WELCOME_LOCAL = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/welcome-staged.html"
UNFOLD_SHA = "e21f08d0fcd1ae2a299065697a3bba43354c7210b68271ab0f0e1a00026e6671"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    r = subprocess.run(["node", WORK + "/transform-fix7-stdout2.js"],
                       capture_output=True, timeout=120)
    print("transform stderr:", r.stderr.decode("utf-8", "replace")[-400:], flush=True)
    fix7 = r.stdout
    print("fix7 bytes:", len(fix7), "sha:", sha(fix7)[:12], flush=True)
    assert len(fix7) == 117636 and sha(fix7) == UNFOLD_SHA, "fix7 bytes moved"
    welcome = open(WELCOME_LOCAL, "rb").read()
    print("welcome:", len(welcome), "sha:", sha(welcome)[:12], flush=True)
    workers = []
    for n in range(2):
        import os
        env = dict(os.environ)
        env["UNFOLD_RAW"] = fix7.decode("utf-8")
        r = subprocess.run([sys.executable, BUILDER, "--stdout", "--welcome-stdin"],
                           input=welcome, capture_output=True, timeout=300, env=env)
        print("builder run %d rc=%d" % (n + 1, r.returncode), flush=True)
        print("builder log tail:", r.stderr.decode("utf-8", "replace")[-500:], flush=True)
        assert r.returncode == 0, "builder failed"
        workers.append(r.stdout)
        print("worker %d: %d B sha %s" % (n + 1, len(r.stdout), sha(r.stdout)[:12]), flush=True)
    assert workers[0] == workers[1], "worker build not deterministic"
    w = workers[0]
    for marker in (b"fpFrame7", b"FIX6 (2026-11-19", b"gateDone6", b"claimRow6"):
        assert marker in w, "worker missing marker %s" % marker
    dec = json.JSONDecoder()
    for name in ("WALK", "IDENTITY", "WELCOME", "UNFOLD", "PERSONAL_TEMPLATE"):
        i = w.find(("const %s = " % name).encode())
        assert i >= 0, "worker missing %s" % name
        j = w.find(b'"', i)
        val, _ = dec.raw_decode(w[j:].decode("utf-8"))
        print("embed %s: %d B sha %s" % (name, len(val), sha(val.encode("utf-8"))[:12]), flush=True)
    print("SMOKE-OK worker_sha=%s worker_bytes=%d" % (sha(w), len(w)), flush=True)


if __name__ == "__main__":
    main()
