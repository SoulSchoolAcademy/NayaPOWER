#!/usr/bin/env python3
"""Q10 maker probe — Walk question pages 10/10 fix.
Staged only. Full loop FROM THE LOGIN PAGE at 1440 + 390, spot at 360.
Fresh aliases q10walk1 (1440), q10walk2 (390), q10walk3 (360).
Per-step presentation measurements at EVERY question step, both widths.
Screenshots + results.json are best-effort (EPERM flake may block python
file writes); every measurement prints to stdout as the primary record.
"""
import json
import subprocess
import time
import urllib.request
from playwright.sync_api import sync_playwright

BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
OUT = "/home/hatch/workspace/team-nitro/walk-questions-10-20261112/"
R = {"pass": [], "fail": [], "notes": [], "measure": {}}

def shot(pg, name):
    try:
        pg.screenshot(path=OUT + name)
    except Exception as e:
        R["notes"].append(f"shot {name} skipped: {str(e)[:80]}")

def dump():
    try:
        R["notes"] = [f"pass={len(R['pass'])} fail={len(R['fail'])}"]
        json.dump(R, open(OUT + "q10-results.json", "w"), indent=2)
    except Exception:
        pass

def check(name, ok, detail=""):
    (R["pass"] if ok else R["fail"]).append(name + (" :: " + str(detail) if detail else ""))
    print(("PASS " if ok else "FAIL ") + name + (" :: " + str(detail) if detail else ""))
    try:
        dump()
    except Exception:
        pass

def overflow(pg):
    return pg.evaluate("document.documentElement.scrollWidth + '/' + document.documentElement.clientWidth")

def rgb_ok(color):
    import re
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)", color or "")
    if not m:
        return False, color
    r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
    a = float(m.group(4)) if m.group(4) is not None else 1.0
    return (r >= 200 and g >= 200 and b >= 200 and a >= 0.9), color

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

A1440 = {
    "into": "hello world from the walk - edited by hand",
    "vision": "The intelligent internet. One click, and you're with your people. Always.",
    "mission": "To help ten families in my street start their own small business.",
    "motto": "Small steps every day beat big plans that never start.",
    "goal": "To own my own home and give my children a safe place to grow up.",
    "biz_do": "I bake cakes for birthdays and weddings in my town.",
    "biz_offer": "Fresh cakes made to order, delivered to your door on the day.",
    "biz_building": "I am building a small bakery. The goal is twenty regular customers by Christmas.",
}
A390_INTO = "I'm into people finding each other — the person who loves what you love, doing what you do, anywhere in the world. Because nobody should feel alone in the thing they love.!"
A390 = {
    "into": A390_INTO,
    "vision": "hello world from the walk",
    "mission": "To teach young people the skills I wish someone had taught me.",
    "motto": "Be kind, work hard, and share what you learn.",
    "goal": "To travel to three new countries and learn how other people live.",
    "biz_do": "I fix phones and laptops for people in my area.",
    "biz_offer": "Fast, honest phone repairs with a price agreed before I start.",
    "biz_building": "I am building a repair shop online. The goal is to help one hundred people this year.",
}
# board own-colors: A purple, B blue, C green, Custom gold
OWN_RGB = {"A": "160, 107, 255", "B": "63, 184, 255", "C": "47, 232, 158"}
GOLD_RGB = "255, 191, 61"

MEASURE_JS = """(n) => {
  const step = document.querySelector('#step-' + n);
  if (!step) return {error: 'no step ' + n};
  const main = step.querySelector('.p3-main');
  const boards = [...step.querySelectorAll('.p3-choice')];
  const texts = [...step.querySelectorAll('.p3-choice-text')];
  const edits = [...step.querySelectorAll('.p3-choice-edit')].slice(0,3);
  const eyes = [...step.querySelectorAll('.p3-choice-eye')].slice(0,3);
  const photos = [...step.querySelectorAll('.p3-choice-photo')];
  const letters = [...step.querySelectorAll('.p3-choice-letter')];
  const icons = [...step.querySelectorAll('.p3-choice-icon')];
  const cs = (el, p, pseudo) => getComputedStyle(el, pseudo || null)[p];
  const top = step.querySelector('.p3-choices-top');
  const s123 = [...step.querySelectorAll('.p3-steps123 li')];
  const nums = [...step.querySelectorAll('.p3-step123-n')];
  const custom = step.querySelector('.p3-custom-q');
  const box = (el) => { const r = el.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height)]; };
  return {
    colW: main ? Math.round(main.getBoundingClientRect().width) : null,
    textSize: texts.map(t => parseFloat(cs(t,'fontSize'))),
    textColor: texts.map(t => cs(t,'color')),
    textOpacity: texts.map(t => parseFloat(cs(t,'opacity'))),
    textClip: texts.map(t => t.scrollHeight - t.clientHeight),
    topSize: top ? parseFloat(cs(top,'fontSize')) : null,
    topOpacity: top ? parseFloat(cs(top,'opacity')) : null,
    topColor: top ? cs(top,'color') : null,
    topText: top ? top.textContent.trim().slice(0,120) : null,
    editSize: edits.map(e => parseFloat(cs(e,'fontSize'))),
    eyeBox: eyes.map(box),
    badgeBox: letters.map(box),
    badgeSize: letters.map(l => parseFloat(cs(l,'fontSize'))),
    photoBox: photos.map(box),
    photoSrc: photos.map(p => (p.currentSrc || '').split('/').pop()),
    photoNat: photos.map(p => p.naturalWidth),
    topBar: boards.map(b => cs(b,'backgroundColor','::before')),
    borderColor: boards.map(b => cs(b,'borderColor')),
    iconKey: icons.map(i => i.innerHTML.replace(/\\s+/g,' ').trim()),
    styleNames: [...step.querySelectorAll('.p3-choice-style')].map(s => s.textContent.trim()),
    letters: letters.map(l => l.textContent.trim()),
    s123count: s123.length,
    s123text: s123.map(li => li.textContent.trim()),
    numBox: nums.map(box),
    customTopBar: custom ? cs(custom,'backgroundColor','::before') : null,
    customTextSize: custom ? parseFloat(cs(custom.querySelector('.p3-choice-text') || custom,'fontSize')) : null,
    overflow: document.documentElement.scrollWidth + '/' + document.documentElement.clientWidth
  };
}"""

