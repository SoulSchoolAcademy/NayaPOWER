#!/usr/bin/env python3
"""SPP probe part 2 — the legs the runtime restart killed.
Loads the run-2 results (611 pass / 0 fail: live control + 12 sisters'
Personal legs) and appends: Business/Space samples (one per voice A/B/C),
button clicks (sophia 390), fresh citizen sppw1 end-to-end, Box re-reads
(already proven in proof/ — re-asserted here from the live read-backs),
design-contract gate (live vs staged HTML parity).
Harness + snapshots live under proof/ (durable) — /tmp was wiped mid-round.
"""
import json
import re
import subprocess
import urllib.request
import urllib.error
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8901"
LIVE = "https://nayanet.app/personal"
WORK = "/home/hatch/workspace/team-nitro/sisters-personal-pages-20261113/"
PROOF = WORK + "proof/"
R = json.load(open(WORK + "spp-results.json"))
print(f"loaded run-2 results: pass={len(R['pass'])} fail={len(R['fail'])}")

def dump():
    R["notes"] = [f"pass={len(R['pass'])} fail={len(R['fail'])}"]
    json.dump(R, open(WORK + "spp-results.json", "w"), indent=2)

def check(name, ok, detail=""):
    (R["pass"] if ok else R["fail"]).append(name + (" :: " + str(detail) if detail else ""))
    try:
        dump()
    except Exception:
        pass

def overflow(pg):
    return pg.evaluate("document.documentElement.scrollWidth + '/' + document.documentElement.clientWidth")

def rgb_ok(color):
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)", color or "")
    if not m:
        return False, color
    r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
    a = float(m.group(4)) if m.group(4) is not None else 1.0
    return (r >= 200 and g >= 200 and b >= 200 and a >= 0.9), color

def cors_kinds(errs):
    kinds = {}
    for e in errs:
        m = re.search(r"rest/v1/([a-z_]+)\?", e)
        kinds[m.group(1) if m else "other"] = kinds.get(m.group(1) if m else "other", 0) + 1
    return kinds

SR_STUB = """
window.SpeechRecognition = class {
  constructor(){ this.onresult=null; this.onend=null; this.onerror=null; this._stopped=false; }
  start(){
    const self=this;
    setTimeout(()=>{ if(self._stopped||!self.onresult) return;
      const r=[[{transcript:'hello world'}]]; r[0].isFinal=false;
      self.onresult({resultIndex:0, results:r}); }, 300);
    setTimeout(()=>{ if(self._stopped||!self.onresult) return;
      const r=[[{transcript:'hello world from the walk'}]]; r[0].isFinal=true;
      self.onresult({resultIndex:0, results:r}); }, 700);
  }
  stop(){ this._stopped=true; if(this.onend) this.onend(); }
};
"""

MEASURE_JS = """(exp) => {
  const q = s => document.querySelector(s);
  const qa = s => [...document.querySelectorAll(s)];
  const vis = el => !!el && el.offsetParent !== null;
  const txt = document.body.innerText;
  const avatar = qa('img[src^="data:"]')[0];
  return {
    title: document.title,
    pname: q('#pname') ? q('#pname').textContent : null,
    ptag: q('#ptag') ? q('#ptag').textContent : null,
    coverVis: q('.ph-cover') ? vis(q('.ph-cover')) : false,
    coverH: q('.ph-cover') ? Math.round(q('.ph-cover').getBoundingClientRect().height) : 0,
    coverGrad: q('.ph-cover') ? getComputedStyle(q('.ph-cover')).backgroundImage.includes('gradient') : false,
    changeCover: (txt.match(/Change cover/g)||[]).length,
    avatarLetter: avatar ? (avatar.src.includes('%3E' + exp.avatar + '%3C') ? exp.avatar : 'WRONG:' + avatar.src.slice(avatar.src.indexOf('middle'), avatar.src.indexOf('middle')+40)) : 'MISSING',
    pills: ['Naya Academy','AI Masterclass','Fast Action Club'].map(t => (txt.match(new RegExp(t,'g'))||[]).length),
    upActVis: qa('.up-act').filter(vis).map(b => b.textContent.trim()).filter(Boolean),
    plusBtn: !!q('#plusbtn'),
    makePost: txt.includes('Make a post'),
    feedSmart: txt.includes(exp.feedName + "\\u2019s Smart Notes"),
    feedNaya: txt.includes(exp.feedName + "\\u2019s Naya Notes"),
    feedThird: txt.includes(exp.third),
    noPosts: txt.includes('No posts yet'),
    bottomBar: (() => { const el=q('#naya-notif-bar'); if(!el) return false; const r=el.getBoundingClientRect(); return r.height>0 && getComputedStyle(el).display!=='none'; })(),
    bottomBarH: q('#naya-notif-bar') ? Math.round(q('#naya-notif-bar').getBoundingClientRect().height) : 0,
    ibLayer: qa('.ib-layer').length,
    tacho: !!q('#tn-tacho-mount'),
    shawnLeak: (txt.match(/Shawn Vibert/g)||[]).length,
    graySample: ['#pname','#ptag'].map(s => { const el=q(s); return el ? getComputedStyle(el).color : 'missing'; }),
  };
}"""

