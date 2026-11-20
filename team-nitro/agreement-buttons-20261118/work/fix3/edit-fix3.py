#!/usr/bin/env python3
"""AGREEMENT BUTTONS FIX 3 (2026-11-18) — maker driver.

Eye verdict 04:55Z (GOES BACK): round 1's three headline changes landed
on the bridge-final pair (#fpBridgeDeck/#fpBridgeLetter) but NOT on the
intro pair (#fpChoiceDeck/#fpChoiceLetter), the first view the user sees.
This round finishes them on the intro pair, and brings the bridge-final
pair above the fold at 1919. Welcome file ONLY. Work dir:
~/workspace/team-nitro/agreement-buttons-20261118/work/fix3/

  1. LABEL: #fpChoiceLetter -> "Read the agreement" (exactly as
     #fpBridgeLetter reads).
  2. JEWEL: add the .fp-btn-jewel span to BOTH intro buttons, removing
     the literal U+25C6 diamond text from both. HARVESTED, not redrawn:
     the data-URI is decoded from the filed welcome blob's own
     .fp-btn-jewel rule (the same byte-identical PNG already on the
     bridge pair: 12,715 B, sha e583f51f..., 96x96) and verified before
     use. No new image bytes are introduced.
  3. PICK LINE GONE: #fpIntroPick ("Pick your view - one, or both, as
     you wish.") removed from the intro view. Zero JS references exist
     (proven from bytes); no JS change.
  4. BRIDGE-FINAL FOLD: tighten spacing above the bridge-final buttons,
     bridge view only, 64px in all (steplabel 4, jewels 6, choices 4,
     logo gap 20, head gap 22, side gap 8), so the letter bottom moves
     1130 -> 1066 at 1919 on first paint, without scrolling the
     container. Intro fold, hero row, button sizes, press/hover, deck,
     legal row, #fpNextBtn2, bridge jewel/label all untouched.

Base: welcome blob e32fe54a, 1,165,606 B, sha256
48fc853ffd668a96f8cf02108ceaa5108944529bd70d8d4bddda1f4c01921096
(branch walk-end/agreement-merge-20261117, tip
45826b0959b50f632ebb37cd9488280929dbce30).

Modes:
  edit - compute the new welcome bytes + sha, verify every assert, run
         the design-law checker (base vs new, in memory) and the node
         parse checks. NO network, NO filing.
  all  - edit, then build the worker via the builder (--stdout
         --welcome-stdin; builder must already be patched to the new
         welcome sha - see patch step in the report), file ONE commit
         (welcome + worker + builder + this driver), PUT to staging,
         verify all 7 routes by sha256.

Pipeline is in memory throughout (EPERM flake: disk writes are attempted
with retries but never trusted; a 0-byte file is flake damage, never
truth). gh-direct.py / cf-worker.py read their payloads from stdin where
the size allows.
"""
import base64, hashlib, io, json, os, re, subprocess, sys, time

HOME = os.path.expanduser("~")
WORK = os.path.join(HOME, "workspace/team-nitro/agreement-buttons-20261118/work/fix3")
V23 = os.path.join(HOME, "workspace/team-nitro/walk-v23-assembly-20261114")
BASE_WELCOME = os.path.join(V23, "welcome-staged.html")
WORK_COPY = os.path.join(WORK, "welcome-fix3.html")
BUILDER = os.path.join(V23, "build-v23-staging-worker.py")
CHECKER = os.path.join(HOME, "workspace/team-nitro/check-design-laws.py")
GH = os.path.join(HOME, "workspace/team-nitro/gh-direct.py")
CF = os.path.join(HOME, "workspace/project-intelligence/cf-worker.py")
META = os.path.join(V23, "v23-meta.json")
REPO = "SoulSchoolAcademy/NayaPOWER"
BRANCH = "walk-end/agreement-merge-20261117"
PARENT_TIP = "45826b0959b50f632ebb37cd9488280929dbce30"
BASE_BLOB = "e32fe54aeeadf3a6fbdc6c1bbe0ae7dd31d887c4"
BASE_SHA = "48fc853ffd668a96f8cf02108ceaa5108944529bd70d8d4bddda1f4c01921096"
BASE_BYTES = 1165606
JEWEL_SHA = "e583f51f6a2dfe551ac3379ca8eb67e10f10b79d1236d7961122c800009377d2"
JEWEL_BYTES = 12715
CF_ACCOUNT = "b5e2a51b3e883f7722287c5f51b1196b"
CF_SCRIPT = "naya-walk-beginning-staging"
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
# Eye measurements, bridge-final at 1919 on first paint (EYE-VERDICT.md):
EYE_DECK_BOTTOM = 1055
EYE_LETTER_BOTTOM = 1130
FOLD_1919 = 1080
# Savings above the bridge-final letter button, all bridge-view scoped:
FOLD_SAVINGS = {"steplabel": 4, "jewels": 6, "choices": 4,
                "logo_gap": 20, "head_gap": 22, "side_gap": 8}

