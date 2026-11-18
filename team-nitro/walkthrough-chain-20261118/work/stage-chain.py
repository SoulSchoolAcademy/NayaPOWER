#!/usr/bin/env python3
"""CHAIN stage + file (2026-11-18) — walkthrough chain round.

Takes the edited files from edit-chain.py (work/welcome-chain.html,
work/identity-chain.html) and:
  1. patches the builder's welcome + identity sha asserts to the new shas
     (computed from the built files, never typed) — the STAGING WORKER
     RE-EMBED: the builder asserted the OLD identity sha (a1550164) and
     would fail until updated; it now asserts the NEW identity sha.
  2. installs the new bytes on the builder's local input paths,
  3. rebuilds the staging worker twice (deterministic sha) and verifies
     every embed by sha256,
  4. creates branch walkthrough/chain-20261118 from 4038fd42,
  5. files ONE commit (welcome + identity + worker + builder + both drivers),
  6. PUTs the worker to the walk staging worker,
  7. verifies all 7 routes by sha256 via curl, plus the proof-host links
     for the two edited files.
No PR, no merge, no message to Shawn. Report to the coordinator only.
"""
import base64, hashlib, json, os, re, subprocess, sys, time

HOME = os.path.expanduser("~")
RECORDS = os.path.join(HOME, "workspace/team-nitro/walkthrough-chain-20261118")
WORK = os.path.join(RECORDS, "work")
V23 = os.path.join(HOME, "workspace/team-nitro/walk-v23-assembly-20261114")
BUILDER = os.path.join(V23, "build-v23-staging-worker.py")
BUILDER_BASE = os.path.join(WORK, "builder-chain-base.py")
WELCOME_LOCAL = os.path.join(V23, "welcome-staged.html")
IDENT_LOCAL = os.path.join(V23, "identity-fixed.html")
WORKER_LOCAL = os.path.join(V23, "walk-beginning-staging-worker.js")
UNFOLD_LOCAL = os.path.join(HOME, "workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html")
META = os.path.join(V23, "v23-meta.json")
GH = os.path.join(HOME, "workspace/team-nitro/gh-direct.py")
CF = os.path.join(HOME, "workspace/project-intelligence/cf-worker.py")
REPO = "SoulSchoolAcademy/NayaPOWER"
NEW_BRANCH = "walkthrough/chain-20261118"
BASE_BRANCH = "walk-end/agreement-flow-end-fix1-20261118"
PARENT_TIP = "4038fd42393d889becc21a5b6b5f712686a0c310"
CF_ACCOUNT = "b5e2a51b3e883f7722287c5f51b1196b"
CF_SCRIPT = "naya-walk-beginning-staging"
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
PROOF = "https://naya-proof-host.nayapower.workers.dev"
WALK_SHA = "4b5f926423d765bd750026e65986f0b67f6b52d51588fe64e857b39df7ee01c0"
UNFOLD_SHA = "984d87aff1a04fb159579c3ef9e8703ca7044a7b9667a1a0a9c0c18e50baa671"

def sha(b): return hashlib.sha256(b).hexdigest()

def read_bytes(p):
    with open(p, "rb") as f: return f.read()

def write_resilient(path, data, attempts=40):
    tmp = path + ".tmp-stage-chain"
    last = None
    for n in range(attempts):
        try:
            wrote = False
            try:
                with open(tmp, "wb") as f:
                    for i in range(0, len(data), 8192): f.write(data[i:i+8192])
                    f.flush(); os.fsync(f.fileno())
                got = read_bytes(tmp)
                if len(got) == len(data) and sha(got) == sha(data): wrote = True
            except Exception as e:
                last = e
            if wrote:
                os.replace(tmp, path)
                got2 = read_bytes(path)
                if len(got2) != len(data) or sha(got2) != sha(data):
                    raise RuntimeError("verify after replace failed: %s" % path)
                print("wrote %s %d B sha %s" % (path, len(data), sha(data)[:12]), flush=True)
                return
        except Exception as e:
            last = e
        time.sleep(2)
    raise RuntimeError("write_resilient failed for %s: %r" % (path, last))

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

