#!/usr/bin/env python3
"""Whole-system connection round — AGREEMENT build (maker v1).

Base: maker/agreement-base.html (round-2 tip d22bccf8, blob 8b8ccd95,
22,886,321 B, sha 68dd6ae0). Output: maker/agreement.html.

A1 items 10/15/16/18/19/20/22: the CHOICE view is the first load — play disc
centred, two pills underneath, nothing else; no scrollable letter on choice;
fits one screen; title clear of emblems (the choice screen carries no corner
emblems); deep links ?view=deck|letter.
A2 item 11: choice pills press in (scale .97); the Agree .94 lives in the
portal (dealAgreeBtn) — verified there, not duplicated here.
A3 items 14/27: Accessibility + Disclaimer become real legal pages (12/12),
verbatim from legal-official-20261116/11-accessibility.md +
12-disclaimer.md, in the file's own board format; footer gains the 2 buttons.
The md meta-blockquotes and the bracketed [..Shawn: confirm..] lines are
instructions, not publishable text — EXCLUDED and named in the report.
A4 item 44: PORTRAITS[0] -> 'NAYA_POWER.jpg'.
A5 items 42/43: the N ball HOLDS 2s, then onward in place to the portal's
name box (/?from=agreement#userName) — never a new tab, never back.
A6 item 53: the final-board link row (The Invitation — his pick still owed;
this is the recommendation) — 8 links, each opening its answer in a frame,
all verbatim from SOUL.md vow, the Wise One manifesto, NAYA-PROTOCOL.md,
and the file's own letter beats. Nothing invented.
A7 item 47: hover-tip — no hover-tip element exists in this base (N/A);
legal-row clip — the row already wraps (DONE in bytes); 1919 void — the
stage fills the viewport by design, the empty middle is the frame's own
breathing room (judgment, frame law §14).
A8 item 7: VERIFIED DONE in bytes — ensureAnalyser wires
createMediaElementSource(audio) and drawWave reads getByteFrequencyData;
the synthetic branch is only the fallback. No change.
A9 item 55: VERIFIED DONE in bytes — the daybar IS the old-way bar (orb +
NAYANET left, title dead centre, her photo + NAYA right); the certificate
is the frame standard in identity.html. No redesign.
Item 74: boards untouched — .intel-board CSS rules are asserted unchanged.
Item 3/U1: slide 11 asserted byte-identical (hash 33b0590cfb9f811a).
"""
import hashlib
import html
import json
import re

BASE = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/maker/agreement-base.html"
OUT = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/maker/agreement.html"
LEGAL_DIR = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/legal-official-20261116"
SOUL = "/home/hatch/SOUL.md"
PROTOCOL = "/home/hatch/workspace/team-nitro/NAYA-PROTOCOL.md"
MANIFESTO = "/home/hatch/workspace/your_files/the-wise-one-manifesto.md"
JEWEL = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/maker/jewel-96.png"

text = open(BASE, encoding="utf-8", errors="ignore").read()
base_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
assert base_sha.startswith("68dd6ae0"), base_sha
print("base ok:", len(text.encode("utf-8")), base_sha[:12])
intel_board_rules_before = len(re.findall(r"\.intel-board", text))


def replace_once(s, old, new, name):
    assert s.count(old) == 1, f"{name}: anchor count {s.count(old)} != 1: {old[:90]!r}"
    return s.replace(old, new, 1)


def esc(s):
    return html.escape(s, quote=False)


def md_plain(s):
    """Light markdown strip for reader text: headings lose '#', bold loses '**'."""
    s = re.sub(r"^#{1,6}\s+", "", s, flags=re.M)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"\*([^*]+)\*", r"\1", s)
    s = re.sub(r"> ", "", s)
    return s.strip()


