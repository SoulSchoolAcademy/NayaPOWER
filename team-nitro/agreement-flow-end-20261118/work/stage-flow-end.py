#!/usr/bin/env python3
"""FLOW-END stage + file (2026-11-18) — agreement flow-end round.

Takes the edited files from edit-flow-end.py (work/welcome-flow-end.html,
work/unfold-flow-end.html) and, per the brief:
  1. patches the builder's welcome + unfold sha asserts to the new shas,
  2. installs the new bytes on the builder's local input paths,
  3. rebuilds the staging worker twice (deterministic sha) and verifies
     every embed by sha256,
  4. creates branch walk-end/agreement-flow-end-20261118 from 8f822c76,
  5. files ONE commit (welcome + worker + builder + unfold + both drivers),
  6. PUTs the worker to the walk staging worker,
  7. verifies all 7 routes by sha256 via curl.
No PR, no merge, no message to Shawn. Report to the coordinator only.
"""
import base64, hashlib, json, os, re, subprocess, sys, time

HOME = os.path.expanduser("~")
RECORDS = os.path.join(HOME, "workspace/team-nitro/agreement-flow-end-20261118")
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
BASE_BRANCH = "walk-end/agreement-merge-20261117"
NEW_BRANCH = "walk-end/agreement-flow-end-20261118"
PARENT_TIP = "8f822c768938b7a58d705a4a3908fa4dc78d5a63"
CF_ACCOUNT = "b5e2a51b3e883f7722287c5f51b1196b"
CF_SCRIPT = "naya-walk-beginning-staging"
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
WELCOME_SHA = "018d488a1a1fb771b8996b655ae0f36bf7435d8337dfd87becd4c61760c16cc1"
UNFOLD_SHA = "fb0ab19b4cafe6bc7e92f47980ea551d3cf131dff4bfb135151297db8c7cfe37"
WALK_SHA = "4b5f926423d765bd750026e65986f0b67f6b52d51588fe64e857b39df7ee01c0"
IDENT_SHA = "a1550164251ef804ff51b129c75c33571fedfdbb0554cd70f094dc5ec25c984e"

def sha(b): return hashlib.sha256(b).hexdigest()

def read_bytes(p):
    with open(p, "rb") as f: return f.read()

def write_resilient(path, data, attempts=40):
    tmp = path + ".tmp-stage"
    last = None
    for n in range(attempts):
        try:
            with open(tmp, "wb") as f:
                for i in range(0, len(data), 8192):
                    f.write(data[i:i+8192])
                f.flush(); os.fsync(f.fileno())
            got = read_bytes(tmp)
            if len(got) != len(data) or sha(got) != sha(data):
                raise IOError("tmp verify failed")
            os.replace(tmp, path)
            got2 = read_bytes(path)
            if len(got2) != len(data) or sha(got2) != sha(data):
                raise IOError("post-replace verify failed")
            print("wrote %s %d B sha %s" % (path, len(data), sha(data)[:12]))
            return
        except Exception as e:
            last = e
            print("write attempt %d failed: %s" % (n + 1, e))
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

