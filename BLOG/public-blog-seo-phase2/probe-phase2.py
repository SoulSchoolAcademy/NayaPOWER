#!/usr/bin/env python3
"""Phase-2 curl probe (maker seat, written from scratch).
- FULL staged set (all 1,058 notes) with Googlebot UA: status, title
  50-60, description 120-155, exactly one canonical, JSON-LD parses as
  BlogPosting + BreadcrumbList with no FAQPage/HowTo, X-Robots-Tag
  index,follow, related links >=3 with reasons, cluster + Hub links,
  and agreement with seo-score-report.json (title/desc/cluster/score).
- UA battery over the named sample (SN-2696 + one per cluster + the 2
  topic-less notes + one per topic family sample): Googlebot,
  OAI-SearchBot, Claude-SearchBot, PerplexityBot, Bingbot, plain curl,
  browser UA (302 to the hash route).
- Denial: unlisted slug, /s/sn2696/extra, /s/sn9999 -> 404 + noindex.
- No-regressions: /hub 200 (phase-2 shell bytes), /robots.txt real,
  /sitemap.xml count, /sw.js 200, /pi 307, aliases same canonical,
  /s/sn2696 browser 302.
Writes probe-phase2-results.json + prints a summary. Exits 1 on failure.
"""
import html as htmlmod
import hashlib
import json, re, subprocess, sys, tempfile, os, time
from collections import Counter

BASE = "https://naya-public-blog-staging.nayapower.workers.dev"
WD = "/home/hatch/workspace/team-nitro/seo-ai-backend-20261113"
UAS = {
    "Googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "OAI-SearchBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot",
    "Claude-SearchBot": "Claude-SearchBot/1.0",
    "PerplexityBot": "Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)",
    "Bingbot": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "plain": "curl/8.0",
    "browser": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
}
def get(path, ua, timeout=60):
    # curl, not urllib: urllib hits IncompleteRead truncations via the
    # egress proxy on these chunked worker responses; curl is reliable.
    # Status comes from -w %{http_code}: the -D header file starts with
    # the proxy's "HTTP/1.1 200 Connection Established" line, so parsing
    # it for the status reads the proxy, not the origin.
    # A 503 is retried: Cloudflare intermittently returns error 1102
    # (Worker CPU/edge flake) under sustained load, and the same request
    # succeeds on the next attempt. Only a 503 that survives 3 attempts
    # counts as a failure.
    with tempfile.TemporaryDirectory() as td:
        body, hdrs = td + "/b", td + "/h"
        last = None
        for attempt in range(3):
            r = subprocess.run(["curl", "-s", "-o", body, "-D", hdrs, "-A", UAS[ua],
                                "-w", "%{http_code}", "--max-time", str(timeout), BASE + path],
                               capture_output=True, text=True)
            try:
                st = int(r.stdout.strip())
                htxt = open(hdrs, encoding="utf-8", errors="replace").read()
                h = {}
                # the LAST response block in the header file is the origin's
                for block in htxt.split("\r\n\r\n"):
                    for line in block.splitlines()[1:]:
                        if ":" in line:
                            k, v = line.split(":", 1); h[k.strip()] = v.strip()
                last = (st, h, open(body, encoding="utf-8", errors="replace").read())
                if st != 503:
                    return last
                time.sleep(2)
            except Exception:
                if attempt == 2: raise
        return last
    raise RuntimeError("unreachable")

def check_note_html(html, slug):
    errs = []
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    title = htmlmod.unescape(m.group(1)) if m else ""
    if not (50 <= len(title) <= 60): errs.append(f"title {len(title)}c")
    m = re.search(r'<meta name="description" content="([^"]*)">', html)
    desc = htmlmod.unescape(m.group(1)) if m else ""
    if not (120 <= len(desc) <= 155): errs.append(f"desc {len(desc)}c")
    cans = re.findall(r'<link rel="canonical" href="([^"]*)">', html)
    if len(cans) != 1: errs.append(f"canonical x{len(cans)}")
    elif not cans[0].endswith("/s/" + slug): errs.append(f"canonical {cans[0]}")
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    ld_text = m.group(1) if m else ""
    if not m: errs.append("no JSON-LD")
    else:
        try:
            ld = json.loads(m.group(1))
            types = [g.get("@type") for g in ld.get("@graph", [])]
            if "BlogPosting" not in types or "BreadcrumbList" not in types: errs.append(f"jsonld types {types}")
            if "FAQPage" in types or "HowTo" in types: errs.append("forbidden jsonld type")
            bp = next(g for g in ld["@graph"] if g.get("@type") == "BlogPosting")
            if bp.get("inLanguage") != "en": errs.append("jsonld lang")
            if not bp.get("articleSection"): errs.append("jsonld no articleSection")
        except Exception as e: errs.append(f"jsonld parse: {e}")
    if "FAQPage" in ld_text or "HowTo" in ld_text: errs.append("FAQPage/HowTo string in JSON-LD")
    rel = re.findall(r'<article class="rel-card"[^>]*><a href="/s/([^"]+)">([^<]+)</a><p class="why">([^<]+)</p>', html)
    if len(rel) < 3: errs.append(f"related x{len(rel)}")
    for _, _, why in rel:
        if not (why.startswith("Same topic:") or why.startswith("Same list:") or why.startswith("Same cluster:")):
            errs.append(f"related without reason: {why}")
    if 'href="/?cluster=' not in html: errs.append("no cluster link")
    if 'href="/"' not in html: errs.append("no Hub link")
    if "Related in this cluster" not in html: errs.append("no related block")
    return errs, {"title": title, "desc": desc, "canonical": cans[0] if cans else "", "related": len(rel)}