# ---------------------------------------------------------------- beats (file's own)
def beat_text(kind):
    m = re.search(
        r'<span class="ib-kind">' + re.escape(kind) + r"</span>"
        r".*?<div class=\"ib-nutshell\">(.*?)</div>", text, re.S)
    assert m, "beat not found: " + kind
    h = re.sub(r"<[^>]+>", " ", m.group(1))
    return html.unescape(re.sub(r"\s+", " ", h)).strip()


# ---------------------------------------------------------------- A4 item 44
text = replace_once(text, "PORTRAITS = ['Naya_Profile_2.jpg',",
                    "PORTRAITS = ['NAYA_POWER.jpg',", "item44-portraits")
print("item44: PORTRAITS[0] is NAYA_POWER.jpg")

# ---------------------------------------------------------------- A5 items 42/43
old = """function goToPortal(){
  var a = document.createElement('a');
  a.href = 'https://nayanet.app'; a.target = '_blank'; a.rel = 'noopener';
  document.body.appendChild(a); a.click(); a.remove();
}"""
new = """function goToPortal(){
  /* WHOLE-SYSTEM CONNECTION 2026-11-24 (items 42/43): the beautiful N ball
     HOLDS — two full seconds, the N, then ONWARD in place to the portal's
     name box, then the Hub. Never a new tab, never back to the bridge. */
  var hold = document.createElement('div');
  hold.id = 'fpNHold';
  hold.style.cssText = 'position:fixed;inset:0;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;background:#02030a';
  hold.innerHTML = '<img src="' + EMBED.ball + '" alt="Naya" style="width:180px;height:180px" /><p style="color:#fff;font-size:19px;font-weight:800;margin:0">Welcome home.</p>';
  document.body.appendChild(hold);
  setTimeout(function(){ window.location.href = 'https://nayanet.app/?from=agreement#userName'; }, 2000);
}"""
text = replace_once(text, old, new, "items42-43-gotoportal")
print("items42/43: N holds 2s, then in place to the portal name box")

# ---------------------------------------------------------------- A1 choice screen
jewel_b64 = open(JEWEL, "rb").read()
import base64
jewel_uri = "data:image/png;base64," + base64.b64encode(jewel_b64).decode()
assert jewel_uri.startswith("data:image/png;base64,iVBOR"), "jewel uri"

choice_css = """
/* WHOLE-SYSTEM CONNECTION 2026-11-24 (items 10/11/15/16/18/19/20/22) — the
   CHOICE view: the play disc centred, the two buttons underneath, nothing
   else. No scrollable letter here. Everything fits on one screen; the title
   carries no emblems over it. */
#screen-choice .choice-inner{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;min-height:100%;padding:24px 16px 20px;box-sizing:border-box}
#screen-choice .choice-kicker{font-size:13px;font-weight:800;letter-spacing:.22em;color:#fff;margin:0 0 10px}
#screen-choice .choice-title{font-family:Marcellus,Georgia,serif;font-size:34px;line-height:1.2;color:#fff;margin:0 0 6px}
#screen-choice .choice-welcome{font-size:17px;color:#fff;margin:0 0 20px}
#screen-choice .choice-play{display:flex;flex-direction:column;align-items:center;gap:8px;background:none;border:0;cursor:pointer;padding:0;margin:0 0 22px}
#screen-choice .choice-play .pm-play-disc{width:96px;height:96px;border-radius:50%;display:grid;place-items:center;font-size:38px;color:#fff}
#screen-choice .choice-play-label{font-size:13px;font-weight:800;letter-spacing:.22em;color:#fff}
#screen-choice .choice-pills{display:flex;flex-direction:column;align-items:center;gap:13px}
#screen-choice .choice-pill{display:block;min-width:179px;height:48px;padding:0 24px;white-space:nowrap;border-radius:30px;border:1.5px solid rgba(255,255,255,.5);color:#fff;background:#050507;font:inherit;font-size:17px;font-weight:700;cursor:pointer;box-shadow:0 0 6px 0 rgba(255,255,255,.12)}
#screen-choice .choice-pill--deck{border-color:rgba(142,36,170,.65);background:radial-gradient(circle at 50% 0%,#2a0a33,#05060a)}
#screen-choice .choice-pill--letter{border-color:rgba(47,232,158,.65);background:radial-gradient(circle at 50% 0%,#0b2e21,#05060a)}
#screen-choice .choice-pill:active{transform:translateY(1px) scale(.97);filter:brightness(.72);box-shadow:0 0 2px 0 rgba(255,255,255,.08)}
#screen-choice .fp-btn-jewel{display:inline-block;width:18px;height:18px;margin-left:8px;vertical-align:-3px;background:url("__JEWEL__") center/contain no-repeat}
@media(max-width:640px){
#screen-choice .choice-title{font-size:25px}
#screen-choice .choice-pill{width:100%;max-width:340px}
#screen-choice .choice-play .pm-play-disc{width:72px;height:72px;font-size:30px}
}""".replace("__JEWEL__", jewel_uri)