def measure_step(pg, n, width, tag):
    m = pg.evaluate(MEASURE_JS, n)
    key = f"{tag}-q{n}"
    R["measure"][key] = m
    print(f"MEASURE {key}: " + json.dumps(m)[:1500])
    min_text = 18 if width == 1440 else 17
    min_photo = 72 if width == 1440 else 64
    if m.get("error"):
        check(f"{tag} Q{n} measured", False, m["error"])
        return m
    check(f"{tag} Q{n} column >=1100px at 1440" if width == 1440 else f"{tag} Q{n} column present",
          (m["colW"] or 0) >= 1100 if width == 1440 else (m["colW"] or 0) > 300, f"colW={m['colW']}")
    check(f"{tag} Q{n} choice text >={min_text}px",
          all(s >= min_text for s in m["textSize"]), f"sizes={m['textSize']}")
    check(f"{tag} Q{n} choice text white/lit (never grey)",
          all(rgb_ok(c)[0] for c in m["textColor"]), f"colors={m['textColor']}")
    check(f"{tag} Q{n} choice text opacity 1.0",
          all(o >= 1.0 for o in m["textOpacity"]), f"opacity={m['textOpacity']}")
    check(f"{tag} Q{n} helper >=16px opacity 1.0 white",
          (m["topSize"] or 0) >= 16 and (m["topOpacity"] or 0) >= 1.0 and rgb_ok(m["topColor"] or "")[0],
          f"size={m['topSize']} op={m['topOpacity']} color={m['topColor']}")
    check(f"{tag} Q{n} EDIT >=14px", all(s >= 14 for s in m["editSize"]), f"sizes={m['editSize']}")
    check(f"{tag} Q{n} eye >=40px touch target",
          all(w >= 40 and h >= 40 for w, h in m["eyeBox"]), f"boxes={m['eyeBox']}")
    check(f"{tag} Q{n} letter badge >=44px",
          all(w >= 44 and h >= 44 for w, h in m["badgeBox"]), f"boxes={m['badgeBox']} letters={m['letters']}")
    check(f"{tag} Q{n} Naya picture >={min_photo}px circle, loaded, one per board",
          all(w >= min_photo and h >= min_photo for w, h in m["photoBox"])
          and m["photoSrc"] == ["naya-a.jpg", "naya-b.jpg", "naya-c.jpg"]
          and all(nw > 0 for nw in m["photoNat"]),
          f"boxes={m['photoBox']} src={m['photoSrc']} nat={m['photoNat']}")
    check(f"{tag} Q{n} three boards, three top-bar colors (A purple B blue C green)",
          len(set(m["topBar"])) == 3
          and OWN_RGB["A"] in m["topBar"][0] and OWN_RGB["B"] in m["topBar"][1] and OWN_RGB["C"] in m["topBar"][2],
          f"topBar={m['topBar']}")
    check(f"{tag} Q{n} three DISTINCT icons (no shared eye)",
          len(set(m["iconKey"])) == 3, f"icons={m['iconKey']}")
    check(f"{tag} Q{n} style names A/B/C distinct",
          m["styleNames"] == ["Warm & Plain", "Bold & Short", "Full & Visionary"], f"names={m['styleNames']}")
    check(f"{tag} Q{n} 1-2-3 steps present (3, numbered, big tiles)",
          m["s123count"] == 3 and all(w >= 44 and h >= 44 for w, h in m["numBox"])
          and "Pick the style you like" in m["s123text"][0] and "Make it yours" in m["s123text"][1] and "Press Enter" in m["s123text"][2],
          f"s123={m['s123text']} numBox={m['numBox']}")
    check(f"{tag} Q{n} Full Custom gold top bar",
          GOLD_RGB in (m["customTopBar"] or ""), f"customTopBar={m['customTopBar']}")
    check(f"{tag} Q{n} examples read whole (no clipping)",
          all(d <= 2 for d in m["textClip"]), f"clip={m['textClip']}")
    check(f"{tag} Q{n} overflow 0", m["overflow"].split("/")[0] == m["overflow"].split("/")[1], m["overflow"])
    return m

