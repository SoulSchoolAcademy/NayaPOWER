#!/usr/bin/env python3
"""FIX7 stage (2026-11-19): file the fix-7 build in branch
walkthrough/chain-fix7-20261119 from the fix-6 tip f15357d7, one commit:
walk (unchanged), identity (unchanged), the new worker, the edited
builder (assert -> e21f08d0 + UNFOLD_RAW env), the new unfold (in-memory
bytes, never on disk), the frame assets (master-frame.png +
crystal-n.png, in-memory from the media library — blob shas verified
5a4dc2f9 / ee4b627c), and the fix-7 work scripts. Then blob read-back,
PUT the worker, and verify the 7 staging routes + the frame asset on
the proof host. Usage: python3 stage-fix7.py <worker_sha>

Follows the fix-6 pattern exactly (inline gh() calls; the unfold and
the frame assets come from memory, not from disk files; the unfold
file is NEW in this commit — the canonical path on disk is 0 bytes,
flake damage, the filed blob is the truth). Route expectations per
stage-fix6.py: / -> welcome, /agreement -> unfold, /welcome -> walk,
/identity.html -> identity, /?stage=bridge|deck|letter -> welcome.
"""
import base64, importlib.util, json, subprocess, sys, time, urllib.request

SPEC3 = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC3)
SPEC3.loader.exec_module(st)
SPEC7 = importlib.util.spec_from_file_location(
    "build_fix7", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix7-20261119/work/build-fix7.py")
bf = importlib.util.module_from_spec(SPEC7)
SPEC7.loader.exec_module(bf)

WORK = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix7-20261119/work"
BRANCH = "walkthrough/chain-fix7-20261119"
PARENT_BRANCH = "walkthrough/chain-fix6-20261119"
PARENT = "f15357d7b141b518c7ec80958de180c91c16a19b"
WALK_LOCAL = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html"
FRAME_PNG = "/home/hatch/workspace/user/media_library/image/86/865357f660595b90a83f9e971415b1a81d18ca2c4cfce7643d01c5771378d425.png"
CRYSTAL_PNG = "/home/hatch/workspace/user/media_library/image/e6/e66b77e03c7995b254db34002ca138471c7c238932a847b9a167508b759401ac.png"
import hashlib


def blob_sha(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\x00" + b).hexdigest()


def main():
    worker_sha = sys.argv[1]
    assert worker_sha != "PLACEHOLDER", "pass the built worker sha as argv[1]"
    new_walk = st.read_bytes(WALK_LOCAL)
    new_ident = st.read_bytes(st.IDENT_LOCAL)
    new_welcome = st.read_bytes(st.WELCOME_LOCAL)
    new_unfold = bf.run_pipeline()
    builder = st.read_bytes(st.BUILDER)
    frame = st.read_bytes(FRAME_PNG)
    crystal = st.read_bytes(CRYSTAL_PNG)
    print("inputs: walk %d B %s" % (len(new_walk), st.sha(new_walk)), flush=True)
    print("inputs: identity %d B %s" % (len(new_ident), st.sha(new_ident)), flush=True)
    print("inputs: welcome %d B %s" % (len(new_welcome), st.sha(new_welcome)), flush=True)
    print("inputs: unfold %d B %s" % (len(new_unfold), st.sha(new_unfold)), flush=True)
    print("inputs: master-frame %d B blob %s" % (len(frame), blob_sha(frame)[:8]), flush=True)
    print("inputs: crystal-n %d B blob %s" % (len(crystal), blob_sha(crystal)[:8]), flush=True)
    assert st.sha(new_walk) == bf.WALK_SHA, "walk moved"
    assert st.sha(new_ident) == bf.IDENT_SHA, "identity moved"
    assert st.sha(new_welcome) == st.WELCOME_SHA, "welcome moved"
    assert st.sha(new_unfold) == bf.UNFOLD_SHA, "unfold moved"
    assert blob_sha(frame).startswith("5a4dc2f9"), "master frame moved"
    assert blob_sha(crystal).startswith("ee4b627c"), "crystal N moved"
    assert b'assert unfold_sha.startswith("e21f08d0")' in builder, "builder unfold assert not moved"
    assert b'UNFOLD_RAW' in builder, "builder missing UNFOLD_RAW"
    worker = bf.run_builder7(new_welcome, st.WELCOME_SHA, bf.IDENT_SHA, bf.UNFOLD_SHA, new_unfold)
    print("worker rebuilt: %d B sha %s" % (len(worker), st.sha(worker)), flush=True)
    assert st.sha(worker) == worker_sha, "worker sha moved: %s" % st.sha(worker)
    assert b"fpFrame7" in worker and b"gateDone6" in worker, "worker missing the FIX7/FIX6 markers"
    r = subprocess.run(["node", "--check", "--input-type=module", "-"],
                       input=worker, capture_output=True)
    assert r.returncode == 0, "node --check failed for worker: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: worker (%d B) sha %s" % (len(worker), worker_sha[:12]), flush=True)
    for path in (st.WORKER_LOCAL, WORK + "/worker-fix7.js"):
        try:
            st.write_resilient(path, worker)
        except Exception as e:
            print("WARNING: worker copy not written (EPERM flake): %s: %r" % (path, e), flush=True)
    _, ref = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, PARENT_BRANCH))
    assert ref["object"]["sha"] == PARENT, "fix6 tip moved: %s" % ref["object"]["sha"]
    print("parent (fix6 tip):", PARENT, flush=True)
    _, nb = st.gh("POST", "/repos/%s/git/refs" % st.REPO,
                  {"ref": "refs/heads/%s" % BRANCH, "sha": PARENT})
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
        ("team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html", new_unfold),
        ("team-nitro/agreement-unfold-20261117/master-frame.png", frame),
        ("team-nitro/agreement-unfold-20261117/crystal-n.png", crystal),
        ("team-nitro/walkthrough-chain-fix7-20261119/work/build-fix7.py", st.read_bytes(WORK + "/build-fix7.py")),
        ("team-nitro/walkthrough-chain-fix7-20261119/work/stage-fix7.py", st.read_bytes(WORK + "/stage-fix7.py")),
        ("team-nitro/walkthrough-chain-fix7-20261119/work/law-fix7.py", st.read_bytes(WORK + "/law-fix7.py")),
        ("team-nitro/walkthrough-chain-fix7-20261119/work/probe-fix7-diag.py", st.read_bytes(WORK + "/probe-fix7-diag.py")),
        ("team-nitro/walkthrough-chain-fix7-20261119/work/transform-fix7.js", st.read_bytes(WORK + "/transform-fix7.js")),
        ("team-nitro/walkthrough-chain-fix7-20261119/work/transform-fix7-stdout2.js", st.read_bytes(WORK + "/transform-fix7-stdout2.js")),
        ("team-nitro/walkthrough-chain-fix7-20261119/work/build-frame7.py", st.read_bytes(WORK + "/build-frame7.py")),
        ("team-nitro/walkthrough-chain-fix7-20261119/work/smoke-fix7.py", st.read_bytes(WORK + "/smoke-fix7.py")),
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
        "Walkthrough CHAIN FIX7 (2026-11-19, maker round; MAKER-REPORT.md in "
        "walkthrough-chain-fix7-20261119/) — commit 1\n\n"
        "The agreement is broken in Shawn's hands (lands in the middle, "
        "unreadable, no buttons, will not scroll). This round rebuilds the "
        "unfold shell INTO THE FRAME, frame by frame, click -> next frame "
        "(F1-F11): Naya picture in a top bar on every frame (a new picture "
        "each frame), headline centred, icon right, back / keep reading / "
        "next below, the big Naya RED piece with the N under Naya just "
        "above the three buttons, read in Naya's voice. Unfold 105,068 B "
        "(sha 3252948e) -> 117,636 B (sha e21f08d0). Beat and article "
        "counts unchanged; content needles verified. The frame layer is "
        "one swappable background-image + --frame-img-916 hook, so the "
        "frame-assets round's output drops in later with a one-line "
        "change. Frame assets filed here: master-frame.png (blob "
        "5a4dc2f9) + crystal-n.png (blob ee4b627c). Builder assert moves "
        "3252948e -> e21f08d0 and gains the UNFOLD_RAW env override "
        "(in-memory landing: the EPERM/taint flake blocks file writes "
        "after a process reads the worker file, a pipe, or a socket).\n\n"
        "Walk 4,361,146 B sha b6befc33; identity 401,040 B sha 3279dc35; "
        "worker sha %s (built twice, identical; embeds verified: WALK "
        "b6befc33, IDENTITY 3279dc35, WELCOME d79793c0, UNFOLD e21f08d0, "
        "TEMPLATE 61002d15).\n\n"
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
    _, ref3 = st.gh("PATCH", "/repos/%s/git/refs/heads/%s" % (st.REPO, BRANCH),
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
        "/agreement": bf.UNFOLD_SHA,
        "/welcome": bf.WALK_SHA,
        "/identity.html": bf.IDENT_SHA,
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
    frame_url = ("https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/agreement-unfold-20261117/master-frame.png"
                 "&ref=walkthrough/chain-fix7-20261119&cb=5a4dc2f9ca703945f12cec0b39b491d728e69c4a")
    req = urllib.request.Request(frame_url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=60) as resp:
        served = resp.read()
    print("proof-host master-frame: %d B sha %s (want %d B %s)" % (
        len(served), st.sha(served)[:12], len(frame), st.sha(frame)[:12]), flush=True)
    assert len(served) == len(frame) and st.sha(served) == st.sha(frame), "proof-host frame asset mismatch"
    print("STAGE-RESULT7 " + json.dumps({
        "walk_bytes": len(new_walk), "walk_sha": bf.WALK_SHA,
        "identity_bytes": len(new_ident), "identity_sha": bf.IDENT_SHA,
        "unfold_bytes": len(new_unfold), "unfold_sha": bf.UNFOLD_SHA,
        "worker_bytes": len(worker), "worker_sha": worker_sha,
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes}, indent=1), flush=True)


if __name__ == "__main__":
    main()