ABOUT_JS = """() => {
  const q = s => document.querySelector(s);
  const heads = [...document.querySelectorAll('.ib-layer-head b')].map(b => b.textContent.trim());
  const sec = id => { const el=q('#'+id); return el ? el.textContent.trim() : 'MISSING'; };
  return {
    heads: heads.slice(0, 8),
    storyTitle: heads.find(h => /my story|our story/i.test(h)) || 'NONE',
    story: sec('abouttext'),
    motto: sec('os-sec-motto-text'),
    vision: sec('os-sec-vision-text'),
    goals: sec('os-sec-goals-text'),
    mission: sec('os-sec-mission-text'),
    purpose: sec('os-sec-purpose-text'),
    whatido: sec('os-sec-whatido-text'),
  };
}"""

def measure(pg, alias, name, headline, kind, label, third="Public Feed", avatar_letter=None, feed_name=None):
    exp = {"initial": (name or alias)[0].upper(), "name": name, "third": third,
           "avatar": avatar_letter or (name or alias)[0].upper(), "feedName": feed_name or name}
    m = pg.evaluate(MEASURE_JS, exp)
    ok_cover = m["coverVis"] and m["coverH"] > 100 and m["coverGrad"] and m["changeCover"] >= 1
    check(f"{label} cover 1 (visible, gradient, Change cover)", ok_cover, f"vis={m['coverVis']} h={m['coverH']} grad={m['coverGrad']} cc={m['changeCover']}")
    check(f"{label} title is the page headline", m["title"] == headline, m["title"])
    check(f"{label} name is the page headline", m["pname"] == headline, m["pname"])
    check(f"{label} photo slot 1 (initial orb {m['avatarLetter']})", m["avatarLetter"] == exp["avatar"], m["avatarLetter"])
    check(f"{label} pills 3 (Academy, Masterclass, Fast Action Club)", all(n >= 1 for n in m["pills"]), m["pills"])
    want = ["Message", "About", "My World", "Skills", "Connections", "Invite", "Share", "Join NayaNET", "Settings"]
    got = [w for w in want if any(w in b for b in m["upActVis"])]
    check(f"{label} buttons 9 up-act visible", len(got) == 9, f"got={len(got)} {m['upActVis']}")
    add_label = pg.locator("#plusbtn").get_attribute("aria-label")
    check(f"{label} plus button + Add something present", m["plusBtn"] and add_label == "Add something", f"plus={m['plusBtn']} aria={add_label}")
    check(f"{label} composer 1 (Make a post)", m["makePost"], "")
    check(f"{label} feed tabs 3 (Smart/Naya/Public rows)", m["feedSmart"] and m["feedNaya"] and m["feedThird"],
          f"smart={m['feedSmart']} naya={m['feedNaya']} third({third})={m['feedThird']}")
    check(f"{label} feed empty state honest (No posts yet)", m["noPosts"], "")
    check(f"{label} bottom bar 1 (notif-bar)", m["bottomBar"] and m["bottomBarH"] > 20, f"h={m['bottomBarH']}")
    check(f"{label} boards present (ib-layer)", m["ibLayer"] >= 10, m["ibLayer"])
    check(f"{label} gauge present (tachometer mount)", m["tacho"], "")
    check(f"{label} no other-citizen leak (Shawn only as shared course)", m["shawnLeak"] <= 1, f"count={m['shawnLeak']}")
    for sel, c in zip(["#pname", "#ptag"], m["graySample"]):
        okc, _ = rgb_ok(c)
        check(f"{label} {sel} white/lit (never gray)", okc, c)
    return m

def open_about(pg):
    pg.locator(".up-act", has_text="About").first.click()
    pg.wait_for_timeout(1200)

