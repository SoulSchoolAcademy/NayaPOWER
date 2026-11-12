#!/usr/bin/env python3
"""NEW-ACCOUNT BUG verify v3 (Shawn 22:36Z) — AFTER the fix + heal + pair rule.
Re-run of v2 with fresh aliases/profiles: the v2 run was killed by the
runtime restart after 1 check, and /tmp was wiped (profiles gone, v1/v2
aliases already claimed). Leg 0 (heal): claim healwalk1, POISON the stored
name to "Mike" deliberately (the old walk ingest's damage), load
/identity.html with no ?name= -> restore paints Heal Walker (registry
truth) and heals the stored name.
(a) Fresh persistent profile holding bugowner9 (claimed + walked): new name
    Mike + Create a new account -> certificate composes for MIKE (alias
    field open), claim mike8, walk Q1-Q10 fresh, end slide + pages.
(b) Same browser after (a): Jump back in as Bug Owner still lands on Bug
    Owner's Hub; identity?name=Bug Owner stays composing, typing bugowner9
    certifies as Bug Owner.
(c) Fresh browser: whole S2 flow still works (regression).
Writes bug-verify-*.png + bug-verify-results.json into the work dir.
"""
import json
import subprocess
import time
from playwright.sync_api import sync_playwright

BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
OUT = "/home/hatch/workspace/team-nitro/walk/end-slide-10-20261112/"
PROFILE_OLD = "/tmp/bug3-profile-poison"
PROFILE_NEW = "/tmp/bug3-profile-main"
R = {"pass": [], "fail": [], "notes": []}

def dump():
    R["notes"] = [f"pass={len(R['pass'])} fail={len(R['fail'])}"]
    json.dump(R, open(OUT + "bug-verify-results.json", "w"), indent=2)

def check(name, ok, detail=""):
    (R["pass"] if ok else R["fail"]).append(name + (" :: " + str(detail) if detail else ""))
    try:
        dump()
    except Exception:
        pass

def overflow(pg):
    return pg.evaluate("document.documentElement.scrollWidth + '/' + document.documentElement.clientWidth")

def dismiss_veil(pg):
    try:
        pg.wait_for_selector("#installLater:visible", timeout=8000)
        pg.locator("#installLater").click()
        pg.wait_for_timeout(500)
        return True
    except Exception:
        return False

def cert_state(pg):
    return pg.evaluate("""() => {
      const q = s => { const el = document.querySelector(s); return el ? el.innerText : 'MISSING:' + s; };
      const vis = s => { const el = document.querySelector(s); if (!el) return 'MISSING'; const cs = getComputedStyle(el); return (cs.display === 'none' || el.hidden) ? 'hidden' : 'visible'; };
      return {
        displayName: q('#displayName'),
        status: q('#aliasStatus'),
        certNo: q('#certNoValue'),
        link: q('#displayLink'),
        plaqueCertified: (document.querySelector('#certPlaque') || {classList:{contains:()=>false}}).classList.contains('is-certified'),
        aliasFieldWrapper: vis('.alias-field-wrapper'),
        aliasInputValue: (document.querySelector('#aliasInput') || {}).value,
      };
    }""")

def api_get(path):
    last = None
    for _ in range(3):
        try:
            out = subprocess.run(["curl", "-s", "-A", "Mozilla/5.0 bugfix-probe",
                                  BASE + path], capture_output=True, text=True, timeout=40)
            return json.loads(out.stdout)
        except Exception as e:
            last = e
            time.sleep(2)
    raise last

