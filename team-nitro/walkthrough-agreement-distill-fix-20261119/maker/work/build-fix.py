#!/usr/bin/env python3
"""In-memory fix worker build (2026-11-19, agreement-distill fix round):
runs transform-fix.js (distill outputs + counted fixes), reads the edited
local walk file from disk (its sha matches the filed base + the one-line
5e fix), execs the builder in-process with open() patched for UNFOLD and
the three sha asserts re-pointed at the new bytes. Writes NOTHING to disk.
Deterministic: run twice, compare. Prints BUILD-RESULT on success."""
import base64, hashlib, io, json, os, re, subprocess, sys, builtins

WORK = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix-20261119/maker/work"
BUILDER = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py"
UNFOLD_PATH = "/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html"
WALK_PATH = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run_fix():
    r = subprocess.run(["node", WORK + "/transform-fix.js"],
                       capture_output=True, timeout=180)
    assert r.returncode == 0, "transform-fix failed: %s" % r.stderr.decode("utf-8", "replace")[-800:]
    d = json.loads(r.stdout.decode("utf-8"))
    u = base64.b64decode(d["unfold_b64"])
    w = base64.b64decode(d["welcome_b64"])
    assert len(u) == d["unfold_bytes"] and len(w) == d["welcome_bytes"]
    return u, w


def run_builder_once(unfold, welcome):
    src = open(BUILDER, encoding="utf-8").read()
    walk_raw = open(WALK_PATH, "rb").read()
    walk_sha = sha(walk_raw)
    # Re-point the builder's three base asserts at the new bytes.
    src2, n1 = re.subn(r'assert walk_sha\.startswith\("[0-9a-f]+"\)',
                       'assert walk_sha.startswith("%s")' % walk_sha[:8], src)
    assert n1 == 1, "walk assert not found"
    src2, n2 = re.subn(r'assert welcome_sha\.startswith\("[0-9a-f]+"\)',
                       'assert welcome_sha.startswith("%s")' % sha(welcome)[:8], src2)
    assert n2 == 1, "welcome assert not found"
    src2, n3 = re.subn(r'assert unfold_sha\.startswith\("[0-9a-f]+"\)',
                       'assert unfold_sha.startswith("%s")' % sha(unfold)[:8], src2)
    assert n3 == 1, "unfold assert not found"
    src = src2
    real_open = builtins.open

    def patched_open(path, *a, **k):
        if isinstance(path, str) and os.path.abspath(path) == os.path.abspath(UNFOLD_PATH):
            return io.BytesIO(unfold)
        return real_open(path, *a, **k)

    out_buf = io.BytesIO()

    class Out:
        buffer = out_buf

        def write(self, s):
            sys.stderr.write(s)

        def flush(self):
            pass

    class Stdin:
        buffer = io.BytesIO(welcome)

    old_stdout, old_stdin, old_argv = sys.stdout, sys.stdin, sys.argv
    had_raw = "UNFOLD_RAW" in os.environ
    old_raw = os.environ.get("UNFOLD_RAW")
    try:
        builtins.open = patched_open
        sys.stdout = Out()
        sys.stdin = Stdin()
        sys.argv = ["build-v23-staging-worker.py", "--stdout", "--welcome-stdin"]
        if had_raw:
            del os.environ["UNFOLD_RAW"]
        g = {"__name__": "__main__"}
        exec(compile(src, BUILDER, "exec"), g)
    finally:
        builtins.open = real_open
        sys.stdout, sys.stdin, sys.argv = old_stdout, old_stdin, old_argv
        if had_raw:
            os.environ["UNFOLD_RAW"] = old_raw
    return out_buf.getvalue(), walk_sha, len(walk_raw)


def main():
    u, w = run_fix()
    print("fixed unfold: %d B sha %s" % (len(u), sha(u)), flush=True)
    print("fixed welcome: %d B sha %s" % (len(w), sha(w)), flush=True)
    workers = []
    walk_sha = walk_len = None
    for n in range(2):
        wk, walk_sha, walk_len = run_builder_once(u, w)
        print("builder run %d: worker %d B sha=%s" % (n + 1, len(wk), sha(wk)), flush=True)
        workers.append(wk)
    assert workers[0] == workers[1], "worker build not deterministic"
    worker = workers[0]
    print("walk: %d B sha %s" % (walk_len, walk_sha), flush=True)
    for marker in (b"fpFrameAF", b"fpDeckAF", b"af-prog", b"wireProgDistill", b"fpFrame9",
                   b"fpFrame8", b"fpMediaFrame", b"stay on the entrance", b"gateDone6",
                   b"claimRow6", b"dk6", b"verdictChecked", b"checkAliasAvailability",
                   b"fpFixDistill", b"__fpStageEnd", b"__fpHoldThen", b"__fpFromBridge",
                   b"/?stage=", b"showDoor();"):
        assert marker in worker, "worker missing marker %s" % marker
    dec = json.JSONDecoder()
    embeds = {}
    for name in ("WALK", "IDENTITY", "WELCOME", "UNFOLD", "PERSONAL_TEMPLATE"):
        i = worker.find(("const %s = " % name).encode())
        assert i >= 0, "worker missing %s" % name
        j = worker.find(b'"', i)
        val, _ = dec.raw_decode(worker[j:].decode("utf-8"))
        embeds[name] = val.encode("utf-8")
    print("worker embeds: " + ", ".join("%s %d B %s" % (k, len(v), sha(v)[:8]) for k, v in embeds.items()), flush=True)
    assert sha(embeds["WELCOME"]) == sha(w), "worker does not embed the new welcome"
    assert sha(embeds["UNFOLD"]) == sha(u), "worker does not embed the new unfold"
    assert sha(embeds["WALK"]) == walk_sha, "worker does not embed the new walk"
    assert sha(embeds["IDENTITY"]) == "3279dc3572337e5e971369a3742effcaac7f6e5b059192ddaa6e689f0f92886c", "worker identity changed"
    assert sha(embeds["PERSONAL_TEMPLATE"])[:8] == "61002d15", "worker template changed"
    r = subprocess.run(["node", "--check", "--input-type=module", "-"],
                       input=worker, capture_output=True)
    assert r.returncode == 0, "node --check failed for worker: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: worker (%d B) sha %s" % (len(worker), sha(worker)), flush=True)
    print("BUILD-RESULT worker_bytes=%d worker_sha=%s unfold_sha=%s welcome_sha=%s walk_sha=%s walk_bytes=%d" % (
        len(worker), sha(worker), sha(u), sha(w), walk_sha, walk_len), flush=True)
    return u, w, worker


if __name__ == "__main__":
    main()
