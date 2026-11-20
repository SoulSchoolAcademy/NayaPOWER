#!/usr/bin/env python3
"""AGREEMENT-DISTILL stage, fix-2 (2026-11-19): file the button-destination
wiring as a new commit on walkthrough/agreement-distill-20261119, on top of
the fix-1 tip 7c5c89ec (parent chain verified). No page bytes change in this
commit — the transform guards + this script + the report are the new files;
the worker is rebuilt in-memory (deterministic, identical sha) and re-PUT,
and the 7 staging routes + the proof-host unfold are re-verified by sha256.
Fully in-memory (EPERM flake: no disk writes at all — the worker, unfold
and welcome come from build-mem.py).

Route expectations: / -> welcome (distill), /agreement -> unfold (distill),
/welcome -> walk, /identity.html -> identity,
/?stage=bridge|deck|letter -> welcome (distill).
Usage: python3 stage-distill.py"""
import base64, hashlib, importlib.util, json, subprocess, sys, time, urllib.request

SPEC3 = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC3)
SPEC3.loader.exec_module(st)
SPECBM = importlib.util.spec_from_file_location(
    "build_mem", "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-20261119/maker/work/build-mem.py")
bm = importlib.util.module_from_spec(SPECBM)
SPECBM.loader.exec_module(bm)

WORK = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-20261119/maker/work"
BRANCH = "walkthrough/agreement-distill-20261119"
PARENT_BRANCH = "walkthrough/agreement-frame-20261119"
PARENT = "83ff20f641d3c878261d56d1cbe01ac8d589e8d9"
WALK_LOCAL = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html"
MP3_LOCAL = "/home/hatch/workspace/your_files/agreement-naya-voice.mp3"
MP3_SHA = "62bf05e68a036e86b5aa3280c16b9dd810dda711abf1fd34612cda10b2b9261a"