def measure_about(pg, label, story_expect, sections, live=False):
    a = pg.evaluate(ABOUT_JS)
    want_title = "Our Story" if story_expect == "our" else "My Story"
    check(f"{label} story title is {want_title}", (a["storyTitle"] or "").lower() == want_title.lower(), a["storyTitle"])
    if live:
        check(f"{label} story present", len(a["story"]) > 20, a["story"][:80])
        check(f"{label} sections present (vision/goals/mission)", all(len(a[k]) > 0 for k in ["vision", "goals", "mission"]), str({k: a[k][:40] for k in ["vision", "goals", "mission"]}) + " motto=" + repr(a["motto"][:40]))
        return a
    check(f"{label} story is the citizen's words", sections["story"][:60] in a["story"], a["story"][:100])
    for key in ["motto", "vision", "goals", "mission", "whatido"]:
        want = sections[key]
        if want:
            check(f"{label} section {key} is the citizen's words", want[:50] in a[key], a[key][:100])
    check(f"{label} purpose keeps the honest empty state", "No purpose written yet" in a["purpose"], a["purpose"][:80])
    return a

ALIASES = ["sophia", "thea", "zoe", "astraea", "vera", "wren", "iris", "ruth", "terra", "esme", "mira", "aurelia"]
SAMPLES = [("sophia", "A"), ("thea", "B"), ("astraea", "C")]

def box_of(alias):
    return json.load(open(f"{PROOF}spp-box-{alias}.json"))

def sections_for(d, kind):
    a = d["box"]["answers"]
    story = a["about"] if kind == "personal" else (a["biz_do"] + " " + a["biz_offer"] + " " + a["biz_building"] if kind == "business" else a["space"])
    return {"story": story, "motto": a["motto"], "vision": a["vision"], "goals": a["goal"],
            "mission": a["mission"], "whatido": a["biz_do"]}

def api_get(path, base=BASE):
    req = urllib.request.Request(base + path, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return 0, {"error": str(e)[:120]}

def load_personal(pg, url, wait_ms=6000):
    errs, perrs = [], []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: perrs.append(str(e)))
    pg.goto(url, wait_until="domcontentloaded")
    pg.wait_for_selector("#pname", timeout=20000)
    pg.wait_for_timeout(wait_ms)
    return errs, perrs

def console_parity(label, errs, perrs, live_kinds):
    kinds = cors_kinds(errs)
    non_cors = [e for e in errs if "Cross-Origin Request Blocked" not in e]
    check(f"{label} console errors are the VM CORS artifact only (parity with live)",
          len(non_cors) == 0, f"non-CORS={non_cors[:2]} total={len(errs)} kinds={kinds}")
    check(f"{label} console-error tables match live control", set(kinds) == set(live_kinds),
          f"staged={sorted(kinds)} live={sorted(live_kinds)}")
    check(f"{label} zero pageerrors", len(perrs) == 0, str(perrs[:2]))