ANS = {
    1: "I am a baker from the valley, growing food for my neighbours.",
    2: "I am into growing food and sharing the harvest.",
    3: "A street where every garden feeds a family.",
    4: "To turn ten front gardens into food gardens this year.",
    5: "Grow a little every day.",
    6: "To own a small farm and teach children to grow food.",
    7: "I grow vegetables and sell boxes of fresh food each week.",
    8: "A weekly box of fresh vegetables, picked the same morning.",
    9: "I am building a market garden. The goal is fifty weekly boxes.",
    10: "A garden room for growers and cooks, where we swap seeds and recipes.",
}
MIKE = {
    1: "I am Mike, a mechanic who keeps old cars running.",
    2: "I am into fixing engines and teaching young people how they work.",
    3: "A town where no good car is scrapped for a small fault.",
    4: "To keep one hundred old cars on the road this year.",
    5: "Fix it right, or don't fix it at all.",
    6: "To open my own garage and train two apprentices.",
    7: "I repair cars and vans for people in my area.",
    8: "Honest car repairs with the price agreed before I start.",
    9: "I am building a mobile mechanic service. The goal is fifty regular customers.",
    10: "A garage room for drivers and makers, where we swap tools and stories.",
}
FRESH = {
    2: "I am into mending clothes and keeping them out of landfill.",
    3: "A town where nothing useful is thrown away.",
    4: "To teach ten neighbours to mend their own clothes this year.",
    5: "Mend it first, buy it last.",
    6: "To open a repair cafe where anyone can bring a broken thing.",
    7: "I mend clothes and curtains for people in my area.",
    8: "Careful mending with the price agreed before I start.",
    9: "I am building a mending circle online. The goal is one hundred mends this year.",
}