assert text.count("</style>") == 1
text = text.replace("</style>", choice_css + "\n</style>", 1)

choice_html = """
    <!-- ======= CHOICE — first load (WHOLE-SYSTEM CONNECTION 2026-11-24, item 10):
         the play disc centred, the two buttons underneath, nothing else.
         No scrollable letter here — the letter lives behind the Read button. -->
    <section class="screen active" id="screen-choice">
      <div class="panel-body">
        <div class="choice-inner">
          <p class="choice-kicker">NAYANET &middot; THE COLLECTIVE INTELLIGENCE NETWORK</p>
          <h1 class="choice-title">The Collective Agreement</h1>
          <p class="choice-welcome">Welcome. Let&rsquo;s begin with trust.</p>
          <button class="choice-play" id="fpChoicePlay" type="button" aria-label="Begin the visual story"><span class="pm-play-disc" aria-hidden="true">&#9654;</span><span class="choice-play-label">NAYA</span></button>
          <div class="choice-pills">
            <button class="choice-pill choice-pill--deck" id="fpChoiceDeck" type="button">Begin the visual story <span class="fp-btn-jewel" aria-hidden="true"></span></button>
            <button class="choice-pill choice-pill--letter" id="fpChoiceLetter" type="button">Read the agreement <span class="fp-btn-jewel" aria-hidden="true"></span></button>
          </div>
        </div>
      </div>
    </section>
"""
old = '<section class="screen active" id="screen-cover">'
assert text.count(old) == 1
text = text.replace(old, choice_html + '    <section class="screen" id="screen-cover">', 1)
# screens object gains the choice screen; show('choice') keeps the bar.
old = "screens = { cover: document.getElementById('screen-cover'), slide: document.getElementById('screen-slide'), legal: document.getElementById('screen-legal') };"
new = "screens = { cover: document.getElementById('screen-cover'), slide: document.getElementById('screen-slide'), legal: document.getElementById('screen-legal'), choice: document.getElementById('screen-choice') };"
text = replace_once(text, old, new, "choice-screens-object")
old = "if (name === 'cover') barForCover();"
new = "if (name === 'cover' || name === 'choice') barForCover();"
text = replace_once(text, old, new, "choice-show-bar")
print("item10: choice screen is the first load; cover no longer active")

# ---------------------------------------------------------------- A3 legal pages
def parse_legal_md(path):
    """Boards from a legal md: list of (kind, title, [paragraphs]).
    Excludes the meta Status blockquote and the bracketed [..Shawn: confirm..]
    lines (instructions, not publishable text). The closing italic line is
    kept as the last paragraph of the last board."""
    raw = open(path, encoding="utf-8").read()
    # drop the Status blockquote (lines starting with '>')
    lines = [ln for ln in raw.splitlines() if not ln.startswith(">")]
    body = "\n".join(lines)
    parts = re.split(r"\n### Board \d+ — ", body)
    boards = []
    for part in parts[1:]:
        title, _, rest = part.partition("\n")
        paras = []
        for chunk in re.split(r"\n\s*\n", rest.strip()):
            chunk = chunk.strip()
            if not chunk or chunk.startswith("---"):
                continue
            if re.match(r"^\[.*\]$", chunk):
                continue  # bracketed instruction to Shawn, not text
            # bold -> strong, italic -> em (whole-paragraph italics only)
            if chunk.startswith("*") and chunk.endswith("*") and chunk.count("*") == 2:
                paras.append("<p><em>" + esc(chunk.strip("*")) + "</em></p>")
                continue
            chunk = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", chunk)
            chunk = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", chunk)
            paras.append("<p>" + chunk.replace("\n", " ") + "</p>")
        boards.append((title.strip(), paras))
    return boards


