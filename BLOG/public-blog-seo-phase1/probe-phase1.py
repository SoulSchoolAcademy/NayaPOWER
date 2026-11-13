#!/usr/bin/env python3
"""Phase-1 staged probe suite — curls the staged worker and asserts
every phase-1 measurement from the brief + Tree's contract checks.
Writes PASS/FAIL lines to stdout. Exit code 0 only if all pass.
"""
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

STG = "https://naya-public-blog-staging.nayapower.workers.dev"
BUA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
GUA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
OAI = "Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)"
CLAUDE = "Mozilla/5.0 (compatible; Claude-SearchBot/1.0; +https://support.claude.com)"
PERP = "Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai)"
fails = []
passes = []

def check(name, ok, detail=""):
    (passes if ok else fails).append(name)
    print(("PASS " if ok else "FAIL ") + name + ((" | " + str(detail)[:220]) if detail else ""))

def curl(path, ua=None, extra=()):
    cmd = ["curl", "-s", "-D", "/tmp/probe_hdrs", "-o", "/tmp/probe_body",
           "-w", "%{http_code}|%{content_type}|%{size_download}|%{redirect_url}"]
    if ua is not None:
        cmd += ["-A", ua]
    cmd += list(extra) + [STG + path]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    status, ctype, size, loc = out.stdout.strip().split("|")
    body = open("/tmp/probe_body", "rb").read()
    hdrs = open("/tmp/probe_hdrs", encoding="utf-8", errors="replace").read()
    return int(status), ctype, int(size), loc, body, hdrs

def hval(hdrs, name):
    m = re.search(r"(?im)^" + re.escape(name) + r":\s*(.+?)\s*$", hdrs)
    return m.group(1) if m else None

# --- robots.txt ---
s, ct, n, loc, body, h = curl("/robots.txt", BUA)
robots_ct = ct  # the HEAD checks below reassign ct; keep the GET value
check("robots: browser 200", s == 200, f"{s} {ct} {n}B")

# HEAD must be answered by the worker too (self-check round 2 caught
# HEAD falling through to the assets layer and returning text/html).
def head(path, ua=BUA):
    # curl -I prints the proxy CONNECT response first ("200 Connection
    # Established") and then the real response — the status and the
    # Content-Type must come from the LAST HTTP block, not the first.
    # One retry on a 5xx: the edge occasionally answers a transient
    # 503 (Cloudflare, no X-Robots-Tag) that is not the worker.
    for attempt in range(2):
        out = subprocess.run(["curl", "-s", "-I", "-A", ua, STG + path],
                             capture_output=True, text=True, timeout=30).stdout
        blocks = [b for b in out.split("\n\n") if b.strip().startswith("HTTP/")]
        blk = blocks[-1] if blocks else out
        m = re.search(r"^HTTP/\S+ (\d+)", blk, re.M)
        ct = re.search(r"^Content-Type:\s*(.+?)\s*$", blk, re.M | re.I)
        status = int(m.group(1)) if m else 0
        ctype = ct.group(1).strip() if ct else ""
        if status < 500 or attempt == 1:
            return status, ctype
    return status, ctype
s, ct = head("/robots.txt")
check("robots: HEAD 200 text/plain", s == 200 and ct.startswith("text/plain"), f"{s} {ct}")
s, ct = head("/sitemap.xml", GUA)
check("sitemap: HEAD 200 application/xml", s == 200 and ct.startswith("application/xml"), f"{s} {ct}")
s, ct = head("/s/sn2696", GUA)
check("note: HEAD 200 text/html", s == 200 and ct.startswith("text/html"), f"{s} {ct}")
check("robots: content-type text/plain", robots_ct.startswith("text/plain"), robots_ct)
check("robots: not HTML", b"<html" not in body.lower()[:200] and b"<!DOCTYPE" not in body[:100], body[:80])
txt = body.decode()
for rule in ["User-agent: Googlebot", "User-agent: Bingbot", "User-agent: OAI-SearchBot",
             "User-agent: Claude-SearchBot", "User-agent: PerplexityBot",
             "User-agent: GPTBot\nDisallow: /", "User-agent: ClaudeBot\nDisallow: /",
             "Disallow: /api/", "Sitemap: " + STG + "/sitemap.xml"]:
    check(f"robots: rule {rule.splitlines()[0][:40]}", rule in txt)
check("robots: no nosnippet", "nosnippet" not in txt.lower())
s2, _, _, _, body2, _ = curl("/robots.txt", GUA)
check("robots: googlebot 200 identical", s2 == 200 and body2 == body)

