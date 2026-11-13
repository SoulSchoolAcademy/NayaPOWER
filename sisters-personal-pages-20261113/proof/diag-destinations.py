"""Every button clicked, every destination recorded (brief Step 4)."""
import json
from playwright.sync_api import sync_playwright
OUT = "/home/hatch/workspace/team-nitro/sisters-personal-pages-20261113/"
R = json.load(open(OUT + "spp-results.json"))
def check(name, ok, detail=""):
    (R["pass"] if ok else R["fail"]).append(name + (" :: " + str(detail) if detail else ""))
    json.dump(R, open(OUT + "spp-results.json", "w"), indent=2)
with sync_playwright() as pw:
    br = pw.firefox.launch()
    ctx = br.new_context(viewport={"width": 390, "height": 844})
    pg = ctx.new_page()
    pg.goto("http://127.0.0.1:8901/pages/sophia/sophia", wait_until="domcontentloaded")
    pg.wait_for_selector("#pname", timeout=20000)
    pg.wait_for_timeout(5000)
    dests = {}
    for label in ["Message", "About", "My World", "Skills", "Connections", "Invite", "Share", "Join NayaNET", "Settings"]:
        if label == "Join NayaNET":
            href = pg.locator(".up-act:visible", has_text=label).first.get_attribute("href")
            dests[label] = href
            check(f"sophia destination {label} -> {href}", href and "nayanet.app/joinus" in href, href)
            continue
        try:
            pg.locator(".up-act:visible", has_text=label).first.click(timeout=10000)
            pg.wait_for_timeout(1000)
            dests[label] = pg.evaluate("""() => {
              const vis = [...document.querySelectorAll('.ib-layer.open, [data-os-view]')].map(e => (e.id || e.className || e.getAttribute('data-os-view') || '').toString().slice(0,60)).filter(Boolean).slice(0,3);
              return location.hash + ' | ' + (document.querySelector('h1,h2,.os-view-title') ? document.querySelector('h1,h2,.os-view-title').textContent.trim().slice(0,60) : '') + ' | open:' + vis.join(',');
            }""")
            check(f"sophia destination {label} recorded", True, dests[label])
        except Exception as e:
            dests[label] = "CLICK FAILED: " + str(e)[:100]
            check(f"sophia destination {label} recorded", False, dests[label])
        pg.goto("http://127.0.0.1:8901/pages/sophia/sophia", wait_until="domcontentloaded")
        pg.wait_for_selector("#pname", timeout=20000)
        pg.wait_for_timeout(2500)
    # plus-menu items -> destinations
    pg.locator("#plusbtn").click()
    pg.wait_for_timeout(800)
    for item in ["Make a post", "Send a message", "Add a Smart Link", "Add to a list"]:
        try:
            pg.locator(".ph-plusitem:visible", has_text=item).first.click(timeout=8000)
            pg.wait_for_timeout(1000)
            d = pg.evaluate("() => location.hash + ' | ' + document.body.innerText.slice(0, 100).replace(/\\n/g, ' | ')")
            dests["+" + item] = d
            check(f"sophia destination +{item} recorded", True, d[:120])
        except Exception as e:
            check(f"sophia destination +{item} recorded", False, str(e)[:120])
        pg.goto("http://127.0.0.1:8901/pages/sophia/sophia", wait_until="domcontentloaded")
        pg.wait_for_selector("#pname", timeout=20000)
        pg.wait_for_timeout(2000)
        pg.locator("#plusbtn").click()
        pg.wait_for_timeout(800)
    ctx.close()
    br.close()
json.dump(dests, open(OUT + "spp-destinations.json", "w"), indent=2)
print("DESTINATIONS:")
for k, v in dests.items():
    print(f"  {k}: {v}")
print(f"DONE: pass={len(R['pass'])} fail={len(R['fail'])}")
