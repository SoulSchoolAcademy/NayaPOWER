#!/usr/bin/env python3
"""THE INTERFACE FACTORY — spec in, elite interface out, in minutes.

A smart factory of smart apps: an assembler that takes a short interface spec
and produces a complete, triple-A, gate-verified interface composed VERBATIM
from the blessed parts in PARTS-MATRIX.md. The factory NEVER invents chrome —
every element traces to the parts matrix (the machine form of Law 14 and the
franchise law: the pieces ARE the brand).

Pipeline: spec -> assemble -> node --check wiring -> design gate -> output.
Gate failure = the factory does not emit. No exceptions.

Format step (Phase 2, 2026-11-17): every build also emits the two canonical
official formats (formats/official-unfold.html + formats/official-slideshow.html)
verbatim into the output dir — the Recipe's outputs, harvested from the
official-formats round, verified by size + sha256 before they are written.
See FORMATS below and formats/FORMATS.md.

Usage:
    python3 factory.py specs/smart-links-stats.json
    python3 factory.py specs/smart-links-stats.json --out out/custom.html --no-gate

Spec shape:
    {"name","title","subtitle","purpose","parts":[...],"data":{...},"wiring":"..."}

Part entries: "dashboard-door" | "briefing-strip" | "chart-taxonomy"
           | {"registry": "NAYA-BTN-009", "slots": {...}}
           | {"part": "chart-taxonomy", "slots": {...}}
"""
import hashlib
import html as htmlmod
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY_PATH = os.path.join(HERE, "parts-registry-v1.json")
GATE_PATH = os.path.expanduser("~/workspace/team-nitro/design-gate/design-gate.py")

# ----------------------------------------------------------------------------
# SHELL — doctrine baseplate (DESIGN-LANGUAGE §1.5 field, §4.1 tokens, §5.1
# button DNA, §6 type). This is the Lego baseplate, not a part.
# ----------------------------------------------------------------------------
SHELL_CSS = r"""
:root{
  --bg:#0B0D12; --bg-panel:#12151D; --bg-card:#171B25; --edge:#252B39;
  --purple:#a06bff; --blue:#3fb8ff; --green:#2fe89e; --gold:#ffbf3d;
  --orange:#ff9a5a; --red:#ff5e6c; --magenta:#e84fff;
  --ink:#F5F7FB; --dim:#a7a7b3; --faint:#8a8a96;
  --depth-hi:inset 0 1px rgba(255,255,255,.4);
  --depth-drop:0 18px 42px rgba(0,0,0,.73);
  --dur-fast:.18s; --dur-med:.28s; --dur-slow:.5s;
  --ease:cubic-bezier(.16,.84,.22,1);
  --font:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:#020204;color:var(--ink);font-family:var(--font);
  font-size:16px;line-height:1.6;min-height:100vh}
.fx-wrap{width:100%;padding:0 20px 80px;max-width:none}
@media(max-width:640px){.fx-wrap{padding:0 12px 64px}}
h1,h2,h3{font-family:Newsreader,Georgia,serif}
/* ---- the one button DNA (DESIGN-LANGUAGE §5.1): black center, white text,
   white rim at rest, own-color edge ignition, text stays white ---- */
button{font-family:inherit;appearance:none;cursor:pointer;border-radius:999px;
  padding:10px 20px;font-size:13.5px;font-weight:800;color:#fff;
  background:linear-gradient(180deg,#16161e,#0a0a10);
  border:1.5px solid rgba(255,255,255,.28);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.35),inset 0 -3px 8px rgba(0,0,0,.5),0 6px 16px rgba(0,0,0,.5);
  transition:border-color var(--dur-med) var(--ease),box-shadow var(--dur-med) var(--ease),transform var(--dur-med) var(--ease)}
button:hover{border-color:var(--pc,#a06bff);color:#fff;transform:translateY(-2px);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 0 14px var(--pc,#a06bff),0 0 34px -6px var(--pc,#a06bff)}
button:active{transform:translateY(1px)}
button:disabled{opacity:.45;cursor:not-allowed;transform:none}
button:focus-visible{outline:2px solid #fff;outline-offset:2px}
a{color:var(--green)}
/* ---- dashboard door: every page carries a Dashboard button (his law) ---- */
.fx-topbar{display:flex;align-items:center;gap:14px;padding:18px 0 6px}
.fx-brand{display:flex;align-items:center;gap:12px;flex:1 1 auto;min-width:0}
.fx-orb{flex:none;width:40px;height:40px;border-radius:50%;
  background:radial-gradient(circle at 35% 30%,#f0a6ff,#a06bff 55%,#241243);
  box-shadow:0 0 18px rgba(168,107,255,.85),inset 0 2px 6px rgba(255,255,255,.35)}
.fx-brand h1{margin:0;font-size:22px;font-weight:800;color:#fff;letter-spacing:.01em}
.fx-brand p{margin:2px 0 0;font-size:12.5px;color:var(--dim)}
.fx-dash{flex:none;text-decoration:none;display:inline-flex;align-items:center;
  padding:10px 22px;border-radius:999px;font-size:13.5px;font-weight:800;color:#fff;
  --pc:#a06bff;background:linear-gradient(180deg,#16161e,#0a0a10);
  border:1.5px solid rgba(255,255,255,.28);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.35),inset 0 -3px 8px rgba(0,0,0,.5),0 6px 16px rgba(0,0,0,.5);
  transition:border-color var(--dur-med) var(--ease),box-shadow var(--dur-med) var(--ease),transform var(--dur-med) var(--ease)}
.fx-dash:hover{border-color:var(--pc);color:#fff;transform:translateY(-2px);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 0 14px var(--pc),0 0 34px -6px var(--pc)}
/* ---- factory proof note cards (wiring output, labeled) ---- */
.fx-note{margin:12px 2px 0;background:linear-gradient(180deg,#101016,#0a0a10);
  border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:14px 16px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.08),0 10px 24px rgba(0,0,0,.45);
  font-size:14px;color:#fff}
.fx-note .fx-note-k{font-size:10.5px;font-weight:800;letter-spacing:.16em;
  text-transform:uppercase;color:var(--green);text-shadow:0 0 10px var(--green)}
.fx-note.smart .fx-note-k{color:var(--magenta);text-shadow:0 0 10px var(--magenta)}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

DOOR_HTML = """<header class="fx-topbar">
  <div class="fx-brand"><span class="fx-orb" aria-hidden="true"></span>
    <div><h1>{{title}}</h1><p>{{subtitle}}</p></div></div>
  <a class="fx-dash" href="https://nayanet.live/dashboard">Dashboard</a>
