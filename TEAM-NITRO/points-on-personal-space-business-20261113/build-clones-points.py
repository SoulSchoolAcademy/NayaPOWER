#!/usr/bin/env python3
"""Build the Space/Business clones for the POINTS round (Clone Law, Shawn 22:35Z).

Lane-local adaptation of space-business-mirror-personal-20261112/build-clone.py
(the original script and the audit files it reads are untouched). The ONLY
differences from the original:
  - the rooms template source is the lane-local rooms-points.html (the audit
    rooms file + the points pill + wiring, sha 553ec866…; the audit file itself
    is never modified, so the original script still re-runs unchanged);
  - live + the worlds' live files are read from the original lane dir (SRC);
  - outputs are space-points.html / business-points.html in this lane dir;
  - the template-vs-hero assertion additionally allows the pill hunks
    (pill markup + wiring), named explicitly below.

Template = rooms-points (live Personal v9 + rooms-plus fix + pill + wiring)
           + hero-fix block.
Clone = template with ONLY: title + story/mission voice (my->our, via the
page-kind mechanism + the world's own story text) + the world's own content
(name, tagline, avatar, PAGE_ALIAS, feed-row owner names, smart-name default).
Everything else byte-identical to the template. Every swap is asserted by count.
"""
import hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.expanduser("~/workspace/team-nitro/space-business-mirror-personal-20261112")
AUDIT = os.path.expanduser("~/workspace/team-nitro/page-audit-remeasure-20261112")

def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return open(p, "rb").read()

LIVE_SHA = "992ab18c29315e7654f45c36eb43e30aadfc2ea5642394bbd9884f21617e3f50"
HERO_SHA = "8d0273fc7c1437698f739d4e8a0d8677258a50e919b4aa416f8c28a5cc8494f0"
ROOMS_POINTS_SHA = "553ec8660c8c8918fae11444ea8c8ad18574dff3aa18985d4ef3ccdc353109ef"

live = read(os.path.join(SRC, "personal-live.html"))
assert sha(live) == LIVE_SHA, f"live base sha moved: {sha(live)}"
hero = read(os.path.join(AUDIT, "personal-hero-fix.html")).decode("utf-8", "replace")
assert sha(read(os.path.join(AUDIT, "personal-hero-fix.html"))) == HERO_SHA, "hero fix sha mismatch"
rooms = read(os.path.join(HERE, "rooms-points.html")).decode("utf-8", "replace")
assert sha(read(os.path.join(HERE, "rooms-points.html"))) == ROOMS_POINTS_SHA, "rooms-points sha mismatch"
assert sha(live.decode("utf-8", "replace").encode("utf-8")) == LIVE_SHA  # live file is the base
assert 'id="pointsdisplay"' in rooms and "POINTS PILL (2026-11-13)" in rooms, "rooms-points lacks the pill"

# --- compose template: rooms-plus file + hero-fix style block before </body> ---
m = re.search(r'<style id="hero-fix-20261112">.*?</style>', hero, re.S)
assert m, "hero block not found in hero-fix file"
hero_block = m.group(0)
assert hero_block not in rooms, "hero block already in rooms file (unexpected)"
idx = rooms.rfind("</body>")
assert idx > 0
template = rooms[:idx] + hero_block + "\n" + rooms[idx:]
# verify composition: template vs hero file differs only by the rooms-plus hunks
import difflib
def diff_ops(a, b):
    return [(t, i1, i2, j1, j2) for t, i1, i2, j1, j2 in
            difflib.SequenceMatcher(None, a.splitlines(), b.splitlines(), autojunk=False).get_opcodes() if t != "equal"]
ops_th = diff_ops(template, hero)
print("template-vs-hero-fix non-equal ops:", [(t, i1, i2) for t, i1, i2, j1, j2 in ops_th])
for t, i1, i2, j1, j2 in ops_th:
    seg = "\n".join(template.splitlines()[i1:i2])
    assert ("rooms.style.position=phone?'absolute':'fixed'" in seg or "ROOMS-PLUS OCCLUSION FIX" in seg
            or "ph-points" in seg or "POINTS PILL" in seg or "pointscount" in seg), f"unexpected template-vs-hero hunk: {seg[:200]}"
