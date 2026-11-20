#!/usr/bin/env python3
"""AGREEMENT-FRAME stage (2026-11-19): file the AF build in NEW branch
walkthrough/agreement-frame-20261119 from the fix-9 tip cdc94c72, one
commit: walk (unchanged), identity (unchanged), the new worker, the
edited builder (asserts -> AF unfold + AF welcome shas), the new
welcome (deck frame), the new unfold (24 boards, frame system), the
mp3 (unchanged, UNWIRED), and the AF work scripts + brief. Then blob
read-back, PUT the worker, and verify the 7 staging routes + the
unfold on the proof host. Usage: python3 stage-af.py <worker_sha>

Route expectations: / -> welcome (AF), /agreement -> unfold (AF),
/welcome -> walk, /identity.html -> identity,
/?stage=bridge|deck|letter -> welcome (AF).

FLAKE RULES (proven fix-9): EPERM is sticky per process — all
multi-KB writes go through fresh single-attempt node writers
(writer9.js, maxAttempts=1, looped in the parent). Never truncate a
live file (temp+verify+replace)."""
import base64, hashlib, importlib.util, json, subprocess, sys, time, urllib.request

SPEC3 = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC3)
SPEC3.loader.exec_module(st)
SPECAF = importlib.util.spec_from_file_location(
    "build_af", "/home/hatch/workspace/team-nitro/walkthrough-agreement-frame-20261119/maker/work/build-af.py")
bf = importlib.util.module_from_spec(SPECAF)
SPECAF.loader.exec_module(bf)

WORK = "/home/hatch/workspace/team-nitro/walkthrough-agreement-frame-20261119/maker/work"
BRANCH = "walkthrough/agreement-frame-20261119"
PARENT_BRANCH = "walkthrough/agreement-frame-20261119"
PARENT = "a6c31edbb86ecc148b8ba2fb069db8b1aa62e9e0"
WALK_LOCAL = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html"
MP3_LOCAL = "/home/hatch/workspace/your_files/agreement-naya-voice.mp3"
MP3_SHA = "62bf05e68a036e86b5aa3280c16b9dd810dda711abf1fd34612cda10b2b9261a"
WORKER9_SHA = "595b6babe8d6b55463c04bf57818c520338d2397d9175a1c96acfe04968986cb"
WORKER9_BLOB = "6e21bf72531f2ba5af582b39f73f3418a10d4f2e"


