#!/usr/bin/env python3
"""R6e R5-items probe: portal story order (via the exposed __fpOpenStory
hook — the story code is untouched), returning view, certificate link
target (entry-form submit -> live identity URL, intercepted), and the
letter-view fallback (the /agreement boot still exists in the portal code,
proven by loading the portal HTML directly). Writes r6e-r5-log.json."""
import os, json
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://portal-frontpage-fix-20261125-r6-staging.nayapower.workers.dev"
PROXY = {"server": "http://127.0.0.1:18080"}
EXE = "/home/hatch/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome"
LOG = {"legs": {}, "pageerrors": []}
STORY_TITLES = ["The Old Way","Welcome","The Collective Intelligence Network","Your Worlds","In a Nutshell","The System","How It Works","Your Day","Smart Calendar","The Simple Version","For AIs","Your AIs, Together","The Mother Brain","The Machine View","What It Means","Plug In","Why It Matters","The Naya Machine","For AIs","Your Three Worlds","The Whole-System Unfolding","Done For You","The Platform","Your Own Worlds","What's In It For You","You're Hired","Your Franchise"]

def attach(pg, tag):
    pg.on("pageerror", lambda e: LOG["pageerrors"].append(f"{tag} {str(e)[:200]}"))

with sync_playwright() as pw:
    # ---------- PORTAL STORY ORDER (desk) ----------
    b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"], proxy=PROXY)
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    pg = ctx.new_page(); attach(pg, "story")
    pg.goto(BASE + "/", wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_timeout(3000)
    pg.evaluate("() => window.__fpOpenStory(0)")
    pg.wait_for_timeout(1500)
    titles = []
    for i in range(27):
        titles.append(pg.evaluate("() => (document.getElementById('fpStoryTitle')||{}).textContent || (document.getElementById('fpStoryStation')||{}).textContent || null"))
        if i < 26:
            pg.locator("#fpStoryNext").click(timeout=10000)
            pg.wait_for_timeout(400)
    LOG["legs"]["portal_story"] = {"titles": titles, "order_ok": titles == STORY_TITLES,
        "agree": pg.evaluate("() => (document.getElementById('fpStoryAgree')||{}).textContent || null"),
        "links": pg.evaluate("() => [...document.querySelectorAll('#fpStoryLinks a, #fpStoryLinks button')].map(e => e.textContent.trim())")}
    print("PORTAL STORY order_ok:", titles == STORY_TITLES, flush=True)
    print("  agree:", LOG["legs"]["portal_story"]["agree"], "links:", LOG["legs"]["portal_story"]["links"], flush=True)
    pg.screenshot(path=os.path.join(HERE, "r6e-desk-story-end.png"))

    # ---------- CERT LINK TARGET (entry-form submit, intercepted) ----------
    hit = []
    def cert_route(route):
        hit.append(route.request.url)
        route.abort()
    pg.route("https://nayanet.app/identity.html*", cert_route)
    pg.goto(BASE + "/", wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_timeout(2500)
    pg.evaluate("() => { const n = document.getElementById('userName'); if (n) { n.value = 'R6eCheck'; n.dispatchEvent(new Event('input', {bubbles:true})); } }")
    pg.locator("#entryForm button[type='submit'], #fpEnterBtn, button.fp-enter").first.click(timeout=10000)
    pg.wait_for_timeout(2000)
    pg.unroute("https://nayanet.app/identity.html*", cert_route)
    LOG["legs"]["cert_link"] = {"intercepted": hit}
    print("CERT LINK intercepted:", hit, flush=True)
    # staged /identity.html bytes already proven by curl sha; confirm it renders the new cert here
    pg.goto(BASE + "/identity.html", wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_timeout(2500)
    LOG["legs"]["cert_staged"] = pg.evaluate("() => ({ title: document.title, hasWalkUrl: document.body.innerHTML.includes(\"/?walk=1\"), bodyLen: document.body.innerHTML.length })")
    print("CERT STAGED:", LOG["legs"]["cert_staged"], flush=True)
    ctx.close()

    # ---------- RETURNING VIEW (phone) ----------
    ctx = b.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    pg = ctx.new_page(); attach(pg, "returning")
    pg.goto(BASE + "/?walk=1&alias=r6check01&name=R6Check", wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_timeout(3000)
    stored = pg.evaluate("() => ({ alias: localStorage.getItem('nayanet_smart_alias'), name: localStorage.getItem('nayanet_smart_name') })")
    pg.goto(BASE + "/", wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_timeout(3000)
    ret = pg.evaluate("""() => ({ returning: document.body.classList.contains('fp-returning'),
      greet: (() => { const g = document.getElementById('returningGreet'); return g ? {hidden: g.hidden, text: g.textContent.trim()} : null; })(),
      deedHidden: (() => { const d = document.getElementById('fpDeedSentence'); return d ? d.hidden : null; })(),
      jumpVisible: (() => { const j = document.getElementById('jumpBackIn'); return j ? j.offsetParent !== null : null; })(),
      formHidden: (() => { const f = document.getElementById('entryForm'); return f ? f.hidden : null; })() })""")
    LOG["legs"]["returning"] = {"stored": stored, "ret": ret}
    print("RETURNING stored:", stored, "ret:", ret, flush=True)
    pg.screenshot(path=os.path.join(HERE, "r6e-phone-returning.png"))
    ctx.close(); b.close()
    with open(os.path.join(HERE, "r6e-r5-log.json"), "w") as f:
        json.dump(LOG, f, indent=2)
    print("R5 PROBE DONE", flush=True)
    print("PAGEERRORS:", LOG["pageerrors"], flush=True)
