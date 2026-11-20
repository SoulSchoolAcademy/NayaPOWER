import json
from playwright.sync_api import sync_playwright
GEO = r"""() => {
  const nav = document.querySelector('#fpLegal .fp-legal-links');
  const cs = getComputedStyle(nav);
  const links = [...nav.querySelectorAll('a, button')].map(el => el.textContent.trim());
  const max = nav.scrollWidth - nav.clientWidth;
  const seen = links.map(() => null);
  const pos = [0];
  for (let s = 100; s < max; s += 100) pos.push(s);
  if (max > 0) pos.push(max);
  for (const sl of pos) {
    nav.scrollLeft = sl;
    const a = nav.scrollLeft;
    [...nav.querySelectorAll('a, button')].forEach((el, i) => {
      const r = el.getBoundingClientRect();
      if (r.left >= 0 && r.right <= 390 && seen[i] === null) seen[i] = a;
    });
  }
  nav.scrollLeft = 0;
  const at0 = [...nav.querySelectorAll('a, button')].slice(0,3).map(el => { const r = el.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.right)]; });
  return {scrollWidth: nav.scrollWidth, clientWidth: nav.clientWidth, maxScroll: max,
    justify: cs.justifyContent, reachable: seen.map((s,i)=>({link: links[i], ok: s!==null, at: s})),
    unreachable: seen.filter(s=>s===null).length, firstThreeAt0: at0};
}"""
with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width":390,"height":844}, device_scale_factor=2, ignore_https_errors=True)
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
    pg.on("console", lambda m: errs.append(m.type+": "+m.text[:150]) if m.type=="error" else None)
    pg.goto("https://naya-walk-beginning-staging.nayapower.workers.dev/agreement", timeout=60000)
    pg.wait_for_timeout(2000)
    for i in range(40):
        if pg.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /I agree/i.test(x.innerText))"):
            break
        pg.locator("button", has_text="Next").locator("visible=true").first.click(timeout=5000)
        pg.wait_for_timeout(400)
    pg.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=5000)
    pg.wait_for_timeout(2500)
    res = pg.evaluate(GEO)
    print(json.dumps(res, indent=1))
    print("consoleErrors:", errs)
    pg.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = 0; }")
    pg.wait_for_timeout(400)
    pg.screenshot(path="proof-fix5/fix5-staged-bridge-s0.png")
    b.close()
print("STAGED SPOT-CHECK DONE")