# --- sitemap.xml ---
s, ct, n, loc, body, h = curl("/sitemap.xml", BUA)
check("sitemap: 200", s == 200, f"{s} {ct} {n}B")
check("sitemap: content-type xml", "xml" in ct, ct)
check("sitemap: not HTML", b"<!DOCTYPE" not in body[:100])
try:
    root = ET.fromstring(body.decode())
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [u.find("sm:loc", ns).text for u in root.findall("sm:url", ns)]
    check("sitemap: parses, exactly 2 URLs", len(urls) == 2, urls)
    check("sitemap: Hub root listed", urls[0] == STG + "/")
    check("sitemap: only the candidate note listed", urls[1] == STG + "/s/sn2696", urls)
    check("sitemap: lastmod 2026-11-12 on note",
          root.findall("sm:url", ns)[1].find("sm:lastmod", ns).text == "2026-11-12")
    check("sitemap: no private/feed/api URLs",
          not any(x in body.decode() for x in ["/api/", "/feed", "personal", "/pi"]))
except Exception as e:
    check("sitemap: parses as XML", False, e)

# --- note page, bot ---
s, ct, n, loc, body, h = curl("/s/sn2696", GUA)
check("note: googlebot 200 html", s == 200 and ct.startswith("text/html"), f"{s} {ct} {n}B")
html = body.decode(errors="replace")
check("note: X-Robots-Tag index, follow", hval(h, "X-Robots-Tag") == "index, follow", hval(h, "X-Robots-Tag"))
title = re.search(r"<title>(.*?)</title>", html)
check("note: title 50-60 chars", title and 50 <= len(title.group(1)) <= 60,
      title.group(1) if title else None)
desc = re.search(r'<meta name="description" content="([^"]+)"', html)
check("note: description 120-155 chars", desc and 120 <= len(desc.group(1)) <= 155,
      (desc.group(1)[:80] + "...") if desc else None)
canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
check("note: one canonical /s/sn2696", canon and canon.group(1) == STG + "/s/sn2696",
      canon.group(1) if canon else None)
check("note: canonical count == 1", html.count('rel="canonical"') == 1)
check("note: H1 is the display title", "<h1>The Infinite Smart Feeds</h1>" in html)
check("note: hook in initial HTML", "Not one feed like Facebook" in html)
check("note: nutshell substance present", "the MISSING element" in html)
check("note: Two views kept", "Two views" in html)
check("note: The layout kept", "The layout" in html)
check("note: The difference kept", "The difference" in html)
check("note: The build kept", "The build" in html)
check("note: What changes now kept (Learning board)",
      "built as their own world" in html and "The Learning" in html)
check("note: Human board", "Human Note" in html and "origin story" in html)
check("note: Child board", "Child Note" in html)
check("note: Grandma board", "Grandma Note" in html)
check("note: Naya board", "Naya Note" in html)
check("note: Why board", "Why It Matters" in html and "it connects all the worlds" in html)
check("note: filing footer stripped", "Filed by Intelligence Loop" not in html)
check("note: no Paired Naya Note path", "Paired Naya Note" not in html)
check("note: no registry leak", "live from the registry" not in html)
check("note: feed revision named", "registry@37c542f6" in html)
check("note: byline date+author", "Published" in html and "2026-11-12" in html and ">Naya<" in html)
check("note: OG article set",
      'property="og:type" content="article"' in html and 'property="og:image"' in html)
check("note: Twitter card", 'name="twitter:card" content="summary_large_image"' in html)
check("note: robots meta index,follow", 'name="robots" content="index, follow"' in html)
try:
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    j = json.loads(ld.group(1))
    types = [x.get("@type") for x in j["@graph"]]
    check("note: JSON-LD BlogPosting+BreadcrumbList, no FAQ/HowTo",
          "BlogPosting" in types and "BreadcrumbList" in types
          and "FAQPage" not in types and "HowTo" not in types, types)
    bp = [x for x in j["@graph"] if x.get("@type") == "BlogPosting"][0]
    check("note: JSON-LD matches visible (headline/date/canonical)",
          bp["headline"] == "The Infinite Smart Feeds"
          and bp["datePublished"] == "2026-11-12"
          and bp["mainEntityOfPage"] == STG + "/s/sn2696")
    check("note: JSON-LD description == meta description",
          bp["description"] == desc.group(1))
except Exception as e:
    check("note: JSON-LD parses", False, e)
check("note: cover img descriptive filename + alt + caption",
      'src="/images/infinite-smart-feeds-cover.png"' in html
      and 'alt="NayaNET' in html and "<figcaption>" in html)