def legal_page(key, aria, title, sub, tone_class, tone_hex, boards, kinds):
    assert len(boards) == len(kinds)
    dots = "".join(
        '<span class="ldot%s" style="--dc:%s"></span>' % (" on" if i == 0 else "", tone_hex)
        for i in range(len(boards))
    )
    # dots cycle the three family colours, as the existing pages do
    cycle = ["#a06bff", "#3fb8ff", "#2fe89e"]
    dots = "".join(
        '<span class="ldot%s" style="--dc:%s"></span>' % (" on" if i == 0 else "", cycle[i % 3])
        for i in range(len(boards))
    )
    arts = []
    for (btitle, paras), kind in zip(boards, kinds):
        arts.append(
            '<article class="intel-board tone-%s letter-beat" data-legal-beat>'
            '<div class="ib-blocktop"><div class="ib-identity">'
            '<span class="ib-jewel" aria-hidden="true">&#9670;</span><div>'
            '<span class="ib-kind">%s</span><h2 class="ib-title">%s</h2></div></div></div>'
            '<div class="ib-nutshell">%s</div>'
            '<div class="ib-foot"><img class="ib-foot-logo" data-emb-logo="1" alt="NayaNET"> &middot; NayaNET &middot; The Whole Deal</div>'
            '</article>' % (tone_class, esc(kind), esc(btitle), "".join(paras)))
    return (
        '<section class="p3-deal-unfold fp-legal-page" id="legal-%s" hidden aria-label="%s" style="--tone:%s">'
        '<p class="letter-steplabel">NayaNET &middot; The Whole Deal</p>'
        '<h2 class="deal-title">%s</h2><p class="deck-sub">%s</p>'
        '<div class="letter-controls"><div class="letter-dots" aria-hidden="true">%s</div>'
        '<button class="letter-all" type="button" data-legal-all>or read the whole page at once</button></div>'
        '<div class="fp-legal-body">%s</div>'
        '<div class="letter-controls"><button class="naya-btn naya-btn--primary naya-btn--sm legal-next-btn" type="button" data-legal-next>Keep reading &#9670;</button>'
        '<button class="naya-btn naya-btn--secondary naya-btn--sm legal-close-btn" type="button" data-legal-close>Close &#9670; Back to the footer</button></div>'
        '</section>' % (key, esc(aria), tone_hex, esc(title), esc(sub), dots, "".join(arts)))


acc = parse_legal_md(LEGAL_DIR + "/11-accessibility.md")
dis = parse_legal_md(LEGAL_DIR + "/12-disclaimer.md")
print("accessibility boards:", len(acc), [t for t, _ in acc])
print("disclaimer boards:", len(dis), [t for t, _ in dis])
assert len(acc) == 7, len(acc)
assert len(dis) == 8, len(dis)
acc_kinds = ["FOR EVERYONE", "THE STANDARD", "IN PLAIN WORDS", "WHAT WE HAVE DONE",
             "STILL DOING", "TELL US", "FITS TOGETHER"]
dis_kinds = ["WHAT IT IS", "WHAT IT IS NOT", "AN AI, NOT A HUMAN", "NOT AN ADVISER",
             "YOUR JUDGMENT", "CAN BE WRONG", "PROTECTS ITSELF", "NO PROMISE"]
