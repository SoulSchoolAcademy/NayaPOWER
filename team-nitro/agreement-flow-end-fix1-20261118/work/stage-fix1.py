#!/usr/bin/env python3
"""FIX1 stage + file (2026-11-18) — agreement flow-end FIX round.

Takes the edited files from edit-fix1.py (work/welcome-fix1.html,
work/unfold-fix1.html) and, per the brief:
  1. patches the builder's welcome + unfold sha asserts to the new shas
     (computed from the built files, never typed),
  2. installs the new bytes on the builder's local input paths,
  3. rebuilds the staging worker twice (deterministic sha) and verifies
     every embed by sha256,
  4. creates branch walk-end/agreement-flow-end-fix1-20261118 from 19d8c9ab,
  5. files ONE commit (welcome + worker + builder + unfold + both drivers),
  6. PUTs the worker to the walk staging worker,
  7. verifies all 7 routes by sha256 via curl.
No PR, no merge, no message to Shawn. Report to the coordinator only.
"""
import base64, hashlib, json, os, re, subprocess, sys, time

HOME = os.path.expanduser("~")
RECORDS = os.path.join(HOME, "workspace/team-nitro/agreement-flow-end-fix1-20261118")
WORK = os.path.join(RECORDS, "work")
V23 = os.path.join(HOME, "workspace/team-nitro/walk-v23-assembly-20261114")
BUILDER = os.path.join(V23, "build-v23-staging-worker.py")
WELCOME_LOCAL = os.path.join(V23, "welcome-staged.html")
WORKER_LOCAL = os.path.join(V23, "walk-beginning-staging-worker.js")
UNFOLD_LOCAL = os.path.join(HOME, "workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html")
META = os.path.join(V23, "v23-meta.json")
GH = os.path.join(HOME, "workspace/team-nitro/gh-direct.py")
CF = os.path.join(HOME, "workspace/project-intelligence/cf-worker.py")
REPO = "SoulSchoolAcademy/NayaPOWER"
NEW_BRANCH = "walk-end/agreement-flow-end-fix1-20261118"
PARENT_TIP = "19d8c9ab38687c40862a8efc7ffa032084fd2167"
CF_ACCOUNT = "b5e2a51b3e883f7722287c5f51b1196b"
CF_SCRIPT = "naya-walk-beginning-staging"
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
OLD_WELCOME_PREFIX = "018d488a"
OLD_UNFOLD_PREFIX = "fb0ab19b"
WALK_SHA = "4b5f926423d765bd750026e65986f0b67f6b52d51588fe64e857b39df7ee01c0"
IDENT_SHA = "a1550164251ef804ff51b129c75c33571fedfdbb0554cd70f094dc5ec25c984e"

def sha(b): return hashlib.sha256(b).hexdigest()

def read_bytes(p):
    with open(p, "rb") as f: return f.read()

def write_resilient(path, data, attempts=40):
    tmp = path + ".tmp-stage-fix1"
    last = None
    for n in range(attempts):
        try:
            wrote = False
            try:
                with open(tmp, "wb") as f:
                    for i in range(0, len(data), 8192):
                        f.write(data[i:i+8192])
                    f.flush(); os.fsync(f.fileno())
                got = read_bytes(tmp)
                if len(got) == len(data) and sha(got) == sha(data):
                    wrote = True
            except Exception as e:
                last = e
            if not wrote:
                r = subprocess.run(['/bin/bash', '-c', 'cat > "$1"', 'bash', tmp],
                                   input=data, capture_output=True, timeout=120)
                if r.returncode != 0:
                    raise IOError('shell write failed rc=%d' % r.returncode)
                got = read_bytes(tmp)
                if len(got) != len(data) or sha(got) != sha(data):
                    raise IOError("shell verify failed")
            os.replace(tmp, path)
            got2 = read_bytes(path)
            if len(got2) != len(data) or sha(got2) != sha(data):
                raise IOError("post-replace verify failed")
            print("wrote %s %d B sha %s" % (path, len(data), sha(data)[:12]), flush=True)
            return
        except Exception as e:
            last = e
            print("write attempt %d failed: %s" % (n + 1, e), flush=True)
            time.sleep(2 + n)
    raise IOError("write_resilient gave up on %s: %s" % (path, last))

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
    try:
        data = json.loads(payload) if payload.strip() else {}
    except json.JSONDecodeError:
        data = {"_raw": payload[:500]}
    if status >= 400 or p.returncode != 0:
        print("FAIL %s %s: HTTP %s\n%s" % (method, path, status, payload[:800]), file=sys.stderr)
        sys.exit(1)
    return status, data

