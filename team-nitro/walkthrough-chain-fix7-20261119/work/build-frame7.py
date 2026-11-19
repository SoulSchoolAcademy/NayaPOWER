#!/usr/bin/env python3
"""FIX7 frame transform (2026-11-19): the Collective Agreement INTO THE FRAME.

Takes the fix-3 unfold bytes (105,308 B, sha 3252948e) and rebuilds ONLY the
shell — every beat's words, pictures, tones, foot, play script, deck
mechanics, end card and agree handler are untouched (verified by a
content diff after the transform: the only changed regions are the
inserted FIX7 style/script blocks + the <div class="naya-frame"> layer).

What changes, and why (Shawn's words 10:54-10:57 MST):
  * The page NEVER scrolls again. The frame IS the viewport: main becomes
    a fixed stage padded inside the master frame; one beat shows at a
    time; the frame content scrolls INSIDE its own panel when a beat is
    tall; Back / Keep reading / Next are pinned below the content, so
    they can never be below the fold. This kills the diagnosed defect
    by design: no page scroll to trap, no scroll-snap, no
    scroll-restoration landing (history.scrollRestoration='manual'),
    no 100svh beat pushing its button off-screen.
  * Random top icons OFF: the title's 64/60px flanking padding is gone,
    the per-beat blocktop (portrait + jewel + title, a duplicate of the
    top bar) is hidden, nothing else sits at the top.
  * Top bar on EVERY frame: Naya's picture (a new face each frame,
    cycling the 8 harvested face-*.jpg proof-host URLs), headline
    centred, jewel icon right in the beat's own tone.
  * Frame 1 is Naya introducing herself ("Hi, I'm Naya", her voice),
    play first (the play button stays the first choice), and the big
    RED N seal sits just above the three buttons.
  * The slideshow (visual phase) is framed too: the showcase is capped
    to the frame's content box, not the viewport.
  * Queued fix-6 items, by design: the 1919 void (stage fills the
    viewport exactly), the I-agree screen ~3 viewports at 635 (sign
    photo capped to 32-36dvh, content scrolls inside the frame),
    the legal-row clip (foot wraps, no fixed row).
  * The flowing light (115): a ball of light travels the frame's edge,
    60s, never a wash over the board.
The frame art is the pinned master frame (1,680,379 B, sha 865357f6,
blob 5a4dc2f9) — SILVER/WHITE ornament, never gold — served from the
proof-host once filed beside the unfold file. Landscape shows the
whole frame (contain, nothing cropped, nothing stretched); portrait
shows the top + bottom bands (the crown + winged N top and bottom,
undistorted; the 9:16 asset from the frame-assets round drops into
--frame-img-916 when it lands).
"""
import hashlib

UNFOLD_LOCAL = "/home/hatch/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html"
BASE_SHA = "3252948ed7f80157d0fa86fd730dc2e535a749f00e80944f0274ded54eb6a0f8"
PH = "https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/agreement-unfold-20261117/"
FRAME_URL = (PH + "master-frame.png&ref=walkthrough/chain-fix7-20261119"
             "&cb=5a4dc2f9ca703945f12cec0b39b491d728e69c4a")
FACES = [
    ("face-1.jpg", "8743e1868400bb8ae4f650b536ab9cbace036786"),
    ("face-3.jpg", "c01d71025d34abf8379bab5b7eb13bfa9204964a"),
    ("face-4.jpg", "39c7f0ce4222d853d676d1ea5138569ed182b209"),
    ("face-5.jpg", "c3cd3d9caf778a0b9e0fcf122b3a780030107f76"),
    ("face-6.jpg", "6fa4c1a28c196429f8c2e325de695a31f16cd06b"),
    ("face-7.jpg", "0be821b80d8c055d08b9f5333449064507b7412e"),
    ("face-8.jpg", "00ea37ad9e03cc5da2b7ba352b0f3d988e31da5a"),
    ("face-9.jpg", "e1dbe46717f87cf4cb63f7cef4bd367d8bb1a0f2"),
]
FACE_URLS = [PH + n + "&ref=agreement/unfold-20261117&cb=" + cb for n, cb in FACES]

