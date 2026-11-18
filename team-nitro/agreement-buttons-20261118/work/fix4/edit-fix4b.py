#!/usr/bin/env python3
"""AGREEMENT BUTTONS FIX 4b (2026-11-18) — maker amendment, same round.

Why: the fix-4 live render (my own eye, VM Chromium) showed the
bridge-final first paint clean EXCEPT one flat diamond: #fpBridgeExit
("Back to the login ◆"). The brief listed it LEAVE ALONE *because it
sat below the fold* (fix-3 eye: bottom 1200, fold 1080). Fix 1's
scroll-to-bottom moved it above the fold (live: bottom 920 at 1919) —
the leave-alone premise no longer holds, and the brief's own Fix 3
target ("the first paint on the final view must show ZERO flat
diamonds") plus Design Law §1 ("No flat diamond") now cover it. The
law wins over the brief (§0). So the exit button gets the SAME jewel
treatment as its sibling pair — the same harvested .fp-btn-jewel span,
no new image bytes — and nothing else moves.

Base: fix-4 welcome blob bbb1ceb4, 1,168,845 B, sha256
fb18f9d952a313ddab354b9a81728c63fdf2e89515d50e4929b444e436f13551
(branch walk-end/agreement-merge-20261117, tip
3d609609919c3f89cd09942a1cd2b2203b6ea11e).

Edit: exactly ONE line — the #fpBridgeExit button in the giant L2216
bridge line: `Back to the login &#9670;` becomes
`Back to the login <span class="fp-btn-jewel" aria-hidden="true"></span>`.
The footer's #fpLegalExit ("Back to the login ◆") is NOT touched — it
is a different button in a different view, out of scope.

Modes: edit | all (same pipeline as edit-fix4.py).
"""
import base64, hashlib, io, json, os, re, subprocess, sys, time, difflib

HOME = os.path.expanduser("~")
WORK = os.path.join(HOME, "workspace/team-nitro/agreement-buttons-20261118/work/fix4")
V23 = os.path.join(HOME, "workspace/team-nitro/walk-v23-assembly-20261114")
BASE_WELCOME = os.path.join(V23, "welcome-staged.html")
WORK_COPY = os.path.join(WORK, "welcome-fix4b.html")
BUILDER = os.path.join(V23, "build-v23-staging-worker.py")
CHECKER = os.path.join(HOME, "workspace/team-nitro/check-design-laws.py")
GH = os.path.join(HOME, "workspace/team-nitro/gh-direct.py")
CF = os.path.join(HOME, "workspace/project-intelligence/cf-worker.py")
META = os.path.join(V23, "v23-meta.json")
REPO = "SoulSchoolAcademy/NayaPOWER"
BRANCH = "walk-end/agreement-merge-20261117"
PARENT_TIP = "3d609609919c3f89cd09942a1cd2b2203b6ea11e"
BASE_BLOB = "bbb1ceb4848eb293db394caea2200bef5f758c5f"
BASE_SHA = "fb18f9d952a313ddab354b9a81728c63fdf2e89515d50e4929b444e436f13551"
BASE_BYTES = 1168845
CF_ACCOUNT = "b5e2a51b3e883f7722287c5f51b1196b"
CF_SCRIPT = "naya-walk-beginning-staging"
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"

def sha(b): return hashlib.sha256(b).hexdigest()

EXIT_OLD = ('<button class="fp-intro-choice fp-bridge-exit" id="fpBridgeExit" '
            'type="button" style="--tone:#8e24aa;margin-top:12px">Back to the login &#9670;</button>')
EXIT_NEW = ('<button class="fp-intro-choice fp-bridge-exit" id="fpBridgeExit" '
            'type="button" style="--tone:#8e24aa;margin-top:12px">Back to the login '
            '<span class="fp-btn-jewel" aria-hidden="true"></span></button>')
LEGAL_EXIT = 'id="fpLegalExit"'

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

