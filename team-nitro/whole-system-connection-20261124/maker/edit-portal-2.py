#!/usr/bin/env python3
"""Whole-system connection round — PORTAL build part 2 (maker v1).

Input: maker/welcome-staged.html (part 1 output). Applies items 59, 60/61/63,
65/67/70/72, 32, 46 (+ top-menu Certificate entry if the menu anchor exists),
then verifies items 11/54/56/57. Writes the file back in place.
"""
import hashlib
import json
import re

P = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/maker/welcome-staged.html"
WALK_DEFAULTS = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/scratch/walk-defaults.json"

text = open(P, encoding="utf-8", errors="ignore").read()
print("part2 input:", len(text.encode("utf-8")))


def brace_block(s, start):
    assert s[start] == "{"
    d = 0
    for i in range(start, len(s)):
        if s[i] == "{":
            d += 1
        elif s[i] == "}":
            d -= 1
            if d == 0:
                return start, i + 1
    raise AssertionError("unbalanced braces")


def rule_text(s, selector):
    i = s.find(selector)
    assert i >= 0, "rule not found: " + selector
    j = s.find("{", i)
    a, b = brace_block(s, j)
    return s[i:b]


def replace_once(s, old, new, name):
    assert s.count(old) == 1, f"{name}: anchor count {s.count(old)} != 1: {old[:90]!r}"
    return s.replace(old, new, 1)


# ---------------------------------------------------------------- P8 item 59
# The stage-intro legal row is position:fixed at the bottom with nowrap
# links — at phone width it covers the Read button. At <=480px it must flow
# below the choice buttons (static) with wrapping links, never overlaying.
links_rule = rule_text(text, "html.fp-locked body.fp-stage-on.fp-intro #fpLegal .fp-legal-links{")
assert "flex-wrap:nowrap" in links_rule, links_rule[:200]
i = text.find(links_rule)
assert i >= 0
j = text.find("{", i)
_, b = brace_block(text, j)
fix59 = """
/* WHOLE-SYSTEM CONNECTION 2026-11-24 (item 59): at phone width the fixed
   legal row covered the Read button. It now flows below the choice buttons
   (static) with wrapping links — never an overlay, never a cover. */
@media(max-width:480px){
html.fp-locked body.fp-stage-on.fp-intro #fpLegal{position:static;padding:10px 8px 14px;background:#050507}
html.fp-locked body.fp-stage-on.fp-intro #fpLegal .fp-legal-links{flex-wrap:wrap;overflow:visible}
html.fp-locked body.fp-stage-on.fp-intro #fpLegal .fp-legal-link{white-space:normal}
}"""
text = text[:b] + fix59 + text[b:]
print("item59: phone legal-bar fix added")

# ---------------------------------------------------------------- P9 items 60/61/63
# The official sentence + the i-reader unfold on the typed face (name entry
# IS the agreement). The i- text is the captain's draft offered 02:28Z
# (item 61) — verbatim, split into short paragraphs, one at a time.
DEED_PARAS = [
    "Imagine the internet on steroids. When you put your name here, you get your own world — high-level digital assets which we call digital real estate.",
    "The land. The house — your personal page. Your business. Your space. Part of the NayaNET franchise, the brand Naya — all yours.",
    "You build it, you grow it, and it becomes super valuable.",
    "You get access to the intelligence network — everybody collectively comes together, and we compound intelligence. We call it CSI. You can use all of it.",
    "You're hired — you get the job, you're an ambassador automatically, with an opportunity to earn money: half of what your world brings in, paid to you every day.",
    "You get nine days free to try it out — the Bugatti of the internet. Try it before you buy it.",
    "Hook up your AI to Naya Power and she automates your world — that's your choice.",
    "NayaNET is free forever whether you get Power or not. There's no cost to sign up, nothing upfront, no BS — we set it all up for you, based on what you put in.",
    "You get your own private vault — nobody gets into it, no AIs. AI runs the system, but it cannot access anyone's vault.",
    "No one AI looks over the system — many AIs plug in, all separate, but they can communicate, talk, send messages, and collaborate with you, and they have profiles you can learn about.",
    "You get a private way to communicate — with your friends and family, completely private — and you meet new people automatically, people of like mind.",
    "And all you agree to is one thing: do no harm.",
]
deed_html = """
          <p class="fp-deed-sentence" id="fpDeedSentence">By entering your name, you make it official &mdash; you are signing the Collective Agreement, and you get the deed to your own world: high-level digital real estate &mdash; your personal page, your business, your space &mdash; free forever. <button class="fp-deed-info" id="fpDeedInfo" type="button" aria-label="Read the full agreement">&#9432;</button></p>
          <div class="fp-deed-reader" id="fpDeedReader" hidden>
            <p class="fp-deed-para" id="fpDeedPara"></p>
            <div class="fp-deed-nav"><button class="fp-deed-navbtn" id="fpDeedBack" type="button">&lsaquo; Back</button><span class="fp-deed-count" id="fpDeedCount"></span><button class="fp-deed-navbtn" id="fpDeedNext" type="button">Next &rsaquo;</button></div>
          </div>"""
