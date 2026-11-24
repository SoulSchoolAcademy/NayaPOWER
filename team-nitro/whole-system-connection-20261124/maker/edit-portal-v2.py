#!/usr/bin/env python3
"""Whole-system connection round — PORTAL fix v2 (checker FAIL -> fix).

Input: maker/welcome-staged.html (v1 output, sha 55eb1b1e). Output: same file,
in place. Every edit asserts its anchor; a failed assert stops the build.

Fixes (checker verdict 2026-11-24):
 1. Phone front door (check A / G.1): at 390px the deed sentence (268px tall)
    overflowed the 288px circle and pushed #userName above it, where the
    portal ring covered it (hit=DIV.portal). Below 480px the deed sentence +
    reader move OUT of the circle to sit under the portal in the stage flow
    (whole, unclipped, tappable); the portal shrinks so presence + form fit
    the circle; presence grows to a readable 15px. Desktop untouched.
 2. Walk into view (item 65): .fp-login has display:flex in CSS, which beats
    the hidden attribute's UA display:none — the login stayed visible and the
    walk sat a full viewport below it. Add .fp-login[hidden]{display:none}
    and scroll the walk into view on load + on the end slide.
 5. Button label (item 37): the VISIBLE #fpEnterDeal still read the long
    label (v1 changed only the capital-C stage labels). Shorten it + the
    comment that quotes it.
 6. Tidies: remove the duplicated "Welcome home." on the walk end slide
    (qEl already says it on completion); hide the deed sentence + reader
    when the returning view shows (typed face only, item 63) so the
    "New user?" line stops clipping on the circle edge.
"""
import hashlib

P = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/maker/welcome-staged.html"

text = open(P, encoding="utf-8", errors="ignore").read()
print("v2 input:", len(text.encode("utf-8")), hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])
assert hashlib.sha256(text.encode("utf-8")).hexdigest().startswith("55eb1b1e"), "v1 base moved"


def replace_once(s, old, new, name):
    assert s.count(old) == 1, f"{name}: anchor count {s.count(old)} != 1: {old[:90]!r}"
    return s.replace(old, new, 1)


# ---------------------------------------------------------------- F5 item 37
# The VISIBLE footer button (case-sensitive: the long label here is
# lowercase "collective"; v1's replace_all only caught the capital-C form).
text = replace_once(text,
                    ">Read the collective agreement &#9670;</button>",
                    ">Read the agreement &#9670;</button>",
                    "item37-visible-button")
text = replace_once(text,
                    "login's 'Read the collective agreement' button",
                    "login's 'Read the agreement' button",
                    "item37-comment-quote")
assert text.count("Read the collective agreement") == 0, "long label left"
print("item37: visible button is now 'Read the agreement'")

# ---------------------------------------------------------------- F2 item 65
# .fp-login[hidden] must actually hide: author display:flex beats the UA
# [hidden] rule. Without this the 100svh login stays up and the walk sits
# a full viewport below the fold.
old = "#fpWalk{display:block;max-width:720px;margin:0 auto;padding:48px 20px 64px;text-align:center;color:#fff}"
new = old + "\n.fp-login[hidden]{display:none} /* WHOLE-SYSTEM CONNECTION v2 (item 65): the author display:flex beat the [hidden] rule, so the login stayed up and the walk sat below the fold. */"
text = replace_once(text, old, new, "item65-login-hidden")
# Scroll the walk into view on load (belt + braces: with the login hidden
# it is already at the top; the scroll covers any residual offset).
old = "  render();\n})();"
new = ("  render();\n"
       "  /* WHOLE-SYSTEM CONNECTION v2 (item 65): the walk must PRESENT on load — Q1 fully in view. */\n"
       "  try { walk.scrollIntoView({block:'start'}); } catch(e){}\n"
       "})();")
text = replace_once(text, old, new, "item65-scroll-on-load")
# End slide: bring the end buttons into view too.
old = "      endEl.hidden = false;\n    }"
new = ("      endEl.hidden = false;\n"
       "      try { walk.scrollIntoView({block:'start'}); } catch(e){}\n"
       "    }")
text = replace_once(text, old, new, "item65-scroll-on-end")
print("item65: login hides, walk scrolls into view on load + end")

# ---------------------------------------------------------------- F10 tidy: "Welcome home." x2 on the end slide
# complete() already sets qEl to 'Welcome home.' — the end slide's own h1
# duplicates it. Remove the end-slide h1 (the endlines + link + buttons stay).
old = '    <div id="fpWalkEnd" hidden>\n      <h1 class="fp-walk-q">Welcome home.</h1>\n'
new = '    <div id="fpWalkEnd" hidden>\n'
text = replace_once(text, old, new, "tidy-welcome-home-dup")
print("tidy: end-slide 'Welcome home.' h1 removed (qEl keeps it)")

