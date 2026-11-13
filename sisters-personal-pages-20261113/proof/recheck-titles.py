#!/usr/bin/env python3
"""Re-check the 6 Business/Space story titles with the CORRECT element.
The probe measured `.ib-layer-head b` ("My story" — the About view's static
section heading, lowercase, never relabeled by design). The relabel target
is `#os-story-title`, set by applyStoryLabels() from window.MSHIP_PAGE_KIND
on DOMContentLoaded. Corrects the 6 wrong-element fails in spp-results.json.
"""
import json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8901"
WORK = "/home/hatch/workspace/team-nitro/sisters-personal-pages-20261113/"
R = json.load(open(WORK + "spp-results.json"))
before_fail = len(R["fail"])
# remove the 6 wrong-element fails (audit-noted, not hidden — see record Addendum C)
R["fail"] = [f for f in R["fail"] if "story title is Our Story" not in f]
print(f"removed {before_fail - len(R['fail'])} wrong-element fails")

def check(name, ok, detail=""):
    (R["pass"] if ok else R["fail"]).append(name + (" :: " + str(detail) if detail else ""))
    json.dump(R, open(WORK + "spp-results.json", "w"), indent=2)

ABOUT_JS = """() => {
  const q = s => document.querySelector(s);
  const sec = id => { const el=q('#'+id); return el ? el.textContent.trim() : 'MISSING'; };
  return {
    storyTitle: q('#os-story-title') ? q('#os-story-title').textContent.trim() : 'MISSING',
    layerHead: [...document.querySelectorAll('.ib-layer-head b')].map(b => b.textContent.trim()).find(h => /my story|our story/i.test(h)) || 'NONE',
    story: sec('abouttext'),
    motto: sec('os-sec-motto-text'),
  };
}"""

CASES = [
    ("sophia", "business", "sophias-lessons"),
    ("sophia", "space", "the-learning-circle"),
    ("thea", "business", "theas-record"),
    ("thea", "space", "the-knowing-room"),
    ("astraea", "business", "astraeas-gates"),
    ("astraea", "space", "the-scales-room"),
]
with sync_playwright() as pw:
    br = pw.firefox.launch()
    for alias, kind, slug in CASES:
        ctx = br.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        pg.goto(f"{BASE}/pages/{alias}/{slug}", wait_until="domcontentloaded")
        pg.wait_for_selector("#pname", timeout=20000)
        pg.wait_for_timeout(6000)
        check(f"{alias} {kind} 1440 story title element is #os-story-title (relabel target)",
              pg.locator("#os-story-title").count() == 1, "")
        pg.locator(".up-act", has_text="About").first.click()
        pg.wait_for_timeout(1200)
        a = pg.evaluate(ABOUT_JS)
        check(f"{alias} {kind} 1440 story title is Our Story (corrected element: #os-story-title)",
              a["storyTitle"] == "Our Story", f"title={a['storyTitle']!r} layerHead={a['layerHead']!r} (static, never relabeled)")
        check(f"{alias} {kind} 1440 About story+motto still the citizen's words after re-check",
              len(a["story"]) > 20 and len(a["motto"]) > 0, f"story={a['story'][:50]!r} motto={a['motto'][:50]!r}")
        ctx.close()
    br.close()

R["notes"] = [f"pass={len(R['pass'])} fail={len(R['fail'])}",
              "2026-11-13 ~05:20Z: 6 story-title fails superseded — probe measured .ib-layer-head b (static 'My story'); correct element is #os-story-title, relabeled by applyStoryLabels() from MSHIP_PAGE_KIND. See record Addendum C."]
json.dump(R, open(WORK + "spp-results.json", "w"), indent=2)
print(f"RE-CHECK DONE: pass={len(R['pass'])} fail={len(R['fail'])}")
for f in R["fail"]:
    print("FAIL:", f)
