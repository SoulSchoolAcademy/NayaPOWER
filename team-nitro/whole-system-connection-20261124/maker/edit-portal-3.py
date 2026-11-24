#!/usr/bin/env python3
"""Whole-system connection round — PORTAL build part 3: the walk view.

Items 65/67/68/72: the portal itself presents the 15-question walkthrough —
land on nayanet.app -> name in -> certificate -> the 15 questions presenting.
Questions + default answers harvested VERBATIM from the live walk
(nayanet.app/welcome, 124,064 B, sha 7fd0c05b — the D1-fixed walk file itself
is NOT touched; its question texts are quoted here). State key + shape kept
identical to the walk: naya_welcome_right_v1 {alias, answers, topics, reveal}.
The /api/welcome/complete POST is attempted best-effort (3s timeout) and
NEVER blocks the walk: the end slide renders locally regardless, with the
Smart Link falling back to https://nayanet.app/joinus?ref=<alias> — the same
fallback the walk's own renderEnd uses. Flow order (item 67): agreement ->
15 questions -> world -> pricing.
"""
import hashlib
import json

P = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/maker/welcome-staged.html"
WALK_DEFAULTS = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/scratch/walk-defaults.json"

QUESTIONS = [
    ("motto", "What is your motto?"),
    ("vision", "What is your vision?"),
    ("goal", "What is your goal?"),
    ("mission", "What is your mission?"),
    ("love", "What do you love?"),
    ("dont", "What don't you love?"),
    ("thing", "What's your thing?"),
    ("values", "What are your values?"),
    ("laws", "What laws do you follow?"),
    ("declaration", "What's your declaration?"),
    ("offer", "What do you offer?"),
    ("help", "How does it help?"),
    ("moment", "Tell us about a moment you've done it."),
    ("howwork", "How do you work?"),
    ("start", "How do people start with you?"),
]

defaults = json.load(open(WALK_DEFAULTS))
assert len(defaults) == 15, len(defaults)
QUESTIONS_JSON = json.dumps([
    {"key": k, "q": q, "def": defaults[str(i + 1)]}
    for i, (k, q) in enumerate(QUESTIONS)
])

text = open(P, encoding="utf-8", errors="ignore").read()
print("part3 input:", len(text.encode("utf-8")))

anchor = "</div><!-- /fp-login -->"
assert text.count(anchor) == 1, "login close anchor"
assert 'class="fp-login"' in text, "fp-login class"

