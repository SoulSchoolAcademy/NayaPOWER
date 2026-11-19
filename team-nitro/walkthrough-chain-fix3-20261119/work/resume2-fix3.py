#!/usr/bin/env python3
"""FIX3 finish — commit 9a1109b3 is on the branch; read back all filed blobs
by full sha, PUT the worker, verify the 7 routes + 2 proof-host pages."""
import base64, importlib.util, json, time

SPEC = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(st)

WORKER_PATH = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/worker-fix3.js"
COMMIT = "9a1109b32baff414b1b4b4fa7249665abcf18f47"
BLOBS = {
    "team-nitro/walk-v23-assembly-20261114/welcome-staged.html": "c66e2fa20d2e82a9d10e7eac2d2f11f6a156768f",
    "team-nitro/walk-v23-assembly-20261114/identity-fixed.html": "63217489bd0e31662f1a516177da4f52ac2dd6c4",
    "team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html": "8980e57786c9bb196fb1ac5252f483995228e337",
    "team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js": "30ceb06b97e1295a5d06b12a432e8f6c3b702e5a",
    "team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py": "960334a2ea7752087171a8d4ba9776460dbcc224",
    "team-nitro/walkthrough-chain-fix3-20261119/work/fetch-bases.py": "4801e21bb9b057f27c7563a5d8cd5447cb4eaaab",
    "team-nitro/walkthrough-chain-fix3-20261119/work/law-fix3.py": "d9bb2cdba5754f23a01277a196f335de98096bab",
    "team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py": "bd8346eaaeb98541a5a0fc8d2a0a6d99e9552a12",
}
FILES = [
    ("team-nitro/walk-v23-assembly-20261114/welcome-staged.html", st.read_bytes(st.WELCOME_LOCAL)),
    ("team-nitro/walk-v23-assembly-20261114/identity-fixed.html", st.read_bytes(st.IDENT_LOCAL)),
    ("team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html", st.read_bytes(st.UNFOLD_LOCAL)),
    ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", st.read_bytes(WORKER_PATH)),
    ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", st.read_bytes(st.BUILDER)),
    ("team-nitro/walkthrough-chain-fix3-20261119/work/fetch-bases.py", st.read_bytes(st.WORK + "/fetch-bases.py")),
    ("team-nitro/walkthrough-chain-fix3-20261119/work/law-fix3.py", st.read_bytes(st.WORK + "/law-fix3.py")),
    ("team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py", st.read_bytes(st.WORK + "/stage-fix3.py")),
]

def main():
    worker = st.read_bytes(WORKER_PATH)
    assert st.sha(worker).startswith("7b058fde"), st.sha(worker)[:12]
    _, ref = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, st.NEW_BRANCH))
    assert ref["object"]["sha"] == COMMIT, ref["object"]["sha"]
    print("branch at commit:", COMMIT, flush=True)
    for path, data in FILES:
        _, rb = st.gh("GET", "/repos/%s/git/blobs/%s" % (st.REPO, BLOBS[path]))
        raw = base64.b64decode("".join(rb["content"].split()))
        if path.endswith("stage-fix3.py"):
            # KNOWN DIFF: the filed blob is the pre-fix driver (it died on the
            # % in the commit message); the local file carries only the one-char
            # -50% -> -50%% escape fix. The resume scripts carry the fix.
            print("blob read-back KNOWN-DIFF (%% escape fix after filing):", path.split("/")[-1], len(raw), "filed vs", len(data), "local", flush=True)
            continue
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
        "commit": COMMIT, "tree": "5cf4cb7791618f692e1dcb42f5af5a1cf96da809", "blobs": BLOBS,
        "routes": routes, "proof": proof}, indent=1), flush=True)

if __name__ == "__main__":
    main()