def sha(b): return hashlib.sha256(b).hexdigest()

# ---------------------------------------------------------------- jewel
def jewel_data_uri(text):
    """Decode the jewel PNG from the filed welcome blob's own .fp-btn-jewel
    rule (round 1's harvest) and verify it byte-identically before reuse.
    No new image bytes are introduced: the intro buttons reuse the shared
    class, so the data-URI occurrence count in the file does not move."""
    m = re.search(r'\.fp-btn-jewel\{[^}]*background:url\("data:image/png;base64,([^"]+)"\)', text)
    assert m, ".fp-btn-jewel rule with data-URI not found in base"
    png = base64.b64decode(m.group(1))
    assert len(png) == JEWEL_BYTES, "jewel PNG size %d, want %d" % (len(png), JEWEL_BYTES)
    assert sha(png) == JEWEL_SHA, "jewel PNG sha mismatch: %s" % sha(png)
    from PIL import Image
    im = Image.open(io.BytesIO(png))
    assert im.size == (96, 96) and im.mode == "RGBA", "jewel geometry wrong: %s %s" % (im.size, im.mode)
    print("jewel verified from base bytes: %d B sha=%s 96x96 RGBA" % (len(png), sha(png)[:8]))
    return "data:image/png;base64," + m.group(1)

# ---------------------------------------------------------------- edits
CHOICE_DECK_OLD = ('<button class="fp-intro-choice" id="fpChoiceDeck" type="button" '
                   'style="--tone:#8e24aa">Begin the visual story \u25c6</button>')
CHOICE_DECK_NEW = ('<button class="fp-intro-choice" id="fpChoiceDeck" type="button" '
                   'style="--tone:#8e24aa">Begin the visual story '
                   '<span class="fp-btn-jewel" aria-hidden="true"></span></button>')
CHOICE_LETTER_OLD = ('<button class="fp-intro-choice" id="fpChoiceLetter" type="button" '
                     'style="--tone:#07925f">Read the Collective Agreement \u25c6</button>')
CHOICE_LETTER_NEW = ('<button class="fp-intro-choice" id="fpChoiceLetter" type="button" '
                     'style="--tone:#07925f">Read the agreement '
                     '<span class="fp-btn-jewel" aria-hidden="true"></span></button>')
PICK_LINE = ('<p class="fp-intro-pick" id="fpIntroPick">Pick your view \u2014 one, '
             'or both, as you wish.</p>\n')
# Round-1 CSS block ends with this rule, directly before </style>.
CSS_ANCHOR = ("html.fp-locked body.fp-stage-on.fp-bridge "
              "#fpAgreement.fp-layer-on{padding-top:40px}\n</style>")

