import io, sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import numpy as np
HTML = open("base-fix17.html", encoding="utf-8").read()
W = int(sys.argv[1]) if len(sys.argv) > 1 else 1920
H = 844 if W == 390 else 999
DAY = int(sys.argv[2]) if len(sys.argv) > 2 else 19
with sync_playwright() as p:
    b = p.firefox.launch()
    pg = b.new_page(viewport={"width":W,"height":H})
    pg.set_content(HTML, wait_until="load", timeout=60000)
    pg.wait_for_timeout(3000)
    pg.evaluate("() => { const b=document.getElementById('backToMonth'); if(b) b.click(); }")
    pg.wait_for_timeout(600)
    pg.evaluate("(dd) => { const c=[...document.querySelectorAll('.cell[data-d]')].find(x=>+x.dataset.d===dd); if(c) c.click(); }", DAY)
    pg.wait_for_timeout(2000)
    print("cover src:", pg.evaluate("() => { const c=document.querySelector('#coverImg'); return (c.currentSrc||c.src||'').split('/').pop().split('&')[0]; }"))
    clip = pg.evaluate("() => { const b=document.querySelector('#dayScroll').getBoundingClientRect(); return {x:b.x,y:b.y,width:b.width,height:b.height}; }")
    for i in (0, 1, 3, 5):
        pg.evaluate("(ii) => { const dots=[...document.querySelectorAll('#dayScroll .sb-dots button')]; if(dots[ii]) dots[ii].click(); }", i)
        pg.wait_for_timeout(2500)
        pg.evaluate("() => { document.querySelector('#dayCoverBg').style.display=''; }")
        pg.wait_for_timeout(300)
        a = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
        pg.evaluate("() => { document.querySelector('#dayCoverBg').style.display='none'; }")
        pg.wait_for_timeout(300)
        c = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
        pg.evaluate("() => { document.querySelector('#dayCoverBg').style.display=''; }")
        d = np.array(ImageChops.difference(a, c).convert("L"))
        mask = d > 12
        ys, xs = np.where(mask)
        # interior diff: exclude 6px frame
        inner = mask[6:-6, 6:-6]
        print(f"day {DAY} W{W} slide {i}: diff px={int(mask.sum())} ({mask.mean()*100:.2f}%) interior(>6px from edge)={int(inner.sum())}")
    b.close()
