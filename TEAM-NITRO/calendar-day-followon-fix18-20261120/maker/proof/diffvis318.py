import io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import numpy as np
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
    clip = pg.evaluate("() => { const b=document.querySelector('#dayScroll').getBoundingClientRect(); return {x:b.x,y:b.y,width:b.width,height:b.height}; }")
    for i in (1, 0):
        pg.evaluate("(ii) => { const dots=[...document.querySelectorAll('#dayScroll .sb-dots button')]; if(dots[ii]) dots[ii].click(); }", i)
        pg.wait_for_timeout(2500)
        pg.evaluate("() => { document.querySelector('#dayCoverBg').style.display=''; }")
        pg.wait_for_timeout(300)
        a = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
        pg.evaluate("() => { document.querySelector('#dayCoverBg').style.display='none'; }")
        pg.wait_for_timeout(300)
        c = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
        pg.evaluate("() => { document.querySelector('#dayCoverBg').style.display=''; }")
        a.save(f"shots18/dv1920-{i}-on.png"); c.save(f"shots18/dv1920-{i}-off.png")
        d = np.array(ImageChops.difference(a, c).convert("L"))
        mask = d > 12
        vis = np.array(a).copy(); vis[mask] = [255, 0, 0]
        Image.fromarray(vis).save(f"shots18/dv1920-{i}-diff.png")
        ys, xs = np.where(mask)
        inner = mask[6:-6, 6:-6]
        print(f"slide {i}: interior diff={int(inner.sum())}; y-range of interior diff:",
              (int(ys.min()), int(ys.max())) if len(ys) else None)
    b.close()