def patch_builder(new_welcome_sha, new_unfold_sha):
    btxt = read_bytes(BUILDER)
    old_w = (b'assert welcome_sha.startswith("018d488a"), "welcome sha is not the '
             b'AGREEMENT FLOW-END welcome sha (2026-11-18: N hold, Smart Block, portrait, play)"')
    old_u = (b'assert unfold_sha.startswith("fb0ab19b"), "unfold sha is not the '
             b'AGREEMENT FLOW-END unfold sha (2026-11-18: Smart Show, full screen, one visual per block)"')
    assert btxt.count(old_w) == 1, "builder welcome assert not found exactly once"
    assert btxt.count(old_u) == 1, "builder unfold assert not found exactly once"
    comment_w = (
        b"# AGREEMENT FLOW-END FIX1 (2026-11-18, maker round -\n"
        b"# agreement-flow-end-fix1-20261118/work/edit-fix1.py): the welcome\n"
        b"# sha moves 018d488a -> %s: the N hold is BULLETPROOFED (render()\n"
        b"# no longer hides a shown hold; visible 3s fill ring; agree\n"
        b"# scroll guarded; deck beat 9 shows its visual, then the hold);\n"
        b"# play reads aloud for real (svg[hidden] fix; voice warm-up +\n"
        b"# pick + no-start watchdog); the letter goes full-screen (the\n"
        b"# two 640px!important caps now say max-width:none; nutshell gets\n"
        b"# the bounded scroll so no line slices mid-glyph); visuals are\n"
        b"# contain, never cropped (4:3 images in a 16:9 slot); the 'Tap\n"
        b"# the picture' pill moves below the frame. Intro row + fix-4\n"
        b"# untouched; F2 has no key handler in the bytes (UNVERIFIED).\n" % new_welcome_sha[:8].encode())
    new_w = (b'assert welcome_sha.startswith("%s"), "welcome sha is not the '
             b'AGREEMENT FLOW-END FIX1 welcome sha (2026-11-18: N hold bulletproofed, play reads aloud, letter full-screen)"' % new_welcome_sha[:8].encode())
    comment_u = (
        b"# AGREEMENT FLOW-END FIX1 (2026-11-18, same round): the unfold sha\n"
        b"# moves fb0ab19b -> %s: Play controls speech ONLY now (same\n"
        b"# distilled-script player as the intro, stop/pause/play) - it no\n"
        b"# longer advances the deck; the deck advances via Keep reading.\n"
        b"# Gentle scroll-snap on the deck (proximity) toward one block\n"
        b"# per viewport. Welcome, walk, template, identity shas unchanged.\n" % new_unfold_sha[:8].encode())
    new_u = (b'assert unfold_sha.startswith("%s"), "unfold sha is not the '
             b'AGREEMENT FLOW-END FIX1 unfold sha (2026-11-18: Play is speech-only, scroll-snap)"' % new_unfold_sha[:8].encode())
    patched = btxt.replace(old_w, comment_w + new_w).replace(old_u, comment_u + new_u)
    assert b"AGREEMENT FLOW-END FIX1 (2026-11-18" in patched
    write_resilient(BUILDER, patched)
    _rc = subprocess.run([sys.executable, "-m", "py_compile", BUILDER], capture_output=True)
    assert _rc.returncode == 0, "patched builder does not compile: %s" % _rc.stderr.decode("utf-8", "replace")[-500:]
    print("builder patched: welcome -> %s, unfold -> %s (%d B)" % (new_welcome_sha[:8], new_unfold_sha[:8], len(patched)))
    return patched

def run_builder(new_welcome, welcome_sha, unfold_sha):
    workers = []
    for n in range(2):
        r = subprocess.run([sys.executable, BUILDER, "--stdout", "--welcome-stdin"],
                           input=new_welcome, capture_output=True, timeout=300)
        assert r.returncode == 0, "builder failed: %s" % r.stderr.decode("utf-8", "replace")[-800:]
        log = r.stderr.decode("utf-8", "replace")
        for needle in (welcome_sha[:8], unfold_sha[:8], "4b5f9264", "61002d15", "a1550164"):
            assert needle in log, "builder log missing %s; log tail: %s" % (needle, log[-600:])
        workers.append(r.stdout)
        print("builder run %d: worker %d B sha=%s" % (n + 1, len(r.stdout), sha(r.stdout)))
    assert workers[0] == workers[1], "worker build not deterministic"
    w = workers[0]
    for marker in (b"fpNHold", b"FP_DISTILLED_SCRIPT", b"fp-smart-visual", b"Welcome home.", b"data-smart-block",
                   b"fpNHoldFill", b"fpSpeechVoice", b"svg[hidden]"):
        assert marker in w, "worker missing fix1 marker %s" % marker
    dec = json.JSONDecoder()
    embeds = {}
    for name in ("WALK", "IDENTITY", "WELCOME", "UNFOLD", "PERSONAL_TEMPLATE"):
        i = w.find(("const %s = " % name).encode())
        assert i >= 0, "worker missing %s" % name
        j = w.find(b'"', i)
        val, _ = dec.raw_decode(w[j:].decode("utf-8"))
        embeds[name] = val.encode("utf-8")
    print("worker embeds: " + ", ".join("%s %d B %s" % (k, len(v), sha(v)[:8]) for k, v in embeds.items()))
    assert sha(embeds["WELCOME"]) == welcome_sha, "worker does not embed the new welcome"
    assert sha(embeds["UNFOLD"]) == unfold_sha, "worker does not embed the new unfold"
    assert sha(embeds["WALK"]) == WALK_SHA, "worker walk changed"
    assert sha(embeds["IDENTITY"]) == IDENT_SHA, "worker identity changed"
    assert sha(embeds["PERSONAL_TEMPLATE"])[:8] == "61002d15", "worker template changed"
    return w

