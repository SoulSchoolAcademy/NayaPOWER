#!/usr/bin/env python3
"""FIX8 stage (2026-11-19): file the fix-8 build in branch
walkthrough/chain-fix8-20261119 from the fix-7 tip 3c621b7d, one commit:
walk (unchanged), identity (unchanged), the new worker, the edited
builder (asserts -> 2062739e welcome + 0bb21457 unfold), the new unfold
(in-memory bytes, never on disk), the edited welcome (F6: no-alias
auto-enter removed), the narration mp3 (F9, filed), and the fix-8 work
scripts + brief. Then blob read-back, PUT the worker, and verify the 7
staging routes + the mp3 on the proof host. Usage:
python3 stage-fix8.py <worker_sha>

Route expectations: / -> welcome (new), /agreement -> unfold (new),
/welcome -> walk, /identity.html -> identity,
/?stage=bridge|deck|letter -> welcome (new).
"""
import base64, hashlib, importlib.util, json, subprocess, sys, time, urllib.request

SPEC3 = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC3)
SPEC3.loader.exec_module(st)
SPEC8 = importlib.util.spec_from_file_location(
    "build_fix8", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix8-20261119/work/build-fix8.py")
bf = importlib.util.module_from_spec(SPEC8)
SPEC8.loader.exec_module(bf)

WORK = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix8-20261119/work"
BRANCH = "walkthrough/chain-fix8-20261119"
PARENT_BRANCH = "walkthrough/chain-fix7-20261119"
PARENT = "3c621b7d2cc3eca539ed99d5625ca58c4599ef68"
# Third staging commit: the second fix-8 commit (e120ca21) is already on
# this branch; the render probe caught two live defects (the button row
# still clipped below the deck, and the first Next tap only switching
# the picture phase instead of advancing), so the beat padding, the
# foot, the media frame and the navigation were reworked. This run
# files commit 3 on top of commit 2.
TIP1 = "e120ca21d9510b98854cde85c06e1a2841bb3d75"
WALK_LOCAL = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html"
MP3_LOCAL = "/home/hatch/workspace/your_files/agreement-naya-voice.mp3"
MP3_SHA = "62bf05e68a036e86b5aa3280c16b9dd810dda711abf1fd34612cda10b2b9261a"


def blob_sha(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\x00" + b).hexdigest()


def main():
    worker_sha = sys.argv[1]
    assert worker_sha != "PLACEHOLDER", "pass the built worker sha as argv[1]"
    # The pipeline extracts the fix-7 unfold from the LOCAL worker file,
    # but build-fix8.py already overwrote it with the fix-8 worker (the
    # writes landed this round). Restore the fix-7 worker copy first —
    # the durable work copy in the fix-7 records dir — so the pipeline
    # sees its e21f08d0 base again. The staged worker is untouched until
    # the PUT below; this script re-writes the fix-8 worker locally after
    # the rebuild.
    r = subprocess.run(["cp",
                        "/home/hatch/workspace/team-nitro/walkthrough-chain-fix7-20261119/work/worker-fix7.js",
                        st.WORKER_LOCAL], capture_output=True)
    assert r.returncode == 0, "fix-7 worker restore failed: %s" % r.stderr.decode("utf-8", "replace")[:200]
    w7 = st.read_bytes(st.WORKER_LOCAL)
    assert st.sha(w7) == "06874a9a69d55e72247dd4218ac9ef44d62b766eebe0661835591a9487584959", "fix-7 worker restore mismatch"
    print("local worker restored to fix-7 for the pipeline", flush=True)
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
    assert b'assert unfold_sha.startswith("0bb21457")' in builder, "builder unfold assert not moved"
    assert b'assert welcome_sha.startswith("2062739e")' in builder, "builder welcome assert not moved"
    assert b'UNFOLD_RAW' in builder, "builder missing UNFOLD_RAW"
    assert b"stay on the entrance" in new_welcome, "welcome F6 edit missing"
    worker = bf.run_builder8(new_welcome, bf.WELCOME_SHA, bf.IDENT_SHA, bf.UNFOLD_SHA, new_unfold)
    print("worker rebuilt: %d B sha %s" % (len(worker), st.sha(worker)), flush=True)
    assert st.sha(worker) == worker_sha, "worker sha moved: %s" % st.sha(worker)
    assert b"fpFrame8" in worker and b"fpMediaFrame" in worker and b"fpFrame7" in worker, "worker missing the FIX8 markers"
    r = subprocess.run(["node", "--check", "--input-type=module", "-"],
                       input=worker, capture_output=True)
    assert r.returncode == 0, "node --check failed for worker: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: worker (%d B) sha %s" % (len(worker), worker_sha[:12]), flush=True)
    for path in (st.WORKER_LOCAL, WORK + "/worker-fix8.js"):
        try:
            st.write_resilient(path, worker)
        except Exception as e:
            print("WARNING: worker copy not written (EPERM flake): %s: %r" % (path, e), flush=True)
    _, ref = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, PARENT_BRANCH))
    assert ref["object"]["sha"] == PARENT, "fix7 tip moved: %s" % ref["object"]["sha"]
    print("parent (fix7 tip):", PARENT, flush=True)
    _, ref8 = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, BRANCH))
    assert ref8["object"]["sha"] == TIP1, "fix8 tip moved: %s" % ref8["object"]["sha"]
    print("fix8 tip (commit 2):", TIP1, flush=True)
    _, commit = st.gh("GET", "/repos/%s/git/commits/%s" % (st.REPO, TIP1))
    base_tree = commit["tree"]["sha"]
    print("base tree:", base_tree, flush=True)
    files = [
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html", new_walk),
        ("team-nitro/walk-v23-assembly-20261114/identity-fixed.html", new_ident),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
        ("team-nitro/walk-v23-assembly-20261114/welcome-staged.html", new_welcome),
        ("team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html", new_unfold),
        ("team-nitro/agreement-unfold-20261117/agreement-naya-voice.mp3", mp3),
        ("team-nitro/walkthrough-chain-fix8-20261119/FIX8-BRIEF.md", st.read_bytes(
            "/home/hatch/workspace/team-nitro/walkthrough-chain-fix8-20261119/FIX8-BRIEF.md")),
        ("team-nitro/walkthrough-chain-fix8-20261119/work/build-fix8.py", st.read_bytes(WORK + "/build-fix8.py")),
        ("team-nitro/walkthrough-chain-fix8-20261119/work/stage-fix8.py", st.read_bytes(WORK + "/stage-fix8.py")),
        ("team-nitro/walkthrough-chain-fix8-20261119/work/law-fix8.py", st.read_bytes(WORK + "/law-fix8.py")),
        ("team-nitro/walkthrough-chain-fix8-20261119/work/transform-fix8.js", st.read_bytes(WORK + "/transform-fix8.js")),
        ("team-nitro/walkthrough-chain-fix8-20261119/work/build-frame8.py", st.read_bytes(WORK + "/build-frame8.py")),
        ("team-nitro/walkthrough-chain-fix8-20261119/work/probe-render.py", st.read_bytes(WORK + "/probe-render.py")),
        ("team-nitro/walkthrough-chain-fix8-20261119/work/probe-home.py", st.read_bytes(WORK + "/probe-home.py")),
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
        "Walkthrough CHAIN FIX8 (2026-11-19, maker round; MAKER-REPORT.md in "
        "walkthrough-chain-fix8-20261119/) — commit 3\n\n"
        "Commit 3 reworks the render-probe findings: the button row was\n"
        "still clipped below the deck (the beat's own 32/24px padding,\n"
        "content-box, made it 60px taller than its 463px deck), and the\n"
        "first Next tap only switched the picture phase instead of\n"
        "advancing. The beat is now border-box with tight padding, the\n"
        "seal tightens 84 -> 72, the media frame slims, the two-tap\n"
        "talk/visual phase is gone (one tap = one frame; the picture\n"
        "shows inside the reading window), and the deck's buttons are\n"
        "cloned so FIX7's two-tap listener never fires. Nothing else\n"
        "changes.\n\n"
        "The eye sent fix-7 back (GOES BACK, desktop 1920): frame 1 a 90px "
        "strip, the board blanking itself, Next never visibly advancing, "
        "Play doing nothing, flaky top-bar photo, home entrance + nav "
        "invisible, the red N + three buttons not matching, plus F9 the "
        "media frame. Diagnosis was measured in the VM Chromium render "
        "probe (screenshots + rects), not guessed: deckBody was 86px tall "
        "(header + dots + foot-links ate the 579px content box); the "
        "master-frame PNG has an OPAQUE black centre and sat at z-index "
        "60 above the stage, painting over all content once loaded; FIX7 "
        "navigation keyed off the deck's fp-smart-visual class, which "
        "wireDeck never clears on advance; the fresh-visitor auto-enter "
        "in the welcome file put the agreement bridge over the entrance "
        "and nav on load.\n\n"
        "Fix (shell only; beats' words untouched): frame layer behind "
        "the stage (z 0); page header out on every frame (top bar carries "
        "the headline), dots + foot-links slim, seal 120->84; FIX8 owns "
        "navigation with its own per-beat talk/visual phase, one "
        "kr.click() per Next, Back present-but-disabled on frame 1, "
        "I-agree moved into the pinned foot row; top-bar faces gain an "
        "onerror chain (retry, then the filed crystal N); the play orb "
        "moves into the media frame on frame 1 and drives the verified "
        "narration mp3 (AUDIO on top, VIDEO slot below — the slot reveals "
        "the anthem's opening words until the captioned video arrives; "
        "the Oct-29 mp4 and the NotebookLM m4a files are never wired); "
        "welcome: fresh visitors stay on the entrance (no-alias "
        "auto-enter removed; Enter / ?stage= / restores untouched). No "
        "Welcome button or pill introduced anywhere.\n\n"
        "Unfold 117,636 B (sha e21f08d0) -> 131,955 B (sha 0bb21457). "
        "Welcome 1,859,867 B (sha d79793c0) -> 1,861,272 B (sha 2062739e). "
        "Walk 4,361,146 B sha b6befc33; identity 401,040 B sha 3279dc35; "
        "worker sha %s (built twice, identical; embeds verified: WALK "
        "b6befc33, IDENTITY 3279dc35, WELCOME 2062739e, UNFOLD 0bb21457, "
        "TEMPLATE 61002d15). Narration mp3 filed: 5,976,421 B, sha256 "
        "62bf05e6, 12m27s.\n\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after the PUT. "
        "NO PR, NO MERGE — the checker and the captain come after this seat. "
        "Nothing live." % (worker_sha[:8], st.STAGING))
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _, cm = st.gh("POST", "/repos/%s/git/commits" % st.REPO,
                  {"message": msg, "tree": tree["sha"], "parents": [TIP1],
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
    mp3_url = ("https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/agreement-unfold-20261117/agreement-naya-voice.mp3"
               "&ref=walkthrough/chain-fix8-20261119&cb=" + MP3_SHA)
    req = urllib.request.Request(mp3_url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=120) as resp:
        served = resp.read()
    print("proof-host mp3: %d B sha %s (want %d B %s)" % (
        len(served), st.sha(served)[:12], len(mp3), st.sha(mp3)[:12]), flush=True)
    assert len(served) == len(mp3) and st.sha(served) == st.sha(mp3), "proof-host mp3 mismatch"
    frame_url = ("https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/agreement-unfold-20261117/master-frame.png"
                 "&ref=walkthrough/chain-fix7-20261119&cb=5a4dc2f9ca703945f12cec0b39b491d728e69c4a")
    req = urllib.request.Request(frame_url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=60) as resp:
        served = resp.read()
    print("proof-host master-frame: %d B sha %s" % (len(served), st.sha(served)[:12]), flush=True)
    assert st.sha(served)[:12] == "865357f66059"[:12], "proof-host frame asset mismatch"
    print("STAGE-RESULT8 " + json.dumps({
        "walk_bytes": len(new_walk), "walk_sha": bf.WALK_SHA,
        "identity_bytes": len(new_ident), "identity_sha": bf.IDENT_SHA,
        "welcome_bytes": len(new_welcome), "welcome_sha": bf.WELCOME_SHA,
        "unfold_bytes": len(new_unfold), "unfold_sha": bf.UNFOLD_SHA,
        "mp3_bytes": len(mp3), "mp3_sha": MP3_SHA,
        "worker_bytes": len(worker), "worker_sha": worker_sha,
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes}, indent=1), flush=True)


if __name__ == "__main__":
    main()