anchor = "</form>\n          <div class=\"returning\" id=\"returningView\" hidden>"
assert text.count(anchor) == 1, "deed anchor"
text = text.replace(anchor, "</form>" + deed_html + "\n          <div class=\"returning\" id=\"returningView\" hidden>", 1)
# Deed CSS + reader JS: a small dedicated style/script pair right after the
# sentence (isolated; the main style/script blocks are untouched).
deed_css = """
<style>
/* WHOLE-SYSTEM CONNECTION 2026-11-24 (items 60/61/63) — the name box IS the
   deed: the official sentence under it, the i-reader unfold, one paragraph
   at a time, never a wall. */
.fp-deed-sentence{max-width:560px;margin:14px auto 0;padding:0 16px;text-align:center;color:#fff;font-size:17px;line-height:1.55}
.fp-deed-info{display:inline-grid;place-items:center;width:26px;height:26px;border-radius:50%;border:1.5px solid #fff;background:#050507;color:#fff;font-size:17px;line-height:1;cursor:pointer;vertical-align:-5px}
.fp-deed-reader{max-width:560px;margin:12px auto 0;padding:16px 18px;text-align:center;background:#050507;border:1.5px solid rgba(142,36,170,.6);border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.6),0 0 18px rgba(142,36,170,.25)}
.fp-deed-para{color:#fff;font-size:17px;line-height:1.6;margin:0 0 12px}
.fp-deed-nav{display:flex;align-items:center;justify-content:center;gap:16px}
.fp-deed-navbtn{background:#050507;color:#fff;border:1.5px solid rgba(255,255,255,.5);border-radius:999px;padding:8px 18px;font:inherit;font-size:17px;cursor:pointer}
.fp-deed-count{color:#fff;font-size:17px}
</style>"""
deed_js = """
<script>
/* WHOLE-SYSTEM CONNECTION 2026-11-24 (item 61/62) — the i- opens a beautiful
   reader: the full text verbatim, split into short paragraphs, one at a time,
   Next each time, never a wall. */
(function(){
  var PARAS = """ + json.dumps(DEED_PARAS) + """;
  var info = document.getElementById('fpDeedInfo');
  var reader = document.getElementById('fpDeedReader');
  var para = document.getElementById('fpDeedPara');
  var count = document.getElementById('fpDeedCount');
  var next = document.getElementById('fpDeedNext');
  var back = document.getElementById('fpDeedBack');
  if (!info || !reader) return;
  var idx = 0;
  function show(i){
    idx = Math.max(0, Math.min(PARAS.length - 1, i));
    para.textContent = PARAS[idx];
    count.textContent = (idx + 1) + ' of ' + PARAS.length;
    back.hidden = idx === 0;
    next.textContent = idx === PARAS.length - 1 ? 'Done \\u25C6' : 'Next \\u203A';
  }
  info.addEventListener('click', function(){
    var open = reader.hidden;
    reader.hidden = !open;
    if (open) show(0);
  });
  next.addEventListener('click', function(){
    if (idx >= PARAS.length - 1) { reader.hidden = true; return; }
    show(idx + 1);
  });
  back.addEventListener('click', function(){ show(idx - 1); });
})();
</script>"""
anchor2 = "</form>" + deed_html + "\n          <div class=\"returning\" id=\"returningView\" hidden>"
assert text.count(anchor2) == 1
text = text.replace(anchor2, "</form>" + deed_html + deed_css + deed_js + "\n          <div class=\"returning\" id=\"returningView\" hidden>", 1)
# Deed underglow on the name box: the .input keeps its gold start-here edge;
# the deed adds the purple underglow beneath (item 63, one treatment).
input_rule = rule_text(text, ".input{")
assert "box-shadow:" in input_rule
m = re.search(r"box-shadow:\s*([^;]+);", input_rule, re.S)
assert m, "input box-shadow"
old_shadow = m.group(0)
new_shadow = old_shadow[:-1] + ",\n    0 10px 26px rgba(142,36,170,.38);"
text = text.replace(old_shadow, new_shadow, 1)
old = '<form id="entryForm">'
assert text.count(old) == 1
text = text.replace(old, '<form id="entryForm" class="fp-deed">', 1)
print("items 60/61/63: deed sentence + reader + underglow added")

