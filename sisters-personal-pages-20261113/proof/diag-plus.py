from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    br = pw.firefox.launch()
    ctx = br.new_context(viewport={"width": 390, "height": 844})
    pg = ctx.new_page()
    pg.goto("http://127.0.0.1:8901/pages/sophia/sophia", wait_until="domcontentloaded")
    pg.wait_for_selector("#pname", timeout=20000)
    pg.wait_for_timeout(5000)
    pg.locator("#plusbtn").click()
    pg.wait_for_timeout(800)
    items = pg.evaluate("""() => {
      const out = [];
      document.querySelectorAll('.ph-plusitem').forEach(el => {
        const r = el.getBoundingClientRect();
        out.push({text: el.textContent.trim(), visible: r.height > 0 && getComputedStyle(el).display !== 'none',
                  tag: el.tagName, cls: el.className, html: el.outerHTML.slice(0, 200)});
      });
      return out;
    }""")
    for it in items:
        print(it)
    # click the menu item whose text contains 'Make a post' (visible one)
    try:
        pg.locator(".ph-plusitem:visible", has_text="Make a post").first.click(timeout=8000)
        pg.wait_for_timeout(1200)
        print("after click: creator?", pg.evaluate("() => document.body.innerText.includes('Create') || !!document.querySelector('textarea')"))
        print("url:", pg.url)
        pg.screenshot(path="/home/hatch/workspace/team-nitro/sisters-personal-pages-20261113/spp-sophia-creator-390.png")
    except Exception as e:
        print("CLICK FAILED:", str(e)[:300])
        print("menu still open?", pg.evaluate("() => document.querySelectorAll('.ph-plusitem').length"))
    ctx.close()
    br.close()
print("DIAG DONE")