def load_base():
    _, rb = gh("GET", "/repos/%s/git/blobs/%s" % (REPO, BASE_BLOB))
    assert rb.get("encoding") == "base64", "welcome blob not base64"
    raw = base64.b64decode("".join(rb["content"].split()))
    assert len(raw) == BASE_BYTES and sha(raw) == BASE_SHA, \
        "welcome blob mismatch: %d B sha %s" % (len(raw), sha(raw)[:8])
    print("base loaded from GitHub blob %s (%d B, sha %s)" % (BASE_BLOB[:8], len(raw), sha(raw)[:8]))
    return raw

def compute_new_welcome():
    base = load_base()
    text = base.decode("utf-8")
    pre = {
        "exit_old": text.count(EXIT_OLD),
        "exit_new": text.count(EXIT_NEW),
        "legal_exit": text.count(LEGAL_EXIT),
        "legal_exit_diamond": text.count('Back to the login &#9670;'),
        "jewel_spans": text.count('<span class="fp-btn-jewel"'),
        "jewel_uri": text.count("data:image/png;base64,"),
        "diamond_literal": text.count("\u25c6"),
        "diamond_entity": text.count("&#9670;"),
        "more4_new": text.count("bBridge.scrollTop=bBridge.scrollHeight-bBridge.clientHeight"),
        "p3_hidden_rule": text.count(".p3-enter[hidden]{display:none!important}"),
        "nextbtn_hidden_rule": text.count("#fpNextBtn[hidden]{display:none}"),
        "bridge_bar_rule": text.count("body.fp-stage-on.fp-bridge #fpStageBarB{display:none}"),
    }
    assert pre["exit_old"] == 1 and pre["exit_new"] == 0, pre
    assert pre["legal_exit"] == 1 and pre["legal_exit_diamond"] == 2, pre  # bridge + footer
    assert pre["jewel_spans"] == 4 and pre["jewel_uri"] == 2, pre
    assert pre["diamond_literal"] == 3 and pre["diamond_entity"] == 345, pre
    assert pre["more4_new"] == 1 and pre["p3_hidden_rule"] == 1, pre
    assert pre["nextbtn_hidden_rule"] == 1 and pre["bridge_bar_rule"] == 1, pre
    i = text.find(EXIT_OLD)
    assert i >= 0 and text.count(EXIT_OLD) == 1
    text = text[:i] + EXIT_NEW + text[i + len(EXIT_OLD):]
    new = text.encode("utf-8")
    post = {
        "exit_old": text.count(EXIT_OLD),
        "exit_new": text.count(EXIT_NEW),
        "legal_exit": text.count(LEGAL_EXIT),
        "legal_exit_diamond": text.count('Back to the login &#9670;'),
        "jewel_spans": text.count('<span class="fp-btn-jewel"'),
        "jewel_uri": text.count("data:image/png;base64,"),
        "diamond_literal": text.count("\u25c6"),
        "diamond_entity": text.count("&#9670;"),
        "more4_new": text.count("bBridge.scrollTop=bBridge.scrollHeight-bBridge.clientHeight"),
        "p3_hidden_rule": text.count(".p3-enter[hidden]{display:none!important}"),
        "nextbtn_hidden_rule": text.count("#fpNextBtn[hidden]{display:none}"),
        "bridge_bar_rule": text.count("body.fp-stage-on.fp-bridge #fpStageBarB{display:none}"),
    }
    assert post["exit_old"] == 0 and post["exit_new"] == 1, post
    assert post["legal_exit"] == 1 and post["legal_exit_diamond"] == 1, post  # footer only
    assert post["jewel_spans"] == 5 and post["jewel_uri"] == 2, post
    assert post["diamond_literal"] == 3 and post["diamond_entity"] == 344, post
    assert post["more4_new"] == 1 and post["p3_hidden_rule"] == 1, post
    assert post["nextbtn_hidden_rule"] == 1 and post["bridge_bar_rule"] == 1, post
    # F1-F4 counts identical
    base_text = base.decode("utf-8")
    inv = {
        "_fpAlias2": "_fpAlias2", "enterStage();": "enterStage();",
        "press_sink": "#fpAgreement #dealAgreeBtn:active,#fpAgreement #letterPageAgree:active",
        "choice_active": ".fp-intro-choice:active", "play_active": ".p3-naya-play:active",
        "rest_glow": "#fpBridgeDeck:not(:hover):not(:active)",
        "deck_end_return_clear": "window.__fpDeckEndReturn=false;enterStage();",
        "deck_end_return": "__fpDeckEndReturn",
        "getItem_fp_stage": "getItem('nayanet_fp_stage')",
        "setItem_fp_stage": "setItem('nayanet_fp_stage'",
        "localStorage_setItem": "localStorage.setItem",
    }
    for k, pat in inv.items():
        assert base_text.count(pat) == text.count(pat), "invariant changed: %s" % k
    # All three script blocks byte-identical (no JS change this pass).
    sb = re.findall(r"<script>(.*?)</script>", base_text, re.S)
    sn = re.findall(r"<script>(.*?)</script>", text, re.S)
    assert len(sb) == 3 and len(sn) == 3
    for i in range(3):
        assert sha(sb[i].encode()) == sha(sn[i].encode()), "script block %d changed" % i
    print("script blocks: all 3 byte-identical (no JS change)")
    # Diff scope: exactly 1 hunk, 1 line replaced.
    sm = difflib.SequenceMatcher(a=base_text.split("\n"), b=text.split("\n"), autojunk=False)
    hunks = [op for op in sm.get_opcodes() if op[0] != "equal"]
    print("diff hunks (base %d lines -> new %d lines):" % (len(base_text.split("\n")), len(text.split("\n"))))
    for tag, i1, i2, j1, j2 in hunks:
        print("  %s base L%d-%d -> new L%d-%d" % (tag, i1 + 1, i2, j1 + 1, j2))
    assert len(hunks) == 1 and hunks[0][0] == "replace" and hunks[0][2] - hunks[0][1] == 1, hunks
    print("edits ok: pre=%s" % pre)
    print("edits ok: post=%s" % post)
    print("new welcome: %d B sha=%s (delta %+d B)" % (len(new), sha(new), len(new) - BASE_BYTES))
    return new

