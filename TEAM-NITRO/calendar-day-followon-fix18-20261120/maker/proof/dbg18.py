import json
from playwright.sync_api import sync_playwright
HTML = open("base-fix17.html", encoding="utf-8").read()
with sync_playwright() as p:
    b = p.firefox.launch()
    pg = b.new_page(viewport={"width":1920,"height":999})
    errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.set_content(HTML, wait_until="load", timeout=60000)
    pg.wait_for_timeout(3000)
    pg.evaluate("() => { const b=document.getElementById('backToMonth'); if(b) b.click(); }")
    pg.wait_for_timeout(600)
    pg.evaluate("() => { const c=[...document.querySelectorAll('.cell[data-d]')].find(x=>+x.dataset.d===20); if(c) c.click(); }")
    pg.wait_for_timeout(2000)
    pg.evaluate("() => { const dots=[...document.querySelectorAll('#dayScroll .sb-dots button')]; if(dots[1]) dots[1].click(); }")
    pg.wait_for_timeout(2000)
    for t in range(4):
        m = pg.evaluate("""() => {
          const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
          const cs=getComputedStyle(on);
          const kids=[...on.children].map(c=>c.tagName+'.'+String(c.className).split(' ')[0]);
          return {id:on.id, cls:on.className, op:cs.opacity, anim:cs.animationName, animDur:cs.animationDuration,
            bg:cs.backgroundColor.slice(0,40), kids,
            cat: !!on.querySelector('section.cat'), catTag: (on.querySelector('section.cat')||{}).tagName,
            onCount: document.querySelectorAll('#dayScroll .smart-block.on').length};
        }""")
        print(t, json.dumps(m))
        pg.wait_for_timeout(1000)
    print("ERRS:", errs)
    b.close()