def node_check(data, label):
    tmp = os.path.join(WORK, "worker-check-%s.js" % label)
    write_resilient(tmp, data)
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    assert r.returncode == 0, "node --check failed for %s: %s" % (label, r.stderr[:500])
    print("node --check OK: %s (%d B)" % (label, len(data)))
    os.remove(tmp)

def commit_message(worker_sha, worker_bytes, welcome_sha, unfold_sha):
    return (
        "Agreement FLOW-END FIX1 (2026-11-18, maker round; MAKER-REPORT.md in "
        "agreement-flow-end-fix1-20261118/)\n\n"
        "The eye's three GOES-BACK failures, fixed live — all wiring, not "
        "missing code. (1) THE N HOLD: render() hid the hold on any render "
        "while S.view!=='agree', so the deck-end hold (shown while "
        "S.view==='deck') died in the same task before one frame painted — "
        "render() never hides a shown hold now; the agree button's 2000ms "
        "scroll-to-login no longer yanks the viewport under the hold; the "
        "hold carries a VISIBLE white fill ring that completes over "
        "exactly 3000ms; deck beat 9 shows its visual first, then the "
        "hold, like deck-end Enter. (2) PLAY READS ALOUD: the author rule "
        ".p3-naya-play svg{display:block} defeated [hidden], so the pause "
        "bars rendered beside the play triangle — svg[hidden] now hides; "
        "the player warms up voices, picks en-US, and a 2.5s no-start "
        "watchdog says so instead of failing silently; the unfold's Play "
        "now controls speech only (same distilled script, stop/pause/play) "
        "and no longer advances the deck. (3) THE LETTER IS FULL-SCREEN: "
        "the two live 640px!important caps now say max-width:none, and "
        "the nutshell gets the bounded scroll so no line slices mid-glyph; "
        "visuals are object-fit:contain (the 4:3 letter images in a 16:9 "
        "slot were cropped top and bottom by cover); the 'Tap the picture' "
        "pill moves below the frame. F2: no F2 key handler exists in the "
        "bytes (only Escape x3) — UNVERIFIED, honestly. Intro row and "
        "fix-4 untouched.\n\n"
        "Worker built twice, identical sha %s (%d B); embeds verified: "
        "WALK 4b5f9264, IDENTITY a1550164, WELCOME %s, UNFOLD %s, TEMPLATE "
        "61002d15.\n\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after "
        "the PUT. Worker PUT with --meta v23-meta.json (WELCOME_ASSETS "
        "1cf80db6183245d19dd5296645a12bd0 intact). NO PR, NO MERGE — the "
        "checker and the captain come after this seat. Nothing live - the "
        "finished update goes LIVE on the main URL only on Shawn's tap, "
        "after his eye."
        % (worker_sha[:8], worker_bytes, welcome_sha[:8], unfold_sha[:8], STAGING))

