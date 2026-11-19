#!/usr/bin/env python3
"""FIX9 worker build (2026-11-19): rebuild the staging worker from the
fix-9 unfold + the fix-8 welcome (unchanged) through the proven builder,
twice (deterministic sha), verify every embed by sha256 + the FIX9
markers, node --check the built worker and the edited script blocks.

Mirrors build-fix8.py exactly (same pipeline, same guards, same
write paths — the EPERM-flake rules that governed fix-8 govern here:
the unfold bytes never touch disk through python; the transform runs
in node and hands its bytes to the builder through the builder's
native UNFOLD file path, written by node from stdin and sha-verified
after the write; worker copies go through write_resilient, warned
not fatal). The only inputs that move vs fix-8 are the unfold bytes
(131,797 B sha 11130770 -> 137,899 B sha ab8da1fa) and the builder's
unfold assert (line 536 -> ab8da1fa). Walk / identity / welcome are
unchanged (fix-8 shas).
"""
import importlib.util, json, os, subprocess, sys

SPEC = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(st)

WORK = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix9-20261119/maker/work"
UNFOLD_FILE = "/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html"
WALK_LOCAL = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html"
WALK_SHA = "b6befc332d65dd26d01649edd09810e9f83284a73a10a6af30f6691f5f118773"
IDENT_SHA = "3279dc3572337e5e971369a3742effcaac7f6e5b059192ddaa6e689f0f92886c"
WELCOME_SHA = "2062739ecb968b78cd823440bcfd4bbb8f7d0190d3bb2e5443ab3b35c0081955"
UNFOLD_SHA = "ab8da1faf825d9d24e3f4991063e81c052738502063d9e89f4479730fa94348f"
UNFOLD_BYTES = 137899


def run_pipeline():
    """Build the fix-9 unfold bytes in memory. No disk writes."""
    r = subprocess.run(["node", WORK + "/transform-fix9.js"],
                       capture_output=True, timeout=120)
    print("transform stderr:", r.stderr.decode("utf-8", "replace")[-400:], flush=True)
    assert r.returncode == 0, "transform failed"
    fix9 = r.stdout
    print("fix9 bytes: %d sha %s" % (len(fix9), st.sha(fix9)[:12]), flush=True)
    assert len(fix9) == UNFOLD_BYTES and st.sha(fix9) == UNFOLD_SHA, "fix9 bytes moved"
    return fix9


def write_unfold_file(unfold_bytes):
    """Hand the unfold to the builder through its native UNFOLD file
    path. If the file already holds these exact bytes (a previous
    landed write), no write is needed — never rewrite a correct file
    through a flake window. Otherwise the proven chunked stdin-writer
    (writer9.js) lands the bytes; the write is sha-verified on
    read-back before any build."""
    try:
        if st.read_bytes(UNFOLD_FILE) == unfold_bytes:
            print("unfold file already correct: %d B sha %s" % (len(unfold_bytes), st.sha(unfold_bytes)[:12]), flush=True)
            return
    except Exception:
        pass
    r = subprocess.run(["node", WORK + "/writer9.js", UNFOLD_FILE, "40"],
                       input=unfold_bytes, capture_output=True, timeout=300)
    assert r.returncode == 0, "node unfold write failed: %s" % r.stderr.decode("utf-8", "replace")[-400:]
    back = st.read_bytes(UNFOLD_FILE)
    assert st.sha(back) == st.sha(unfold_bytes), "unfold file write mismatch"
    print("unfold file written via node: %d B sha %s" % (len(back), st.sha(back)[:12]), flush=True)


def run_builder9(new_welcome, welcome_sha, ident_sha, unfold_sha, unfold_bytes):
    write_unfold_file(unfold_bytes)
    workers = []
    for n in range(2):
        env = dict(os.environ)
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
    for marker in (b"fpFrame9", b"fpFrame8", b"fpMediaFrame",
                   b"stay on the entrance",
                   b"FIX6 (2026-11-19", b"gateDone6", b"claimRow6", b"dk6",
                   b"verdictChecked", b"FIX5 (2026-11-19", b"checkAliasAvailability"):
        assert marker in w, "worker missing FIX9/FIX8/FIX7/FIX6 marker %s" % marker
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
    new_welcome = st.read_bytes(st.WELCOME_LOCAL)
    new_unfold = run_pipeline()
    builder = st.read_bytes(st.BUILDER)
    print("inputs: walk %d B %s" % (len(new_walk), st.sha(new_walk)), flush=True)
    print("inputs: identity %d B %s" % (len(new_ident), st.sha(new_ident)), flush=True)
    print("inputs: welcome %d B %s" % (len(new_welcome), st.sha(new_welcome)), flush=True)
    print("inputs: unfold %d B %s" % (len(new_unfold), st.sha(new_unfold)), flush=True)
    assert st.sha(new_walk) == WALK_SHA, "walk moved: %s" % st.sha(new_walk)
    assert st.sha(new_ident) == IDENT_SHA, "identity moved: %s" % st.sha(new_ident)
    assert st.sha(new_welcome) == WELCOME_SHA, "welcome moved: %s" % st.sha(new_welcome)
    assert st.sha(new_unfold) == UNFOLD_SHA, "unfold moved"
    assert b'assert unfold_sha.startswith("ab8da1fa")' in builder, "builder unfold assert not moved"
    assert b'assert welcome_sha.startswith("2062739e")' in builder, "builder welcome assert not moved"
    assert b'UNFOLD_RAW' in builder, "builder missing UNFOLD_RAW"
    assert b"stay on the entrance" in new_welcome, "welcome F6 edit missing"
    assert b"enterStage();}" not in new_welcome.split(b"stay on the entrance")[0][-400:], "welcome auto-enter still present near F6"
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
    worker = run_builder9(new_welcome, WELCOME_SHA, IDENT_SHA, UNFOLD_SHA, new_unfold)
    r = subprocess.run(["node", "--check", "--input-type=module", "-"],
                       input=worker, capture_output=True)
    assert r.returncode == 0, "node --check failed for worker: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: worker (%d B) sha %s" % (len(worker), st.sha(worker)), flush=True)
    for path in (st.WORKER_LOCAL, WORK + "/worker-fix9.js"):
        try:
            st.write_resilient(path, worker)
        except Exception as e:
            print("WARNING: worker copy not written (EPERM flake): %s: %r" % (path, e), flush=True)
    print("BUILD-RESULT worker_bytes=%d worker_sha=%s" % (len(worker), st.sha(worker)), flush=True)


if __name__ == "__main__":
    main()