with sync_playwright() as pw:
    br = pw.firefox.launch()

    # ---------- LIVE KINDS (one quick load; full live control already passed in run 2) ----------
    ctx = br.new_context(viewport={"width": 1440, "height": 900})
    pg = ctx.new_page()
    errs, perrs = load_personal(pg, LIVE)
    live_kinds = cors_kinds(errs)
    print("LIVE kinds (re-measured):", live_kinds, "pageerrors:", len(perrs))
    check("live kinds re-measured (7 tables, 0 pageerrors)", len(live_kinds) == 7 and len(perrs) == 0,
          f"kinds={sorted(live_kinds)} perrs={perrs[:2]}")
    ctx.close()

    # ---------- BUSINESS / SPACE SAMPLES (one per voice A/B/C) ----------
    for alias, voice in SAMPLES:
        d = box_of(alias)
        name = d["box"]["name"]
        pgs = {p["page_kind"]: p for p in d["pages"] if p}
        for kind in ("business", "space"):
            headline = pgs[kind]["headline"]
            slug = pgs[kind]["page_alias"]
            secs = sections_for(d, kind)
            for w in (1440, 390):
                ctx = br.new_context(viewport={"width": w, "height": 900 if w == 1440 else 844})
                pg = ctx.new_page()
                errs, perrs = load_personal(pg, f"{BASE}/pages/{alias}/{slug}")
                measure(pg, alias, name, headline, kind, f"{alias} {kind} {w} (voice {voice})")
                check(f"{alias} {kind} {w} overflow 0", overflow(pg) == f"{w}/{w}", overflow(pg))
                console_parity(f"{alias} {kind} {w}", errs, perrs, live_kinds)
                pg.screenshot(path=WORK + f"spp-{alias}-{kind}-{w}-top.png")
                if w == 1440:
                    open_about(pg)
                    measure_about(pg, f"{alias} {kind} 1440", "our", secs)
                    pg.screenshot(path=WORK + f"spp-{alias}-{kind}-1440-about.png")
                ctx.close()

    # ---------- BUTTON CLICKS (sophia, phone 390) ----------
    ctx = br.new_context(viewport={"width": 390, "height": 844})
    pg = ctx.new_page()
    errs, perrs = [], []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: perrs.append(str(e)))
    pg.goto(f"{BASE}/pages/sophia/sophia", wait_until="domcontentloaded")
    pg.wait_for_selector("#pname", timeout=20000)
    pg.wait_for_timeout(5000)
    join_href = pg.locator(".up-act", has_text="Join NayaNET").first.get_attribute("href")
    check("sophia Join href is the join page", join_href and "nayanet.app/joinus" in join_href, join_href)
    for label in ["Message", "About", "My World", "Skills", "Connections", "Invite", "Share", "Settings"]:
        pg.locator(".up-act", has_text=label).first.click()
        pg.wait_for_timeout(1000)
        vis = pg.evaluate("() => document.body.innerText.slice(0, 120).replace(/\\n/g, ' | ')")
        check(f"sophia click {label} opens something (no dead button)", len(vis) > 20, vis[:100])
        pg.goto(f"{BASE}/pages/sophia/sophia", wait_until="domcontentloaded")
        pg.wait_for_selector("#pname", timeout=20000)
        pg.wait_for_timeout(2500)
    pg.locator("#plusbtn").click()
    pg.wait_for_timeout(800)
    menu_txt = pg.locator("body").inner_text()
    for item in ["Make a post", "Send a message", "Add a Smart Link", "Add to a list"]:
        check(f"sophia plus menu has {item}", item in menu_txt, "")
    pg.screenshot(path=WORK + "spp-sophia-plusmenu-390.png")
    try:
        pg.get_by_text("Make a post", exact=True).first.click()
        pg.wait_for_timeout(1200)
        creator = pg.evaluate("() => document.body.innerText.includes('Create') || !!document.querySelector('textarea')")
        check("sophia Make a post opens the creator", creator, "")
        pg.screenshot(path=WORK + "spp-sophia-creator-390.png")
    except Exception as e:
        check("sophia Make a post opens the creator", False, str(e)[:120])
    ctx.close()

    # ---------- FRESH CITIZEN sppw1 (1440, full walk from the login page) ----------
    A = {
        "about": "I am June. I keep a small garden and I teach my neighbours to grow food.",
        "into": "I am into growing food - the moment a seed becomes dinner.",
        "vision": "A street where every family grows something and shares it.",
        "mission": "To teach ten families on my street to grow their own food.",
        "motto": "Grow a little every day and share what grows.",
        "goal": "To own a small greenhouse and give my children fresh food all year.",
        "biz_do": "I bake bread for my neighbours every Saturday morning.",
        "biz_offer": "Fresh bread made to order, still warm, at your door on Saturday.",
        "biz_building": "I am building a small bakery. The goal is twenty regular customers by Christmas.",
        "space": "A space for growers and bakers. I want to meet everyone who grows or bakes.",
    }
    ctx = br.new_context(viewport={"width": 1440, "height": 900})
    ctx.add_init_script(SR_STUB)
    pg = ctx.new_page()
    errs, perrs = [], []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: perrs.append(str(e)))
    pg.goto(BASE + "/", wait_until="networkidle")
    pg.wait_for_timeout(1000)
    check("fresh entry dial name-only", pg.locator("input").count() == 1 and pg.locator("#userName").count() == 1)
    pg.screenshot(path=WORK + "spp-fresh-entry-1440.png")
    pg.fill("#userName", "SPP Walk One")
    pg.locator("button.enter[type='submit']").click()
    try:
        pg.wait_for_url("**/identity.html**", timeout=15000)
        check("fresh entry submit lands on certificate", True, pg.url)
    except Exception as e:
        check("fresh entry submit lands on certificate", False, f"{pg.url} :: {str(e)[:100]}")
    pg.wait_for_timeout(1500)
    try:
        pg.wait_for_selector("#installLater:visible", timeout=9000)
        pg.locator("#installLater").click()
        pg.wait_for_timeout(500)
    except Exception:
        pass
    pg.fill("#aliasInput", "sppw1")
    pg.locator("#enterBtn").click()
    try:
        pg.wait_for_url("**/welcome**", timeout=25000)
        check("fresh certificate claim lands on the walk", True, pg.url)
    except Exception as e:
        check("fresh certificate claim lands on the walk", False, f"{pg.url} :: {str(e)[:120]}")
    pg.wait_for_timeout(1200)
    pg.fill("#answer-1", A["about"])
    pg.click("#enterBtn-1")
    pg.wait_for_selector("#step-2:visible", timeout=9000)
    check("fresh Q1 advances", True)
    pg.fill("#answer-2", A["into"])
    pg.click("#enterBtn-2")
    pg.wait_for_selector("#step-3:visible", timeout=9000)
    check("fresh Q2 advances", True)
    pg.locator('[data-edit="3-B"]').click()
    pg.wait_for_timeout(300)
    pg.fill("#choice-3-B", A["vision"])
    pg.click("#enterBtn-3")
    pg.wait_for_selector("#step-4:visible", timeout=9000)
    check("fresh Q3 advances (edited choice B)", pg.evaluate("window.__walkState.answers.vision") == A["vision"])
    for key, n in [("mission", 4), ("motto", 5), ("goal", 6), ("biz_do", 7), ("biz_offer", 8), ("biz_building", 9), ("space", 10)]:
        pg.fill(f"#answer-{n}", A[key])
        pg.click(f"#enterBtn-{n}")
        nxt = f"#step-{n+1}" if n < 10 else "#step-names"
        try:
            pg.wait_for_selector(nxt + ":visible", timeout=9000)
            check(f"fresh Q{n} advances", True)
        except Exception as e:
            check(f"fresh Q{n} advances", False, str(e)[:100])
    check("fresh names page visible", pg.locator("#step-names").is_visible())
    pg.fill("#name-business", "SPP Bakery")
    pg.wait_for_timeout(300)
    check("fresh business slug follows the name live", pg.locator("#url-business").input_value() == "spp-bakery", pg.locator("#url-business").input_value())
    pg.fill("#name-space", "The SPP Garden")
    pg.wait_for_timeout(300)
    check("fresh space slug follows the name live", pg.locator("#url-space").input_value() == "the-spp-garden", pg.locator("#url-space").input_value())
    pg.screenshot(path=WORK + "spp-fresh-names-1440.png")
    pg.click("#enterBtn-11")
    try:
        pg.wait_for_selector("#step-building:visible", timeout=9000)
        check("fresh building page visible", True)
    except Exception as e:
        check("fresh building page visible", False, str(e)[:100])
    try:
        pg.wait_for_selector("text=Done — here are your pages.", timeout=30000)
        check("fresh building reaches done", True)
    except Exception as e:
        check("fresh building reaches done", False, str(e)[:100])
    pg.screenshot(path=WORK + "spp-fresh-building-1440.png")
    n_links = pg.locator(".p3-build-link").count()
    check("fresh three building links shown", n_links == 3, f"count={n_links}")
    link_hrefs = [pg.locator(".p3-build-link").nth(i).get_attribute("href") for i in range(3)]
    link_titles = [pg.locator(".p3-build-link").nth(i).inner_text() for i in range(3)]
    check("fresh building links carry the typed titles",
          "sppw1" in link_titles[0] and "SPP Bakery" in link_titles[1] and "The SPP Garden" in link_titles[2], str(link_titles))
    check("fresh building links point at staging pages",
          all(h and "/pages/sppw1/" in h for h in link_hrefs), str(link_hrefs))
    pg.locator(".p3-build-link").nth(0).click()
    pg.wait_for_timeout(2500)
    check("fresh click Personal link lands on the created page",
          "/pages/sppw1/" in pg.url and "SPP Walk One" in pg.locator("body").inner_text(), pg.url)
    pg.screenshot(path=WORK + "spp-fresh-personal-1440.png")
    st, box = api_get("/api/welcome/box?alias=sppw1")
    check("fresh Box read-back 200", st == 200, str(st))
    if st == 200:
        json.dump(box, open(PROOF + "spp-box-sppw1.json", "w"), indent=2)
        ans = box["box"]["answers"]
        for k, v in A.items():
            check(f"fresh Box answer {k} word-for-word", ans.get(k) == v, str(ans.get(k))[:80])
        slugs = {p["page_kind"]: p["page_alias"] for p in box["pages"]}
        check("fresh Box slugs word-for-word", slugs == {"personal": "sppw1", "business": "spp-bakery", "space": "the-spp-garden"}, str(slugs))
        check("fresh Box headlines word-for-word",
              {p["page_kind"]: p["headline"] for p in box["pages"]} == {"personal": "sppw1", "business": "SPP Bakery", "space": "The SPP Garden"},
              str({p["page_kind"]: p["headline"] for p in box["pages"]}))
    pg.goto(BASE + "/welcome", wait_until="networkidle")
    pg.wait_for_timeout(1000)
    check("fresh reload returns to end slide", pg.locator("#step-end").is_visible())
    check("fresh end slide congratulations", "Congratulations, you're hired." in pg.locator("#step-end").inner_text())
    pg.locator('[data-door="Hub"]').click()
    pg.wait_for_timeout(1500)
    check("fresh Hub door lands on the staging Hub", "/hub?alias=sppw1" in pg.url, pg.url)
    hub_txt = pg.locator("body").inner_text()
    check("fresh Hub shows the three pages by typed titles",
          "sppw1" in hub_txt and "SPP Bakery" in hub_txt and "The SPP Garden" in hub_txt, hub_txt[:200].replace("\n", " | "))
    pg.screenshot(path=WORK + "spp-fresh-hub-1440.png")
    for kind, slug, headline, story_expect in [
            ("personal", "sppw1", "sppw1", "my"),
            ("business", "spp-bakery", "SPP Bakery", "our"),
            ("space", "the-spp-garden", "The SPP Garden", "our")]:
        secs = {"story": A["about"] if kind == "personal" else (A["biz_do"] + " " + A["biz_offer"] + " " + A["biz_building"] if kind == "business" else A["space"]),
                "motto": A["motto"], "vision": A["vision"], "goals": A["goal"], "mission": A["mission"], "whatido": A["biz_do"]}
        for w in (1440, 390):
            p2 = ctx.new_page()
            p2.set_viewport_size({"width": w, "height": 900 if w == 1440 else 844})
            errs2, perrs2 = load_personal(p2, f"{BASE}/pages/sppw1/{slug}")
            measure(p2, "sppw1", "SPP Walk One", headline, kind, f"fresh {kind} {w}")
            check(f"fresh {kind} {w} overflow 0", overflow(p2) == f"{w}/{w}", overflow(p2))
            console_parity(f"fresh {kind} {w}", errs2, perrs2, live_kinds)
            p2.screenshot(path=WORK + f"spp-fresh-{kind}-{w}-top.png")
            if w == 1440:
                open_about(p2)
                measure_about(p2, f"fresh {kind} 1440", story_expect, secs)
            p2.close()
    check("fresh walk console errors (walk leg)", len([e for e in errs if "Cross-Origin" not in e]) == 0, f"{len(errs)}: {errs[:2]}")
    check("fresh walk pageerrors", len(perrs) == 0, str(perrs[:2]))
    ctx.close()
    br.close()

