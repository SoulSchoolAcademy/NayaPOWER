#!/usr/bin/env python3
"""R6e full-loop probe: portal front (orb = ONE entry, no bottom button,
N upright, energy ring, menu rest, ring moving, heading) -> orb click
(intercepted, exact URL) -> staged /agreement (cover first, zero preview,
visual whole + centered, one play button, audio bar gone, 4:18, facade
click -> video playing) -> LET'S GO -> 27 slides in exact order -> end
slide (deed verbatim + Agree at bottom flashing + 8 links below page) ->
Agree click (intercepted, exact return URL, flag set) -> back at name
entry -> reload at rest, no re-prompt. Runs at 390x844 then 1440x900.
Writes r6e-loop-log.json + screenshots. Reads staged only."""
import os, json, math, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://portal-frontpage-fix-20261125-r6-staging.nayapower.workers.dev"
PROXY = {"server": "http://127.0.0.1:18080"}
EXE = "/home/hatch/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome"
VENV = "/home/hatch/workspace/team-nitro/dashboard/update-20261124/.venv/bin/python"
LOG = {"legs": {}, "pageerrors": [], "failed_requests": [], "requestfailed": []}
DEED = "By entering your name, you make it official \u2014 you are signing the Collective Agreement, and you get the deed to your own world: high-level digital real estate \u2014 your personal page, your business, your space \u2014 free forever."
TITLES = ["THE OLD WAY","WELCOME","THE COLLECTIVE INTELLIGENCE NETWORK","YOUR WORLDS","IN A NUTSHELL","THE SYSTEM","HOW IT WORKS","YOUR DAY","SMART CALENDAR","THE SIMPLE VERSION","FOR AIS","YOUR AIS, TOGETHER","THE MOTHER BRAIN","THE MACHINE VIEW","WHAT IT MEANS","PLUG IN","WHY IT MATTERS","THE NAYA MACHINE","FOR AIS","YOUR THREE WORLDS","THE WHOLE-SYSTEM UNFOLDING","DONE FOR YOU","THE PLATFORM","YOUR OWN WORLDS","WHAT\u2019S IN IT FOR YOU","YOU\u2019RE HIRED","YOUR FRANCHISE"]

N_ANGLE_JS = """() => {
  const ang = (el) => { if (!el) return null; const t = getComputedStyle(el).transform;
    if (t === 'none') return 0; const v = t.replace(/matrix\\(|\)/g,'').split(',').map(Number);
    return Math.round(Math.atan2(v[1], v[0]) * 180 / Math.PI); };
  return { circle: ang(document.getElementById('fpCircleNImg')),
    red: ang(document.querySelector('.ncorner-right img')),
    black: ang(document.querySelector('.ncorner-left img')) };
}"""

RING_JS = """() => {
  const portal=document.querySelector('.portal').getBoundingClientRect();
  const cx=portal.x+portal.width/2, cy=portal.y+portal.height/2;
  const out={cx, cy, portalW: portal.width, jewels: []};
  document.querySelectorAll('.naya-jewel').forEach(el=>{
    const r=el.getBoundingClientRect(); const x=r.x+r.width/2, y=r.y+r.height/2;
    out.jewels.push({ang: Math.round(Math.atan2(y-cy,x-cx)*180/Math.PI), rad: Math.round(Math.hypot(x-cx,y-cy))});
  });
  return out;
}"""

def attach(pg, tag):
    pg.on("pageerror", lambda e: LOG["pageerrors"].append(f"{tag} {str(e)[:200]}"))
    pg.on("console", lambda m: LOG["pageerrors"].append(f"{tag} console.{m.type} {m.text[:160]}") if m.type == "error" else None)
    pg.on("response", lambda r: LOG["failed_requests"].append(f"{tag} {r.status} {r.url[:140]}") if r.status >= 400 else None)
    pg.on("requestfailed", lambda r: LOG["requestfailed"].append(f"{tag} {r.failure} {r.url[:140]}") if r.url.startswith("http") else None)

def new_page(pw, w, h, touch=False):
    b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"], proxy=PROXY)
    ctx = b.new_context(viewport={"width": w, "height": h}, has_touch=touch, is_mobile=touch)
    pg = ctx.new_page()
    return b, ctx, pg