def hover_boards(pg, n, tag):
    """Rest-vs-hover per board: box-shadow/border must change, glow in the board's own color."""
    for i, key in enumerate(["A", "B", "C"]):
        sel = f"#step-{n} .p3-choice[data-choice='{key}']"
        rest = pg.locator(sel).evaluate("el => getComputedStyle(el).boxShadow + '|' + getComputedStyle(el).borderColor")
        pg.locator(sel).hover()
        pg.wait_for_timeout(500)
        lit = pg.locator(sel).evaluate("el => getComputedStyle(el).boxShadow + '|' + getComputedStyle(el).borderColor")
        check(f"{tag} Q{n} board {key} lights up on hover in its own color",
              rest != lit and OWN_RGB[key] in lit,
              f"rest={rest[:90]} lit={lit[:140]}")

def api_get(path):
    last = None
    for _ in range(3):
        try:
            out = subprocess.run(["curl", "-s", "-A", "Mozilla/5.0 Q10-probe",
                                  BASE + path], capture_output=True, text=True, timeout=40)
            return json.loads(out.stdout)
        except Exception as e:
            last = e
            time.sleep(2)
    raise last

def claim_via_ui(pg, name, alias):
    claim_resp = {}
    def on_resp(resp):
        try:
            if "/api/welcome/claim" in resp.url:
                claim_resp["body"] = resp.text()
                claim_resp["status"] = resp.status
        except Exception:
            pass
    pg.on("response", on_resp)
    pg.goto(BASE + "/", wait_until="networkidle")
    pg.wait_for_timeout(1000)
    check("entry dial name-only (one text input, no code field)",
          pg.locator("input").count() == 1 and pg.locator("#userName").count() == 1,
          f"inputs={pg.locator('input').count()}")
    check("entry returning-citizen choice present",
          pg.locator("#jumpBackIn").count() == 1 and "Jump back in" in pg.locator("#jumpBackIn").inner_text()
          and "New user? Create a new account" in pg.locator("#newAccountLine").inner_text())
    shot(pg, f"q10-entry-{alias}.png")
    pg.fill("#userName", name)
    pg.locator("button.enter[type='submit']").click()
    try:
        pg.wait_for_url("**/identity.html**", timeout=15000)
        check("entry submit lands on certificate", True, pg.url)
    except Exception as e:
        check("entry submit lands on certificate", False, f"{pg.url} :: {str(e)[:100]}")
        return False
    pg.wait_for_timeout(1500)
    try:
        pg.wait_for_selector("#installLater:visible", timeout=9000)
        pg.locator("#installLater").click()
        check("install veil dismissed (Not now)", True)
        pg.wait_for_timeout(500)
    except Exception:
        check("install veil dismissed (Not now)", True, "no veil shown")
    check("certificate alias-only (one input, no name/code field)",
          pg.locator("input").count() == 1 and pg.locator("#aliasInput").count() == 1,
          f"inputs={pg.locator('input').count()}")
    shot(pg, f"q10-identity-{alias}.png")
    pg.fill("#aliasInput", alias)
    pg.locator("#enterBtn").click()
    try:
        pg.wait_for_url("**/welcome**", timeout=25000)
        check("certificate claim lands on the walk", True, pg.url)
    except Exception as e:
        check("certificate claim lands on the walk", False, f"{pg.url} :: {str(e)[:120]}")
        shot(pg, f"q10-identity-stuck-{alias}.png")
        return False
    # join-attribution smoke: the claim response must parse; join rides in it when an SL is present
    if claim_resp.get("body"):
        try:
            cj = json.loads(claim_resp["body"])
            check("claim response parses (join code ran, no error)",
                  claim_resp.get("status") == 200 and cj.get("ok") is not False,
                  f"status={claim_resp.get('status')} keys={sorted(cj.keys())} join={cj.get('join')}")
        except Exception as e:
            check("claim response parses (join code ran, no error)", False, str(e)[:120])
    else:
        R["notes"].append("claim response not captured (no SL in this walk, join expected absent)")
    return True