# ---------------------------------------------------------------- F1 phone front door
v2_css = """
<style>
/* WHOLE-SYSTEM CONNECTION 2026-11-24 v2 (fix 1 — phone front door): at 390px
   the deed sentence (268px tall) overflowed the 288px circle and pushed the
   name box above it, where the portal ring covered it (hit=DIV.portal).
   Below 480px the portal shrinks so presence + form fit the circle, and the
   deed sentence + reader sit UNDER the portal in the stage flow (moved by
   the script below) — whole, unclipped, tappable. Desktop is untouched. */
@media(max-width:480px){
  .portal{width:min(72vw,248px);height:min(72vw,248px)}
  .presence{font-size:15px;letter-spacing:.12em}
  .stage{flex-direction:column}
  #fpDeedSentence{max-width:360px;margin:10px auto 0}
  #fpDeedReader{max-width:360px;margin:10px auto 0}
}
</style>"""
assert text.count("</head>") == 1
text = text.replace("</head>", v2_css + "\n</head>", 1)

v2_js = """
<script>
/* WHOLE-SYSTEM CONNECTION 2026-11-24 v2 (fix 1): at phone width the deed
   sentence + reader move OUT of the circle to sit under the portal, in the
   stage flow — whole, unclipped, tappable. Desktop keeps them in the
   circle. Listeners attached by the deed script survive the move (same
   elements, new parent). Resize moves them back when the viewport widens. */
(function(){
  var stage = document.querySelector('.stage');
  var portal = document.querySelector('.portal');
  var content = document.querySelector('.content');
  var sentence = document.getElementById('fpDeedSentence');
  var reader = document.getElementById('fpDeedReader');
  var returning = document.getElementById('returningView');
  if (!stage || !portal || !content || !sentence || !reader || !returning) return;
  function place(){
    var narrow = window.matchMedia('(max-width:480px)').matches;
    if (narrow){
      if (sentence.parentElement !== stage){
        stage.insertBefore(sentence, portal.nextSibling);
        stage.insertBefore(reader, sentence.nextSibling);
      }
    } else {
      if (sentence.parentElement !== content){
        content.insertBefore(sentence, returning);
        content.insertBefore(reader, returning);
      }
    }
  }
  place();
  try {
    var mq = window.matchMedia('(max-width:480px)');
    if (mq.addEventListener) mq.addEventListener('change', place);
    else if (mq.addListener) mq.addListener(place);
  } catch(e){}
})();
</script>
"""
anchor = '<div class="returning" id="returningView" hidden>'
assert text.count(anchor) == 1
text = text.replace(anchor, v2_js + anchor, 1)
print("fix1: phone deed moves under the portal; portal shrinks to 248px")

# ---------------------------------------------------------------- F10 tidy: deed hides with the returning view
# The sentence + reader live ONLY on the typed face (item 63). In the
# returning state they crowded the circle and clipped the "New user?" line
# on its bottom edge. Hide them with the form; show them again for a new
# account.
old = "form.hidden=true; view.hidden=false;"
new = ("form.hidden=true; view.hidden=false;\n"
       "  var _deed=document.getElementById('fpDeedSentence'); if(_deed) _deed.hidden=true;\n"
       "  var _dr=document.getElementById('fpDeedReader'); if(_dr) _dr.hidden=true;")
text = replace_once(text, old, new, "tidy-deed-hide-returning")
old = "view.hidden=true; form.hidden=false;"
new = ("view.hidden=true; form.hidden=false;\n"
       "    var _deed2=document.getElementById('fpDeedSentence'); if(_deed2) _deed2.hidden=false;")
text = replace_once(text, old, new, "tidy-deed-show-new-account")
print("tidy: deed hides on the returning face, returns for a new account")

# ---------------------------------------------------------------- verify
assert text.count("Read the collective agreement") == 0
assert text.count("Read the agreement") == 6, text.count("Read the agreement")  # 4 stage + 1 footer + 1 comment quote
assert ".fp-login[hidden]{display:none}" in text
assert "walk.scrollIntoView({block:'start'})" in text
assert text.count("Welcome home.") == 2, text.count("Welcome home.")
assert "matchMedia('(max-width:480px)')" in text
open(P, "w", encoding="utf-8").write(text)
b = len(text.encode("utf-8"))
print("V2 written:", P, b, "sha:", hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])
scripts = __import__("re").findall(r"<script>(.*?)</script>", text, __import__("re").S)
print("script blocks:", len(scripts))
for i, sc in enumerate(scripts):
    open(f"/tmp/wsc-p2-{i}.js", "w").write(sc)
