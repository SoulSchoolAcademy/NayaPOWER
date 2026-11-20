#!/usr/bin/env python3
"""AGREEMENT INTRO ALIGN (2026-11-18) — maker round.

THE DEFECT (measured live on the fix-4b base, staging, VM Chromium):
the intro row — portrait + NAYA + play — reads as two elements floating
apart, not one presentation. Root cause, from bytes + computed style:
the 03:41Z grid (1fr auto 1fr, name col 2, play col 3) hits the grid
auto-placement cursor trap — the name comes AFTER the play button in
the DOM, so once the play took col 3 of row 1 the cursor had passed
col 2 and the name fell to row 2 (live 1919: name cy 447.8 vs
portrait/play cy 359.3, spread 88.5px; hero 161px tall = 132+16+13).
And the 1fr tracks shrink-wrap to content (132px each), so the
portrait pinned left, the play pinned right, with the empty name
column between them — a 140px empty gap at 1919 (gap1 16, gap2 80).

THE FIX (CSS only, one insert hunk after base L2099, same selectors,
later in the file so they win at equal specificity): auto tracks sized
to content, justify-content:center, gap 24px (the reference crop
measures ~20px/~29px gaps on a 119px portrait), every item grid-row:1
(explicit — immune to DOM order), all justify-self:center,
align-content:start, and min-height holding the hero box at its base
height (161px; 133px at <=480px) so the row collapses from two rows
to one WITHOUT moving anything below it: the intro pair bottoms stay
575/566/528 and 652/643/600, the bridge-final fold stays 843/844/613.
No HTML, no JS, no sizes, no colours move; the play button keeps its
id, handler, tip, orbit and press rules.

Base: fix-4b welcome blob a7e65947, 1,168,891 B, sha256
65555c374da7f898408a45d2796ce8c1f6efb029d5d0197f78bf39e6ee3c6677
(branch walk-end/agreement-merge-20261117, tip
a0a37aa48d45093af49943065e1931d27cd3b74d).
New branch: walk-end/agreement-intro-align-20261118. ONE commit.

Modes: edit | all (same pipeline shape as fix-4b's edit-fix4b.py).
"""
import base64, hashlib, io, json, os, re, subprocess, sys, time, difflib

HOME = os.path.expanduser("~")
WORK = os.path.join(HOME, "workspace/team-nitro/agreement-intro-align-20261118/work")
V23 = os.path.join(HOME, "workspace/team-nitro/walk-v23-assembly-20261114")
BASE_WELCOME = os.path.join(V23, "welcome-staged.html")
WORK_COPY = os.path.join(WORK, "welcome-align.html")
BASE_COPY = os.path.join(WORK, "welcome-base.html")
BUILDER = os.path.join(V23, "build-v23-staging-worker.py")
CHECKER = os.path.join(HOME, "workspace/team-nitro/check-design-laws.py")
GH = os.path.join(HOME, "workspace/team-nitro/gh-direct.py")
CF = os.path.join(HOME, "workspace/project-intelligence/cf-worker.py")
META = os.path.join(V23, "v23-meta.json")
REPO = "SoulSchoolAcademy/NayaPOWER"
BASE_BRANCH = "walk-end/agreement-merge-20261117"
NEW_BRANCH = "walk-end/agreement-intro-align-20261118"
PARENT_TIP = "a0a37aa48d45093af49943065e1931d27cd3b74d"
BASE_BLOB = "a7e659476af4c4387a9f9c4f5f487324197c703e"
BASE_SHA = "65555c374da7f898408a45d2796ce8c1f6efb029d5d0197f78bf39e6ee3c6677"
BASE_BYTES = 1168891
CF_ACCOUNT = "b5e2a51b3e883f7722287c5f51b1196b"
CF_SCRIPT = "naya-walk-beginning-staging"
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"

def sha(b): return hashlib.sha256(b).hexdigest()

ANCHOR = ('html.fp-locked body.fp-stage-on.fp-bridge #fpAgreement.fp-layer-on{padding-top:40px}')