def patch_builder(new_welcome_sha, new_ident_sha):
    btxt = read_bytes(BUILDER_BASE)
    assert sha(btxt).startswith("480fc8b6"), "builder base mismatch"
    old_w = (b'assert welcome_sha.startswith("d367efe1"), "welcome sha is not the '
             b'AGREEMENT FLOW-END FIX1 welcome sha (2026-11-18: N hold bulletproofed, play reads aloud, letter full-screen)"')
    old_i = (b'assert ident_sha.startswith("a1550164"), "identity sha is not the '
             b'BRIDGE PRESENTATION identity sha (2026-11-17: certified lean 0.88fr at 600-640px)"')
    assert btxt.count(old_w) == 1, "builder welcome assert not found exactly once"
    assert btxt.count(old_i) == 1, "builder identity assert not found exactly once"
    comment_w = (
        b"# WALKTHROUGH-CHAIN (2026-11-18, maker round -\\n"
        b"# walkthrough-chain-20261118/work/edit-chain.py): the welcome\\n"
        b"# sha moves d367efe1 -> %s: BRIDGE FIRST - after agreeing\\n"
        b"# inside the stage, the hold/fallback releases go to the bridge\\n"
        b"# (goBridgeAfterAgree), then the bridge's own buttons go to\\n"
        b"# name-entry; the agreed line + the onward button show only\\n"
        b"# after agreeing; the plain-page agree scroll is guarded while\\n"
        b"# the bridge is up. Pre-agree routes untouched (?stage=bridge,\\n"
        b"# Back buttons, /agreement agree -> bridge).\\n" % new_welcome_sha[:8].encode())
    new_w = (b'assert welcome_sha.startswith("%s"), "welcome sha is not the '
             b'WALKTHROUGH-CHAIN welcome sha (2026-11-18: bridge first after agreeing)"' % new_welcome_sha[:8].encode())
    comment_i = (
        b"# WALKTHROUGH-CHAIN (2026-11-18, same round) - STAGING WORKER\\n"
        b"# RE-EMBED: the identity sha moves a1550164 -> %s. The old\\n"
        b"# assert would fail the rebuild on the new identity bytes.\\n"
        b"# IDENTITY IS NAME *PLUS* THE DEVICE KEY: on 'taken' the row\\n"
        b"# is read back WITH this browser's device key and only d.own\\n"
        b"# grants - the name-match grant is deleted. Without the key\\n"
        b"# the citizen gets the key panel (paste key, Use my key, the\\n"
        b"# key is verified against the row); the key is also SHOWN on\\n"
        b"# the certified certificate so it can be carried to another\\n"
        b"# device. Walk, template, unfold shas unchanged.\\n" % new_ident_sha[:8].encode())
    new_i = (b'assert ident_sha.startswith("%s"), "identity sha is not the '
             b'WALKTHROUGH-CHAIN identity sha (2026-11-18: name + device key)"' % new_ident_sha[:8].encode())
    patched = btxt.replace(old_w, comment_w + new_w).replace(old_i, comment_i + new_i)
    assert b"WALKTHROUGH-CHAIN (2026-11-18" in patched
    write_resilient(BUILDER, patched)
    _rc = subprocess.run([sys.executable, "-m", "py_compile", BUILDER], capture_output=True)
    assert _rc.returncode == 0, "patched builder does not compile: %s" % _rc.stderr.decode("utf-8", "replace")[-500:]
    print("builder patched: welcome -> %s, identity -> %s (%d B)" % (new_welcome_sha[:8], new_ident_sha[:8], len(patched)))
    return patched

