#!/usr/bin/env python3
"""FIX F1 (2026-11-18) — walkthrough chain round, checker verdict.

THE FAILURE (checker, §3.2 / §12.6): two same-color buttons together in
the post-agree bridge final view. welcome-staged.html line 2367: the final
column reads Deck purple / Letter emerald / ToName emerald / Back purple —
pills 2 and 3 directly adjacent, same color, shape, jewel and glow.

THE FIX (one line, as the maker itself named): re-tone #fpBridgeToName to
gold #d4a017. Final then reads purple / emerald / gold / purple. Change
ONLY that tone. Nothing else changes — no redesign, no other edits, no
scope expansion. The bridge ORDER is left alone (the checker's secondary
observation is for the EYE, not this seat).

THEN: re-file on the SAME branch walkthrough/chain-20261118 (new commit,
parent = chain tip 61c3d715), rebuild the staging worker with the round's
builder (only the welcome assert moves a1b67b82 -> new; the identity
assert d8c0d583 is NOT touched), PUT to staging, re-prove all 7 routes
+ proof-host links by sha256, re-run the law checker (must be identical
to the chain welcome). No PR, no merge, no live deploy, no message to
Shawn. Identity is NOT re-filed (unchanged).
"""
import base64, difflib, hashlib, json, os, re, subprocess, sys, time

HOME = os.path.expanduser("~")
RECORDS = os.path.join(HOME, "workspace/team-nitro/walkthrough-chain-20261118")
WORK = os.path.join(RECORDS, "work")
V23 = os.path.join(HOME, "workspace/team-nitro/walk-v23-assembly-20261114")
BUILDER = os.path.join(V23, "build-v23-staging-worker.py")
WELCOME_LOCAL = os.path.join(V23, "welcome-staged.html")
IDENT_LOCAL = os.path.join(V23, "identity-fixed.html")
WORKER_LOCAL = os.path.join(V23, "walk-beginning-staging-worker.js")
UNFOLD_LOCAL = os.path.join(HOME, "workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html")
META = os.path.join(V23, "v23-meta.json")
GH = os.path.join(HOME, "workspace/team-nitro/gh-direct.py")
CF = os.path.join(HOME, "workspace/project-intelligence/cf-worker.py")
CHECKER = os.path.join(HOME, "workspace/team-nitro/check-design-laws.py")
REPO = "SoulSchoolAcademy/NayaPOWER"
BRANCH = "walkthrough/chain-20261118"
CHAIN_TIP = "61c3d7152693fe96c6df0bdcb8a82151f882c041"
CHAIN_TREE = "b1fd5f3a2be0bde6a777f0ae134a815883d64b02"
CHAIN_WELCOME_BLOB = "e41512f176d643535425702d4703e5e188a1dfa0"
CHAIN_WELCOME_SHA = "a1b67b82f721edd58a5c0effeb25c5e4503391084acdaba6d8dd0a24eab9702b"
CHAIN_BUILDER_BLOB = "0acbaa490f9a2580ee9818c9c80003b7b9640644"
CHAIN_BUILDER_SHA = "ed8a133200262e716288ae5cd90f078c6aaf997fb78c146571a20a18a831023f"
CHAIN_IDENT_BLOB = "98b0efc0ca79bd91d5c31203eb1b264aa298985d"
CHAIN_IDENT_SHA = "d8c0d583e16f70194227b017db42980c2d4507283292475c5a8fde9c0fc46219"
CF_ACCOUNT = "b5e2a51b3e883f7722287c5f51b1196b"
CF_SCRIPT = "naya-walk-beginning-staging"
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
PROOF = "https://naya-proof-host.nayapower.workers.dev"
WALK_SHA = "4b5f926423d765bd750026e65986f0b67f6b52d51588fe64e857b39df7ee01c0"
UNFOLD_SHA = "984d87aff1a04fb159579c3ef9e8703ca7044a7b9667a1a0a9c0c18e50baa671"
IDENT_SHA = "d8c0d583e16f70194227b017db42980c2d4507283292475c5a8fde9c0fc46219"

