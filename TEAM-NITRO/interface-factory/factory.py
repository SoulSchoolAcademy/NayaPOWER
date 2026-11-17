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

Epic step (Epic fold-in, 2026-11-17): every build also emits the Intelligent
Block Epic engine (formats/epic-auto-format.html) verbatim into the output
dir — the paste-anything auto-format step, harvested from the Epic filing
(branch intelligent-block/epic-20261117, blob 4319256d), verified by size +
sha256 before it is written. See EPIC below and formats/EPIC.md. The
standalone Epic page is retired as a destination; its only surviving surface
is this engine, inside the Factory (and wherever pasting happens).

Survey step (Epic fold-in, 2026-11-17): the `epic-survey` wiring takes the
walk's ten questions, answered, and produces the citizen's page THROUGH the
Epic engine — the engine's own distiller (run in Node at build time by
epic-distill-harness.js, on the stored engine bytes) turns the answers into
About + Skills + Space boards, and the built page IS the engine page with
those boards added as deck beats, so the paste-anything studio stays live
in the page. See build_epic_survey_page() below.

Usage:
    python3 factory.py specs/formats-test.json --out out/formats-test.html
    python3 factory.py specs/formats-test.json --out out/formats-test.html --no-gate

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
# THE VAULT, SHARPENED (Phase 2 amendment, 2026-11-17): the emitted formats
# are vault assets — LABELED, INVENTORIED, ORGANIZED, ACTIVE. Each FORMATS
# entry carries a `label` (name + role) and a `vault` (where the asset lives:
# the builder's formats/ store = the Factory's vault shelf, filed on the
# factory branch = findable). emit_formats() copies both into the receipt,
# so every build's receipt inventories both assets. See formats/FORMATS.md
# ("The Vault") for the reader-facing inventory.
# ----------------------------------------------------------------------------
FORMATS_DIR = os.path.join(HERE, "formats")
FORMATS = {
    "unfold": {
        "file": "official-unfold.html",
        "blob": "34c756fff6286c46a2ff61fa6224bc49e35d5abf",
        "bytes": 32079,
        "sha256": "70abc8e96712393d0b3f087b8410379fc39970a5905d06de1884afdf2d7b346c",
        "label": "official-unfold — the canonical unfold, About's presentation",
        "vault": "TEAM-NITRO/interface-factory/formats/official-unfold.html — the Factory's vault shelf, filed on the factory branch",
    },
    "slideshow": {
        "file": "official-slideshow.html",
        "blob": "21d08a88e0f2e63d3c30d8f5112a2479ecf52d59",
        "bytes": 34896,
        "sha256": "fcfa0c4c9794b8a92a3dea5ba2e4a1802376b2c75b2ba291fa8791b1da30693f",
        "label": "official-slideshow — the canonical slideshow, Skills' presentation",
        "vault": "TEAM-NITRO/interface-factory/formats/official-slideshow.html — the Factory's vault shelf, filed on the factory branch",
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
    into the build output dir. Returns {name: {path, bytes, sha256, blob,
    label, vault}} — label + vault are the Vault Sharpening: every emitted
    format is a labeled, inventoried vault asset (see FORMATS above)."""
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
            "label": FORMATS[name]["label"],
            "vault": FORMATS[name]["vault"],
        }
        receipt.setdefault("formats", {})[name] = emitted[name]
    return emitted


# ----------------------------------------------------------------------------
# EPIC — the Intelligent Block Epic engine, the Factory's auto-format step.
# The standalone Epic page is retired as a destination; its only surviving
# surface is this engine, stored verbatim in formats/ and emitted verbatim
# on every build, exactly like the two official formats above. NEVER
# re-typed, never edited here: a new engine version arrives as a new filed
# file + new hashes below, from its own round — never by editing the stored
# bytes. Source: the Epic round, branch intelligent-block/epic-20261117,
# commit 3920de9f, PR #3390 (open, unmerged — its bytes are the harvest
# source; whether it merges or closes is Shawn's hand). Its eye PASSED
# 03:34Z 2026-11-17 (paste text/note/image all beautiful, numbers alive,
# self-check 10/10) — the engine works; this round moves its HOME, it does
# not rebuild it. The engine's known loose ends ride along, named in
# formats/EPIC.md, never silently fixed here: "15/15" buttons is 14 rendered
# + 1 template string; _osMiniNumHTML trimmed, not byte-verbatim;
# miniTileHTML re-indented; a wrapped continuation starting with a capital
# or digit splits (the stop-word guard is a follow-on, not this round).
# FIX ROUND 2026-11-17 (fold-in fix, PR #3395): the Factory's copy of the
# engine repairs titleFrom — the nutshell now ends at a phrase boundary,
# never mid-phrase (the eye failed 4 of 10 deck headlines on it). The
# stored engine is therefore NO LONGER byte-identical to the Epic source
# blob 4319256d; the hashes below are the FIXED engine. The Epic branch
# (PR #3390) was not touched — the engine's home is the Factory now, and
# the repair lives here, in the Factory's copy, nowhere else.
# ----------------------------------------------------------------------------
EPIC = {
    "file": "epic-auto-format.html",
    "blob": "3a4b0bf8b2e2f29fe5b956d5d6ca04e6f8c2baef",
    "bytes": 81357,
    "sha256": "158d5e58504e915655f7955ac6c506ce1a514c1d572bc693d0d8fc40f9dbd045",
    "label": "epic-auto-format — the Intelligent Block Epic engine, the Factory's auto-format step",
    "vault": "TEAM-NITRO/interface-factory/formats/epic-auto-format.html — the Factory's vault shelf, filed on the factory branch",
    "source_branch": "intelligent-block/epic-20261117",
    "source_commit": "3920de9f41dbd8bebb6b3faf442b99c92c39572c",
    "source_pr": 3390,
}
HARNESS_PATH = os.path.join(HERE, "epic-distill-harness.js")


def load_epic_bytes():
    """Read the stored Epic engine bytes, verifying size + sha256.

    A mismatch is a hard stop: the stored engine is not the filed engine,
    and the build must fail here — before the gate, before anything ships."""
    path = os.path.join(FORMATS_DIR, EPIC["file"])
    with open(path, "rb") as f:
        data = f.read()
    if len(data) != EPIC["bytes"]:
        raise RuntimeError(
            f"epic engine: stored {len(data)} bytes, filed is {EPIC['bytes']}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EPIC["sha256"]:
        raise RuntimeError(
            f"epic engine: sha256 {digest}, filed is {EPIC['sha256']}")
    return data


def emit_epic(out_dir, receipt):
    """The builder's auto-format step: emit the Epic engine verbatim into
    the build output dir, next to the two canonical formats. Returns
    {path, bytes, sha256, blob, label, vault} — the same Vault Sharpening
    as the formats: a labeled, inventoried vault asset, in every receipt."""
    data = load_epic_bytes()
    dest = os.path.join(out_dir, EPIC["file"])
    with open(dest, "wb") as f:
        f.write(data)
    meta = {
        "path": dest,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "blob": EPIC["blob"],
        "label": EPIC["label"],
        "vault": EPIC["vault"],
        "source_branch": EPIC["source_branch"],
        "source_commit": EPIC["source_commit"],
        "source_pr": EPIC["source_pr"],
    }
    receipt["epic"] = meta
    return meta


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


# ----------------------------------------------------------------------------
# EPIC SURVEY — the walk's ten questions, answered, produce the page
# THROUGH the Epic engine. The builder does not distill, does not format,
# does not write boards: the engine's own distill() + boardHTML() do, run
# in Node at build time by epic-distill-harness.js on the stored engine
# bytes (verified by load_epic_bytes() above). The built page IS the engine
# page — canonical style + epic style + the three engine beats + the
# canonical + epic scripts, byte-identical — with ONLY Factory insertions,
# in the engine page, with ONLY Factory insertions, each wrapped in a
# <!-- FACTORY EPIC FOLD-IN BEGIN x --> ... <!-- FACTORY EPIC FOLD-IN END x -->
# span (so the checker can strip every span and recover the engine bytes
# exactly), plus three exact reversals (hero text, dots, the results-empty
# note) that the verifier reverses by fixed strings:
#   1. a survey audit block (<script type="application/json">) in <head>;
#   2. the hero retitled to the citizen (steplabel / deal-title / deck-sub
#      / <title> — the page's content, not the engine);
#   3. the dots extended to the full deck (one per beat, spectrum flow);
#   4. a deck-next button on the studio beat (beat 3) so the unfold flows
#      on into the citizen's beats;
#   5. the citizen's beats — About (Q1/Q2/Q5/Q6), the vision+mission thread
#      (Q3/Q4), Skills (Q7/Q8/Q9 — the skill is what they do + what they
#      offer; the walk has no separate skill question), the Space (Q10) —
#      distilled by the engine, inserted after the studio beat;
#   6. the three paste proofs baked into #epicResultsBody (plain text ->
#      boards, smart note -> boards with seams stripped, image -> the board
#      itself), so the page SHOWS pastes coming out beautiful — the live
#      studio above them stays live for the citizen's own paste;
#   7. a Factory provenance board before </main>;
#   8. a FACTORY WIRING script before </body> that binds the baked
#      result boards' Keep-reading buttons (the engine's showResults wires
#      only boards it builds at runtime).
# The deck tones run the spectrum flow in order, never twice in a row:
# beats 1-3 keep the engine's purple/sapphire/green; the citizen's beats
# continue gold/orange/red/magenta/purple/sapphire/green. Verify (anyone,
# cold): strip every BEGIN/END span from the built page, reverse the three
# exact replacements (hero text, dots, results-empty note) by fixed
# strings, and the bytes must equal the stored engine file exactly —
# verify_foldin.py does this. A build whose insertions do not strip clean
# is a failed build.
# ----------------------------------------------------------------------------
SURVEY_GROUPS = [
    # (key, kind, mapping keys, tones in deck order)
    ("about", "ABOUT, FROM YOUR ANSWERS", ["q1", "q2", "q5", "q6"],
     ["#d4a017", "#c2410c", "#c62828"]),
    ("thread", "VISION & MISSION \u2014 THE THREAD", ["q3", "q4"],
     ["#a21caf"]),
    ("skills", "SKILLS, FROM YOUR ANSWERS", ["q7", "q8", "q9"],
     ["#8e24aa", "#0f52ba", "#07925f"]),
    ("space", "YOUR SPACE \u2014 AND ITS PEOPLE", ["q10"], ["#07925f"]),
]
DECK_TONES = ["#8e24aa", "#0f52ba", "#07925f", "#d4a017", "#c2410c",
              "#c62828", "#a21caf", "#8e24aa", "#0f52ba", "#07925f"]


def _hex_rgb(hexcode):
    n = int(hexcode.lstrip("#"), 16)
    return "%d,%d,%d" % ((n >> 16) & 255, (n >> 8) & 255, n & 255)


def _replace_once(text, anchor, replacement, what):
    if text.count(anchor) != 1:
        raise RuntimeError(
            f"epic-survey: anchor for {what} found {text.count(anchor)} "
            f"times in the engine (want exactly 1) — the engine changed")
    return text.replace(anchor, replacement)


def run_epic_harness(job):
    """Run the Epic engine's own distiller in Node on the stored engine
    bytes. Returns the harness JSON (groups + pastes + tiles). Any failure
    is a hard stop — the build never formats by itself."""
    if not os.path.exists(HARNESS_PATH):
        raise RuntimeError(f"epic-survey: harness missing: {HARNESS_PATH}")
    engine_path = os.path.join(FORMATS_DIR, EPIC["file"])
    proc = subprocess.run(
        ["node", HARNESS_PATH, engine_path],
        input=json.dumps(job), capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        raise RuntimeError(
            "epic-survey: harness failed:\n" + proc.stderr[-2000:])
    try:
        return json.loads(proc.stdout)
    except ValueError:
        raise RuntimeError(
            "epic-survey: harness printed no JSON:\n" + proc.stdout[-2000:])


def _deck_beat_html(board_html, beat_no, tone, is_last):
    """Turn one engine boardHTML board into a deck beat: hidden until the
    unfold reaches it, marked as Factory-built, carrying a deck-next button
    unless it is the last beat of the deck."""
    import re
    m = re.match(
        r'<article class="intel-board letter-beat epic-result" '
        r'style="--tone:([^"]+)"( hidden)?>', board_html)
    if not m:
        raise RuntimeError(
            "epic-survey: boardHTML output is not the expected article")
    head = ('<article class="intel-board letter-beat epic-result" '
            f'data-factory="epic-survey" data-beat="{beat_no}" '
            f'style="--tone:{m.group(1)}" hidden>')
    rest = board_html[m.end():]
    # The engine's button (epic-result-next) becomes the deck's own
    # Keep-reading button; a board without one still needs one unless it
    # is the last beat — the unfold must flow on.
    btn_pat = re.compile(
        r'<button class="p3-enter letter-next deck-next orbit-btn '
        r'epic-result-next" type="button" style="--oc:([^;]+);'
        r'--oc-rgb:([^"]+)"><span class="orbit-label">Keep reading '
        r'\u25c6</span></button>')
    bm = btn_pat.search(rest)
    if bm:
        rest = btn_pat.sub(
            '<button class="p3-enter letter-next deck-next orbit-btn" '
            f'type="button" data-beat="{beat_no}" '
            f'style="--oc:{bm.group(1)};--oc-rgb:{bm.group(2)}">'
            '<span class="orbit-label">Keep reading \u25c6</span></button>',
            rest, count=1)
    elif not is_last:
        btn = ('<button class="p3-enter letter-next deck-next orbit-btn" '
               f'type="button" data-beat="{beat_no}" '
               f'style="--oc:{tone};--oc-rgb:{_hex_rgb(tone)}">'
               '<span class="orbit-label">Keep reading \u25c6</span></button>')
        if not rest.endswith("</article>"):
            raise RuntimeError("epic-survey: board HTML has no </article>")
        rest = rest[:-len("</article>")] + btn + "</article>"
    return head + rest


def build_epic_survey_page(spec, receipt):
    """Build the citizen's page from the survey spec, through the engine.
    Returns the page HTML (str). Records everything in the receipt."""
    survey = spec["survey"]
    answers = survey["answers"]
    mapping = survey["mapping"]
    citizen = survey.get("citizen", spec.get("title", "you"))

    job = {"groups": []}
    for key, kind, keys, tones in SURVEY_GROUPS:
        job["groups"].append({
            "key": key, "kind": kind,
            "text": " ".join(answers[q] for q in keys),
            "tones": tones,
        })
    result = run_epic_harness(job)

    engine = load_epic_bytes().decode("utf-8")
    page = engine

    # 1. Survey audit block in <head>.
    audit = {
        "citizen": citizen, "alias": survey.get("alias", citizen),
        "questions": survey["questions"], "answers": answers,
        "mapping": mapping, "source": survey.get("source", ""),
        "engine": {"file": EPIC["file"], "blob": EPIC["blob"],
                   "bytes": EPIC["bytes"], "sha256": EPIC["sha256"],
                   "source_branch": EPIC["source_branch"],
                   "source_commit": EPIC["source_commit"],
                   "source_pr": EPIC["source_pr"]},
        "groups": {k: {"title": v["title"], "sentences": v["total"],
                       "boards": len(v["beats"])}
                   for k, v in result["groups"].items()},
        "pastes": {
            "text": {"sentences": result["pastes"]["text"]["total"],
                     "boards": len(result["pastes"]["text"]["beats"])},
            "note": {"sentences": result["pastes"]["note"]["total"],
                     "boards": len(result["pastes"]["note"]["beats"]),
                     "seams_stripped":
                         result["pastes"]["note"]["seamsStripped"]},
            "image": {"board": "epic-img-board, full-bleed cover"}},
        "tiles": result["tiles"]["counts"],
    }
    audit_json = json.dumps(audit, ensure_ascii=False, indent=1)
    if "</script>" in audit_json:
        raise RuntimeError("epic-survey: audit JSON contains </script>")
    audit_block = (
        "<!-- FACTORY EPIC FOLD-IN BEGIN survey-audit -->\n"
        '<script id="factory-survey" type="application/json">\n'
        + audit_json + "\n</script>\n"
        "<!-- FACTORY EPIC FOLD-IN END survey-audit -->\n")
    page = _replace_once(page, "</head>", audit_block + "</head>",
                         "audit block")

    # 2. Hero retitled to the citizen (the page's content, not the engine).
    page = _replace_once(
        page, "<title>The Intelligent Block \u2014 Epic | NayaNET</title>",
        f"<title>{htmlmod.escape(citizen)} \u2014 Your page, built by the "
        "survey | NayaNET</title>", "page title")
    page = _replace_once(
        page, "<p class=\"letter-steplabel\">NayaNET &middot; The "
        "Intelligent Block &middot; Epic</p>",
        "<p class=\"letter-steplabel\">NayaNET &middot; The Smart Factory "
        "&middot; Your page, built by the survey</p>", "steplabel")
    page = _replace_once(
        page, "<h2 class=\"deal-title\">The Intelligent Block, Epic</h2>",
        f"<h2 class=\"deal-title\">{htmlmod.escape(citizen)}</h2>",
        "deal title")
    page = _replace_once(
        page, "<p class=\"deck-sub\">The numbers are alive. The buttons "
        "are the best. Anything you paste comes out beautiful.</p>",
        "<p class=\"deck-sub\">"
        + htmlmod.escape(answers["q1"]) + "</p>", "deck subtitle")

    # 3. Dots extended to the full deck (spectrum flow, one per beat).
    baked_total = sum(len(v["beats"])
                      for v in result["groups"].values())
    deck_total = 3 + baked_total
    if len(DECK_TONES) != deck_total:
        raise RuntimeError(
            f"epic-survey: deck tones {len(DECK_TONES)} != deck beats "
            f"{deck_total} — the tones list must match the deck")
    dots_old = ('<div class="letter-dots" id="studioDots" '
                'aria-hidden="true"><span class="ldot on" '
                'style="--dc:#8e24aa"></span><span class="ldot" '
                'style="--dc:#0f52ba"></span><span class="ldot" '
                'style="--dc:#07925f"></span></div>')
    dots_new = ('<div class="letter-dots" id="studioDots" '
                'aria-hidden="true">'
                + "".join(
                    '<span class="ldot%s" style="--dc:%s"></span>'
                    % (" on" if i == 0 else "", tone)
                    for i, tone in enumerate(DECK_TONES))
                + "</div>")
    page = _replace_once(page, dots_old, dots_new, "dots")

    # 4 + 5. Studio beat gets a deck-next button; the citizen's beats
    # follow it in the deck (About, thread, Skills, Space — deck order).
    baked = []
    beat_no = 4
    for key, _kind, _keys, _tones in SURVEY_GROUPS:
        group = result["groups"][key]
        for i, beat in enumerate(group["beats"]):
            is_last = (key == SURVEY_GROUPS[-1][0]
                       and i == len(group["beats"]) - 1)
            baked.append(_deck_beat_html(beat["html"], beat_no,
                                         beat["tone"], is_last))
            beat_no += 1
    studio_btn = (
        "<!-- FACTORY EPIC FOLD-IN BEGIN studio-next -->\n"
        '<div class="epic-actions">'
        '<button class="p3-enter letter-next deck-next orbit-btn" '
        'type="button" data-beat="3" '
        'style="--oc:#07925f;--oc-rgb:7,146,95">'
        '<span class="orbit-label">Keep reading \u25c6</span></button>'
        "</div>\n"
        "<!-- FACTORY EPIC FOLD-IN END studio-next -->\n")
    anchor = ('</div>\n</article>\n</div>\n<div class="slides-nav" '
              'id="slidesNav" hidden>')
    replacement = (
        "</div>\n" + studio_btn + "</article>\n"
        "<!-- FACTORY EPIC FOLD-IN BEGIN citizen-beats -->\n"
        + "\n".join(baked)
        + "\n<!-- FACTORY EPIC FOLD-IN END citizen-beats -->\n"
        + "</div>\n"
        + '<div class="slides-nav" id="slidesNav" hidden>')
    page = _replace_once(page, anchor, replacement, "citizen beats")

    # 6. The three paste proofs baked into #epicResultsBody.
    results_html = (
        "<!-- FACTORY EPIC FOLD-IN BEGIN paste-proofs -->\n"
        "<!-- Pasted in the Factory, made beautiful by the Epic engine "
        "(plain text, a smart note, an image). The live studio above stays "
        "live for your own paste — pressing \u201cMake it beautiful\u201d "
        "replaces these with yours. -->\n"
        + "\n".join(b["html"] for b in result["pastes"]["text"]["beats"])
        + "\n"
        + "\n".join(b["html"] for b in result["pastes"]["note"]["beats"])
        + "\n" + result["pastes"]["image"]["boardHtml"]
        + "\n<!-- FACTORY EPIC FOLD-IN END paste-proofs -->\n")
    page = _replace_once(
        page, '<div id="epicResultsBody"></div>',
        '<div id="epicResultsBody">' + results_html + "</div>",
        "paste proofs")
    page = _replace_once(
        page, '<div class="epic-results-empty" id="epicResultsEmpty">',
        '<div class="epic-results-empty" id="epicResultsEmpty" hidden>',
        "results empty note")

    # 7. Factory provenance board before </main>.
    footer = (
        "<!-- FACTORY EPIC FOLD-IN BEGIN provenance -->\n"
        '<section class="intel-board" data-factory="epic-survey" '
        'style="--tone:#d4a017;margin-top:32px">'
        '<div class="ib-blocktop"><div class="face-mono" '
        'style="--tone:#d4a017">N</div><div class="ib-identity">'
        '<span class="ib-jewel" aria-hidden="true">\u25c6</span><div>'
        '<span class="ib-kind">BUILT BY THE SMART FACTORY</span>'
        '<h2 class="ib-title">The Epic engine formatted this page.</h2>'
        '<p class="ib-subtitle">Your ten answers became About, Skills and '
        'your Space — distilled by the Epic engine, inside the Factory.</p>'
        '</div></div></div><div class="ib-nutshell">'
        f'<p>{deck_total} boards in the deck — 3 from the engine, '
        f'{baked_total} from your answers. <span '
        'id="factory-provenance-pastes">3 pastes proved in the studio '
        'above: plain text, a smart note, an image — each came out '
        'beautiful.</span></p><p>Paste anything of your own in the studio above '
        'and press \u201cMake it beautiful\u201d — the same engine formats '
        'it, the same way.</p></div></section>\n'
        "<!-- FACTORY EPIC FOLD-IN END provenance -->\n")
    page = _replace_once(page, "</section>\n</main>",
                         "</section>\n" + footer + "</main>",
                         "provenance board")

    # 8. FACTORY WIRING: bind the baked result boards' Keep-reading
    # buttons (the engine's showResults wires only boards it builds).
    wiring = (
        "<!-- FACTORY EPIC FOLD-IN BEGIN factory-wiring -->\n"
        "<script>\n/* FACTORY WIRING — generated for this survey build, not "
        "a part and not engine code. Binds the Keep-reading buttons on the "
        "paste-proof boards the builder baked into #epicResultsBody, the "
        "way the engine's showResults binds the ones it builds at runtime. "
        "*/\n(function(){\n'use strict';\n"
        "var body=document.getElementById('epicResultsBody');\n"
        "if(!body) return;\n"
        "body.querySelectorAll('.epic-result-next').forEach(function(btn){\n"
        "  btn.addEventListener('click',function(){\n"
        "    var cur=btn.closest('.epic-result');\n"
        "    var next=cur&&cur.nextElementSibling;\n"
        "    if(next&&next.classList.contains('epic-result')){\n"
        "      next.hidden=false; next.classList.add('reveal');\n"
        "      btn.hidden=true;\n"
        "      next.scrollIntoView({behavior:'smooth',block:'nearest'});\n"
        "    }\n  });\n});\n"
        "/* FIX 2026-11-17 — the provenance board says what the studio\n"
        "   SHOWS, so when a visitor's own paste replaces the baked proofs\n"
        "   the line follows it: it counts the boards actually in the\n"
        "   results, and it never says \"below\" (the studio sits above the\n"
        "   board, not below it). The baked line stands until the first real\n"
        "   paste; every paste after that re-counts. */\n"
        "var prov=document.getElementById('factory-provenance-pastes');\n"
        "if(prov&&('MutationObserver' in window)){\n"
        "  new MutationObserver(function(){\n"
        "    var n=body.querySelectorAll('.epic-result, .epic-img-board').length;\n"
        "    prov.textContent='Your paste proved in the studio above — '+n+' board'\n"
        "      +(n===1?'':'s')+', the same engine, the same way.';\n"
        "  }).observe(body,{childList:true});\n"
        "}\n})();\n</script>\n"
        "<!-- FACTORY EPIC FOLD-IN END factory-wiring -->\n")
    page = _replace_once(page, "</script>\n</body>",
                         "</script>\n" + wiring + "</body>",
                         "factory wiring script")

    receipt["epic_survey"] = {
        "citizen": citizen,
        "deck_beats": deck_total,
        "engine_beats": 3,
        "citizen_beats": baked_total,
        "groups": {k: {"title": v["title"], "sentences": v["total"],
                       "boards": len(v["beats"])}
                   for k, v in result["groups"].items()},
        "pastes": audit["pastes"],
        "tiles": result["tiles"]["counts"],
        "dots": len(DECK_TONES),
    }
    return page


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

    wiring_name = spec.get("wiring")
    if wiring_name == "epic-survey":
        # The survey build does not assemble from parts: the page IS the
        # engine page, with the citizen's distilled beats added (see
        # build_epic_survey_page). The engine + formats still emit below.
        page = build_epic_survey_page(spec, receipt)
    else:
        css_body, body_parts, reg_parts = assemble(spec, receipt)

        if wiring_name not in WIRINGS:
            print(f"unknown wiring: {wiring_name!r}", file=sys.stderr)
            return 2
        wiring_js = WIRINGS[wiring_name](spec)

        # wiring must be syntactically valid JS before it ships
        with tempfile.NamedTemporaryFile("w", suffix=".js",
                                        delete=False) as tf:
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

    # EPIC STEP (Epic fold-in): the auto-format engine, emitted verbatim
    # into the same output dir on EVERY build. A bad stored engine fails
    # the build here, before the gate, before anything ships.
    epic_meta = emit_epic(os.path.dirname(out), receipt)
    print(f"epic: -> {epic_meta['path']} "
          f"({epic_meta['bytes']} bytes, sha256 {epic_meta['sha256'][:16]}...)")

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
