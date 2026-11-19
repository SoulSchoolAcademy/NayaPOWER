#!/usr/bin/env python3
"""FIX8 render verification (python playwright): staged /agreement + /
at 1920x999 via the h1 forwarder proxy. Proves F1-F9 on the live staged
bytes: frame 1 whole, no blanking over 10s, Next/Keep reading moving
frame by frame, Back present, Play/audio playing, video slot, faces
loaded, home entrance + nav visible. No sign-in, no submit, no agree —
navigation clicks only (Next/Keep reading/Back/video-note toggle)."""
import json
from playwright.sync_api import sync_playwright

OUT = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix8-20261119/work/"
BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
AGREE_JS = r"""
() => {
  const q = (s) => document.querySelector(s);
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), display: cs.display, opacity: cs.opacity}; };
  const beats = [...document.querySelectorAll('#deckBody .letter-beat')];
  const cur = beats.findIndex(b => b.classList.contains('frame-now'));
  const cb = beats[cur];
  const row = cb ? cb.querySelector('.frame-btnrow') : null;
  const btns = row ? [...row.querySelectorAll('button')].map(x => ({t: x.textContent.trim(), hidden: x.hidden, disabled: x.disabled, disp: getComputedStyle(x).display, rect: r(x)})) : null;
  const sc = cb ? cb.querySelector('.frame-scroll') : null;
  const face = cb ? cb.querySelector('.frame-face') : null;
  const media = q('#fpMediaFrame');
  const audio = q('#fpAgreeAudio');
  return {
    cur, beatsTotal: beats.length,
    mainClass: (q('main.p3-deal-unfold') || {}).className,
    deckBodyRect: r(q('#deckBody')),
    topbarRect: cb ? r(cb.querySelector('.frame-topbar')) : null,
    scrollRect: r(sc), scrollH: sc ? sc.scrollHeight : null, scrollTop: sc ? sc.scrollTop : null,
    footRect: cb ? r(cb.querySelector('.frame-foot')) : null,
    seal: cb ? r(cb.querySelector('.frame-red-n')) : null,
    btns,
    face: face ? {complete: face.complete, nw: face.naturalWidth, src: face.src.slice(-40)} : null,
    title: cb ? (cb.querySelector('.frame-title') || {}).textContent : null,
    firstPara: cb ? (cb.querySelector('.ib-nutshell p') || {}).textContent : null,
    media: media ? {rect: r(media), audioBtn: (() => { const b = q('#playBtn'); return b ? {rect: r(b), label: b.getAttribute('aria-label')} : null; })(),
      state: (q('#fpAudioState') || {}).textContent,
      videoBtn: (() => { const b = q('#fpAnthemVideoBtn'); return b ? {rect: r(b), slot: b.getAttribute('data-anthem-slot')} : null; })(),
      noteHidden: (q('#fpAnthemNote') || {}).hidden} : null,
    audio: audio ? {src: audio.src.slice(0, 110), paused: audio.paused, time: Math.round(audio.currentTime * 10) / 10, dur: Math.round(audio.duration || 0)} : null,
    dots: r(q('#deckControls')),
    footLinks: r(q('.foot-links')),
    frameZ: (() => { const f = q('.naya-frame'); return f ? getComputedStyle(f).zIndex : null; })(),
    stageZ: (() => { const m = q('main.p3-deal-unfold'); return m ? getComputedStyle(m).zIndex : null; })(),
    scrollY: window.scrollY, docH: document.documentElement.scrollHeight,
  };
}
"""
HOME_JS = r"""
() => {
  const q = (s) => document.querySelector(s);
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), display: cs.display, opacity: cs.opacity}; };
  return {
    scrollY: Math.round(window.scrollY), docH: document.documentElement.scrollHeight,
    stageOn: document.body.classList.contains('fp-stage-on'),
    nav: r(q('nav.eco-inline')),
    navDots: [...document.querySelectorAll('nav.eco-inline a')].slice(0, 3).map(a => ({t: a.getAttribute('title'), rect: r(a)})),
    stage: r(q('section.stage')), portal: r(q('.portal')), enterBtn: r(q('button.enter')),
    enterDeal: r(q('#fpEnterDeal')),
    agreement: r(q('#fpAgreement')),
    login: (() => { const els = [...document.querySelectorAll('a,button')].filter(e => (e.textContent || '').trim() === '‹ Login'); return els.map(e => r(e)); })(),
  };
}
"""

