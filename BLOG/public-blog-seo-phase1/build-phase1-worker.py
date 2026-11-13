#!/usr/bin/env python3
"""Build the PHASE-1 Hub worker from the canonical live worker.
Base: hub-worker-harvested-main.js — byte-identical to GitHub main
  HUB/hub-worker.js AND to the live "hub" worker script
  (sha256 701c2bb85a1931e288a3ceb0eb7243ac1238e3cc7359bbec73a9d6d0c9ecd24c,
  verified 2026-11-12 by cf-worker.py get-script + raw fetch).
Additions: phase1-additions.js (this round's seam only: robots.txt,
  sitemap.xml, the bot note page for ONE proposed candidate, the cover
  image). No phase-2 machinery: no /feed, no /cluster, no /api/seo, no
  scorer, no Hub shell change.
Output: hub-worker-phase1.js

The title + description are DERIVED from the live feed entry for
SN-2696 (~/workspace/factory-pipeline/hub-feed-live.json) and asserted
here (title 50-60 chars, description 120-155 chars, description a
verbatim substring of the note's own hook/nutshell). The section
parser is mirrored in Python over the real subtitle and asserted here
(all seven public sections present) — the staged curl probe is the
second proof that the JS parser renders them.
Every splice is byte-exact and asserted. The base is kept verbatim:
the built file must start with the base bytes up to the splice point.
"""
import hashlib
import json
import re
import sys

WD = "/home/hatch/workspace/team-nitro/public-blog-seo-20261112"
BASE = WD + "/hub-worker-harvested-main.js"
ADD = WD + "/phase1-additions.js"
OUT = WD + "/hub-worker-phase1.js"
FEED = "/home/hatch/workspace/factory-pipeline/hub-feed-live.json"
LIVE_SHA = "701c2bb85a1931e288a3ceb0eb7243ac1238e3cc7359bbec73a9d6d0c9ecd24c"

base = open(BASE, encoding="utf-8").read()
add = open(ADD, encoding="utf-8").read()
feed = json.load(open(FEED, encoding="utf-8"))

# 0 — the base is the canonical live worker, byte for byte.
sha = hashlib.sha256(open(BASE, "rb").read()).hexdigest()
assert sha == LIVE_SHA, f"base sha {sha} != live {LIVE_SHA}"
print(f"OK base == live hub worker ({len(base)} bytes, sha {sha[:12]})")

# 1 — find the candidate note in the live feed.
note = None
for n in feed["notes"]:
    if re.search(r"SN-2696\b", str(n.get("title", ""))):
        note = n
        break
assert note is not None, "SN-2696 not in live feed"
assert not note.get("personal"), "candidate is personal — STOP"
print(f"OK candidate in feed: {note['id']} | personal={note.get('personal')} "
      f"| kind={note.get('kind')} | created={note.get('created')}")
print(f"   feed revision: {feed.get('generated_from')} | notes: {feed.get('count')}")

sub = note["subtitle"]

def strip_md(t):
    return re.sub(r"\s+", " ", re.sub(r"[*_`#>\[\]()!]", " ", t or "")).strip()

def first_sentence(s):
    s = re.sub(r"\s+", " ", s or "").strip()
    m = re.match(r"^.*?[.!?](?=\s|$)", s)
    return m.group(0) if m else s

# 2 — derive the display title from the note's own id slug.
slug = re.match(r"^(?:IB-SMART-NOTE|NN)-\d{8}-(.+)$", note["id"]).group(1)
display = slug.replace("-", " ").title()
assert display == "The Infinite Smart Feeds", f"display title: {display}"
# 3 — derive the <title> (50-60 chars, topic first, brand last).
for title in [
    display + " \u2014 one feed per topic \u00b7 NayaNET",
    display + " \u2014 one feed for every topic \u00b7 NayaNET",
    "Infinite Smart Feeds \u2014 one feed for every topic \u00b7 NayaNET",
]:
    if 50 <= len(title) <= 60:
        break
assert 50 <= len(title) <= 60, f"title {len(title)} chars: {title}"
assert title.startswith(display), "title must agree with the H1"
print(f"OK title ({len(title)} chars): {title}")

# 4 — derive the meta description (120-155 chars, verbatim from the
# note's own hook / nutshell — never composed text).
hook_m = re.search(r"\*\*Hook:\*\*\s*(.*?)(?:\n\s*\n|\*\*Nutshell:\*\*|$)",
                   sub, re.S)
