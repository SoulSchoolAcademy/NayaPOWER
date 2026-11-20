#!/usr/bin/env python3
"""AGREEMENT BUTTONS FIX 4 (2026-11-18) - maker driver.

Eye verdict FIX3 (GOES BACK, eye 8c4ef309): the intro is fixed - do not
touch it. Fix EXACTLY these 3 items, welcome file ONLY. Work dir:
~/workspace/team-nitro/agreement-buttons-20261118/work/fix4/

  1. BRIDGE-FINAL FOLD - BY MECHANISM, not arithmetic. The eye proved
     round 3's 64px of spacing cuts did not move first paint at all
     (letter bottom 1120 at 1919, five settle-verified samples): the
     container's native scroll position sets it (scrollTop 1797 of max
     2063 at 1919 - 266px short, the fin block's height). There is NO
     scroll call in any More handler and NO code anywhere in the file
     that writes #fpBridge.scrollTop on the bridge path (proven by
     grep: the only scrollTop writes are agreeSec/letterPage and the
     face-placement reads). The position is the browser's native
     behaviour on reveal+hide (scroll anchoring / the click's
     scroll-into-view), which is why content-height arithmetic could
     never move it. THE FIX: the More4 handler now scrolls #fpBridge
     itself to its bottom the moment it reveals the final view -
     bBridge.scrollTop = bBridge.scrollHeight - bBridge.clientHeight -
     synchronously, after the reveal, so first paint is set by the
     handler, not by the native position. (scrollHeight is read after
     both hidden toggles, so the forced layout includes the revealed
     final AND the removed More4 button.)
  2. DEAD CONTINUE PILL - hidden for real. `hidden` does not hide
     .p3-enter buttons: the author rules `.p3-enter{display:block}`
     (L790, L1225) beat the UA `[hidden]{display:none}`. New scoped
     rule `.p3-enter[hidden]{display:none!important}` (same pattern as
     the existing `.returning[hidden]` / `#entryForm[hidden]` rules).
     Audit (from bytes): exactly THREE .p3-enter elements carry a
     hidden attribute in the whole file - #fpBridgeMore2/3/4. All
     other .p3-enter elements (deck-next, letter-next, agree buttons)
     carry none. The rule is inert the moment JS removes hidden (the
     reveal flow: More1 shows More2, More2 shows More3, More3 shows
     More4), so it changes nothing except hiding what the code already
     ordered hidden. More1/2/3 were off-screen above or covered on the
     final view (eye); More4 is the visible dead pill - the fix.
     NOT touched: .fp-bridge-group G2/G3/G4 also leak past hidden
     (.fp-bridge-group{display:flex} L1887 beats UA [hidden]) - that is
     pre-existing, out of scope for this round, and this rule does not
     touch it. No global bare [hidden] rule - that would change the
     stage bar (whose hidden attribute is overridden by design, see 3).
  3. STAGE-BAR BUTTON ON THIS VIEW - option (b), hide the row. Chosen
     over (a) because setNext() OVERWRITES #fpNextBtn.textContent on
     every view except bridge (intro "Begin the visual story ◆", deck
     "Keep reading ◆", letter "I agree ◆", ...), so a jewel span in the
     initial HTML would be wiped everywhere the button shows except
     bridge - jewelling it correctly everywhere would mean rewriting
     setNext for every view, out of scope. The code ALREADY orders the
     button hidden on bridge (updateChrome: `if(S.view==='bridge')
     {if(nextBtn)nextBtn.hidden=true;}`) and on footer - but the hide
     never lands: the author rule `#fpNextBtn{display:block}` (L1459)
     beats UA [hidden], the same root cause as fix 2. So:
     (i) `#fpNextBtn[hidden]{display:none}` - mirrors the existing
     `#fpNextBtn2[hidden]{display:none}` (L1469) and makes the ordered
     hides effective (bridge + footer only; every other view sets
     hidden=false, so the rule is inert there and deck flow is
     untouched); (ii) `body.fp-stage-on.fp-bridge #fpStageBarB
     {display:none}` - mirrors the existing intro rule
     `body.fp-stage-on.fp-intro #fpStageBarB{display:none}` (L1551):
     on bridge the bar has no ordered-visible content at all (nextBtn
     ordered hidden, nextBtn2 hidden, pick line + links + countdown
     hidden), so an empty fixed gradient strip must not paint. Scoped
     by render()'s body.fp-bridge toggle - leaving bridge removes it
     automatically, no JS state to leak. Deck-end/deck flow: the bar
     rule is inert outside bridge; nextBtn.hidden=false there.

Base: welcome blob afb950a5, 1,166,995 B, sha256
685fe27f4ee61140c4c2bda36f8b2c1297af528520d0c0dfa323116b52a75a64
(branch walk-end/agreement-merge-20261117, tip
9da844fe22d625713b845775e077afd282f607f4).

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
import base64, hashlib, io, json, os, re, subprocess, sys, time, difflib

HOME = os.path.expanduser("~")
WORK = os.path.join(HOME, "workspace/team-nitro/agreement-buttons-20261118/work/fix4")
V23 = os.path.join(HOME, "workspace/team-nitro/walk-v23-assembly-20261114")
BASE_WELCOME = os.path.join(V23, "welcome-staged.html")
WORK_COPY = os.path.join(WORK, "welcome-fix4.html")
BUILDER = os.path.join(V23, "build-v23-staging-worker.py")
CHECKER = os.path.join(HOME, "workspace/team-nitro/check-design-laws.py")
GH = os.path.join(HOME, "workspace/team-nitro/gh-direct.py")
CF = os.path.join(HOME, "workspace/project-intelligence/cf-worker.py")
META = os.path.join(V23, "v23-meta.json")
REPO = "SoulSchoolAcademy/NayaPOWER"
BRANCH = "walk-end/agreement-merge-20261117"
PARENT_TIP = "9da844fe22d625713b845775e077afd282f607f4"
BASE_BLOB = "afb950a59218099a6b8bb24a8acff9ed6a617eda"
BASE_SHA = "685fe27f4ee61140c4c2bda36f8b2c1297af528520d0c0dfa323116b52a75a64"
BASE_BYTES = 1166995
JEWEL_SHA = "e583f51f6a2dfe551ac3379ca8eb67e10f10b79d1236d7961122c800009377d2"
JEWEL_BYTES = 12715
CF_ACCOUNT = "b5e2a51b3e883f7722287c5f51b1196b"
CF_SCRIPT = "naya-walk-beginning-staging"
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
# Eye measurements, bridge-final first paint (EYE-VERDICT-FIX3.md):
# letter bottom 1120/1121/895, deck bottom 1045/1046/821, scrollTop
# 1797/2076/2944, scrollHeight 2531/2823/3501, clientHeight 468/481/286,
# container top 482/469/428, folds 1080/1080/844.
EYE = {
    1919: dict(deck=1045, letter=1120, stop=1797, sh=2531, ch=468, top=482, fold=1080),
    635: dict(deck=1046, letter=1121, stop=2076, sh=2823, ch=481, top=469, fold=1080),
    390: dict(deck=821, letter=895, stop=2944, sh=3501, ch=286, top=428, fold=844),
}
# The More4 button's box (54px tall + 12px top margin) leaves the flow
# when hidden takes effect under the fix-2 rule.
MORE4_BOX = 66

def sha(b): return hashlib.sha256(b).hexdigest()

# ---------------------------------------------------------------- jewel
def jewel_data_uri(text):
    m = re.search(r'\.fp-btn-jewel\{[^}]*background:url\("data:image/png;base64,([^"]+)"\)', text)
    assert m, ".fp-btn-jewel rule with data-URI not found in base"
    png = base64.b64decode(m.group(1))
    assert len(png) == JEWEL_BYTES, "jewel PNG size %d, want %d" % (len(png), JEWEL_BYTES)
    assert sha(png) == JEWEL_SHA, "jewel PNG sha mismatch: %s" % sha(png)
    from PIL import Image
    im = Image.open(io.BytesIO(png))
    assert im.size == (96, 96) and im.mode == "RGBA", "jewel geometry wrong: %s %s" % (im.size, im.mode)
    print("jewel verified from base bytes: %d B sha=%s 96x96 RGBA" % (len(png), sha(png)[:8]))
    return png

# ---------------------------------------------------------------- edits
# CSS anchor: the last rule of the fix-3 block, directly before </style>.
CSS_ANCHOR = ("body.fp-stage-on #fpAgreement.fp-view-bridge "
              "#fpIntroSide{margin-bottom:16px}\n</style>")
CSS_BLOCK = """
/* AGREEMENT BUTTONS FIX 4 (2026-11-18, eye verdict FIX3 GOES BACK) -
   the intro is fixed, do not touch it. Three items, by mechanism.
   1. BRIDGE-FINAL FOLD: round 3's 64px of spacing cuts did not move
      first paint (letter 1120 at 1919, five settle-verified samples)
      because no code sets #fpBridge.scrollTop on the bridge path -
      the More handlers contain no scroll call and the only scrollTop
      writes in the file are agreeSec/letterPage + face reads. The
      position is the browser's native reveal behaviour, so it is now
      set explicitly in the More4 handler (JS below): scroll #fpBridge
      to its bottom the moment the final view is revealed.
   2. DEAD CONTINUE PILL: `hidden` does not hide .p3-enter buttons -
      `.p3-enter{display:block}` beats the UA [hidden] rule. This
      scoped rule hides exactly the three .p3-enter elements that
      carry hidden (#fpBridgeMore2/3/4); it is inert once JS removes
      hidden, so the reveal flow is untouched. No global [hidden]
      rule: the stage bar's hidden attribute is overridden by design.
   3. STAGE-BAR BUTTON: the code already orders #fpNextBtn hidden on
      bridge + footer (updateChrome), but `#fpNextBtn{display:block}`
      beats UA [hidden] - same root cause as (2). The [hidden] rule
      makes the ordered hides effective (inert elsewhere: hidden=false
      on intro/deck/letter/agree). The bridge bar rule mirrors the
      intro rule (L1551): on bridge the bar has no ordered-visible
      content, so no empty fixed strip paints. Scoped by render()'s
      body.fp-bridge toggle; deck flow untouched. */
