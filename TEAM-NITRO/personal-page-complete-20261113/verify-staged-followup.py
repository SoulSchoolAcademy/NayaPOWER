#!/usr/bin/env python3
"""Staged verification of the follow-up build on the proof host.
Fresh cb per width (cb = bab47fb67-w<width>). Re-measures Defect 1 (drawers),
the seven round-1 items, and the Public keyword pull with the REAL fixture
rows read back from the table and injected as stubs (this browser cannot
fetch — the live fetch is the captain's leg). Writes
verify-staged-followup.json + screenshots.
"""
import json, subprocess
from playwright.sync_api import sync_playwright

COMMIT = "bab47fb67"
BASE = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/"
        "personal-page-complete-20261113/personal-complete.html"
        "&ref=personal/personal-page-complete-20261113")
OUT = "/home/hatch/workspace/team-nitro/personal-page-complete-20261113"
LOCAL_SHA = "4872414a1d428a940a4e12ac31c419f999843a2fde072a9ac91d09b42051c666"

def box(page, sel):
    el = page.query_selector(sel)
    if not el: return None
    b = el.bounding_box()
    if not b: return None
    return {"x": round(b["x"], 1), "y": round(b["y"], 1), "w": round(b["width"], 1), "h": round(b["height"], 1)}

def inter(a, b):
    if not a or not b: return False
    return a["x"] < b["x"]+b["w"] and b["x"] < a["x"]+a["w"] and a["y"] < b["y"]+b["h"] and b["y"] < a["y"]+a["h"]

# staged sha read fresh via curl
r = subprocess.run(["curl", "-s", BASE + "&cb=" + COMMIT + "-sha"], capture_output=True)
import hashlib
staged_bytes = r.stdout
res = {"staged_sha": hashlib.sha256(staged_bytes).hexdigest(),
       "staged_bytes": len(staged_bytes),
       "staged_matches_local": hashlib.sha256(staged_bytes).hexdigest() == LOCAL_SHA,
       "widths": {}, "public": {}}

OWNER_STUBS = [
    {"j": {"k": "wall", "a": "Shawn Vibert", "b": "Building the new feed today.", "t": "Building"}, "at": "2026-11-13T10:00:00Z", "id": "stub-1"},
    {"j": {"k": "wall", "a": "Shawn Vibert", "b": "Second post by the owner, about shipping.", "t": "Shipping"}, "at": "2026-11-13T09:00:00Z", "id": "stub-2"},
]
# Real collective rows, read back from the table via service key before this run:
# 3 fixture rows (pcfollowup20261113) + 3 pre-existing renderable other-owner rows.
COLLECTIVE_STUBS = [
    {"j": {"k": "wall", "a": "Follow-Up Tester", "b": "Follow-up keyword test — garden notes: I grow tomatoes and herbs in the garden, and I trade cuttings with neighbours."}, "at": "2026-11-13T15:42:00Z", "id": "41fba108-fac6-4742-9736-e7808abdddb0", "owner": "pcfollowup20261113"},
    {"j": {"k": "wall", "a": "Follow-Up Tester", "b": "Follow-up keyword test — garden tools: my favourite garden tools are the hand fork and the watering can."}, "at": "2026-11-13T15:41:00Z", "id": "3f9bcbda-0387-4e61-9e06-615cf12fb3ae", "owner": "pcfollowup20261113"},
    {"j": {"k": "wall", "a": "Follow-Up Tester", "b": "Follow-up keyword test — harvest morning: we picked the harvest at sunrise and shared the baskets."}, "at": "2026-11-13T15:40:00Z", "id": "25ea46ec-e293-4ef3-b2c6-4da79935c3b6", "owner": "pcfollowup20261113"},
    {"j": {"k": "wall", "a": "Chi DV Spc", "b": "Verification wall post CHI-DV-SPC-WALL-20261022-0010 — newest-first and stamp colours under test."}, "at": "2026-10-22T00:10:00Z", "id": "chi-spc", "owner": "flagship-community"},
    {"j": {"k": "wall", "a": "Chi DV Biz", "b": "Verification wall post CHI-DV-BIZ-WALL-20261022-0010 — newest-first and stamp colours under test."}, "at": "2026-10-22T00:10:00Z", "id": "chi-biz", "owner": "flagship-business"},
    {"j": {"k": "wall", "a": "", "b": "Heartbeat test - NayaPOWER is alive"}, "at": "2026-10-22T00:00:00Z", "id": "heartbeat", "owner": "shawn"},
]

