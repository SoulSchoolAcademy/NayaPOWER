import json
from playwright.sync_api import sync_playwright
HTML = open("base-fix17.html", encoding="utf-8").read()
with sync_playwright() as p:
    b = p.firefox.launch()
    pg = b.new_page(viewport={"width":1920,"height":999})
    pg.set_content(HTML, wait_until="load", timeout=60000)
    pg.wait_for_timeout(3000)
    pg.evaluate("() => { const b=document.getElementById('backToMonth'); if(b) b.click(); }")
    pg.wait_for_timeout(600)
    pg.evaluate("() => { const c=[...document.querySelectorAll('.cell[data-d]')].find(x=>+x.dataset.d===20); if(c) c.click(); }")
    pg.wait_for_timeout(2000)
    pg.evaluate("() => { const dots=[...document.querySelectorAll('#dayScroll .sb-dots button')]; if(dots[1]) dots[1].click(); }")
    pg.wait_for_timeout(2500)
    def probe():
        return pg.evaluate("""() => {
          const sec=[...document.querySelectorAll('section.cat')].find(s=>getComputedStyle(s).display!=='none');
          const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
          const sb=on.querySelector('.sb-scroll');
          const cs=(el)=>{if(!el) return null; const c=getComputedStyle(el); return {bg:c.backgroundColor, bgImg:c.backgroundImage.slice(0,90), op:c.opacity, anim:c.animationName};};
          return {sec: cs(sec), sb: cs(sb), slide: cs(on),
            secRect: sec ? (()=>{const r=sec.getBoundingClientRect(); return [Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height)];})() : null};
        }""")
    print("UNFROZEN:", json.dumps(probe(), indent=1))
    pg.screenshot(path="shots18/dbg318-unfrozen.png")
    n = pg.evaluate("""() => {
      document.getAnimations().forEach(a => { try { a.pause(); } catch(e){} });
      const st = document.createElement('style');
      st.textContent = '*{animation-play-state:paused!important;transition:none!important}';
      document.head.appendChild(st);
      return document.getAnimations().length;
    }""")
    pg.wait_for_timeout(300)
    print("FROZEN anims:", n)
    print("FROZEN:", json.dumps(probe(), indent=1))
    pg.screenshot(path="shots18/dbg318-frozen.png")
    b.close()