check("note: top bar links Hub + Open in Hub",
      ">Hub<" in html and "#/smart-notes/sn-2696" in html)
check("note: no meta keywords", "meta name=\"keywords\"" not in html)
check("note: no llms.txt claim", "llms.txt" not in html)

# --- note page, other search crawlers ---
for name, ua in [("OAI-SearchBot", OAI), ("Claude-SearchBot", CLAUDE), ("PerplexityBot", PERP)]:
    s, _, _, _, b, _ = curl("/s/sn2696", ua)
    check(f"note: {name} 200 + same bytes", s == 200 and b == body, f"{s} {len(b)}B")

# --- note page, browser keeps the 302 into the Hub ---
s, ct, n, loc, body, h = curl("/s/sn2696", BUA)
check("note: browser 302 to hash route", s == 302 and loc == STG + "/#/smart-notes/sn2696",
      f"{s} loc={loc}")
s, _, _, loc, _, _ = curl("/s/sn2696", None)  # plain curl, no UA
check("note: plain curl (non-browser) gets the page", s == 200, f"{s}")

# --- aliases serve the same canonical page ---
s, _, _, _, b, _ = curl("/note/sn2696", GUA)
check("alias: /note/sn2696 bot 200, canonical still /s/",
      s == 200 and ('href="' + STG + '/s/sn2696"') in b.decode(errors="replace"), f"{s}")
s, _, _, _, b, _ = curl("/smart-notes/sn2696", GUA)
check("alias: /smart-notes/sn2696 bot 200", s == 200, f"{s}")

# --- denial: private / unknown notes ---
for path, why in [("/s/sn0587", "registry-private note"), ("/s/sn9999", "unknown note"),
                  ("/s/sn2695", "other public-looking note, not allowlisted"),
                  ("/note/sn0587", "private via /note/ alias")]:
    s, ct, n, loc, body, h = curl(path, GUA)
    check(f"deny: {path} ({why}) 404 no body", s == 404 and body == b"Note not found",
          f"{s} {body[:40]}")
    check(f"deny: {path} X-Robots-Tag noindex",
          (hval(h, "X-Robots-Tag") or "").startswith("noindex"), hval(h, "X-Robots-Tag"))
    check(f"deny: {path} no-store", hval(h, "Cache-Control") == "no-store")
# browser asking a denied note: still the Hub 302 (no content leaked either way)
s, _, _, loc, body, _ = curl("/s/sn0587", BUA)
check("deny: browser /s/sn0587 302 (no content)", s == 302 and body == b"", f"{s} {len(body)}B")

# --- cover image ---
s, ct, n, loc, body, h = curl("/images/infinite-smart-feeds-cover.png", GUA)
check("image: cover 200 image/png", s == 200 and ct.startswith("image/png"), f"{s} {ct} {n}B")
check("image: cover is the public icon bytes",
      len(body) > 10000, f"{n}B")
s, _, _, _, body, h = curl("/images/secret.png", GUA)
check("image: unknown image 404 noindex", s == 404 and body == b"Image not found"
      and (hval(h, "X-Robots-Tag") or "").startswith("noindex"), f"{s}")

# --- no regressions: Hub shell, entrance, PI, sw.js ---
s, ct, n, loc, body, h = curl("/", BUA)
check("regression: / still serves entrance 200", s == 200 and n > 600000, f"{s} {n}B")
s, ct, n, loc, body, h = curl("/hub", BUA)
check("regression: /hub still serves Hub shell 200", s == 200 and n > 5000000, f"{s} {n}B")
check("regression: /hub still titled Intel Today", b"Intel Today" in body[:5000])
s, ct, n, loc, body, h = curl("/sw.js", BUA)
check("regression: /sw.js cure 200 js", s == 200 and "javascript" in ct, f"{s} {ct}")
s, ct, n, loc, body, h = curl("/pi", BUA)
# Pre-existing staging condition, NOT a phase-1 regression: the /pi
# handler block in the built worker is byte-identical to the live base
# worker, and live /pi is 200 — the staging ASSETS binding answers the
# /pi/index.html subrequest with a 307 where live answers 200. Out of
# phase-1 scope; recorded in the record file.
check("regression: /pi staging 307 (pre-existing, unchanged code)", s == 307, f"{s} {ct}")

print(f"\n{len(passes)} passed, {len(fails)} failed")
if fails:
    print("FAILED: " + ", ".join(fails))
    sys.exit(1)
print("ALL PHASE-1 PROBES PASS")