with sync_playwright() as pw:
    # ================= LEG 0: HEAL the poisoned profile =================
    # The old walk ingest overwrote the stored name ("Mike") while the
    # registry still holds the truth ("Heal Walker"). The /tmp profiles were
    # wiped by the restart, so poison it deliberately: claim healwalk1, then
    # overwrite the stored name with "Mike", then load /identity.html with
    # no ?name= — the fix must restore the registry truth + heal.
    ctx0 = pw.firefox.launch_persistent_context(PROFILE_OLD, viewport={"width": 1440, "height": 900})
    p0 = ctx0.new_page()
    p0.goto(BASE + "/", wait_until="networkidle")
    p0.wait_for_timeout(1000)
    check("(0) setup: fresh entry dial (one input)", p0.locator("input").count() == 1)
    p0.fill("#userName", "Heal Walker")
    p0.locator("button.enter[type='submit']").click()
    p0.wait_for_url("**/identity.html**", timeout=15000)
    dismiss_veil(p0)
    p0.fill("#aliasInput", "healwalk1")
    p0.locator("#enterBtn").click()
    p0.wait_for_url("**/welcome**", timeout=25000)
    check("(0) setup: healwalk1 claimed, stored identity is Heal Walker",
          p0.evaluate("localStorage.getItem('nayanet_smart_alias')") == "healwalk1"
          and p0.evaluate("localStorage.getItem('nayanet_smart_name')") == "Heal Walker")
    p0.evaluate("""() => {
      localStorage.setItem('nayanet_smart_name', 'Mike');
      const l = JSON.parse(localStorage.getItem('nayanet_smart_identities') || '[]');
      l.forEach(x => { if (x.alias === 'healwalk1') x.name = 'Mike'; });
      localStorage.setItem('nayanet_smart_identities', JSON.stringify(l));
    }""")
    poisoned = p0.evaluate("() => localStorage.getItem('nayanet_smart_name') + ' / ' + localStorage.getItem('nayanet_smart_identities')")
    check("(0) poisoned profile state before restore (stored name = Mike, registry = Heal Walker)",
          "Mike" in poisoned, poisoned)
    p0.goto(BASE + "/identity.html", wait_until="networkidle")
    p0.wait_for_timeout(2500)
    dismiss_veil(p0)
    p0.wait_for_timeout(1500)
    st0 = cert_state(p0)
    print("CERT HEAL:", json.dumps(st0))
    check("(0) no-?name= restore still paints the registry truth (Heal Walker)",
          st0["displayName"].strip() == "Heal Walker" and "welcome back" in st0["status"], str(st0))
    check("(0) HEAL: stored name corrected back to Heal Walker",
          p0.evaluate("localStorage.getItem('nayanet_smart_name')") == "Heal Walker",
          p0.evaluate("localStorage.getItem('nayanet_smart_name')"))
    check("(0) HEAL: remembered identity name corrected too",
          "Heal Walker" in (p0.evaluate("localStorage.getItem('nayanet_smart_identities')") or ""),
          p0.evaluate("localStorage.getItem('nayanet_smart_identities')"))
    p0.screenshot(path=OUT + "bug-verify-healed.png")
    ctx0.close()
    dump()

    # ================= SETUP: fresh persistent profile, stored bugowner9 =================
    ctx = pw.firefox.launch_persistent_context(PROFILE_NEW, viewport={"width": 1440, "height": 900})
    pg = ctx.new_page()
    errs, perrs = [], []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: perrs.append(str(e)))
    pg.goto(BASE + "/", wait_until="networkidle")
    pg.wait_for_timeout(1000)
    check("setup: fresh entry dial (one input)", pg.locator("input").count() == 1)
    pg.fill("#userName", "Bug Owner")
    pg.locator("button.enter[type='submit']").click()
    pg.wait_for_url("**/identity.html**", timeout=15000)
    dismiss_veil(pg)
    pg.fill("#aliasInput", "bugowner9")
    pg.locator("#enterBtn").click()
    pg.wait_for_url("**/welcome**", timeout=25000)
    check("setup: claim bugowner9 lands on the walk", True, pg.url)
    pg.wait_for_timeout(1200)
    for n in range(1, 11):
        pg.fill(f"#answer-{n}", ANS[n])
        pg.click(f"#enterBtn-{n}")
        nxt = f"#step-{n+1}" if n < 10 else "#step-names"
        pg.wait_for_selector(nxt + ":visible", timeout=9000)
    pg.fill("#name-business", "Bug Bakery")
    pg.fill("#name-space", "Bug Garden")
    pg.wait_for_timeout(300)
    pg.click("#enterBtn-11")
    pg.wait_for_selector("text=Done — here are your pages.", timeout=25000)
    check("setup: building done (reveal exists)", True)
    pg.click("#buildGo")
    pg.wait_for_selector("#step-end:visible", timeout=9000)
    check("setup: stored citizen reaches the end slide", pg.locator("#step-end").is_visible())
    check("setup: stored identity is bugowner9 / Bug Owner (never poisoned)",
          pg.evaluate("localStorage.getItem('nayanet_smart_alias')") == "bugowner9"
          and pg.evaluate("localStorage.getItem('nayanet_smart_name')") == "Bug Owner")

    # ================= (a) RETURNING BROWSER, NEW ACCOUNT =================
    pg.goto(BASE + "/", wait_until="networkidle")
    pg.wait_for_timeout(1200)
    check("(a) returning view shown for the stored profile",
          pg.locator("#returningView").is_visible())
    pg.locator("#newAccountLine").click()
    pg.wait_for_timeout(500)
    check("(a) Create a new account reveals the dial", pg.locator("#entryForm").is_visible())
    pg.fill("#userName", "Mike")
    pg.locator("button.enter[type='submit']").click()
    pg.wait_for_url("**/identity.html**", timeout=15000)
    pg.wait_for_timeout(2500)
    dismiss_veil(pg)
    pg.wait_for_timeout(1500)
    check("(a) certificate URL carries the new name whole", "name=Mike" in pg.url, pg.url)
    st = cert_state(pg)
    print("CERT MIKE:", json.dumps(st))
    check("(a) FIX: certificate does NOT show the old name",
          st["displayName"].strip() == "", str(st))
    check("(a) FIX: no welcome-back for the old profile",
          "welcome back" not in st["status"], st["status"])
    check("(a) FIX: plaque is NOT certified for the new citizen",
          st["plaqueCertified"] is False, str(st))
    check("(a) FIX: alias field is OPEN (wrapper visible)",
          st["aliasFieldWrapper"] == "visible", str(st))
    check("(a) FIX: no old certificate number painted",
          st["certNo"].strip() == "", st["certNo"])
    pg.screenshot(path=OUT + "bug-verify-cert-mike.png")
    pg.fill("#aliasInput", "mike8")
    pg.wait_for_timeout(2500)
    st2 = cert_state(pg)
    check("(a) typing the alias echoes the NEW name (Mike7)",
          st2["displayName"].strip() == "Mike7", str(st2))
    check("(a) new alias is available to claim",
          "Available" in st2["status"] and "mike8.nayanet.app" in st2["link"], str(st2))
    pg.locator("#enterBtn").click()
    try:
        pg.wait_for_url("**/welcome**", timeout=25000)
        check("(a) claim lands on the walk (not the end slide)", True, pg.url)
    except Exception as e:
        check("(a) claim lands on the walk (not the end slide)", False, f"{pg.url} :: {str(e)[:120]}")
        raise SystemExit(1)
    pg.wait_for_timeout(1200)
    check("(a) FIX: Mike sees Q1 fresh — the ten questions, not the end slide",
          pg.locator("#step-1").is_visible() and pg.locator("#step-end").is_hidden())
    check("(a) stored identity is now Mike (pair rule: name stored with its alias)",
          pg.evaluate("localStorage.getItem('nayanet_smart_alias')") == "mike8"
          and pg.evaluate("localStorage.getItem('nayanet_smart_name')") == "Mike")
    check("(a) identities list holds BOTH profiles (adds, never replaces)",
          pg.evaluate("() => { const l = JSON.parse(localStorage.getItem('nayanet_smart_identities') || '[]'); return l.map(x => x.alias).join(','); }") == "mike8,bugowner9",
          pg.evaluate("localStorage.getItem('nayanet_smart_identities')"))
    for n in range(1, 11):
        pg.fill(f"#answer-{n}", MIKE[n])
        pg.click(f"#enterBtn-{n}")
        nxt = f"#step-{n+1}" if n < 10 else "#step-names"
        pg.wait_for_selector(nxt + ":visible", timeout=9000)
    check("(a) Mike walks all ten questions", True)
    pg.fill("#name-business", "Mike's Fix-It")
    pg.fill("#name-space", "Mike's Room")
    pg.wait_for_timeout(300)
    pg.click("#enterBtn-11")
    pg.wait_for_selector("text=Done — here are your pages.", timeout=25000)
    check("(a) Mike's building reaches done", True)
    pg.click("#buildGo")
    pg.wait_for_selector("#step-end:visible", timeout=9000)
    check("(a) Mike's end slide shows his Smart Link",
          pg.locator("#linkFace").inner_text() == "nayanet.app/mike8", pg.locator("#linkFace").inner_text())
    check("(a) Mike's world cards carry his titles + words",
          "Mike's Fix-It" in pg.locator("#step-end").inner_text()
          and "I repair cars and vans" in pg.locator("#step-end").inner_text()
          and "Mike's Room" in pg.locator("#step-end").inner_text())
    check("(a) Mike's agreement board present",
          pg.locator("#dealBoard").count() == 1)
    check("(a) overflow 0 on Mike's end slide", overflow(pg) == "1440/1440", overflow(pg))
    pg.screenshot(path=OUT + "bug-verify-mike-end.png")
    check("(a) console errors", len(errs) == 0, f"{len(errs)}: {errs[:3]}")
    check("(a) pageerrors", len(perrs) == 0, f"{len(perrs)}: {perrs[:3]}")
    ctx.close()
    dump()

    # ================= (a) READ-BACK: Mike's Box + pages; old profile untouched =================
    box = api_get("/api/welcome/box?alias=mike8")
    check("(a) exactly one Box record for mike8", box.get("box_count") == 1, str(box.get("box_count")))
    ans = ((box.get("box") or {}).get("answers") or {})
    pairs = [("about", MIKE[1]), ("into", MIKE[2]), ("vision", MIKE[3]), ("mission", MIKE[4]),
             ("motto", MIKE[5]), ("goal", MIKE[6]), ("biz_do", MIKE[7]), ("biz_offer", MIKE[8]),
             ("biz_building", MIKE[9]), ("space", MIKE[10])]
    missing = [k for k, v in pairs if ans.get(k) != v]
    check("(a) all ten of Mike's answers word for word in the Box", not missing, f"mismatch={missing}")
    check("(a) exactly one live project row for mike8", box.get("project_count") == 1, str(box.get("project_count")))
    pages = [p for p in (box.get("pages") or []) if p]
    check("(a) three pages read back for mike8", len(pages) == 3, f"count={len(pages)}")
    box_old = api_get("/api/welcome/box?alias=bugowner9")
    check("(a) old profile's Box still exactly one", box_old.get("box_count") == 1, str(box_old.get("box_count")))
    check("(a) old profile's project still exactly one", box_old.get("project_count") == 1, str(box_old.get("project_count")))
    dump()

    # ================= (b) SAME BROWSER: JUMP BACK IN AS BUG OWNER =================
    ctx2 = pw.firefox.launch_persistent_context(PROFILE_NEW, viewport={"width": 1440, "height": 900})
    p2 = ctx2.new_page()
    errs2, perrs2 = [], []
    p2.on("console", lambda m: errs2.append(m.text) if m.type == "error" else None)
    p2.on("pageerror", lambda e: perrs2.append(str(e)))
    # ?name= for a known other stays composing WHILE current is still Mike;
    # typing the old alias certifies it (the live check is the truth).
    p2.goto(BASE + "/identity.html?name=Bug%20Owner", wait_until="networkidle")
    p2.wait_for_timeout(2500)
    dismiss_veil(p2)
    p2.wait_for_timeout(1500)
    st3 = cert_state(p2)
    print("CERT KNOWN-OTHER BY NAME:", json.dumps(st3))
    check("(b) identity?name=Bug Owner stays composing (no silent restore of another)",
          st3["displayName"].strip() == "" and st3["plaqueCertified"] is False
          and st3["aliasFieldWrapper"] == "visible", str(st3))
    p2.fill("#aliasInput", "bugowner9")
    p2.wait_for_timeout(2500)
    st3b = cert_state(p2)
    check("(b) typing the old alias certifies as Bug Owner (live check is the truth)",
          st3b["displayName"].strip() == "Bug Owner" and "welcome back" in st3b["status"], str(st3b))
    # Now the Jump: entry offers the other profile; clicking it switches current.
    p2.goto(BASE + "/", wait_until="networkidle")
    p2.wait_for_timeout(1200)
    check("(b) returning view offers the OTHER profile too",
          p2.locator("#returningOthers").is_visible()
          and "Jump back in as Bug Owner" in p2.locator("#returningOthers").inner_text(),
          p2.locator("#returningOthers").inner_text()[:200])
    p2.screenshot(path=OUT + "bug-verify-others.png")
    p2.locator(".returning-other").click()
    p2.wait_for_timeout(2000)
    check("(b) Jump back in as Bug Owner lands on Bug Owner's Hub",
          "/hub?" in p2.url and "alias=bugowner9" in p2.url, p2.url)
    hub_txt = p2.locator("body").inner_text()
    check("(b) Bug Owner's Hub lists Bug Owner's pages",
          "Bug Bakery" in hub_txt and "Bug Garden" in hub_txt, hub_txt[:240].replace("\n", " | "))
    check("(b) overflow 0 at Bug Owner's Hub", overflow(p2) == "1440/1440", overflow(p2))
    p2.goto(BASE + "/identity.html?name=Zara", wait_until="networkidle")
    p2.wait_for_timeout(2500)
    dismiss_veil(p2)
    p2.wait_for_timeout(1500)
    st4 = cert_state(p2)
    check("(b) identity?name=Zara (brand new) stays composing",
          st4["displayName"].strip() == "" and st4["plaqueCertified"] is False
          and st4["aliasFieldWrapper"] == "visible", str(st4))
    check("(b) console errors", len(errs2) == 0, f"{len(errs2)}: {errs2[:3]}")
    check("(b) pageerrors", len(perrs2) == 0, f"{len(perrs2)}: {perrs2[:3]}")
    ctx2.close()
    dump()

    # ================= (c) FRESH BROWSER: whole flow still works =================
    br = pw.firefox.launch()
    ctx3 = br.new_context(viewport={"width": 1440, "height": 900})
    p3 = ctx3.new_page()
    errs3, perrs3 = [], []
    p3.on("console", lambda m: errs3.append(m.text) if m.type == "error" else None)
    p3.on("pageerror", lambda e: perrs3.append(str(e)))
    p3.goto(BASE + "/", wait_until="networkidle")
    p3.wait_for_timeout(1000)
    check("(c) fresh entry dial name-only", p3.locator("input").count() == 1)
    check("(c) fresh entry has NO returning view", p3.locator("#returningView").is_hidden())
    p3.fill("#userName", "Bug Fresh")
    p3.locator("button.enter[type='submit']").click()
    p3.wait_for_url("**/identity.html**", timeout=15000)
    p3.wait_for_timeout(1500)
    dismiss_veil(p3)
    p3.wait_for_timeout(1000)
    check("(c) fresh certificate is composing (no stored profile to restore)",
          cert_state(p3)["plaqueCertified"] is False)
    p3.fill("#aliasInput", "bugfresh2")
    p3.locator("#enterBtn").click()
    p3.wait_for_url("**/welcome**", timeout=25000)
    check("(c) fresh claim lands on the walk", True, p3.url)
    p3.wait_for_timeout(1000)
    p3.click("#skipBtn-1")
    p3.wait_for_selector("#step-2:visible", timeout=9000)
    check("(c) skip Q1 stores nothing",
          p3.evaluate("!('about' in window.__walkState.answers)"))
    for n in range(2, 10):
        p3.fill(f"#answer-{n}", FRESH[n])
        p3.click(f"#enterBtn-{n}")
        nxt = f"#step-{n+1}" if n < 10 else "#step-10"
        p3.wait_for_selector(nxt + ":visible", timeout=9000)
    p3.click("#skipBtn-10")
    p3.wait_for_selector("#step-names:visible", timeout=9000)
    check("(c) skip Q10 stores nothing",
          p3.evaluate("!('space' in window.__walkState.answers)"))
    check("(c) overflow 0 at names", overflow(p3) == "1440/1440", overflow(p3))
    p3.fill("#name-business", "Fresh Mends")
    p3.fill("#name-space", "Mending Circle")
    p3.wait_for_timeout(300)
    p3.click("#enterBtn-11")
    p3.wait_for_selector("text=Done — here are your pages.", timeout=25000)
    check("(c) fresh building reaches done", True)
    check("(c) three building links shown", p3.locator(".p3-build-link").count() == 3)
    p3.click("#buildGo")
    p3.wait_for_selector("#step-end:visible", timeout=9000)
    check("(c) fresh end slide: cards carry typed titles + words",
          "Fresh Mends" in p3.locator("#step-end").inner_text()
          and "I mend clothes and curtains" in p3.locator("#step-end").inner_text())
    check("(c) fresh end slide: agreement board present",
          p3.locator("#dealBoard").count() == 1)
    check("(c) fresh end slide: Smart Link chip",
          p3.locator("#linkFace").inner_text() == "nayanet.app/bugfresh2")
    check("(c) overflow 0 on end slide", overflow(p3) == "1440/1440", overflow(p3))
    p3.screenshot(path=OUT + "bug-verify-fresh-end.png")
    p3.locator('[data-door="Hub"]').click()
    p3.wait_for_timeout(1500)
    check("(c) Hub door lands + lists the fresh pages",
          "/hub?alias=bugfresh2" in p3.url
          and "Fresh Mends" in p3.locator("body").inner_text(), p3.url)
    check("(c) console errors", len(errs3) == 0, f"{len(errs3)}: {errs3[:3]}")
    check("(c) pageerrors", len(perrs3) == 0, f"{len(perrs3)}: {perrs3[:3]}")
    ctx3.close()
    br.close()
    dump()

R["notes"] = [f"pass={len(R['pass'])} fail={len(R['fail'])}"]
json.dump(R, open(OUT + "bug-verify-results.json", "w"), indent=2)
print(f"PASS {len(R['pass'])} / FAIL {len(R['fail'])}")
for f in R["fail"]:
    print("FAIL:", f)
for p_ in R["pass"]:
    print("PASS:", p_)