</header>"""

# ----------------------------------------------------------------------------
# SHELF — every part's harvest address. The factory pulls bytes verbatim.
# ----------------------------------------------------------------------------
DASH = os.path.expanduser("~/workspace/ninaya/purpose")
SHELF = {
    "dashboard-door": {"kind": "doctrine"},
    "briefing-strip": {
        "kind": "harvest",
        "file": os.path.join(DASH, "living-intel-block.html"),
        "html": ('<section class="tn-li"', "</section>"),
        "css": ("<style>", "</style>"),
        "script": None,  # engine is dashboard-coupled; factory wiring binds it
    },
    "chart-taxonomy": {
        "kind": "harvest",
        "file": os.path.join(DASH, "page.html"),
        "html": ('<section class="tn-rooms-sec" data-tn-rooms="trend"', "</section>"),
        "css": [
            ("[data-tn-rooms]{",
             "/* ---------- the grid that cannot overlap ---------- */"),
            ("/* ---------- pills ---------- */",
             "/* ===== CHART CONTROLS 2026-10-31"),
            ("/* ===== CHART CONTROLS 2026-10-31",
             "/* CHART ENGINE 2026-10-31"),
        ],
        "script": None,
    },
    "ph-msg": {
        "kind": "harvest-css",
        "file": os.path.expanduser("~/workspace/factory-models/src/os-style.html"),
        "css": [(".ph-msg{",
                 "/* the next-best-moves action buttons were",
                 False)],
    },
}


# ----------------------------------------------------------------------------
# FORMATS — the two official formats (Naya Code §9), harvested verbatim.
# The Recipe's outputs. The builder stores the canonical bytes in formats/
# and emits them byte-identical on every test build. NEVER re-typed, never
# edited here: a new canonical version arrives as a new filed file + new
# hashes below, from its own round — never by editing the stored bytes.
# Source: the official-formats round, branch
#   personal/official-formats-bridge-20261116, fix commits 84bd32c9 (unfold)
#   and a456d270 (slideshow), filed at
#   TEAM-NITRO/official-formats-bridge-20261116/official-unfold.html and
#   TEAM-NITRO/official-formats-bridge-20261116/official-slideshow.html.
#   Harvested from the Studio's canonical code (wireDeck / showSlide,
#   Studio blob a7114308); re-checker PASS on all items.
# Auto-format lives INSIDE these bytes (both presentations read the same
# beat node list); the builder never splits them and never re-implements
# them — emitting them verbatim preserves the auto-format.
# Format assignment: unfold -> About, slideshow -> Skills, one format per
# bridge (the entrance bridge still uses both for the agreement/legal pages).
# ----------------------------------------------------------------------------
FORMATS_DIR = os.path.join(HERE, "formats")
FORMATS = {
    "unfold": {
        "file": "official-unfold.html",
        "blob": "34c756fff6286c46a2ff61fa6224bc49e35d5abf",
        "bytes": 32079,
        "sha256": "70abc8e96712393d0b3f087b8410379fc39970a5905d06de1884afdf2d7b346c",
    },
    "slideshow": {
        "file": "official-slideshow.html",
        "blob": "21d08a88e0f2e63d3c30d8f5112a2479ecf52d59",
        "bytes": 34896,
        "sha256": "fcfa0c4c9794b8a92a3dea5ba2e4a1802376b2c75b2ba291fa8791b1da30693f",
    },
}


def load_format_bytes(name):
    """Read one canonical format's stored bytes, verifying size + sha256.

    A mismatch is a hard stop: the stored asset is not canonical, and the
    build must fail here — before the gate, before anything ships."""
    meta = FORMATS[name]
    path = os.path.join(FORMATS_DIR, meta["file"])
    with open(path, "rb") as f:
        data = f.read()
    if len(data) != meta["bytes"]:
        raise RuntimeError(
            f"format {name}: stored {len(data)} bytes, canonical is {meta['bytes']}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != meta["sha256"]:
        raise RuntimeError(
            f"format {name}: sha256 {digest}, canonical is {meta['sha256']}")
    return data


def emit_formats(out_dir, receipt):
    """The builder's format step: emit both canonical formats verbatim
    into the build output dir. Returns {name: {path, bytes, sha256, blob}}."""
    emitted = {}
    for name in ("unfold", "slideshow"):
        data = load_format_bytes(name)
        dest = os.path.join(out_dir, FORMATS[name]["file"])
        with open(dest, "wb") as f:
            f.write(data)
        emitted[name] = {
            "path": dest,
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "blob": FORMATS[name]["blob"],
        }
        receipt.setdefault("formats", {})[name] = emitted[name]
    return emitted


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()[:16]


def extract(path, start_marker, end_marker, include_end=True):
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    i = text.find(start_marker)
    if i < 0:
        raise RuntimeError(f"harvest start marker not found: {start_marker!r} in {path}")
    j = text.find(end_marker, i)
    if j < 0:
        raise RuntimeError(f"harvest end marker not found: {end_marker!r} in {path}")
    chunk = text[i:j + (len(end_marker) if include_end else 0)]
    return chunk, sha(chunk.encode())


def load_registry():
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        return json.load(f)


def registry_part(reg, pid):
    for part in reg["interface_parts"]:
        if part.get("model") == pid:
            return part
    for part in reg.get("functional_parts", []):
        if part.get("id") == pid:
            return part
    raise RuntimeError(f"registry part not found: {pid}")


def fill_slots(text, slots):
    for k, v in (slots or {}).items():
        text = text.replace("{{" + k + "}}",
                            htmlmod.escape(str(v), quote=True))
    return text


def assemble(spec, receipt):
    """Returns (html, css_notes). Records every harvested hash in receipt."""
    reg = load_registry()
    css_parts = [("shell", SHELL_CSS, "doctrine")]
    body_parts = []
    reg_parts = []

    # ph-msg CSS rides with any part that uses it (briefing strip does)
    need_phmsg = False

    for entry in spec["parts"]:
        if isinstance(entry, str):
            key, slots = entry, {}
        else:
            key = entry.get("part") or entry.get("registry")
            slots = entry.get("slots", {})

        if isinstance(entry, dict) and "registry" in entry:
            part = registry_part(reg, entry["registry"])
            chunk = part["html"]
            receipt["parts"].append({
                "id": entry["registry"], "name": part.get("name"),
                "source": "PARTS-REGISTRY-V1.json", "sha": sha(chunk.encode()),
            })
            reg_parts.append(fill_slots(chunk, slots))
            continue

        if key == "dashboard-door":
            receipt["parts"].append({"id": "dashboard-door",
                                    "source": "doctrine shell", "sha": "doctrine"})
            body_parts.append(fill_slots(DOOR_HTML, {
                "title": spec.get("title", spec["name"]),
                "subtitle": spec.get("subtitle", ""),
            }))
            continue

        shelf = SHELF.get(key)
        if not shelf:
            raise RuntimeError(f"unknown part: {key!r} — not on the shelf")

        if shelf["kind"] == "harvest":
            s, e = shelf["html"]
            chunk, h = extract(shelf["file"], s, e)
            receipt["parts"].append({"id": key, "source": shelf["file"],
                                    "markers": [s[:48], e[:24]], "sha": h})
            body_parts.append(fill_slots(chunk, slots))
            css_spec = shelf["css"]
            if isinstance(css_spec, tuple):
                css_spec = [css_spec]
            for cs, ce in css_spec:
                cchunk, ch = extract(shelf["file"], cs, ce)
                css_parts.append((key, cchunk, ch))
                receipt["css"].append({"for": key, "sha": ch,
                                      "chars": len(cchunk)})
            if key == "briefing-strip":
                need_phmsg = True
        elif shelf["kind"] == "harvest-css":
            for spec3 in shelf["css"]:
                cs, ce = spec3[0], spec3[1]
                inc = spec3[2] if len(spec3) > 2 else True
                cchunk, ch = extract(shelf["file"], cs, ce, inc)
                css_parts.append((key, cchunk, ch))
                receipt["css"].append({"for": key, "sha": ch,
                                      "chars": len(cchunk)})

    if need_phmsg:
        shelf = SHELF["ph-msg"]
        for spec3 in shelf["css"]:
            cs, ce = spec3[0], spec3[1]
            inc = spec3[2] if len(spec3) > 2 else True
            cchunk, ch = extract(shelf["file"], cs, ce, inc)
            css_parts.append(("ph-msg", cchunk, ch))
            receipt["css"].append({"for": "ph-msg", "sha": ch,
                                  "chars": len(cchunk)})

    # strip raw <style> wrappers from harvested css (we re-wrap once)
    css_body = []
    for pid, chunk, _h in css_parts:
        if pid == "shell":
            css_body.append(chunk)
        else:
            c = chunk.strip()
            if c.startswith("<style>"):
                c = c[len("<style>"):]
            if c.endswith("</style>"):
                c = c[:-len("</style>")]
            css_body.append(f"\n/* ===== harvested: {pid} ===== */\n" + c)

    return css_body, body_parts, reg_parts


# ----------------------------------------------------------------------------
# WIRING — generated per-spec data binding. Marked, honest, minimal.
# ----------------------------------------------------------------------------
def wiring_smart_links(spec):
    data = spec["data"]
    payload = json.dumps({
        "clicks_daily": data["clicks_daily"],
        "day_names": data.get("day_names", []),
        "window_note": data.get("window_note", ""),
        "link_name": data.get("link_name", "your Smart Link"),
    })
    return r"""/* FACTORY WIRING — generated for this spec, not a part.
   Binds spec data to harvested parts. Honest fixture: the numbers below are
   the spec's data, stated in the page note. */