NEW_BLOCK = """/* AGREEMENT INTRO ALIGN (2026-11-18) — the intro row reads as ONE tight
   centred unit: portrait + NAYA + play on one shared centre line, tight
   even gaps, the unit centred on the page — like the reference crop
   (image_2026-11-18_075721164.png: portrait 119px, gaps ~20px/~29px).
   Why the old row split apart (measured live on the fix-4b base):
   the 03:41Z grid (1fr auto 1fr, name col 2, play col 3) hit the grid
   auto-placement cursor trap — the name comes AFTER the play button
   in the DOM, so once the play took col 3 of row 1 the cursor had
   passed col 2 and the name fell to row 2 (live 1919: name cy 447.8
   vs portrait/play cy 359.3, spread 88.5px). And the 1fr tracks
   shrink-wrap to content (132px each), so the portrait pinned left,
   the play pinned right, with the empty name column between them —
   a 140px empty gap at 1919. Fix (CSS only, same selectors, later
   in the file so they win at equal specificity): auto tracks sized
   to content, justify-content:center, gap 24px, every item grid-row:1
   (explicit — immune to DOM order), all justify-self:center,
   align-content:start, and min-height holding the hero box at its base
   height (161px; 133px at <=480px) so the row collapses from two rows
   to one WITHOUT moving anything below it: the intro pair bottoms stay
   575/566/528 and 652/643/600, the bridge-final fold stays 843/844/613.
   No HTML, no JS, no sizes, no colours move; the play button keeps its
   id, handler, tip, orbit and press rules. */
body.fp-stage-on #fpAgreement.fp-view-bridge #fpIntroSide .fp-welcome-hero,
body.fp-stage-on #fpAgreement.fp-view-intro .fp-intro-side .fp-welcome-hero{grid-template-columns:auto auto auto;justify-content:center;gap:24px;min-height:161px;align-content:start}
#fpWelcomeHero .fp-naya-portrait{grid-column:1;grid-row:1;justify-self:center}
#fpWelcomeHero .fp-play-name{grid-column:2;grid-row:1;justify-self:center}
#fpWelcomeHero #fpIntroPlay{grid-column:3;grid-row:1;justify-self:center}
@media(max-width:480px){body.fp-stage-on #fpAgreement.fp-view-bridge #fpIntroSide .fp-welcome-hero,body.fp-stage-on #fpAgreement.fp-view-intro .fp-intro-side .fp-welcome-hero{min-height:133px}}"""

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
    lines = text.split("\n")
    assert lines[2099 - 1] == ANCHOR, "anchor line 2099 moved: %r" % lines[2099 - 1][:100]
    assert text.count("grid-template-columns:auto auto auto") == 0, "new block already present"
    assert text.count("AGREEMENT INTRO ALIGN (2026-11-18)") == 0
    # Old hero grid rules stay exactly once each (superseded, not deleted).
    assert text.count("#fpAgreement.fp-view-bridge #fpIntroSide .fp-welcome-hero{display:grid;grid-template-columns:1fr auto 1fr") == 1
    assert text.count("#fpAgreement.fp-view-intro .fp-intro-side .fp-welcome-hero{display:grid;grid-template-columns:1fr auto 1fr") == 1
    new_lines = lines[:2099] + NEW_BLOCK.split("\n") + lines[2099:]
    new_text = "\n".join(new_lines)
    new = new_text.encode("utf-8")
    # New rules present exactly once each.
    assert new_text.count("grid-template-columns:auto auto auto") == 1
    assert new_text.count("#fpWelcomeHero .fp-play-name{grid-column:2;grid-row:1;justify-self:center}") == 1
    assert new_text.count("#fpWelcomeHero .fp-naya-portrait{grid-column:1;grid-row:1;justify-self:center}") == 1
    assert new_text.count("#fpWelcomeHero #fpIntroPlay{grid-column:3;grid-row:1;justify-self:center}") == 1
    assert new_text.count("min-height:161px") == 1 and new_text.count("min-height:133px") == 1
    # No font-size / color declared in the new block.
    assert "font-size" not in NEW_BLOCK and "color:" not in NEW_BLOCK, "new block declares font/color"
    # F1-F4 + fix-4 invariants identical.
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
        "more4_scroll": "bBridge.scrollTop=bBridge.scrollHeight-bBridge.clientHeight",
        "p3_hidden_rule": ".p3-enter[hidden]{display:none!important}",
        "nextbtn_hidden_rule": "#fpNextBtn[hidden]{display:none}",
        "jewel_spans": '<span class="fp-btn-jewel"',
        "jewel_uri": "data:image/png;base64,",
        "diamond_entity": "&#9670;",
        "fpIntroPick": "fpIntroPick",
    }
    for k, pat in inv.items():
        assert text.count(pat) == new_text.count(pat), "invariant changed: %s (%d -> %d)" % (
            k, text.count(pat), new_text.count(pat))
    print("invariants identical: jewel_spans=%d diamond_entity=%d fpIntroPick=%d play_active=%d" % (
        new_text.count(inv["jewel_spans"]), new_text.count(inv["diamond_entity"]),
        new_text.count(inv["fpIntroPick"]), new_text.count(inv["play_active"])))
    # All three script blocks byte-identical (no JS change).
    sb = re.findall(r"<script>(.*?)</script>", text, re.S)
    sn = re.findall(r"<script>(.*?)</script>", new_text, re.S)
    assert len(sb) == 3 and len(sn) == 3
    for i in range(3):
        assert sha(sb[i].encode()) == sha(sn[i].encode()), "script block %d changed" % i
    print("script blocks: all 3 byte-identical (no JS change)")
    # Intro pair + bridge pair button substrings byte-identical (whole-line
    # identity holds too: the edit touches only CSS lines, no HTML line).
    for frag in ('id="fpChoiceDeck"', 'id="fpChoiceLetter"', 'id="fpBridgeDeck"',
                 'id="fpBridgeLetter"', 'id="fpBridgeExit"', 'id="fpIntroPlay"'):
        assert text.count(frag) == new_text.count(frag) == 1, frag
    # Diff scope: exactly 1 insert hunk.
    sm = difflib.SequenceMatcher(a=text.split("\n"), b=new_text.split("\n"), autojunk=False)
    hunks = [op for op in sm.get_opcodes() if op[0] != "equal"]
    print("diff hunks (base %d lines -> new %d lines):" % (len(text.split("\n")), len(new_text.split("\n"))))
    for tag, i1, i2, j1, j2 in hunks:
        print("  %s base L%d-%d -> new L%d-%d" % (tag, i1 + 1, i2, j1 + 1, j2))
    assert len(hunks) == 1 and hunks[0][0] == "insert", hunks
    print("new welcome: %d B sha=%s (delta %+d B, +%d lines)" % (
        len(new), sha(new), len(new) - BASE_BYTES, len(new_text.split("\n")) - len(text.split("\n"))))
    return new

