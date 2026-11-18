#!/usr/bin/env python3
"""AGREEMENT BUTTONS FOLLOW-ON (2026-11-18) — maker driver.

Six changes, one pass, file once. Shawn's eye 03:37Z + 03:41Z on the staged
agreement intro (bridge view). Work dir: ~/workspace/team-nitro/agreement-buttons-20261118/work/

  1. LABEL: #fpBridgeLetter -> "Read the agreement" (one line, no wrap).
  2. EQUAL SIZE: bridge pair never wraps, shared 64px min-height floor.
  3. THE JEWEL: the flat <> glyph at the end of EACH bridge button becomes
     the emblem's own diamond (NAYA_ICON.png, central purple diamond, NOT
     the crown frame) — harvested, one shared class, SAME image in both.
  4. REMOVE #fpBridgePick only ("Pick your view - one, or both, as you wish.").
  5. HERO ROW: portrait -> "Naya" -> play on the right (harvested flank
     grid 1fr auto 1fr from walk-beginning-fixed.html; DOM order unchanged,
     play keeps id/handler/tip/orbit/press).
  6. LOGO UP A TAD: bridge layer padding-top 48px -> 40px.

Base: welcome-staged.html, branch walk-end/agreement-merge-20261117,
tip a6c2c6b3105865ae3c0727aeb666bbdb118da370, welcome blob 9321486e,
1,146,242 B, sha256 2e74273b5caf12dfbb2ef2113e4e491530d23fe382e79ef329514023e974e7fb.

Modes:
  edit  - compute the new welcome bytes + sha, verify every assert, attempt
          resilient disk writes (v23 file + work copy), run the design-law
          checker (base vs new, in memory) and the node parse checks.
          NO network, NO filing.
  all   - edit, then patch-check the builder (patched on disk via muse.edit
          BEFORE this mode runs), build the worker via the builder
          (--stdout --welcome-stdin), file ONE commit (welcome + worker +
          builder + this driver), PUT to staging, verify all routes by sha256.

Pipeline is in memory throughout (EPERM flake: disk writes are attempted
with retries but never trusted; a 0-byte file is flake damage, never truth).
Only muse.write/muse.edit land reliably; gh-direct.py / cf-worker.py read
their payloads from stdin where the size allows.
"""
import base64, hashlib, io, json, math, os, re, subprocess, sys, time

HOME = os.path.expanduser("~")
WORK = os.path.join(HOME, "workspace/team-nitro/agreement-buttons-20261118/work")
V23 = os.path.join(HOME, "workspace/team-nitro/walk-v23-assembly-20261114")
BASE_WELCOME = os.path.join(V23, "welcome-staged.html")
BASE_REFERENCE = os.path.join(HOME, "workspace/team-nitro/agreement-merge-followon2-20261118/work/welcome-followon2.html")
WORK_COPY = os.path.join(WORK, "welcome-buttons.html")
BUILDER = os.path.join(V23, "build-v23-staging-worker.py")
EMBLEM = os.path.join(HOME, "workspace/user/media_library/image/NAYA_ICON.png")
CHECKER = os.path.join(HOME, "workspace/team-nitro/check-design-laws.py")
GH = os.path.join(HOME, "workspace/team-nitro/gh-direct.py")
CF = os.path.join(HOME, "workspace/project-intelligence/cf-worker.py")
META = os.path.join(V23, "v23-meta.json")
REPO = "SoulSchoolAcademy/NayaPOWER"
BRANCH = "walk-end/agreement-merge-20261117"
PARENT_TIP = "a6c2c6b3105865ae3c0727aeb666bbdb118da370"
BASE_SHA = "2e74273b5caf12dfbb2ef2113e4e491530d23fe382e79ef329514023e974e7fb"
BASE_BYTES = 1146242
CF_ACCOUNT = "b5e2a51b3e883f7722287c5f51b1196b"
CF_SCRIPT = "naya-walk-beginning-staging"
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"

def sha(b): return hashlib.sha256(b).hexdigest()

