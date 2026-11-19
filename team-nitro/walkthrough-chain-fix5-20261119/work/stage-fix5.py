#!/usr/bin/env python3
"""FIX5 stage + file (2026-11-19) — commit 1 on walkthrough/chain-fix5-20261119.

The captain's cloud eye (04:53-05:02Z) claimed taken alias "jordantest" on
what it called a fresh device and saw no "already claimed" flag and no
device-key prompt — ENTER went straight to /welcome. Diagnosis (from the
filed bytes + live API probes, see MAKER-REPORT.md): the typing check is
debounced 300ms and ENTER never consulted it, so a fast ENTER claimed
blind. The fix is the FIX5 gate in activateAndRedirect: ENTER resolves
the availability verdict FIRST (same /api/claim GET the typing check
uses); taken shows the flag + the key panel and returns with no
localStorage write and no claim POST; own/available fall through to the
claim below, and a failed or timed-out verdict falls through too. The
claim POST stays the authority; the worker claim handler is untouched.

This script: verifies the local inputs by sha, node --checks the identity
script block, rebuilds the staging worker twice in-process (deterministic
sha, embeds verified by sha256, FIX5 marker present), creates the fix5
branch from the fix4 tip, files ONE commit (identity + worker + builder +
drivers), read-back verifies every blob, PUTs the worker, and verifies
the 7 routes by sha (curl piped to sha, never a file write — EPERM).
The 2 proof-host pages are verified by the standalone
verify-proof-fix5.py (the stage-fix4.py KeyError trap: welcome was NOT
filed in the fix4 commit, and is not filed in fix5 either — never look
it up in this commit's blobs). No PR, no merge, no live deploy, no
message to Shawn.
"""
import base64, importlib.util, json, re, subprocess, time

SPEC = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(st)

WORK5 = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix5-20261119/work"
NEW_BRANCH = "walkthrough/chain-fix5-20261119"
PARENT = "0c436d580256b2be0d2b05131d5c0e7234b24c86"
IDENT_SHA = "6f805eba00fa7ccbf89103c46878c352e73db5b26792010dc2de535c706418f0"
WORKER_SHA = "PLACEHOLDER"