with sync_playwright() as pw:
    br = pw.firefox.launch()
    stored = "{}"
    # ================= 1440 LEG (q10walk1) =================
    ctx = br.new_context(viewport={"width": 1440, "height": 900})
    ctx.add_init_script(SR_STUB)
    pg = ctx.new_page()
    errs, perrs = [], []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: perrs.append(str(e)))
    ok = claim_via_ui(pg, "Q10 Walk One", "q10walk1")
    if ok:
        pg.wait_for_timeout(1200)
        check("1440 Q1 shown directly (no greeting)", pg.locator("#step-1").is_visible())
        check("1440 Q1 exact words", "Tell me who you are, in your own words" in pg.locator("#step-1").inner_text())
        check("1440 old helper lines gone (no .p3-choices-styles, no .p3-choices-q)",
              pg.locator(".p3-choices-styles").count() == 0 and pg.locator(".p3-choices-q").count() == 0)
        check("1440 old 'Do you want A, B or C?' line is gone",
              "Do you want A, B or C?" not in pg.locator("#step-1").inner_text())
        check("1440 top line kept in plain words",
              "These are examples" in pg.locator("#step-1").inner_text()
              and "click the edit and make it your own" in pg.locator("#step-1").inner_text()
              and "Click the eye for more information" in pg.locator("#step-1").inner_text())
        measure_step(pg, 1, 1440, "1440")
        hover_boards(pg, 1, "1440")
        shot(pg, "q10-q1-1440.png")
        pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        pg.wait_for_timeout(400)
        check("1440 Q1 overflow 0 scrolled", overflow(pg) == "1440/1440", overflow(pg))
        shot(pg, "q10-q1-scrolled-1440.png")
        pg.evaluate("window.scrollTo(0,0)")

        # G — Skip Q1 -> Q2, nothing stored
        pg.click("#skipBtn-1")
        try:
            pg.wait_for_selector("#step-2:visible", timeout=9000)
            check("G skip Q1 lands on Q2", True)
        except Exception as e:
            check("G skip Q1 lands on Q2", False, str(e)[:100])
        check("G skipped Q1 stores nothing",
              pg.evaluate("!('about' in window.__walkState.answers) && document.querySelector('#answer-1').value === ''"),
              str(pg.evaluate("window.__walkState.answers"))[:120])
        measure_step(pg, 2, 1440, "1440")

        # H — Speak on Q2 with the stub
        check("speak button present on Q2", pg.locator("#speakBtn-2").is_visible())
        pg.click("#speakBtn-2")
        pg.wait_for_timeout(200)
        check("H tap Speak shows Listening at once",
              "Listening" in (pg.locator("#speakNote-2").inner_text() or ""),
              pg.locator("#speakNote-2").inner_text()[:60])
        pg.wait_for_timeout(500)
        v_mid = pg.locator("#answer-2").input_value()
        check("H interim transcript lands in the box live", "hello world" in v_mid, v_mid)
        pg.wait_for_timeout(800)
        v_fin = pg.locator("#answer-2").input_value()
        check("H final transcript in the box", v_fin == "hello world from the walk", v_fin)
        pg.locator("#answer-2").click()
        pg.keyboard.press("End")
        pg.keyboard.type(" - edited by hand")
        v_ed = pg.locator("#answer-2").input_value()
        check("H box stays editable after dictation", v_ed == A1440["into"], v_ed)
        shot(pg, "q10-q2-speak-1440.png")
        pg.click("#enterBtn-2")
        try:
            pg.wait_for_selector("#step-3:visible", timeout=9000)
            check("H Enter submits after dictation", True)
        except Exception as e:
            check("H Enter submits after dictation", False, str(e)[:100])

        # Q3 choices: measure + hover + edit B in place + eye nutshells + Enter
        measure_step(pg, 3, 1440, "1440")
        hover_boards(pg, 3, "1440")
        check("I every choice carries EDIT + EYE (4 each on the step)",
              pg.locator("#step-3 .p3-choice-edit").count() == 4 and pg.locator("#step-3 .p3-choice-eye").count() == 4,
              f"edit={pg.locator('#step-3 .p3-choice-edit').count()} eye={pg.locator('#step-3 .p3-choice-eye').count()}")
        check("I choice B is read-only until EDIT",
              pg.locator("#choice-3-B").evaluate("el => el.hasAttribute('readonly')"))
        edit_rest = pg.locator('[data-edit="3-B"]').evaluate("el => getComputedStyle(el).boxShadow")
        pg.locator('[data-edit="3-B"]').hover()
        pg.wait_for_timeout(400)
        edit_lit = pg.locator('[data-edit="3-B"]').evaluate("el => getComputedStyle(el).boxShadow")
        check("I EDIT lights up on hover", edit_rest != edit_lit, f"rest={edit_rest[:80]} lit={edit_lit[:80]}")
        eye_rest = pg.locator('[data-eye="3-B"]').evaluate("el => getComputedStyle(el).boxShadow")
        pg.locator('[data-eye="3-B"]').hover()
        pg.wait_for_timeout(400)
        eye_lit = pg.locator('[data-eye="3-B"]').evaluate("el => getComputedStyle(el).boxShadow")
        check("I EYE lights up on hover", eye_rest != eye_lit, f"rest={eye_rest[:80]} lit={eye_lit[:80]}")
        check("I choice B is Naya's own bold & short answer (verbatim)",
              pg.locator("#choice-3-B").input_value() == "The intelligent internet. One click, and you're with your people.",
              pg.locator("#choice-3-B").input_value())
        pg.locator('[data-eye="3-B"]').click()
        pg.wait_for_timeout(600)
        check("I choice B eye opens its nutshell", pg.locator("#choiceModal").is_visible())
        nut_b = pg.locator("#choiceModal").inner_text()
        check("I nutshell names what/why/connects/for-you",
              "What it is" in nut_b and "Why it matters" in nut_b and "How it connects" in nut_b and "What's in it for you" in nut_b,
              nut_b[:240].replace("\n", " | "))
        pg.locator("#choiceClose").click()
        pg.wait_for_timeout(300)
        pg.locator('[data-eye="3-A"]').click()
        pg.wait_for_timeout(500)
        nut_a = pg.locator("#choiceModal").inner_text()
        check("I choice A eye opens a DIFFERENT nutshell", nut_a != nut_b and "simply" in nut_a,
              nut_a[:160].replace("\n", " | "))
        pg.locator("#choiceClose").click()
        pg.wait_for_timeout(300)
        pg.locator('[data-edit="3-B"]').click()
        pg.wait_for_timeout(300)
        check("I EDIT makes the choice editable in place",
              not pg.locator("#choice-3-B").evaluate("el => el.hasAttribute('readonly')")
              and pg.locator("#choice-3-B").evaluate("el => document.activeElement === el"))
        pg.fill("#choice-3-B", "The intelligent internet. One click, and you're with your people. Always.")
        pg.wait_for_timeout(300)
        check("I edited choice is marked selected",
              pg.locator("#choices-3 .p3-choice[data-choice='B']").evaluate("el => el.classList.contains('selected')"))
        check("I edited choice B holds the edited text", pg.locator("#choice-3-B").input_value() == A1440["vision"])
        # selected board keeps its own-color glow (blue for B)
        sel_glow = pg.locator("#choices-3 .p3-choice[data-choice='B']").evaluate("el => getComputedStyle(el).boxShadow + '|' + getComputedStyle(el).borderColor")
        check("I selected board B keeps its blue glow", OWN_RGB["B"] in sel_glow, sel_glow[:160])
        shot(pg, "q10-q3-choices-1440.png")
        pg.click("#enterBtn-3")
        pg.wait_for_selector("#step-4:visible", timeout=9000)
        check("I Enter submits the edited choice", pg.evaluate("window.__walkState.answers.vision") == A1440["vision"],
              str(pg.evaluate("window.__walkState.answers.vision"))[:120])

        # Q4: measure, Enter-empty no-advance, Full Custom eye, fill, Enter
        measure_step(pg, 4, 1440, "1440")
        pg.click("#enterBtn-4")
        pg.wait_for_timeout(600)
        check("I Enter with nothing edited does not advance",
              pg.locator("#step-4").is_visible() and pg.locator("#enterNote-4").is_visible(),
              pg.locator("#enterNote-4").inner_text()[:80])
        pg.locator('[data-eye="4-custom"]').click()
        pg.wait_for_timeout(500)
        check("I Full Custom eye opens", pg.locator("#choiceModal").is_visible())
        cust = pg.locator("#choiceModal").inner_text()
        check("I Full Custom eye names the three ways",
              "Copy it in from your AI" in cust and "Dictate" in cust and "take one of the examples" in cust,
              cust[:260].replace("\n", " | "))
        pg.locator("#choiceClose").click()
        pg.wait_for_timeout(300)
        pg.fill("#answer-4", A1440["mission"])
        pg.click("#enterBtn-4")
        pg.wait_for_selector("#step-5:visible", timeout=9000)

        # Q5-Q9 typed, measured each step
        typed = [("motto", 5), ("goal", 6), ("biz_do", 7), ("biz_offer", 8), ("biz_building", 9)]
        for key, n in typed:
            measure_step(pg, n, 1440, "1440")
            if n == 5:
                shot(pg, "q10-q5-1440.png")
                pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                pg.wait_for_timeout(300)
                check("1440 Q5 overflow 0 scrolled", overflow(pg) == "1440/1440", overflow(pg))
                pg.evaluate("window.scrollTo(0,0)")
            pg.fill(f"#answer-{n}", A1440[key])
            pg.click(f"#enterBtn-{n}")
            nxt = f"#step-{n+1}" if n < 9 else "#step-10"
            try:
                pg.wait_for_selector(nxt + ":visible", timeout=9000)
                check(f"Q{n} advances", True)
            except Exception as e:
                check(f"Q{n} advances", False, str(e)[:100])

        # Q10: measure, hover, then Skip
        measure_step(pg, 10, 1440, "1440")
        hover_boards(pg, 10, "1440")
        shot(pg, "q10-q10-1440.png")
        check("skip present on Q10", pg.locator("#skipBtn-10").is_visible())
        pg.click("#skipBtn-10")
        try:
            pg.wait_for_selector("#step-names:visible", timeout=9000)
            check("G skip Q10 lands on the names page", True)
        except Exception as e:
            check("G skip Q10 lands on the names page", False, str(e)[:100])
        check("G skipped Q10 stores nothing",
              pg.evaluate("!('space' in window.__walkState.answers)"),
              str(pg.evaluate("window.__walkState.answers"))[:200])
        check("names page visible", pg.locator("#step-names").is_visible())
        check("overflow 0 at 1440 names", overflow(pg) == "1440/1440", overflow(pg))
        shot(pg, "q10-names-1440.png")
        check("B2 personal slug prefilled from alias", pg.locator("#url-personal").input_value() == "q10walk1", pg.locator("#url-personal").input_value())
        pg.fill("#name-business", "My Cool Biz")
        pg.wait_for_timeout(300)
        check("B2 business slug follows the name live", pg.locator("#url-business").input_value() == "my-cool-biz", pg.locator("#url-business").input_value())
        pg.fill("#name-space", "The Garden")
        pg.wait_for_timeout(300)
        check("B2 space slug follows the name live", pg.locator("#url-space").input_value() == "the-garden", pg.locator("#url-space").input_value())
        pg.click("#enterBtn-11")
        try:
            pg.wait_for_selector("#step-building:visible", timeout=9000)
            check("building page visible", True)
        except Exception as e:
            check("building page visible", False, str(e)[:100])
        try:
            pg.wait_for_selector("text=Done — here are your pages.", timeout=25000)
            check("building reaches done", True)
        except Exception as e:
            check("building reaches done", False, str(e)[:100])
        check("overflow 0 at 1440 building", overflow(pg) == "1440/1440", overflow(pg))
        shot(pg, "q10-building-done-1440.png")
        n_links = pg.locator(".p3-build-link").count()
        check("D three building links shown", n_links == 3, f"count={n_links}")
        link_hrefs = [pg.locator(".p3-build-link").nth(i).get_attribute("href") for i in range(3)]
        link_titles = [pg.locator(".p3-build-link").nth(i).inner_text() for i in range(3)]
        check("D building links carry the typed titles",
              "q10walk1" in link_titles[0] and "My Cool Biz" in link_titles[1] and "The Garden" in link_titles[2],
              str(link_titles))
        check("D building links point at staging pages",
              all(h and "/pages/q10walk1/" in h for h in link_hrefs), str(link_hrefs))
        pg.locator(".p3-build-link").nth(0).click()
        pg.wait_for_timeout(1500)
        check("D click Personal link lands on the created page",
              "/pages/q10walk1/" in pg.url and "q10walk1" in pg.locator("body").inner_text(), pg.url)
        shot(pg, "q10-page-personal-1440.png")
        pg.goto(BASE + "/welcome", wait_until="networkidle")
        pg.wait_for_timeout(1000)
        check("reload returns to end slide (stored reveal)", pg.locator("#step-end").is_visible())
        for kind, title, section in [(1, "My Cool Biz", "Nutshell"), (2, "The Garden", "Why it matters")]:
            p2 = ctx.new_page()
            p2.goto(link_hrefs[kind], wait_until="networkidle")
            p2.wait_for_timeout(800)
            check(f"D building link {kind+1} lands on its created page",
                  title in p2.locator("body").inner_text() and section in p2.locator("body").inner_text(), p2.url)
            p2.close()
        pg.evaluate("window.scrollTo(0,0)")
        check("end slide congratulations", "Congratulations, you're hired." in pg.locator("#step-end").inner_text())
        check("overflow 0 at 1440 end", overflow(pg) == "1440/1440", overflow(pg))
        shot(pg, "q10-end-1440.png")
        pg.locator('[data-door="Personal"]').click()
        pg.wait_for_timeout(1500)
        check("Personal door lands on the created staging page",
              "/pages/q10walk1/" in pg.url and "q10walk1" in pg.locator("body").inner_text(), pg.url)
        pg.goto(BASE + "/welcome", wait_until="networkidle")
        pg.wait_for_timeout(1000)
        pg.locator('[data-door="Hub"]').click()
        pg.wait_for_timeout(1500)
        check("Hub door lands on the staging Hub", "/hub?alias=q10walk1" in pg.url, pg.url)
        hub_txt = pg.locator("body").inner_text()
        check("E Hub shows the three pages by typed titles",
              "q10walk1" in hub_txt and "My Cool Biz" in hub_txt and "The Garden" in hub_txt,
              hub_txt[:200].replace("\n", " | "))
        check("overflow 0 at 1440 Hub", overflow(pg) == "1440/1440", overflow(pg))
        shot(pg, "q10-hub-1440.png")
        pg.locator(".hcard").nth(1).click()
        pg.wait_for_timeout(1200)
        check("E Hub card click opens the Business page",
              "/pages/q10walk1/my-cool-biz" in pg.url and "My Cool Biz" in pg.locator("body").inner_text(), pg.url)
        stored = pg.evaluate("JSON.stringify(Object.fromEntries(Object.entries(localStorage)))")
        check("1440 console errors", len(errs) == 0, f"{len(errs)}: {errs[:3]}")
        check("1440 pageerrors", len(perrs) == 0, f"{len(perrs)}: {perrs[:3]}")
    ctx.close()
    dump()

    # ================= READ-BACKS q10walk1 (independent, no browser) =================
    box = api_get("/api/welcome/box?alias=q10walk1")
    check("A exactly one Box record for q10walk1", box.get("box_count") == 1, str(box.get("box_count")))
    b = box.get("box") or {}
    check("A Box table named citizen_worlds", b.get("table") == "citizen_worlds", str(b.get("table")))
    check("A Box store reported", b.get("store") in ("citizen_worlds", "kv-fallback"), str(b.get("store")))
    ans = (b.get("answers") or {})
    missing = [k for k in A1440 if ans.get(k) != A1440[k]]
    check("C all eight given answers word for word in the Box", not missing, f"mismatch={missing}")
    check("C skipped Q1 stores nothing (no 'about' key)", "about" not in ans, str(sorted(ans.keys())))
    check("C skipped Q10 stores nothing (no 'space' key)", "space" not in ans, str(sorted(ans.keys())))
    pn = ((b.get("settings") or {}).get("pageNames") or {})
    check("C edited business slug read back in the Box", (pn.get("business") or {}).get("slug") == "my-cool-biz", str(pn))
    check("C space slug read back in the Box", (pn.get("space") or {}).get("slug") == "the-garden", str(pn))
    check("A exactly one live project row", box.get("project_count") == 1, str(box.get("project_count")))
    check("A project row is the citizen's", (box.get("project_rows") or [{}])[0].get("owner_alias") == "q10walk1",
          str(box.get("project_rows"))[:200])
    pages = [p for p in (box.get("pages") or []) if p]
    check("B three pages read back", len(pages) == 3, f"count={len(pages)}")
    by_kind = {(p.get("page_kind") or p.get("kind")): p for p in pages}
    check("B personal page: typed title + citizen words",
          by_kind.get("personal", {}).get("headline") == "q10walk1" and "hello world from the walk" in by_kind.get("personal", {}).get("body", ""),
          str(by_kind.get("personal", {}).get("headline")))
    check("B business page: typed title + citizen words",
          by_kind.get("business", {}).get("headline") == "My Cool Biz" and "I bake cakes" in by_kind.get("business", {}).get("body", ""),
          str(by_kind.get("business", {}).get("headline")))
    check("B space page: typed title + citizen words",
          by_kind.get("space", {}).get("headline") == "The Garden" and "The intelligent internet" in by_kind.get("space", {}).get("body", ""),
          str(by_kind.get("space", {}).get("headline")))
    comp = api_get("/api/welcome/complete?alias=q10walk1")
    check("completion read-back holds the answers", (comp.get("answers") or {}).get("motto") == A1440["motto"])
    box3 = api_get("/api/welcome/box?alias=q10nevercompleted")
    check("A no Box for an alias that never completed", box3.get("box_count") == 0 and box3.get("project_count") == 0)
    dump()

    # ================= 390 LEG (q10walk2) =================
    ctx2 = br.new_context(viewport={"width": 390, "height": 844})
    ctx2.add_init_script(SR_STUB)
    p2 = ctx2.new_page()
    errs2, perrs2 = [], []
    p2.on("console", lambda m: errs2.append(m.text) if m.type == "error" else None)
    p2.on("pageerror", lambda e: perrs2.append(str(e)))
    ok2 = claim_via_ui(p2, "Q10 Walk Two", "q10walk2")
    if ok2:
        p2.wait_for_timeout(1000)
        check("390 Q1 shown directly", p2.locator("#step-1").is_visible())
        measure_step(p2, 1, 390, "390")
        hover_boards(p2, 1, "390")
        shot(p2, "q10-q1-390.png")
        p2.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        p2.wait_for_timeout(300)
        check("390 Q1 overflow 0 scrolled", overflow(p2) == "390/390", overflow(p2))
        p2.evaluate("window.scrollTo(0,0)")
        p2.click("#skipBtn-1")
        p2.wait_for_selector("#step-2:visible", timeout=9000)
        check("390 G skip Q1 lands on Q2", True)
        measure_step(p2, 2, 390, "390")
        check("390 old 'Do you want A, B or C?' line is gone",
              "Do you want A, B or C?" not in p2.locator("#step-2").inner_text())
        check("390 1-2-3 present", "Pick the style you like" in p2.locator("#step-2").inner_text())
        p2.locator('[data-eye="2-A"]').click()
        p2.wait_for_timeout(500)
        check("390 I choice A eye opens its nutshell", p2.locator("#choiceModal").is_visible()
              and "What it is" in p2.locator("#choiceModal").inner_text())
        p2.locator("#choiceClose").click()
        p2.wait_for_timeout(300)
        p2.locator('[data-edit="2-A"]').click()
        p2.wait_for_timeout(300)
        check("390 I EDIT unlocks choice A",
              not p2.locator("#choice-2-A").evaluate("el => el.hasAttribute('readonly')"))
        p2.fill("#choice-2-A", A390_INTO)
        p2.wait_for_timeout(300)
        check("390 I edited choice A is selected",
              p2.locator("#choices-2 .p3-choice[data-choice='A']").evaluate("el => el.classList.contains('selected')"))
        shot(p2, "q10-q2-choices-390.png")
        p2.click("#enterBtn-2")
        p2.wait_for_selector("#step-3:visible", timeout=9000)
        measure_step(p2, 3, 390, "390")
        p2.click("#speakBtn-3")
        p2.wait_for_timeout(1400)
        check("390 H transcript lands live in the box", "hello world" in p2.locator("#answer-3").input_value(), p2.locator("#answer-3").input_value())
        p2.click("#enterBtn-3")
        p2.wait_for_selector("#step-4:visible", timeout=9000)
        rest390 = {4: A390["mission"], 5: A390["motto"], 6: A390["goal"],
                   7: A390["biz_do"], 8: A390["biz_offer"], 9: A390["biz_building"]}
        for n, txt in rest390.items():
            measure_step(p2, n, 390, "390")
            if n == 5:
                shot(p2, "q10-q5-390.png")
            p2.fill(f"#answer-{n}", txt)
            p2.click(f"#enterBtn-{n}")
            nxt = f"#step-{n+1}" if n < 9 else "#step-10"
            p2.wait_for_selector(nxt + ":visible", timeout=9000)
        measure_step(p2, 10, 390, "390")
        shot(p2, "q10-q10-390.png")
        p2.click("#skipBtn-10")
        p2.wait_for_selector("#step-names:visible", timeout=9000)
        check("390 G skip Q10 lands on names", True)
        check("390 overflow 0 at names", overflow(p2) == "390/390", overflow(p2))
        p2.fill("#name-business", "Phone Fixers")
        p2.wait_for_timeout(300)
        check("390 B2 slug follows name live", p2.locator("#url-business").input_value() == "phone-fixers", p2.locator("#url-business").input_value())
        p2.fill("#url-business", "fixers-390")
        p2.wait_for_timeout(200)
        check("390 B2 edited slug kept", p2.locator("#url-business").input_value() == "fixers-390")
        p2.fill("#name-space", "Fixers Club")
        shot(p2, "q10-names-390.png")
        p2.click("#enterBtn-11")
        p2.wait_for_selector("text=Done — here are your pages.", timeout=25000)
        check("390 building reaches done", True)
        check("390 overflow 0 at building", overflow(p2) == "390/390", overflow(p2))
        check("390 D three building links shown", p2.locator(".p3-build-link").count() == 3)
        p2.locator(".p3-build-link").nth(2).click()
        p2.wait_for_timeout(1500)
        check("390 D click Space link lands on the created page",
              "/pages/q10walk2/" in p2.url and "Fixers Club" in p2.locator("body").inner_text(), p2.url)
        shot(p2, "q10-page-space-390.png")
        p2.goto(BASE + "/hub?alias=q10walk2", wait_until="networkidle")
        p2.wait_for_timeout(800)
        hub2 = p2.locator("body").inner_text()
        check("390 E Hub shows the three pages by typed titles",
              "q10walk2" in hub2 and "Phone Fixers" in hub2 and "Fixers Club" in hub2, hub2[:200].replace("\n", " | "))
        check("390 overflow 0 at Hub", overflow(p2) == "390/390", overflow(p2))
        shot(p2, "q10-hub-390.png")
        check("390 console errors", len(errs2) == 0, f"{len(errs2)}: {errs2[:3]}")
        check("390 pageerrors", len(perrs2) == 0, f"{len(perrs2)}: {perrs2[:3]}")
    ctx2.close()
    dump()

    # read-back q10walk2
    boxB = api_get("/api/welcome/box?alias=q10walk2")
    bB = boxB.get("box") or {}
    ansB = (bB.get("answers") or {})
    missingB = [k for k in A390 if ansB.get(k) != A390[k]]
    check("390 C all eight given answers word for word in the Box", not missingB, f"mismatch={missingB}")
    check("390 C skipped Q1/Q10 store nothing", "about" not in ansB and "space" not in ansB, str(sorted(ansB.keys())))
    check("390 A exactly one Box record", boxB.get("box_count") == 1, str(boxB.get("box_count")))

    # ================= 360 LEG =================
    ctx3 = br.new_context(viewport={"width": 360, "height": 800})
    ctx3.add_init_script(SR_STUB)
    p3 = ctx3.new_page()
    errs3, perrs3 = [], []
    p3.on("console", lambda m: errs3.append(m.text) if m.type == "error" else None)
    p3.on("pageerror", lambda e: perrs3.append(str(e)))
    ok3 = claim_via_ui(p3, "Q10 Walk Three", "q10walk3")
    if ok3:
        p3.wait_for_timeout(1000)
        check("360 Q1 shown directly", p3.locator("#step-1").is_visible())
        measure_step(p3, 1, 360, "360")
        shot(p3, "q10-q1-360.png")
        p3.click("#skipBtn-1")
        p3.wait_for_selector("#step-2:visible", timeout=9000)
        measure_step(p3, 2, 360, "360")
        p3.fill("#answer-2", "I love making things with my hands.")
        p3.click("#enterBtn-2")
        p3.wait_for_selector("#step-3:visible", timeout=9000)
        measure_step(p3, 3, 360, "360")
    # seeded completed -> end slide at 360 (q10walk1 localStorage)
    p3.goto(BASE + "/welcome", wait_until="networkidle")
    p3.evaluate(f"const s={stored}; for (const k in s) localStorage.setItem(k, s[k]);")
    p3.goto(BASE + "/welcome", wait_until="networkidle")
    p3.wait_for_timeout(1200)
    check("360 seeded completed -> end slide direct", p3.locator("#step-end").is_visible())
    check("360 overflow 0 at end", overflow(p3) == "360/360", overflow(p3))
    shot(p3, "q10-end-360.png")
    p3.goto(BASE + "/hub?alias=q10walk1", wait_until="networkidle")
    p3.wait_for_timeout(800)
    check("360 Hub shows the pages", "My Cool Biz" in p3.locator("body").inner_text())
    check("360 overflow 0 at Hub", overflow(p3) == "360/360", overflow(p3))
    p3.goto(BASE + "/pages/q10walk1/my-cool-biz", wait_until="networkidle")
    p3.wait_for_timeout(800)
    check("360 page renders the title", "My Cool Biz" in p3.locator("body").inner_text())
    check("360 overflow 0 at page", overflow(p3) == "360/360", overflow(p3))
    check("360 console errors", len(errs3) == 0, f"{len(errs3)}: {errs3[:3]}")
    check("360 pageerrors", len(perrs3) == 0, f"{len(perrs3)}: {perrs3[:3]}")
    ctx3.close()
    br.close()

R["notes"] = [f"pass={len(R['pass'])} fail={len(R['fail'])}"]
dump()
print(f"=== Q10 PROBE DONE: PASS {len(R['pass'])} / FAIL {len(R['fail'])} ===")
for f in R["fail"]:
    print("FAIL:", f)