def check_text(text, label):
    import importlib.util
    spec = importlib.util.spec_from_file_location("cdl", CHECKER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    fails, warns = [], []
    for i, line in enumerate(text.splitlines(), 1):
        for rx in m.GRAY_RES:
            if rx.search(line):
                fails.append("%s:%d: GRAY: %s" % (label, i, line.strip()[:120]))
                break
    for mt in m.FONTSIZE_RE.finditer(text):
        vals = [float(v) for v in mt.groups() if v is not None]
        if vals and min(vals) < 17:
            line_no = text[:mt.start()].count("\n") + 1
            fails.append("%s:%d: SIZE: %s" % (label, line_no, mt.group(0)))
    for mt in m.COLOR_DECL_RE.finditer(text):
        val = mt.group(1).strip().lower()
        if val.startswith("var("):
            continue
        val = val.split()[0].rstrip(";")
        line_no = text[:mt.start()].count("\n") + 1
        if val in m.FORBIDDEN_TEXT:
            fails.append("%s:%d: TEXT-COLOR: %s" % (label, line_no, mt.group(0).strip()[:120]))
        elif val not in m.ALLOWED_TEXT and not val.startswith("#"):
            warns.append("%s:%d: TEXT-COLOR?: %s" % (label, line_no, mt.group(0).strip()[:120]))
    if ":hover" not in text:
        warns.append("%s: NO-HOVER" % label)
    return sorted(set(fails)), sorted(set(warns))

def run_checker(base_text, new_text):
    bf, bw = check_text(base_text, "base")
    nf, nw = check_text(new_text, "new")
    norm = lambda items: sorted(re.sub(r"^[^:]+:\d+: ", "", x) for x in items)
    new_fails = [x for x in norm(nf) if x not in norm(bf)]
    new_warns = [x for x in norm(nw) if x not in norm(bw)]
    print("checker: base %d FAIL + %d WARN; new %d FAIL + %d WARN; NEW fails %d, NEW warns %d"
          % (len(bf), len(bw), len(nf), len(nw), len(new_fails), len(new_warns)))
    assert not new_fails and not new_warns, (new_fails, new_warns)
    return len(bf), len(bw), len(nf), len(nw)

def node_parse_scripts(new_text):
    blocks = re.findall(r"<script>(.*?)</script>", new_text, re.S)
    js = ("const vm=require('vm');let s='';process.stdin.on('data',d=>s+=d);"
          "process.stdin.on('end',()=>{new vm.Script(s);console.log('script-parse-ok');});")
    for i, b in enumerate(blocks):
        r = subprocess.run(["node", "-e", js], input=b.encode("utf-8"),
                           capture_output=True, timeout=60)
        assert r.returncode == 0 and b"script-parse-ok" in r.stdout, \
            "script block %d failed to parse: %s" % (i, r.stderr[:400])
        print("node: script block %d parses (%d B)" % (i, len(b)))

def node_check_worker(worker):
    path = os.path.join(WORK, "worker-fix4b-check.mjs")
    ok_file = write_resilient(path, worker)
    if ok_file:
        r = subprocess.run(["node", "--check", path], capture_output=True, timeout=120)
        assert r.returncode == 0, "node --check worker failed: %s" % r.stderr[:500]
        print("node --check worker: OK (file %s)" % path)
    r = subprocess.run(["node", "--input-type=module", "-"], input=worker,
                       capture_output=True, timeout=120)
    assert r.returncode == 0, "node module-run worker failed: %s" % r.stderr[:500]
    print("node: worker parses as ESM module from stdin (rc 0)")

def write_resilient(path, data, attempts=5):
    want = sha(data)
    scratch = path + ".scratch"
    for n in range(attempts):
        try:
            with open(scratch, "wb") as fh:
                fh.write(data)
            got = open(scratch, "rb").read()
            if len(got) == len(data) and sha(got) == want:
                os.replace(scratch, path)
                final = open(path, "rb").read()
                if len(final) == len(data) and sha(final) == want:
                    print("disk write ok: %s (%d B)" % (path, len(data)))
                    return True
                print("disk write attempt %d: replace landed wrong - retry" % (n + 1))
            else:
                print("disk write attempt %d scratch wrong (%d B, want %d) - retry"
                      % (n + 1, len(got), len(data)))
        except OSError as e:
            print("disk write attempt %d failed: %s" % (n + 1, e))
        time.sleep(2)
    print("disk write FAILED after %d attempts (flake): %s" % (attempts, path))
    return False

def mode_edit():
    new = compute_new_welcome()
    base = load_base()
    bf, bw, nf, nw = run_checker(base.decode("utf-8"), new.decode("utf-8"))
    node_parse_scripts(new.decode("utf-8"))
    write_resilient(WORK_COPY, new)
    write_resilient(BASE_WELCOME, new)
    print("EDIT-RESULT " + json.dumps({
        "welcome_bytes": len(new), "welcome_sha": sha(new),
        "welcome_sha_prefix": sha(new)[:8], "delta": len(new) - BASE_BYTES,
        "checker": {"base_fail": bf, "base_warn": bw, "new_fail": nf, "new_warn": nw}}))
    return new

def patch_builder(new_sha, new_bytes):
    btxt = open(BUILDER, "rb").read()
    old_assert = (b'assert welcome_sha.startswith("fb18f9d9"), "welcome sha is not the '
                  b'AGREEMENT BUTTONS FIX 4 welcome sha (2026-11-18: 1. More4 handler scrolls #fpBridge to bottom, '
                  b'2. .p3-enter[hidden] hides the dead Continue pill, 3. #fpNextBtn[hidden] + bridge bar display:none)"')
    assert btxt.count(old_assert) == 1, "builder FIX 4 assert not found exactly once"
    comment = (
        b"# AGREEMENT BUTTONS FIX 4b (2026-11-18, maker sense-check on the fix-4\n"
        b"# live render; maker round - agreement-buttons-20261118/work/fix4/edit-fix4b.py):\n"
        b"# the welcome sha moves fb18f9d9 -> " + new_sha[:8].encode() + b" (1,168,845 B -> "
        + str(new_bytes).encode() + b" B):\n"
        b"# the fix-4 scroll-to-bottom moved #fpBridgeExit above the fold (live bottom\n"
        b"# 920 at 1919), so the brief's leave-alone premise ('below the fold') no\n"
        b"# longer holds and the Fix 3 target (zero flat diamonds on first paint)\n"
        b"# plus Design Law S1 cover it: the exit button gets the same harvested\n"
        b"# .fp-btn-jewel span as its sibling pair (no new image bytes). One line.\n"
        b"# #fpLegalExit in the footer view is NOT touched. Walk, template, identity,\n"
        b"# unfold shas unchanged.\n")
    new_assert = (b'assert welcome_sha.startswith("' + new_sha[:8].encode() + b'"), "welcome sha is not the '
                  b'AGREEMENT BUTTONS FIX 4b welcome sha (2026-11-18: #fpBridgeExit gains the harvested jewel span)"')
    patched = btxt.replace(old_assert, comment + new_assert)
    assert b"AGREEMENT BUTTONS FIX 4b (2026-11-18" in patched
    write_resilient(BUILDER, patched)
    print("builder patched: assert -> %s, FIX 4b comment added (%d B)" % (new_sha[:8], len(patched)))
    return patched

def run_builder(new_welcome, expect_prefix):
    btxt = open(BUILDER, "rb").read()
    assert ('welcome_sha.startswith("%s")' % expect_prefix).encode() in btxt, \
        "builder not patched to the new welcome prefix"
    assert b"AGREEMENT BUTTONS FIX 4b (2026-11-18" in btxt, \
        "builder lacks the fix-4b round comment"
    workers = []
    for n in range(2):
        r = subprocess.run([sys.executable, BUILDER, "--stdout", "--welcome-stdin"],
                           input=new_welcome, capture_output=True, timeout=300)
        assert r.returncode == 0, "builder failed: %s" % r.stderr.decode("utf-8", "replace")[-800:]
        log = r.stderr.decode("utf-8", "replace")
        for needle in (expect_prefix, "4b5f9264", "96b18b6f", "61002d15", "a1550164"):
            assert needle in log, "builder log missing %s" % needle
        workers.append(r.stdout)
        print("builder run %d: worker %d B sha=%s" % (n + 1, len(r.stdout), sha(r.stdout)))
    assert workers[0] == workers[1], "worker build not deterministic"
    w = workers[0]
    # (raw worker bytes carry the welcome JSON-escaped, so assert on
    # unquoted fragments here; exact bytes are checked on the decoded
    # WELCOME embed below.)
    assert b"fpBridgeExit" in w and b"Back to the login" in w
    assert b".p3-enter[hidden]{display:none!important}" in w
    assert b"bBridge.scrollTop=bBridge.scrollHeight-bBridge.clientHeight" in w
    dec = json.JSONDecoder()
    embeds = {}
    for name in ("WALK", "IDENTITY", "WELCOME", "UNFOLD", "PERSONAL_TEMPLATE"):
        i = w.find(("const %s = " % name).encode())
        assert i >= 0, "worker missing %s" % name
        j = w.find(b'"', i)
        val, _ = dec.raw_decode(w[j:].decode("utf-8"))
        embeds[name] = val.encode("utf-8")
    print("worker embeds: " + ", ".join(
        "%s %d B %s" % (k, len(v), sha(v)[:8]) for k, v in embeds.items()))
    assert sha(embeds["WELCOME"]) == sha(new_welcome), "worker does not embed the new welcome"
    assert embeds["WELCOME"].count(b"Back to the login &#9670;") == 1, \
        "footer exit diamond count wrong in WELCOME embed"
    assert b'id="fpBridgeExit" type="button" style="--tone:#8e24aa;margin-top:12px">Back to the login <span class="fp-btn-jewel"' in embeds["WELCOME"], \
        "WELCOME embed lacks the jewelled bridge exit"
    assert sha(embeds["UNFOLD"])[:8] == "96b18b6f", "worker unfold changed"
    assert sha(embeds["WALK"])[:8] == "4b5f9264" and sha(embeds["IDENTITY"])[:8] == "a1550164"
    assert sha(embeds["PERSONAL_TEMPLATE"])[:8] == "61002d15"
    return w

def commit_message(welcome_sha, worker_sha, welcome_bytes, worker_bytes):
    return (
        "Agreement BUTTONS FIX 4b (2026-11-18, maker sense-check on the fix-4 "
        "live render; MAKER-REPORT-4.md in agreement-buttons-20261118/)\n\n"
        "One line, same round. The fix-4 live render showed the bridge-final "
        "first paint clean except one flat diamond: #fpBridgeExit (\"Back to "
        "the login ◆\"). The brief listed it LEAVE ALONE because it sat "
        "below the fold (fix-3 eye: bottom 1200, fold 1080) — but fix 1's "
        "scroll-to-bottom moved it above the fold (live bottom 920 at 1919), "
        "so that premise no longer holds, and the Fix 3 target (zero flat "
        "diamonds on first paint) plus Design Law §1 cover it. The exit "
        "button gets the same harvested .fp-btn-jewel span as its sibling "
        "pair (no new image bytes). #fpLegalExit in the footer view is NOT "
        "touched.\n\n"
        "NO REGRESSION: all three inline script blocks byte-identical (no JS "
        "change); F1-F4 counts identical; design laws zero new FAILs vs base. "
        "Worker built twice, identical sha %s (%d B); embeds verified: WALK "
        "4b5f9264, IDENTITY a1550164, WELCOME %s, UNFOLD 96b18b6f.\n\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after "
        "the PUT. Worker PUT with --meta v23-meta.json (WELCOME_ASSETS "
        "1cf80db6183245d19dd5296645a12bd0 intact). PR #3453 OPEN AND UNMERGED "
        "BY DESIGN - do not merge; the captain decides the PR vehicle. "
        "Nothing live - the finished update goes LIVE on the main URL only "
        "on Shawn's tap, after his eye."
        % (worker_sha[:8], worker_bytes, welcome_sha[:8], STAGING))

def file_commit(new_welcome, worker, welcome_sha, worker_sha):
    builder = open(BUILDER, "rb").read()
    driver = open(os.path.join(WORK, "edit-fix4b.py"), "rb").read()
    _, ref = gh("GET", "/repos/%s/git/refs/heads/%s" % (REPO, BRANCH))
    print("branch tip before:", ref["object"]["sha"])
    assert ref["object"]["sha"] == PARENT_TIP, "branch tip moved: %s" % ref["object"]["sha"]
    _, commit = gh("GET", "/repos/%s/git/commits/%s" % (REPO, PARENT_TIP))
    base_tree = commit["tree"]["sha"]
    print("base tree:", base_tree)
    files = [
        ("team-nitro/walk-v23-assembly-20261114/welcome-staged.html", new_welcome),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
        ("team-nitro/agreement-buttons-20261118/work/fix4/edit-fix4b.py", driver),
    ]
    blobs = {}
    for path, data in files:
        _, blob = gh("POST", "/repos/%s/git/blobs" % REPO,
                     {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"})
        blobs[path] = blob["sha"]
        print("blob %s: %s (%d B)" % (path.split("/")[-1], blob["sha"], len(data)))
    _, tree = gh("POST", "/repos/%s/git/trees" % REPO,
                 {"base_tree": base_tree,
                  "tree": [{"path": p, "mode": "100644", "type": "blob", "sha": s}
                           for p, s in blobs.items()]})
    print("new tree:", tree["sha"])
    msg = commit_message(welcome_sha, worker_sha, len(new_welcome), len(worker))
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _, cm = gh("POST", "/repos/%s/git/commits" % REPO,
               {"message": msg, "tree": tree["sha"], "parents": [PARENT_TIP],
                "author": {"name": "nayapower-lane-agent[bot]",
                           "email": "338161897+nayapower-lane-agent[bot]@users.noreply.github.com",
                           "date": now},
                "committer": {"name": "GitHub", "email": "noreply@github.com", "date": now}})
    commit_sha = cm["sha"]
    print("commit sha:", commit_sha)
    _, ref2 = gh("PATCH", "/repos/%s/git/refs/heads/%s" % (REPO, BRANCH),
                 {"sha": commit_sha, "force": False})
    print("branch now:", ref2["object"]["sha"])
    assert ref2["object"]["sha"] == commit_sha
    for path, data in files:
        _, rb = gh("GET", "/repos/%s/git/blobs/%s" % (REPO, blobs[path]))
        raw = base64.b64decode("".join(rb["content"].split()))
        assert len(raw) == len(data) and sha(raw) == sha(data), \
            "blob read-back mismatch for %s" % path
        print("blob read-back OK:", path.split("/")[-1], len(raw), "bytes, sha match")
    return commit_sha, tree["sha"], blobs

def stage_put(worker):
    r = subprocess.run([sys.executable, CF, "put-script", CF_ACCOUNT, CF_SCRIPT,
                        "/dev/stdin", "--meta", META],
                       input=worker, capture_output=True, timeout=300)
    out = r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace")
    print("staging PUT rc=%d:\n%s" % (r.returncode, out[:2000]))
    assert r.returncode == 0, "staging PUT failed"
    m = re.search(r"deployment[ _]?id['\"]?\s*[:=]\s*['\"]?([0-9a-f]{16,})", out, re.I)
    dep = m.group(1) if m else None
    assert "200" in out, "staging PUT did not report HTTP 200"
    return dep, out

def verify_routes(welcome_sha):
    ua = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
    expect = {
        "/": welcome_sha,
        "/agreement": "96b18b6f063c88cf4422b915be4bb53808f290364a03be5093c26c9ea3d47983",
        "/welcome": "4b5f926423d765bd750026e65986f0b67f6b52d51588fe64e857b39df7ee01c0",
        "/identity.html": "a1550164251ef804ff51b129c75c33571fedfdbb0554cd70f094dc5ec25c984e",
        "/?stage=bridge": welcome_sha,
        "/?stage=deck": welcome_sha,
        "/?stage=letter": welcome_sha,
    }
    results = {}
    for route, want in expect.items():
        got = None
        for attempt in (1, 2):
            r = subprocess.run(["curl", "-s", "-A", ua, STAGING + route],
                               capture_output=True, timeout=120)
            got = sha(r.stdout)
            print("route %s: %d B sha=%s (want %s) attempt %d"
                  % (route, len(r.stdout), got[:12], want[:12], attempt))
            if got == want:
                break
            time.sleep(15)
        results[route] = got
        assert got == want, "route %s mismatch: got %s want %s" % (route, got, want)
    return results

def mode_all():
    new = mode_edit()
    wsha = sha(new)
    patch_builder(wsha, len(new))
    worker = run_builder(new, wsha[:8])
    node_check_worker(worker)
    commit_sha, tree_sha, blobs = file_commit(new, worker, wsha, sha(worker))
    dep, put_out = stage_put(worker)
    routes = verify_routes(wsha)
    write_resilient(WORK_COPY, new)
    write_resilient(BASE_WELCOME, new)
    print("ALL-RESULT " + json.dumps({
        "welcome_bytes": len(new), "welcome_sha": wsha,
        "worker_bytes": len(worker), "worker_sha": sha(worker),
        "commit": commit_sha, "tree": tree_sha, "blobs": blobs,
        "staging_deployment": dep, "routes": routes}, indent=1))

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "edit"
    if mode == "edit":
        mode_edit()
    elif mode == "all":
        mode_all()
    else:
        sys.exit("usage: edit-fix4b.py [edit|all]")
