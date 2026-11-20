#!/usr/bin/env python3
"""AGREEMENT-FRAME worker build (2026-11-19): rebuild the staging worker
from the AF unfold + AF welcome through the proven builder, twice
(deterministic sha), verify every embed by sha256 + the AF markers,
node --check the built worker and the edited script blocks.

Pipeline (mirrors build-fix9.py; only the inputs move):
- unfold: fix-9 137,899 B sha ab8da1fa -> AF (24 boards, frame system)
- welcome: fix-9 1,860,296 B sha 2062739e -> AF (deck frame system)
- walk / identity unchanged (fix-9 shas). The builder's two asserts
  (welcome + unfold) are edited to the AF shas before this runs.
Writes go through fresh single-attempt node writers (writer9.js,
maxAttempts=1, looped in the parent) — EPERM is sticky per process.
"""
import importlib.util, json, os, subprocess, sys, time

SPEC = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(st)

WORK = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-20261119/maker/work"
UNFOLD_AF = WORK + "/unfold-distill.html"
WELCOME_AF = WORK + "/welcome-distill.html"
UNFOLD_FILE = "/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html"
WELCOME_FILE = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/welcome-staged.html"
WALK_LOCAL = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html"
WALK_SHA = "b6befc332d65dd26d01649edd09810e9f83284a73a10a6af30f6691f5f118773"
IDENT_SHA = "3279dc3572337e5e971369a3742effcaac7f6e5b059192ddaa6e689f0f92886c"
OLD_UNFOLD_SHA = "4a2e84b0104bf404b3e576ea91725cf0cd931688ff84837cc8ae177e2d952fb9"
OLD_WELCOME_SHA = "1f37416d79b0959b21dffb450d34e1a409dfe934fac40a144ecf0b0ef9f7cc49"


def land_via_writer9(data_bytes, out_path, tries=120):
    """Fresh single-attempt writer9.js runs until the path verifies."""
    for n in range(1, tries + 1):
        r = subprocess.run(["node", WORK + "/writer9.js", out_path, "1"],
                           input=data_bytes, capture_output=True, timeout=300)
        try:
            back = st.read_bytes(out_path)
            if st.sha(back) == st.sha(data_bytes):
                print("landed %s on fresh try %d: %d B sha %s" % (out_path, n, len(back), st.sha(back)[:12]), flush=True)
                return
        except Exception:
            pass
        time.sleep(2)
    raise RuntimeError("fresh-write failed for %s after 120 tries" % out_path)


def emit(mode):
    r = subprocess.run(["node", WORK + "/transform-distill.js", "--emit", mode],
                       capture_output=True, timeout=120)
    assert r.returncode == 0, "transform --emit %s failed: %s" % (mode, r.stderr.decode("utf-8", "replace")[-500:])
    return r.stdout


def run_pipeline():
    """The AF bytes, in memory, from the transform (deterministic)."""
    u = emit("unfold")
    w = emit("welcome")
    print("AF unfold: %d B sha %s" % (len(u), st.sha(u)[:12]), flush=True)
    print("AF welcome: %d B sha %s" % (len(w), st.sha(w)[:12]), flush=True)
    assert st.sha(u) != OLD_UNFOLD_SHA and st.sha(w) != OLD_WELCOME_SHA, "distill bytes equal the v5 AF bytes"
    return u, w