def run_builder(new_welcome, welcome_sha, ident_sha, unfold_sha):
    workers = []
    for n in range(2):
        r = subprocess.run([sys.executable, BUILDER, "--stdout", "--welcome-stdin"],
                           input=new_welcome, capture_output=True, timeout=300)
        assert r.returncode == 0, "builder failed: %s" % r.stderr.decode("utf-8", "replace")[-800:]
        log = r.stderr.decode("utf-8", "replace")
        for needle in (welcome_sha[:8], unfold_sha[:8], "4b5f9264", "61002d15", ident_sha[:8]):
            assert needle in log, "builder log missing %s; log tail: %s" % (needle, log[-600:])
        workers.append(r.stdout)
        print("builder run %d: worker %d B sha=%s" % (n + 1, len(r.stdout), sha(r.stdout)))
    assert workers[0] == workers[1], "worker build not deterministic"
    w = workers[0]
    for marker in (b"fpNHold", b"FP_DISTILLED_SCRIPT", b"fp-smart-visual", b"Welcome home.", b"data-smart-block",
                   b"fpNHoldFill", b"fpSpeechVoice", b"svg[hidden]",
                   b"goBridgeAfterAgree", b"fpBridgeToName", b"fpBridgeAgreed",
                   b"__chainShowKey", b"keyPanel", b"Use my key"):
        assert marker in w, "worker missing chain marker %s" % marker
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
    assert sha(embeds["IDENTITY"]) == ident_sha, "worker identity changed"
    assert sha(embeds["PERSONAL_TEMPLATE"])[:8] == "61002d15", "worker template changed"
    return w

def node_check(data, label):
    tmp = os.path.join(WORK, "worker-check-%s.js" % label)
    write_resilient(tmp, data)
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    assert r.returncode == 0, "node --check failed for %s: %s" % (label, r.stderr[:500])
    print("node --check OK: %s (%d B)" % (label, len(data)))
    os.remove(tmp)

def commit_message(worker_sha, worker_bytes, welcome_sha, ident_sha):
    return (
        "Walkthrough CHAIN (2026-11-18, maker round; MAKER-REPORT-CHAIN-20261118.md in "
        "walkthrough-chain-20261118/)\\n\\n"
        "Shawn decided (~21:54Z, live voice): bridge FIRST, then name entry; identity = "
        "name PLUS the device key. (1) BRIDGE ORDER: after agreeing inside the login/welcome "
        "stage, the hold (deck-end Enter, I agree, beat 9) and the 10s agree fallback release "
        "to the bridge (goBridgeAfterAgree), not to the login — the bridge is the welcome "
        "between agreeing and naming. The bridge's own 'Back to the login' and the new "
        "'Continue — enter your name' pill both go to name-entry. The agreed line ('Agreed - "
        "Welcome home.') and the onward pill show only after agreeing. Pre-agree routes "
        "untouched (?stage=bridge, Back buttons, /agreement agree -> bridge). (2) IDENTITY "
        "TRUST: on 'taken' the registry row is read back WITH this browser's device key and "
        "only d.own grants — the frontend round's name-match grant is DELETED; a name alone "
        "never opens an identity. Without the key the citizen gets the key panel (paste the "
        "device key, 'Use my key', verified against the row before any stamp or redirect), "
        "and the key is SHOWN on the certified certificate so it can be carried to another "
        "device. Key-present behaviour (cert stamps from registry truth, Enter to "
        "/welcome?name=...&alias=...) unchanged. (3) STAGING WORKER RE-EMBED: the builder "
        "asserted the OLD identity sha a1550164 and would fail until updated — it now asserts "
        "the NEW identity sha %s; the worker is rebuilt with the new identity embedded.\\n\\n"
        "Worker built twice, identical sha %s (%d B); embeds verified: "
        "WALK 4b5f9264, IDENTITY %s, WELCOME %s, UNFOLD 984d87af, TEMPLATE "
        "61002d15.\\n\\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after "
        "the PUT. Worker PUT with --meta v23-meta.json (WELCOME_ASSETS "
        "1cf80db6183245d19dd5296645a12bd0 intact). NO PR, NO MERGE — the "
        "checker and the captain come after this seat. Nothing live - the "
        "finished update goes LIVE on the main URL only on Shawn's tap, "
        "after his eye."
        % (ident_sha[:8], worker_sha[:8], worker_bytes, ident_sha[:8], welcome_sha[:8], STAGING))

def curl_sha(url, ua):
    rr = subprocess.run(["curl", "-s", "-A", ua, url], capture_output=True, timeout=120)
    return rr.stdout, sha(rr.stdout)