CSS_BLOCK = """
/* AGREEMENT BUTTONS FIX 3 (2026-11-18, eye verdict 04:55Z) - round 1's
   three changes landed on the bridge-final pair but not on the intro
   pair, the first view. This block finishes them on the intro pair and
   brings the bridge-final pair above the fold at 1919.
   1. LABEL + JEWEL (HTML below): the intro letter button reads "Read
      the agreement" with the same jewel span as the bridge pair; the
      intro deck button gains the same jewel span. No new image: the
      spans use the shared .fp-btn-jewel class from round 1.
   2. PICK LINE GONE: the intro pick line is removed from the HTML
      below; the .fp-intro-pick rule stays (dead, harmless).
   3. BRIDGE-FINAL FOLD: tighten spacing above the bridge-final
      buttons, bridge view only, 64px in all (steplabel 4, jewels 6,
      choices 4, logo gap 20, head gap 22, side gap 8), so the letter
      bottom moves 1130 -> 1066 at 1919 on first paint. The intro
      view, the hero row, the button sizes and the press rules are
      untouched. */
#fpBridgeFinal .letter-steplabel{margin-bottom:8px}
.fp-bridge-jewels{margin:8px auto 4px}
.fp-bridge-choices{margin:8px auto 8px}
body.fp-stage-on #fpAgreement.fp-view-bridge .fp-agree-logo{margin-bottom:8px}
body.fp-stage-on #fpAgreement.fp-view-bridge .fp-agree-head{margin-bottom:8px}
body.fp-stage-on #fpAgreement.fp-view-bridge #fpIntroSide{margin-bottom:16px}
"""

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
    """Read the base welcome bytes from the GitHub blob API. The local
    v23 file is 0 bytes (EPERM flake damage, 04:06Z) and is NEVER used."""
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
    jewel_uri = jewel_data_uri(text)
    assert text.count("data:image/png;base64,") == 2, "unexpected data-URI count in base"
    # --- three pairs, verified from bytes before editing ---
    # (1) intro/choice pair: #fpChoiceDeck/#fpChoiceLetter in #fpIntroChoices
    #     (line 2200), inside <section id="deckUnfold"> inside #fpAgreement.
    # (2) bridge-final pair: #fpBridgeDeck/#fpBridgeLetter in #fpBridgeChoices
    #     inside #fpBridgeFinal inside #fpBridge (giant line 2193).
    # (3) deck-end pair: #fpNextBtn/#fpNextBtn2 in #fpNextRow inside
    #     #fpStageBarB (line 2182) - deck-only, untouched by this round.
    pre = {
        "choice_deck_old": text.count(CHOICE_DECK_OLD),
        "choice_letter_old": text.count(CHOICE_LETTER_OLD),
        "pick_line": text.count(PICK_LINE),
        "pick_id": text.count("fpIntroPick"),
        "bridge_deck_new": text.count('id="fpBridgeDeck" type="button" style="--tone:#8e24aa">Begin the visual story <span class="fp-btn-jewel"'),
        "bridge_letter_new": text.count('id="fpBridgeLetter" type="button" style="--tone:#07925f">Read the agreement <span class="fp-btn-jewel"'),
        "next_btn2": text.count('id="fpNextBtn2"'),
        "css_anchor": text.count(CSS_ANCHOR),
        "diamond_literal": text.count("\u25c6"),
        "diamond_entity": text.count("&#9670;"),
        "jewel_spans": text.count('<span class="fp-btn-jewel"'),
        "jewel_uri": text.count("data:image/png;base64,"),
        "read_agreement": text.count("Read the agreement "),
    }
    assert pre["choice_deck_old"] == 1 and pre["choice_letter_old"] == 1, pre
    assert pre["pick_line"] == 1 and pre["pick_id"] == 1, pre
    assert pre["bridge_deck_new"] == 1 and pre["bridge_letter_new"] == 1, pre
    assert pre["next_btn2"] == 1 and pre["css_anchor"] == 1, pre
    assert pre["diamond_literal"] == 5 and pre["diamond_entity"] == 345, pre
    assert pre["jewel_spans"] == 2 and pre["jewel_uri"] == 2, pre
    assert pre["read_agreement"] == 1, pre  # bridge letter only, so far
    # --- JS safety for the pick removal: zero references anywhere ---
    scripts = re.findall(r"<script>(.*?)</script>", text, re.S)
    assert len(scripts) == 3, "script block count %d" % len(scripts)
    for i, s in enumerate(scripts):
        assert "fpIntroPick" not in s, "script block %d references fpIntroPick" % i
        assert "fp-intro-pick" not in s, "script block %d references fp-intro-pick" % i
    assert text.count("fpIntroPick") == 1, "fpIntroPick occurs outside its own line"
    print("JS safety proven: fpIntroPick occurs 0x in all 3 script blocks (only its own HTML line)")
    # --- the edits ---
    offsets = {}
    def sub(old, new, key):
        nonlocal text
        i = text.find(old)
        assert i >= 0, "anchor missing: %s" % key
        assert text.count(old) == 1, "anchor not unique: %s" % key
        offsets[key] = i
        text = text[:i] + new + text[i + len(old):]
    sub(CHOICE_DECK_OLD, CHOICE_DECK_NEW, "choice_deck")
    sub(CHOICE_LETTER_OLD, CHOICE_LETTER_NEW, "choice_letter")
    sub(PICK_LINE, "", "pick")
    sub(CSS_ANCHOR, CSS_ANCHOR.replace("\n</style>", "\n" + CSS_BLOCK + "</style>"), "css_block")
    new = text.encode("utf-8")
    post = {
        "choice_deck_new": text.count(CHOICE_DECK_NEW),
        "choice_letter_new": text.count(CHOICE_LETTER_NEW),
        "choice_deck_old": text.count(CHOICE_DECK_OLD),
        "choice_letter_old": text.count(CHOICE_LETTER_OLD),
        "pick_line": text.count(PICK_LINE),
        "pick_id": text.count("fpIntroPick"),
        "bridge_deck_new": text.count('id="fpBridgeDeck" type="button" style="--tone:#8e24aa">Begin the visual story <span class="fp-btn-jewel"'),
        "bridge_letter_new": text.count('id="fpBridgeLetter" type="button" style="--tone:#07925f">Read the agreement <span class="fp-btn-jewel"'),
        "next_btn2": text.count('id="fpNextBtn2"'),
        "diamond_literal": text.count("\u25c6"),
        "diamond_entity": text.count("&#9670;"),
        "jewel_spans": text.count('<span class="fp-btn-jewel"'),
        "jewel_uri": text.count("data:image/png;base64,"),
        "read_agreement": text.count("Read the agreement "),
        "css_steplabel": text.count("#fpBridgeFinal .letter-steplabel{margin-bottom:8px}"),
        "css_jewels": text.count(".fp-bridge-jewels{margin:8px auto 4px}"),
        "css_choices": text.count(".fp-bridge-choices{margin:8px auto 8px}"),
        "css_logo": text.count("body.fp-stage-on #fpAgreement.fp-view-bridge .fp-agree-logo{margin-bottom:8px}"),
        "css_head": text.count("body.fp-stage-on #fpAgreement.fp-view-bridge .fp-agree-head{margin-bottom:8px}"),
        "css_side": text.count("body.fp-stage-on #fpAgreement.fp-view-bridge #fpIntroSide{margin-bottom:16px}"),
    }
    assert post["choice_deck_new"] == 1 and post["choice_letter_new"] == 1, post
    assert post["choice_deck_old"] == 0 and post["choice_letter_old"] == 0, post
    assert post["pick_line"] == 0 and post["pick_id"] == 0, post
    assert post["bridge_deck_new"] == 1 and post["bridge_letter_new"] == 1, post
    assert post["next_btn2"] == 1, post
    assert post["diamond_literal"] == 3 and post["diamond_entity"] == 345, post
    assert post["jewel_spans"] == 4 and post["jewel_uri"] == 2, post
    assert post["read_agreement"] == 2, post
    for k in ("css_steplabel", "css_jewels", "css_choices", "css_logo", "css_head", "css_side"):
        assert post[k] == 1, (k, post)
    # remaining literal diamonds must all be inside CSS comments (invisible)
    in_comment = False
    for n, l in enumerate(text.split("\n"), 1):
        # track /* ... */ state across lines (multi-line comments exist)
        idx = 0
        line_is_comment = in_comment
        while idx < len(l):
            if not in_comment:
                j = l.find("/*", idx)
                if j < 0:
                    break
                in_comment = True
                line_is_comment = True
                idx = j + 2
            else:
                j = l.find("*/", idx)
                if j < 0:
                    break
                in_comment = False
                idx = j + 2
        if "\u25c6" in l:
            assert line_is_comment, \
                "literal diamond survives outside a comment at line %d: %s" % (n, l.strip()[:120])
    # --- F1-F4 no-regression anchors, byte-identical ---
    base_text = base.decode("utf-8")
    f_base, f_new = {}, {}
    inv = {
        "_fpAlias2": "_fpAlias2",
        "enterStage();": "enterStage();",
        "press_sink": "#fpAgreement #dealAgreeBtn:active,#fpAgreement #letterPageAgree:active",
        "choice_active": ".fp-intro-choice:active",
        "play_active": ".p3-naya-play:active",
        "rest_glow": "#fpBridgeDeck:not(:hover):not(:active)",
        "deck_end_return_clear": "window.__fpDeckEndReturn=false;enterStage();",
        "deck_end_return": "__fpDeckEndReturn",
        "getItem_fp_stage": "getItem('nayanet_fp_stage')",
        "setItem_fp_stage": "setItem('nayanet_fp_stage'",
        "localStorage_setItem": "localStorage.setItem",
    }
    for k, pat in inv.items():
        f_base[k] = base_text.count(pat)
        f_new[k] = text.count(pat)
        assert f_base[k] == f_new[k], "invariant changed: %s %s -> %s" % (k, f_base[k], f_new[k])
    assert f_new["_fpAlias2"] == 3 and f_new["enterStage();"] == 3, f_new
    assert f_new["press_sink"] == 1 and f_new["choice_active"] == 2 and f_new["play_active"] == 2, f_new
    assert f_new["rest_glow"] == 1 and f_new["deck_end_return_clear"] == 1, f_new
    assert f_new["deck_end_return"] == 5 and f_new["getItem_fp_stage"] == 2, f_new
    assert f_new["setItem_fp_stage"] == 1 and f_new["localStorage_setItem"] == 6, f_new
    # --- inline script blocks byte-identical to base ---
    new_scripts = re.findall(r"<script>(.*?)</script>", text, re.S)
    assert len(new_scripts) == 3
    for i, (a, b) in enumerate(zip(scripts, new_scripts)):
        assert sha(a.encode()) == sha(b.encode()), "script block %d changed" % i
    # --- diff scope: only the CSS block insert + pick line + choice line ---
    import difflib
    base_lines = base_text.split("\n")
    new_lines = text.split("\n")
    sm = difflib.SequenceMatcher(a=base_lines, b=new_lines, autojunk=False)
    hunks = [op for op in sm.get_opcodes() if op[0] != "equal"]
    print("diff hunks (base %d lines -> new %d lines):" % (len(base_lines), len(new_lines)))
    for tag, i1, i2, j1, j2 in hunks:
        print("  %s base L%d-%d -> new L%d-%d" % (tag, i1 + 1, i2, j1 + 1, j2))
    # Exactly 2 hunks: (a) the CSS block insert before </style>; (b) the
    # adjacent pick-line removal + choice-line replacement (base L2199-2200,
    # one line removed, one line replaced - difflib merges adjacent edits).
    assert len(hunks) == 2, "expected exactly 2 diff hunks, got %d" % len(hunks)
    assert hunks[0][0] == "insert", hunks
    assert hunks[1][0] == "replace" and hunks[1][1] == 2198 and hunks[1][2] == 2200, hunks
    # --- fold math ---
    saved = sum(FOLD_SAVINGS.values())
    assert saved == 64, FOLD_SAVINGS
    new_deck = EYE_DECK_BOTTOM - saved
    new_letter = EYE_LETTER_BOTTOM - saved
    assert new_letter <= FOLD_1919, "letter still below fold: %d" % new_letter
    print("fold math: saved %dpx %s; deck bottom %d -> %d; letter bottom %d -> %d (fold %d, slack %dpx)"
          % (saved, FOLD_SAVINGS, EYE_DECK_BOTTOM, new_deck, EYE_LETTER_BOTTOM, new_letter,
             FOLD_1919, FOLD_1919 - new_letter))
    print("edits ok: pre=%s" % pre)
    print("edits ok: post=%s" % post)
    print("edits ok: F1-F4=%s" % f_new)
    print("edits ok: offsets=%s" % offsets)
    print("new welcome: %d B sha=%s (delta %+d B)" % (len(new), sha(new), len(new) - BASE_BYTES))
    return new, offsets

