import io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
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
    dom = pg.evaluate("""() => {
      const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
      const sb=on.querySelector('.sb-scroll');
      const sec=on.querySelector('section');
      const allSecs=[...document.querySelectorAll('section.cat')].map(s=>{const r=s.getBoundingClientRect(); return {inDayScroll: !!document.querySelector('#dayScroll').contains(s), vis: getComputedStyle(s).display, x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height)};});
      return {sbKids: sb ? [...sb.children].map(c=>c.tagName+'.'+String(c.className).split(' ')[0]).slice(0,8) : null,
        secInSb: sec ? sec.tagName+'.'+sec.className : null,
        allSecs,
        panelContent: !!document.querySelector('#panelContent'),
        dayScrollKids: [...document.querySelector('#dayScroll').children].map(c=>c.tagName+'#'+(c.id||'')+'.'+String(c.className).split(' ')[0])};
    }""")
    print(dom)
    clip = pg.evaluate("() => { const b=document.querySelector('#dayScroll').getBoundingClientRect(); return {x:b.x,y:b.y,width:b.width,height:b.height}; }")
    def shot():
        return Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
    def diffcount(a, b):
        d = ImageChops.difference(a, b).convert("L")
        return sum(1 for px in d.getdata() if px > 12)
    a1 = shot(); pg.wait_for_timeout(300); a2 = shot()
    print("drift cover-ON 300ms apart: differing px =", diffcount(a1, a2), "of", a1.width*a1.height)
    pg.evaluate("() => { document.querySelector('#dayCoverBg').style.display='none'; }")
    pg.wait_for_timeout(300)
    b1 = shot()
    print("cover ON vs OFF: differing px =", diffcount(a1, b1))
    bb = b1.getbbox()
    d = ImageChops.difference(a1, b1).convert("L")
    # bounding box of differing pixels
    import numpy as np
    arr = np.array(d)
    ys, xs = np.where(arr > 12)
    if len(xs):
        print("diff bbox x:", xs.min(), xs.max(), "y:", ys.min(), ys.max(), "count:", len(xs))
    else:
        print("no differing pixels above threshold")
    b.close()
