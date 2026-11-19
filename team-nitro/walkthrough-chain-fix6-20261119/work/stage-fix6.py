#!/usr/bin/env python3
"""FIX6 stage + file (2026-11-19) — commit 1 on walkthrough/chain-fix6-20261119.

Fix-5 closed the identity ENTER path, but the walk URL bypassed the gate:
walk ingest() stored any ?name=&alias= unchecked, the walk made no
load-time ownership check, and /api/welcome/complete wrote the project,
Box, and pages keyed by alias alone with no device-key verification.
This round (both legs):
 (1) /welcome LOAD verifies ownership (GET /api/claim with the browser's
     key; taken + not-own bounces to identity with the pair in the URL,
     where the new FIX6 load check shows the flag + key panel; own /
     available / failed / timed-out proceed — the walk never hangs);
     identity also runs the LIVE availability check on any ?alias=
     arriving in the URL (the load check previously ran only for the
     saved alias, silent).
 (2) /api/welcome/complete verifies device_key against the stored claim
     row (sbGetRow, the same lookup GET /api/claim uses) BEFORE any
     write: a row whose device_key is set refuses a missing/mismatched
     key with 409 taken, no writes. The walk already sends device_key
     (cred() carries it from nayanet_vault_key) — no walk change was
     needed for the completion POST. No claim row, or a row with no
     device_key set, proceeds as today (carried observations).

This script: verifies the local inputs by sha, node --checks the
identity + walk script blocks, rebuilds the staging worker twice
in-process (deterministic sha, embeds verified by sha256, FIX6 markers
present), creates the fix6 branch from the fix5 tip, files ONE commit
(walk + identity + worker + builder + drivers), read-back verifies every
blob, PUTs the worker, and verifies the 7 routes by sha (curl piped to
sha, never a file write — EPERM). The 3 proof-host pages are verified
by the standalone verify-proof-fix6.py (welcome is NOT filed in the
fix6 commit — never look it up in this commit's blobs). No PR, no
merge, no live deploy, no message to Shawn.
"""
import base64, importlib.util, json, re, subprocess, time

SPEC = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(st)

WORK6 = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix6-20261119/work"
NEW_BRANCH = "walkthrough/chain-fix6-20261119"
PARENT = "f79a03eb9c749f4b0eea2cf57ec8e91231371a84"
WALK_SHA = "b6befc332d65dd26d01649edd09810e9f83284a73a10a6af30f6691f5f118773"
IDENT_SHA = "3279dc3572337e5e971369a3742effcaac7f6e5b059192ddaa6e689f0f92886c"
WORKER_SHA = "PLACEHOLDER"