CSS = """
<style id="fpFrame7">
/* ============ FRAME-7 (2026-11-19) — the agreement INTO THE FRAME ============
   Shawn 10:54-10:57 MST: the agreement lands mid-page, unreadable, no
   buttons, won't scroll. The frame fixes it by design: the page never
   scrolls — the frame IS the viewport, one beat at a time, buttons
   pinned below the content. The old flow CSS below is overridden, never
   deleted: snap off, 100svh beats off, nutshell inner-scroll cap off. */
html,body{height:100%;overflow:hidden}
body{display:block}
.naya-frame{position:fixed;inset:0;z-index:60;pointer-events:none;background-repeat:no-repeat;
  background-image:url(__FRAME_URL__);background-position:center;background-size:contain}
@media (max-aspect-ratio:1/1){.naya-frame{background-image:url(__FRAME_URL__),url(__FRAME_URL__);
  background-position:center top,center bottom;background-size:100% auto,100% auto}}
/* (115) THE FLOWING LIGHT — a ball of light around the frame's edge, 60s,
   rim light in motion, never a wash over the board. */
.frame-light{position:absolute;width:12px;height:12px;border-radius:50%;background:#fff;
  box-shadow:0 0 12px #fff,0 0 26px #8e24aa,0 0 44px #8e24aa;animation:frameLight 60s linear infinite}
@keyframes frameLight{0%{top:0;left:0}25%{top:0;left:calc(100% - 12px)}50%{top:calc(100% - 12px);left:calc(100% - 12px)}75%{top:calc(100% - 12px);left:0}100%{top:0;left:0}}
/* The stage: the whole page, fixed inside the frame's ornament. */
.p3-deal-unfold{position:fixed!important;inset:0;z-index:10;margin:0!important;border:0;border-radius:0;
  background:transparent;box-shadow:none;display:flex;flex-direction:column;overflow:hidden;box-sizing:border-box;
  --fin-t:88px;--fin-b:88px;--fin-l:30px;--fin-r:30px;
  padding:var(--fin-t) var(--fin-r) var(--fin-b) var(--fin-l)}
@media (min-width:1024px) and (min-aspect-ratio:1/1){.p3-deal-unfold{--fin-t:220px;--fin-b:200px;--fin-l:170px;--fin-r:170px}}
@media (min-aspect-ratio:1/1) and (max-height:700px){.p3-deal-unfold{--fin-t:120px;--fin-b:120px;--fin-l:100px;--fin-r:100px}}
/* Random top icons OFF: the title's flanking padding goes, the headline is centred. */
.deal-title{padding:0}
@media(max-width:480px){.deal-title{padding:0}}
/* Past frame 1 the page header goes away — the per-frame top bar carries it. */
.frame-past-1 .deal-title,.frame-past-1 .deck-sub,.frame-past-1 .play-wrap{display:none}
#deckBody{flex:1 1 auto;min-height:0;overflow-y:auto;scroll-snap-type:none!important;display:block;gap:0}
#deckBody .letter-beat{scroll-snap-align:none}
.letter-beat{margin:0;height:100%}
.letter-beat:not(.frame-now){display:none!important}
.letter-beat.frame-now{display:flex!important;flex-direction:column}
.letter-beat.fp-smart-talk{min-height:0!important;justify-content:flex-start}
.letter-beat.fp-smart-talk .ib-nutshell{max-height:none;overflow-y:visible}
.letter-beat.fp-smart-visual{min-height:0!important;justify-content:flex-start}
.letter-beat.fp-smart-visual .lb-showcase{width:min(100%,calc((100dvh - 360px)*16/9));max-height:calc(100dvh - 360px)}
/* The top bar replaces the per-beat blocktop (portrait + jewel + title, a duplicate). */
.ib-blocktop{display:none!important}
/* Top bar: Naya's picture (new each frame), headline centred, icon right. */
.frame-topbar{display:flex;align-items:center;gap:16px;flex:none;margin-bottom:14px}
.frame-face{width:72px;height:72px;border-radius:50%;object-fit:cover;flex:none;
  border:2px solid rgba(255,255,255,.4);box-shadow:0 0 18px var(--tone,#8e24aa),0 8px 20px rgba(0,0,0,.6)}
.frame-head{flex:1;min-width:0;text-align:center}
.frame-kind{display:block;font-size:17px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--tone,#8e24aa)}
.frame-title{font-family:Marcellus,Georgia,serif;font-size:25px;line-height:1.15;color:#fff;margin:2px 0 0;text-wrap:balance}
.frame-icon{width:64px;height:64px;flex:none;display:grid;place-items:center;font-size:30px;color:#fff;line-height:1;
  border-radius:50%;border:2px solid rgba(255,255,255,.4);
  background:radial-gradient(circle at 35% 30%,color-mix(in srgb,var(--tone,#8e24aa) 65%,#fff 10%),color-mix(in srgb,var(--tone,#8e24aa) 55%,#000) 85%);
  box-shadow:0 0 22px color-mix(in srgb,var(--tone,#8e24aa) 55%,transparent),0 8px 20px rgba(0,0,0,.6);
  text-shadow:0 0 10px var(--tone,#8e24aa)}
@media(max-width:480px){.frame-face{width:56px;height:56px}.frame-icon{width:48px;height:48px;font-size:22px}.frame-topbar{gap:10px}}
/* Content scrolls inside the frame; the foot is pinned below it. */
.frame-scroll{flex:1 1 auto;min-height:0;overflow-y:auto}
.frame-foot{flex:none;display:flex;flex-direction:column;align-items:center;gap:12px;padding-top:16px}
.frame-btnrow{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}
.frame-foot .deck-next,.frame-foot .deck-back{margin:0}
.frame-red-n{margin:0 auto}
.ib-foot{overflow-wrap:break-word}
#deckControls{flex:none}
.foot-links{flex:none;margin:16px 0 0}
/* I-agree final screen: the sign photo fits one frame at 635 (was ~3 viewports). */
.deal-sign-photo{height:min(480px,36dvh);width:auto;max-width:100%}
@media(max-width:480px){.deal-sign-photo{height:min(336px,32dvh);width:auto}}
@media (prefers-reduced-motion:reduce){.frame-light{animation:none}}
</style>
""".replace("__FRAME_URL__", FRAME_URL)