acc_page = legal_page("accessibility", "Accessibility Statement", "Accessibility Statement",
                      "Built for everyone — in plain words.", "sapphire", "#3fb8ff", acc, acc_kinds)
dis_page = legal_page("disclaimer", "Disclaimer", "Disclaimer",
                      "What NayaNET is, and what it is not — in plain words.", "emerald", "#2fe89e", dis, dis_kinds)
# insert after the young page's closing </section>
i = text.find('id="legal-young"')
j = text.find("</section>", i)
assert i > 0 and j > i
text = text[:j + len("</section>")] + acc_page + dis_page + text[j + len("</section>"):]
# footer buttons
old = '<button class="fp-legal-link" type="button" data-legal-open="young">Young Citizens</button>'
new = (old + '<button class="fp-legal-link" type="button" data-legal-open="accessibility">Accessibility Statement</button>'
       '<button class="fp-legal-link" type="button" data-legal-open="disclaimer">Disclaimer</button>')
text = replace_once(text, old, new, "footer-buttons-12")
print("items14/27: 12/12 legal pages + buttons")

# ---------------------------------------------------------------- A6 final-board row
soul = open(SOUL, encoding="utf-8").read()
vow_m = re.search(r"## THE ULTIMATE ME — THE VOW.*?\n\n(.*?)\n\n## THE DECLARATION", soul, re.S)
assert vow_m, "vow section"
vow_text = md_plain(vow_m.group(1))
man = open(MANIFESTO, encoding="utf-8").read()
oath_m = re.search(r"## V\. The Declaration(.*?)$", man, re.S)
assert oath_m, "manifesto V"
oath_text = md_plain(oath_m.group(1))
proto = open(PROTOCOL, encoding="utf-8").read()
const_text = md_plain(proto)
laws_m = re.search(r"## 1\. THE PROTOCOL(.*?)## 3\. THE MACHINE", proto, re.S)
assert laws_m, "protocol 1-2"
laws_text = md_plain("## 1. THE PROTOCOL" + laws_m.group(1))
deal_text = beat_text("THE DEAL") + "\n\n" + beat_text("WHAT YOU GET")
promise_text = beat_text("JOINING IS FREE") + "\n\n" + beat_text("THE ONE LAW")
rules_text = beat_text("THE RULE") + "\n\n" + beat_text("THE EXCEPTION")
gov_text = beat_text("THE MOTHER BEE") + "\n\n" + beat_text("THE LAW")
FINAL = {
    "vow": {"t": "Our Vow", "body": vow_text},
    "deal": {"t": "The Deal", "body": deal_text},
    "promise": {"t": "Our Promise", "body": promise_text},
    "governance": {"t": "The Governance", "body": gov_text},
    "constitution": {"t": "Our Constitution", "body": const_text},
    "laws": {"t": "Our Laws", "body": laws_text},
    "rules": {"t": "Our Rules", "body": rules_text},
    "oath": {"t": "Our Oath", "body": oath_text},
}
for k, v in FINAL.items():
    assert len(v["body"]) > 40, (k, len(v["body"]))
    print("final-row", k, len(v["body"]), "chars")