(function(){
"use strict";
var D=__PAYLOAD__;
var DAYC={6:"#6675ff",0:"#a06bff",1:"#ff9a5a",2:"#ffbf3d",3:"#5b8fc9",4:"#2e9e6a",5:"#ff5e6c"};
function $(s,r){return (r||document).querySelector(s)}
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;")}
function sum(a){return a.reduce(function(x,y){return x+y},0)}
var W2D={live:1,hour:1,"7":7,"30":30,all:30};
var curRange="7", curKind="clicks";
function sliceFor(r){
  var n=W2D[r]||7, d=D.clicks_daily.slice(-n);
  return {vals:d, names:D.day_names.slice(-n)};
}
function render(){
  var s=sliceFor(curRange), vals=s.vals, names=s.names;
  var board=$('[data-tn-trend]'); if(!board) return;
  var max=Math.max.apply(null,vals.concat([1]));
  var h='<div class="tn-rooms-bars" role="img" aria-label="Smart Link clicks per day">';
  for(var i=0;i<vals.length;i++){
    var dt=new Date(); dt.setDate(dt.getDate()-(vals.length-1-i));
    var c=DAYC[dt.getDay()];
    var pct=Math.max(3,Math.round(vals[i]/max*100));
    h+='<div class="tn-rooms-barcol"><div class="tn-rooms-barnum">'+vals[i]+'</div>'
      +'<div class="tn-rooms-bar" style="--bc:'+c+';height:'+pct+'%"></div></div>';
  }
  h+='</div><div class="tn-rooms-barlabels">'
    +names.map(function(n){return '<span>'+esc(n)+'</span>'}).join('')+'</div>'
    +'<div class="tn-rooms-maxy">peak '+max+'</div>';
  board.innerHTML=h;
  var tot=sum(vals), peak=vals.indexOf(max);
  var n1=$('[data-tn-n="clicks"]'); if(n1) n1.textContent=tot.toLocaleString();
  var line=$('[data-tn-li="line"]');
  if(line) line.innerHTML='Your strongest current is <b>Smart Link clicks</b> — '
    +'<b>'+tot.toLocaleString()+'</b> in the window. Peak day: <b>'+esc(names[peak]||"")+'</b>.';
  var note=$('[data-tn-trend-note]');
  if(note) note.textContent=D.window_note+' — every bar is a real day from the spec data.';
  var ins=$('[data-tn-li="insight-text"]'), iw=$('[data-tn-li="insight"]');
  if(ins&&iw&&vals.length>=7){
    var wk=sum(vals.slice(-7)), share=Math.round(max/Math.max(1,wk)*100);
    ins.textContent='Peak day carried '+share+'% of the last 7 days\u2019 clicks — that\u2019s the day to study.';
    iw.hidden=false;
  }
}
function wirePills(){
  var when=$('[data-tn-pills="range"]');
  if(when) when.addEventListener("click",function(e){
    var b=e.target.closest("button"); if(!b||b.disabled) return;
    when.querySelectorAll("button").forEach(function(x){x.classList.remove("on")});
    b.classList.add("on"); curRange=b.getAttribute("data-range")||"7"; render();
  });
  var what=$('[data-tn-pills="kind"]');
  if(what) what.addEventListener("click",function(e){
    var b=e.target.closest("button"); if(!b||b.disabled) return;
    var k=b.getAttribute("data-kind");
    var note=$('[data-tn-trend-note]');
    if(k!=="clicks"){ if(note) note.textContent='This proof wires Smart Link clicks only — '+b.textContent.trim()+' lands with its pipeline.'; return; }
    what.querySelectorAll("button").forEach(function(x){x.classList.remove("on")});
    b.classList.add("on"); render();
  });
  var ix=$('[data-tn-li="insight-x"]');
  if(ix) ix.addEventListener("click",function(){ $('[data-tn-li="insight"]').hidden=true; });
  var info=$('[data-tn-li="info"]'), det=$('[data-tn-li="detail"]');
  if(info&&det) info.addEventListener("click",function(){
    det.hidden=!det.hidden;
    if(!det.hidden) det.innerHTML='<b>What this reading is:</b> the spec\u2019s Smart Link click ledger, '
      +'summed per day and drawn as living bars. No invented numbers — the note under the chart states the window.';
  });
  var brief=$('[data-tn-li="brief"]'), acts=$('[data-tn-li="actions"]');
  if(brief&&acts) brief.addEventListener("click",function(){ acts.hidden=!acts.hidden; });
  var status=$('[data-tn-li="status"]');
  function say(m){ if(status) status.textContent=m; }
  function noteCard(kind){
    var line=$('[data-tn-li="line"]');
    var txt=line?line.textContent:'';
    var d=document.createElement("div");
    d.className='fx-note'+(kind==="smart"?" smart":"");
    d.innerHTML='<div class="fx-note-k">'+(kind==="smart"?"Smart note":"Note")+' · factory proof</div><p style="margin:8px 0 0">'+esc(txt)+'</p>';
    var sec=$('[data-tn-li="strip"]'); if(sec) sec.appendChild(d);
    say((kind==="smart"?"Smart note":"Note")+' placed on the page — proof fixture, not saved to a store.');
  }
  var an=$('[data-tn-li-act="note"]'); if(an) an.addEventListener("click",function(){noteCard("note")});
  var asn=$('[data-tn-li-act="smartnote"]'); if(asn) asn.addEventListener("click",function(){noteCard("smart")});
  var am=$('[data-tn-li-act="mail"]'); if(am) am.addEventListener("click",function(){
    var inp=$('[data-tn-li-mailto]'); var alias=inp&&inp.value.trim();
    say(alias?('Proof fixture — "'+alias+'" is not mailed. Connect Smart Mail to send for real.')
             :'Type an alias first — proof fixture, nothing is sent.');
  });
}
try{ render(); wirePills(); }catch(err){ /* honest: never break the page */ }
})();""".replace("__PAYLOAD__", payload)


WIRINGS = {"smart-links": wiring_smart_links}


def build_page(spec, css_body, body_parts, reg_parts, wiring_js):
    css = "\n".join(css_body)
    body = "\n".join(body_parts + reg_parts)
    title = htmlmod.escape(spec.get("title", spec["name"]))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — NayaNET factory proof</title>
<!-- INTERFACE FACTORY PROOF — spec: {htmlmod.escape(spec['name'])} -->
<!-- Assembled verbatim from blessed parts (PARTS-MATRIX.md). The pieces are the brand. -->
<style>{css}
</style>
</head>
<body>
<div class="fx-wrap">
{body}
</div>
<script>
{wiring_js}
</script>
</body>
</html>
"""