def main():
    import sys
    worker_sha = sys.argv[1] if len(sys.argv) > 1 else WORKER_SHA
    assert worker_sha != "PLACEHOLDER", "pass the built worker sha as argv[1]"
    new_ident = st.read_bytes(st.IDENT_LOCAL)
    new_welcome = st.read_bytes(st.WELCOME_LOCAL)
    new_unfold = st.read_bytes(st.UNFOLD_LOCAL)
    builder = st.read_bytes(st.BUILDER)
    assert st.sha(new_ident) == IDENT_SHA, "identity moved: %s" % st.sha(new_ident)
    assert st.sha(new_welcome) == st.WELCOME_SHA, "welcome moved"
    assert st.sha(new_unfold) == st.UNFOLD_SHA, "unfold moved"
    assert b'assert ident_sha.startswith("6f805eba")' in builder, "builder assert not moved"
    print("inputs: identity %d B %s, welcome %d B %s, unfold %d B %s, builder %d B" % (
        len(new_ident), IDENT_SHA[:12], len(new_welcome), st.WELCOME_SHA[:12],
        len(new_unfold), st.UNFOLD_SHA[:12], len(builder)), flush=True)
    for code in st.extract_scripts(new_ident, "identity"):
        st.node_check_script(code, "identity")
    worker = st.run_builder(new_welcome, st.WELCOME_SHA, IDENT_SHA, st.UNFOLD_SHA)
    assert st.sha(worker) == worker_sha, "worker sha moved: %s" % st.sha(worker)
    assert b"verdictChecked" in worker, "worker missing the FIX5 gate"
    r = subprocess.run(["node", "--check", "--input-type=module", "-"],
                       input=worker, capture_output=True)
    assert r.returncode == 0, "node --check failed for worker: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: worker (%d B) sha %s" % (len(worker), worker_sha[:12]), flush=True)
    for path, data in ((st.WORKER_LOCAL, worker), (WORK5 + "/worker-fix5.js", worker)):
        try:
            st.write_resilient(path, data)
        except Exception as e:
            print("WARNING: worker copy not written (EPERM flake): %s: %r" % (path, e), flush=True)
    _, ref = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, "walkthrough/chain-fix4-20261119"))
    assert ref["object"]["sha"] == PARENT, "fix4 tip moved: %s" % ref["object"]["sha"]
    print("parent (fix4 tip):", PARENT, flush=True)
    _, nb = st.gh("POST", "/repos/%s/git/refs" % st.REPO,
                  {"ref": "refs/heads/%s" % NEW_BRANCH, "sha": PARENT})
    print("new branch created:", nb["ref"], nb["object"]["sha"], flush=True)
    assert nb["object"]["sha"] == PARENT
    _, commit = st.gh("GET", "/repos/%s/git/commits/%s" % (st.REPO, PARENT))
    base_tree = commit["tree"]["sha"]
    print("base tree:", base_tree, flush=True)
    files = [
        ("team-nitro/walk-v23-assembly-20261114/identity-fixed.html", new_ident),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
        ("team-nitro/walkthrough-chain-fix5-20261119/work/build-fix5.py",
         st.read_bytes(WORK5 + "/build-fix5.py")),
        ("team-nitro/walkthrough-chain-fix5-20261119/work/law-fix5.py",
         st.read_bytes(WORK5 + "/law-fix5.py")),
        ("team-nitro/walkthrough-chain-fix5-20261119/work/probe-fix5-live.py",
         st.read_bytes(WORK5 + "/probe-fix5-live.py")),
        ("team-nitro/walkthrough-chain-fix5-20261119/work/stage-fix5.py",
         st.read_bytes(WORK5 + "/stage-fix5.py")),
        ("team-nitro/walkthrough-chain-fix5-20261119/work/verify-proof-fix5.py",
         st.read_bytes(WORK5 + "/verify-proof-fix5.py")),
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
        "Walkthrough CHAIN FIX5 (2026-11-19, maker round; MAKER-REPORT.md in "
        "walkthrough-chain-fix5-20261119/) — commit 1\\n\\n"
        "The captain's cloud eye (04:53-05:02Z) claimed taken alias "
        "'jordantest' and saw no 'already claimed' flag and no device-key "
        "prompt — ENTER went straight to /welcome. Diagnosis: the typing "
        "check is debounced 300ms and ENTER never consulted it, so a fast "
        "ENTER claimed blind; the claim POST is the only guard, and it "
        "resolves only after the round-trip. The fix is the FIX5 gate in "
        "activateAndRedirect (identity-fixed.html only): ENTER resolves "
        "the availability verdict FIRST (the same /api/claim GET the "
        "typing check uses); taken shows the flag + the device-key panel "
        "and returns with no localStorage write and no claim POST; "
        "own/available fall through to the claim below, and a failed or "
        "timed-out (4s) verdict falls through too. The claim POST stays "
        "the authority; the worker claim handler is untouched. Live API "
        "probes in the diagnosis: GET jordantest exists:true own:false; "
        "POST with a fresh key returns 409 taken; the typing path was "
        "already live-proven in fix3 (note + panel visible, ENTER dim).\\n\\n"
        "Identity 400,253 B sha 6f805eba; worker sha %s "
        "(built twice, identical; embeds verified: WALK 4b5f9264, IDENTITY "
        "6f805eba, WELCOME d79793c0, UNFOLD 3252948e, TEMPLATE 61002d15). Law "
        "check: welcome still 83 FAIL / 4 WARN, identity still 11 FAIL / 2 WARN, "
        "zero new violations.\\n\\n"
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
        "/welcome": st.WALK_SHA,
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
    print("STAGE-RESULT5 " + json.dumps({
        "identity_bytes": len(new_ident), "identity_sha": IDENT_SHA,
        "worker_bytes": len(worker), "worker_sha": worker_sha,
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes}, indent=1), flush=True)


if __name__ == "__main__":
    main()
