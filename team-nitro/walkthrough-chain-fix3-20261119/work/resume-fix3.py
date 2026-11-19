#!/usr/bin/env python3
"""FIX3 resume — the stage driver built everything (worker, branch, blobs,
tree 5cf4cb77...) then died on a % in the commit message. This resumes from
the existing tree: create the commit, move the branch, read back blobs, PUT
the worker, verify routes + proof-host pages. Idempotent on re-run only up
to the PUT; the ref update asserts the branch is still at the parent tip.
"""
import importlib.util, json, sys, time

SPEC = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(st)

WORKER_PATH = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/worker-fix3.js"
TREE_SHA = "5cf4cb7791618f692e1dcb42f5af5a1cf96da809"
BLOBS = {
    "team-nitro/walk-v23-assembly-20261114/welcome-staged.html": "c66e2fa20d2e",
    "team-nitro/walk-v23-assembly-20261114/identity-fixed.html": "63217489bd0e",
    "team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html": "8980e57786c9",
    "team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js": "30ceb06b97e1",
    "team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py": "960334a2ea77",
    "team-nitro/walkthrough-chain-fix3-20261119/work/fetch-bases.py": "4801e21bb9b0",
    "team-nitro/walkthrough-chain-fix3-20261119/work/law-fix3.py": "d9bb2cdba575",
    "team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py": "bd8346eaaeb9",
}
FILES = [
    ("team-nitro/walk-v23-assembly-20261114/welcome-staged.html",
     st.read_bytes(st.WELCOME_LOCAL)),
    ("team-nitro/walk-v23-assembly-20261114/identity-fixed.html",
     st.read_bytes(st.IDENT_LOCAL)),
    ("team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html",
     st.read_bytes(st.UNFOLD_LOCAL)),
    ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js",
     st.read_bytes(WORKER_PATH)),
    ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py",
     st.read_bytes(st.BUILDER)),
    ("team-nitro/walkthrough-chain-fix3-20261119/work/fetch-bases.py",
     st.read_bytes(st.WORK + "/fetch-bases.py")),
    ("team-nitro/walkthrough-chain-fix3-20261119/work/law-fix3.py",
     st.read_bytes(st.WORK + "/law-fix3.py")),
    ("team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py",
     st.read_bytes(st.WORK + "/stage-fix3.py")),
]

def main():
    worker = st.read_bytes(WORKER_PATH)
    assert st.sha(worker).startswith("7b058fde"), st.sha(worker)[:12]
    print("worker %d B sha %s" % (len(worker), st.sha(worker)), flush=True)
    _, ref2 = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, st.NEW_BRANCH))
    print("branch now at:", ref2["object"]["sha"], flush=True)
    assert ref2["object"]["sha"] == st.PARENT_TIP
    msg = st.commit_message(st.sha(worker), len(worker), st.WELCOME_SHA, st.IDENT_SHA, st.UNFOLD_SHA)
    print("commit message renders OK (%d chars)" % len(msg), flush=True)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _, cm = st.gh("POST", "/repos/%s/git/commits" % st.REPO,
               {"message": msg, "tree": TREE_SHA, "parents": [st.PARENT_TIP],
                "author": {"name": "nayapower-lane-agent[bot]",
                           "email": "338161897+nayapower-lane-agent[bot]@users.noreply.github.com",
                           "date": now},
                "committer": {"name": "GitHub", "email": "noreply@github.com", "date": now}})
    commit_sha = cm["sha"]
    print("commit sha:", commit_sha, flush=True)
    _, ref3 = st.gh("PATCH", "/repos/%s/git/refs/heads/%s" % (st.REPO, st.NEW_BRANCH),
                 {"sha": commit_sha, "force": False})
    print("branch now:", ref3["object"]["sha"], flush=True)
    assert ref3["object"]["sha"] == commit_sha
    import base64
    for path, data in FILES:
        _, rb = st.gh("GET", "/repos/%s/git/blobs/%s" % (st.REPO, BLOBS[path]))
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
        "/identity.html": st.IDENT_SHA,
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
            ("identity", "team-nitro/walk-v23-assembly-20261114/identity-fixed.html", st.IDENT_SHA)):
        url = "%s/?file=%s&ref=%s&cb=%s&t=%d" % (st.PROOF, path, st.NEW_BRANCH, BLOBS[path], int(time.time()))
        _, got = st.curl_sha(url, ua)
        print("proof %s: sha=%s (want %s)" % (label, got[:12], want[:12]), flush=True)
        assert got == want, "proof-host %s mismatch" % label
        proof[label] = url
    print("STAGE-RESULT " + json.dumps({
        "welcome_bytes": len(FILES[0][1]), "welcome_sha": st.WELCOME_SHA,
        "identity_bytes": len(FILES[1][1]), "identity_sha": st.IDENT_SHA,
        "unfold_bytes": len(FILES[2][1]), "unfold_sha": st.UNFOLD_SHA,
        "worker_bytes": len(worker), "worker_sha": st.sha(worker),
        "commit": commit_sha, "tree": TREE_SHA, "blobs": BLOBS,
        "routes": routes, "proof": proof}, indent=1), flush=True)

if __name__ == "__main__":
    main()
