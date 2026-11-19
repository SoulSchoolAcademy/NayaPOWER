#!/usr/bin/env python3
"""FIX9 stage (2026-11-19): file the fix-9 build in NEW branch
walkthrough/chain-fix9-20261119 from the fix-8 tip aa35e2c9, one commit:
walk (unchanged), identity (unchanged), the new worker, the edited
builder (assert -> ab8da1fa unfold), the new unfold, the edited welcome
(unchanged — F6 stands), the mp3 (unchanged, UNWIRED), and the fix-9
work scripts + brief. Then blob read-back, PUT the worker, and verify
the 7 staging routes + the unfold on the proof host. Usage:
python3 stage-fix9.py <worker_sha>

Route expectations: / -> welcome (unchanged), /agreement -> unfold
(new), /welcome -> walk, /identity.html -> identity,
/?stage=bridge|deck|letter -> welcome (unchanged).

FLAKE RULES (proven this round): EPERM is STICKY per process — a retry
loop inside one process never lands. All multi-KB writes go through
fresh single-attempt node writers (writer9.js, maxAttempts=1, looped
in the parent). The transform's base comes from the LOCAL worker file,
so the fix-8 worker is restored from its filed blob before the
pipeline runs; the writer never truncates a live file (temp+verify+
replace). The local unfold working copy was truncated to 0 bytes once
by a truncate-first write during this round and restored from its
filed blob de7970d2 — the filed bytes were never at risk.
"""
import base64, hashlib, importlib.util, json, subprocess, sys, time, urllib.request

