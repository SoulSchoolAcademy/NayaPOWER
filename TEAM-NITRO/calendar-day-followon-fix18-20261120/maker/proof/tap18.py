"""CAL-FIX18: Change-cover tap test on FIXED bytes — the pill where it remains
must open the native file picker; where it is hidden it must not be clickable.
"""
import sys
from playwright.sync_api import sync_playwright
HTML = open("fixed-fix18.html", encoding="utf-8").read()
def goto(page, d):
    page.evaluate("() => { const b=document.getElementById('backToMonth'); if(b) b.click(); }")
    page.wait_for_timeout(600)
    page.evaluate("(dd) => { const c=[...document.querySelectorAll('.cell[data-d]')].find(x=>+x.dataset.d===dd); if(c) c.click(); }", d)
    page.wait_for_timeout(2000)
def slide(page, i):
    page.evaluate("(ii) => { const dots=[...document.querySelectorAll('#dayScroll .sb-dots button')]; if(dots[ii]) dots[ii].click(); }", i)
    page.wait_for_timeout(2000)
with sync_playwright() as p:
    b = p.firefox.launch()
    for (W, H, label) in ((1920, 999, "1920"), (390, 844, "390")):
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.set_content(HTML, wait_until="load", timeout=60000)
        pg.wait_for_timeout(3000)
        goto(pg, 20)
        for (i, name, expect) in ((0, "wisdom", W == 1920), (3, "worlds", True), (1, "notifications", False)):
            slide(pg, i)
            vis = pg.evaluate("() => { const c=[...document.querySelectorAll('button')].find(b=>/Change cover/i.test(b.textContent)); return c ? (getComputedStyle(c).display !== 'none' && c.getBoundingClientRect().width > 0) : null; }")
            if expect:
                try:
                    with pg.expect_file_chooser(timeout=5000) as fc:
                        pg.evaluate("() => { const c=[...document.querySelectorAll('button')].find(b=>/Change cover/i.test(b.textContent)); c.click(); }")
                    print(f"{label} slide {i} {name}: pill visible={vis} TAP -> file picker OPENED")
                except Exception as e:
                    print(f"{label} slide {i} {name}: pill visible={vis} TAP FAILED: {str(e)[:120]}")
            else:
                print(f"{label} slide {i} {name}: pill visible={vis} (expect hidden) {'OK' if vis is False else 'MISMATCH'}")
        pg.close()
    b.close()