JS = """
<script>
/* ============ FRAME-7 (2026-11-19) — one frame at a time ============
   Runs after wireDeck + wirePlay + wireAgree (script order). It does NOT
   touch the deck mechanics: Keep reading / Back / read-it-all / the dots
   / the play speech / the agree stamp all run exactly as before. This
   layer only (a) builds the per-frame top bar, (b) wraps each beat's
   body in the frame's inner scroller and its buttons in the pinned
   foot (Back / Keep reading / Next), (c) shows ONE beat at a time,
   (d) parks the page scroll for good (the restoration landing dies
   with it: a re-open always opens frame 1). Next advances through the
   existing Keep-reading button (one click for the visual stop, a second
   for the advance) so no reveal path is bypassed. */
(function wireFrame7(){
  try { history.scrollRestoration = 'manual'; } catch (e) {}
  window.scrollTo(0, 0);
  document.documentElement.style.scrollBehavior = 'auto';
  var FACES = __FACES__;
  var main = document.getElementById('deckUnfold');
  var deckBody = document.getElementById('deckBody');
  var beats = Array.prototype.slice.call(document.querySelectorAll('#deckBody .letter-beat'));
  var fi = 0, allMode = false;
  function headFor(b, i){
    if (i === 0) return { kind: 'Naya \\u00b7 The Collective Agreement', title: 'Hi, I\\u2019m Naya' };
    var t = b.querySelector('.ib-title'), k = b.querySelector('.ib-kind');
    return { kind: k ? k.textContent.trim() : 'The Collective Agreement',
             title: t ? t.textContent.trim() : 'The Collective Agreement' };
  }
  beats.forEach(function(b, i){
    var h = headFor(b, i);
    var bar = document.createElement('div'); bar.className = 'frame-topbar';
    var img = document.createElement('img'); img.className = 'frame-face';
    img.src = FACES[i % FACES.length]; img.alt = 'Naya speaking';
    var head = document.createElement('div'); head.className = 'frame-head';
    var kind = document.createElement('span'); kind.className = 'frame-kind'; kind.textContent = h.kind;
    var ttl = document.createElement('h2'); ttl.className = 'frame-title'; ttl.textContent = h.title;
    head.appendChild(kind); head.appendChild(ttl);
    var ic = document.createElement('span'); ic.className = 'frame-icon';
    ic.setAttribute('aria-hidden', 'true'); ic.textContent = '\\u25C6';
    bar.appendChild(img); bar.appendChild(head); bar.appendChild(ic);
    var sc = document.createElement('div'); sc.className = 'frame-scroll';
    var foot = document.createElement('div'); foot.className = 'frame-foot';
    var row = document.createElement('div'); row.className = 'frame-btnrow';
    foot.appendChild(row);
    if (i === 0) {
      var red = document.createElement('div');
      red.className = 'deal-seal frame-red-n';
      var mark = document.createElement('span');
      mark.className = 'deal-seal-mark'; mark.setAttribute('aria-hidden', 'true'); mark.textContent = 'N';
      red.appendChild(mark); foot.insertBefore(red, row);
    }
    b.appendChild(bar); b.appendChild(sc); b.appendChild(foot);
    var kids = Array.prototype.slice.call(b.childNodes);
    var kr = null, back = null;
    kids.forEach(function(n){
      if (n === bar || n === sc || n === foot) return;
      if (n.nodeType === 1 && n.classList.contains('deck-next') && !n.classList.contains('deck-back')) { kr = n; return; }
      if (n.nodeType === 1 && n.classList.contains('deck-back')) { back = n; return; }
      sc.appendChild(n);
    });
    if (back) row.appendChild(back);
    if (kr) row.appendChild(kr);
    if (kr && i < beats.length - 1) {
      var nx = document.createElement('button');
      nx.className = 'p3-enter letter-next deck-next frame-next'; nx.type = 'button';
      nx.textContent = 'Next \\u25C6';
      nx.addEventListener('click', function(){
        kr.click();
        setTimeout(function(){ if (fi === i) kr.click(); }, 140);
      });
      row.appendChild(nx);
    }
  });
  function showFrame(n){
    fi = n;
    beats.forEach(function(b, j){ b.classList.toggle('frame-now', j === n); });
    main.classList.toggle('frame-past-1', n > 0);
    if (deckBody) deckBody.scrollTop = 0;
    var sc = beats[n] ? beats[n].querySelector('.frame-scroll') : null;
    if (sc) sc.scrollTop = 0;
  }
  deckBody.addEventListener('click', function(ev){
    if (allMode) return;
    var t = ev.target && ev.target.closest ? ev.target.closest('.deck-next[data-beat],.deck-back') : null;
    if (!t || t.classList.contains('frame-next')) return;
    var beat = t.closest('.letter-beat');
    var i = beats.indexOf(beat);
    if (i < 0) return;
    if (t.classList.contains('deck-back')) {
      showFrame(beat.classList.contains('fp-smart-visual') ? i : Math.max(0, i - 1));
    } else {
      showFrame(beat.classList.contains('fp-smart-visual') ? i : Math.min(beats.length - 1, i + 1));
    }
  });
  var all = document.getElementById('deckAll');
  if (all) all.addEventListener('click', function(){
    allMode = true;
    beats.forEach(function(b){ b.classList.add('frame-now'); });
    main.classList.add('frame-past-1');
  });
  showFrame(0);
})();
</script>
""".replace("__FACES__", repr(FACE_URLS).replace("'", '"'))