def run_width(pw, tag, w, h):
    b, ctx, pg = new_page(pw, w, h, touch=(tag == "phone"))
    attach(pg, tag)
    leg = {}
    # ---------- PORTAL FRONT ----------
    pg.goto(BASE + "/", wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_timeout(3500)
    leg["front"] = pg.evaluate("""() => {
      const orb = document.getElementById('fpCircleN');
      const o = orb ? orb.getBoundingClientRect() : null;
      const img = document.getElementById('fpCircleNImg');
      const vw = window.innerWidth;
      return {
        orbPresent: !!orb,
        orbCenterX: o ? Math.round(o.x + o.width / 2) : null,
        viewportCenterX: Math.round(vw / 2),
        orbTop: o ? Math.round(o.y) : null,
        orbW: o ? Math.round(o.width) : null,
        orbAria: orb ? orb.getAttribute('aria-label') : null,
        orbRingAnim: orb ? getComputedStyle(orb, '::before').animationName : null,
        orbHaloAnim: orb ? getComputedStyle(orb, '::after').animationName : null,
        orbImgAnim: img ? getComputedStyle(img).animationName : null,
        fpEnterDeal: document.querySelectorAll('#fpEnterDeal').length,
        bottomReadBtn: [...document.querySelectorAll('button')].filter(x => x.offsetParent !== null && x.textContent.includes('Read the agreement')).map(x => x.id || x.className),
        iCount: (document.body.innerText.match(/\\u24D8/g) || []).length,
        menuLabels: document.querySelectorAll('.eco-label').length,
        menuTips0: [...document.querySelectorAll('nav.eco-inline > a')].map(a => { const t = a.querySelector('.eco-tip'); return t ? getComputedStyle(t).opacity : null; }),
        heading: (document.querySelector('.presence') || {}).textContent ? document.querySelector('.presence').textContent.trim() : null,
        redCornerHref: (document.querySelector('.ncorner-right') || {}).href || null,
        redCornerAria: (document.querySelector('.ncorner-right') || {}).getAttribute ? document.querySelector('.ncorner-right').getAttribute('aria-label') : null,
        blackCornerHref: (document.querySelector('.ncorner-left') || {}).href || null,
        nameInput: !!document.getElementById('userName'),
        stageOn: document.body.classList.contains('fp-stage-on'),
      };
    }""")
    leg["n_angle_t0"] = pg.evaluate(N_ANGLE_JS)
    leg["ring_t0"] = pg.evaluate(RING_JS)
    pg.wait_for_timeout(12000)
    leg["n_angle_t12"] = pg.evaluate(N_ANGLE_JS)
    leg["ring_t12"] = pg.evaluate(RING_JS)
    pg.screenshot(path=os.path.join(HERE, f"r6e-{tag}-front.png"))
    print(f"FRONT {tag}:", json.dumps(leg["front"]), flush=True)
    print(f"N-ANGLE {tag} t0:", leg["n_angle_t0"], "t12:", leg["n_angle_t12"], flush=True)
    d0 = [a["ang"] for a in leg["ring_t0"]["jewels"]]; d1 = [a["ang"] for a in leg["ring_t12"]["jewels"]]
    def delta(a, b):
        d = abs(a - b) % 360
        return min(d, 360 - d)
    leg["ring_delta"] = [round(delta(x, y), 1) for x, y in zip(d0, d1)]
    print(f"RING {tag} deltas:", leg["ring_delta"], flush=True)

    # ---------- ORB CLICK -> exact URL (intercepted) ----------
    hit = []
    def orb_route(route):
        hit.append(route.request.url)
        route.abort()
    pg.route("https://nayanet.app/agreement", orb_route)
    pg.locator("#fpCircleN").click(timeout=10000)
    pg.wait_for_timeout(1500)
    pg.unroute("https://nayanet.app/agreement", orb_route)
    leg["orb_click_url"] = hit
    print(f"ORB CLICK {tag}: intercepted navigations:", hit, flush=True)

    # ---------- STAGED /agreement — COVER ----------
    pg.goto(BASE + "/agreement", wait_until="domcontentloaded", timeout=180000)
    try:
        pg.wait_for_function("() => { const c = document.getElementById('screen-cover'); return c && c.classList.contains('active'); }", timeout=60000)
    except Exception as e:
        print(f"COVER WAIT {tag} FAILED:", str(e)[:200], flush=True)
    pg.wait_for_timeout(4000)
    leg["cover"] = pg.evaluate("""() => {
      const body = document.body.innerText;
      const poster = document.getElementById('videoPoster');
      const pr = poster ? poster.getBoundingClientRect() : null;
      const frame = document.getElementById('videoFrame');
      const fr = frame ? frame.getBoundingClientRect() : null;
      const facade = document.getElementById('videoFacade');
      const fcr = facade ? facade.getBoundingClientRect() : null;
      const audio = document.getElementById('welcomeAudio');
      return {
        coverActive: (document.getElementById('screen-cover') || {}).classList ? document.getElementById('screen-cover').classList.contains('active') : null,
        choiceNull: document.getElementById('screen-choice') === null,
        previewStrings: { beginStory: (body.match(/Begin the visual story/g) || []).length,
          readAgreement: (body.match(/Read the agreement/g) || []).length,
          trust: (body.match(/Welcome\\. Let's begin with trust\\./g) || []).length },
        marquee: (document.querySelector('.pm-marquee, marquee') || {}).textContent ? document.querySelector('.pm-marquee, marquee').textContent.trim().slice(0, 120) : null,
        poster: poster ? { complete: poster.complete, natural: [poster.naturalWidth, poster.naturalHeight],
          fit: getComputedStyle(poster).objectFit, pos: getComputedStyle(poster).objectPosition,
          box: {x: Math.round(pr.x), y: Math.round(pr.y), w: Math.round(pr.width), h: Math.round(pr.height)} } : null,
        frame: fr ? {x: Math.round(fr.x), y: Math.round(fr.y), w: Math.round(fr.width), h: Math.round(fr.height)} : null,
        facade: facade ? { count: document.querySelectorAll('#videoFacade').length,
          belowFrame: fr ? Math.round(fcr.y) >= Math.round(fr.y + fr.height) - 2 : null,
          box: {x: Math.round(fcr.x), y: Math.round(fcr.y), w: Math.round(fcr.width), h: Math.round(fcr.height)},
          coversPoster: (pr && fcr) ? !(fcr.y >= pr.y + pr.height || fcr.y + fcr.height <= pr.y || fcr.x >= pr.x + pr.width || fcr.x + fcr.width <= pr.x) : null } : null,
        audio: audio ? { hidden: audio.hidden, hasControls: audio.hasAttribute('controls'),
          duration: audio.duration, readyState: audio.readyState, srcKind: (audio.currentSrc || '').slice(0, 30) } : null,
        panelHas418: body.includes('4:18'),
        tDur: (document.getElementById('tDur') || {}).textContent || null,
        transport: [...document.querySelectorAll('.deck-ctl button, .pm-transport button')].map(x => (x.getAttribute('aria-label') || x.textContent || '').trim()).filter(Boolean),
        capText: (document.querySelector('#screen-cover .pm-cap') || {}).textContent ? document.querySelector('#screen-cover .pm-cap').textContent.trim().slice(0, 80) : null,
        letsGo: (document.getElementById('btnStart') || {}).textContent ? document.getElementById('btnStart').textContent.trim() : null,
      };
    }""")
    print(f"COVER {tag}:", json.dumps(leg["cover"]), flush=True)
    pg.screenshot(path=os.path.join(HERE, f"r6e-{tag}-cover.png"))

    # ---------- FACADE CLICK -> video playing ----------
    pg.locator("#videoFacade").click(timeout=10000)
    pg.wait_for_timeout(4000)
    leg["facade_click"] = pg.evaluate("""() => {
      const shell = document.getElementById('videoShell');
      const iframe = shell ? shell.querySelector('iframe') : null;
      const frame = document.getElementById('videoFrame');
      return { shellHidden: shell ? shell.hidden : null,
        iframe: iframe ? { src: iframe.src, w: iframe.width, h: iframe.height } : null,
        framePlaying: frame ? frame.classList.contains('playing') : null,
        facadeHidden: (() => { const f = document.getElementById('videoFacade'); return f ? getComputedStyle(f).display === 'none' : null; })(),
        status: (document.querySelector('#screen-cover .pm-cap') || {}).textContent ? document.querySelector('#screen-cover .pm-cap').textContent.trim().slice(0, 60) : null,
        tDur: (document.getElementById('tDur') || {}).textContent || null };
    }""")
    print(f"FACADE CLICK {tag}:", json.dumps(leg["facade_click"]), flush=True)
    pg.screenshot(path=os.path.join(HERE, f"r6e-{tag}-playing.png"))

    # ---------- LET'S GO -> 27 slides ----------
    pg.locator("#btnStart").click(timeout=10000)
    pg.wait_for_timeout(1500)
    stations = []
    st0 = pg.evaluate("() => ({ slideActive: (document.getElementById('screen-slide')||{}).classList ? document.getElementById('screen-slide').classList.contains('active') : null, station: (document.getElementById('slideStation')||{}).textContent || null })")
    stations.append(st0["station"])
    pg.screenshot(path=os.path.join(HERE, f"r6e-{tag}-slide1.png"))
    for i in range(26):
        pg.locator("#btnForward").click(timeout=10000)
        pg.wait_for_timeout(450)
        stations.append(pg.evaluate("() => (document.getElementById('slideStation')||{}).textContent || null"))
    leg["slide_walk"] = {"first": st0, "stations": stations, "order_ok": stations == TITLES}
    print(f"SLIDES {tag} order_ok={stations == TITLES}:", stations, flush=True)
    pg.screenshot(path=os.path.join(HERE, f"r6e-{tag}-endslide.png"))

    # ---------- END SLIDE ----------
    leg["end"] = pg.evaluate("""() => {
      const row = document.getElementById('fpFinalRow');
      const bar = document.getElementById('fpLinksBar');
      const agree = document.querySelector('[data-fp-agree]');
      const nav = document.querySelector('#screen-slide .floatnav');
      const rr = row ? row.getBoundingClientRect() : null;
      const ar = agree ? agree.getBoundingClientRect() : null;
      const nr = nav ? nav.getBoundingClientRect() : null;
      const sec = document.getElementById('screen-slide');
      return {
        deed: row ? (row.querySelector('.fp-final-deed') || {}).textContent || null : null,
        deedVerbatim: row ? ((row.querySelector('.fp-final-deed') || {}).textContent || '').trim() === """ + json.dumps(DEED) + """ : null,
        agreeText: agree ? agree.textContent.trim() : null,
        agreeAnim: agree ? getComputedStyle(agree).animationName : null,
        agreeBottomAboveArrows: (ar && nr) ? Math.round(ar.bottom) <= Math.round(nr.y) + 2 : null,
        agreeBottom: ar ? Math.round(ar.bottom) : null, arrowsTop: nr ? Math.round(nr.y) : null,
        linksOnSlide: row ? row.querySelectorAll('[data-final]').length : null,
        linksInBar: bar ? [...bar.querySelectorAll('[data-final]')].map(x => x.textContent.trim()) : null,
        barAfterArrows: (bar && nav) ? (bar.compareDocumentPosition(nav) & Node.DOCUMENT_POSITION_PRECEDING) !== 0 : null,
        rowBeforeArrows: (row && nav) ? (row.compareDocumentPosition(nav) & Node.DOCUMENT_POSITION_FOLLOWING) !== 0 : null,
        viewportH: window.innerHeight, agreeVisible: ar ? (ar.top >= 0 && ar.bottom <= window.innerHeight) : null,
      };
    }""")
    print(f"END {tag}:", json.dumps(leg["end"]), flush=True)

    # ---------- AGREE CLICK -> return URL + flag ----------
    hit2 = []
    def agree_route(route):
        hit2.append(route.request.url)
        route.abort()
    pg.route("https://nayanet.app/?from=agreement*", agree_route)
    pg.locator("[data-fp-agree]").click(timeout=10000)
    # goToPortal() sets the flag synchronously, then holds 2s before the
    # navigation fires. Read the flag BEFORE the aborted navigation turns
    # the document into an error page (localStorage then throws).
    pg.wait_for_timeout(800)
    leg["flag"] = pg.evaluate("() => localStorage.getItem('nayanet_agreement_done')")
    pg.wait_for_timeout(2200)
    pg.unroute("https://nayanet.app/?from=agreement*", agree_route)
    leg["agree_click_url"] = hit2
    print(f"AGREE CLICK {tag}:", hit2, "flag:", leg["flag"], flush=True)

    # ---------- BACK AT NAME ENTRY + RELOAD AT REST ----------
    pg.goto(BASE + "/?from=agreement#userName", wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_timeout(3000)
    leg["return"] = pg.evaluate("""() => ({ nameInput: !!document.getElementById('userName'),
      nameVisible: (() => { const n = document.getElementById('userName'); return n ? n.offsetParent !== null : null; })(),
      stageOn: document.body.classList.contains('fp-stage-on'),
      url: location.pathname + location.search + location.hash,
      flag: localStorage.getItem('nayanet_agreement_done') })""")
    pg.reload(wait_until="domcontentloaded", timeout=120000)
    pg.wait_for_timeout(3000)
    leg["reload"] = pg.evaluate("""() => ({ stageOn: document.body.classList.contains('fp-stage-on'),
      view: window.__fpStage ? window.__fpStage.state.view : null,
      flag: localStorage.getItem('nayanet_agreement_done'),
      modalOpen: !!document.querySelector('.fp-nutshell-pop, [role="dialog"]:not([hidden])') })""")
    print(f"RETURN {tag}:", json.dumps(leg["return"]), "RELOAD:", json.dumps(leg["reload"]), flush=True)
    pg.screenshot(path=os.path.join(HERE, f"r6e-{tag}-after-return.png"))
    LOG["legs"][tag] = leg
    ctx.close(); b.close()

with sync_playwright() as pw:
    run_width(pw, "phone", 390, 844)
    run_width(pw, "desk", 1440, 900)
    with open(os.path.join(HERE, "r6e-loop-log.json"), "w") as f:
        json.dump(LOG, f, indent=2)
    print("LOOP PROBE DONE", flush=True)
    print("PAGEERRORS:", LOG["pageerrors"], flush=True)
    print("FAILED REQUESTS:", LOG["failed_requests"][:20], flush=True)
    print("REQUESTFAILED:", LOG["requestfailed"][:20], flush=True)
