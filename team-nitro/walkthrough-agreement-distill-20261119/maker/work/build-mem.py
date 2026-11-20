#!/usr/bin/env python3
"""In-memory distill worker build (2026-11-19, EPERM-flake workaround):
the transform's bytes never touch disk (disk writes are 0-byte/EPERM in
this window — only the file tool lands, and it cannot take a pipe).
The builder is exec'd in-process with open() patched for the UNFOLD path
(the 141KB unfold exceeds the 128KB single-env-string limit, so the
UNFOLD_RAW env path that served v5 cannot carry it) and stdin/stdout
captured. Writes NOTHING to disk. Deterministic: run twice, compare."""
import hashlib, io, json, os, subprocess, sys, builtins

WORK = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-20261119/maker/work"
BUILDER = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py"
UNFOLD_PATH = "/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html"
UNFOLD_SHA = "760b8ea05fb5"
WELCOME_SHA = "85ae106d47e9"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def emit(mode):
    r = subprocess.run(["node", WORK + "/transform-distill.js", "--emit", mode],
                       capture_output=True, timeout=120)
    assert r.returncode == 0, "transform --emit %s failed: %s" % (mode, r.stderr.decode("utf-8", "replace")[-500:])
    return r.stdout


def run_builder_once(unfold, welcome):
    src = open(BUILDER, encoding="utf-8").read()
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
    return out_buf.getvalue()


def build_worker():
    u = emit("unfold")
    w = emit("welcome")
    print("distill unfold: %d B sha %s" % (len(u), sha(u)[:12]), flush=True)
    print("distill welcome: %d B sha %s" % (len(w), sha(w)[:12]), flush=True)
    assert sha(u).startswith(UNFOLD_SHA), "unfold sha moved: %s" % sha(u)
    assert sha(w).startswith(WELCOME_SHA), "welcome sha moved: %s" % sha(w)
    workers = []
    for n in range(2):
        wk = run_builder_once(u, w)
        print("builder run %d: worker %d B sha=%s" % (n + 1, len(wk), sha(wk)[:12]), flush=True)
        workers.append(wk)
    assert workers[0] == workers[1], "worker build not deterministic"
    worker = workers[0]
    for marker in (b"fpFrameAF", b"fpDeckAF", b"af-prog", b"wireProgDistill", b"fpFrame9",
                   b"fpFrame8", b"fpMediaFrame", b"stay on the entrance", b"gateDone6",
                   b"claimRow6", b"dk6", b"verdictChecked", b"checkAliasAvailability"):
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
    assert sha(embeds["WELCOME"]).startswith(WELCOME_SHA), "worker does not embed the new welcome"
    assert sha(embeds["UNFOLD"]).startswith(UNFOLD_SHA), "worker does not embed the new unfold"
    assert sha(embeds["WALK"]) == "b6befc332d65dd26d01649edd09810e9f83284a73a10a6af30f6691f5f118773", "worker walk changed"
    assert sha(embeds["IDENTITY"]) == "3279dc3572337e5e971369a3742effcaac7f6e5b059192ddaa6e689f0f92886c", "worker identity changed"
    assert sha(embeds["PERSONAL_TEMPLATE"])[:8] == "61002d15", "worker template changed"
    r = subprocess.run(["node", "--check", "--input-type=module", "-"],
                       input=worker, capture_output=True)
    assert r.returncode == 0, "node --check failed for worker: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: worker (%d B) sha %s" % (len(worker), sha(worker)), flush=True)
    return u, w, worker


if __name__ == "__main__":
    u, w, worker = build_worker()
    print("BUILD-RESULT worker_bytes=%d worker_sha=%s unfold_sha=%s welcome_sha=%s" % (
        len(worker), sha(worker), sha(u), sha(w)), flush=True)