final_css = """
/* WHOLE-SYSTEM CONNECTION 2026-11-24 (item 53) — the final-board link row:
   The Invitation, eight links, each opening its answer in a frame. */
.fp-final-row{margin:18px auto 0;text-align:center;max-width:860px}
.fp-final-invite{font-family:Marcellus,Georgia,serif;font-size:25px;color:#fff;margin:0 0 10px}
.fp-final-links{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 14px}
.fp-final-link{background:none;border:0;color:#fff;font:inherit;font-size:17px;font-weight:700;text-decoration:underline;text-underline-offset:3px;cursor:pointer;padding:6px 4px}
.fp-final-reader{position:fixed;inset:0;z-index:9998;display:flex;align-items:center;justify-content:center;background:rgba(2,3,10,.88);padding:20px;box-sizing:border-box}
.fp-final-reader[hidden]{display:none}
.fp-final-frame{max-width:680px;max-height:86vh;overflow:auto;background:#050507;border:1.5px solid rgba(142,36,170,.6);border-radius:20px;padding:24px 26px;box-shadow:0 8px 24px rgba(0,0,0,.6),0 0 18px rgba(142,36,170,.25);color:#fff;text-align:left}
.fp-final-frame h2{font-family:Marcellus,Georgia,serif;font-size:25px;margin:0 0 12px;text-align:center}
.fp-final-frame .fp-final-body{white-space:pre-wrap;font-size:17px;line-height:1.6}
.fp-final-close{display:block;margin:18px auto 0;background:#050507;color:#fff;border:1.5px solid rgba(255,255,255,.5);border-radius:999px;padding:10px 22px;font:inherit;font-size:17px;cursor:pointer}
@media(max-width:640px){.fp-final-invite{font-size:25px}.fp-final-link{font-size:17px}}"""
text = text.replace("</style>", final_css + "\n</style>", 1)
reader_html = """
<div class="fp-final-reader" id="fpFinalReader" hidden>
  <div class="fp-final-frame">
    <h2 id="fpFinalTitle"></h2>
    <div class="fp-final-body" id="fpFinalBody"></div>
    <button class="fp-final-close" id="fpFinalClose" type="button">Close &#9670;</button>
  </div>
</div>"""
assert text.count("</body>") == 1
text = text.replace("</body>", reader_html + "\n</body>", 1)
# row injection in renderSlide + reader wiring at script end
old = "document.getElementById('slideBoards').innerHTML = boardsFor(s);"
new = (old + "\n  /* WHOLE-SYSTEM CONNECTION 2026-11-24 (item 53): on the last board,\n"
       "     the link row — The Invitation — each link opens its answer. */\n"
       "  var _oldRow = document.getElementById('fpFinalRow');\n"
       "  if (_oldRow) _oldRow.remove();\n"
       "  if (current === TOTAL - 1){\n"
       "    var _row = document.createElement('div');\n"
       "    _row.id = 'fpFinalRow'; _row.className = 'fp-final-row';\n"
       "    _row.innerHTML = '<p class=\"fp-final-invite\">The Invitation</p>' +\n"
       "      '<nav class=\"fp-final-links\">' +\n"
       "      '<button class=\"fp-final-link\" type=\"button\" data-final=\"vow\">Our Vow</button>' +\n"
       "      '<button class=\"fp-final-link\" type=\"button\" data-final=\"deal\">The Deal</button>' +\n"
       "      '<button class=\"fp-final-link\" type=\"button\" data-final=\"promise\">Our Promise</button>' +\n"
       "      '<button class=\"fp-final-link\" type=\"button\" data-final=\"governance\">The Governance</button>' +\n"
       "      '<button class=\"fp-final-link\" type=\"button\" data-final=\"constitution\">Our Constitution</button>' +\n"
       "      '<button class=\"fp-final-link\" type=\"button\" data-final=\"laws\">Our Laws</button>' +\n"
       "      '<button class=\"fp-final-link\" type=\"button\" data-final=\"rules\">Our Rules</button>' +\n"
       "      '<button class=\"fp-final-link\" type=\"button\" data-final=\"oath\">Our Oath</button></nav>';\n"
       "    document.getElementById('slideBoards').appendChild(_row);\n"
       "    _row.querySelectorAll('[data-final]').forEach(function(b){\n"
       "      b.addEventListener('click', function(){ openFinal(b.getAttribute('data-final')); });\n"
       "    });\n"
       "  }")
text = replace_once(text, old, new, "item53-row-inject")
print("item53: final-board link row + reader")

# ---------------------------------------------------------------- A7 item 46 (legal Next locks at viewport top)
old = "beats[idx].scrollIntoView({behavior:'smooth', block:'nearest'});"
assert text.count(old) == 1, "legal next scroll anchor"
text = text.replace(old, "beats[idx].scrollIntoView({behavior:'smooth', block:'start'});", 1)
print("item46: legal Next locks the board at the viewport top")