def run():
    with sync_playwright() as p:
        b = p.firefox.launch()
        for w in (390, 1440, 360):
            errs, perrs = [], []
            pg = b.new_page(viewport={"width": w, "height": 844})
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e: perrs.append(str(e)))
            pg.goto(BASE + "&cb=" + COMMIT + "-w" + str(w), wait_until="load", timeout=60000)
            pg.wait_for_timeout(4000)
            d = {"viewport": w, "url": pg.url}
            d["overflowX"] = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            btns = {bid: box(pg, "#" + bid) for bid in ("msgbtn", "aboutbtn", "myworldbtn", "skillsbtn", "connbtn", "growthbtn", "sharebtn", "joinbtn")}
            widths = [v["w"] for v in btns.values() if v]
            d["buttons_equal_2px"] = (max(widths) - min(widths) <= 2) if widths else False
            d["gear_text"] = pg.evaluate("(document.getElementById('settingsbtn')||{}).textContent")
            d["name"] = box(pg, "#pname"); d["pill"] = box(pg, "#pointsdisplay"); d["cvrbtn"] = box(pg, "#cvrbtn")
            d["name_vs_cvrbtn"] = inter(d["name"], d["cvrbtn"]); d["pill_vs_name"] = inter(d["pill"], d["name"])
            d["pill_text"] = pg.evaluate("(document.getElementById('pointscount')||{}).textContent")
            d["notif_segs"] = pg.evaluate("() => Array.from(document.querySelectorAll('.notif-seg')).map(e => e.getAttribute('data-notif'))")
            d["seg_shadow"] = pg.evaluate("() => { const s=document.querySelector('.notif-seg'); return s ? getComputedStyle(s).boxShadow : 'none'; }")
            d["tab_labels"] = pg.evaluate("() => Array.from(document.querySelectorAll('#mwFeedTabs .lens-tab')).map(e => (e.innerText||'').trim())")
            d["feedline"] = pg.evaluate("(() => { const e=document.querySelector('.pc-feedline'); return e ? e.textContent.trim() : null; })()")
            d["rail_cards"] = pg.evaluate("() => document.querySelectorAll('#pcRail .pc-card').length")
            d["rail_imgs"] = pg.evaluate("() => document.querySelectorAll('#pcRail img').length")
            d["wall_cards_staged_live"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .intel-board').length")
            d["wall_placeholder"] = pg.evaluate("(() => { const e=document.querySelector('#os-wall-list .ph-card p'); return e ? e.textContent : null; })()")
            # Defect 1 on staged (the checker's exact failing test)
            url_before = pg.url
            pg.click('.notif-seg[data-notif="spaces"]', timeout=8000); pg.wait_for_timeout(500)
            d["spaces_tap_url_unchanged"] = (pg.url == url_before)
            d["left_drawer_open"] = pg.evaluate("() => document.getElementById('os-drawer').classList.contains('open')")
            d["left_drawer_box"] = box(pg, "#os-drawer")
            pg.mouse.click(pg.evaluate("() => document.getElementById('os-drawer').getBoundingClientRect().right + 20"), 400); pg.wait_for_timeout(400)
            d["left_drawer_closed_on_backdrop_tap"] = pg.evaluate("() => !document.getElementById('os-drawer').classList.contains('open')")
            pg.click('.notif-seg[data-notif="eco"]', timeout=8000); pg.wait_for_timeout(500)
            d["eco_tap_url_unchanged"] = (pg.url == url_before)
            d["right_drawer_open"] = pg.evaluate("() => document.getElementById('os-drawer-right').classList.contains('open')")
            d["right_drawer_box"] = box(pg, "#os-drawer-right")
            pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
            d["right_drawer_closed_on_escape"] = pg.evaluate("() => !document.getElementById('os-drawer-right').classList.contains('open')")
            if w == 1440:
                try:
                    pg.click('.notif-seg[data-notif="spaces"]', timeout=8000); pg.wait_for_timeout(400)
                    d["left_drawer_open_again"] = pg.evaluate("() => document.getElementById('os-drawer').classList.contains('open')")
                    pg.click('.notif-seg[data-notif="spaces"]', timeout=8000); pg.wait_for_timeout(400)
                    d["left_drawer_closed_on_retap_desktop"] = pg.evaluate("() => !document.getElementById('os-drawer').classList.contains('open')")
                except Exception as e:
                    d["retap_error"] = str(e)[:200]
            d["console_errors"] = len(errs); d["pageerrors"] = perrs
            res["widths"][w] = d
            pg.screenshot(path="%s/staged-followup-%d-top.png" % (OUT, w))
            pg.close()
        # staged public keyword pull with the real rows as stubs
        pg = b.new_page(viewport={"width": 1440, "height": 844})
        pg.goto(BASE + "&cb=" + COMMIT + "-public", wait_until="load", timeout=60000); pg.wait_for_timeout(4000)
        pg.evaluate("(posts) => { window.MW_PUBLIC_POSTS = posts; window.MW_PUBLIC_LOADED = true; }", COLLECTIVE_STUBS)
        pg.evaluate("(posts) => { window.MW_WALL_POSTS = posts; window.mwPaintWallPosts(posts); }", OWNER_STUBS)
        pub = {}
        pg.click("#mwTabNaya"); pg.wait_for_timeout(600)
        pub["public_cards"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .intel-board').length")
        pub["public_meta"] = pg.evaluate("(() => { const e=document.getElementById('os-wall-meta'); return e ? e.textContent : null; })()")
        pg.click("#pcSearchBtn"); pg.wait_for_timeout(500)
        pub["popup_open"] = pg.evaluate("() => { const s=document.getElementById('nsbSearchLevel'); return s && s.classList.contains('nsb-modal') && getComputedStyle(s).display!=='none'; }")
        pg.fill('#nsbSearchLevel input[type="search"]', "garden"); pg.wait_for_timeout(600)
        pub["garden_cards"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .intel-board').length")
        pub["garden_meta"] = pg.evaluate("(() => { const e=document.getElementById('os-wall-meta'); return e ? e.textContent : null; })()")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
        pg.click("#pcSearchBtn"); pg.wait_for_timeout(400)
        pg.fill('#nsbSearchLevel input[type="search"]', "harvest"); pg.wait_for_timeout(600)
        pub["harvest_cards"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .intel-board').length")
        pg.fill('#nsbSearchLevel input[type="search"]', ""); pg.wait_for_timeout(600)
        pub["cleared_cards"] = pg.evaluate("() => document.querySelectorAll('#os-wall-list .intel-board').length")
        res["public"] = pub
        pg.close()
        b.close()
    print(json.dumps(res, indent=2)[:6000])
    with open("%s/verify-staged-followup.json" % OUT, "w") as f: json.dump(res, f, indent=2)
    print("wrote verify-staged-followup.json")

run()