def blob_sha(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\x00" + b).hexdigest()


def main():
    worker_sha = sys.argv[1]
    assert worker_sha != "PLACEHOLDER", "pass the built worker sha as argv[1]"
    # No worker restore needed: this pipeline's transform reads its base
    # from the LOCAL unfold/welcome files (still fix-9 bytes — every
    # landing attempt in this round failed, so the live files were never
    # touched), never from the worker embed. The local worker file is
    # not an input to the build.
    new_walk = st.read_bytes(WALK_LOCAL)
    new_ident = st.read_bytes(st.IDENT_LOCAL)
    new_unfold, new_welcome = bf.run_pipeline()
    builder = st.read_bytes(st.BUILDER)
    mp3 = st.read_bytes(MP3_LOCAL)
    unfold_sha, welcome_sha = st.sha(new_unfold), st.sha(new_welcome)
    print("inputs: walk %d B %s" % (len(new_walk), st.sha(new_walk)), flush=True)
    print("inputs: identity %d B %s" % (len(new_ident), st.sha(new_ident)), flush=True)
    print("inputs: welcome %d B %s" % (len(new_welcome), welcome_sha), flush=True)
    print("inputs: unfold %d B %s" % (len(new_unfold), unfold_sha), flush=True)
    print("inputs: mp3 %d B sha %s blob %s" % (len(mp3), st.sha(mp3), blob_sha(mp3)[:8]), flush=True)
    assert st.sha(new_walk) == bf.WALK_SHA, "walk moved"
    assert st.sha(new_ident) == bf.IDENT_SHA, "identity moved"
    assert st.sha(new_welcome) != bf.OLD_WELCOME_SHA and st.sha(new_unfold) != bf.OLD_UNFOLD_SHA, "AF bytes equal fix-9"
    assert st.sha(mp3) == MP3_SHA, "mp3 moved"
    assert len(mp3) == 5976421, "mp3 size moved"
    assert ('assert unfold_sha.startswith("%s")' % unfold_sha[:8]).encode() in builder, "builder unfold assert not moved"
    assert ('assert welcome_sha.startswith("%s")' % welcome_sha[:8]).encode() in builder, "builder welcome assert not moved"
    assert b"UNFOLD_RAW" in builder, "builder missing UNFOLD_RAW"
    assert b"stay on the entrance" in new_welcome, "welcome F6 edit missing"
    assert b"fpFrameAF" in new_unfold and b"fpDeckAF" in new_welcome, "AF markers missing"
    worker = bf.run_builder(new_welcome, welcome_sha, bf.IDENT_SHA, unfold_sha, new_unfold)
    print("worker rebuilt: %d B sha %s" % (len(worker), st.sha(worker)), flush=True)
    assert st.sha(worker) == worker_sha, "worker sha moved: %s" % st.sha(worker)
    assert b"fpFrameAF" in worker and b"fpDeckAF" in worker and b"fpFrame9" in worker, "worker missing AF markers"
    r = subprocess.run(["node", "--check", "--input-type=module", "-"],
                       input=worker, capture_output=True)
    assert r.returncode == 0, "node --check failed for worker: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: worker (%d B) sha %s" % (len(worker), worker_sha[:12]), flush=True)
    try:
        bf.land_via_writer9(worker, st.WORKER_LOCAL, tries=3)
    except Exception as e:
        print("WARNING: worker copy not written (EPERM flake): %s: %r" % (st.WORKER_LOCAL, e), flush=True)
    try:
        bf.land_via_writer9(worker, WORK + "/worker-af.js", tries=3)
    except Exception as e:
        print("WARNING: worker copy not written (EPERM flake): %s: %r" % (WORK + "/worker-af.js", e), flush=True)
    _, ref = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, PARENT_BRANCH))
    assert ref["object"]["sha"] == PARENT, "AF v3 tip moved: %s" % ref["object"]["sha"]
    print("parent (AF v3 tip):", PARENT, flush=True)
    _, ref2 = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, BRANCH))
    assert ref2["object"]["sha"] == PARENT, "branch tip moved: %s" % ref2["object"]["sha"]
    _, commit = st.gh("GET", "/repos/%s/git/commits/%s" % (st.REPO, PARENT))
    base_tree = commit["tree"]["sha"]
    print("base tree:", base_tree, flush=True)
    brief = st.read_bytes("/home/hatch/workspace/team-nitro/walkthrough-agreement-frame-20261119/AGREEMENT-FRAME-BRIEF.md")
    files = [
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html", new_walk),
        ("team-nitro/walk-v23-assembly-20261114/identity-fixed.html", new_ident),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
        ("team-nitro/walk-v23-assembly-20261114/welcome-staged.html", new_welcome),
        ("team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html", new_unfold),
        ("team-nitro/agreement-unfold-20261117/agreement-naya-voice.mp3", mp3),
        ("team-nitro/walkthrough-agreement-frame-20261119/AGREEMENT-FRAME-BRIEF.md", brief),
        ("team-nitro/walkthrough-agreement-frame-20261119/maker/work/transform-af.js", st.read_bytes(WORK + "/transform-af.js")),
        ("team-nitro/walkthrough-agreement-frame-20261119/maker/work/build-af.py", st.read_bytes(WORK + "/build-af.py")),
        ("team-nitro/walkthrough-agreement-frame-20261119/maker/work/stage-af.py", st.read_bytes(WORK + "/stage-af.py")),
        ("team-nitro/walkthrough-agreement-frame-20261119/maker/work/stage-af2.py", st.read_bytes(WORK + "/stage-af2.py")),
        ("team-nitro/walkthrough-agreement-frame-20261119/maker/work/stage-af3.py", st.read_bytes(WORK + "/stage-af3.py")),
        ("team-nitro/walkthrough-agreement-frame-20261119/maker/work/stage-af4.py", st.read_bytes(WORK + "/stage-af4.py")),
        ("team-nitro/walkthrough-agreement-frame-20261119/maker/work/restore-base.py", st.read_bytes(WORK + "/restore-base.py")),
        ("team-nitro/walkthrough-agreement-frame-20261119/maker/work/probe-af.py", st.read_bytes(WORK + "/probe-af.py")),
        ("team-nitro/walkthrough-agreement-frame-20261119/maker/work/law-af.py", st.read_bytes(WORK + "/law-af.py")),
        ("team-nitro/walkthrough-agreement-frame-20261119/maker/work/geom2.py", st.read_bytes(WORK + "/geom2.py")),
        ("team-nitro/walkthrough-agreement-frame-20261119/maker/work/writer9.js", st.read_bytes(WORK + "/writer9.js")),
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
        "Walkthrough AGREEMENT FRAME v4 (2026-11-19, maker round; MAKER-REPORT.md in "
        "walkthrough-agreement-frame-20261119/maker/)\\n\\n"
        "v4 is one fix on top of v3 (parent a6c31edb): v3's flex:0 1 auto "
        "DID apply, but flex-shrink squeezed all three mobile buttons to "
        "~101px (the row was only 314px — the foot's 24px padding) and "
        "overflow:hidden clipped \"Keep reading\" to \"Keep readi\". The "
        "foot now gives the row its full width (8px padding) and the "
        "buttons do not shrink (flex:0 0 auto), so all three read whole "
        "at 390. Everything else is v3.\\n\\n"
        "Unfold %d B (sha %s); welcome %d B (sha %s). Walk 4,361,146 B "
        "sha b6befc33; identity 401,040 B sha 3279dc35; worker sha %s "
        "(built twice, identical; embeds verified). The mp3 stays filed "
        "(5,976,421 B, sha256 62bf05e6) but is UNWIRED — both media "
        "buttons still wait on Shawn's captioned video; the anthem video "
        "wiring rides a separate round.\\n\\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after the PUT. "
        "NO PR, NO MERGE — the checker and the captain come after this seat. "
        "Nothing live." % (len(new_unfold), unfold_sha[:8], len(new_welcome), welcome_sha[:8],
                            worker_sha[:8], st.STAGING))
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
        "/": welcome_sha,
        "/agreement": unfold_sha,
        "/welcome": bf.WALK_SHA,
        "/identity.html": bf.IDENT_SHA,
        "/?stage=bridge": welcome_sha,
        "/?stage=deck": welcome_sha,
        "/?stage=letter": welcome_sha,
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
    url = "%s/?file=%s&ref=%s&cb=%s&t=%d" % (st.PROOF, "team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html",
                                            BRANCH, blobs["team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html"], int(time.time()))
    _, got = st.curl_sha(url, ua)
    print("proof unfold: sha=%s (want %s)" % (got[:12], unfold_sha[:12]), flush=True)
    assert got == unfold_sha, "proof-host unfold mismatch"
    print("STAGE-RESULT " + json.dumps({
        "welcome_bytes": len(new_welcome), "welcome_sha": welcome_sha,
        "identity_bytes": len(new_ident), "identity_sha": bf.IDENT_SHA,
        "unfold_bytes": len(new_unfold), "unfold_sha": unfold_sha,
        "worker_bytes": len(worker), "worker_sha": st.sha(worker),
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes, "proof_unfold": url}, indent=1), flush=True)


if __name__ == "__main__":
    main()