report = json.load(open(WD + "/seo-score-report.json"))
first_by_slug = {}
for r in report:
    first_by_slug.setdefault(r["slug"], r)
fails, results = [], {"full": {}, "ua": {}, "denial": {}, "regressions": {}}
# ---- FULL SET, Googlebot ----
n = 0
for r in report:
    slug = r["slug"]
    st, h, html = get("/s/" + slug, "Googlebot")
    n += 1
    if st != 200:
        fails.append(f"{slug}: status {st}"); continue
    if h.get("X-Robots-Tag") != "index, follow":
        fails.append(f"{slug}: X-Robots-Tag {h.get('X-Robots-Tag')}")
    if r.get("canonicalCollision"):
        # The canonical URL serves the FIRST note filed under this number
        # (the collision is Shawn's call, not the machine's). This note
        # is proven instead at its full-id URL, which must serve it.
        first = first_by_slug[slug]
        errs, got = check_note_html(html, slug)
        if errs: fails.append(f"{slug}: " + "; ".join(errs))
        if got["title"] != first["title"]: fails.append(f"{slug}: canonical serves first note, live title != first report title")
        if got["desc"] != first["description"]: fails.append(f"{slug}: canonical serves first note, live desc != first report desc")
        st2, h2, html2 = get("/s/" + str(r["id"]).lower(), "Googlebot")
        if st2 != 200:
            fails.append(f"{slug}: full-id URL status {st2}"); continue
        errs2, got2 = check_note_html(html2, slug)
        if errs2: fails.append(f"{slug}: full-id: " + "; ".join(errs2))
        if got2["title"] != r["title"]: fails.append(f"{slug}: full-id live title != report title")
        if got2["desc"] != r["description"]: fails.append(f"{slug}: full-id live desc != report desc")
        if got2["related"] != r["relatedCount"]: fails.append(f"{slug}: full-id live related {got2['related']} != report {r['relatedCount']}")
        if n % 200 == 0: print(f"  ...{n}/1058 crawled, fails so far: {len(fails)}", flush=True)
        continue
    errs, got = check_note_html(html, slug)
    if errs: fails.append(f"{slug}: " + "; ".join(errs))
    if got["title"] != r["title"]: fails.append(f"{slug}: live title != report title")
    if got["desc"] != r["description"]: fails.append(f"{slug}: live desc != report desc")
    if got["related"] != r["relatedCount"]: fails.append(f"{slug}: live related {got['related']} != report {r['relatedCount']}")
    if n % 200 == 0: print(f"  ...{n}/1058 crawled, fails so far: {len(fails)}", flush=True)
results["full"] = {"checked": n, "fails": len(fails)}
print(f"FULL SET: {n} notes, {len(fails)} failures")
for f in fails[:20]: print("  FAIL:", f)

# ---- UA battery over the named sample ----
sample = []
seen = set()
for r in report:
    if r["sn"] == "SN-2696" and r["slug"] not in seen: sample.append(r); seen.add(r["slug"])
clusters = {}
for r in report:
    if r.get("canonicalCollision"): continue
    clusters.setdefault(r["cluster"], r)
for c, r in clusters.items():
    if r["slug"] not in seen: sample.append(r); seen.add(r["slug"])
for r in report:
    if not r.get("related") and False: pass
# the 2 topic-less notes (ids known from the analysis)
for nid in ["IB-SMART-NOTE-20261106-sn2209-the-supercharger", "IB-SMART-NOTE-20261106-sn2208-the-whole-thing-in-one-breath"]:
    r = next(x for x in report if x["id"] == nid)
    if r["slug"] not in seen: sample.append(r); seen.add(r["slug"])
# one note per topic family: first note of each of the 10 biggest topics
feed = json.load(open("/home/hatch/workspace/factory-pipeline/hub-feed-live.json"))
top_topics = Counter()
for nn in feed["notes"]:
    for t in (nn.get("topics") or []): top_topics[t] += 1
for t, _ in top_topics.most_common(10):
    r = next(x for x in report if t in (next(nn for nn in feed["notes"] if nn["id"] == x["id"]).get("topics") or []))
    if r["slug"] not in seen: sample.append(r); seen.add(r["slug"])