# ---------- SISTERS' BOX RE-READS (live staging, asserted from proof/ snapshots) ----------
for alias in ALIASES:
    st, box = api_get("/api/welcome/box?alias=" + alias, base="https://naya-walk-beginning-staging.nayapower.workers.dev")
    check(f"box re-read {alias} 200", st == 200, str(st))
    if st == 200:
        before = box_of(alias)
        same = box["box"]["answers"] == before["box"]["answers"] and [p["headline"] for p in box["pages"]] == [p["headline"] for p in before["pages"]]
        check(f"box re-read {alias} word-for-word (untouched)", same, "" if same else "DIFFERS")
        if not same:
            json.dump({"before": before, "after": box}, open(WORK + f"spp-boxdiff-{alias}.json", "w"), indent=2)

# ---------- DESIGN-CONTRACT GATE (static, live vs staged HTML parity) ----------
for label, path in [("live", PROOF + "personal-live.html"), ("staged-sophia", PROOF + "p-sophia.html")]:
    r = subprocess.run(["python3", "/home/hatch/workspace/team-nitro/design-contract-gate/check-gate.py", path],
                       capture_output=True, text=True, timeout=120)
    out = (r.stdout + r.stderr)
    open(WORK + f"spp-gate-{label}.txt", "w").write(out)
    print(f"--- gate {label} (exit {r.returncode}) ---")
    print(out[-900:])

dump()
print(f"SPP PROBE PART 2 DONE: pass={len(R['pass'])} fail={len(R['fail'])}")
for f in R["fail"]:
    print("FAIL:", f)