def blob_sha(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\x00" + b).hexdigest()


def main():
    new_walk = st.read_bytes(WALK_LOCAL)
    new_ident = st.read_bytes(st.IDENT_LOCAL)
    new_unfold, new_welcome, worker = bm.build_worker()
    builder = st.read_bytes(st.BUILDER)
    mp3 = st.read_bytes(MP3_LOCAL)
    unfold_sha, welcome_sha, worker_sha = bm.sha(new_unfold), bm.sha(new_welcome), bm.sha(worker)
    print("inputs: walk %d B %s" % (len(new_walk), st.sha(new_walk)), flush=True)
    print("inputs: identity %d B %s" % (len(new_ident), st.sha(new_ident)), flush=True)
    print("inputs: welcome %d B %s" % (len(new_welcome), welcome_sha), flush=True)
    print("inputs: unfold %d B %s" % (len(new_unfold), unfold_sha), flush=True)
    print("inputs: worker %d B %s" % (len(worker), worker_sha), flush=True)
    print("inputs: mp3 %d B sha %s blob %s" % (len(mp3), st.sha(mp3), blob_sha(mp3)[:8]), flush=True)
    assert st.sha(new_walk) == "b6befc332d65dd26d01649edd09810e9f83284a73a10a6af30f6691f5f118773", "walk moved"
    assert st.sha(new_ident) == "3279dc3572337e5e971369a3742effcaac7f6e5b059192ddaa6e689f0f92886c", "identity moved"
    assert st.sha(mp3) == MP3_SHA, "mp3 moved"
    assert len(mp3) == 5976421, "mp3 size moved"
    assert ('assert unfold_sha.startswith("%s")' % unfold_sha[:8]).encode() in builder, "builder unfold assert not moved"
    assert ('assert welcome_sha.startswith("%s")' % welcome_sha[:8]).encode() in builder, "builder welcome assert not moved"
    assert b"UNFOLD_RAW" in builder, "builder missing UNFOLD_RAW"
    assert b"stay on the entrance" in new_welcome, "welcome F6 edit missing"
    assert b"fpFrameAF" in new_unfold and b"fpDeckAF" in new_welcome, "AF markers missing"
    assert b"af-prog" in new_unfold and b"wireProgDistill" in new_unfold, "progress pill missing"
    import re as _re
    def _visible(b):
        s = b.decode("utf-8", "replace")
        s = _re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s)
        return s
    assert "read the whole letter" not in _visible(new_unfold), "read-it-all text remains in unfold"
    assert "read the whole letter" not in _visible(new_welcome), "read-it-all text remains in welcome"
    # The plain-letter dialog + every opener element are gone; only
    # unreachable dead JS remains (openPlainLetter's two listeners are
    # null-guarded and their elements are removed, so no click can reach it).
    for _id in (b'id="dealPlain"', b'id="dealEyeMain"', b'id="letterAll"',
                b'id="fpLinkLetterAll"', b'id="deckAll"'):
        assert _id not in new_unfold and _id not in new_welcome, "long-version element remains: %s" % _id
    _, ref = st.gh("GET", "/repos/%s/git/refs/heads/%s" % (st.REPO, PARENT_BRANCH))
    assert ref["object"]["sha"] == PARENT, "v5 tip moved: %s" % ref["object"]["sha"]
    print("parent (v5 tip):", PARENT, flush=True)
    probe = subprocess.run([sys.executable, st.GH, "GET",
                            "/repos/%s/git/refs/heads/%s" % (st.REPO, BRANCH)], capture_output=True)
    pout = probe.stdout.decode("utf-8", "replace")
    pstatus = int(pout.split("\n", 1)[0].split()[1]) if pout.startswith("HTTP") else -1
    assert pstatus == 200, "distill branch missing (HTTP %s) — run-1 commit expected" % pstatus
    tip1 = json.loads(pout.split("\n", 1)[1])["object"]["sha"]
    assert tip1 == "7c5c89ec3abd4c8b2b5616dc25ece114847c4ac2", "distill branch tip moved: %s" % tip1
    print("distill branch tip (fix-1 commit):", tip1, flush=True)
    _, tip1c = st.gh("GET", "/repos/%s/git/commits/%s" % (st.REPO, tip1))
    assert tip1c["parents"][0]["sha"] == "4ed1fbbeeebf5db6d7ecadc78c1d2342be283327", "fix-1 commit is not on the run-1 commit"
    _, commit = st.gh("GET", "/repos/%s/git/commits/%s" % (st.REPO, tip1))
    base_tree = commit["tree"]["sha"]
    print("base tree (fix-1):", base_tree, flush=True)
    brief = st.read_bytes("/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-20261119/AGREEMENT-DISTILL-BRIEF.md")
    files = [
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html", new_walk),
        ("team-nitro/walk-v23-assembly-20261114/identity-fixed.html", new_ident),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
        ("team-nitro/walk-v23-assembly-20261114/welcome-staged.html", new_welcome),
        ("team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html", new_unfold),
        ("team-nitro/agreement-unfold-20261117/agreement-naya-voice.mp3", mp3),
        ("team-nitro/walkthrough-agreement-distill-20261119/AGREEMENT-DISTILL-BRIEF.md", brief),
        ("team-nitro/walkthrough-agreement-distill-20261119/maker/work/transform-distill.js", st.read_bytes(WORK + "/transform-distill.js")),
        ("team-nitro/walkthrough-agreement-distill-20261119/maker/work/boards-distill.js", st.read_bytes(WORK + "/boards-distill.js")),
        ("team-nitro/walkthrough-agreement-distill-20261119/maker/work/build-distill.py", st.read_bytes(WORK + "/build-distill.py")),
        ("team-nitro/walkthrough-agreement-distill-20261119/maker/work/build-mem.py", st.read_bytes(WORK + "/build-mem.py")),
        ("team-nitro/walkthrough-agreement-distill-20261119/maker/work/stage-distill.py", st.read_bytes(WORK + "/stage-distill.py")),
        ("team-nitro/walkthrough-agreement-distill-20261119/maker/work/law-distill.py", st.read_bytes(WORK + "/law-distill.py")),
        ("team-nitro/walkthrough-agreement-distill-20261119/maker/work/writer9.js", st.read_bytes(WORK + "/writer9.js")),
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
        "Walkthrough AGREEMENT DISTILL v1 fix-2 (2026-11-19, maker round; "
        "MAKER-REPORT.md in walkthrough-agreement-distill-20261119/maker/)\\n\\n"
        "On top of the fix-1 commit: the button-destination standing order "
        "(Shawn 20:14 MST). Every button in the three presentations was "
        "audited in code and lands on a current, relevant page — Back, Keep "
        "reading, Next, the buttons into the presentations, and the final "
        "I-agree (full table in MAKER-REPORT.md). The transform now carries "
        "destination guards, so a lost destination fails the build: 36 "
        "Keep-reading buttons on the unfold, the I-agree bridge destination, "
        "the media block, the three /agreement buttons (four navigation "
        "sites), and the stage agree/exit/resume functions. No button "
        "destination needed changing. NO PAGE BYTES CHANGED in this commit: "
        "unfold sha 760b8ea0 and welcome sha d9577f61 are identical to "
        "fix-1, so the worker sha is identical too; the changed files are "
        "the transform guards, this stage script, and the report.\\n\\n"
        "Unfold %d B (sha %s); welcome %d B (sha %s). Walk 4,361,146 B "
        "sha b6befc33; identity 401,040 B sha 3279dc35; worker sha %s "
        "(built twice in-memory, identical; embeds verified). The mp3 stays filed "
        "(5,976,421 B, sha256 62bf05e6) but is UNWIRED — both media "
        "buttons still wait on Shawn's captioned video; the anthem video "
        "wiring rides a separate round.\\n\\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after the PUT. "
        "NO PR, NO MERGE — the checker and the captain come after this seat. "
        "Nothing live." % (len(new_unfold), unfold_sha[:8], len(new_welcome), welcome_sha[:8],
                            worker_sha[:8], st.STAGING))
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _, cm = st.gh("POST", "/repos/%s/git/commits" % st.REPO,
                  {"message": msg, "tree": tree["sha"], "parents": [tip1],
                   "author": {"name": "nayapower-lane-agent[bot]",
                              "email": "338161897+nayapower-lane-agent[bot]@users.noreply.github.com",
                              "date": now},
                   "committer": {"name": "GitHub", "email": "noreply@github.com", "date": now}})
    commit_sha = cm["sha"]
    print("commit sha:", commit_sha, flush=True)
    _, ref2 = st.gh("PATCH", "/repos/%s/git/refs/heads/%s" % (st.REPO, BRANCH),
                    {"sha": commit_sha, "force": False})
    print("branch updated:", ref2["ref"], ref2["object"]["sha"], flush=True)
    assert ref2["object"]["sha"] == commit_sha
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
        "/welcome": "b6befc332d65dd26d01649edd09810e9f83284a73a10a6af30f6691f5f118773",
        "/identity.html": "3279dc3572337e5e971369a3742effcaac7f6e5b059192ddaa6e689f0f92886c",
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
        "identity_bytes": len(new_ident), "identity_sha": "3279dc3572337e5e971369a3742effcaac7f6e5b059192ddaa6e689f0f92886c",
        "unfold_bytes": len(new_unfold), "unfold_sha": unfold_sha,
        "worker_bytes": len(worker), "worker_sha": worker_sha,
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes, "proof_unfold": url}, indent=1), flush=True)


if __name__ == "__main__":
    main()
