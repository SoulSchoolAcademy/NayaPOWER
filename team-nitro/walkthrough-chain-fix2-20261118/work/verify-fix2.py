#!/usr/bin/env python3
"""FIX2 verify-only (2026-11-18): the stage driver already filed the commit
(a89e10aedd35fb5e065d45db4fc11396b9b03b09) and PUT the worker (HTTP 200,
success true, modified 2026-11-18T23:50:04Z) — this script does only the
route + proof-host sha verification that the driver's own assert cut short
(it checked for '"success":true' without the space; the API pretty-prints
'"success": true'). No disk writes, no rebuild, no re-PUT."""
import hashlib, json, subprocess, sys, time

GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
REPO = "SoulSchoolAcademy/NayaPOWER"
NEW_BRANCH = "walkthrough/chain-fix2-20261118"
TREE_SHA = "59680fea0740c9c349f18c33ccaa025f67c1a996"
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
PROOF = "https://naya-proof-host.nayapower.workers.dev"
WELCOME_SHA = "c8581fca0a697204a94d64b17b28e5ae67ef70d887fd95dd2cdd5b8ba1815d03"
IDENT_SHA = "803e7ea8a7822f8f1e5942913615ca62bfec81e54b28bb4a05924134322bd617"
UNFOLD_SHA = "984d87aff1a04fb159579c3ef9e8703ca7044a7b9667a1a0a9c0c18e50baa671"
WALK_SHA = "4b5f926423d765bd750026e65986f0b67f6b52d51588fe64e857b39df7ee01c0"

def sha(b):
    return hashlib.sha256(b).hexdigest()

def gh(method, path, body=None):
    args = [sys.executable, GH, method, path]
    inp = None
    if body is not None:
        args.append("@/dev/stdin")
        inp = json.dumps(body).encode()
    p = subprocess.run(args, input=inp, capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    lines = out.split("\n", 1)
    status = int(lines[0].split()[1]) if lines and lines[0].startswith("HTTP") else -1
    payload = lines[1] if len(lines) > 1 else ""
    data = json.loads(payload) if payload.strip() else {}
    if status >= 400 or p.returncode != 0:
        print("FAIL %s %s: HTTP %s\n%s" % (method, path, status, payload[:800]), file=sys.stderr)
        sys.exit(1)
    return status, data

def curl_sha(url, ua):
    rr = subprocess.run(["curl", "-s", "-A", ua, url], capture_output=True, timeout=120)
    return rr.stdout, sha(rr.stdout)

def main():
    ua = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
    expect = {
        "/": WELCOME_SHA,
        "/agreement": UNFOLD_SHA,
        "/welcome": WALK_SHA,
        "/identity.html": IDENT_SHA,
        "/?stage=bridge": WELCOME_SHA,
        "/?stage=deck": WELCOME_SHA,
        "/?stage=letter": WELCOME_SHA,
    }
    routes = {}
    for route, want in expect.items():
        got = None
        for attempt in (1, 2, 3):
            body, got = curl_sha(STAGING + route, ua)
            print("route %s: %d B sha=%s (want %s) attempt %d" % (route, len(body), got[:12], want[:12], attempt), flush=True)
            if got == want:
                break
            time.sleep(15)
        routes[route] = got
        assert got == want, "route %s mismatch: got %s want %s" % (route, got, want)
    _, tree = gh("GET", "/repos/%s/git/trees/%s?recursive=1" % (REPO, TREE_SHA))
    blobs = {e["path"]: e["sha"] for e in tree["tree"]}
    print("tree blobs: welcome %s identity %s" % (blobs["team-nitro/walk-v23-assembly-20261114/welcome-staged.html"][:12],
          blobs["team-nitro/walk-v23-assembly-20261114/identity-fixed.html"][:12]), flush=True)
    import base64
    _, wblob = gh("GET", "/repos/%s/git/blobs/%s" % (REPO, blobs["team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js"]))
    wraw = base64.b64decode("".join(wblob["content"].split()))
    worker_sha = sha(wraw)
    print("filed worker blob: %d B sha=%s" % (len(wraw), worker_sha), flush=True)
    assert worker_sha.startswith("2a348c2d6354"), "filed worker sha moved"
    proof = {}
    for label, path, want in (
            ("welcome", "team-nitro/walk-v23-assembly-20261114/welcome-staged.html", WELCOME_SHA),
            ("identity", "team-nitro/walk-v23-assembly-20261114/identity-fixed.html", IDENT_SHA)):
        url = "%s/?file=%s&ref=%s&cb=%s&t=%d" % (PROOF, path, NEW_BRANCH, blobs[path], int(time.time()))
        body, got = curl_sha(url, ua)
        print("proof %s: %d B sha=%s (want %s)" % (label, len(body), got[:12], want[:12]), flush=True)
        assert got == want, "proof-host %s mismatch" % label
        proof[label] = url
    print("VERIFY-RESULT " + json.dumps({
        "welcome_sha": WELCOME_SHA, "identity_sha": IDENT_SHA,
        "worker_sha": worker_sha, "worker_bytes": len(wraw),
        "commit": "a89e10aedd35fb5e065d45db4fc11396b9b03b09",
        "routes": routes, "proof": proof}, indent=1), flush=True)

if __name__ == "__main__":
    main()