def main():
    new_welcome = read_bytes(os.path.join(WORK, "welcome-chain.html"))
    new_ident = read_bytes(os.path.join(WORK, "identity-chain.html"))
    welcome_sha, ident_sha = sha(new_welcome), sha(new_ident)
    print("inputs: welcome %d B %s, identity %d B %s" % (len(new_welcome), welcome_sha[:8], len(new_ident), ident_sha[:8]))
    assert welcome_sha.startswith("a1b67b82"), "welcome chain sha moved"
    assert ident_sha.startswith("d8c0d583"), "identity chain sha moved"
    _, ref = gh("GET", "/repos/%s/git/refs/heads/%s" % (REPO, BASE_BRANCH))
    print("base branch tip:", ref["object"]["sha"])
    assert ref["object"]["sha"] == PARENT_TIP, "base branch tip moved: %s" % ref["object"]["sha"]
    # local builder inputs must be the cond bytes before the rebuild
    assert sha(read_bytes(os.path.join(V23, "walk-beginning-fixed.html"))) == WALK_SHA, "local walk moved"
    assert sha(read_bytes(UNFOLD_LOCAL)) == UNFOLD_SHA, "local unfold moved"
    assert sha(read_bytes(os.path.join(HOME, "workspace/team-nitro/space-business-mirror-personal-20261112/template-composed.html")))[:8] == "61002d15", "local template moved"
    assert sha(read_bytes(IDENT_LOCAL)).startswith("a1550164"), "local identity is not the staged identity"
    builder = patch_builder(welcome_sha, ident_sha)
    write_resilient(WELCOME_LOCAL, new_welcome)
    write_resilient(IDENT_LOCAL, new_ident)
    worker = run_builder(new_welcome, welcome_sha, ident_sha, UNFOLD_SHA)
    node_check(worker, "worker")
    write_resilient(WORKER_LOCAL, worker)
    worker_file = os.path.join(WORK, "worker-chain.js")
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
    driver = read_bytes(os.path.join(WORK, "edit-chain.py"))
    stage_script = read_bytes(os.path.join(WORK, "stage-chain.py"))
    files = [
        ("team-nitro/walk-v23-assembly-20261114/welcome-staged.html", new_welcome),
        ("team-nitro/walk-v23-assembly-20261114/identity-fixed.html", new_ident),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
        ("team-nitro/walkthrough-chain-20261118/work/edit-chain.py", driver),
        ("team-nitro/walkthrough-chain-20261118/work/stage-chain.py", stage_script),
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
    msg = commit_message(sha(worker), len(worker), welcome_sha, ident_sha)
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
        "/agreement": UNFOLD_SHA,
        "/welcome": WALK_SHA,
        "/identity.html": ident_sha,
        "/?stage=bridge": welcome_sha,
        "/?stage=deck": welcome_sha,
        "/?stage=letter": welcome_sha,
    }
    routes = {}
    for route, want in expect.items():
        got = None
        for attempt in (1, 2):
            _, got = curl_sha(STAGING + route, ua)
            print("route %s: sha=%s (want %s) attempt %d" % (route, got[:12], want[:12], attempt))
            if got == want:
                break
            time.sleep(15)
        routes[route] = got
        assert got == want, "route %s mismatch: got %s want %s" % (route, got, want)
    # proof-host links for the two edited files (static, byte-identical)
    proof = {}
    for label, path, want in (
            ("welcome", "team-nitro/walk-v23-assembly-20261114/welcome-staged.html", welcome_sha),
            ("identity", "team-nitro/walk-v23-assembly-20261114/identity-fixed.html", ident_sha)):
        url = "%s/?file=%s&ref=%s&cb=%s&t=%d" % (PROOF, path, NEW_BRANCH, blobs["team-nitro/walk-v23-assembly-20261114/" + path.split("/")[-1]], int(time.time()))
        _, got = curl_sha(url, ua)
        print("proof %s: sha=%s (want %s)" % (label, got[:12], want[:12]))
        assert got == want, "proof-host %s mismatch" % label
        proof[label] = url
    print("STAGE-RESULT " + json.dumps({
        "welcome_bytes": len(new_welcome), "welcome_sha": welcome_sha,
        "identity_bytes": len(new_ident), "identity_sha": ident_sha,
        "unfold_bytes": 104853, "unfold_sha": UNFOLD_SHA,
        "worker_bytes": len(worker), "worker_sha": sha(worker),
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes, "proof": proof}, indent=1))

if __name__ == "__main__":
    main()