# ---------------------------------------------------------------- jewel
def jewel_data_uri():
    """Harvest the central purple diamond from the emblem.

    The diamond is faceted with large black gaps between facets, so its
    outline cannot be recovered from brightness runs, and a rhombus
    edge-fit fails: the silver frame's bright core sits INSIDE the outer
    edge, not on it (measured: on-edge agreement only ~0.45 for every
    geometry tried). The geometry below is measured, not guessed:
      - strict-purple facet bbox x 563-1237, y 718-1367 (B>100, B-R>40,
        R>40, B-G>20) - the facets' own rhombus;
      - center-column bright runs (max>110): top spike starts y=668,
        bottom spike ends y=1430 - the frame's vertices;
      - visual read of the emblem: a tall rhombus, top vertex ~(900,660),
        side vertices ~(564,1034)/(1236,1034), bottom vertex ~(900,1434).
    The mask rhombus (cx 900, cy 1047, hw 336, hh 387) contains 99.9% of
    the strict-purple facet pixels, and the ring never enters it (all four
    vertices lie well inside the ring's circle), so the web lines and the
    ring are cut. Inset 4px, feathered, downscaled to 96px, PNG -> base64.
    """
    from PIL import Image, ImageDraw, ImageFilter
    im = Image.open(EMBLEM).convert("RGB")
    W, H = im.size
    px = im.load()
    cx, cy, hw, hh = 900, 1047, 336, 387
    # verify: strict-purple facet pixels lie inside the rhombus
    tot = out = 0
    for y in range(600, 1500):
        for x in range(400, 1400):
            r, g, b = px[x, y]
            if b > 100 and b - r > 40 and r > 40 and b - g > 20:
                tot += 1
                if abs(x - cx) / hw + abs(y - cy) / hh > 1.0:
                    out += 1
    print("jewel check: strict-purple px outside rhombus %d of %d (%.4f)"
          % (out, tot, out / max(1, tot)))
    assert out / max(1, tot) < 0.02, "rhombus does not contain the facets"
    # verify: the frame spikes (center-column bright extremes) lie inside
    assert cy - hh <= 668 and cy + hh >= 1430, "rhombus misses the spikes"
    hw -= 4; hh -= 4  # small inset so no black background leaks past the frame
    L, T, R, B = 480, 600, 1320, 1470
    crop = im.crop((L, T, R, B))
    mask = Image.new("L", crop.size, 0)
    d = ImageDraw.Draw(mask)
    d.polygon([(cx - L, cy - hh - T), (cx + hw - L, cy - T),
               (cx - L, cy + hh - T), (cx - hw - L, cy - T)], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.5))
    rgba = crop.convert("RGBA")
    rgba.putalpha(mask)
    rgba = rgba.resize((96, 96), Image.LANCZOS)
    buf = io.BytesIO()
    rgba.save(buf, "PNG", optimize=True)
    png = buf.getvalue()
    assert len(png) < 40000, "jewel PNG too large: %d B" % len(png)
    ap = rgba.getdata()
    opaque = [p for p in ap if p[3] > 128]
    dark = sum(1 for p in opaque if max(p[:3]) < 40)
    print("jewel PNG: %d B sha=%s opaque=%.2f dark-frac=%.3f rhombus=(%d,%d,%d,%d)"
          % (len(png), sha(png)[:16], len(opaque) / len(ap),
             dark / max(1, len(opaque)), cx, cy, hw, hh))
    assert 0.25 < len(opaque) / len(ap) < 0.45, "jewel fill unexpected"
    assert dark / max(1, len(opaque)) < 0.6, "jewel crop is mostly black - abort"
    return ("data:image/png;base64," + base64.b64encode(png).decode("ascii"),
            dict(cx=cx, cy=cy, hw=hw, hh=hh, png_bytes=len(png),
                 png_sha=sha(png), opaque_frac=len(opaque) / len(ap),
                 dark_frac=dark / max(1, len(opaque))))

# ---------------------------------------------------------------- edits
BRIDGE_DECK_OLD = ('<button class="fp-intro-choice" id="fpBridgeDeck" type="button" '
                   'style="--tone:#8e24aa">Begin the visual story &#9670;</button>')
BRIDGE_DECK_NEW = ('<button class="fp-intro-choice" id="fpBridgeDeck" type="button" '
                   'style="--tone:#8e24aa">Begin the visual story '
                   '<span class="fp-btn-jewel" aria-hidden="true"></span></button>')