ops_tr = diff_ops(template, rooms)
print("template-vs-rooms non-equal ops:", [(t, i1, i2) for t, i1, i2, j1, j2 in ops_tr])
assert len(ops_tr) == 1 and ops_tr[0][0] == "delete" and (ops_tr[0][2] - ops_tr[0][1]) == 23, "template-vs-rooms-points must be exactly the 23-line hero insertion"
open(os.path.join(HERE, "template-points-composed.html"), "w", encoding="utf-8").write(template)
print("template-points-composed.html sha:", sha(template.encode("utf-8")), "bytes:", len(template.encode("utf-8")))

# --- harvest the world's own values from its live file ---
PERSONAL_STORY = ("Shawn Vibert builds NayaNET — the intelligent layer of the internet, where "
    "intelligence compounds and everybody wins. This is his personal world: his feed, his messages, "
    "his invites, his reports and intel, all working, all live. Welcome to the new world. Welcome to the new net.")
PERSONAL_TAG = "Welcome to my world — make a post on my feed, send a message, make yourself at home"

def harvest(world_file):
    s = open(os.path.join(SRC, world_file), encoding="utf-8", errors="replace").read()
    name = re.search(r"<title>(.*?)</title>", s).group(1)
    tagline = re.search(r'id="ptag"[^>]*>(.*?)</div>', s).group(1)
    story = re.search(r'id="abouttext">(.*?)</p>', s).group(1)
    kind = re.search(r"window\.MSHIP_PAGE_KIND='([^']*)'", s).group(1)
    alias = re.search(r"window\.MSHIP_PAGE_ALIAS=\(typeof PAGE_ALIAS!==\"undefined\"\?PAGE_ALIAS:'([^']*)'\)", s).group(1)
    stroke = re.search(r'stroke%3D%22%23([0-9a-f]{6})%22', s).group(1)
    letter = re.search(r'middle%22%3E(.)%3C/text', s).group(1)
    return {"name": name, "tagline": tagline, "story": story, "kind": kind, "alias": alias,
            "stroke": stroke, "letter": letter}

WORLDS = {
    "space": harvest("space-live.html"),
    "business": harvest("business-live.html"),
}
print("harvested:", json.dumps(WORLDS, indent=1, ensure_ascii=False))
assert WORLDS["space"] == {"name": "Our Community", "tagline": "Together we grow",
    "kind": "space", "alias": "flagship-community", "stroke": "2fe89e", "letter": "C",
    "story": WORLDS["space"]["story"]}, "space harvest mismatch"
assert WORLDS["business"]["name"] == "Acme Corp" and WORLDS["business"]["kind"] == "business" \
    and WORLDS["business"]["alias"] == "flagship-business" and WORLDS["business"]["stroke"] == "3fb8ff" \
    and WORLDS["business"]["letter"] == "A" and WORLDS["business"]["tagline"] == "We build amazing things"

def swap(text, old, new, expect, label):
    n = text.count(old)
    assert n == expect, f"{label}: expected {expect} occurrences of {old[:70]!r}, found {n}"
    return text.replace(old, new)