def patch_builder():
    btxt = read_bytes(BUILDER)
    old_w = (b'assert welcome_sha.startswith("e4fe0d52"), "welcome sha is not the '
             b'AGREEMENT INTRO ALIGN welcome sha (2026-11-18: intro row one tight centred unit)"')
    assert btxt.count(old_w) == 1, "builder welcome assert not found exactly once"
    old_u = (b'assert unfold_sha.startswith("96b18b6f"), "unfold sha is not the '
             b'AGREEMENT INTRO LAYOUT FOLLOW-ON #2 unfold sha (2026-11-18: picture centred, '
             b'opening header + voice line removed, dots + read-all moved below the letter, 88,848 B)"')
    assert btxt.count(old_u) == 1, "builder unfold assert not found exactly once"
    comment_w = (
        b"# AGREEMENT FLOW-END (2026-11-18, maker round -\n"
        b"# agreement-flow-end-20261118/work/edit-flow-end.py): the welcome sha\n"
        b"# moves e4fe0d52 -> 018d488a (1,171,088 B -> 1,847,528 B): the N ball\n"
        b"# HOLDS (full-screen N hold, 3s, both end paths); the flow ends at\n"
        b"# the name-entry login; portrait -> NAYA_POWER.jpg verbatim (data\n"
        b"# URI); play reads the distilled script (stop/pause/play, Web\n"
        b"# Speech); every board is one Smart Block locked to one viewport\n"
        b"# (Smart Show: full screen, one visual per block, 16:9, click to\n"
        b"# unfold, always go back); 390 tip overflow + legal-row clip fixed;\n"
        b"# the intro N seal fills the 1919 void. Intro row + fix-4 untouched.\n")
    new_w = (b'assert welcome_sha.startswith("018d488a"), "welcome sha is not the '
             b'AGREEMENT FLOW-END welcome sha (2026-11-18: N hold, Smart Block, portrait, play)"')
    comment_u = (
        b"# AGREEMENT FLOW-END (2026-11-18, same round): the unfold sha moves\n"
        b"# 96b18b6f -> fb0ab19b (88,848 B -> 92,519 B): the /agreement page is\n"
        b"# the Smart Show too - full-screen container (the 980px column goes),\n"
        b"# full-width showcase, every beat one viewport-tall Smart Block\n"
        b"# (talk, then its visual alone at 16:9), click to unfold, always go\n"
        b"# back. Welcome, walk, template, identity shas unchanged.\n")
    new_u = (b'assert unfold_sha.startswith("fb0ab19b"), "unfold sha is not the '
             b'AGREEMENT FLOW-END unfold sha (2026-11-18: Smart Show, full screen, one visual per block)"')
    patched = btxt.replace(old_w, comment_w + new_w).replace(old_u, comment_u + new_u)
    assert b"AGREEMENT FLOW-END (2026-11-18" in patched
    write_resilient(BUILDER, patched)
    print("builder patched: welcome -> 018d488a, unfold -> fb0ab19b (%d B)" % len(patched))
    return patched

def run_builder(new_welcome):
    btxt = read_bytes(BUILDER)
    assert b'welcome_sha.startswith("018d488a")' in btxt, "builder not patched (welcome)"
    assert b'unfold_sha.startswith("fb0ab19b")' in btxt, "builder not patched (unfold)"
    workers = []
    for n in range(2):
        r = subprocess.run([sys.executable, BUILDER, "--stdout", "--welcome-stdin"],
                           input=new_welcome, capture_output=True, timeout=300)
        assert r.returncode == 0, "builder failed: %s" % r.stderr.decode("utf-8", "replace")[-800:]
        log = r.stderr.decode("utf-8", "replace")
        for needle in ("018d488a", "fb0ab19b", "4b5f9264", "61002d15", "a1550164"):
            assert needle in log, "builder log missing %s; log tail: %s" % (needle, log[-600:])
        workers.append(r.stdout)
        print("builder run %d: worker %d B sha=%s" % (n + 1, len(r.stdout), sha(r.stdout)))
    assert workers[0] == workers[1], "worker build not deterministic"
    w = workers[0]
    for marker in (b"fpNHold", b"FP_DISTILLED_SCRIPT", b"fp-smart-visual", b"Welcome home.", b"data-smart-block"):
        assert marker in w, "worker missing flow-end marker %s" % marker
    dec = json.JSONDecoder()
    embeds = {}
    for name in ("WALK", "IDENTITY", "WELCOME", "UNFOLD", "PERSONAL_TEMPLATE"):
        i = w.find(("const %s = " % name).encode())
        assert i >= 0, "worker missing %s" % name
        j = w.find(b'"', i)
        val, _ = dec.raw_decode(w[j:].decode("utf-8"))
        embeds[name] = val.encode("utf-8")
    print("worker embeds: " + ", ".join("%s %d B %s" % (k, len(v), sha(v)[:8]) for k, v in embeds.items()))
    assert sha(embeds["WELCOME"]) == WELCOME_SHA, "worker does not embed the new welcome"
    assert sha(embeds["UNFOLD"]) == UNFOLD_SHA, "worker does not embed the new unfold"
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