OLD_BTN = b'id="fpBridgeToName" type="button" style="--tone:#07925f;margin-top:12px"'
NEW_BTN = b'id="fpBridgeToName" type="button" style="--tone:#d4a017;margin-top:12px"'

def sha(b): return hashlib.sha256(b).hexdigest()

def read_bytes(p):
    with open(p, "rb") as f: return f.read()

def write_resilient(path, data, attempts=40):
    tmp = path + ".tmp-fix-f1"
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

def gh_blob(blob_sha):
    _, rb = gh("GET", "/repos/%s/git/blobs/%s" % (REPO, blob_sha))
    assert rb.get("sha") == blob_sha, "blob sha mismatch: %s" % rb.get("sha")
    raw = base64.b64decode("".join(rb["content"].split()))
    return raw

def node_check(data, label):
    tmp = os.path.join(WORK, "nodecheck-fix-f1-%s.js" % label)
    write_resilient(tmp, data)
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    assert r.returncode == 0, "node --check failed for %s: %s" % (label, r.stderr[:500])
    print("node --check OK: %s (%d B)" % (label, len(data)))
    os.remove(tmp)

def node_check_html(html, label):
    blocks = re.findall(rb"<script(?:\s[^>]*)?>(.*?)</script>", html, re.DOTALL)
    blocks = [b for b in blocks if b.strip()]
    print("%s: %d inline script blocks" % (label, len(blocks)))
    for i, b in enumerate(blocks):
        node_check(b, "%s-%d" % (label, i))

def patch_builder(new_welcome_sha):
    btxt = read_bytes(BUILDER)
    assert sha(btxt) == CHAIN_BUILDER_SHA, "local builder is not the filed chain builder"
    ident_assert = b'assert ident_sha.startswith("d8c0d583")'
    assert btxt.count(ident_assert) == 1, "identity assert not found exactly once"
    ident_line_before = [l for l in btxt.split(b"\n") if ident_assert in l]
    assert len(ident_line_before) == 1
    assert btxt.count(b'startswith("a1b67b82")') == 1, "welcome assert not found exactly once"
    assert btxt.count(b'd367efe1 -> a1b67b82') == 1, "welcome comment move not found exactly once"
    new8 = new_welcome_sha[:8].encode()
    patched = btxt.replace(b'startswith("a1b67b82")', b'startswith("' + new8 + b'")')
    patched = patched.replace(b'd367efe1 -> a1b67b82', b'a1b67b82 -> ' + new8)
    old_msg = (b'"welcome sha is not the WALKTHROUGH-CHAIN welcome sha '
               b'(2026-11-18: bridge first after agreeing)"')
    new_msg = (b'"welcome sha is not the WALKTHROUGH-CHAIN welcome sha '
               b'(2026-11-18: bridge first after agreeing; FIX F1: fpBridgeToName '
               b'emerald -> gold, no adjacent repeat)"')
    assert patched.count(old_msg) == 1, "welcome assert message not found exactly once"
    patched = patched.replace(old_msg, new_msg)
    # identity assert line must be byte-identical before/after
    ident_line_after = [l for l in patched.split(b"\n") if ident_assert in l]
    assert ident_line_after == ident_line_before, "IDENTITY ASSERT MOVED - abort"
    assert patched.count(ident_assert) == 1
    d = list(difflib.unified_diff(btxt.decode().splitlines(), patched.decode().splitlines(), lineterm=""))
    changed = [l for l in d if (l.startswith("+") and not l.startswith("+++")) or (l.startswith("-") and not l.startswith("---"))]
    print("builder diff changed lines: %d" % len(changed))
    assert len(changed) == 2, "builder patch must touch exactly one line (+1/-1): %s" % changed
    write_resilient(BUILDER, patched)
    rc = subprocess.run([sys.executable, "-m", "py_compile", BUILDER], capture_output=True)
    assert rc.returncode == 0, "patched builder does not compile: %s" % rc.stderr.decode("utf-8", "replace")[-500:]
    print("builder patched: welcome -> %s, identity assert UNTOUCHED (%d B)" % (new_welcome_sha[:8], len(patched)))
    return patched