assert hook_m, "no **Hook:** in subtitle"
hook = strip_md(hook_m.group(1))
nut_m = re.search(r"\*\*Nutshell:\*\*\s*(.*?)(?:\n\s*\n\*\*|\Z)", sub, re.S)
nut_first = first_sentence(strip_md(nut_m.group(1))) if nut_m else ""
cands = [first_sentence(hook), first_sentence(hook) + " " + nut_first, hook]
desc = None
for c in cands:
    if 120 <= len(c) <= 155:
        desc = c
        break
if desc is None:
    cut = hook[:154]
    sp = cut.rfind(" ")
    desc = (cut[:sp] if sp > 100 else cut).strip() + "\u2026"
assert 120 <= len(desc) <= 155, f"description {len(desc)} chars"
flat = re.sub(r"\s+", " ", sub)
assert re.sub(r"\s+", " ", desc.rstrip("\u2026")) in re.sub(r"\s+", " ", strip_md(sub)) or \
    desc.rstrip("\u2026") in strip_md(sub), "description must be verbatim from the note"
print(f"OK description ({len(desc)} chars): {desc}")

# 5 — mirror the JS section parser over the real subtitle.
def norm_head(h):
    h = re.sub(r"[*_`#>]", " ", str(h or ""))
    h = h.lower().replace("\u2018", "").replace("\u2019", "")
    h = re.sub(r"[^a-z0-9 ]", " ", h)
    return re.sub(r"\s+", " ", h).strip()

def clean_section(t):
    t = re.sub(r"\r\n", "\n", str(t or ""))
    t = re.sub(r"^\s*-{3,}\s*$", "", t, flags=re.M)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()

SECTION_MAP = {
    "nutshell": "nutshell", "human": "human", "child": "child",
    "grandma": "grandma", "naya": "naya",
    "what it all means": "means", "what it means": "means",
    "why": "why", "how it connects": "connects",
    "what is in it for you": "foryou", "what changes now": "learning",
    "the learning": "learning", "learning": "learning",
}
ELAB = {"two views", "the layout", "the difference", "the build"}
def split_inline_nutshell(body):
    INLINE = ["Two views", "The layout", "The difference", "Why", "The build"]
    tmp = str(body or "")
    for L in INLINE:
        tmp = tmp.replace("**" + L + ":**", "\n\x00" + L + "\x01")
    parts = tmp.split("\n\x00")
    nutshell = clean_section(parts[0] if parts else "")
    why = ""
    for seg in parts[1:]:
        cut = seg.find("\x01")
        label = "" if cut == -1 else seg[:cut]
        text = clean_section(seg if cut == -1 else seg[cut + 1:])
        if not text:
            continue
        if label == "Why":
            if not why:
                why = text
            continue
        nutshell = (nutshell + "\n\n**" + label + ":** " + text) if nutshell else text
    return nutshell, why

paras = re.split(r"\n\s*\n", sub)
secs = {}
hook_py = ""
for p in paras:
    t = p.strip()
    if not t:
        continue
    if t.startswith("*Filed by Intelligence Loop"):
        continue
    if "Paired Naya Note:" in t:
        continue
    m = re.match(r"^\*\*([^*]+):\*\*\s*(.*)$", t, re.S)
    if not m:
        if "nutshell" not in secs:
            secs["nutshell"] = clean_section(t)
        continue
    label = norm_head(m.group(1))
    body = clean_section(m.group(2))
    if not body:
        continue
    if label == "hook":
        hook_py = re.sub(r"\s+", " ", body).strip()
        continue
    if label == "nutshell":
        nut, why = split_inline_nutshell(body)
        secs["nutshell"] = nut
        if why and "why" not in secs:
            secs["why"] = why
        continue
    if label in ELAB:
        secs["nutshell"] = (secs.get("nutshell", "") + "\n\n" + body).strip() \
            if secs.get("nutshell") else body
        continue
    key = SECTION_MAP.get(label)
    if key and key not in secs:
        secs[key] = body
need = ["nutshell", "human", "child", "grandma", "naya", "why", "learning"]
missing = [k for k in need if k not in secs]
assert not missing, f"sections missing from parse: {missing}"
assert hook_py, "hook missing from parse"
print("OK sections parsed from the real subtitle:")
for k in need:
    print(f"   {k}: {len(secs[k].split())} words")
print(f"   hook: {len(hook_py.split())} words")
assert "Two views" in secs["nutshell"], "nutshell lost 'Two views'"
assert "The build" in secs["nutshell"], "nutshell lost 'The build'"
assert "it connects all the worlds" in secs["why"], "why section wrong"
assert "built as their own world" in secs["learning"], "learning section wrong"
print("OK footer stripped: 'Filed by Intelligence Loop' not in any section:",
      all("Filed by Intelligence Loop" not in v for v in secs.values()))