def main():
    new_welcome = read_bytes(os.path.join(WORK, "welcome-fix1.html"))
    new_unfold = read_bytes(os.path.join(WORK, "unfold-fix1.html"))
    welcome_sha, unfold_sha = sha(new_welcome), sha(new_unfold)
    print("inputs: welcome %d B %s, unfold %d B %s" % (len(new_welcome), welcome_sha[:8], len(new_unfold), unfold_sha[:8]))
    _, ref = gh("GET", "/repos/%s/git/refs/heads/%s" % (REPO, "walk-end/agreement-flow-end-20261118"))
    print("base branch tip:", ref["object"]["sha"])
    assert ref["object"]["sha"] == PARENT_TIP, "base branch tip moved: %s" % ref["object"]["sha"]
    builder = patch_builder(welcome_sha, unfold_sha)
    write_resilient(WELCOME_LOCAL, new_welcome)
    write_resilient(UNFOLD_LOCAL, new_unfold)
    worker = run_builder(new_welcome, welcome_sha, unfold_sha)
    node_check(worker, "worker")
    write_resilient(WORKER_LOCAL, worker)
    worker_file = os.path.join(WORK, "worker-fix1.js")
    write_resilient(worker_file, worker)
    _, nb = gh("POST", "/repos/%s/git/refs" % REPO,
               {"ref": "refs/heads/%s" % NEW_BRANCH, "sha": PARENT_TIP})
    print("new branch created:", nb["ref"], nb["object"]["sha"])
    assert nb["object"]["sha"] == PARENT_TIP
    _, ref2 = gh("GET", "/repos/%s/git/refs/heads/%s" % (REPO, NEW_BRANCH))
    assert ref2["object"]["sha"] == PARENT_TIP, "branch tip moved: %s" % ref2["object"]["sha"]
    _, commit = gh("GET", "/repos/%s/git/commits/%s" % (REPO, PARENT_TIP))
    base_tree = commit["tree"]["sha"]
    print("base tree:", base_tree)
    driver = read_bytes(os.path.join(WORK, "edit-fix1.py"))
    stage_script = read_bytes(os.path.join(WORK, "stage-fix1.py"))
    files = [
        ("team-nitro/walk-v23-assembly-20261114/welcome-staged.html", new_welcome),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
        ("team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html", new_unfold),
        ("team-nitro/agreement-flow-end-fix1-20261118/work/edit-fix1.py", driver),
        ("team-nitro/agreement-flow-end-fix1-20261118/work/stage-fix1.py", stage_script),
    ]
    blobs = {}
    for path, data in files:
        _, blob = gh("POST", "/repos/%s/git/blobs" % REPO,
                     {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"})
        blobs[path] = blob["sha"]
        print("blob %s: %s (%d B)" % (path.split("/")[-1], blob["sha"], len(data)))
    _, tree = gh("POST", "/repos/%s/git/trees" % REPO,
                 {"base_tree": base_tree,
                  "tree": [{"path": p, "mode": "100644", "type": "blob", "sha": s} for p, s in blobs.items()]})
    print("new tree:", tree["sha"])
    msg = commit_message(sha(worker), len(worker), welcome_sha, unfold_sha)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _, cm = gh("POST", "/repos/%s/git/commits" % REPO,
               {"message": msg, "tree": tree["sha"], "parents": [PARENT_TIP],
                "author": {"name": "nayapower-lane-agent[bot]",
                           "email": "338161897+nayapower-lane-agent[bot]@users.noreply.github.com",
                           "date": now},
                "committer": {"name": "GitHub", "email": "noreply@github.com", "date": now}})
    commit_sha = cm["sha"]
    print("commit sha:", commit_sha)
    _, ref3 = gh("PATCH", "/repos/%s/git/refs/heads/%s" % (REPO, NEW_BRANCH),
                 {"sha": commit_sha, "force": False})
    print("branch now:", ref3["object"]["sha"])
    assert ref3["object"]["sha"] == commit_sha
    for path, data in files:
        _, rb = gh("GET", "/repos/%s/git/blobs/%s" % (REPO, blobs[path]))
        raw = base64.b64decode("".join(rb["content"].split()))
        assert len(raw) == len(data) and sha(raw) == sha(data), "blob read-back mismatch for %s" % path
        print("blob read-back OK:", path.split("/")[-1], len(raw), "bytes, sha match")
    r = subprocess.run([sys.executable, CF, "put-script", CF_ACCOUNT, CF_SCRIPT,
                        worker_file, "--meta", META],
                       capture_output=True, timeout=300)
    out = r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace")
    print("staging PUT rc=%d:\n%s" % (r.returncode, out[:2000]))
    assert r.returncode == 0 and "200" in out, "staging PUT failed"
    ua = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
    expect = {
        "/": welcome_sha,
        "/agreement": unfold_sha,
        "/welcome": WALK_SHA,
        "/identity.html": IDENT_SHA,
        "/?stage=bridge": welcome_sha,
        "/?stage=deck": welcome_sha,
        "/?stage=letter": welcome_sha,
    }
    routes = {}
    for route, want in expect.items():
        got = None
        for attempt in (1, 2):
            rr = subprocess.run(["curl", "-s", "-A", ua, STAGING + route],
                                capture_output=True, timeout=120)
            got = sha(rr.stdout)
            print("route %s: %d B sha=%s (want %s) attempt %d"
                  % (route, len(rr.stdout), got[:12], want[:12], attempt))
            if got == want:
                break
            time.sleep(15)
        routes[route] = got
        assert got == want, "route %s mismatch: got %s want %s" % (route, got, want)
    print("STAGE-RESULT " + json.dumps({
        "welcome_bytes": len(new_welcome), "welcome_sha": welcome_sha,
        "unfold_bytes": len(new_unfold), "unfold_sha": unfold_sha,
        "worker_bytes": len(worker), "worker_sha": sha(worker),
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes}, indent=1))

if __name__ == "__main__":
    main()