# ---------------------------------------------------------------- P10 items 70/72
# Greeting by name on return + a "This is me" path (never a dead end).
old = '<button class="enter" type="button" id="jumpBackIn">Jump back in &rarr;</button>'
assert text.count(old) == 1
new = ('<p class="returning-greet" id="returningGreet" hidden></p>\n            '
       + old + '\n            <button class="new-account" type="button" id="thisIsMeLine">This is me &mdash; it&rsquo;s my name &rarr;</button>')
text = text.replace(old, new, 1)
# Greeting CSS (green, bigger, unmissable) + fill it + wire This-is-me.
greet_css = """
<style>
.returning-greet{color:#2fe89e;font-size:19px;font-weight:800;text-align:center;margin:0 0 10px}
</style>"""
anchor3 = '<p class="returning-greet" id="returningGreet" hidden></p>'
assert text.count(anchor3) == 1
text = text.replace(anchor3, anchor3 + greet_css, 1)
old = "form.hidden=true; view.hidden=false;"
assert text.count(old) == 1, "returning show anchor"
new = ("form.hidden=true; view.hidden=false;\n"
       "  var _greet=document.getElementById('returningGreet');\n"
       "  if(_greet && name){ _greet.textContent='Welcome back, '+name+'.'; _greet.hidden=false; }")
text = text.replace(old, new, 1)
old = "fresh.addEventListener('click',function(){"
assert text.count(old) == 1
new = ("var _tim=document.getElementById('thisIsMeLine');\n"
       "  if(_tim){ _tim.addEventListener('click',function(){ window.location.href='/identity.html'; }); }\n"
       "  fresh.addEventListener('click',function(){")
text = text.replace(old, new, 1)
print("items 70/72: greeting + This-is-me added")

# ---------------------------------------------------------------- P11 item 32
# A #userName arrival (or ?from=agreement) drops the reader IN the name box
# in every browser state — the returning gate is bypassed for that arrival.
old = "if(!alias){return;}"
assert text.count(old) == 1, "alias guard anchor"
new = ("if(!alias){return;}\n"
       "  /* WHOLE-SYSTEM CONNECTION 2026-11-24 (item 32): a #userName arrival\n"
       "     drops the reader IN the name box — the returning gate is bypassed\n"
       "     for that arrival, in every browser state. */\n"
       "  if(window.location.hash==='#userName'||/[?&]from=agreement/.test(window.location.search)){\n"
       "    var _nm=document.getElementById('userName'); if(_nm){ _nm.focus(); }\n"
       "    return;\n"
       "  }")
text = text.replace(old, new, 1)
print("item32: #userName arrival bypasses the returning gate")

# ---------------------------------------------------------------- P12 item 46
# One block per viewport: the next board locks at the top of the viewport
# (block:'start'), never halfway down it. The helper exists in three copies
# (deck / letter / agreement) — all three take the same fix.
old = "b.scrollIntoView({ behavior: scrollBehavior(), block: 'nearest', inline: 'nearest' });"
assert text.count(old) == 3, f"ensureBeatVisible anchor count {text.count(old)}"
text = text.replace(old, "b.scrollIntoView({ behavior: scrollBehavior(), block: 'start', inline: 'nearest' });")
print("item46: next board locks at viewport top (3 copies)")

# ---------------------------------------------------------------- P13 top-menu Certificate
# Shawn 2026-11-24 10:21: connect the menu to the new certificate.
# Add a Certificate entry to the portal top menu if its anchor is found.
menu_hit = re.search(r'(<a[^>]*>PowerCast</a>|>PowerCast<)', text)
if menu_hit:
    anchor_m = menu_hit.group(0)
    cert_item = anchor_m + '<a class="fp-menu-cert" href="/identity.html">Certificate</a>'
    text = text.replace(anchor_m, cert_item, 1)
    print("menu: Certificate entry added after PowerCast")
else:
    print("menu: no PowerCast anchor found — Certificate entry NOT added (flagged)")

# ---------------------------------------------------------------- verify-only
assert "window.__fpDeckEndReturn=false;S.view='deck'" not in text, "item13 branch left"
assert text.count("Read the Collective Agreement") == 0, "item37 long label left"
assert text.count("/hub?name=") == 0, "item58 hub jump left"
assert text.count("/personal?name=") >= 2, "item58 personal jump missing"
assert "if(!_fpStage&&_fpRestoreStage" not in text and "enterStage();" not in text.split("window.__fpStage=")[0][-2000:], "item56/57 boot"
assert "enterBtn)enterBtn.addEventListener('click',function(){window.location.href='/agreement';});" in text, "item54 portal button"
assert text.count("scale(.94)") >= 1 and text.count("scale(.97)") >= 1, "item11 press rules"
print("verify-only: 13/37/58/54/56-57/11 all hold")

open(P, "w", encoding="utf-8").write(text)
b = len(text.encode("utf-8"))
print("PART2 written:", P, b, "sha:", hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])