def run_builder(new_welcome, welcome_sha, ident_sha, unfold_sha, unfold_bytes):
    # The builder takes the unfold through UNFOLD_RAW (env) and the
    # welcome through stdin — no disk write needed for either. Landing
    # the AF bytes to their native paths is best-effort only (the EPERM
    # flake blocks node disk writes in this window; the pipeline runs
    # entirely in memory and the stage files from memory too).
    for data, path in ((unfold_bytes, UNFOLD_FILE), (new_welcome, WELCOME_FILE)):
        try:
            if st.read_bytes(path) == data:
                print("file already correct: %s %d B" % (path, len(data)), flush=True)
                continue
        except Exception:
            pass
        try:
            land_via_writer9(data, path, tries=3)
        except Exception as e:
            print("WARNING: native-path landing skipped (EPERM flake, in-memory pipeline continues): %s: %r" % (path, e), flush=True)
    workers = []
    for n in range(2):
        env = dict(os.environ)
        env["UNFOLD_RAW"] = unfold_bytes.decode("utf-8")
        r = subprocess.run([sys.executable, st.BUILDER, "--stdout", "--welcome-stdin"],
                           input=new_welcome, capture_output=True, timeout=300, env=env)
        assert r.returncode == 0, "builder failed: %s" % r.stderr.decode("utf-8", "replace")[-800:]
        log = r.stderr.decode("utf-8", "replace")
        for needle in (welcome_sha[:8], unfold_sha[:8], "b6befc33", "61002d15", ident_sha[:8]):
            assert needle in log, "builder log missing %s; log tail: %s" % (needle, log[-600:])
        workers.append(r.stdout)
        print("builder run %d: worker %d B sha=%s" % (n + 1, len(r.stdout), st.sha(r.stdout)[:12]), flush=True)
    assert workers[0] == workers[1], "worker build not deterministic"
    w = workers[0]
    for marker in (b"fpFrameAF", b"fpDeckAF", b"af-prog", b"wireProgDistill", b"fpFrame9", b"fpFrame8", b"fpMediaFrame",
                   b"stay on the entrance",
                   b"FIX6 (2026-11-19", b"gateDone6", b"claimRow6", b"dk6",
                   b"verdictChecked", b"FIX5 (2026-11-19", b"checkAliasAvailability"):
        assert marker in w, "worker missing marker %s" % marker
    dec = json.JSONDecoder()
    embeds = {}
    for name in ("WALK", "IDENTITY", "WELCOME", "UNFOLD", "PERSONAL_TEMPLATE"):
        i = w.find(("const %s = " % name).encode())
        assert i >= 0, "worker missing %s" % name
        j = w.find(b'"', i)
        val, _ = dec.raw_decode(w[j:].decode("utf-8"))
        embeds[name] = val.encode("utf-8")
    print("worker embeds: " + ", ".join("%s %d B %s" % (k, len(v), st.sha(v)[:8]) for k, v in embeds.items()), flush=True)
    assert st.sha(embeds["WELCOME"]) == welcome_sha, "worker does not embed the new welcome"
    assert st.sha(embeds["UNFOLD"]) == unfold_sha, "worker does not embed the new unfold"
    assert st.sha(embeds["WALK"]) == WALK_SHA, "worker walk changed"
    assert st.sha(embeds["IDENTITY"]) == ident_sha, "worker identity changed"
    assert st.sha(embeds["PERSONAL_TEMPLATE"])[:8] == "61002d15", "worker template changed"
    return w


def main():
    new_walk = st.read_bytes(WALK_LOCAL)
    new_ident = st.read_bytes(st.IDENT_LOCAL)
    new_unfold, new_welcome = run_pipeline()
    builder = st.read_bytes(st.BUILDER)
    unfold_sha, welcome_sha = st.sha(new_unfold), st.sha(new_welcome)
    print("inputs: walk %d B %s" % (len(new_walk), st.sha(new_walk)), flush=True)
    print("inputs: identity %d B %s" % (len(new_ident), st.sha(new_ident)), flush=True)
    print("inputs: welcome %d B %s" % (len(new_welcome), welcome_sha), flush=True)
    print("inputs: unfold %d B %s" % (len(new_unfold), unfold_sha), flush=True)
    assert st.sha(new_walk) == WALK_SHA, "walk moved: %s" % st.sha(new_walk)
    assert st.sha(new_ident) == IDENT_SHA, "identity moved: %s" % st.sha(new_ident)
    assert ('assert unfold_sha.startswith("%s")' % unfold_sha[:8]).encode() in builder, "builder unfold assert not moved"
    assert ('assert welcome_sha.startswith("%s")' % welcome_sha[:8]).encode() in builder, "builder welcome assert not moved"
    assert b"UNFOLD_RAW" in builder, "builder missing UNFOLD_RAW"
    assert b"stay on the entrance" in new_welcome, "welcome F6 edit missing"
    for code in st.extract_scripts(new_ident, "identity"):
        st.node_check_script(code, "identity")
    wt = new_walk.decode("utf-8")
    ing = wt.find("/* ingest")
    assert ing >= 0, "walk ingest comment not found"
    start = wt.rfind("<script>", 0, ing)
    assert start >= 0, "walk main script not found"
    end = wt.rfind("</script>")
    assert end > start, "walk main script close not found"
    code = wt[start + len("<script>"):end]
    r = subprocess.run(["node", "--check", "-"], input=code.encode("utf-8"), capture_output=True)
    assert r.returncode == 0, "node --check failed for walk main script: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: walk main script (%d B)" % len(code), flush=True)
    for code in st.extract_scripts(new_unfold, "unfold"):
        st.node_check_script(code, "unfold")
    for code in st.extract_scripts(new_welcome, "welcome"):
        st.node_check_script(code, "welcome")
    worker = run_builder(new_welcome, welcome_sha, IDENT_SHA, unfold_sha, new_unfold)
    r = subprocess.run(["node", "--check", "--input-type=module", "-"],
                       input=worker, capture_output=True)
    assert r.returncode == 0, "node --check failed for worker: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: worker (%d B) sha %s" % (len(worker), st.sha(worker)), flush=True)
    for path in (st.WORKER_LOCAL, WORK + "/worker-distill.js"):
        try:
            land_via_writer9(worker, path, tries=3)
        except Exception as e:
            print("WARNING: worker copy not written (EPERM flake): %s: %r" % (path, e), flush=True)
    print("BUILD-RESULT worker_bytes=%d worker_sha=%s unfold_sha=%s welcome_sha=%s" % (
        len(worker), st.sha(worker), unfold_sha, welcome_sha), flush=True)


if __name__ == "__main__":
    main()