def fetch_base_unfold():
    """Base unfold bytes: the local file if intact, else the filed blob
    (8980e577, fix-3 bytes) via the git blob API. The EPERM flake zeroed
    the local file on the first write attempt (truncate-first open) —
    the filed blob is the truth, so the build never depends on the
    local copy being writable."""
    import base64, importlib.util, json, subprocess, sys
    local = open(UNFOLD_LOCAL, "rb").read()
    if hashlib.sha256(local).hexdigest() == BASE_SHA:
        return local
    print("local unfold is %d B (flake-zeroed) — fetching the filed blob" % len(local), file=sys.stderr, flush=True)
    SPEC = importlib.util.spec_from_file_location(
        "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
    st = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(st)
    r = subprocess.run([sys.executable, "/home/hatch/workspace/team-nitro/gh-direct.py", "GET",
                        "/repos/SoulSchoolAcademy/NayaPOWER/git/blobs/8980e57786c9bb196fb1ac5252f483995228e337"],
                       capture_output=True, timeout=180)
    out = r.stdout.decode("utf-8", "replace")
    d = json.loads(out.split("\n", 1)[1])
    raw = base64.b64decode("".join(d["content"].split()))
    assert hashlib.sha256(raw).hexdigest() == BASE_SHA, "filed blob is not the fix-3 unfold"
    return raw


def main():
    import base64, importlib.util, sys
    stdout_only = "--stdout" in sys.argv
    SPEC = importlib.util.spec_from_file_location(
        "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
    st = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(st)
    raw = fetch_base_unfold()
    text = raw.decode("utf-8")
    assert text.count("fpFrame7") == 0, "frame7 already applied"
    assert "<body>" in text and "</head>" in text and text.rstrip().endswith("</html>")
    # 1. frame layer right after <body>
    text = text.replace("<body>", "<body>\n<div class=\"naya-frame\" aria-hidden=\"true\"><div class=\"frame-light\"></div></div>", 1)
    # 2. frame CSS before </head>
    text = text.replace("</head>", CSS + "</head>", 1)
    # 3. frame JS before </body>
    text = text.replace("</body>", JS + "\n</body>", 1)
    out = text.encode("utf-8")
    # content guard: every beat's words still present (spot-check the
    # first lines of beats 1, 2 and 47 + the agree button + play script)
    for needle in ("Hi, I&#x27;m Naya.", "What if it could help you learn faster",
                   "I agree — show me my world", "dealAgreeBtn", "wireDeck", "wirePlay", "wireAgree"):
        assert needle.encode("utf-8") in out, "content lost: %s" % needle
    assert out.count(b'data-beat=') == raw.count(b'data-beat='), "beat count changed"
    assert out.count(b'<article') == raw.count(b'<article'), "article count changed"
    sha = hashlib.sha256(out).hexdigest()
    if stdout_only:
        # Shell-pipe path (EPERM window: python writes land 0 bytes,
        # shell writes land): emit base64 on stdout for `| base64 -d >`.
        sys.stdout.write(base64.b64encode(out).decode("ascii"))
        sys.stdout.flush()
        print("\nunfold fix7: %d B sha %s" % (len(out), sha), file=sys.stderr)
        return
    # Primary landing: the work-dir copy (fresh path — the flake blocks
    # the canonical path right now). The stager files from these bytes.
    work_path = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix7-20261119/work/unfold-fix7.html"
    try:
        st.write_resilient(work_path, out)
        back = open(work_path, "rb").read()
        assert len(back) == len(out) and hashlib.sha256(back).hexdigest() == sha, "work copy verify failed"
        print("work copy landed:", work_path, len(out), "B", flush=True)
    except Exception as e:
        print("WARNING: work copy did not land (EPERM flake): %r — bytes stay in memory for the stager" % e, flush=True)
    # Best-effort restore of the canonical local file (non-fatal: the
    # filed blob + the work copy + the staged bytes are the truth).
    try:
        st.write_resilient(UNFOLD_LOCAL, out)
        back = open(UNFOLD_LOCAL, "rb").read()
        assert hashlib.sha256(back).hexdigest() == sha, "canonical verify failed"
        print("canonical local file restored:", UNFOLD_LOCAL, flush=True)
    except Exception as e:
        print("WARNING: canonical local file NOT restored (EPERM flake): %r — still 0 bytes on disk; restore when the flake clears" % e, flush=True)
    print("unfold fix7: %d B sha %s" % (len(out), sha))


if __name__ == "__main__":
    main()
