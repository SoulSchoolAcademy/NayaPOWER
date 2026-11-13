#!/usr/bin/env python3
"""Dedupe re-probe (fix round, F3): full staged set, Googlebot UA.
For every note in seo-score-report.json (1,058), fetch its SERVING URL
(canonical /s/<slug>; full-id /s/<id> for the 10 canonical-collision
second notes) and extract the related-card hrefs. Report:
  - notes whose related list contains a duplicated href (before: 147, all /s/sn2650)
  - notes with <3 DISTINCT related destinations (floor, must be 0)
  - the sn2650 pair detail: /s/sn2696's list, and the Manual's full-id page
Writes probe-dedupe-results.json. Exits 1 if any dup or any floor breach.
Method harvested from probe-phase2.py (same curl get() with 503 retries,
same rel-card regex) — one probe method, before and after.
"""
import html as htmlmod
import json, re, subprocess, sys, tempfile, time

BASE = "https://naya-public-blog-staging.nayapower.workers.dev"
WD = "/home/hatch/workspace/team-nitro/seo-ai-backend-20261113"
UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

def get(path, timeout=60):
    with tempfile.TemporaryDirectory() as td:
        body, hdrs = td + "/b", td + "/h"
        last = None
        for attempt in range(3):
            r = subprocess.run(["curl", "-s", "-o", body, "-D", hdrs, "-A", UA,
                                "-w", "%{http_code}", "--max-time", str(timeout), BASE + path],
                               capture_output=True, text=True)
            try:
                st = int(r.stdout.strip())
                last = (st, open(body, encoding="utf-8", errors="replace").read())
                if st != 503:
                    return last
                time.sleep(2)
            except Exception:
                if attempt == 2: raise
        return last
    raise RuntimeError("unreachable")

REL_RE = re.compile(r'<article class="rel-card"[^>]*><a href="/s/([^"]+)">([^<]+)</a><p class="why">([^<]+)</p>')

report = json.load(open(WD + "/seo-score-report.json"))
dup_notes, floor_notes, details = [], [], {}
n = 0
for r in report:
    slug = r["slug"]
    url = "/s/" + str(r["id"]).lower() if r.get("canonicalCollision") else "/s/" + slug
    st, html = get(url)
    n += 1
    if st != 200:
        dup_notes.append({"slug": slug, "url": url, "error": f"status {st}"})
        continue
    rel = REL_RE.findall(html)
    hrefs = ["/s/" + h for h, _, _ in rel]
    distinct = set(hrefs)
    if len(hrefs) != len(distinct):
        from collections import Counter
        dups = sorted({h for h, c in Counter(hrefs).items() if c > 1})
        dup_notes.append({"slug": slug, "url": url, "hrefs": hrefs, "duplicated": dups})
    if len(distinct) < 3:
        floor_notes.append({"slug": slug, "url": url, "distinct": len(distinct), "hrefs": hrefs})
    if slug in ("sn2696", "sn2650"):
        details[slug] = {"url": url, "hrefs": hrefs,
                         "titles": [t for _, t, _ in rel],
                         "reasons": [w for _, _, w in rel]}
    if n % 200 == 0:
        print(f"  ...{n}/{len(report)} crawled, dup notes so far: {len(dup_notes)}, floor breaches: {len(floor_notes)}", flush=True)

out = {"checked": n, "dup_notes": len(dup_notes), "floor_breaches": len(floor_notes),
       "dup_detail": dup_notes[:20], "floor_detail": floor_notes[:20], "pair_detail": details}
json.dump(out, open(WD + "/probe-dedupe-results.json", "w"), indent=1)
print(f"DEDUPE PROBE: {n} notes checked, {len(dup_notes)} with a duplicated related href, "
      f"{len(floor_notes)} below the 3-distinct floor")
for d in dup_notes[:10]:
    print("  DUP:", d.get("slug"), d.get("duplicated") or d.get("error"))
for f in floor_notes[:10]:
    print("  FLOOR:", f)
print("PAIR DETAIL:", json.dumps(details, indent=1))
if dup_notes or floor_notes:
    sys.exit(1)
print("DEDUPE PROBE GREEN")