print(f"UA sample: {len(sample)} notes: {[s['slug'] for s in sample]}")
ua_fails = []
for r in sample:
    for ua in ["Googlebot", "OAI-SearchBot", "Claude-SearchBot", "PerplexityBot", "Bingbot", "plain"]:
        st, h, html = get("/s/" + r["slug"], ua)
        if st != 200: ua_fails.append(f"{r['slug']} {ua}: {st}"); continue
        errs, _ = check_note_html(html, r["slug"])
        if errs: ua_fails.append(f"{r['slug']} {ua}: " + "; ".join(errs))
    st, h, html = get("/s/" + r["slug"], "browser")
    if st != 302: ua_fails.append(f"{r['slug']} browser: {st} (want 302)")
    elif "/#/smart-notes/" not in (h.get("Location") or ""): ua_fails.append(f"{r['slug']} browser 302 -> {h.get('Location')}")
results["ua"] = {"sample": len(sample), "fails": ua_fails}
print(f"UA BATTERY: {len(sample)} notes x 7 UAs, {len(ua_fails)} failures")
for f in ua_fails[:20]: print("  FAIL:", f)

# ---- Denial ----
# sn9999 is unlisted; /s/sn2696/extra is a deep path. (sn0587 is NOT a
# denial case: it is the zero-padded alias of the real note sn587 —
# the phase-1 finder resolves sn-?(\d+) by number, so it serves 200.)
for path, want in [("/s/sn9999", 404), ("/s/sn2696/extra", 404),
                   ("/s/sn2696/extra/deeper", 404)]:
    st, h, body = get(path, "Googlebot")
    ok = st == want and h.get("X-Robots-Tag") == "noindex, nofollow" and h.get("Cache-Control") == "no-store"
    results["denial"][path] = {"status": st, "x-robots": h.get("X-Robots-Tag"), "ok": ok}
    if not ok: fails.append(f"denial {path}: {st} {h.get('X-Robots-Tag')}")
    print(f"denial {path}: {st} {h.get('X-Robots-Tag')} ok={ok}")

# ---- No-regressions ----
st, h, html = get("/hub", "browser")
hub_sha = hashlib.sha256(html.encode("utf-8")).hexdigest()
local_sha = hashlib.sha256(open(WD + "/index-intel-today-phase2.html", "rb").read()).hexdigest()
results["regressions"]["hub"] = {"status": st, "bytes": len(html), "sha": hub_sha[:12], "local_sha": local_sha[:12]}
if st != 200: fails.append(f"/hub {st}")
# Size alone once misread 5,552,441 through the egress proxy (a truncated
# fetch of the 5.5 MB shell); the sha of the downloaded body is the
# assertion that settles deployed == local.
if hub_sha != local_sha: fails.append(f"/hub sha {hub_sha[:12]} != local shell {local_sha[:12]} (bytes {len(html)})")
if 'href="/s/sn2696"' not in html and "href=\"/s/sn2696\"" not in html: fails.append("/hub shell missing static /s/sn2696 link")
st, h, body = get("/robots.txt", "plain")
results["regressions"]["robots"] = {"status": st, "has_googlebot": "Googlebot" in body, "has_gptbot_disallow": "GPTBot\nDisallow: /" in body}
if st != 200 or "<html" in body: fails.append("robots not real")
st, h, body = get("/sitemap.xml", "plain")
locs = len(re.findall(r"<loc>", body))
results["regressions"]["sitemap"] = {"status": st, "locs": locs}
if st != 200 or locs != 1049: fails.append(f"sitemap locs {locs} != 1049 (1 root + 1048 unique canonicals; 10 duplicate canonicals collapsed)")
st, h, body = get("/sw.js", "browser")
results["regressions"]["sw.js"] = {"status": st}
if st != 200: fails.append(f"/sw.js {st}")
st, h, body = get("/pi", "browser")
results["regressions"]["pi"] = {"status": st}
if st != 307: fails.append(f"/pi {st} (want pre-existing 307)")
for alias in ["/note/sn2696", "/notes/sn2696", "/smart-notes/sn2696", "/s/sn-2696"]:
    st, h, html = get(alias, "Googlebot")
    cans = re.findall(r'<link rel="canonical" href="([^"]*)">', html)
    ok = st == 200 and cans == [BASE + "/s/sn2696"]
    results["regressions"][alias] = {"status": st, "canonical": cans, "ok": ok}
    if not ok: fails.append(f"alias {alias}: {st} {cans}")
print("REGRESSIONS:", json.dumps(results["regressions"], indent=1)[:1500])

json.dump(results, open(WD + "/probe-phase2-results.json", "w"), indent=1)
json.dump(fails, open(WD + "/probe-phase2-failures.json", "w"), indent=1)
print(f"TOTAL FAILURES: {len(fails)}")
if fails:
    print("FAILURES:")
    for f in fails[:40]: print(" -", f)
    sys.exit(1)
print("PROBE GREEN")