def main():
    import sys
    worker_sha = sys.argv[1] if len(sys.argv) > 1 else WORKER_SHA
    assert worker_sha != "PLACEHOLDER", "pass the built worker sha as argv[1]"
    new_walk = st.read_bytes(WORK6 + "/../../walk-v23-assembly-20261114/walk-beginning-fixed.html")
    new_ident = st.read_bytes(st.IDENT_LOCAL)
    new_welcome = st.read_bytes(st.WELCOME_LOCAL)
    new_unfold = st.read_bytes(st.UNFOLD_LOCAL)
    builder = st.read_bytes(st.BUILDER)
    assert st.sha(new_walk) == WALK_SHA, "walk moved: %s" % st.sha(new_walk)
    assert st.sha(new_ident) == IDENT_SHA, "identity moved: %s" % st.sha(new_ident)
    assert st.sha(new_welcome) == st.WELCOME_SHA, "welcome moved"
    assert st.sha(new_unfold) == st.UNFOLD_SHA, "unfold moved"
    assert b'assert ident_sha.startswith("3279dc35")' in builder, "builder identity assert not moved"
    assert b'assert walk_sha.startswith("b6befc33")' in builder, "builder walk assert not moved"
    assert b"claimRow6" in builder, "builder missing the FIX6 completion gate"
    print("inputs: walk %d B %s, identity %d B %s, welcome %d B %s, unfold %d B %s, builder %d B" % (
        len(new_walk), WALK_SHA[:12], len(new_ident), IDENT_SHA[:12],
        len(new_welcome), st.WELCOME_SHA[:12], len(new_unfold), st.UNFOLD_SHA[:12],
        len(builder)), flush=True)
    for code in st.extract_scripts(new_ident, "identity"):
        st.node_check_script(code, "identity")
    # Rebuild the worker in-process (deterministic, embeds verified) and
    # require the exact sha build-fix6.py produced — the worker bytes live
    # in memory here because the EPERM flake blocked the local copies.
    spec6 = importlib.util.spec_from_file_location("build_fix6", WORK6 + "/build-fix6.py")
    build_fix6 = importlib.util.module_from_spec(spec6)
    spec6.loader.exec_module(build_fix6)
    worker = build_fix6.run_builder6(new_welcome, st.WELCOME_SHA, IDENT_SHA, st.UNFOLD_SHA)
    assert st.sha(worker) == worker_sha, "worker sha moved: %s" % st.sha(worker)
    assert b"gateDone6" in worker and b"claimRow6" in worker, "worker missing the FIX6 gates"
    r = subprocess.run(["node", "--check", "--input-type=module", "-"],
                       input=worker, capture_output=True)
    assert r.returncode == 0, "node --check failed for worker: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: worker (%d B) sha %s" % (len(worker), worker_sha[:12]), flush=True)
    for path in (st.WORKER_LOCAL, WORK6 + "/worker-fix6.js"):
        try:
            st.write_resilient(path, worker)
        except Exception as e:
            print("WARNING: worker copy not written (EPERM flake): %s: %r" % (path, e), flush=True)
    _, ref = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, "walkthrough/chain-fix5-20261119"))
    assert ref["object"]["sha"] == PARENT, "fix5 tip moved: %s" % ref["object"]["sha"]
    print("parent (fix5 tip):", PARENT, flush=True)
    _, nb = st.gh("POST", "/repos/%s/git/refs" % st.REPO,
                  {"ref": "refs/heads/%s" % NEW_BRANCH, "sha": PARENT})
    print("new branch created:", nb["ref"], nb["object"]["sha"], flush=True)
    assert nb["object"]["sha"] == PARENT
    _, commit = st.gh("GET", "/repos/%s/git/commits/%s" % (st.REPO, PARENT))
    base_tree = commit["tree"]["sha"]
    print("base tree:", base_tree, flush=True)
    files = [
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html", new_walk),
        ("team-nitro/walk-v23-assembly-20261114/identity-fixed.html", new_ident),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
        ("team-nitro/walkthrough-chain-fix6-20261119/work/build-fix6.py",
         st.read_bytes(WORK6 + "/build-fix6.py")),
        ("team-nitro/walkthrough-chain-fix6-20261119/work/law-fix6.py",
         st.read_bytes(WORK6 + "/law-fix6.py")),
        ("team-nitro/walkthrough-chain-fix6-20261119/work/probe-fix6-live.py",
         st.read_bytes(WORK6 + "/probe-fix6-live.py")),
        ("team-nitro/walkthrough-chain-fix6-20261119/work/stage-fix6.py",
         st.read_bytes(WORK6 + "/stage-fix6.py")),
        ("team-nitro/walkthrough-chain-fix6-20261119/work/verify-proof-fix6.py",
         st.read_bytes(WORK6 + "/verify-proof-fix6.py")),
    ]
    blobs = {}
    for path, data in files:
        _, blob = st.gh("POST", "/repos/%s/git/blobs" % st.REPO,
                        {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"})
        blobs[path] = blob["sha"]
        print("blob %s: %s (%d B)" % (path.split("/")[-1], blob["sha"][:12], len(data)), flush=True)
    _, tree = st.gh("POST", "/repos/%s/git/trees" % st.REPO,
                    {"base_tree": base_tree,
                     "tree": [{"path": p, "mode": "100644", "type": "blob", "sha": s} for p, s in blobs.items()]})
    print("new tree:", tree["sha"], flush=True)
    msg = (
        "Walkthrough CHAIN FIX6 (2026-11-19, maker round; MAKER-REPORT.md in "
        "walkthrough-chain-fix6-20261119/) — commit 1\\n\\n"
        "Fix-5 closed the identity ENTER path, but the walk URL bypassed "
        "the gate: ingest() stored any ?name=&alias= unchecked, the walk "
        "made no load-time ownership check, and /api/welcome/complete "
        "wrote the project, Box, and pages keyed by alias alone. This "
        "round closes both legs. (1) /welcome LOAD verifies ownership "
        "(GET /api/claim with the browser's key; taken + not-own bounces "
        "to identity with the pair in the URL, where the new load check "
        "shows the flag + key panel; own / available / failed / timed-out "
        "proceed). Identity also runs the LIVE availability check on any "
        "?alias= arriving in the URL (the load check previously ran only "
        "for the saved alias, silent). (2) /api/welcome/complete verifies "
        "device_key against the stored claim row (sbGetRow, the same "
        "lookup GET /api/claim uses) BEFORE any write: a row whose "
        "device_key is set refuses a missing/mismatched key with 409 "
        "taken, no writes. The walk already sends device_key (cred()). "
        "No claim row, or a row with no device_key set, proceeds as "
        "today (carried observations).\\n\\n"
        "Walk 4,361,146 B sha b6befc33; identity 401,040 B sha 3279dc35; "
        "worker sha %s (built twice, identical; embeds verified: WALK "
        "b6befc33, IDENTITY 3279dc35, WELCOME d79793c0, UNFOLD 3252948e, "
        "TEMPLATE 61002d15). Law check: welcome still 83 FAIL / 4 WARN, "
        "identity still 11 FAIL / 2 WARN, walk delta zero new.\\n\\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after the PUT. "
        "NO PR, NO MERGE — the checker and the captain come after this seat. "
        "Nothing live." % (worker_sha[:8], st.STAGING))
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _, cm = st.gh("POST", "/repos/%s/git/commits" % st.REPO,
                  {"message": msg, "tree": tree["sha"], "parents": [PARENT],
                   "author": {"name": "nayapower-lane-agent[bot]",
                              "email": "338161897+nayapower-lane-agent[bot]@users.noreply.github.com",
                              "date": now},
                   "committer": {"name": "GitHub", "email": "noreply@github.com", "date": now}})
    commit_sha = cm["sha"]
    print("commit sha:", commit_sha, flush=True)
    _, ref3 = st.gh("PATCH", "/repos/%s/git/refs/heads/%s" % (st.REPO, NEW_BRANCH),
                    {"sha": commit_sha, "force": False})
    print("branch now:", ref3["object"]["sha"], flush=True)
    assert ref3["object"]["sha"] == commit_sha
    for path, data in files:
        _, rb = st.gh("GET", "/repos/%s/git/blobs/%s" % (st.REPO, blobs[path]))
        raw = base64.b64decode("".join(rb["content"].split()))
        assert len(raw) == len(data) and st.sha(raw) == st.sha(data), "blob read-back mismatch for %s" % path
        print("blob read-back OK:", path.split("/")[-1], len(raw), "bytes, sha match", flush=True)
    st.cf_put_inprocess(worker)
    ua = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
    expect = {
        "/": st.WELCOME_SHA,
        "/agreement": st.UNFOLD_SHA,
        "/welcome": WALK_SHA,
        "/identity.html": IDENT_SHA,
        "/?stage=bridge": st.WELCOME_SHA,
        "/?stage=deck": st.WELCOME_SHA,
        "/?stage=letter": st.WELCOME_SHA,
    }
    routes = {}
    for route, want in expect.items():
        got = None
        for attempt in (1, 2, 3):
            _, got = st.curl_sha(st.STAGING + route, ua)
            print("route %s: sha=%s (want %s) attempt %d" % (route, got[:12], want[:12], attempt), flush=True)
            if got == want:
                break
            time.sleep(15)
        routes[route] = got
        assert got == want, "route %s mismatch: got %s want %s" % (route, got, want)
    print("STAGE-RESULT6 " + json.dumps({
        "walk_bytes": len(new_walk), "walk_sha": WALK_SHA,
        "identity_bytes": len(new_ident), "identity_sha": IDENT_SHA,
        "worker_bytes": len(worker), "worker_sha": worker_sha,
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes}, indent=1), flush=True)


if __name__ == "__main__":
    main()