def run_builder(new_welcome, welcome_sha):
    workers = []
    for n in range(2):
        r = subprocess.run([sys.executable, BUILDER, "--stdout", "--welcome-stdin"],
                           input=new_welcome, capture_output=True, timeout=300)
        assert r.returncode == 0, "builder failed: %s" % r.stderr.decode("utf-8", "replace")[-800:]
        log = r.stderr.decode("utf-8", "replace")
        for needle in (welcome_sha[:8], UNFOLD_SHA[:8], "4b5f9264", "61002d15", IDENT_SHA[:8]):
            assert needle in log, "builder log missing %s; log tail: %s" % (needle, log[-600:])
        workers.append(r.stdout)
        print("builder run %d: worker %d B sha=%s" % (n + 1, len(r.stdout), sha(r.stdout)))
    assert workers[0] == workers[1], "worker build not deterministic"
    w = workers[0]
    for marker in (b"fpNHold", b"FP_DISTILLED_SCRIPT", b"fp-smart-visual", b"Welcome home.", b"data-smart-block",
                   b"fpNHoldFill", b"fpSpeechVoice", b"svg[hidden]",
                   b"goBridgeAfterAgree", b"fpBridgeToName", b"fpBridgeAgreed",
                   b"__chainShowKey", b"keyPanel", b"Use my key",
                   b'id=\\"fpBridgeToName\\" type=\\"button\\" style=\\"--tone:#d4a017;margin-top:12px\\"'):
        assert marker in w, "worker missing marker %s" % marker
    assert b'--tone:#07925f;margin-top:12px' not in w, "worker still embeds the old emerald ToName tone"
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
    assert sha(embeds["UNFOLD"]) == UNFOLD_SHA, "worker does not embed the new unfold"
    assert sha(embeds["WALK"]) == WALK_SHA, "worker walk changed"
    assert sha(embeds["IDENTITY"]) == IDENT_SHA, "worker identity changed"
    assert sha(embeds["PERSONAL_TEMPLATE"])[:8] == "61002d15", "worker template changed"
    return w

def curl_sha(url, ua):
    rr = subprocess.run(["curl", "-s", "-A", ua, url], capture_output=True, timeout=120)
    return rr.stdout, sha(rr.stdout)

def run_checker_norm(path):
    r = subprocess.run([sys.executable, CHECKER, path], capture_output=True, text=True, timeout=120)
    txt = r.stdout + r.stderr
    norm = sorted(l.split(":", 1)[1] if ":" in l else l for l in txt.splitlines() if l.strip())
    return r.returncode, norm, txt

def commit_message(worker_sha, worker_bytes, welcome_sha):
    return (
        "Walkthrough CHAIN FIX F1 (2026-11-18; CHECKER-VERDICT-CHAIN-20261118.md)\\n\\n"
        "Checker failure F1 (Design Laws §3.2 / §12.6): two same-color buttons "
        "together in the post-agree bridge final view — the final column read "
        "Deck purple / Read the agreement emerald / Continue emerald / Back "
        "purple, pills 2 and 3 directly adjacent, same color, shape, jewel "
        "and glow. THE FIX, one line, as the maker itself named: #fpBridgeToName "
        "re-toned emerald #07925f -> gold #d4a017 (welcome-staged.html line "
        "2367, the style attribute only). The final column now reads purple / "
        "emerald / gold / purple — no adjacent repeat. NOTHING else changes: "
        "no redesign, no other edits, no scope expansion. The bridge ORDER is "
        "left alone — the checker's secondary observation (onward pill sits "
        "third in the column) is for the EYE to judge. The identity assert "
        "(d8c0d583) and the identity file are untouched; the builder's welcome "
        "assert moves a1b67b82 -> %s and the worker is rebuilt with the new "
        "welcome embedded.\\n\\n"
        "Worker built twice, identical sha %s (%d B); embeds verified: "
        "WALK 4b5f9264, IDENTITY d8c0d583, WELCOME %s, UNFOLD 984d87af, "
        "TEMPLATE 61002d15.\\n\\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after "
        "the PUT. NO PR, NO MERGE — the checker and the captain come after "
        "this seat. Nothing live - the finished update goes LIVE on the main "
        "URL only on Shawn's tap, after his eye."
        % (welcome_sha[:8], worker_sha[:8], worker_bytes, welcome_sha[:8], STAGING))