walk_html = """
<!-- WHOLE-SYSTEM CONNECTION 2026-11-24 (items 65/67) — the walkthrough lives
     HERE, on the portal. Land on nayanet.app -> name in -> certificate ->
     these 15 questions presenting. The /welcome gate is dead; this is the
     walk. Questions + defaults quoted verbatim from the live D1-fixed walk. -->
<section id="fpWalk" hidden>
  <div class="fp-walk-inner">
    <p class="fp-walk-kicker">Your walkthrough</p>
    <h1 class="fp-walk-q" id="fpWalkQ"></h1>
    <p class="fp-walk-progress" id="fpWalkProgress"></p>
    <textarea class="fp-walk-answer" id="fpWalkAnswer" rows="4"></textarea>
    <p class="fp-walk-hint">Type your answer &mdash; it saves as you go. Tap Enter for the next question.</p>
    <div class="fp-walk-nav">
      <button class="fp-walk-navbtn" id="fpWalkBack" type="button">&lsaquo; Back</button>
      <button class="fp-walk-enter" id="fpWalkEnter" type="button">Enter</button>
    </div>
    <div id="fpWalkEnd" hidden>
      <h1 class="fp-walk-q">Welcome home.</h1>
      <p class="fp-walk-endline">Your own personal branded Smart Link</p>
      <p class="fp-walk-linkrow"><span class="fp-walk-link" id="fpWalkLink"></span> <button class="fp-walk-copy" id="fpWalkCopy" type="button">Copy</button></p>
      <p class="fp-walk-endline">Your answers are saved on this device. Your world is ready &mdash; go see it, then choose your plan.</p>
      <div class="fp-walk-nav">
        <button class="fp-walk-enter" id="fpWalkWorld" type="button">See my world &rarr;</button>
        <button class="fp-walk-navbtn" id="fpWalkPricing" type="button">Choose your plan &rarr;</button>
      </div>
    </div>
  </div>
</section>
<style>
/* WHOLE-SYSTEM CONNECTION 2026-11-24 (items 65/67) — the walk view: one
   question per screen, obsidian + white, the portal's own button language. */
#fpWalk{display:block;max-width:720px;margin:0 auto;padding:48px 20px 64px;text-align:center;color:#fff}
#fpWalk[hidden]{display:none}
.fp-walk-kicker{font-size:15px;font-weight:800;letter-spacing:.22em;text-transform:uppercase;color:#fff;margin:0 0 14px}
.fp-walk-q{font-family:Marcellus,Georgia,serif;font-size:25px;line-height:1.3;color:#fff;margin:0 0 10px}
.fp-walk-progress{color:#fff;font-size:17px;margin:0 0 16px}
.fp-walk-answer{width:100%;min-height:120px;box-sizing:border-box;border-radius:18px;padding:16px 18px;background:#050507;color:#fff;border:1.5px solid rgba(142,36,170,.6);font:inherit;font-size:17px;line-height:1.6;resize:none;box-shadow:0 8px 24px rgba(0,0,0,.6),0 0 18px rgba(142,36,170,.25)}
.fp-walk-hint{color:#fff;font-size:17px;margin:12px 0 18px}
.fp-walk-nav{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:6px}
.fp-walk-enter{display:block;min-width:179px;height:48px;padding:0 24px;white-space:nowrap;border-radius:30px;border:1.5px solid rgba(47,232,158,.65);color:#fff;background:radial-gradient(circle at 50% 0%,#0b2e21,#05060a);font:inherit;font-size:17px;font-weight:800;cursor:pointer}
.fp-walk-enter:active{transform:translateY(1px) scale(.94);filter:brightness(.72)}
.fp-walk-navbtn{background:#050507;color:#fff;border:1.5px solid rgba(255,255,255,.5);border-radius:999px;padding:12px 20px;font:inherit;font-size:17px;cursor:pointer}
.fp-walk-endline{color:#fff;font-size:17px;line-height:1.6}
.fp-walk-linkrow{margin:10px 0 16px}
.fp-walk-link{color:#fff;font-size:17px;font-weight:800}
.fp-walk-copy{background:#050507;color:#fff;border:1.5px solid rgba(255,255,255,.5);border-radius:999px;padding:8px 16px;font:inherit;font-size:17px;cursor:pointer}
</style>
<script>
/* WHOLE-SYSTEM CONNECTION 2026-11-24 (items 65/67/68/72) — the portal walk.
   Entry: ?walk=1&name=...&alias=... (the certificate hands off here).
   State key + shape identical to the live walk: naya_welcome_right_v1
   {alias, answers, topics, reveal}. The complete POST is best-effort and
   never blocks: the end renders locally regardless. */
(function(){
  var QUESTIONS = """ + QUESTIONS_JSON + """;
  var KEY = 'naya_welcome_right_v1';
  var PRICING_URL = 'https://naya-model-pricing.nayapower.workers.dev/';
  var walk = document.getElementById('fpWalk');
  if (!walk) return;
  var params = new URLSearchParams(window.location.search);
  if (params.get('walk') !== '1') return; /* the walk presents only on entry */
  var login = document.querySelector('.fp-login');
  if (login) login.hidden = true;
  walk.hidden = false;
  var alias = params.get('alias') || '';
  var pname = params.get('name') || '';
  try {
    if (alias) localStorage.setItem('nayanet_smart_alias', alias);
    if (pname) localStorage.setItem('nayanet_smart_name', pname);
    if (!alias) alias = localStorage.getItem('nayanet_smart_alias') || '';
    if (!pname) pname = localStorage.getItem('nayanet_smart_name') || '';
  } catch(e){}
  var S = {alias: alias, answers: {}, topics: [], reveal: null};
  try {
    var saved = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (saved && typeof saved === 'object') {
      if (saved.answers) S.answers = saved.answers;
      if (saved.topics) S.topics = saved.topics;
      if (saved.reveal) S.reveal = saved.reveal;
      if (saved.alias) S.alias = saved.alias;
    }
  } catch(e){}
  if (alias) S.alias = alias;
  function save(){ try { localStorage.setItem(KEY, JSON.stringify(S)); } catch(e){} }
  var qEl = document.getElementById('fpWalkQ');
  var progEl = document.getElementById('fpWalkProgress');
  var ansEl = document.getElementById('fpWalkAnswer');
  var backBtn = document.getElementById('fpWalkBack');
  var enterBtn = document.getElementById('fpWalkEnter');
  var endEl = document.getElementById('fpWalkEnd');
  var idx = 0;
  function fit(){ /* D1 pattern: the answer box grows only, never clips */
    ansEl.style.height = 'auto';
    ansEl.style.height = Math.max(120, ansEl.scrollHeight) + 'px';
  }
  function render(){
    var q = QUESTIONS[idx];
    qEl.textContent = '\\u201C' + q.q + '\\u201D';
    progEl.textContent = (idx + 1) + ' of ' + QUESTIONS.length;
    ansEl.value = S.answers[q.key] || q.def || '';
    ansEl.hidden = false;
    backBtn.hidden = idx === 0;
    enterBtn.textContent = idx === QUESTIONS.length - 1 ? 'Finish \\u25C6' : 'Enter';
    endEl.hidden = true;
    fit();
    ansEl.focus();
  }
  ansEl.addEventListener('input', function(){
    S.answers[QUESTIONS[idx].key] = ansEl.value;
    save(); fit();
  });
  backBtn.addEventListener('click', function(){
    if (idx > 0) { idx--; render(); }
  });
  enterBtn.addEventListener('click', function(){
    S.answers[QUESTIONS[idx].key] = ansEl.value;
    save();
    if (idx < QUESTIONS.length - 1) { idx++; render(); return; }
    complete();
  });
  function complete(){
    var done = false;
    function finish(){
      if (done) return; done = true;
      try {
        if (pname) localStorage.setItem('nayanet_smart_name', pname);
        if (S.alias) localStorage.setItem('nayanet_smart_alias', S.alias);
      } catch(e){}
      var a = S.alias || 'yourname';
      var link = (S.reveal && S.reveal.ambassador_link) || ('https://nayanet.app/joinus?ref=' + a);
      document.getElementById('fpWalkLink').textContent = a + '.nayanet.app';
      document.getElementById('fpWalkLink').setAttribute('data-real', link);
      qEl.textContent = 'Welcome home.';
      progEl.textContent = 'Welcome complete';
      ansEl.hidden = true;
      backBtn.hidden = true;
      enterBtn.hidden = true;
      document.querySelector('.fp-walk-hint').hidden = true;
      endEl.hidden = false;
    }
    try {
      var to = setTimeout(finish, 3000);
      fetch('/api/welcome/complete', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({answers: S.answers, topics: S.topics})})
        .then(function(r){ return r.ok ? r.json() : null; })
        .then(function(d){ clearTimeout(to); if (d) S.reveal = d; save(); finish(); })
        .catch(function(){ clearTimeout(to); finish(); });
    } catch(e){ finish(); }
  }
  document.getElementById('fpWalkCopy').addEventListener('click', function(){
    var real = document.getElementById('fpWalkLink').getAttribute('data-real') || '';
    function done(btn){ var b = btn; var t = b.textContent; b.textContent = 'Copied'; setTimeout(function(){ b.textContent = t; }, 1200); }
    var btn = document.getElementById('fpWalkCopy');
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(real).then(function(){ done(btn); }, function(){ done(btn); });
    } else { done(btn); }
  });
  document.getElementById('fpWalkWorld').addEventListener('click', function(){
    var a = S.alias || 'yourname';
    window.location.href = '/personal?name=' + encodeURIComponent(pname || a) + '&alias=' + encodeURIComponent(a);
  });
  document.getElementById('fpWalkPricing').addEventListener('click', function(){
    window.location.href = PRICING_URL;
  });
  render();
})();
</script>"""

text = text.replace(anchor, anchor + walk_html, 1)
open(P, "w", encoding="utf-8").write(text)
b = len(text.encode("utf-8"))
print("PART3 written:", P, b, "sha:", hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])
print("walk markers: fpWalk=", text.count("fpWalk"), " ?walk=1:", text.count("walk') !== '1'"), " questions:", text.count("What is your motto?"))
