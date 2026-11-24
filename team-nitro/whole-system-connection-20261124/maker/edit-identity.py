#!/usr/bin/env python3
"""Whole-system connection round — IDENTITY build (maker v1).

Base: scratch/identity.html (live nayanet.app/identity.html, 307,759 B,
sha bdd8af83 — byte-identical to the workers.dev copy; the certificate
already lives on nayanet.app). Output: maker/identity.html.
I1 (item 69): the certificate handoff goes to the portal walk '/?walk=1',
never to /welcome (dead) and never to a workers.dev address.
I2 (item 70 + item-61 amendment): the already-claimed state is never a dead
end — a "This is me" button sets the device-local walk identity and opens
the portal walk; the message goes GREEN + bigger + unmissable, fits whole in
the viewport.
"""
import hashlib
import re

BASE = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/scratch/identity.html"
OUT = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/maker/identity.html"

text = open(BASE, encoding="utf-8", errors="ignore").read()
print("base:", len(text.encode("utf-8")))


def replace_once(s, old, new, name):
    assert s.count(old) == 1, f"{name}: anchor count {s.count(old)} != 1: {old[:90]!r}"
    return s.replace(old, new, 1)


# ---------------------------------------------------------------- I1 item 69
old = ("var WALKTHROUGH_URL = '/welcome';   /* the Official Welcome walk — "
       "identity hands off here, the walk hands off to the Hub */")
new = ("var WALKTHROUGH_URL = '/?walk=1';   /* WHOLE-SYSTEM CONNECTION "
       "2026-11-24 (item 69): the portal walk — identity hands off here, the "
       "walk hands off to the Hub. /welcome is dead; the certificate lives "
       "on nayanet.app, never a workers.dev address. */")
text = replace_once(text, old, new, "item69-walkthrough-url")
old = ("/* The walkthrough lives on this same origin (/welcome), so the Smart\n"
       "       Identity in localStorage carries over — the query handoff is belt\n"
       "       and suspenders for the walk's own ingest. */")
new = ("/* The walkthrough lives on the portal (/?walk=1) on this same origin,\n"
       "       so the Smart Identity in localStorage carries over — the query\n"
       "       handoff is belt and suspenders for the walk's own ingest. */")
text = replace_once(text, old, new, "item69-walkthrough-comment")
print("item69: handoff now /?walk=1")

# ---------------------------------------------------------------- I2 item 70
old = ("note.textContent = 'That alias is already claimed on another device. "
       "Pick a different alias to continue.';\n          note.hidden = false;\n          return;")
new = ("note.textContent = 'That alias is already claimed on another device. "
       "Pick a different alias to continue.';\n          note.hidden = false;\n"
       "          /* WHOLE-SYSTEM CONNECTION 2026-11-24 (item 70 + item-61\n"
       "             amendment): an existing member's own name must never\n"
       "             dead-end. The message goes GREEN + bigger + unmissable,\n"
       "             and This-is-me sets the device-local walk identity and\n"
       "             opens the portal walk. */\n"
       "          note.classList.add('fp-taken-green');\n"
       "          note.appendChild(document.createElement('br'));\n"
       "          var _tim = document.createElement('button');\n"
       "          _tim.id = 'fpThisIsMe'; _tim.type = 'button';\n"
       "          _tim.className = 'fp-this-is-me';\n"
       "          _tim.textContent = 'This is me \\u2014 it\\u2019s my name \\u2192';\n"
       "          _tim.addEventListener('click', function(){\n"
       "            var _nm = rawName || prettyName(finalAlias);\n"
       "            try { localStorage.setItem('nayanet_smart_name', _nm);\n"
       "                 localStorage.setItem('nayanet_smart_alias', finalAlias); } catch(e){}\n"
       "            window.location.href = '/?walk=1&name=' + encodeURIComponent(_nm)\n"
       "              + '&alias=' + encodeURIComponent(finalAlias);\n"
       "          });\n"
       "          note.appendChild(_tim);\n          return;")
text = replace_once(text, old, new, "item70-this-is-me")
css = """
<style>
/* WHOLE-SYSTEM CONNECTION 2026-11-24 (item 70 + item-61 amendment): the
   already-claimed message goes GREEN, bigger, unmissable, fits whole in the
   viewport; This-is-me is the way back in — never a dead end. */
#hubNote.fp-taken-green{color:#2fe89e !important;font-size:19px !important;font-weight:800;text-align:center}
.fp-this-is-me{display:inline-block;margin-top:10px;padding:12px 22px;border-radius:999px;border:1.5px solid rgba(47,232,158,.65);background:radial-gradient(circle at 50% 0%,#0b2e21,#05060a);color:#fff;font:inherit;font-size:17px;font-weight:800;cursor:pointer}
.fp-this-is-me:active{transform:translateY(1px) scale(.94);filter:brightness(.72)}
</style>"""
assert text.count("</head>") == 1
text = text.replace("</head>", css + "\n</head>", 1)
print("item70: This-is-me + green taken message added")

# ---------------------------------------------------------------- verify
assert "WALKTHROUGH_URL = '/?walk=1'" in text
assert "fpThisIsMe" in text and "fp-taken-green" in text
print("remaining '/welcome' mentions:", text.count("/welcome"))
for m in re.finditer(r"/welcome", text):
    print("  ", repr(text[max(0, m.start() - 60):m.start() + 20]))
open(OUT, "w", encoding="utf-8").write(text)
print("written:", OUT, len(text.encode("utf-8")), "sha:", hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])
scripts = re.findall(r"<script>(.*?)</script>", text, re.S)
print("script blocks:", len(scripts))
for i, sc in enumerate(scripts):
    open(f"/tmp/wsc-id-{i}.js", "w").write(sc)