def show(label, obj):
    print("=== " + label + " ===")
    print(json.dumps(obj, indent=1))

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"], proxy={"server": "http://127.0.0.1:18080"})
    pg = b.new_page(viewport={"width": 1920, "height": 999})
    errs, failed = [], []
    pg.on("pageerror", lambda e: errs.append("PAGEERROR: " + str(e)[:200]))
    pg.on("console", lambda m: errs.append("CONSOLE: " + m.text[:200]) if m.type == "error" else None)
    pg.on("requestfailed", lambda r: failed.append(r.url[:150] + " :: " + str(r.failure)))
    pg.on("response", lambda r: failed.append(str(r.status) + " " + r.url[:150]) if r.status >= 400 else None)

    # ---- /agreement ----
    pg.goto(BASE + "/agreement", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(2000)
    pg.screenshot(path=OUT + "verify-agree-f1.png")
    s = pg.evaluate(AGREE_JS); show("AGREE frame1 t+2s", s)
    pg.wait_for_timeout(8000)
    pg.screenshot(path=OUT + "verify-agree-f1-t10.png")
    s = pg.evaluate(AGREE_JS); show("AGREE frame1 t+10s (F2: still visible?)", s)
    # F3: click Next three times, record the frame each time
    for n in (1, 2, 3):
        pg.click("#deckBody .letter-beat.frame-now .frame-btnrow .frame-next")
        pg.wait_for_timeout(700)
        s = pg.evaluate(AGREE_JS)
        print("AFTER Next #%d: cur=%s title=%r btns=%s" % (n, s["cur"], s["title"], [x["t"] for x in (s["btns"] or [])]))
        if n == 3:
            pg.screenshot(path=OUT + "verify-agree-f4.png")
    # Back once
    pg.click("#deckBody .letter-beat.frame-now .frame-btnrow .deck-back")
    pg.wait_for_timeout(700)
    s = pg.evaluate(AGREE_JS)
    print("AFTER Back: cur=%s title=%r" % (s["cur"], s["title"]))
    # Back to frame 1 via Back again (frame 3->2->1 needs two Backs; do one more)
    pg.click("#deckBody .letter-beat.frame-now .frame-btnrow .deck-back")
    pg.wait_for_timeout(700)
    s = pg.evaluate(AGREE_JS)
    print("AFTER Back#2: cur=%s title=%r" % (s["cur"], s["title"]))
    # Single-tap now: 3 Nexts = +3 frames, 2 Backs = -2, so we sit on
    # frame 2 (cur=1). One more Back returns to frame 1 for the Play
    # check (the media frame lives on frame 1 only).
    pg.click("#deckBody .letter-beat.frame-now .frame-btnrow .deck-back")
    pg.wait_for_timeout(700)
    s = pg.evaluate(AGREE_JS)
    print("AFTER Back#3: cur=%s title=%r" % (s["cur"], s["title"]))
    # F3: the picture shows inside frame 1's own reading window now —
    # scroll the window down to it and prove it rendered.
    pg.evaluate("() => { const sc = document.querySelector('#deckBody .letter-beat.frame-now .frame-scroll'); const im = document.querySelector('#deckBody .letter-beat.frame-now .lb-showcase img'); if (sc && im) { sc.scrollTop = im.getBoundingClientRect().top - sc.getBoundingClientRect().top + sc.scrollTop - 20; } return im ? {complete: im.complete, nw: im.naturalWidth, alt: im.alt} : null; }")
    pg.wait_for_timeout(600)
    pg.screenshot(path=OUT + "verify-agree-showcase.png")
    print("SHOWCASE frame1: " + str(pg.evaluate("() => { const im = document.querySelector('#deckBody .letter-beat.frame-now .lb-showcase img'); return im ? {complete: im.complete, nw: im.naturalWidth, alt: im.alt.slice(0,60)} : null; }")))
    pg.evaluate("() => { const sc = document.querySelector('#deckBody .letter-beat.frame-now .frame-scroll'); if (sc) sc.scrollTop = 0; }")
    pg.wait_for_timeout(400)
    # F4/F9: click the audio orb, wait, check playing state + time advancing
    pg.click("#playBtn")
    pg.wait_for_timeout(3000)
    s = pg.evaluate(AGREE_JS)
    print("AFTER Play click: audio=%s state=%r" % (s["audio"], (s["media"] or {}).get("state")))
    pg.screenshot(path=OUT + "verify-agree-playing.png")
    pg.wait_for_timeout(2000)
    s2 = pg.evaluate(AGREE_JS)
    print("AUDIO +2s: time=%s paused=%s" % ((s2["audio"] or {}).get("time"), (s2["audio"] or {}).get("paused")))
    pg.click("#playBtn")  # pause again
    pg.wait_for_timeout(500)
    # F9 video slot toggle
    pg.click("#fpAnthemVideoBtn")
    pg.wait_for_timeout(500)
    s = pg.evaluate(AGREE_JS)
    print("AFTER Video click: noteHidden=%s" % ((s["media"] or {}).get("noteHidden")))
    pg.screenshot(path=OUT + "verify-agree-video.png")
    print("AGREE ERRORS:", errs or "(none)")
    print("AGREE FAILED REQ (first 15):", failed[:15] or "(none)")

    # ---- / home ----
    errs.clear(); failed.clear()
    pg.goto(BASE + "/", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(2500)
    pg.screenshot(path=OUT + "verify-home.png")
    show("HOME t+2.5s", pg.evaluate(HOME_JS))
    pg.wait_for_timeout(4000)
    pg.screenshot(path=OUT + "verify-home-t6.png")
    show("HOME t+6.5s", pg.evaluate(HOME_JS))
    # ?stage=bridge still opens the stage (no submit)
    pg.goto(BASE + "/?stage=bridge", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(2000)
    h = pg.evaluate(HOME_JS)
    print("STAGE=bridge: stageOn=%s agreement=%s" % (h["stageOn"], h["agreement"]))
    print("HOME ERRORS:", errs or "(none)")
    print("HOME FAILED REQ (first 15):", failed[:15] or "(none)")
    b.close()
print("VERIFY DONE")
