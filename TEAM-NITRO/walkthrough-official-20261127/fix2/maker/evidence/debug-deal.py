# DEBUG: map the live-tap route to the deal view's plain dialog + zoom.
import json
from playwright.sync_api import sync_playwright
BASE = "https://official-walkthrough-staging.nayapower.workers.dev"
OUT = "/home/hatch/workspace/team-nitro/walkthrough-official-20261127/fix2/maker/evidence/"
STATE_JS = """() => {
  const S = window.__fpStage ? window.__fpStage.state : null;
  const vis = (sel) => { const e = document.querySelector(sel); if (!e) return 'absent'; const r = e.getBoundingClientRect(); return (e.offsetParent !== null) ? ('visible ' + Math.round(r.width) + 'x' + Math.round(r.height)) : 'hidden-el'; };
  const letterShown = [...document.querySelectorAll('#letterBody .letter-beat')].filter(b => !b.hidden).length;
  const deckShown = [...document.querySelectorAll('#deckBody .letter-beat')].filter(b => !b.hidden).length;
  return {view: S ? S.view : null, deck: S ? S.deck : null, letter: S ? S.letter : null,
    stageOn: document.body.classList.contains('fp-stage-on'),
    eye: vis('#dealEyeMain'), letterAll: vis('#letterAll'), mirrorAll: vis('#fpLinkLetterAll'),
    nextBtn: document.getElementById('fpNextBtn') ? document.getElementById('fpNextBtn').textContent : null,
    nextBtn2: document.getElementById('fpNextBtn2') ? (document.getElementById('fpNextBtn2').hidden ? 'hidden' : document.getElementById('fpNextBtn2').textContent) : null,
    letterShown, deckShown};
}"""
with sync_playwright() as pw:
    b = pw.chromium.launch(proxy={"server": "http://127.0.0.1:18080"})
    ctx = b.new_context(viewport={"width": 390, "height": 844}, ignore_https_errors=True)
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "/", wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_timeout(1200)
    print("plain-load:", json.dumps(pg.evaluate(STATE_JS)), flush=True)
    print("eye display on plain load:", pg.evaluate("() => { const e=document.getElementById('dealEyeMain'); const cs=getComputedStyle(e); return {disp: cs.display, secDisp: getComputedStyle(document.getElementById('fpAgreement')).display}; }"), flush=True)
    pg.evaluate("() => window.__fpStage.enter()")
    pg.wait_for_timeout(800)
    print("after enter():", json.dumps(pg.evaluate(STATE_JS)), flush=True)
    # intro view: the bottom bar is display:none here — the tap target is
    # the in-flow choice button #fpChoiceDeck ("Begin the visual story").
    ch = pg.locator("#fpChoiceDeck")
    print("choiceDeck visible:", ch.count(), pg.evaluate("() => { const e=document.getElementById('fpChoiceDeck'); return e ? e.offsetParent !== null : false; }"), flush=True)
    ch.click()
    pg.wait_for_timeout(900)
    print("after Begin (choiceDeck):", json.dumps(pg.evaluate(STATE_JS)), flush=True)
    # step through the deck
    for i in range(9):
        st = pg.evaluate(STATE_JS)
        print("deck step", i, ":", json.dumps(st), flush=True)
        if st["view"] != "deck":
            print("LEFT DECK at step", i, flush=True)
            break
        # try the zoom on this beat first (real tap on showcase img if visible)
        show = pg.evaluate("() => [...document.querySelectorAll('#deckBody .letter-beat.fp-now .lb-showcase img')].map(im => ({vis: im.offsetParent !== null, src: (im.getAttribute('src')||'').slice(0,50)}))")
        print("  showcase imgs on this beat:", json.dumps(show), flush=True)
        if show and show[0]["vis"]:
            pg.locator("#deckBody .letter-beat.fp-now .lb-showcase img").first.click()
            pg.wait_for_timeout(700)
            z = pg.evaluate("() => { const z=document.getElementById('fpZoom'); return z ? {hidden: z.hidden, open: z.classList.contains('fp-open'), rect: JSON.stringify(z.getBoundingClientRect())} : null; }")
            print("  ZOOM after tap:", json.dumps(z), flush=True)
            pg.screenshot(path=OUT + "fix2-390-zoom.png")
            pg.locator("#fpZoomClose").click()
            pg.wait_for_timeout(500)
            print("  zoom closed:", pg.evaluate("() => document.getElementById('fpZoom').hidden"), flush=True)
            break
        pg.locator("#fpNextBtn").click()
        pg.wait_for_timeout(800)
    print("after deck walk:", json.dumps(pg.evaluate(STATE_JS)), flush=True)
    # letterPage via the exposed state API (no tap route exists) — then REAL TAP on the mirror link
    pg.evaluate("() => { const st = window.__fpStage; st.state.view='letterPage'; st.state.letter=0; st.render(); }")
    pg.wait_for_timeout(900)
    print("letterPage via state API:", json.dumps(pg.evaluate(STATE_JS)), flush=True)
    mir = pg.locator("#fpLinkLetterAll")
    print("mirror count/visible:", mir.count(), pg.evaluate("() => { const e=document.getElementById('fpLinkLetterAll'); return e ? e.offsetParent !== null : false; }"), flush=True)
    if mir.count():
        mir.click()
        pg.wait_for_timeout(800)
        plain = pg.evaluate("""() => { const d = document.getElementById('dealPlain'); if (!d) return null;
          const r = d.getBoundingClientRect(); const t = document.getElementById('dealPlainText');
          const c = document.getElementById('dealPlainClose');
          return {hidden: d.hidden, rect: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
            textHead: t ? t.textContent.slice(0, 40) : null, closeVis: c ? c.offsetParent !== null : false}; }""")
        print("dealPlain after mirror tap:", json.dumps(plain), flush=True)
        pg.screenshot(path=OUT + "fix2-390-dealplain.png")
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(500)
        print("plain closed on Esc:", pg.evaluate("() => document.getElementById('dealPlain').hidden"), flush=True)
    print("pageerrors:", errs, flush=True)
    pg.close()
    b.close()
print("DEBUG DONE")