# ---------------------------------------------------------------- init block (choice wiring + reader + deep links)
init_js = """
/* WHOLE-SYSTEM CONNECTION 2026-11-24 (items 10/53) — choice wiring + the
   final-board reader. Deep links: ?view=deck starts the visual story,
   ?view=letter opens the letter. Closing a legal page returns to the view
   it came from (lastScreen), so the choice is the bridge. */
(function(){
  function startDeck(){ current = 0; renderSlide(); show('slide'); }
  var deckBtn = document.getElementById('fpChoiceDeck');
  var letterBtn = document.getElementById('fpChoiceLetter');
  var playBtn = document.getElementById('fpChoicePlay');
  if (deckBtn) deckBtn.addEventListener('click', startDeck);
  if (playBtn) playBtn.addEventListener('click', startDeck);
  if (letterBtn) letterBtn.addEventListener('click', function(){ openLegal('terms'); });
  var q = new URLSearchParams(window.location.search);
  if (q.get('view') === 'deck'){ startDeck(); }
  else if (q.get('view') === 'letter'){ openLegal('terms'); }
})();
var FP_FINAL = """ + json.dumps(FINAL) + """;
function openFinal(key){
  var e = FP_FINAL[key]; if (!e) return;
  document.getElementById('fpFinalTitle').textContent = e.t;
  document.getElementById('fpFinalBody').textContent = e.body;
  document.getElementById('fpFinalReader').hidden = false;
}
document.getElementById('fpFinalClose').addEventListener('click', function(){
  document.getElementById('fpFinalReader').hidden = true;
});
"""
assert text.count("</script>") >= 1
# append at the end of the LAST script block (the main script)
last = text.rfind("</script>")
text = text[:last] + init_js + text[last:]
print("init block appended")

# ---------------------------------------------------------------- verify
# slide 11 byte-identical (item 3 / U1)
m = re.search(r"var SLIDES = \[(.*?)\];", text, re.S)
slides = re.findall(r'\{t:"(.*?)"\s*,\s*x:"(.*?)"\s*,\s*a:"(.*?)"\}', m.group(1), re.S)
assert len(slides) == 27, len(slides)
assert hashlib.sha256(slides[10][1].encode()).hexdigest().startswith("33b0590cfb9f811a"), "slide 11 changed!"
# item 74: boards untouched
assert len(re.findall(r"\.intel-board", text)) == intel_board_rules_before, "intel-board CSS changed"
# item 7: analyser wired
assert "createMediaElementSource(audio)" in text and "analyser.getByteFrequencyData(freqData)" in text
# item 55: old-way bar present, untouched
assert "function logoSlot()" in text and 'id="tbTitle"' in text and "portraitSlot(PORTRAITS[0], 0)" in text
# item 47b: legal row wraps
assert "flex-wrap:wrap" in text and "fp-legal-links{display:flex;flex-wrap:wrap" in text
# counts
print("choice screen:", text.count('id="screen-choice"'), "| cover active:", text.count('screen active" id="screen-cover"'))
print("legal pages:", text.count("fp-legal-page"), "| footer buttons:", text.count("data-legal-open"))
print("final row keys:", text.count("data-final="), "| reader:", text.count('id="fpFinalReader"'))
print("goToPortal in-place:", "window.location.href = 'https://nayanet.app/?from=agreement#userName'" in text,
      "| new-tab gone:", "a.target = '_blank'" not in text)
print("PORTRAITS[0]:", text.count("PORTRAITS = ['NAYA_POWER.jpg'"))
open(OUT, "w", encoding="utf-8").write(text)
print("written:", OUT, len(text.encode("utf-8")), "sha:", hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])
scripts = re.findall(r"<script>(.*?)</script>", text, re.S)
print("script blocks:", len(scripts))
for i, sc in enumerate(scripts):
    open(f"/tmp/wsc-ag-{i}.js", "w").write(sc)