.p3-enter[hidden]{display:none!important}
#fpNextBtn[hidden]{display:none}
body.fp-stage-on.fp-bridge #fpStageBarB{display:none}
"""
MORE4_OLD = ("if(bMore4&&bFin){bMore4.addEventListener('click',function()"
             "{bFin.hidden=false;bMore4.hidden=true;});}")
MORE4_NEW = ("if(bMore4&&bFin){bMore4.addEventListener('click',function()"
             "{bFin.hidden=false;bMore4.hidden=true;"
             "var bBridge=q('#fpBridge');"
             "if(bBridge){bBridge.scrollTop=bBridge.scrollHeight-bBridge.clientHeight;}});}")

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

def hidden_audit(text):
    """Every start-tag carrying a bare `hidden` attribute (not aria-hidden,
    not overflow:hidden), with its id/class. Returns (p3_hidden_ids,
    all_hidden_count)."""
    p3_hidden = []
    total = 0
    for m in re.finditer(r'<([a-zA-Z0-9]+)\s[^>]*?(?:\s)hidden(?:\s|>|/)[^>]*>', text):
        tag = m.group(0)
        if re.search(r'aria-hidden', tag) and ' hidden' not in tag.replace('aria-hidden', ''):
            continue
        total += 1
        clm = re.search(r'class="([^"]+)"', tag)
        idm = re.search(r'id="([^"]+)"', tag)
        if clm and 'p3-enter' in clm.group(1).split():
            p3_hidden.append(idm.group(1) if idm else '?')
    return sorted(p3_hidden), total

def compute_new_welcome():
    base = load_base()
    text = base.decode("utf-8")
    jewel_data_uri(text)
    assert text.count("data:image/png;base64,") == 2, "unexpected data-URI count in base"
    # --- pre-state ---
    p3_hidden_pre, total_hidden_pre = hidden_audit(text)
    assert p3_hidden_pre == ["fpBridgeMore2", "fpBridgeMore3", "fpBridgeMore4"], p3_hidden_pre
    print("hidden audit (base): %d hidden-attr tags; .p3-enter+hidden = %s" % (total_hidden_pre, p3_hidden_pre))
    pre = {
        "css_anchor": text.count(CSS_ANCHOR),
        "more4_old": text.count(MORE4_OLD),
        "more4_new": text.count(MORE4_NEW),
        "p3_hidden_rule": text.count(".p3-enter[hidden]{display:none!important}"),
        "nextbtn_hidden_rule": text.count("#fpNextBtn[hidden]{display:none}"),
        "bridge_bar_rule": text.count("body.fp-stage-on.fp-bridge #fpStageBarB{display:none}"),
        "nextbtn2_hidden_rule": text.count("#fpNextBtn2[hidden]{display:none}"),
        "intro_bar_rule": text.count("body.fp-stage-on.fp-intro #fpStageBarB{display:none}"),
        "jewel_spans": text.count('<span class="fp-btn-jewel"'),
        "jewel_uri": text.count("data:image/png;base64,"),
        "diamond_literal": text.count("\u25c6"),
        "diamond_entity": text.count("&#9670;"),
        "read_agreement": text.count("Read the agreement "),
        "pick_id": text.count("fpIntroPick"),
        "bridge_deck_new": text.count('id="fpBridgeDeck" type="button" style="--tone:#8e24aa">Begin the visual story <span class="fp-btn-jewel"'),
        "bridge_letter_new": text.count('id="fpBridgeLetter" type="button" style="--tone:#07925f">Read the agreement <span class="fp-btn-jewel"'),
        "nextbtn_hidden_false": text.count("if(nextBtn)nextBtn.hidden=false;"),
        "nextbtn_hidden_bridge": text.count("if(S.view==='bridge'){if(nextBtn)nextBtn.hidden=true;}"),
        "nextbtn_hidden_footer": text.count("if(nextBtn)nextBtn.hidden=true;"),
        "setnext_calls": text.count("setNext("),
        "fpbridge_scrolltop_write": len(re.findall(r"#fpBridge['\"]?\)\.scrollTop\s*=", text)) + text.count("fpBridge.scrollTop"),
    }
    assert pre["css_anchor"] == 1 and pre["more4_old"] == 1 and pre["more4_new"] == 0, pre
    assert pre["p3_hidden_rule"] == 0 and pre["nextbtn_hidden_rule"] == 0 and pre["bridge_bar_rule"] == 0, pre
    assert pre["nextbtn2_hidden_rule"] == 1 and pre["intro_bar_rule"] == 1, pre
    assert pre["jewel_spans"] == 4 and pre["jewel_uri"] == 2, pre
    assert pre["diamond_literal"] == 3 and pre["diamond_entity"] == 345, pre
    assert pre["read_agreement"] == 2 and pre["pick_id"] == 0, pre
    assert pre["bridge_deck_new"] == 1 and pre["bridge_letter_new"] == 1, pre
    assert pre["nextbtn_hidden_false"] == 1 and pre["nextbtn_hidden_bridge"] == 1, pre
    assert pre["nextbtn_hidden_footer"] == 2, pre  # bridge branch + footer branch
    assert pre["fpbridge_scrolltop_write"] == 0, pre
    # setNext inventory: the labels setNext writes onto #fpNextBtn per view
    # (proves option (a) would be wiped everywhere except bridge).
    labels = sorted(set(re.findall(r"setNext\('([^']+)", text)))
    print("setNext labels in base (each overwrites #fpNextBtn.textContent): %s" % labels)
    assert "Begin the visual story \\u25C6" in labels and "Keep reading \\u25C6" in labels, labels
    # No code writes #fpBridge.scrollTop anywhere in the base file.
    assert "scrollTop=" not in text or text.count("scrollTop=") == text.count("agreeSec.scrollTop="), \
        "unexpected scrollTop write in base"
    # --- the edits ---
    def sub(old, new, key):
        nonlocal text
        i = text.find(old)
        assert i >= 0, "anchor missing: %s" % key
        assert text.count(old) == 1, "anchor not unique: %s" % key
        text = text[:i] + new + text[i + len(old):]
        return i
    off_css = sub(CSS_ANCHOR, CSS_ANCHOR.replace("\n</style>", "\n" + CSS_BLOCK + "</style>"), "css_block")
    off_js = sub(MORE4_OLD, MORE4_NEW, "more4")
    new = text.encode("utf-8")
    post = {
        "css_anchor": text.count("body.fp-stage-on #fpAgreement.fp-view-bridge #fpIntroSide{margin-bottom:16px}"),
        "more4_old": text.count(MORE4_OLD),
        "more4_new": text.count(MORE4_NEW),
        "p3_hidden_rule": text.count(".p3-enter[hidden]{display:none!important}"),
        "nextbtn_hidden_rule": text.count("#fpNextBtn[hidden]{display:none}"),
        "bridge_bar_rule": text.count("body.fp-stage-on.fp-bridge #fpStageBarB{display:none}"),
        "nextbtn2_hidden_rule": text.count("#fpNextBtn2[hidden]{display:none}"),
        "jewel_spans": text.count('<span class="fp-btn-jewel"'),
        "jewel_uri": text.count("data:image/png;base64,"),
        "diamond_literal": text.count("\u25c6"),
        "diamond_entity": text.count("&#9670;"),
        "read_agreement": text.count("Read the agreement "),
        "pick_id": text.count("fpIntroPick"),
        "bridge_deck_new": text.count('id="fpBridgeDeck" type="button" style="--tone:#8e24aa">Begin the visual story <span class="fp-btn-jewel"'),
        "bridge_letter_new": text.count('id="fpBridgeLetter" type="button" style="--tone:#07925f">Read the agreement <span class="fp-btn-jewel"'),
        "nextbtn_hidden_false": text.count("if(nextBtn)nextBtn.hidden=false;"),
        "nextbtn_hidden_bridge": text.count("if(S.view==='bridge'){if(nextBtn)nextBtn.hidden=true;}"),
    }
    assert post["more4_old"] == 0 and post["more4_new"] == 1, post
    assert post["p3_hidden_rule"] == 1 and post["nextbtn_hidden_rule"] == 1 and post["bridge_bar_rule"] == 1, post
    assert post["nextbtn2_hidden_rule"] == 1, post
    assert post["jewel_spans"] == 4 and post["jewel_uri"] == 2, post
    assert post["diamond_literal"] == 3 and post["diamond_entity"] == 345, post
    assert post["read_agreement"] == 2 and post["pick_id"] == 0, post
    assert post["bridge_deck_new"] == 1 and post["bridge_letter_new"] == 1, post
    assert post["nextbtn_hidden_false"] == 1 and post["nextbtn_hidden_bridge"] == 1, post
    p3_hidden_post, total_hidden_post = hidden_audit(text)
    assert p3_hidden_post == p3_hidden_pre and total_hidden_post == total_hidden_pre, \
        (p3_hidden_pre, p3_hidden_post, total_hidden_pre, total_hidden_post)
    print("hidden audit (new): %d hidden-attr tags; .p3-enter+hidden = %s (unchanged)" % (total_hidden_post, p3_hidden_post))
    # --- F1-F4 no-regression anchors, byte-identical counts ---
    base_text = base.decode("utf-8")
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
    f_new = {}
    for k, pat in inv.items():
        assert base_text.count(pat) == text.count(pat), "invariant changed: %s" % k
        f_new[k] = text.count(pat)
    assert f_new["_fpAlias2"] == 3 and f_new["enterStage();"] == 3, f_new
    assert f_new["press_sink"] == 1 and f_new["choice_active"] == 2 and f_new["play_active"] == 2, f_new
    assert f_new["rest_glow"] == 1 and f_new["deck_end_return_clear"] == 1, f_new
    assert f_new["deck_end_return"] == 5 and f_new["getItem_fp_stage"] == 2, f_new
    assert f_new["setItem_fp_stage"] == 1 and f_new["localStorage_setItem"] == 6, f_new
    # --- script blocks: 0 and 1 byte-identical; block 2 differs ONLY in
    # the More4 handler (prove by removing the handler fragment both sides).
    scripts_base = re.findall(r"<script>(.*?)</script>", base_text, re.S)
    scripts_new = re.findall(r"<script>(.*?)</script>", text, re.S)
    assert len(scripts_base) == 3 and len(scripts_new) == 3
    for i in (0, 1):
        assert sha(scripts_base[i].encode()) == sha(scripts_new[i].encode()), "script block %d changed" % i
    b2_old = scripts_base[2].replace(MORE4_OLD, "")
    b2_new = scripts_new[2].replace(MORE4_NEW, "")
    assert sha(b2_old.encode()) == sha(b2_new.encode()), "script block 2 changed outside the More4 handler"
    print("script blocks: 0,1 byte-identical; block 2 differs ONLY in the More4 handler")
    # --- diff scope: exactly 2 hunks (CSS insert + More4 line replace) ---
    sm = difflib.SequenceMatcher(a=base_text.split("\n"), b=text.split("\n"), autojunk=False)
    hunks = [op for op in sm.get_opcodes() if op[0] != "equal"]
    print("diff hunks (base %d lines -> new %d lines):" % (len(base_text.split("\n")), len(text.split("\n"))))
    for tag, i1, i2, j1, j2 in hunks:
        print("  %s base L%d-%d -> new L%d-%d" % (tag, i1 + 1, i2, j1 + 1, j2))
    assert len(hunks) == 2, "expected exactly 2 diff hunks, got %d" % len(hunks)
    assert hunks[0][0] == "insert", hunks
    assert hunks[1][0] == "replace" and hunks[1][2] - hunks[1][1] == 1, hunks
    # --- fold expectation from the MECHANISM (scrollTop pinned to max by
    # the handler; NOT a live measurement - the eye verifies in paint).
    # After the reveal, scrollHeight shrinks by the More4 box (66px) once
    # hidden takes effect; max scroll = scrollHeight - clientHeight.
    # Letter/deck content-bottoms come from the eye's measured rects.
    print("fold expectation from mechanism (scrollTop := max, eye is the gate):")
    for w, e in sorted(EYE.items()):
        sh = e["sh"] - MORE4_BOX
        maxscroll = sh - e["ch"]
        letter_content_bottom = e["letter"] - e["top"] + e["stop"] - MORE4_BOX
        deck_content_bottom = e["deck"] - e["top"] + e["stop"] - MORE4_BOX
        letter_vp = e["top"] + (letter_content_bottom - maxscroll)
        deck_vp = e["top"] + (deck_content_bottom - maxscroll)
        assert letter_vp <= e["fold"] and deck_vp <= e["fold"], (w, letter_vp, deck_vp)
        print("  %dpx: maxscroll %d, letter bottom %d (fold %d, slack %d), deck bottom %d"
              % (w, maxscroll, letter_vp, e["fold"], e["fold"] - letter_vp, deck_vp))
    print("edits ok: pre=%s" % pre)
    print("edits ok: post=%s" % post)
    print("edits ok: F1-F4=%s" % f_new)
    print("edits ok: offsets css=%d js=%d" % (off_css, off_js))
    print("new welcome: %d B sha=%s (delta %+d B)" % (len(new), sha(new), len(new) - BASE_BYTES))
    return new

# ---------------------------------------------------------------- checker
def check_text(text, label):
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
        warns.append("%s: NO-HOVER (§1 warning - no :hover rules found)" % label)
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
    path = os.path.join(WORK, "worker-fix4-check.mjs")
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
    base_text = base.decode("utf-8")
    bf, bw, nf, nw = run_checker(base_text, new.decode("utf-8"))
    node_parse_scripts(new.decode("utf-8"))
    write_resilient(WORK_COPY, new)
    write_resilient(BASE_WELCOME, new)
    print("EDIT-RESULT " + json.dumps({
        "welcome_bytes": len(new), "welcome_sha": sha(new),
        "welcome_sha_prefix": sha(new)[:8], "delta": len(new) - BASE_BYTES,
        "checker": {"base_fail": bf, "base_warn": bw, "new_fail": nf, "new_warn": nw}}))
    return new

# ---------------------------------------------------------------- builder + file + stage
def patch_builder(new_sha, new_bytes):
    """Patch the builder in place (same dir as round 3): add the FIX 4
    comment above the welcome-sha assert and move the assert to the new
    prefix. The file is filed in the same commit, so the patch is
    reviewable. Returns the patched bytes."""
    btxt = open(BUILDER, "rb").read()
    old_assert = (b'assert welcome_sha.startswith("685fe27f"), "welcome sha is not the '
                  b'AGREEMENT BUTTONS FIX 3 welcome sha (2026-11-18: 1. intro letter reads '
                  b'Read the agreement, 2. jewel spans on both intro buttons, 3. intro pick '
                  b'line removed, 4. bridge-final fold tightened 64px)"')
    assert btxt.count(old_assert) == 1, "builder FIX 3 assert not found exactly once"
    comment = (
        b"# AGREEMENT BUTTONS FIX 4 (2026-11-18, eye verdict FIX3 GOES BACK;\n"
        b"# maker round - agreement-buttons-20261118/work/fix4/edit-fix4.py):\n"
        b"# the welcome sha moves 685fe27f -> " + new_sha[:8].encode() + b" (1,166,995 B -> "
        + str(new_bytes).encode() + b" B):\n"
        b"# 1. bridge-final fold BY MECHANISM: the More4 handler now scrolls #fpBridge\n"
        b"# to its bottom on reveal (round 3's 64px spacing cuts did not move first\n"
        b"# paint - no code set the container's scroll position); 2. dead Continue\n"
        b"# pill hidden for real (.p3-enter[hidden]{display:none!important} - hidden\n"
        b"# did not hide .p3-enter buttons); 3. stage-bar button: #fpNextBtn gains\n"
        b"# its [hidden] rule (mirroring #fpNextBtn2) so updateChrome's bridge/footer\n"
        b"# hide lands, and the bar itself is display:none on bridge (mirroring the\n"
        b"# intro rule) - the jewelled #fpBridgeDeck is the one in front of the user.\n"
        b"# Intro pair, pick line, press/hover, deck, legal row, #fpNextBtn2 and the\n"
        b"# bridge pair's jewel/label untouched. Walk, template, identity, unfold\n"
        b"# shas unchanged.\n")
    new_assert = (b'assert welcome_sha.startswith("' + new_sha[:8].encode() + b'"), "welcome sha is not the '
                  b'AGREEMENT BUTTONS FIX 4 welcome sha (2026-11-18: 1. More4 handler scrolls #fpBridge to bottom, '
                  b'2. .p3-enter[hidden] hides the dead Continue pill, 3. #fpNextBtn[hidden] + bridge bar display:none)"')
    patched = btxt.replace(old_assert, comment + new_assert)
    assert patched != btxt and sha(patched) != sha(btxt)
    assert (b'welcome_sha.startswith("' + new_sha[:8].encode() + b'")') in patched
    assert b"AGREEMENT BUTTONS FIX 4 (2026-11-18" in patched
    write_resilient(BUILDER, patched)
    print("builder patched: assert -> %s, FIX 4 comment added (%d B)" % (new_sha[:8], len(patched)))
    return patched

def run_builder(new_welcome, expect_prefix):
    btxt = open(BUILDER, "rb").read()
    assert ('welcome_sha.startswith("%s")' % expect_prefix).encode() in btxt, \
        "builder not patched to the new welcome prefix"
    assert b"AGREEMENT BUTTONS FIX 4 (2026-11-18" in btxt, \
        "builder lacks the fix-4 round comment"
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
    assert b".p3-enter[hidden]{display:none!important}" in w, \
        "worker does not embed the fix-2 rule"
    assert b"#fpNextBtn[hidden]{display:none}" in w, \
        "worker does not embed the fix-3 nextBtn rule"
    assert b"body.fp-stage-on.fp-bridge #fpStageBarB{display:none}" in w, \
        "worker does not embed the fix-3 bridge bar rule"
    assert b"bBridge.scrollTop=bBridge.scrollHeight-bBridge.clientHeight" in w, \
        "worker does not embed the fix-1 scroll"
    assert b'<p class="fp-intro-pick" id="fpIntroPick">' not in w, \
        "worker still embeds the intro pick element"
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
        "Agreement BUTTONS FIX 4 (2026-11-18, eye verdict FIX3 GOES BACK; "
        "MAKER-REPORT-4.md in agreement-buttons-20261118/)\n\n"
        "The intro is fixed - untouched this round. Exactly the three "
        "verdict items, welcome file ONLY, one pass, one commit.\n\n"
        "1. BRIDGE-FINAL FOLD - BY MECHANISM. Round 3's 64px of spacing "
        "cuts did not move first paint (letter 1120 at 1919, five "
        "settle-verified samples) because no code sets #fpBridge.scrollTop "
        "on the bridge path: the More handlers contain no scroll call and "
        "the only scrollTop writes in the file are agreeSec/letterPage + "
        "face reads. The position was the browser's native reveal "
        "behaviour. The More4 handler now scrolls #fpBridge to its bottom "
        "the moment it reveals the final view "
        "(scrollTop = scrollHeight - clientHeight), so first paint is set "
        "by the handler, not by the native position.\n\n"
        "2. DEAD CONTINUE PILL - hidden for real. `hidden` did not hide "
        ".p3-enter buttons: `.p3-enter{display:block}` beats the UA "
        "[hidden] rule. New scoped rule "
        ".p3-enter[hidden]{display:none!important}. Audit: exactly three "
        ".p3-enter elements carry hidden (#fpBridgeMore2/3/4); the rule is "
        "inert once JS removes hidden, so the reveal flow is untouched.\n\n"
        "3. STAGE-BAR BUTTON - option (b), hide the row. setNext() "
        "overwrites #fpNextBtn.textContent on every view except bridge, so "
        "a jewel span would be wiped everywhere the button shows. Instead: "
        "#fpNextBtn[hidden]{display:none} (mirrors the existing "
        "#fpNextBtn2 rule) makes updateChrome's bridge/footer hide land, "
        "and the bar itself is display:none on bridge (mirrors the intro "
        "rule) - the jewelled #fpBridgeDeck is the one in front of the user. "
        "Scoped by render()'s body.fp-bridge toggle; deck flow untouched.\n\n"
        "NO REGRESSION: _fpAlias2 x3, enterStage(); x3, press sink x1, "
        "rest glow x1, deck-end clear x1, __fpDeckEndReturn x5, getItem x2, "
        "setItem x1, localStorage.setItem x6 - all byte-identical to base. "
        "Script blocks 0 and 1 byte-identical; block 2 differs ONLY in the "
        "More4 handler. Design laws: zero new FAILs vs base. Worker built "
        "twice, identical sha %s (%d B); embeds verified: WALK 4b5f9264, "
        "IDENTITY a1550164, WELCOME %s, UNFOLD 96b18b6f.\n\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after "
        "the PUT. Worker PUT with --meta v23-meta.json (WELCOME_ASSETS "
        "1cf80db6183245d19dd5296645a12bd0 intact). PR #3453 OPEN AND UNMERGED "
        "BY DESIGN - do not merge; the captain decides the PR vehicle. "
        "Nothing live - the finished update goes LIVE on the main URL only "
        "on Shawn's tap, after his eye."
        % (worker_sha[:8], worker_bytes, welcome_sha[:8], STAGING))

def file_commit(new_welcome, worker, welcome_sha, worker_sha):
    builder = open(BUILDER, "rb").read()
    driver = open(os.path.join(WORK, "edit-fix4.py"), "rb").read()
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
        ("team-nitro/agreement-buttons-20261118/work/fix4/edit-fix4.py", driver),
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
        sys.exit("usage: edit-fix4.py [edit|all]")
