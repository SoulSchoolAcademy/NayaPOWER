import io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import numpy as np
HTML = open("base-fix17.html", encoding="utf-8").read()
PAUSE = """() => { let n=0;
  document.getAnimations().forEach(a => { try { if (a.playState === 'running') { a.pause(); n++; } } catch(e){} });
  return n; }"""
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
        pg.evaluate(PAUSE)
        pg.wait_for_timeout(200)
        a = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
        pg.evaluate("() => { document.querySelector('#dayCoverBg').style.display='none'; }")
        pg.wait_for_timeout(300)
        c = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
        pg.evaluate("() => { document.querySelector('#dayCoverBg').style.display=''; }")
        d = np.array(ImageChops.difference(a, c).convert("L"))
        mask = d > 12
        inner = mask[6:-6, 6:-6]
        ys, xs = np.where(inner)
        print(f"slide {i}: interior={int(inner.sum())}", end=" ")
        if len(xs):
            print(f"x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()}")
            # column/row profile: which x-bands and y-bands
            import collections
            print("  y-bands:", dict(sorted(collections.Counter((y//60)*60 for y in ys).items())))
            print("  x-bands:", dict(sorted(collections.Counter((x//200)*200 for x in xs).items())))
        vis = np.array(a).copy(); vis[mask] = [255, 0, 0]
        Image.fromarray(vis).save(f"shots18/dv4-1920-{i}-diff.png")
    b.close()