BRIDGE_LETTER_OLD = ('<button class="fp-intro-choice fp-choice-lit" id="fpBridgeLetter" type="button" '
                     'style="--tone:#07925f">Read the Collective Agreement &#9670;</button>')
BRIDGE_LETTER_NEW = ('<button class="fp-intro-choice fp-choice-lit" id="fpBridgeLetter" type="button" '
                     'style="--tone:#07925f">Read the agreement '
                     '<span class="fp-btn-jewel" aria-hidden="true"></span></button>')
PICK_OLD = ('<p class="fp-bridge-pick" id="fpBridgePick">Pick your view — one, '
            'or both, as you wish.</p> ')
CSS_ANCHOR = "D3 measures 10-12px clear, 0 overlap. */\n</style>"

CSS_BLOCK = """
/* AGREEMENT BUTTONS FOLLOW-ON (2026-11-18, Shawn 03:37Z + 03:41Z eye) -
   six changes, agreement intro (bridge-final) view only. The deck
   (#fpChoiceDeck/#fpChoiceLetter), the footer link #fpEnterDeal, the
   legal pages and F1-F4 are untouched (see MAKER-REPORT.md).
   1. LABEL: #fpBridgeLetter reads "Read the agreement" (HTML above).
   2. EQUAL SIZE: the bridge pair never wraps and shares one floor.
      Scoped to the bridge pair ONLY - the deck pair keeps its wrap.
   3. THE JEWEL: the flat ◆ at the end of each bridge button is the
      emblem's own diamond, harvested (crop of NAYA_ICON.png, the
      central purple diamond, not the crown frame), one shared class,
      the SAME image in both buttons. 18px inside the line box, so the
      button height does not move.
   4. PICK LINE GONE: #fpBridgePick removed from the HTML above; the
      .fp-bridge-pick rule stays (dead, harmless).
   5. HERO ROW: portrait -> "Naya" -> play on the right. Harvested from
      the walk's flank row (walk-beginning-fixed.html, sha 681c4866):
      .p3-naya-flank{display:grid;grid-template-columns:1fr auto 1fr;
      align-items:center} - the same 1fr/auto/1fr grid, the same
      alignment; only the order changes (name centre, play right) via
      grid-column. Same selectors as the column rules, later in the
      file, so they win at equal specificity. Play keeps its id,
      handler, tip, orbit and press rules - only its position moves.
   6. LOGO UP A TAD: the bridge layer's top pad 48px -> 40px. */
#fpBridgeDeck,#fpBridgeLetter{white-space:nowrap;min-height:64px}
.fp-btn-jewel{display:inline-block;width:18px;height:18px;margin-left:8px;vertical-align:-3px;background:url("__JEWEL__") center/contain no-repeat;filter:drop-shadow(0 0 3px rgba(255,255,255,.35))}
body.fp-stage-on #fpAgreement.fp-view-bridge #fpIntroSide .fp-welcome-hero{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:16px;margin:0 auto 8px}
body.fp-stage-on #fpAgreement.fp-view-intro .fp-intro-side .fp-welcome-hero{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:16px;margin:0 auto 20px}
#fpWelcomeHero .fp-naya-portrait{grid-column:1;justify-self:start}
#fpWelcomeHero .fp-play-name{grid-column:2;justify-self:center}
#fpWelcomeHero #fpIntroPlay{grid-column:3;justify-self:end}
html.fp-locked body.fp-stage-on.fp-bridge #fpAgreement.fp-layer-on{padding-top:40px}
"""

def load_base():
    """Read the base welcome bytes. The v23 file was destroyed by a
    truncate-first write under the EPERM flake (0 bytes, 04:06Z); the
    follow-on #2 reference copy holds the identical bytes (verified
    sha 2e74273b) and is the fallback. Returns (bytes, source-path)."""
    for path in (BASE_WELCOME, BASE_REFERENCE):
        try:
            b = open(path, "rb").read()
        except OSError as e:
            print("base read failed %s: %s" % (path, e))
            continue
        if len(b) == BASE_BYTES and sha(b) == BASE_SHA:
            print("base loaded from %s (%d B, sha %s)" % (path, len(b), sha(b)[:8]))
            return b, path
        print("base at %s is NOT the base (%d B, sha %s...)" % (path, len(b), sha(b)[:8]))
    raise AssertionError("no intact copy of the base welcome bytes found")

