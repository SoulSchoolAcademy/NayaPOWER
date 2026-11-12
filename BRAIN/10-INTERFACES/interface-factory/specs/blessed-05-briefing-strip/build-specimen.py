#!/usr/bin/env python3
"""Assemble the Blessed-05 specimen page by verbatim harvest from the part file.
The part is canonical; this script only inlines its <style> and <script>
blocks. Never hand-edit the assembled output."""
import os, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = ["nj-briefing-strip.html"]

def extract(path, tag):
    t = open(os.path.join(HERE, path), encoding="utf-8").read()
    # ^ anchor: the doc comment mentions <style>/<script> in prose — only
    # match the real tags, which start at the beginning of a line.
    m = re.search(r"^<%s>(.*?)</%s>" % (tag, tag), t, re.S | re.M)
    return m.group(1) if m else ""

styles = "\n".join(extract(p, "style") for p in PARTS)
scripts = "\n".join(extract(p, "script") for p in PARTS)

SPEC_CSS = """
/* ---- specimen page chrome (NOT part of the blessed part) ---- */
html,body{margin:0;padding:0;background:#050507;color:#fff;
  font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;}
.nj-spec{max-width:1060px;margin:0 auto;padding:40px 24px 80px;}
.nj-spec-head{margin-bottom:36px;}
.nj-spec-kicker{font-size:12px;font-weight:800;letter-spacing:.14em;
  text-transform:uppercase;color:#fff;opacity:.65;margin-bottom:10px;}
.nj-spec-head h1{margin:0;font-size:34px;font-weight:800;color:#fff;}
.nj-spec-head p{margin:8px 0 0;color:#fff;opacity:.7;font-size:15px;max-width:640px;line-height:1.6;}
.nj-spec-block{background:#0a0a0f;border:1.5px solid rgba(255,255,255,.12);
  border-radius:20px;padding:28px;margin-bottom:24px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 18px 44px rgba(0,0,0,.5);}
.nj-spec-block h2{margin:0 0 6px;font-size:20px;color:#fff;}
.nj-spec-note{margin:0 0 20px;color:#fff;opacity:.6;font-size:13.5px;line-height:1.6;}
.nj-spec-stack{display:flex;flex-direction:column;gap:16px;}
.nj-spec-lab{font-size:11px;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;color:#fff;opacity:.5;margin:0;}
.nj-spec-foot{margin-top:36px;color:#fff;opacity:.55;font-size:13px;line-height:1.6;}
.nj-spec-foot b{color:#fff;}
@media(max-width:700px){ .nj-spec{padding:24px 16px 60px;} .nj-spec-head h1{font-size:26px;}
  .nj-spec-block{padding:20px 16px;} }
"""

PURPLE = ("#a06bff", "160,107,255")
BLUE   = ("#3fb8ff", "63,184,255")
GREEN  = ("#2fe89e", "47,232,158")
GOLD   = ("#ffbf3d", "255,191,61")
ORANGE = ("#ff9a5a", "255,154,90")
RED    = ("#ff5e6c", "255,94,108")
MAGENTA= ("#e84fff", "232,79,255")

def strip(tag, c, r, what, why, verb, extra_cls="", extra_attr=""):
    open_tag = ('<%s class="nj-brief %s" style="--nj-c:%s;--nj-c-rgb:%s"%s>'
                % (tag, extra_cls, c, r, extra_attr)).replace('class="nj-brief "', 'class="nj-brief"')
    return (
        open_tag +
        '<span class="nj-brief-what">%s</span>' % what +
        '<span class="nj-brief-sep" aria-hidden="true">—</span>' +
        '<span class="nj-brief-why">%s</span>' % why +
        '<span class="nj-brief-dot" aria-hidden="true">·</span>' +
        '<span class="nj-brief-verb">%s<span class="nj-brief-arrow" aria-hidden="true">→</span></span>' % verb +
        '</%s>' % tag
    )

def lab(t):
    return '<p class="nj-spec-lab">%s</p>' % t

