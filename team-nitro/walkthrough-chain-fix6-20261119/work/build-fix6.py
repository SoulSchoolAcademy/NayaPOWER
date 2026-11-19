#!/usr/bin/env python3
"""FIX6 worker build (2026-11-19): rebuild the staging worker from the edited
walk + identity through the proven builder, twice (deterministic sha), verify
every embed by sha256 + the FIX6 markers, node --check the built worker and
the edited script blocks. Adapted from build-fix5.py; run_builder is copied
from stage-fix3.py with the walk sha + FIX6 markers (stage-fix3's own
run_builder hard-codes the fix-4 walk sha needle, so it cannot be reused
unpatched for a walk change).

New shas (computed, never typed into the asserts by hand — asserted here):
  walk b6befc33... (4,361,146 B), identity 3279dc35... (401,040 B).
Writes the worker to the V23 worker file and to work/worker-fix6.js via
write_resilient (chunked writes + verify; EPERM flake live). If the local
copies cannot land, the in-memory bytes are still filed by stage-fix6.py.
"""
import importlib.util, json, re, subprocess, sys

SPEC = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(st)

WORK = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix6-20261119/work"
WALK_LOCAL = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html"
WALK_SHA = "b6befc332d65dd26d01649edd09810e9f83284a73a10a6af30f6691f5f118773"
IDENT_SHA = "3279dc3572337e5e971369a3742effcaac7f6e5b059192ddaa6e689f0f92886c"


def run_builder6(new_welcome, welcome_sha, ident_sha, unfold_sha):
    workers = []
    for n in range(2):
        r = subprocess.run([sys.executable, st.BUILDER, "--stdout", "--welcome-stdin"],
                           input=new_welcome, capture_output=True, timeout=300)
        assert r.returncode == 0, "builder failed: %s" % r.stderr.decode("utf-8", "replace")[-800:]
        log = r.stderr.decode("utf-8", "replace")
        for needle in (welcome_sha[:8], unfold_sha[:8], "b6befc33", "61002d15", ident_sha[:8]):
            assert needle in log, "builder log missing %s; log tail: %s" % (needle, log[-600:])
        workers.append(r.stdout)
        print("builder run %d: worker %d B sha=%s" % (n + 1, len(r.stdout), st.sha(r.stdout)[:12]), flush=True)
    assert workers[0] == workers[1], "worker build not deterministic"
    w = workers[0]
    for marker in (b"FIX6 (2026-11-19", b"gateDone6", b"claimRow6", b"dk6",
                   b"verdictChecked", b"FIX5 (2026-11-19", b"checkAliasAvailability"):
        assert marker in w, "worker missing FIX6/FIX5 marker %s" % marker
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
    new_unfold = st.read_bytes(st.UNFOLD_LOCAL)
    print("inputs: walk %d B %s" % (len(new_walk), st.sha(new_walk)), flush=True)
    print("inputs: identity %d B %s" % (len(new_ident), st.sha(new_ident)), flush=True)
    print("inputs: welcome %d B %s" % (len(new_welcome), st.sha(new_welcome)), flush=True)
    print("inputs: unfold %d B %s" % (len(new_unfold), st.sha(new_unfold)), flush=True)
    assert st.sha(new_walk) == WALK_SHA, "walk moved: %s" % st.sha(new_walk)
    assert st.sha(new_ident) == IDENT_SHA, "identity moved: %s" % st.sha(new_ident)
    assert st.sha(new_welcome) == st.WELCOME_SHA, "welcome moved"
    assert st.sha(new_unfold) == st.UNFOLD_SHA, "unfold moved"
    # node --check the edited script blocks: identity (all blocks) + walk
    # main script (the block opened just before the ingest comment; matched
    # to its closing tag before </body>, so </script> literals inside
    # strings cannot truncate it the way the naive regex would).
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
    worker = run_builder6(new_welcome, st.WELCOME_SHA, IDENT_SHA, st.UNFOLD_SHA)
    r = subprocess.run(["node", "--check", "--input-type=module", "-"],
                       input=worker, capture_output=True)
    assert r.returncode == 0, "node --check failed for worker: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: worker (%d B) sha %s" % (len(worker), st.sha(worker)), flush=True)
    for path in (st.WORKER_LOCAL, WORK + "/worker-fix6.js"):
        try:
            st.write_resilient(path, worker)
        except Exception as e:
            print("WARNING: worker copy not written (EPERM flake): %s: %r" % (path, e), flush=True)
    print("BUILD-RESULT worker_bytes=%d worker_sha=%s" % (len(worker), st.sha(worker)), flush=True)


if __name__ == "__main__":
    main()