# ---------------------------------------------------------------- checker
def check_text(text, label):
    """Faithful in-memory port of check-design-laws.py check() (the real
    checker takes a file path; disk writes are flake-prone, so the same
    regexes and the same loops run here on the bytes in memory)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("cdl", CHECKER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    fails, warns = [], []
    for i, line in enumerate(text.splitlines(), 1):
        for rx in m.GRAY_RES:
            if rx.search(line):
                fails.append("%s:%d: GRAY (§2.2 no gray text): %s"
                             % (label, i, line.strip()[:120]))
                break
    for mt in m.FONTSIZE_RE.finditer(text):
        vals = [float(v) for v in mt.groups() if v is not None]
        if vals and min(vals) < 17:
            line_no = text[:mt.start()].count("\n") + 1
            fails.append("%s:%d: SIZE (§2.3 below 17px): %s"
                         % (label, line_no, mt.group(0)))
    for mt in m.COLOR_DECL_RE.finditer(text):
        val = mt.group(1).strip().lower()
        if val.startswith("var("):
            continue
        val = val.split()[0].rstrip(";")
        line_no = text[:mt.start()].count("\n") + 1
        if val in m.FORBIDDEN_TEXT:
            fails.append("%s:%d: TEXT-COLOR (§2.2 red/orange/magenta as text): %s"
                         % (label, line_no, mt.group(0).strip()[:120]))
        elif val not in m.ALLOWED_TEXT and not val.startswith("#"):
            warns.append("%s:%d: TEXT-COLOR? (§2.2 check by eye): %s"
                         % (label, line_no, mt.group(0).strip()[:120]))
    if ":hover" not in text:
        warns.append("%s: NO-HOVER (§1 warning — no :hover rules found)" % label)
    return sorted(set(fails)), sorted(set(warns))

def run_checker(base_text, new_text):
    bf, bw = check_text(base_text, "base")
    nf, nw = check_text(new_text, "new")
    norm = lambda items: sorted(re.sub(r"^[^:]+:\d+: ", "", x) for x in items)
    new_fails = [x for x in norm(nf) if x not in norm(bf)]
    new_warns = [x for x in norm(nw) if x not in norm(bw)]
    print("checker: base %d FAIL + %d WARN; new %d FAIL + %d WARN; NEW fails %d, NEW warns %d"
          % (len(bf), len(bw), len(nf), len(nw), len(new_fails), len(new_warns)))
    for x in new_fails:
        print("  NEW FAIL: %s" % x)
    for x in new_warns:
        print("  NEW WARN: %s" % x)
    assert not new_fails, "new design-law FAILs introduced"
    assert not new_warns, "new design-law WARNs introduced"
    return len(bf), len(bw), len(nf), len(nw)

def node_parse_scripts(new_text):
    script_re = re.compile(r"<script>(.*?)</script>", re.S)
    blocks = script_re.findall(new_text)
    js = ("const vm=require('vm');let s='';process.stdin.on('data',d=>s+=d);"
          "process.stdin.on('end',()=>{new vm.Script(s);console.log('script-parse-ok');});")
    for i, b in enumerate(blocks):
        r = subprocess.run(["node", "-e", js], input=b.encode("utf-8"),
                           capture_output=True, timeout=60)
        assert r.returncode == 0 and b"script-parse-ok" in r.stdout, \
            "script block %d failed to parse: %s" % (i, r.stderr[:400])
        print("node: script block %d parses (%d B)" % (i, len(b)))

def node_check_worker(worker):
    path = os.path.join(WORK, "worker-fix3-check.mjs")
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
    """Write via a scratch file + os.replace (EPERM flake: per-path per-moment).
    NEVER truncate-first: a 0-byte file is flake damage, never truth — verify
    size+sha after every attempt."""
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
    new, offsets = compute_new_welcome()
    base = load_base()
    base_text = base.decode("utf-8")
    bf, bw, nf, nw = run_checker(base_text, new.decode("utf-8"))
    node_parse_scripts(new.decode("utf-8"))
    write_resilient(WORK_COPY, new)
    write_resilient(BASE_WELCOME, new)
    print("EDIT-RESULT " + json.dumps({
        "welcome_bytes": len(new), "welcome_sha": sha(new),
        "welcome_sha_prefix": sha(new)[:8], "delta": len(new) - BASE_BYTES,
        "checker": {"base_fail": bf, "base_warn": bw, "new_fail": nf, "new_warn": nw},
        "offsets": offsets}))
    return new

# ---------------------------------------------------------------- builder + file + stage
def run_builder(new_welcome, expect_prefix):
    """Build the staging worker twice (determinism check) via the patched
    builder, welcome from stdin. Returns the worker bytes."""
    btxt = open(BUILDER, "rb").read()
    assert ('welcome_sha.startswith("%s")' % expect_prefix).encode() in btxt, \
        "builder not patched to the new welcome prefix"
    assert b"AGREEMENT BUTTONS FIX 3 (2026-11-18" in btxt, \
        "builder lacks the fix-3 round comment"
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
    assert b"Read the agreement" in w and b"fp-btn-jewel" in w, \
        "worker does not embed the new welcome"
    assert b'<p class="fp-intro-pick" id="fpIntroPick">' not in w, \
        "worker still embeds the intro pick element"
    assert w.count(b"fpIntroPick") == 0, \
        "worker fpIntroPick count %d (want 0)" % w.count(b"fpIntroPick")
    # worker embeds: JSON-decode each asset literal, hash the bytes
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
    saved = sum(FOLD_SAVINGS.values())
    return (
        "Agreement BUTTONS FIX 3 (2026-11-18, eye verdict 04:55Z GOES BACK; "
        "MAKER-REPORT-3.md in agreement-buttons-20261118/)\n\n"
        "Round 1's three headline changes landed on the bridge-final pair "
        "but not on the intro pair, the first view the user sees. This "
        "round finishes them there, and brings the bridge-final pair above "
        "the fold at 1919. Welcome file ONLY, one pass, one commit.\n\n"
        "1. LABEL: #fpChoiceLetter reads 'Read the agreement' (exactly as "
        "#fpBridgeLetter reads). The intro deck button's label is unchanged.\n\n"
        "2. THE JEWEL: both intro buttons gain the .fp-btn-jewel span (the "
        "same shared class as the bridge pair) and the literal flat diamond "
        "text is gone from both. No new image: the span reuses round 1's "
        "harvested jewel PNG (12,715 B, sha e583f51f, 96x96), decoded from "
        "the filed welcome blob's own .fp-btn-jewel rule and verified "
        "byte-identical before use.\n\n"
        "3. PICK LINE GONE: #fpIntroPick removed ('Pick your view - one, or "
        "both, as you wish.'). Zero JS references exist (proven from bytes "
        "in all three script blocks), so no JS change was needed. The dead "
        ".fp-intro-pick CSS rule stays, harmless.\n\n"
        "4. BRIDGE-FINAL FOLD: tighten spacing above the bridge-final "
        "buttons, bridge view only, %dpx in all (steplabel 4, jewels 6, "
        "choices 4, logo gap 20, head gap 22, side gap 8), so the letter "
        "bottom moves 1130 -> %d at 1919 on first paint, without scrolling "
        "the container. The intro pair's fold, the hero row, the button "
        "sizes, the press/hover rules, the deck, the legal row, #fpNextBtn2 "
        "and the bridge pair's jewel/label are untouched.\n\n"
        "NO REGRESSION: _fpAlias2 x3, enterStage(); x3, press sink (2,1,0) "
        "x1, rest glow x1, deck-end clear x1, __fpDeckEndReturn x5, getItem "
        "x2, setItem x1, localStorage.setItem x6 - all byte-identical to "
        "base. All three inline script blocks byte-identical. Design laws: "
        "zero new FAILs vs base. Worker built twice, identical sha %s "
        "(%d B); embeds verified: WALK 4b5f9264, IDENTITY a1550164, WELCOME "
        "%s, UNFOLD 96b18b6f.\n\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after "
        "the PUT. Worker PUT with --meta v23-meta.json (WELCOME_ASSETS "
        "1cf80db6183245d19dd5296645a12bd0 intact). PR #3453 OPEN AND UNMERGED "
        "BY DESIGN - do not merge; the captain decides the PR vehicle. "
        "Nothing live - the finished update goes LIVE on the main URL only "
        "on Shawn's tap, after his eye."
        % (saved, EYE_LETTER_BOTTOM - saved, worker_sha[:8], worker_bytes,
           welcome_sha[:8], STAGING))

def file_commit(new_welcome, worker, welcome_sha, worker_sha):
    builder = open(BUILDER, "rb").read()
    driver = open(os.path.join(WORK, "edit-fix3.py"), "rb").read()
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
        ("team-nitro/agreement-buttons-20261118/work/fix3/edit-fix3.py", driver),
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
        sys.exit("usage: edit-fix3.py [edit|all]")
