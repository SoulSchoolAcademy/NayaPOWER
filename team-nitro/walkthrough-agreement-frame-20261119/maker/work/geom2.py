from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox","--disable-gpu"], proxy={"server":"http://127.0.0.1:18080"})
    pg = b.new_page(viewport={"width":1920,"height":999})
    pg.goto("https://naya-walk-beginning-staging.nayapower.workers.dev/agreement", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(2000)
    print(json.dumps(pg.evaluate("""() => {
      const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); return {x:Math.round(b.x),y:Math.round(b.y),w:Math.round(b.width),h:Math.round(b.height)}; };
      const db = document.querySelector('#deckBody');
      const beat = document.querySelector('#deckBody .letter-beat.frame-now');
      const sc = beat ? beat.querySelector('.frame-scroll') : null;
      const foot = beat ? beat.querySelector('.frame-foot') : null;
      const main = document.querySelector('.p3-deal-unfold');
      const cs = (el, prop) => el ? getComputedStyle(el)[prop] : null;
      return {mainDisp: cs(main,'display'), mainDir: cs(main,'flexDirection'),
        deckBodyRect: r(db), deckBodyFlex: cs(db,'flex'), deckBodyDisp: cs(db,'display'),
        beatRect: r(beat), beatH: cs(beat,'height'), beatDisp: cs(beat,'display'), beatDir: cs(beat,'flexDirection'),
        scrollRect: r(sc), scrollFlex: cs(sc,'flex'), scrollH: sc ? sc.scrollHeight : null,
        footRect: r(foot), controls: r(document.querySelector('#deckControls')), footlinks: r(document.querySelector('.foot-links')),
        hasStretchRule: [...document.styleSheets].some(s => { try { return [...s.cssRules].some(r2 => r2.cssText && r2.cssText.includes('letter-beat{height:100%')); } catch(e){ return false; } })};
    }"""), indent=1))
    b.close()