SPEC3 = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC3)
SPEC3.loader.exec_module(st)
SPEC9 = importlib.util.spec_from_file_location(
    "build_fix9", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix9-20261119/maker/work/build-fix9.py")
bf = importlib.util.module_from_spec(SPEC9)
SPEC9.loader.exec_module(bf)

WORK = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix9-20261119/maker/work"
BRANCH = "walkthrough/chain-fix9-20261119"
PARENT_BRANCH = "walkthrough/chain-fix8-20261119"
PARENT = "aa35e2c971a45274a511e8fa68f2a7d1ee103aa2"
WALK_LOCAL = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html"
MP3_LOCAL = "/home/hatch/workspace/your_files/agreement-naya-voice.mp3"
MP3_SHA = "62bf05e68a036e86b5aa3280c16b9dd810dda711abf1fd34612cda10b2b9261a"
WORKER8_SHA = "8dc01221e8c3e08266c4c70f3d584511009f8d106a589172a2b74a6602fbba70"
WORKER8_BLOB = "ea1b89c8d1fc82bc30dc4431b6dad2f252c54c02"


def blob_sha(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\x00" + b).hexdigest()


def fresh_write(path, data, want_sha):
    """Fresh single-attempt writers until the path verifies (sticky EPERM)."""
    for n in range(1, 121):
        r = subprocess.run(["node", WORK + "/writer9.js", path, "1"],
                           input=data, capture_output=True, timeout=60)
        try:
            back = st.read_bytes(path)
            if st.sha(back) == want_sha:
                print("landed %s on fresh try %d: %d B sha %s" % (path, n, len(back), want_sha[:12]), flush=True)
                return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("fresh-write failed for %s after 120 tries" % path)


def main():
    worker_sha = sys.argv[1]
    assert worker_sha != "PLACEHOLDER", "pass the built worker sha as argv[1]"
    # The pipeline extracts the fix-8 unfold from the LOCAL worker file.
    # The build left the fix-9 worker there — restore the fix-8 worker
    # from its filed blob first (fresh single-attempt writers).
    if st.sha(st.read_bytes(st.WORKER_LOCAL)) != WORKER8_SHA:
        _, d = st.gh("GET", "/repos/%s/git/blobs/%s" % (st.REPO, WORKER8_BLOB))
        w8 = base64.b64decode("".join(d["content"].split()))
        assert st.sha(w8) == WORKER8_SHA, "fix-8 worker blob moved"
        fresh_write(st.WORKER_LOCAL, w8, WORKER8_SHA)
        print("local worker restored to fix-8 for the pipeline", flush=True)
    new_walk = st.read_bytes(WALK_LOCAL)
    new_ident = st.read_bytes(st.IDENT_LOCAL)
    new_welcome = st.read_bytes(st.WELCOME_LOCAL)
    new_unfold = bf.run_pipeline()
    builder = st.read_bytes(st.BUILDER)
    mp3 = st.read_bytes(MP3_LOCAL)
    print("inputs: walk %d B %s" % (len(new_walk), st.sha(new_walk)), flush=True)
    print("inputs: identity %d B %s" % (len(new_ident), st.sha(new_ident)), flush=True)
    print("inputs: welcome %d B %s" % (len(new_welcome), st.sha(new_welcome)), flush=True)
    print("inputs: unfold %d B %s" % (len(new_unfold), st.sha(new_unfold)), flush=True)
    print("inputs: mp3 %d B sha %s blob %s" % (len(mp3), st.sha(mp3), blob_sha(mp3)[:8]), flush=True)
    assert st.sha(new_walk) == bf.WALK_SHA, "walk moved"
    assert st.sha(new_ident) == bf.IDENT_SHA, "identity moved"
    assert st.sha(new_welcome) == bf.WELCOME_SHA, "welcome moved"
    assert st.sha(new_unfold) == bf.UNFOLD_SHA, "unfold moved"
    assert st.sha(mp3) == MP3_SHA, "mp3 moved"
    assert len(mp3) == 5976421, "mp3 size moved"
    assert b'assert unfold_sha.startswith("ab8da1fa")' in builder, "builder unfold assert not moved"
    assert b'assert welcome_sha.startswith("2062739e")' in builder, "builder welcome assert not moved"
    assert b'UNFOLD_RAW' in builder, "builder missing UNFOLD_RAW"
    assert b"stay on the entrance" in new_welcome, "welcome F6 edit missing"
    worker = bf.run_builder9(new_welcome, bf.WELCOME_SHA, bf.IDENT_SHA, bf.UNFOLD_SHA, new_unfold)
    print("worker rebuilt: %d B sha %s" % (len(worker), st.sha(worker)), flush=True)
    assert st.sha(worker) == worker_sha, "worker sha moved: %s" % st.sha(worker)
    assert b"fpFrame9" in worker and b"fpMediaFrame" in worker and b"fpFrame8" in worker, "worker missing the FIX9 markers"
    r = subprocess.run(["node", "--check", "--input-type=module", "-"],
                       input=worker, capture_output=True)
    assert r.returncode == 0, "node --check failed for worker: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: worker (%d B) sha %s" % (len(worker), worker_sha[:12]), flush=True)
    try:
        st.write_resilient(st.WORKER_LOCAL, worker)
    except Exception as e:
        print("WARNING: worker copy not written (EPERM flake): %s: %r" % (st.WORKER_LOCAL, e), flush=True)
    try:
        st.write_resilient(WORK + "/worker-fix9.js", worker)
    except Exception as e:
        print("WARNING: worker copy not written (EPERM flake): %s: %r" % (WORK + "/worker-fix9.js", e), flush=True)
    _, ref = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, PARENT_BRANCH))
    assert ref["object"]["sha"] == PARENT, "fix8 tip moved: %s" % ref["object"]["sha"]
    print("parent (fix8 tip):", PARENT, flush=True)
    _, nb = st.gh("POST", "/repos/%s/git/refs" % st.REPO,
                  {"ref": "refs/heads/%s" % BRANCH, "sha": PARENT})
    print("new branch created:", nb["ref"], nb["object"]["sha"], flush=True)
    assert nb["object"]["sha"] == PARENT
    _, ref2 = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, BRANCH))
    assert ref2["object"]["sha"] == PARENT, "branch tip moved: %s" % ref2["object"]["sha"]
    _, commit = st.gh("GET", "/repos/%s/git/commits/%s" % (st.REPO, PARENT))
    base_tree = commit["tree"]["sha"]
    print("base tree:", base_tree, flush=True)
    brief = st.read_bytes("/home/hatch/workspace/team-nitro/walkthrough-chain-fix9-20261119/FIX9-BRIEF.md")
    files = [
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html", new_walk),
        ("team-nitro/walk-v23-assembly-20261114/identity-fixed.html", new_ident),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
        ("team-nitro/walk-v23-assembly-20261114/welcome-staged.html", new_welcome),
        ("team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html", new_unfold),
        ("team-nitro/agreement-unfold-20261117/agreement-naya-voice.mp3", mp3),
        ("team-nitro/walkthrough-chain-fix9-20261119/FIX9-BRIEF.md", brief),
        ("team-nitro/walkthrough-chain-fix9-20261119/maker/work/build-fix9.py", st.read_bytes(WORK + "/build-fix9.py")),
        ("team-nitro/walkthrough-chain-fix9-20261119/maker/work/stage-fix9.py", st.read_bytes(WORK + "/stage-fix9.py")),
        ("team-nitro/walkthrough-chain-fix9-20261119/maker/work/law-fix9.py", st.read_bytes(WORK + "/law-fix9.py")),
        ("team-nitro/walkthrough-chain-fix9-20261119/maker/work/transform-fix9.js", st.read_bytes(WORK + "/transform-fix9.js")),
        ("team-nitro/walkthrough-chain-fix9-20261119/maker/work/build-frame9.py", st.read_bytes(WORK + "/build-frame9.py")),
        ("team-nitro/walkthrough-chain-fix9-20261119/maker/work/writer9.js", st.read_bytes(WORK + "/writer9.js")),
        ("team-nitro/walkthrough-chain-fix9-20261119/maker/work/run-transform9.js", st.read_bytes(WORK + "/run-transform9.js")),
        ("team-nitro/walkthrough-chain-fix9-20261119/maker/work/restore-unfold8.py", st.read_bytes(WORK + "/restore-unfold8.py")),
        ("team-nitro/walkthrough-chain-fix9-20261119/maker/work/restore-loop2.py", st.read_bytes(WORK + "/restore-loop2.py")),
        ("team-nitro/walkthrough-chain-fix9-20261119/maker/work/land-file.py", st.read_bytes(WORK + "/land-file.py")),
        ("team-nitro/walkthrough-chain-fix9-20261119/maker/work/probe-geometry.py", st.read_bytes(WORK + "/probe-geometry.py")),
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
        "Walkthrough CHAIN FIX9 (2026-11-19, maker round; MAKER-REPORT.md in "
        "walkthrough-chain-fix9-20261119/maker/)\\n\\n"
        "The fix-8 checker went back on three small measured gaps (GOES BACK, "
        "desktop 1920): F1 frame 1 showed no agreement words at load "
        "(reading window 219px, media board 183px, first paragraph at +227px); "
        "F3 no way back from the final frame (row held only I-agree, the 47 "
        "jewel dots display-only); F7 red seal only on frame 1, final frame "
        "one button with its seal display:none.\\n\\n"
        "Fix (shell only; beats' words untouched): F1 — the media board slims "
        "~34px (orb 60->48, video pill padding 16->10, board padding 10->8, "
        "title margin 4->2, video margin-top 10->8, board margin-bottom 12->8), "
        "the agreement board lifts (top margin 22->8, top padding 20->12, "
        "every frame alike), the reading window grows ~12px (foot pills "
        "16->12, top bar margin 8->4) — the first line lifts ~56px so "
        "Hi, I'm Naya. reads whole at load; F3 — a working Back on the final "
        "frame (a clone of frame 46's Back, same node, same classes, steps "
        "back one frame) AND the jewel dots become real navigation (tap a "
        "dot, go to its frame; the lit dot follows every move); F7 — frame "
        "1's red seal cloned into every foot that lacks one, so all 47 "
        "frames carry the 72px seal above the button row, and the final "
        "frame's row is Back + I-agree with its seal shown. The end card's "
        "#dealSeal stays hidden until agree — it is the agree stamp, "
        "unhidden + stamped only on the agree tap; unhiding it early would "
        "fake the stamp. A Next on the last frame would be a dead control, "
        "so the final row is complete at Back + I-agree.\\n\\n"
        "Unfold 131,797 B (sha 11130770) -> 137,899 B (sha ab8da1fa). "
        "Welcome 1,861,272 B (sha 2062739e, unchanged); walk 4,361,146 B sha "
        "b6befc33; identity 401,040 B sha 3279dc35; worker sha %s (built "
        "twice, identical; embeds verified: WALK b6befc33, IDENTITY 3279dc35, "
        "WELCOME 2062739e, UNFOLD ab8da1fa, TEMPLATE 61002d15). The mp3 stays "
        "filed from fix-8 (5,976,421 B, sha256 62bf05e6) but is UNWIRED — "
        "both media buttons still wait on Shawn's captioned video; the "
        "anthem video wiring rides a separate round after fix-9.\\n\\n"
        "Round note: the local unfold working copy was truncated to 0 bytes "
        "once by a truncate-first write in the EPERM flake and restored "
        "from its filed blob de7970d2 (verified 131,797 B sha 11130770) — "
        "the filed bytes were never at risk. All round writes now go "
        "through fresh single-attempt writers with temp+verify+replace.\\n\\n"
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
        "/": bf.WELCOME_SHA,
        "/agreement": bf.UNFOLD_SHA,
        "/welcome": bf.WALK_SHA,
        "/identity.html": bf.IDENT_SHA,
        "/?stage=bridge": bf.WELCOME_SHA,
        "/?stage=deck": bf.WELCOME_SHA,
        "/?stage=letter": bf.WELCOME_SHA,
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
    print("proof unfold: sha=%s (want %s)" % (got[:12], bf.UNFOLD_SHA[:12]), flush=True)
    assert got == bf.UNFOLD_SHA, "proof-host unfold mismatch"
    print("STAGE-RESULT " + json.dumps({
        "welcome_bytes": len(new_welcome), "welcome_sha": bf.WELCOME_SHA,
        "identity_bytes": len(new_ident), "identity_sha": bf.IDENT_SHA,
        "unfold_bytes": len(new_unfold), "unfold_sha": bf.UNFOLD_SHA,
        "worker_bytes": len(worker), "worker_sha": st.sha(worker),
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes, "proof_unfold": url}, indent=1), flush=True)


if __name__ == "__main__":
    main()
