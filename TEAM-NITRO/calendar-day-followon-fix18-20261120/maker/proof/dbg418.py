import io
from playwright.sync_api import sync_playwright
from PIL import Image
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
    print("clip:", clip, "scrollY:", pg.evaluate("() => window.scrollY"))
    pg.evaluate("() => { const dots=[...document.querySelectorAll('#dayScroll .sb-dots button')]; if(dots[1]) dots[1].click(); }")
    pg.wait_for_timeout(2500)
    n = pg.evaluate("""() => {
      document.getAnimations().forEach(a => { try { a.pause(); } catch(e){} });
      const st = document.createElement('style');
      st.textContent = '*{animation-play-state:paused!important;transition:none!important}';
      document.head.appendChild(st);
      return document.getAnimations().length;
    }""")
    print("frozen anims:", n, "scrollY:", pg.evaluate("() => window.scrollY"))
    pg.evaluate("() => { document.querySelector('#dayCoverBg').style.display=''; }")
    pg.wait_for_timeout(300)
    a = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
    a.save("shots18/dbg418-A.png")
    arr = np.array(a)
    print("A mean color:", arr.reshape(-1,3).mean(axis=0).round(1), "corner px:", arr[10,10].tolist(), arr[40,850].tolist())
    pg.evaluate("() => { document.querySelector('#dayCoverBg').style.display='none'; }")
    pg.wait_for_timeout(300)
    c = Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")
    c.save("shots18/dbg418-B.png")
    arr2 = np.array(c)
    print("B mean color:", arr2.reshape(-1,3).mean(axis=0).round(1), "corner px:", arr2[10,10].tolist(), arr2[40,850].tolist())
    b.close()
