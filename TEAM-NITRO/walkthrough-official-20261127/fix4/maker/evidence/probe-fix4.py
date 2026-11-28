# FIX4 live probe — one phone per screen, ball flash-then-advance, cascade,
# end screen whole, 0 page errors. Chromium via the localhost forwarder.
import json
from playwright.sync_api import sync_playwright
BASE = "https://official-walkthrough-staging.nayapower.workers.dev"
OUT = "/home/hatch/workspace/team-nitro/walkthrough-official-20261127/fix4/maker/evidence/"
fails = []
def check(name, ok, extra=""):
    print(("PASS " if ok else "FAIL ") + name + (" | " + str(extra)[:240] if extra != "" else ""), flush=True)
    if not ok: fails.append(name)
    return ok
with sync_playwright() as pw:
    b = pw.chromium.launch(proxy={"server": "http://127.0.0.1:18080"})
    ctxP = b.new_context(viewport={"width": 390, "height": 844}, ignore_https_errors=True)
    pp = ctxP.new_page()
    perrs, cerrs = [], []
    pp.on("pageerror", lambda e: perrs.append(str(e)))
    pp.on("console", lambda m: cerrs.append(m.text) if m.type == "error" else None)
    pp.add_init_script("""
      localStorage.setItem('nayanet_smart_alias', 'shawn');
      localStorage.setItem('nayanet_smart_name', 'Shawn');
      localStorage.setItem('nayanet_smart_identities', JSON.stringify([{alias:'shawn',name:'Shawn'},{alias:'friend',name:'Friend'}]));
    """)
    pp.goto(BASE + "/?walk=1&name=Shawn&alias=shawn", wait_until="domcontentloaded", timeout=120000)
    pp.wait_for_timeout(2000)
    check("walk section visible", pp.evaluate("() => !document.getElementById('fpWalk').hidden"))
    check("ONE phone only, no trio, no grouping header",
          pp.evaluate("() => document.querySelectorAll('#bdSingle .bd-phone').length === 1 && !document.getElementById('bdTrio') && !document.getElementById('bdGroupProg')"))
    check("step 1 is live", pp.evaluate("() => document.querySelector('#bdSingle .bd-phone').getAttribute('data-key') === 'live'"))
    check("phone is 393/852-shaped", pp.evaluate("() => { const r = document.querySelector('#bdSingle .bd-phone').getBoundingClientRect(); return Math.abs(r.width / r.height - 393 / 852) < 0.02; }"))
    check("ball carries the real marble image (--ball var set)",
          pp.evaluate("() => (document.documentElement.style.getPropertyValue('--ball') || '').includes('data:image/webp;base64,')"))
    check("ball ring is the Settings conic (not the old jewel ring)",
          pp.evaluate("() => getComputedStyle(document.querySelector('#bdSingle .bd-ball')).backgroundImage.indexOf('conic-gradient') >= 0"))
    pp.screenshot(path=OUT + "fix4-390-step1.png")
    # The cascade lives on STEP 1 (live — where you are): country -> province -> city.
    check("province hidden until country chosen",
          pp.evaluate("() => document.querySelector('[data-fid=\"province\"]').closest('.bd-field').classList.contains('bd-cascade-hidden')"))
    pp.select_option('[data-fid="country"]', "canada")
    pp.wait_for_timeout(400)
    check("country chosen: province drops down + country lifts purple",
          pp.evaluate("() => !document.querySelector('[data-fid=\"province\"]').closest('.bd-field').classList.contains('bd-cascade-hidden') && document.querySelector('[data-fid=\"country\"]').closest('.bd-field').classList.contains('bd-chosen')"))
    check("province options are Canada's (Ontario present)",
          pp.evaluate("() => [...document.querySelectorAll('[data-fid=\"province\"] option')].some(o => o.textContent.trim() === 'Ontario')"))
    pp.select_option('[data-fid="province"]', "ontario")
    pp.wait_for_timeout(400)
    check("province chosen: city drops down (Toronto present)",
          pp.evaluate("() => !document.querySelector('[data-fid=\"city\"]').closest('.bd-field').classList.contains('bd-cascade-hidden') && [...document.querySelectorAll('[data-fid=\"city\"] option')].some(o => o.textContent.trim() === 'Toronto')"))
    pp.screenshot(path=OUT + "fix4-390-cascade.png")
    # Step 1 (live, no pic): first ball tap advances straight to step 2.
    pp.click("#bdSingle .bd-ball", force=True)
    pp.wait_for_timeout(600)
    check("no-pic step: first ball tap advances (live -> age_lang)",
          pp.evaluate("() => document.querySelector('#bdSingle .bd-phone').getAttribute('data-key') === 'age_lang'"))
    # Step 2 -> 3 -> 4 -> 5 via the ball.
    for expect in ("gender", "favorites", "industry_all"):
        pp.click("#bdSingle .bd-ball", force=True)
        pp.wait_for_timeout(600)
        check("ball advances to " + expect, pp.evaluate("() => document.querySelector('#bdSingle .bd-phone').getAttribute('data-key') === '" + expect + "'"))
    pp.click("#bdSingle .bd-ball", force=True)
    pp.wait_for_timeout(600)
    check("ball advances to video step", pp.evaluate("() => document.querySelector('#bdSingle .bd-phone').getAttribute('data-key') === 'video'"))
    # Video step: ball does NOT advance; the arrow does.
    pp.click("#bdSingle .bd-ball", force=True)
    pp.wait_for_timeout(600)
    check("video step: ball tap does not advance", pp.evaluate("() => document.querySelector('#bdSingle .bd-phone').getAttribute('data-key') === 'video'"))
    pp.click("#fpWalkNext", force=True)
    pp.wait_for_timeout(600)
    check("next arrow advances video -> motto", pp.evaluate("() => document.querySelector('#bdSingle .bd-phone').getAttribute('data-key') === 'motto'"))
    # Motto HAS a picture: tap 1 flashes it, tap 2 moves on.
    pp.click("#bdSingle .bd-ball", force=True)
    pp.wait_for_timeout(600)
    check("pic step: tap 1 reveals the picture (stays on motto, bgpic visible)",
          pp.evaluate("() => document.querySelector('#bdSingle .bd-phone').getAttribute('data-key') === 'motto' && document.querySelector('#bdSingle .bd-phone').classList.contains('bd-revealed') && getComputedStyle(document.querySelector('#bdSingle .bd-bgpic')).opacity !== '0'"))
    pp.screenshot(path=OUT + "fix4-390-reveal.png")
    pp.click("#bdSingle .bd-ball", force=True)
    pp.wait_for_timeout(600)
    check("pic step: tap 2 moves on (motto -> vision)", pp.evaluate("() => document.querySelector('#bdSingle .bd-phone').getAttribute('data-key') === 'vision'"))
    # Back arrow returns one step.
    pp.click("#fpWalkBack", force=True)
    pp.wait_for_timeout(600)
    check("back arrow returns (vision -> motto)", pp.evaluate("() => document.querySelector('#bdSingle .bd-phone').getAttribute('data-key') === 'motto'"))
    # Drive to the end with the next arrow (collects + advances each step).
    for _ in range(30):
        key = pp.evaluate("() => document.getElementById('bdSingle').hidden ? 'END' : document.querySelector('#bdSingle .bd-phone').getAttribute('data-key')")
        if key == "END": break
        pp.click("#fpWalkNext", force=True)
        pp.wait_for_timeout(250)
    check("reached the end screen", pp.evaluate("() => document.getElementById('bdEndPhone') && !document.getElementById('bdEndPhone').hidden && document.getElementById('bdSingle').hidden"))
    check("end: Hub before Pricing, world button present",
          pp.evaluate("() => document.getElementById('fpWalkHub') && document.getElementById('fpWalkPricing') && (document.getElementById('fpWalkHub').compareDocumentPosition(document.getElementById('fpWalkPricing')) & 4) && [...document.querySelectorAll('#bdEndPhone a, #bdEndPhone button')].some(e => e.textContent.includes('See my world'))"))
    pp.screenshot(path=OUT + "fix4-390-end.png")
    # 1440 end screen.
    ctxD = b.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
    pd = ctxD.new_page()
    pd.add_init_script("""
      localStorage.setItem('nayanet_smart_alias', 'shawn');
      localStorage.setItem('nayanet_smart_name', 'Shawn');
      localStorage.setItem('nayanet_smart_identities', JSON.stringify([{alias:'shawn',name:'Shawn'},{alias:'friend',name:'Friend'}]));
    """)
    pd.goto(BASE + "/?walk=1&name=Shawn&alias=shawn", wait_until="domcontentloaded", timeout=120000)
    pd.wait_for_timeout(1500)
    for _ in range(30):
        key = pd.evaluate("() => document.getElementById('bdSingle').hidden ? 'END' : document.querySelector('#bdSingle .bd-phone').getAttribute('data-key')")
        if key == "END": break
        pd.click("#fpWalkNext", force=True)
        pd.wait_for_timeout(250)
    check("1440: end screen reached", pd.evaluate("() => document.getElementById('bdEndPhone') && !document.getElementById('bdEndPhone').hidden"))
    pd.screenshot(path=OUT + "fix4-1440-end.png")
    check("0 page errors", len(perrs) == 0, perrs[:3])
    check("0 console errors", len(cerrs) == 0, cerrs[:3])
    b.close()
print("PROBE DONE fails=" + str(len(fails)) + (" " + json.dumps(fails) if fails else ""))
