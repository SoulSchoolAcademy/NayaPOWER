#!/usr/bin/env python3
"""Whole-system connection round — PORTAL fix v2b (corrects a v2 parse-order bug).

Found by render: edit-portal-v2.py placed the deed-move script BEFORE the
<div id="returningView"> it looked up, so at parse time
getElementById('returningView') was null and the IIFE returned early — the
deed never moved out of the circle at phone width (probe: deedParent stayed
DIV.content, input still hit SECTION.stage). The fix: the move script no
longer requires `returning` at parse time (it is only needed for the
widen/restore path, looked up lazily inside place()), and place() re-runs on
DOMContentLoaded. Also tightens the phone presence letter-spacing so
"NAYA WELCOMES YOU" fits the 248px circle on one line.

Input: maker/welcome-staged.html (v2 output, sha 157ccc43). Output: same
file, in place.
"""
import hashlib
import re

P = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/maker/welcome-staged.html"

text = open(P, encoding="utf-8", errors="ignore").read()
print("v2b input:", len(text.encode("utf-8")), hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])
assert hashlib.sha256(text.encode("utf-8")).hexdigest().startswith("157ccc43"), "v2 base moved"


def replace_once(s, old, new, name):
    assert s.count(old) == 1, f"{name}: anchor count {s.count(old)} != 1: {old[:90]!r}"
    return s.replace(old, new, 1)


# ---------------------------------------------------------------- parse-order fix
old = """  var stage = document.querySelector('.stage');
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
  place();"""
new = """  var stage = document.querySelector('.stage');
  var portal = document.querySelector('.portal');
  var content = document.querySelector('.content');
  var sentence = document.getElementById('fpDeedSentence');
  var reader = document.getElementById('fpDeedReader');
  /* v2b: `returning` is NOT required here — this script sits BEFORE the
     <div id="returningView"> in the document, so at parse time it is null
     and the old guard returned early, leaving the deed in the circle. The
     narrow path never needs it; the widen path looks it up lazily. */
  if (!stage || !portal || !content || !sentence || !reader) return;
  function place(){
    var narrow = window.matchMedia('(max-width:480px)').matches;
    if (narrow){
      if (sentence.parentElement !== stage){
        stage.insertBefore(sentence, portal.nextSibling);
        stage.insertBefore(reader, sentence.nextSibling);
      }
    } else {
      var returning = document.getElementById('returningView');
      if (returning && sentence.parentElement !== content){
        content.insertBefore(sentence, returning);
        content.insertBefore(reader, returning);
      }
    }
  }
  place();
  if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', place);
  }"""
text = replace_once(text, old, new, "v2b-parse-order")

# ---------------------------------------------------------------- presence fits one line in the 248px circle
old = "  .presence{font-size:15px;letter-spacing:.12em}"
new = "  .presence{font-size:15px;letter-spacing:.06em}"
text = replace_once(text, old, new, "v2b-presence-spacing")

open(P, "w", encoding="utf-8").write(text)
b = len(text.encode("utf-8"))
print("V2b written:", P, b, "sha:", hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])
scripts = re.findall(r"<script>(.*?)</script>", text, re.S)
print("script blocks:", len(scripts))
for i, sc in enumerate(scripts):
    open(f"/tmp/wsc-p2b-{i}.js", "w").write(sc)