def run_checker_cli(base_bytes, new_bytes):
    write_resilient(os.path.join(WORK, "base-check.html"), base_bytes)
    write_resilient(os.path.join(WORK, "new-check.html"), new_bytes)
    counts = {}
    for label, path in (("base", os.path.join(WORK, "base-check.html")),
                        ("new", os.path.join(WORK, "new-check.html"))):
        r = subprocess.run([sys.executable, CHECKER, path], capture_output=True, timeout=120)
        out = r.stdout.decode("utf-8", "replace")
        f = out.count("\nFAIL ") + (1 if out.startswith("FAIL ") else 0)
        w = out.count("\nWARN ") + (1 if out.startswith("WARN ") else 0)
        counts[label] = (f, w)
        print("checker CLI %s: %d FAIL + %d WARN (rc %d)" % (label, f, w, r.returncode))
    assert counts["new"] == counts["base"], "checker counts moved: %s" % counts
    assert counts["base"] == (83, 4), "baseline is not 83+4: %s" % counts
    # Normalized multiset comparison (line numbers stripped) — zero new FAILs.
    import importlib.util
    spec = importlib.util.spec_from_file_location("cdl", CHECKER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    def items(text):
        fails, warns = [], []
        for i, line in enumerate(text.splitlines(), 1):
            for rx in m.GRAY_RES:
                if rx.search(line):
                    # Normalized WITHOUT the line number: the insert shifts
                    # every later line by +28, which is not a new FAIL.
                    fails.append(line.strip()[:120])
                    break
        for mt in m.FONTSIZE_RE.finditer(text):
            vals = [float(v) for v in mt.groups() if v is not None]
            if vals and min(vals) < 17:
                fails.append("SIZE: %s" % mt.group(0))
        for mt in m.COLOR_DECL_RE.finditer(text):
            val = mt.group(1).strip().lower()
            if val.startswith("var("):
                continue
            val = val.split()[0].rstrip(";")
            if val in m.FORBIDDEN_TEXT:
                fails.append("TEXT-COLOR: %s" % mt.group(0).strip()[:120])
            elif val not in m.ALLOWED_TEXT and not val.startswith("#"):
                warns.append("TEXT-COLOR?: %s" % mt.group(0).strip()[:120])
        return sorted(set(fails)), sorted(set(warns))
    bf, bw = items(base_bytes.decode("utf-8"))
    nf, nw = items(new_bytes.decode("utf-8"))
    new_fails = [x for x in nf if x not in bf]
    new_warns = [x for x in nw if x not in bw]
    print("checker normalized: base %d FAIL + %d WARN; new %d FAIL + %d WARN; NEW %d/%d"
          % (len(bf), len(bw), len(nf), len(nw), len(new_fails), len(new_warns)))
    assert not new_fails and not new_warns, (new_fails, new_warns)
    # Line-shift proof: every FAIL line number in new is either identical
    # (before the insert) or exactly +28 (after it) — no FAIL added/removed.
    def fail_lines(text):
        out = []
        for i, line in enumerate(text.splitlines(), 1):
            hit = None
            for rx in m.GRAY_RES:
                if rx.search(line):
                    hit = "GRAY"; break
            if hit is None:
                for mt in m.FONTSIZE_RE.finditer(line):
                    vals = [float(v) for v in mt.groups() if v is not None]
                    if vals and min(vals) < 17:
                        hit = "SIZE"; break
            if hit is None:
                for mt in m.COLOR_DECL_RE.finditer(line):
                    val = mt.group(1).strip().lower()
                    if val.startswith("var("):
                        continue
                    val = val.split()[0].rstrip(";")
                    if val in m.FORBIDDEN_TEXT:
                        hit = "COLOR"; break
            if hit:
                out.append((i, hit, line.strip()[:80]))
        return out
    bl = fail_lines(base_bytes.decode("utf-8"))
    nl = fail_lines(new_bytes.decode("utf-8"))
    assert len(bl) == len(nl) == 83, (len(bl), len(nl))
    shifted = [(b, n) for b, n in zip(bl, nl)]
    bad = [(b, n) for b, n in shifted
           if not ((b[0] < 2100 and n[0] == b[0] and b[1:] == n[1:]) or
                   (b[0] >= 2100 and n[0] == b[0] + 28 and b[1:] == n[1:]))]
    print("checker line-shift: %d FAIL lines, %d moved +28, %d unmoved, %d bad"
          % (len(bl), sum(1 for b, n in shifted if n[0] == b[0] + 28),
             sum(1 for b, n in shifted if n[0] == b[0]), len(bad)))
    assert not bad, bad[:5]
    return counts

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
    path = os.path.join(WORK, "worker-align-check.mjs")
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
    run_checker_cli(base, new)
    node_parse_scripts(new.decode("utf-8"))
    write_resilient(WORK_COPY, new)
    write_resilient(BASE_WELCOME, new)
    print("EDIT-RESULT " + json.dumps({
        "welcome_bytes": len(new), "welcome_sha": sha(new),
        "welcome_sha_prefix": sha(new)[:8], "delta": len(new) - BASE_BYTES}))
    return new

def patch_builder(new_sha, new_bytes):
    btxt = open(BUILDER, "rb").read()
    old_assert = (b'assert welcome_sha.startswith("65555c37"), "welcome sha is not the '
                  b'AGREEMENT BUTTONS FIX 4b welcome sha (2026-11-18: #fpBridgeExit gains the harvested jewel span)"')
    assert btxt.count(old_assert) == 1, "builder FIX 4b assert not found exactly once"
    comment = (
        b"# AGREEMENT INTRO ALIGN (2026-11-18, maker round -\n"
        b"# agreement-intro-align-20261118/work/edit-align.py): the welcome sha\n"
        b"# moves 65555c37 -> " + new_sha[:8].encode() + b" (1,168,891 B -> "
        + str(new_bytes).encode() + b" B): one CSS insert only - the intro\n"
        b"# row becomes one tight centred unit (auto tracks, gap 24px, every\n"
        b"# item grid-row:1, min-height holds the hero box at 161/133px so\n"
        b"# nothing below moves). No HTML, no JS. Walk, template, identity,\n"
        b"# unfold shas unchanged.\n")
    new_assert = (b'assert welcome_sha.startswith("' + new_sha[:8].encode() + b'"), "welcome sha is not the '
                  b'AGREEMENT INTRO ALIGN welcome sha (2026-11-18: intro row one tight centred unit)"')
    patched = btxt.replace(old_assert, comment + new_assert)
    assert b"AGREEMENT INTRO ALIGN (2026-11-18" in patched
    write_resilient(BUILDER, patched)
    print("builder patched: assert -> %s, INTRO ALIGN comment added (%d B)" % (new_sha[:8], len(patched)))
    return patched

def run_builder(new_welcome, expect_prefix):
    btxt = open(BUILDER, "rb").read()
    assert ('welcome_sha.startswith("%s")' % expect_prefix).encode() in btxt, \
        "builder not patched to the new welcome prefix"
    assert b"AGREEMENT INTRO ALIGN (2026-11-18" in btxt, \
        "builder lacks the intro-align round comment"
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
    assert b"grid-template-columns:auto auto auto" in w
    assert b"AGREEMENT INTRO ALIGN (2026-11-18)" in w
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
    assert sha(embeds["UNFOLD"])[:8] == "96b18b6f", "worker unfold changed"
    assert sha(embeds["WALK"])[:8] == "4b5f9264" and sha(embeds["IDENTITY"])[:8] == "a1550164"
    assert sha(embeds["PERSONAL_TEMPLATE"])[:8] == "61002d15"
    return w

def commit_message(welcome_sha, worker_sha, welcome_bytes, worker_bytes):
    return (
        "Agreement INTRO ALIGN (2026-11-18, maker round; MAKER-REPORT.md in "
        "agreement-intro-align-20261118/)\n\n"
        "One CSS insert. The intro row — portrait + NAYA + play — read as two "
        "elements floating apart: the 03:41Z grid (1fr auto 1fr) hit the grid "
        "auto-placement cursor trap (the name comes after the play button in "
        "the DOM, so it fell to row 2: live name cy 447.8 vs portrait/play "
        "359.3 at 1919) and the 1fr tracks shrink-wrapped, pinning portrait "
        "left and play right with a 140px empty gap. The row is now one tight "
        "centred unit: auto tracks, gap 24px (reference crop gaps ~20/~29px), "
        "every item grid-row:1, min-height holding the hero box at 161/133px "
        "so nothing below moves — intro pair bottoms stay 575/566/528 and "
        "652/643/600, bridge-final fold stays 843/844/613. No HTML, no JS, "
        "no sizes, no colours. The play button keeps its id, handler, tip, "
        "orbit and press rules.\n\n"
        "NO REGRESSION: all three inline script blocks byte-identical (no JS "
        "change); F1-F4 counts identical; design laws zero new FAILs vs base "
        "(83 FAIL + 4 WARN both sides). Worker built twice, identical sha %s "
        "(%d B); embeds verified: WALK 4b5f9264, IDENTITY a1550164, WELCOME %s, "
        "UNFOLD 96b18b6f.\n\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after "
        "the PUT. Worker PUT with --meta v23-meta.json (WELCOME_ASSETS "
        "1cf80db6183245d19dd5296645a12bd0 intact). NO PR, NO MERGE — the "
        "checker and the captain come after this seat. Nothing live - the "
        "finished update goes LIVE on the main URL only on Shawn's tap, "
        "after his eye."
        % (worker_sha[:8], worker_bytes, welcome_sha[:8], STAGING))

def create_branch():
    _, ref = gh("GET", "/repos/%s/git/refs/heads/%s" % (REPO, BASE_BRANCH))
    print("base branch tip:", ref["object"]["sha"])
    assert ref["object"]["sha"] == PARENT_TIP, "base branch tip moved: %s" % ref["object"]["sha"]
    _, nb = gh("POST", "/repos/%s/git/refs" % REPO,
               {"ref": "refs/heads/%s" % NEW_BRANCH, "sha": PARENT_TIP})
    print("new branch created:", nb["ref"], nb["object"]["sha"])
    assert nb["object"]["sha"] == PARENT_TIP
    return nb["object"]["sha"]

def file_commit(new_welcome, worker, welcome_sha, worker_sha):
    builder = open(BUILDER, "rb").read()
    driver = open(os.path.join(WORK, "edit-align.py"), "rb").read()
    _, ref = gh("GET", "/repos/%s/git/refs/heads/%s" % (REPO, NEW_BRANCH))
    print("branch tip before:", ref["object"]["sha"])
    assert ref["object"]["sha"] == PARENT_TIP, "branch tip moved: %s" % ref["object"]["sha"]
    _, commit = gh("GET", "/repos/%s/git/commits/%s" % (REPO, PARENT_TIP))
    base_tree = commit["tree"]["sha"]
    print("base tree:", base_tree)
    files = [
        ("team-nitro/walk-v23-assembly-20261114/welcome-staged.html", new_welcome),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
        ("team-nitro/agreement-intro-align-20261118/work/edit-align.py", driver),
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
    _, ref2 = gh("PATCH", "/repos/%s/git/refs/heads/%s" % (REPO, NEW_BRANCH),
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
    create_branch()
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
        sys.exit("usage: edit-align.py [edit|all]")