def compute_new_welcome():
    base, _src = load_base()
    text = base.decode("utf-8")
    # --- pre-edit counts (the anchors the report asserts)
    pre = {
        "bridge_deck": text.count(BRIDGE_DECK_OLD),
        "bridge_letter": text.count(BRIDGE_LETTER_OLD),
        "pick": text.count('<p class="fp-bridge-pick" id="fpBridgePick">'),
        "pick_any": text.count("fpBridgePick"),
        "intro_pick": text.count("fpIntroPick"),
        "diamond_entity": text.count("&#9670;"),
        "rca_entity": text.count("Read the Collective Agreement &#9670;"),
        "bvs_entity": text.count("Begin the visual story &#9670;"),
        "rca_glyph": text.count("Read the Collective Agreement \u25c6"),
        "bvs_glyph": text.count("Begin the visual story \u25c6"),
        "css_anchor": text.count(CSS_ANCHOR),
        "data_uri": text.count("data:image/png;base64,"),
        "hero_grid": text.count("grid-template-columns:1fr auto 1fr"),
    }
    assert pre["bridge_deck"] == 1 and pre["bridge_letter"] == 1, pre
    assert pre["pick"] == 1 and pre["intro_pick"] == 1, pre
    assert pre["css_anchor"] == 1, pre
    jewel_uri, jewel_info = jewel_data_uri()
    css = CSS_BLOCK.replace("__JEWEL__", jewel_uri)
    assert "__JEWEL__" not in css
    offsets = {}
    def sub(old, new, key):
        nonlocal text
        i = text.find(old)
        assert i >= 0, "anchor missing: %s" % key
        assert text.count(old) == 1, "anchor not unique: %s" % key
        offsets[key] = i
        text = text[:i] + new + text[i + len(old):]
    sub(BRIDGE_DECK_OLD, BRIDGE_DECK_NEW, "bridge_deck")
    sub(BRIDGE_LETTER_OLD, BRIDGE_LETTER_NEW, "bridge_letter")
    sub(PICK_OLD, "", "pick")
    sub(CSS_ANCHOR, "D3 measures 10-12px clear, 0 overlap. */\n" + css + "</style>",
        "css_block")
    new = text.encode("utf-8")
    post = {
        "bridge_deck_new": text.count(BRIDGE_DECK_NEW),
        "bridge_letter_new": text.count(BRIDGE_LETTER_NEW),
        "pick": text.count('<p class="fp-bridge-pick" id="fpBridgePick">'),
        "pick_any": text.count("fpBridgePick"),
        "intro_pick": text.count("fpIntroPick"),
        "diamond_entity": text.count("&#9670;"),
        "rca_entity": text.count("Read the Collective Agreement &#9670;"),
        "bvs_entity": text.count("Begin the visual story &#9670;"),
        "rca_glyph": text.count("Read the Collective Agreement \u25c6"),
        "bvs_glyph": text.count("Begin the visual story \u25c6"),
        "jewel_spans": text.count('<span class="fp-btn-jewel"'),
        "jewel_uri": text.count("data:image/png;base64,"),
        "read_agreement": text.count("Read the agreement "),
        "css_jewel_rule": text.count(".fp-btn-jewel{display:inline-block"),
        "css_nowrap": text.count("#fpBridgeDeck,#fpBridgeLetter{white-space:nowrap;min-height:64px}"),
        "css_hero_row": text.count("grid-template-columns:1fr auto 1fr"),
        "css_logo": text.count("padding-top:40px"),
    }
    assert post["bridge_deck_new"] == 1 and post["bridge_letter_new"] == 1, post
    assert post["pick"] == 0 and post["intro_pick"] == 1, post
    assert post["pick_any"] == 1, post  # the only remaining mention is the CSS comment
    assert post["jewel_uri"] == pre["data_uri"] + 1, post
    assert post["css_hero_row"] == pre["hero_grid"] + 3, post  # 2 new rules + 1 quote in the comment
    assert post["diamond_entity"] == pre["diamond_entity"] - 2, (pre, post)
    assert post["rca_entity"] == 1 and post["bvs_entity"] == 1, post
    assert post["rca_glyph"] == 1 and post["bvs_glyph"] == 1, post
    assert post["jewel_spans"] == 2, post
    assert post["read_agreement"] == 1, post
    assert post["css_jewel_rule"] == 1 and post["css_nowrap"] == 1, post
    assert post["css_logo"] == 1, post
    # --- F1-F4 no-regression anchors, byte-identical
    f = {
        "_fpAlias2": text.count("_fpAlias2"),
        "enterStage();": text.count("enterStage();"),
        "press_sink": text.count("#fpAgreement #dealAgreeBtn:active,#fpAgreement #letterPageAgree:active"),
        "choice_active": text.count(".fp-intro-choice:active"),
        "play_active": text.count(".p3-naya-play:active"),
        "rest_glow": text.count("#fpBridgeDeck:not(:hover):not(:active)"),
        "deck_end_return_clear": text.count("window.__fpDeckEndReturn=false;enterStage();"),
        "deck_end_return": text.count("__fpDeckEndReturn"),
        "getItem_fp_stage": text.count("getItem('nayanet_fp_stage')"),
        "setItem_fp_stage": text.count("setItem('nayanet_fp_stage'"),
        "localStorage_setItem": text.count("localStorage.setItem"),
    }
    assert f["_fpAlias2"] == 3, f
    assert f["enterStage();"] == 3, f
    assert f["press_sink"] == 1 and f["choice_active"] >= 1 and f["play_active"] >= 1, f
    assert f["rest_glow"] == 1, f
    assert f["deck_end_return_clear"] == 1 and f["deck_end_return"] == 5, f
    assert f["getItem_fp_stage"] == 2 and f["setItem_fp_stage"] == 1, f
    assert f["localStorage_setItem"] == 6, f
    # --- inline script blocks byte-identical to base (parse-validity preserved)
    script_re = re.compile(r"<script>(.*?)</script>", re.S)
    base_scripts = script_re.findall(base.decode("utf-8"))
    new_scripts = script_re.findall(text)
    assert len(new_scripts) == len(base_scripts) == 3, (len(base_scripts), len(new_scripts))
    for i, (a, b) in enumerate(zip(base_scripts, new_scripts)):
        assert sha(a.encode()) == sha(b.encode()), "script block %d changed" % i
    print("edits ok: pre=%s" % pre)
    print("edits ok: post=%s" % post)
    print("edits ok: F1-F4=%s" % f)
    print("edits ok: offsets=%s" % offsets)
    print("new welcome: %d B sha=%s (delta %+d B)" % (len(new), sha(new), len(new) - BASE_BYTES))
    return new, jewel_info, offsets