def commit_message(worker_sha, worker_bytes):
    return (
        "Agreement FLOW-END (2026-11-18, maker round; MAKER-REPORT.md in "
        "agreement-flow-end-20261118/)\n\n"
        "The N ball HOLDS: the beautiful N orb showed ~0.5s (the deal-stamp "
        ".55s) and now holds a full-screen Smart Block for 3000ms on BOTH "
        "end paths — deck-end Enter and I agree — tap to continue, then the "
        "name-entry login (the Sovereign Entrance, harvested, never "
        "invented), then the Hub. The flow no longer dumps back to the "
        "bridge. Portrait is NAYA_POWER.jpg verbatim (data-URI, sha "
        "6ee884aa). Play reads the distilled script (1,482 words, ~10 "
        "min) with stop / pause / play (Web Speech API — no harvested "
        "speech path existed). Every board is one Smart Block locked to "
        "exactly one viewport (Smart Show: full screen, one visual per "
        "block, oversize boards split, 16:9, click to unfold, always go "
        "back); the /agreement page carries the same law. Secondaries: "
        "390 hover-tip overflow fixed (tip anchors to the play button's "
        "right edge, wraps at 200px); 635/390 legal rows wrap and centre; "
        "the 1919 void holds a quiet breathing N seal. Intro row "
        "(0.0/0.0/24-24) and fix-4 untouched; F2 agree press traced by "
        "bytes, live click owed to the eye.\n\n"
        "NO REGRESSION: design laws zero new FAILs vs base (83 FAIL + 4 "
        "WARN both sides — pre-existing); all script blocks node-parsed; "
        "worker built twice, identical sha %s (%d B); embeds verified: "
        "WALK 4b5f9264, IDENTITY a1550164, WELCOME 018d488a, UNFOLD "
        "fb0ab19b, TEMPLATE 61002d15.\n\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after "
        "the PUT. Worker PUT with --meta v23-meta.json (WELCOME_ASSETS "
        "1cf80db6183245d19dd5296645a12bd0 intact). NO PR, NO MERGE — the "
        "checker and the captain come after this seat. Nothing live - the "
        "finished update goes LIVE on the main URL only on Shawn's tap, "
        "after his eye."
        % (worker_sha[:8], worker_bytes, STAGING))

def main():
    new_welcome = read_bytes(os.path.join(WORK, "welcome-flow-end.html"))
    new_unfold = read_bytes(os.path.join(WORK, "unfold-flow-end.html"))
    assert sha(new_welcome) == WELCOME_SHA, "welcome output sha mismatch: %s" % sha(new_welcome)
    assert sha(new_unfold) == UNFOLD_SHA, "unfold output sha mismatch: %s" % sha(new_unfold)
    print("inputs OK: welcome %d B %s, unfold %d B %s" % (len(new_welcome), WELCOME_SHA[:8], len(new_unfold), UNFOLD_SHA[:8]))
    _, ref = gh("GET", "/repos/%s/git/refs/heads/%s" % (REPO, BASE_BRANCH))
    print("base branch tip:", ref["object"]["sha"])
    assert ref["object"]["sha"] == PARENT_TIP, "base branch tip moved: %s" % ref["object"]["sha"]
    builder = patch_builder()
    write_resilient(WELCOME_LOCAL, new_welcome)
    write_resilient(UNFOLD_LOCAL, new_unfold)
    worker = run_builder(new_welcome)
    node_check(worker, "worker")
    write_resilient(WORKER_LOCAL, worker)
    worker_file = os.path.join(WORK, "worker-flow-end.js")
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
    driver = read_bytes(os.path.join(WORK, "edit-flow-end.py"))
    stage_script = read_bytes(os.path.join(WORK, "stage-flow-end.py"))
    files = [
        ("team-nitro/walk-v23-assembly-20261114/welcome-staged.html", new_welcome),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
        ("team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html", new_unfold),
        ("team-nitro/agreement-flow-end-20261118/work/edit-flow-end.py", driver),
        ("team-nitro/agreement-flow-end-20261118/work/stage-flow-end.py", stage_script),
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
    msg = commit_message(sha(worker), len(worker))
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
        "welcome_bytes": len(new_welcome), "welcome_sha": WELCOME_SHA,
        "unfold_bytes": len(new_unfold), "unfold_sha": UNFOLD_SHA,
        "worker_bytes": len(worker), "worker_sha": sha(worker),
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes}, indent=1))

if __name__ == "__main__":
    main()