def run_gate(path):
    if not os.path.exists(GATE_PATH):
        return None, "gate not found"
    r = subprocess.run([sys.executable, GATE_PATH, "--file", path,
                        "--widths", "1440,390"],
                       capture_output=True, text=True, timeout=600)
    return r.returncode, r.stdout[-3000:] + r.stderr[-1000:]


def main():
    if len(sys.argv) < 2:
        print("usage: factory.py <spec.json> [--out path] [--no-gate]",
              file=sys.stderr)
        return 2
    spec_path = sys.argv[1]
    out = None
    no_gate = False
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--out" and i + 1 < len(args):
            out = args[i + 1]
            i += 2
        elif args[i] == "--no-gate":
            no_gate = True
            i += 1
        else:
            i += 1

    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    if out is None:
        out = os.path.join(HERE, "out", spec["name"] + ".html")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    receipt = {"spec": spec_path, "parts": [], "css": [],
               "spec_sha": sha(json.dumps(spec, sort_keys=True).encode())}

    css_body, body_parts, reg_parts = assemble(spec, receipt)

    wiring_name = spec.get("wiring")
    if wiring_name not in WIRINGS:
        print(f"unknown wiring: {wiring_name!r}", file=sys.stderr)
        return 2
    wiring_js = WIRINGS[wiring_name](spec)

    # wiring must be syntactically valid JS before it ships
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as tf:
        tf.write(wiring_js)
        tf_path = tf.name
    nc = subprocess.run(["node", "--check", tf_path],
                        capture_output=True, text=True)
    os.unlink(tf_path)
    if nc.returncode != 0:
        print("WIRING SYNTAX FAIL:\n" + nc.stderr, file=sys.stderr)
        return 1

    page = build_page(spec, css_body, body_parts, reg_parts, wiring_js)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    receipt["out"] = out
    receipt["bytes"] = len(page.encode())

    # FORMAT STEP (Phase 2): the Recipe's outputs — the canonical unfold +
    # slideshow, emitted verbatim into the same output dir. A bad stored
    # asset fails the build here, before the gate, before anything ships.
    emit_formats(os.path.dirname(out), receipt)
    for _name, _meta in receipt["formats"].items():
        print(f"format: {_name} -> {_meta['path']} "
              f"({_meta['bytes']} bytes, sha256 {_meta['sha256'][:16]}...)")

    if not no_gate:
        code, tail = run_gate(out)
        receipt["gate_exit"] = code
        if code != 0:
            os.unlink(out)
            print(f"GATE FAILED (exit {code}) — output deleted, nothing shipped.")
            print(tail)
            rp = out + ".receipt.json"
            json.dump(receipt, open(rp, "w"), indent=1)
            print(f"receipt: {rp}")
            return 1
        print("GATE PASSED — elite, shippable.")
    else:
        print("gate skipped (--no-gate).")

    rp = out + ".receipt.json"
    json.dump(receipt, open(rp, "w"), indent=1)
    print(f"built: {out} ({receipt['bytes']} bytes)")
    print(f"receipt: {rp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