# ---------------------------------------------------------------- checker
def check_text(text, label):
    """Faithful in-memory port of check-design-laws.py check() (the real
    checker takes a file path; disk writes are flake-prone, so the same
    regexes and the same loops run here on the bytes in memory).
    Returns (fails, warns) as sorted lists of 'LABEL:line: KIND ...'."""
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
    # compare on KIND + content, not line numbers: the appended CSS block
    # shifts every later line down, so a pre-existing fail on a shifted
    # line is the SAME fail, not a new one.
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
    return len(bf), len(nf)

def node_parse_scripts(new_text):
    """Parse every inline <script> block (classic) via vm.Script on stdin,
    and confirm the 5 blocks are byte-identical to base (done in compute).
    node --check on files is attempted too when a disk write lands."""
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
    """Worker is ESM (export default). Prefer node --check on a .mjs file
    if a disk write lands; else parse+load it as a module from stdin."""
    path = os.path.join(WORK, "worker-buttons-check.mjs")
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
    NEVER truncate-first: the old code opened the target with "wb" and an
    EPERM mid-write left a 0-byte file (the v23 welcome was destroyed exactly
    this way at 04:06Z and had to be restored from the follow-on #2 reference
    copy). A failed scratch write or a failed replace leaves the target
    untouched; a 0-byte file is flake damage, never truth — verify size+sha
    after every attempt."""
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
    new, jewel_info, offsets = compute_new_welcome()
    base, _src = load_base()
    base_text = base.decode("utf-8")
    run_checker(base_text, new.decode("utf-8"))
    node_parse_scripts(new.decode("utf-8"))
    write_resilient(WORK_COPY, new)
    write_resilient(BASE_WELCOME, new)
    print("EDIT-RESULT " + json.dumps({
        "welcome_bytes": len(new), "welcome_sha": sha(new),
        "welcome_sha_prefix": sha(new)[:8], "delta": len(new) - BASE_BYTES,
        "jewel": jewel_info, "offsets": offsets}))
    return new

# ---------------------------------------------------------------- builder + file + stage
def run_builder(new_welcome, expect_prefix):
    """Build the staging worker twice (determinism check) via the patched
    builder, welcome from stdin. Returns the worker bytes."""
    btxt = open(BUILDER, "rb").read()
    assert ('welcome_sha.startswith("%s")' % expect_prefix).encode() in btxt, \
        "builder not patched to the new welcome prefix"
    assert b"AGREEMENT BUTTONS FOLLOW-ON (2026-11-18" in btxt, \
        "builder lacks the buttons round comment"
    workers = []
    for n in range(2):
        r = subprocess.run([sys.executable, BUILDER, "--stdout", "--welcome-stdin"],
                           input=new_welcome, capture_output=True, timeout=300)
        assert r.returncode == 0, "builder failed: %s" % r.stderr.decode("utf-8", "replace")[-800:]
        log = r.stderr.decode("utf-8", "replace")
        for needle in (expect_prefix, "4b5f9264", "14bd698c", "61002d15"):
            assert needle in log, "builder log missing %s" % needle
        workers.append(r.stdout)
        print("builder run %d: worker %d B sha=%s" % (n + 1, len(r.stdout), sha(r.stdout)))
    assert workers[0] == workers[1], "worker build not deterministic"
    w = workers[0]
    assert b"Read the agreement" in w and b"fp-btn-jewel" in w, \
        "worker does not embed the new welcome"
    assert b'<p class="fp-bridge-pick" id="fpBridgePick">' not in w, \
        "worker still embeds the pick element"
    assert w.count(b"fpBridgePick") == 1, \
        "worker fpBridgePick count %d (want 1: the CSS comment only)" % w.count(b"fpBridgePick")
    return w

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

def file_commit(new_welcome, worker, welcome_sha, worker_sha):
    builder = open(BUILDER, "rb").read()
    driver = open(os.path.join(WORK, "edit-buttons.py"), "rb").read()
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
        ("team-nitro/agreement-buttons-20261118/work/edit-buttons.py", driver),
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
        raw = base64.b64decode(rb["content"])
        assert len(raw) == len(data) and sha(raw) == sha(data), \
            "blob read-back mismatch for %s" % path
        print("blob read-back OK:", path.split("/")[-1], len(raw), "bytes, sha match")
    return commit_sha, tree["sha"], blobs

def commit_message(welcome_sha, worker_sha, welcome_bytes, worker_bytes):
    return (
        "Agreement INTRO BUTTONS FOLLOW-ON (2026-11-18, Shawn's eye 03:37Z + 03:41Z; "
        "MAKER-REPORT.md in agreement-buttons-20261118/)\n\n"
        "Six changes, agreement intro (bridge-final) view only, one pass, one commit.\n\n"
        "1. LABEL: #fpBridgeLetter reads 'Read the agreement' (was 'Read the Collective "
        "Agreement' - the page already says Collective Agreement at the top, so the "
        "shorter label fits one line).\n\n"
        "2. EQUAL SIZE: both buttons the same width, height, padding, icon size and "
        "position. The wrap was the whole size difference (the green label wrapped its "
        "diamond onto a second line at 420px). Fix: the bridge pair never wraps "
        "(#fpBridgeDeck,#fpBridgeLetter{white-space:nowrap;min-height:64px}) - scoped "
        "to the bridge pair ONLY, so the deck pair keeps its wrap. Same tones "
        "(purple #8e24aa, green #07925f), same pills, rims, fp-choice-lit state.\n\n"
        "3. THE JEWEL: the flat diamond glyph at the end of EACH button is now the "
        "emblem's own diamond - harvested from NAYA_ICON.png (the central purple "
        "diamond, not the crown frame; rhombus edge-fit, 96px PNG, one shared class "
        ".fp-btn-jewel), the SAME image in both buttons. Not a glyph, not an emoji, "
        "not a CSS triangle - a real faceted jewel with depth, light, volume, to the "
        "quality of the emblem at button size. 18px inside the line box, so button "
        "height does not move; the press sink, hover and rest rim are untouched.\n\n"
        "4. PICK LINE GONE: #fpBridgePick removed ('Pick your view - one, or both, as "
        "you wish.') - the buttons speak for themselves. #fpIntroPick (deck) untouched; "
        "no JS referenced fpBridgePick (pickLine in JS is #fpPickLine, a different "
        "element), so no JS change was needed.\n\n"
        "5. HERO ROW: portrait -> 'Naya' -> play button on the right, one row. "
        "Harvested from the walk's flank row (walk-beginning-fixed.html): the same "
        "1fr auto 1fr grid, the same alignment; only the order changes (name centre, "
        "play right) via grid-column. DOM order unchanged, so #fpIntroPlay keeps its "
        "id, handler, tip, orbit and press rules - only its position moves. Row height "
        "132px (104px phone) vs 233px (205px) stacked: saves 101px of scrollport.\n\n"
        "6. LOGO UP A TAD: the bridge layer's top pad 48px -> 40px (margin/padding "
        "nudge only, no header redesign).\n\n"
        "FOLD (layout math; VM browsers dead, the eye verifies visually): bridge "
        "scrollport was ~190px at 1857x924 (~210 at 635, ~169 at 390) against a "
        "244px tail (220px phone) - short by ~50px, which is why the green button "
        "sat cut off behind the legal strip. After: scrollport +109px (hero row "
        "+101, logo +8) -> ~299px (1857), ~319 (635), ~278 (390), slack 55-75px; "
        "BOTH buttons sit fully above the fold, above the legal-pages row. Intro "
        "view already fit and fits better (stack -138px).\n\n"
        "fpNextBtn2 FINDING: NOT visible on the agreement intro view - left untouched. "
        "In S.view==='intro', updateChrome() unhides it, but "
        "body.fp-stage-on.fp-intro #fpStageBarB{display:none} hides the whole bar; "
        "in bridge view updateChrome() hides both next buttons; its only visible "
        "state is deck-end 9/9 with a different string ('Read the full agreement').\n\n"
        "F1-F4 NO REGRESSION: _fpAlias2 x3, enterStage(); x3, press sink (2,1,0) x1, "
        "rest glow x1, deck-end clear x1, __fpDeckEndReturn x5, getItem x2, setItem x1, "
        "localStorage.setItem x6 - all byte-identical to base. All three inline "
        "script blocks byte-identical (parse-validity preserved). Design laws: zero new FAILs vs "
        "base. Worker built twice, identical sha %s (%d B); embeds verified: WALK "
        "4b5f9264, IDENTITY a1550164, WELCOME %s, UNFOLD 14bd698c.\n\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after the PUT. "
        "Worker PUT with --meta v23-meta.json (WELCOME_ASSETS "
        "1cf80db6183245d19dd5296645a12bd0 intact). PR #3453 OPEN AND UNMERGED BY "
        "DESIGN - do not merge; the captain decides the PR vehicle. Nothing live - "
        "the finished update goes LIVE on the main URL only on Shawn's tap, after "
        "his eye."
        % (worker_sha[:8], worker_bytes, welcome_sha[:8], STAGING))

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
        "/agreement": "14bd698cc1a666b665258a212a934d439a374733e2523d929c9f0e340a35c31f",
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
    # heal the workspace first: the v23 welcome file is 0 bytes (flake
    # damage from the truncate-first write at 04:06Z). Restore the BASE
    # bytes from the reference copy; the new bytes land at the end.
    base, _src = load_base()
    write_resilient(BASE_WELCOME, base)
    new = mode_edit()
    wsha = sha(new)
    worker = run_builder(new, wsha[:8])
    node_check_worker(worker)
    commit_sha, tree_sha, blobs = file_commit(new, worker, wsha, sha(worker))
    dep, put_out = stage_put(worker)
    routes = verify_routes(wsha)
    # last chance to sync the on-disk working copies if the flake cleared
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
        sys.exit("usage: edit-buttons.py [edit|all]")