body = "\n".join([
    '<div class="nj-spec">',
    '<div class="nj-spec-head">'
    '<div class="nj-spec-kicker">Blessed 05 · v1.0.0 · Specimen</div>'
    '<h1>Briefing Strip</h1>'
    '<p>The Tell-Me-My-Stats strip. One line: WHAT + WHY + ONE VERB. '
    'Obsidian at rest with a white rim — it ignites in its own color on touch only. '
    'The whole strip is one control. Factory gap #1: Dashboard · Intel Today · Reports.</p>'
    '</div>',

    '<div class="nj-spec-block"><h2>At rest — the spectrum walk</h2>'
    '<p class="nj-spec-note">Each strip owns one spectrum color (Law 5 — one board, one color). '
    'Adjacent strips never share a hue (Law 4). All text is white — hierarchy from size and weight, never color (Law 1).</p>'
    '<div class="nj-spec-stack">'
    + strip("a", *PURPLE, "825 points to go", "about 33 wall posts at your pace", "See how", extra_attr=' href="#dashboard"')
    + strip("a", *BLUE, "3 briefings ready", "today\u2019s intel, scored and waiting", "Read now", extra_attr=' href="#today"')
    + strip("a", *GREEN, "40 link clicks", "busiest day was Friday", "View report", extra_attr=' href="#reports"')
    + strip("button", *GOLD, "1,240 points earned", "your best week yet", "Keep going", extra_attr=' type="button"')
    + '</div></div>',

    '<div class="nj-spec-block"><h2>States</h2>'
    '<p class="nj-spec-note">Rest · hover-touch (rim ignites in own color, arrow nudges) · '
    'press (sinks) · focus-visible (own-color ring). Text stays white in every state.</p>'
    '<div class="nj-spec-stack">'
    + lab("Rest")
    + strip("a", *ORANGE, "12 invites sent", "2 joined — the river is moving", "Invite more", extra_attr=' href="#invite"')
    + lab("Hover / touch-ignited")
    + strip("a", *ORANGE, "12 invites sent", "2 joined — the river is moving", "Invite more", extra_cls="nj-demo-hover", extra_attr=' href="#invite"')
    + lab("Pressed")
    + strip("a", *ORANGE, "12 invites sent", "2 joined — the river is moving", "Invite more", extra_cls="nj-demo-press", extra_attr=' href="#invite"')
    + lab("Focus-visible (keyboard)")
    + strip("a", *ORANGE, "12 invites sent", "2 joined — the river is moving", "Invite more", extra_cls="nj-demo-focus", extra_attr=' href="#invite"')
    + '</div></div>',

    '<div class="nj-spec-block"><h2>One board, one color — ignition</h2>'
    '<p class="nj-spec-note">The strip below owns red. Touch it and only its rim and arrow ignite — '
    'the face stays obsidian, the text stays white. (Law 6: alive = responsive, not lit at rest.)</p>'
    '<div class="nj-spec-stack">'
    + strip("a", *RED, "Streak at 6 days", "one more day beats your best", "Protect it", extra_attr=' href="#streak"')
    + strip("a", *MAGENTA, "2 Smart notes today", "your thinking, compounded", "Review", extra_attr=' href="#notes"')
    + '</div></div>',

    '<div class="nj-spec-foot">Blessed 05 · Briefing Strip · v1.0.0<br>'
    'Law: the Anatomy of Naya Design, ratified 2026-10-31. '
    'Tokens verbatim. Every control works or it does not ship. '
    'Import, never copy.</div>',
    '</div>',
])

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Blessed 05 — Briefing Strip · Specimen</title>
<style>
%s
</style>
<style>
%s
</style>
</head>
<body>
%s
<script>
%s
</script>
</body>
</html>
""" % (styles, SPEC_CSS, body, scripts)

out = os.path.join(HERE, "specimen.html")
open(out, "w", encoding="utf-8").write(html)
print("specimen.html written:", len(html), "bytes")
for p in PARTS:
    hh = hashlib.sha256(open(os.path.join(HERE, p), "rb").read()).hexdigest()[:12]
    print("  harvested", p, "sha256:" + hh)