def main():
    # 0. Branch tip + filed blobs (blob API: decode + size + sha)
    _, ref = gh("GET", "/repos/%s/git/refs/heads/%s" % (REPO, BRANCH))
    print("branch tip:", ref["object"]["sha"])
    assert ref["object"]["sha"] == CHAIN_TIP, "branch tip moved: %s" % ref["object"]["sha"]
    _, commit = gh("GET", "/repos/%s/git/commits/%s" % (REPO, CHAIN_TIP))
    assert commit["tree"]["sha"] == CHAIN_TREE, "chain tree moved"
    base_welcome = gh_blob(CHAIN_WELCOME_BLOB)
    assert len(base_welcome) == 1854672 and sha(base_welcome) == CHAIN_WELCOME_SHA, "welcome blob mismatch"
    print("welcome blob read-back OK: 1854672 B sha a1b67b82...")
    local_chain = read_bytes(os.path.join(WORK, "welcome-chain.html"))
    assert local_chain == base_welcome, "local chain welcome differs from filed blob"
    builder_base = gh_blob(CHAIN_BUILDER_BLOB)
    assert len(builder_base) == 90273 and sha(builder_base) == CHAIN_BUILDER_SHA, "builder blob mismatch"
    assert builder_base == read_bytes(BUILDER), "local builder differs from filed blob"
    print("builder blob read-back OK: 90273 B sha ed8a1332...")
    ident_blob = gh_blob(CHAIN_IDENT_BLOB)
    assert len(ident_blob) == 387458 and sha(ident_blob) == CHAIN_IDENT_SHA, "identity blob mismatch"
    print("identity blob read-back OK (unchanged, NOT re-filed): 387458 B sha d8c0d583...")
    # local builder inputs must be the chain bytes before the rebuild
    assert sha(read_bytes(os.path.join(V23, "walk-beginning-fixed.html"))) == WALK_SHA, "local walk moved"
    assert sha(read_bytes(UNFOLD_LOCAL)) == UNFOLD_SHA, "local unfold moved"
    assert sha(read_bytes(os.path.join(HOME, "workspace/team-nitro/space-business-mirror-personal-20261112/template-composed.html")))[:8] == "61002d15", "local template moved"
    assert sha(read_bytes(IDENT_LOCAL)) == IDENT_SHA, "local identity is not the chain identity"

    # 1. THE ONE-LINE FIX
    assert base_welcome.count(OLD_BTN) == 1, "ToName button not found exactly once"
    assert base_welcome.count(b'--tone:#07925f;margin-top:12px') == 1, "old tone string not unique"
    new_welcome = base_welcome.replace(OLD_BTN, NEW_BTN)
    welcome_sha = sha(new_welcome)
    print("new welcome: %d B sha %s" % (len(new_welcome), welcome_sha))
    assert len(new_welcome) == len(base_welcome), "size changed - the fix must be same-length"
    assert new_welcome.count(NEW_BTN) == 1
    assert new_welcome.count(b'--tone:#07925f;margin-top:12px') == 0, "old tone survives"
    assert base_welcome.count(b'#07925f') - new_welcome.count(b'#07925f') == 1, "emerald count delta != 1"
    assert new_welcome.count(b'#d4a017') - base_welcome.count(b'#d4a017') == 1, "gold count delta != 1"
    # Letter pill untouched, still emerald
    assert b'id="fpBridgeLetter" type="button" style="--tone:#07925f"' in new_welcome, "Letter pill moved"
    # diff must be exactly one line, line 2367
    sm = difflib.SequenceMatcher(None, base_welcome.decode().splitlines(), new_welcome.decode().splitlines())
    diff_lines = [(t, i1, i2, j1, j2) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != "equal"]
    print("welcome diff opcodes:", diff_lines)
    assert len(diff_lines) == 1 and diff_lines[0][0] == "replace" and diff_lines[0][1] == 2366 and diff_lines[0][2] == 2367 and diff_lines[0][3] == 2366 and diff_lines[0][4] == 2367, "diff is not exactly line 2367"
    # final column tones in order: purple / emerald / gold / purple
    line2367 = new_welcome.decode().splitlines()[2366]
    tones = re.findall(r'id="fpBridge(?:Deck|Letter|ToName|Exit)"[^>]*style="--tone:(#[0-9a-f]{6})', line2367)
    print("final column tones:", tones)
    assert tones == ["#8e24aa", "#07925f", "#d4a017", "#8e24aa"], "final column tones wrong: %s" % tones
    assert all(tones[i] != tones[i + 1] for i in range(3)), "adjacent repeat survives"
    node_check_html(new_welcome, "welcome-fix-f1")
    write_resilient(os.path.join(WORK, "welcome-fix-f1.html"), new_welcome)

    # 2. Builder patch (welcome assert only) + rebuild
    builder = patch_builder(welcome_sha)
    write_resilient(WELCOME_LOCAL, new_welcome)
    worker = run_builder(new_welcome, welcome_sha)
    node_check(worker, "worker-fix-f1")
    write_resilient(WORKER_LOCAL, worker)
    worker_file = os.path.join(WORK, "worker-fix-f1.js")
    write_resilient(worker_file, worker)

    # 3. File ONE new commit on the SAME branch (parent = chain tip)
    driver = read_bytes(os.path.join(WORK, "fix-f1.py"))
    files = [
        ("team-nitro/walk-v23-assembly-20261114/welcome-staged.html", new_welcome),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
        ("team-nitro/walkthrough-chain-20261118/work/fix-f1.py", driver),
    ]
    blobs = {}
    for path, data in files:
        _, blob = gh("POST", "/repos/%s/git/blobs" % REPO,
                     {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"})
        blobs[path] = blob["sha"]
        print("blob %s: %s (%d B)" % (path.split("/")[-1], blob["sha"], len(data)))
    _, tree = gh("POST", "/repos/%s/git/trees" % REPO,
                 {"base_tree": CHAIN_TREE,
                  "tree": [{"path": p, "mode": "100644", "type": "blob", "sha": s} for p, s in blobs.items()]})
    print("new tree:", tree["sha"])
    msg = commit_message(sha(worker), len(worker), welcome_sha)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _, cm = gh("POST", "/repos/%s/git/commits" % REPO,
               {"message": msg, "tree": tree["sha"], "parents": [CHAIN_TIP],
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
        raw = gh_blob(blobs[path])
        assert len(raw) == len(data) and sha(raw) == sha(data), "blob read-back mismatch for %s" % path
        print("blob read-back OK:", path.split("/")[-1], len(raw), "bytes, sha match")

    # 4. PUT the rebuilt worker to staging
    r = subprocess.run([sys.executable, CF, "put-script", CF_ACCOUNT, CF_SCRIPT,
                        worker_file, "--meta", META],
                       capture_output=True, timeout=300)
    out = r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace")
    print("staging PUT rc=%d:\n%s" % (r.returncode, out[:2000]))
    assert r.returncode == 0 and "200" in out, "staging PUT failed"

    # 5. Re-prove all 7 routes + proof-host links
    ua = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
    expect = {
        "/": welcome_sha,
        "/agreement": UNFOLD_SHA,
        "/welcome": WALK_SHA,
        "/identity.html": IDENT_SHA,
        "/?stage=bridge": welcome_sha,
        "/?stage=deck": welcome_sha,
        "/?stage=letter": welcome_sha,
    }
    routes = {}
    for route, want in expect.items():
        got = None
        for attempt in (1, 2, 3):
            _, got = curl_sha(STAGING + route, ua)
            print("route %s: sha=%s (want %s) attempt %d" % (route, got[:12], want[:12], attempt))
            if got == want:
                break
            time.sleep(15)
        routes[route] = got
        assert got == want, "route %s mismatch: got %s want %s" % (route, got, want)
    proof = {}
    url_w = "%s/?file=%s&ref=%s&cb=%s&t=%d" % (
        PROOF, "team-nitro/walk-v23-assembly-20261114/welcome-staged.html", BRANCH,
        blobs["team-nitro/walk-v23-assembly-20261114/welcome-staged.html"], int(time.time()))
    _, got = curl_sha(url_w, ua)
    print("proof welcome: sha=%s (want %s)" % (got[:12], welcome_sha[:12]))
    assert got == welcome_sha, "proof-host welcome mismatch"
    proof["welcome"] = url_w
    url_i = "%s/?file=%s&ref=%s&cb=%s&t=%d" % (
        PROOF, "team-nitro/walk-v23-assembly-20261114/identity-fixed.html", BRANCH,
        CHAIN_IDENT_BLOB, int(time.time()))
    _, got = curl_sha(url_i, ua)
    print("proof identity (unchanged): sha=%s (want %s)" % (got[:12], IDENT_SHA[:12]))
    assert got == IDENT_SHA, "proof-host identity mismatch"
    proof["identity"] = url_i

    # 6. Law checker: new welcome vs chain welcome — must be identical
    rc_new, norm_new, _ = run_checker_norm(os.path.join(WORK, "welcome-fix-f1.html"))
    rc_base, norm_base, _ = run_checker_norm(os.path.join(WORK, "welcome-chain.html"))
    print("law checker: new exit=%s findings=%d; base exit=%s findings=%d" % (rc_new, len(norm_new), rc_base, len(norm_base)))
    law_diff_new = [l for l in norm_new if l not in norm_base]
    law_diff_base = [l for l in norm_base if l not in norm_new]
    print("law diff new-minus-base=%d base-minus-new=%d" % (len(law_diff_new), len(law_diff_base)))
    assert law_diff_new == [] and law_diff_base == [], "law checker diff: %s / %s" % (law_diff_new, law_diff_base)

    result = {
        "welcome_bytes": len(new_welcome), "welcome_sha": welcome_sha,
        "welcome_blob": blobs["team-nitro/walk-v23-assembly-20261114/welcome-staged.html"],
        "identity_bytes": 387458, "identity_sha": IDENT_SHA, "identity_blob": CHAIN_IDENT_BLOB,
        "unfold_sha": UNFOLD_SHA, "walk_sha": WALK_SHA,
        "worker_bytes": len(worker), "worker_sha": sha(worker),
        "worker_blob": blobs["team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js"],
        "builder_bytes": len(builder), "builder_sha": sha(builder),
        "builder_blob": blobs["team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py"],
        "driver_blob": blobs["team-nitro/walkthrough-chain-20261118/work/fix-f1.py"],
        "commit": commit_sha, "tree": tree["sha"], "parent": CHAIN_TIP,
        "branch": BRANCH, "blobs": blobs,
        "final_column_tones": tones,
        "routes": routes, "proof": proof,
        "law_checker": {"new_findings": len(norm_new), "base_findings": len(norm_base),
                        "diff_new_minus_base": law_diff_new, "diff_base_minus_new": law_diff_base},
    }
    with open(os.path.join(WORK, "fix-f1-results.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("FIX-F1-RESULT " + json.dumps(result, indent=1))

if __name__ == "__main__":
    main()
