#!/usr/bin/env python3
"""CONDITIONS stage + file (2026-11-18) - agreement flow-end FIX1 conditions.

Takes the edited file from edit-cond.py (work/unfold-cond.html) and:
  1. patches the builder's unfold sha assert to the new sha (computed
     from the built file, never typed); the welcome assert is untouched
     (welcome bytes do not change in this round),
  2. installs the new unfold bytes on the builder's local input path,
  3. rebuilds the staging worker twice (deterministic sha) and verifies
     every embed by sha256,
  4. files ONE commit on the SAME branch
     (walk-end/agreement-flow-end-fix1-20261118, parent 43c8ba1e),
  5. PUTs the worker to the walk staging worker,
  6. verifies all 7 routes by sha256 via curl.
No PR, no merge, no message to Shawn. Report to the coordinator only.
Welcome is NOT in the commit - its bytes are unchanged (blob 0f40f0c5).
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
BRANCH = "walk-end/agreement-flow-end-fix1-20261118"
PARENT_TIP = "43c8ba1e399bdc9a5a03c627865586559c83b995"
BASE_TREE = "84d673749a925039e2d20c64c705d37d81abbcfa"
CF_ACCOUNT = "b5e2a51b3e883f7722287c5f51b1196b"
CF_SCRIPT = "naya-walk-beginning-staging"
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
WELCOME_SHA = "d367efe125a4e06f99be80a79419cf7c498315bfec56c1959ce8c92095276998"
WALK_SHA = "4b5f926423d765bd750026e65986f0b67f6b52d51588fe64e857b39df7ee01c0"
IDENT_SHA = "a1550164251ef804ff51b129c75c33571fedfdbb0554cd70f094dc5ec25c984e"

def sha(b): return hashlib.sha256(b).hexdigest()

def read_bytes(p):
    with open(p, "rb") as f: return f.read()

def write_resilient(path, data, attempts=40):
    tmp = path + ".tmp-stage-cond"
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

def patch_builder(new_unfold_sha):
    btxt = read_bytes(BUILDER)
    old_u = (b'assert unfold_sha.startswith("c295061a"), "unfold sha is not the '
             b'AGREEMENT FLOW-END FIX1 unfold sha (2026-11-18: Play is speech-only, scroll-snap)"')
    assert btxt.count(old_u) == 1, "builder unfold assert not found exactly once"
    # the welcome assert must still say d367efe1 - this round does not move it
    assert b'assert welcome_sha.startswith("d367efe1")' in btxt, "builder welcome assert moved?!"
    comment_u = (
        b"# AGREEMENT FLOW-END FIX1 CONDITIONS (2026-11-18, conditions seat -\n"
        b"# agreement-flow-end-fix1-20261118/work/edit-cond.py): the unfold sha\n"
        b"# moves c295061a -> %s: checker Condition 1 - the visual-phase slot\n"
        b"# rule (.letter-beat.fp-smart-visual .lb-showcase img) goes\n"
        b"# object-fit:cover -> contain, so the 4:3 letter images show whole\n"
        b"# on /agreement too (the two circular-photo cover rules stay);\n"
        b"# checker Condition 2 - the unfold player's 2.5s watchdog now\n"
        b"# writes 'Voice not available on this device - read below' into\n"
        b"# the player's tip element (#playTip, reusing the existing unused\n"
        b"# .play-note style) instead of returning to idle silently.\n"
        b"# Watchdog mechanics unchanged (warm-up, pick, assignment, clear\n"
        b"# on start/end/error). Welcome, walk, template, identity shas\n"
        b"# unchanged. Divider (.ib-foot-logo) untouched - the eye's call.\n" % new_unfold_sha[:8].encode())
    new_u = (b'assert unfold_sha.startswith("%s"), "unfold sha is not the '
             b'AGREEMENT FLOW-END FIX1 CONDITIONS unfold sha (2026-11-18: visual slot contain, no-voice tip)"' % new_unfold_sha[:8].encode())
    patched = btxt.replace(old_u, comment_u + new_u)
    assert b"AGREEMENT FLOW-END FIX1 CONDITIONS (2026-11-18" in patched
    write_resilient(BUILDER, patched)
    _rc = subprocess.run([sys.executable, "-m", "py_compile", BUILDER], capture_output=True)
    assert _rc.returncode == 0, "patched builder does not compile: %s" % _rc.stderr.decode("utf-8", "replace")[-500:]
    print("builder patched: unfold -> %s (%d B)" % (new_unfold_sha[:8], len(patched)))
    return patched

def run_builder(new_unfold, unfold_sha):
    workers = []
    for n in range(2):
        r = subprocess.run([sys.executable, BUILDER, "--stdout", "--welcome-stdin"],
                           input=read_bytes(WELCOME_LOCAL), capture_output=True, timeout=300)
        assert r.returncode == 0, "builder failed: %s" % r.stderr.decode("utf-8", "replace")[-800:]
        log = r.stderr.decode("utf-8", "replace")
        for needle in (WELCOME_SHA[:8], unfold_sha[:8], "4b5f9264", "61002d15", "a1550164"):
            assert needle in log, "builder log missing %s; log tail: %s" % (needle, log[-600:])
        workers.append(r.stdout)
        print("builder run %d: worker %d B sha=%s" % (n + 1, len(r.stdout), sha(r.stdout)))
    assert workers[0] == workers[1], "worker build not deterministic"
    w = workers[0]
    for marker in (b"fpNHold", b"FP_DISTILLED_SCRIPT", b"fp-smart-visual", b"Welcome home.", b"data-smart-block",
                   b"fpNHoldFill", b"fpSpeechVoice", b"svg[hidden]", b"playTip", b"Voice not available"):
        assert marker in w, "worker missing fix1/conditions marker %s" % marker
    dec = json.JSONDecoder()
    embeds = {}
    for name in ("WALK", "IDENTITY", "WELCOME", "UNFOLD", "PERSONAL_TEMPLATE"):
        i = w.find(("const %s = " % name).encode())
        assert i >= 0, "worker missing %s" % name
        j = w.find(b'"', i)
        val, _ = dec.raw_decode(w[j:].decode("utf-8"))
        embeds[name] = val.encode("utf-8")
    print("worker embeds: " + ", ".join("%s %d B %s" % (k, len(v), sha(v)[:8]) for k, v in embeds.items()))
    assert sha(embeds["WELCOME"]) == WELCOME_SHA, "worker welcome changed!"
    assert sha(embeds["UNFOLD"]) == unfold_sha, "worker does not embed the new unfold"
    assert sha(embeds["WALK"]) == WALK_SHA, "worker walk changed"
    assert sha(embeds["IDENTITY"]) == IDENT_SHA, "worker identity changed"
    assert sha(embeds["PERSONAL_TEMPLATE"])[:8] == "61002d15", "worker template changed"
    return w

def node_check(data, label):
    tmp = os.path.join(WORK, "worker-check-cond-%s.js" % label)
    write_resilient(tmp, data)
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    assert r.returncode == 0, "node --check failed for %s: %s" % (label, r.stderr[:500])
    print("node --check OK: %s (%d B)" % (label, len(data)))
    os.remove(tmp)

def commit_message(worker_sha, worker_bytes, unfold_sha):
    return (
        "Agreement FLOW-END FIX1 CONDITIONS (2026-11-18, conditions seat; "
        "CONDITIONS-REPORT.md in agreement-flow-end-fix1-20261118/)\n\n"
        "Closes the checker's two conditions on 43c8ba1e, nothing else. "
        "(1) The /agreement visual-phase slot rule "
        "(.letter-beat.fp-smart-visual .lb-showcase img) goes "
        "object-fit:cover -> contain, so the 4:3 letter images (1448x1086) "
        "show whole on /agreement too - the two circular-photo cover rules "
        "stay. (2) The unfold player's 2.5s no-start watchdog now writes "
        "'Voice not available on this device - read below' into the "
        "player's tip element (#playTip, reusing the existing unused "
        ".play-note style) instead of returning to idle silently; watchdog "
        "mechanics unchanged (warm-up, pick, assignment, clear on "
        "start/end/error). The divider (.ib-foot-logo / deck-logo.jpg) is "
        "untouched - the eye's call. #playStop is a circle, not a square. "
        "F2 stays UNVERIFIED (no handler exists). Welcome bytes unchanged.\n\n"
        "Worker built twice, identical sha %s (%d B); embeds verified: "
        "WALK 4b5f9264, IDENTITY a1550164, WELCOME d367efe1, UNFOLD %s, "
        "TEMPLATE 61002d15.\n\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after "
        "the PUT. Worker PUT with --meta v23-meta.json. NO PR, NO MERGE - "
        "the checker and the captain come after this seat. Nothing live - "
        "the finished update goes LIVE on the main URL only on Shawn's tap, "
        "after his eye."
        % (worker_sha[:8], worker_bytes, unfold_sha[:8], STAGING))

def main():
    new_unfold = read_bytes(os.path.join(WORK, "unfold-cond.html"))
    unfold_sha = sha(new_unfold)
    print("input: unfold %d B %s" % (len(new_unfold), unfold_sha[:8]))
    # welcome on disk must still be the fix1 welcome (this round moves nothing there)
    assert sha(read_bytes(WELCOME_LOCAL)) == WELCOME_SHA, "welcome on disk moved?!"
    _, ref = gh("GET", "/repos/%s/git/refs/heads/%s" % (REPO, BRANCH))
    print("branch tip:", ref["object"]["sha"])
    assert ref["object"]["sha"] == PARENT_TIP, "branch tip moved: %s" % ref["object"]["sha"]
    _, commit = gh("GET", "/repos/%s/git/commits/%s" % (REPO, PARENT_TIP))
    assert commit["tree"]["sha"] == BASE_TREE, "parent tree moved: %s" % commit["tree"]["sha"]
    print("parent tree:", BASE_TREE)
    builder = patch_builder(unfold_sha)
    write_resilient(UNFOLD_LOCAL, new_unfold)
    worker = run_builder(new_unfold, unfold_sha)
    node_check(worker, "worker")
    write_resilient(WORKER_LOCAL, worker)
    worker_file = os.path.join(WORK, "worker-cond.js")
    write_resilient(worker_file, worker)
    driver = read_bytes(os.path.join(WORK, "edit-cond.py"))
    stage_script = read_bytes(os.path.join(WORK, "stage-cond.py"))
    files = [
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
        ("team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html", new_unfold),
        ("team-nitro/agreement-flow-end-fix1-20261118/work/edit-cond.py", driver),
        ("team-nitro/agreement-flow-end-fix1-20261118/work/stage-cond.py", stage_script),
    ]
    blobs = {}
    for path, data in files:
        _, blob = gh("POST", "/repos/%s/git/blobs" % REPO,
                     {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"})
        blobs[path] = blob["sha"]
        print("blob %s: %s (%d B)" % (path.split("/")[-1], blob["sha"], len(data)))
    _, tree = gh("POST", "/repos/%s/git/trees" % REPO,
                 {"base_tree": BASE_TREE,
                  "tree": [{"path": p, "mode": "100644", "type": "blob", "sha": s} for p, s in blobs.items()]})
    print("new tree:", tree["sha"])
    msg = commit_message(sha(worker), len(worker), unfold_sha)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _, cm = gh("POST", "/repos/%s/git/commits" % REPO,
               {"message": msg, "tree": tree["sha"], "parents": [PARENT_TIP],
                "author": {"name": "nayapower-lane-agent[bot]",
                           "email": "338161897+nayapower-lane-agent[bot]@users.noreply.github.com",
                           "date": now},
                "committer": {"name": "GitHub", "email": "noreply@github.com", "date": now}})
    commit_sha = cm["sha"]
    print("commit sha:", commit_sha)
    _, ref3 = gh("PATCH", "/repos/%s/git/refs/heads/%s" % (REPO, BRANCH),
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
        "/": WELCOME_SHA,
        "/agreement": unfold_sha,
        "/welcome": WALK_SHA,
        "/identity.html": IDENT_SHA,
        "/?stage=bridge": WELCOME_SHA,
        "/?stage=deck": WELCOME_SHA,
        "/?stage=letter": WELCOME_SHA,
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
        "unfold_bytes": len(new_unfold), "unfold_sha": unfold_sha,
        "worker_bytes": len(worker), "worker_sha": sha(worker),
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes}, indent=1))

if __name__ == "__main__":
    main()
