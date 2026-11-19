#!/usr/bin/env python3
"""FIX3c stage + file (2026-11-19) — commit 3 on walkthrough/chain-fix3-20261119.

The live Firefox probe of the fix3b staging (evidence/fix3b-live.json)
proved the crests DONE at 1920 + 534 — and proved the certified
certificate at 534 still overlaps: the name tucks 9px under "This
certifies that", the stale "Available — it is yours to claim." status
prints across the member sentence's second line (22px), the Smart Link
label catches its last 3px, and the switch pill straddles the plaque's
bottom edge. Root cause: the certified document is ~41px taller than
its 706px face at 534x900, and the grid's align-items:center splits
the foot's overflow equally up and down, so the foot spills UP into
the center row. The fix (certified + max-width:640px only): the card
grows 36+8px (main padding-bottom + back-row padding released while
certified), the head gives 20px (face + head padding), the stale
status line is hidden, the foot aligns to the top of its track, and
the foot trims 20px (Copy pill, ENTER, regalia, switch). Desktop and
the composing state are untouched. This script files identity + worker
+ builder as commit 3, PUTs the worker, and verifies the 7 routes + 2
proof-host pages by sha. No PR, no merge, no live deploy, no message
to Shawn.
"""
import base64, importlib.util, json, time

SPEC = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(st)

WORKER_B = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/worker-fix3c.js"
PARENT = "76614270c12f6a93081e5ca3e6da07f5ee391ac3"
IDENT_SHA = "88c19001f9e5738de867a43994955c79593fdbdb48c57a89a582398db4a57b88"
WORKER_SHA = "33cbda41030651ee0dc359f9466086c688c44b2136050a31097e70d6d48849cd"
FILES = [
    ("team-nitro/walk-v23-assembly-20261114/identity-fixed.html", st.read_bytes(st.IDENT_LOCAL)),
    ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", st.read_bytes(WORKER_B)),
    ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", st.read_bytes(st.BUILDER)),
    ("team-nitro/walkthrough-chain-fix3-20261119/work/resume2-fix3.py",
     st.read_bytes(st.WORK + "/resume2-fix3.py")),
    ("team-nitro/walkthrough-chain-fix3-20261119/work/probe-fix3-live.py",
     st.read_bytes(st.WORK + "/probe-fix3-live.py")),
    ("team-nitro/walkthrough-chain-fix3-20261119/work/probe-fix3b-live.py",
     st.read_bytes(st.WORK + "/probe-fix3b-live.py")),
    ("team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3c.py",
     st.read_bytes(st.WORK + "/stage-fix3c.py")),
]

def main():
    ident, worker, builder = FILES[0][1], FILES[1][1], FILES[2][1]
    assert st.sha(ident) == IDENT_SHA, st.sha(ident)
    assert st.sha(worker) == WORKER_SHA, st.sha(worker)
    assert b'assert ident_sha.startswith("88c19001")' in builder
    print("inputs: identity %d B %s, worker %d B %s, builder %d B" % (
        len(ident), IDENT_SHA[:12], len(worker), WORKER_SHA[:12], len(builder)), flush=True)
    _, ref = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, st.NEW_BRANCH))
    assert ref["object"]["sha"] == PARENT, ref["object"]["sha"]
    print("branch at commit:", PARENT, flush=True)
    _, commit = st.gh("GET", "/repos/%s/git/commits/%s" % (st.REPO, PARENT))
    base_tree = commit["tree"]["sha"]
    print("base tree:", base_tree, flush=True)
    blobs = {}
    for path, data in FILES:
        _, blob = st.gh("POST", "/repos/%s/git/blobs" % st.REPO,
                        {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"})
        blobs[path] = blob["sha"]
        print("blob %s: %s (%d B)" % (path.split("/")[-1], blob["sha"][:12], len(data)), flush=True)
    _, tree = st.gh("POST", "/repos/%s/git/trees" % st.REPO,
                    {"base_tree": base_tree,
                     "tree": [{"path": p, "mode": "100644", "type": "blob", "sha": s} for p, s in blobs.items()]})
    print("new tree:", tree["sha"], flush=True)
    msg = (
        "Walkthrough CHAIN FIX3b (2026-11-19) — crest rotated-box fix, commit 2\\n\\n"
        "The live Firefox probe of the fix3 staging proved items 1, 2, 3, 4, 6 and "
        "the hero-echo sub-item DONE — and proved one remaining defect: the corner "
        "emblems are STILL clipped 7px at 1920 (x=-7, right edge 1927). The translate "
        "removal alone was not enough: a 100x122 box rotated 59deg has a 156x149 "
        "axis-aligned box, so its centre must sit >=78px from the edge; at 20px the "
        "centre is 70px in. The large-variant offsets move 20px -> 32px (centre 82px "
        "in, ~4px clearance on every side). Same emblem, same rotation, same corner.\\n\\n"
        "Identity 395,010 B sha 6a4615b6; worker 8,336,823 B sha 231e59a2 "
        "(embeds verified: WALK 4b5f9264, IDENTITY 6a4615b6, WELCOME d79793c0, "
        "UNFOLD 3252948e, TEMPLATE 61002d15). Law check: identity still 11 FAIL / "
        "2 WARN, zero new violations.\\n\\n"
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
    _, ref3 = st.gh("PATCH", "/repos/%s/git/refs/heads/%s" % (st.REPO, st.NEW_BRANCH),
                    {"sha": commit_sha, "force": False})
    print("branch now:", ref3["object"]["sha"], flush=True)
    assert ref3["object"]["sha"] == commit_sha
    for path, data in FILES:
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
    # welcome was filed in commit 1 (blob c66e2fa2...); identity is this commit's blob.
    for label, path, want, cb in (
            ("welcome", "team-nitro/walk-v23-assembly-20261114/welcome-staged.html", st.WELCOME_SHA,
             "c66e2fa20d2e82a9d10e7eac2d2f11f6a156768f"),
            ("identity", "team-nitro/walk-v23-assembly-20261114/identity-fixed.html", IDENT_SHA,
             blobs["team-nitro/walk-v23-assembly-20261114/identity-fixed.html"])):
        url = "%s/?file=%s&ref=%s&cb=%s&t=%d" % (st.PROOF, path, st.NEW_BRANCH, cb, int(time.time()))
        _, got = st.curl_sha(url, ua)
        print("proof %s: sha=%s (want %s)" % (label, got[:12], want[:12]), flush=True)
        assert got == want, "proof-host %s mismatch" % label
        proof[label] = url
    print("STAGE-RESULT3 " + json.dumps({
        "identity_bytes": len(ident), "identity_sha": IDENT_SHA,
        "worker_bytes": len(worker), "worker_sha": WORKER_SHA,
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes, "proof": proof}, indent=1), flush=True)

if __name__ == "__main__":
    main()
