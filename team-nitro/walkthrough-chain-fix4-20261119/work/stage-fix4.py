#!/usr/bin/env python3
"""FIX4 stage + file (2026-11-19) — commit 1 on walkthrough/chain-fix4-20261119.

The fix3 checker proved the desktop certified certificate still shows the
stale green "Available — it's yours to claim." status struck across the
member sentence (fix3-live-E-copy-1920.png, Nº 000842): the fix3c hide rule
is max-width:640px only. The fix is one rule in identity-fixed.html — the
same selector lifted out of the media query, so the stale status is hidden
while certified at ALL widths. Welcome, unfold, walk, template untouched.

This script: verifies the local inputs by sha, node --checks the identity
script block, rebuilds the staging worker twice in-process (deterministic
sha, embeds verified by sha256, FIX4 rule present), creates the fix4 branch
from the fix3 tip, files ONE commit (identity + worker + builder + drivers),
read-back verifies every blob, PUTs the worker, and verifies the 7 routes +
2 proof-host pages by sha (curl piped to sha, never a file write — EPERM).
No PR, no merge, no live deploy, no message to Shawn.
"""
import base64, importlib.util, json, re, subprocess, time

SPEC = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(st)

WORK4 = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix4-20261119/work"
NEW_BRANCH = "walkthrough/chain-fix4-20261119"
PARENT = "4bc016b31a175771cc5e107da385e6fd8a745abc"
IDENT_SHA = "85b424470b2cea09a07345f98ed6d5baae412cd1ee9d34926a6ba167b6486b65"
WORKER_SHA = "dd52d1c1f2782a6a104c953f3383c97d1559e440aaac210929344d9ee27d3997"


def main():
    new_ident = st.read_bytes(st.IDENT_LOCAL)
    new_welcome = st.read_bytes(st.WELCOME_LOCAL)
    new_unfold = st.read_bytes(st.UNFOLD_LOCAL)
    builder = st.read_bytes(st.BUILDER)
    assert st.sha(new_ident) == IDENT_SHA, "identity moved: %s" % st.sha(new_ident)
    assert st.sha(new_welcome) == st.WELCOME_SHA, "welcome moved"
    assert st.sha(new_unfold) == st.UNFOLD_SHA, "unfold moved"
    assert b'assert ident_sha.startswith("85b42447")' in builder, "builder assert not moved"
    print("inputs: identity %d B %s, welcome %d B %s, unfold %d B %s, builder %d B" % (
        len(new_ident), IDENT_SHA[:12], len(new_welcome), st.WELCOME_SHA[:12],
        len(new_unfold), st.UNFOLD_SHA[:12], len(builder)), flush=True)
    for code in st.extract_scripts(new_ident, "identity"):
        st.node_check_script(code, "identity")
    worker = st.run_builder(new_welcome, st.WELCOME_SHA, IDENT_SHA, st.UNFOLD_SHA)
    assert st.sha(worker) == WORKER_SHA, "worker sha moved: %s" % st.sha(worker)
    assert b".cert-plaque.is-certified .alias-status { display: none; }" in worker, \
        "worker missing the FIX4 hide rule"
    r = subprocess.run(["node", "--check", "--input-type=module", "-"],
                       input=worker, capture_output=True)
    assert r.returncode == 0, "node --check failed for worker: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: worker (%d B) sha %s" % (len(worker), WORKER_SHA[:12]), flush=True)
    for path, data in ((st.WORKER_LOCAL, worker), (WORK4 + "/worker-fix4.js", worker)):
        try:
            st.write_resilient(path, data)
        except Exception as e:
            print("WARNING: worker copy not written (EPERM flake): %s: %r" % (path, e), flush=True)
    _, ref = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, "walkthrough/chain-fix3-20261119"))
    assert ref["object"]["sha"] == PARENT, "fix3 tip moved: %s" % ref["object"]["sha"]
    print("parent (fix3 tip):", PARENT, flush=True)
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
        ("team-nitro/walkthrough-chain-fix4-20261119/work/build-fix4.py",
         st.read_bytes(WORK4 + "/build-fix4.py")),
        ("team-nitro/walkthrough-chain-fix4-20261119/work/law-fix4.py",
         st.read_bytes(WORK4 + "/law-fix4.py")),
        ("team-nitro/walkthrough-chain-fix4-20261119/work/probe-fix4-live.py",
         st.read_bytes(WORK4 + "/probe-fix4-live.py")),
        ("team-nitro/walkthrough-chain-fix4-20261119/work/stage-fix4.py",
         st.read_bytes(WORK4 + "/stage-fix4.py")),
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
        "Walkthrough CHAIN FIX4 (2026-11-19, maker round; MAKER-REPORT.md in "
        "walkthrough-chain-fix4-20261119/) — commit 1\\n\\n"
        "The fix3 checker proved the desktop certified certificate still shows "
        "the stale green status line struck across the member sentence "
        "(fix3-live-E-copy-1920.png, cert Nº 000842): "
        "the fix3c hide rule is max-width:640px only, so desktop still shows it. "
        "The fix is ONE rule in identity-fixed.html — the same selector "
        "(.cert-plaque.is-certified .alias-status { display: none; }) lifted out "
        "of the media query, so the stale status is hidden while certified at ALL "
        "widths. Composing state untouched (not .is-certified); no other certified "
        "rule sets display on .alias-status. Welcome, unfold, walk, template "
        "untouched.\\n\\n"
        "Identity 397,978 B sha 85b42447; worker 8,339,870 B sha dd52d1c1 "
        "(built twice, identical; embeds verified: WALK 4b5f9264, IDENTITY "
        "85b42447, WELCOME d79793c0, UNFOLD 3252948e, TEMPLATE 61002d15). Law "
        "check: welcome still 83 FAIL / 4 WARN, identity still 11 FAIL / 2 WARN, "
        "zero new violations.\\n\\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after the PUT. "
        "NO PR, NO MERGE — the checker and the captain come after this seat. "
        "Nothing live." % st.STAGING)
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
    proof = {}
    for label, path, want in (
            ("welcome", "team-nitro/walk-v23-assembly-20261114/welcome-staged.html", st.WELCOME_SHA),
            ("identity", "team-nitro/walk-v23-assembly-20261114/identity-fixed.html", IDENT_SHA)):
        url = "%s/?file=%s&ref=%s&cb=%s&t=%d" % (st.PROOF, path, NEW_BRANCH, blobs[path], int(time.time()))
        _, got = st.curl_sha(url, ua)
        print("proof %s: sha=%s (want %s)" % (label, got[:12], want[:12]), flush=True)
        assert got == want, "proof-host %s mismatch" % label
        proof[label] = url
    print("STAGE-RESULT4 " + json.dumps({
        "identity_bytes": len(new_ident), "identity_sha": IDENT_SHA,
        "worker_bytes": len(worker), "worker_sha": WORKER_SHA,
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes, "proof": proof}, indent=1), flush=True)


if __name__ == "__main__":
    main()