report = {}
for world, w in WORLDS.items():
    t = template
    ops = []
    box = [t]
    def do(old, new, expect, label):
        box[0] = swap(box[0], old, new, expect, f"{world}:{label}")
        ops.append({"label": label, "expect": expect, "new": new[:80]})
    # injector fallback FIRST (its default is flagship-community; must not be confused with the alias swap)
    do("(typeof PAGE_ALIAS !== 'undefined' ? PAGE_ALIAS : 'flagship-community')",
       "(typeof PAGE_ALIAS !== 'undefined' ? PAGE_ALIAS : '" + w["alias"] + "')", 1, "injector-fallback-alias")
    # identity: alias literals (7 sites: assignments + fallbacks)
    do("flagship-personal", w["alias"], 7, "page-alias-literals")
    # page kind binding
    do("window.MSHIP_PAGE_KIND='personal'", "window.MSHIP_PAGE_KIND='" + w["kind"] + "'", 1, "page-kind")
    # title + name
    do("<title>Shawn Vibert</title>", "<title>" + w["name"] + "</title>", 1, "title-tag")
    do('>Shawn Vibert</div>', ">" + w["name"] + "</div>", 1, "pname")
    do('class="os-owner-name">Shawn Vibert</span>', 'class="os-owner-name">' + w["name"] + "</span>", 1, "owner-name")
    do("localStorage.setItem('naya.name','Shawn Vibert')",
       "localStorage.setItem('naya.name','" + w["name"] + "')", 1, "name-migration-set")
    do("pn.textContent='Shawn Vibert'", "pn.textContent='" + w["name"] + "'", 1, "name-migration-text")
    do("Memberships \\u2014 Shawn Vibert", "Memberships \\u2014 " + w["name"], 1, "memberships-doc-title")
    # story text (4 identical occurrences: abouttext, story-text, 2 JS fallbacks)
    do(PERSONAL_STORY, w["story"], 4, "story-text")
    # tagline: the Personal tagline carries a trailing period in all 3 spots (static div + 2 JS); the world's own tagline has none
    do(PERSONAL_TAG + ".", w["tagline"], 3, "tagline")
    # feed-row owner names + activity voice
    do("Shawn&rsquo;s Smart Notes", w["name"] + "&rsquo;s Smart Notes", 1, "feed-smart")
    do("Shawn&rsquo;s Naya Notes", w["name"] + "&rsquo;s Naya Notes", 1, "feed-naya")
    do(">My Activity — tap for the full dashboard ↓</button>", ">Our Activity — tap for the full dashboard ↓</button>", 1, "feed-activity")
    # avatar: stroke + letter (data-URI SVG, 1 each)
    do("stroke%3D%22%23a06bff%22", "stroke%3D%22%23" + w["stroke"] + "%22", 1, "avatar-stroke")
    do("middle%22%3EN%3C/text", "middle%22%3E" + w["letter"] + "%3C/text", 1, "avatar-letter")
    # smart-name fallbacks (the visitor's default display name)
    do("var baUser='Shawn'", "var baUser='" + w["name"] + "'", 1, "smartname-bauser")
    do("||'Shawn'", "||'" + w["name"] + "'", 1, "smartname-fallback1")
    do("|| 'Shawn'", "|| '" + w["name"] + "'", 1, "smartname-fallback2")
    do("return 'Shawn'", "return '" + w["name"] + "'", 1, "smartname-fallback3")
    t = box[0]
    # --- integrity: nothing of Personal's identity may remain, except the shared history + shared courses ---
    assert "flagship-personal" not in t, f"{world}: flagship-personal remains"
    assert "Shawn Vibert</title>" not in t and ">Shawn Vibert</div>" not in t, f"{world}: name remains"
    assert PERSONAL_STORY not in t, f"{world}: personal story remains"
    assert PERSONAL_TAG not in t, f"{world}: personal tagline remains"
    assert "Shawn&rsquo;s Smart Notes" not in t and "Shawn&rsquo;s Naya Notes" not in t, f"{world}: feed owner remains"
    # kept deliberately: the shared AI Masterclass course list (Shawn's video) + build-history comments
    assert "Kelowna Dancing Guy" in t, f"{world}: shared course video lost (must stay verbatim)"
    assert "Shawn Vibert’s True Story" in t, f"{world}: shared course video title lost"
    # clone-vs-template diff must be exactly the swaps: count differing lines, all must contain a swapped value
    tlines, clines = template.splitlines(), t.splitlines()
    assert len(tlines) == len(clines), f"{world}: line count changed ({len(tlines)} vs {len(clines)})"
    ndiff = sum(1 for a, b in zip(tlines, clines) if a != b)
    print(f"{world}: {ndiff} lines differ from template (all swaps, no structural change)")
    out = os.path.join(HERE, f"{world}-points.html")
    open(out, "w", encoding="utf-8").write(t)
    report[world] = {"file": f"{world}-points.html", "sha256": sha(t.encode("utf-8")),
                     "bytes": len(t.encode("utf-8")), "diff_lines": ndiff, "swaps": ops,
                     "values": w}
    print(f"{world}: wrote {out} sha {report[world]['sha256']} bytes {report[world]['bytes']}")

with open(os.path.join(HERE, "swap-report-points.json"), "w") as f:
    json.dump(report, f, indent=1, ensure_ascii=False)
print("swap-report-points.json written")