# 6 — fill the meta tokens.
assert add.count("__PHASE1_TITLE__") == 1
assert add.count("__PHASE1_DESCRIPTION__") == 1
add = add.replace("__PHASE1_TITLE__", title)
add = add.replace("__PHASE1_DESCRIPTION__", desc)
assert "__PHASE1_" not in add, "unfilled token left in additions"

# 7 — S1: insert the additions before `export default {`.
anchor = "export default {"
assert base.count(anchor) == 1, f"export default anchor: {base.count(anchor)}"
built = base.replace(anchor, add + "\n" + anchor)
print("OK S1 additions inserted")

# 8 — S2: insert the phase-1 routes before the existing note-route block.
marker = "const noteMatch = url.pathname.match"
assert built.count(marker) == 1, f"note-route marker: {built.count(marker)}"
idx = built.find(marker)
line_start = built.rfind("\n    if (request.method", 0, idx)
assert line_start != -1, "note-route if-statement start not found"
routes = """    // ---- PHASE 1 routes (2026-11-12) ----
    // robots.txt + sitemap.xml + the cover image + the bot note page.
    // Browsers fall through to the existing 302 below (notes open IN
    // the Hub). These routes need run_worker_first entries
    // (/robots.txt, /sitemap.xml, /images, /images/*) or the assets
    // layer answers them with the SPA fallback first — that is the
    // root cause of the live fault (see the record).
    // HEAD is answered like GET on these routes: a HEAD that fell
    // through to the assets layer came back text/html (the SPA shell),
    // which is the same fault in miniature — caught by self-check
    // round 2. The platform strips the body for HEAD responses.
    if ((request.method === "GET" || request.method === "HEAD") && url.pathname === "/robots.txt") {
      return new Response(phase1RobotsTxt(url.origin), { status: 200, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "public, max-age=3600" } });
    }
    if ((request.method === "GET" || request.method === "HEAD") && url.pathname === "/sitemap.xml") {
      return new Response(phase1SitemapXml(url.origin), { status: 200, headers: { "Content-Type": "application/xml;charset=UTF-8", "Cache-Control": "public, max-age=3600" } });
    }
    if ((request.method === "GET" || request.method === "HEAD") && url.pathname === "/images/infinite-smart-feeds-cover.png") {
      return await phase1CoverImage(request, env);
    }
    if ((request.method === "GET" || request.method === "HEAD") && url.pathname.startsWith("/images/")) {
      return new Response("Image not found", { status: 404, headers: { "Content-Type": "text/plain;charset=UTF-8", "Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow" } });
    }
    if (request.method === "GET" || request.method === "HEAD") {
      const p1Match = url.pathname.match(/^\\/(?:s|notes|smart-notes|note)\\/([^/]+)\\/?$/);
      if (p1Match && !phase1IsBrowserUA(request.headers.get("User-Agent") || "")) {
        return await phase1ServeNote(request, env, p1Match[1], url.origin);
      }
    }
"""
built = built[:line_start + 1] + routes + built[line_start + 1:]
print("OK S2 phase-1 routes inserted")

# 9 — guards: the base is untouched, no phase-2 machinery smuggled in.
assert built.startswith(base[:base.find("export default {")]), \
    "base prefix changed — the splice corrupted the base"
for bad in ['"/feed"', '"/cluster', "/api/seo", "seoScorePage", "autoTags",
            "renderPublicNotePage", "renderClusterPage", "renderFeedPage",
            "landingRedirect", "INTEL_TODAY"]:
    assert bad not in built, f"phase-2 marker leaked into phase-1 worker: {bad}"
for fn in ["phase1RobotsTxt", "phase1SitemapXml", "phase1ServeNote",
           "phase1CoverImage", "phase1ParseSections", "renderPhase1Note",
           "phase1CanonicalSlug"]:
    assert built.count(fn) >= 2, f"missing phase-1 function: {fn}"
assert built.count("renderNote(rec)") >= 2, "renderNote reuse missing"
# The slug bug that bit the first probe: the live route is /s/sn2696
# (no hyphen) while the canonical id is sn-2696 — the allowlist
# comparison must be normalized, never raw.
assert 'phase1CanonicalSlug(slug) !== c.slug' in built, "allowlist not normalized"
print("OK guards: base verbatim, no phase-2 markers, all phase-1 functions present")

open(OUT, "w", encoding="utf-8").write(built)
print(f"wrote {OUT}: {len(built)} bytes")
print(f"TITLE={title}")
print(f"DESCRIPTION={desc}")
