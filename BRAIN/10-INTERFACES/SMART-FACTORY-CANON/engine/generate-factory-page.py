#!/usr/bin/env python3
"""Generate the Smart Factory page FROM the canonical piece store.

Factory Contract-Home step 4. The page is REBUILT, never edited: the parts
shelf (step "Pick your pieces") is regenerated from the canon so it cannot
drift from it. Sources (the canonical set, MANIFEST.md):

  * pieces.json                 -- the working store: real markup + dual
                                   labels (name + ai_label{purpose,use_when,
                                   laws}) for every piece.
  * CANONICAL-PIECE-INDEX.json  -- the canon: a piece is canonical only when
                                   this index says so.
  * engine/factory-page-shell.html -- the current live page, harvested
                                   byte-for-byte (the Make It Yours build,
                                   nayanet.live/smartfactory). It is the
                                   DESIGN AUTHORITY: everything outside the
                                   parts shelf is carried over byte-identical;
                                   inside the shelf, every rail wrapper and
                                   card is composed from the page's own
                                   grammar (two card dialects, harvested --
                                   compose, don't create).
  * engine/factory-page-presentation.json -- the harvested presentation map:
                                   per-piece rail, order, spectrum color
                                   (--sc), one-line descriptor, dialect.
                                   Rebuilt by --harvest; the small `overrides`
                                   table covers canonical pieces the current
                                   page does not show (each entry names its
                                   reason). A canonical piece with NO
                                   presentation entry fails the build loud --
                                   a part lands whole (addition rule) or the
                                   page does not regenerate.

  * factory.css                 -- the store's own CSS. Pieces the current
                                   page never showed can carry classes only
                                   this file defines (the crowned Reference
                                   pieces and the app tiles do). The generator
                                   derives exactly those rules (file order,
                                   @media recursed, referenced @keyframes and
                                   shell-missing :root variables carried) and
                                   emits them as one marked <style> block --
                                   the pieces' own CSS, never invented, and
                                   by construction no rule in it can restyle
                                   anything the shell already defines.

  * NAYA-DESIGN-CONTRACT.machine.json -- the contract's machine twin
                                   (Factory Contract-Home step 6). The page
                                   gains a "Check against the contract"
                                   door: ONE contiguous generated region
                                   before </body> carrying the check
                                   parameters extracted from this twin by
                                   check_standard_features.design_params()
                                   (embedded verbatim as JSON) plus the
                                   in-page logic that consumes them. The
                                   build gate's checker and the door read
                                   the same parameter object -- rule values
                                   are defined once, in the twin, and reach
                                   both runtimes as data. Removing the door
                                   region restores the step-5 page byte
                                   for byte.

  * engine/templates-registry.json + engine/templates/ -- the ONE template
                                   registry and the real template bases
                                   (Factory Contract-Home step 5). The page
                                   carries the template grid twice; both
                                   grids are regenerated from the registry so
                                   the shelf cannot drift from it either. A
                                   card is generated only for a registry
                                   template whose base file exists -- the
                                   registry's own `missing` entries (today,
                                   smart-list: no base) get NO card, and a
                                   registry template whose base file vanishes
                                   fails the build loud. Card presentation
                                   (color, gem, brand, nut, detail) is
                                   harvested from the shell into the same
                                   presentation map (template_cards);
                                   registry templates the current page does
                                   not show carry a `template_overrides`
                                   entry with its reason, exactly like piece
                                   overrides. Each generated card is annotated
                                   in the step-4 data-attribute dialect:
                                   data-base names the registry base file and
                                   data-parts lists the canonical pieces the
                                   base's own bytes name (piece ids, slash
                                   rosters expanded) or embed verbatim --
                                   computed from the base at generation time,
                                   so the annotation grows as parts are
                                   harvested into a template, and a part that
                                   is not canonical in the store fails loud
                                   (no fabricated part lists).

The acceptance equations are enforced mechanically on every run:

  count(canonical in index) == count(canonical in store) ==
  count(piece cards in the generated page)

  count(templates in registry) == count(template bases on disk) ==
  count(template cards in EACH generated grid)

and every card carries its store piece's real html verbatim plus its dual
labels (human name + descriptor on the face; ai_label in the card's data
attributes, machine-readable where the piece stands).

Usage:
  generate-factory-page.py [--shell P] [--store P] [--index P] [--map P]
                           [--registry P] [--out P]   # regenerate the page
  generate-factory-page.py --check ...    # exit 0 iff --out is byte-identical
                                          # to a fresh generation
  generate-factory-page.py --harvest ...  # rebuild the presentation map from
                                          # the shell (preserves `overrides`)

Defaults resolve from this file's location (canon/engine/), so the script
works from any checkout. Output is deterministic: no timestamps -- same
inputs in, same bytes out. Deploying the generated page is step 8 and is
NOT this script's business: --out is a preview artifact.
"""
import argparse, hashlib, importlib.util, json, pathlib, re, sys

ENGINE = pathlib.Path(__file__).resolve().parent
CANON = ENGINE.parent
DEFAULT_SHELL = ENGINE / "factory-page-shell.html"
DEFAULT_MAP = ENGINE / "factory-page-presentation.json"
DEFAULT_STORE = CANON / "pieces.json"
DEFAULT_INDEX = CANON / "CANONICAL-PIECE-INDEX.json"
DEFAULT_OUT = CANON / "factory-page.generated.html"
DEFAULT_REGISTRY = ENGINE / "templates-registry.json"
DEFAULT_TWIN = CANON / "NAYA-DESIGN-CONTRACT.machine.json"
STORE_REPO_PATH = "BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json"
INDEX_REPO_PATH = "BRAIN/10-INTERFACES/SMART-FACTORY-CANON/CANONICAL-PIECE-INDEX.json"

WALK = ["#a06bff", "#3fb8ff", "#2fe89e", "#ffbf3d", "#ff9a5a", "#ff5e6c", "#e84fff"]


class GenError(Exception):
    pass


def need(cond, what):
    if not cond:
        raise GenError(what)


def esc_attr(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


def net_divs(html):
    """Net unclosed <div> count in a store fragment.

    Some store pieces are fragments whose outer divs the card closes
    (proven against the live page: stage closes == net + zoom + pstage
    on 138 of 149 standard cards; the rest are page-side extensions,
    named in the build record). The generator closes a fragment's divs
    inside its stage so every generated card is balanced.
    """
    return len(re.findall(r"<div(?:\s|>)", html)) - html.count("</div>")


# --------------------------------------------------------------------------
# Loading + the acceptance equation's left side
# --------------------------------------------------------------------------

def load_canon(store_path, index_path):
    store = json.loads(pathlib.Path(store_path).read_text(encoding="utf-8"))
    index = json.loads(pathlib.Path(index_path).read_text(encoding="utf-8"))
    need(isinstance(store, dict) and isinstance(index.get("pieces"), dict),
         "store/index shape not recognized")
    index_canon = {pid for pid, e in index["pieces"].items()
                   if e.get("status") == "canonical"}
    store_canon = {pid for pid, e in store.items()
                   if e.get("status") != "superseded"}
    need(index_canon == store_canon,
         "canonical sets disagree: index-only "
         f"{sorted(index_canon - store_canon)}, store-only "
         f"{sorted(store_canon - index_canon)}")
    for pid in sorted(store_canon):
        e = store[pid]
        need(e.get("name") and e.get("html"),
             f"{pid}: canonical store entry lacks name/html")
        al = e.get("ai_label") or {}
        need(all(al.get(k) for k in ("purpose", "use_when", "laws")),
             f"{pid}: ai_label incomplete (purpose/use_when/laws required)")
    return store, index_canon


# --------------------------------------------------------------------------
# Harvest: derive the presentation map from the shell
# --------------------------------------------------------------------------

CARD_OPEN = re.compile(
    r'<div class="pcard" style="--sc:(#[0-9a-fA-F]{6})" data-cat="([^"]+)" '
    r'data-model="(NAYA-[A-Z]+-\d+)"( data-wide="(\d+)")? data-name="[^"]*">')


def split_step4(shell):
    s4 = shell.find('<section id="step4">')
    need(s4 >= 0, 'shell: <section id="step4"> not found')
    s4end = shell.find('</section>', s4)
    need(s4end > s4, 'shell: step4 closing </section> not found')
    first_rb = shell.find('<div class="railblock"', s4)
    need(s4 < first_rb < s4end, 'shell: no railblock inside step4')
    return s4, first_rb, s4end


def parse_cards(block):
    starts = [m.start() for m in re.finditer(r'<div class="pcard"', block)]
    out = []
    for j, cs in enumerate(starts):
        ce = starts[j + 1] if j + 1 < len(starts) else len(block)
        out.append(block[cs:ce])
    return out


def parse_card(seg):
    m = CARD_OPEN.match(seg)
    if not m:
        return None
    desc_c = re.search(r'<div style="font-size:12px;opacity:\.6">([^<]*)</div>', seg)
    desc_b = re.search(r'<div class="pdesc">([^<]*)</div>', seg)
    return {
        "sc": m.group(1),
        "cat": m.group(2),
        "id": m.group(3),
        "wide": m.group(5),
        "dialect": "board" if '<div class="pfoot">' in seg else "compact",
        "desc": (desc_b or desc_c).group(1) if (desc_b or desc_c) else None,
    }


def harvest(shell_text):
    """Rail structure + per-piece presentation, derived from the shell."""
    s4, _, s4end = split_step4(shell_text)
    seg = shell_text[s4:s4end]
    rb_starts = [m.start() for m in re.finditer(r'<div class="railblock"', seg)]
    rb_starts.append(len(seg))
    rails, pieces, skipped = [], {}, []
    for i in range(len(rb_starts) - 1):
        blk = seg[rb_starts[i]:rb_starts[i + 1]]
        sec = re.search(r'--sec:(#[0-9a-fA-F]{6})', blk).group(1)
        label = re.search(r'class="pmodel">([^<]+)</span>', blk).group(1)
        ids = []
        for cseg in parse_cards(blk):
            p = parse_card(cseg)
            if p is None:
                mid = re.search(r'data-model="(NAYA-[A-Z]+-\d+)"', cseg)
                skipped.append(mid.group(1) if mid else "?")
                continue
            need(p["desc"], f"harvest: {p['id']} card carries no descriptor")
            ids.append(p["id"])
            pieces[p["id"]] = {"rail": label, "sc": p["sc"], "desc": p["desc"],
                               "dialect": p["dialect"], "cat": p["cat"],
                               **({"wide": p["wide"]} if p["wide"] else {})}
        rails.append({"label": label, "sec": sec, "pieces": ids})
    pills_c = re.search(r'<div class="psizes">(.*?)</div>',
                        parse_cards(seg)[0], re.S).group(1)
    # board pills: first board-dialect card in the shell
    pills_b = None
    for i in range(len(rb_starts) - 1):
        for cseg in parse_cards(seg[rb_starts[i]:rb_starts[i + 1]]):
            if '<div class="pfoot">' in cseg:
                pills_b = re.search(r'<div class="psizes">\n(.*?)</div>', cseg, re.S).group(1)
                break
        if pills_b: break
    need(pills_b, "harvest: no board-dialect card found for the pills block")
    return {"rails": rails, "pieces": pieces, "skipped_unparsed": skipped,
            "templates": {"pills_compact": pills_c, "pills_board": pills_b}}


# --------------------------------------------------------------------------
# Step 5: the template shelf, generated from the one registry
# --------------------------------------------------------------------------

TCARD_OPEN = '<div class="tcard2"'
TCARD = re.compile(
    r'<div class="tcard2" data-t="([^"]+)" style="--tc:(#[0-9a-fA-F]{6})">'
    r'<span class="mini-gem (\w+)" style="--tone:#[0-9a-fA-F]{6}">'
    r'(<svg .*?</svg>)</span>'
    r'<div style="flex:1;min-width:0"><b class="tbrand">(.*?)</b>'
    r'<span class="tnut">(.*?)</span>'
    r'<div class="tdetail">(.*?)</div></div>'
    r'<button class="tview" type="button">VIEW</button></div>', re.S)
PART_REF = re.compile(r'NAYA-([A-Z]+)-(\d+)((?:/\d+)*)')


def normalize_template(name):
    """The registry's own alias rule: lowercase, spaces -> hyphens."""
    return name.lower().replace(" ", "-")


def template_grid_regions(shell_text):
    """Content spans of the template grids: a <div class="tgrid"> whose first
    card is a tcard2 (the ADD-ONS grid, whose cards are addoncard, is not a
    template grid). The page carries the shelf twice and both copies are
    regenerated; returns [(content_start, content_end), ...] in file order."""
    regions = []
    for m in re.finditer(r'<div class="tgrid">', shell_text):
        start = m.start()
        i = start + len('<div class="tgrid">')
        if not shell_text.startswith(TCARD_OPEN, i):
            continue  # not a template grid (e.g. the ADD-ONS grid)
        depth, j = 1, i
        while j < len(shell_text) and depth:
            nxt_open = shell_text.find("<div", j)
            nxt_close = shell_text.find("</div>", j)
            if nxt_close < 0:
                break
            if 0 <= nxt_open < nxt_close:
                depth += 1
                j = nxt_open + 4
            else:
                depth -= 1
                j = nxt_close + len("</div>")
        need(depth == 0, "template grid <div> never closes")
        regions.append((i, j - len("</div>")))
    need(len(regions) == 2,
         f"expected exactly 2 template grids in the shell, found "
         f"{len(regions)} -- the shelf's shape changed; re-harvest and review")
    return regions


def parse_tcard(seg):
    m = TCARD.fullmatch(seg)
    if not m:
        return None
    name, tc, gem, svg, brand, nut, detail = m.groups()
    return {"key": normalize_template(name), "tc": tc, "gem": gem,
            "svg": svg, "brand": brand, "nut": nut, "detail": detail}


def harvest_templates(shell_text):
    """Per-card presentation for the template shelf, from the shell. Both
    grids must be byte-identical and tile exactly into parsed cards."""
    regions = template_grid_regions(shell_text)
    contents = [shell_text[a:b] for a, b in regions]
    need(contents[0] == contents[1],
         "the shell's two template grids differ -- the shelf has already "
         "drifted; reconcile the shell before harvesting")
    cards, order = {}, []
    segs = contents[0].split("\n")
    for seg in segs:
        c = parse_tcard(seg)
        need(c is not None,
             f"template card does not parse to the harvested grammar: "
             f"{seg[:80]}...")
        name = re.match(r'<div class="tcard2" data-t="([^"]+)"', seg).group(1)
        need(name not in cards, f"duplicate template card {name} in the grid")
        cards[name] = c
        order.append(name)
    need("\n".join(segs) == contents[0], "grid does not tile into cards")
    return {"template_order": order, "template_cards": cards}


def load_registry(registry_path):
    """The one registry + proof every templates entry has a real base. The
    base resolves as the registry's own `file` field, relative to the
    registry's folder (engine/)."""
    reg = json.loads(pathlib.Path(registry_path).read_text(encoding="utf-8"))
    need(isinstance(reg.get("templates"), dict) and reg["templates"],
         "registry shape not recognized (no templates table)")
    root = pathlib.Path(registry_path).resolve().parent
    for key, e in sorted(reg["templates"].items()):
        f = e.get("file")
        need(f, f"registry template {key} names no base file")
        need((root / f).is_file(),
             f"registry template {key} has NO base at {f} -- no card without "
             "a base; build the base or move the key to the registry's "
             "missing table")
    return reg


def base_parts(base_text, store, canon):
    """The canonical pieces a base carries, from the base's own bytes: piece
    ids it names (slash rosters like NAYA-BTN-023/024/025/021 expanded) union
    canonical pieces whose store html it embeds verbatim. Any part that is
    not canonical in the store fails loud -- no fabricated part lists."""
    named = set()
    for m in PART_REF.finditer(base_text):
        named.add(f"NAYA-{m.group(1)}-{m.group(2)}")
        for part in m.group(3).split("/"):
            if part:
                named.add(f"NAYA-{m.group(1)}-{part}")
    embedded = {pid for pid in canon
                if store[pid]["html"] and store[pid]["html"] in base_text}
    parts = named | embedded
    unknown = sorted(parts - canon)
    need(not unknown,
         f"base names/embeds pieces that are not canonical in the store: "
         f"{unknown} -- adjudicate them in the store first")
    return sorted(parts)


def resolve_template_shelf(reg, pmap, store, canon, registry_root):
    """The reconciled shelf: one card per registry template, in the page's
    own order (harvested cards keep their places; overrides insert after
    their named anchor). Harvested cards whose key sits in the registry's
    missing table come OUT -- they are returned as `excluded`, never silent.
    Returns (offered, excluded): offered entries carry name/key/presentation
    plus base (the registry file) and parts (censused from the base)."""
    cards = pmap.get("template_cards")
    need(cards is not None,
         "presentation map has no template_cards -- re-run --harvest "
         "(step 5 generates the template shelf from the registry)")
    overrides = pmap.get("template_overrides", {})
    offered, excluded = [], []
    seen = set()
    for name in pmap["template_order"]:
        key = normalize_template(name)
        if key in reg.get("missing", {}):
            excluded.append((name, key))
            continue
        need(key in reg["templates"],
             f"shelf card {name} (key {key}) is not in the registry -- the "
             "registry is the one list; add it there or the card comes out "
             "by hand, never by drift")
        need(name in cards, f"{name}: in template_order but not harvested")
        offered.append({"name": name, "key": key, **cards[name]})
        seen.add(key)
    for name, ov in overrides.items():
        key = normalize_template(name)
        need(key in reg["templates"],
             f"template override {name} names no registry template")
        need(name not in cards,
             f"template override {name} duplicates a harvested card")
        need(ov.get("reason"),
             f"template override {name} carries no reason (addition rule)")
        entry = {"name": name, "key": key,
                 **{k: ov[k] for k in ("tc", "gem", "svg", "brand", "nut",
                                       "detail")}}
        at = next(i for i, o in enumerate(offered)
                  if o["name"] == ov["after"])
        offered.insert(at + 1, entry)
        seen.add(key)
    need(seen == set(reg["templates"]),
         f"offered shelf != registry templates: registry-only "
         f"{sorted(set(reg['templates']) - seen)}, shelf-only "
         f"{sorted(seen - set(reg['templates']))} -- every registry "
         "template gets exactly one card (harvested or override, with its "
         "reason), and no card exists outside the registry")
    for o in offered:
        base_rel = reg["templates"][o["key"]]["file"]
        base_text = (registry_root / base_rel).read_text(encoding="utf-8")
        o["base"] = base_rel
        o["parts"] = base_parts(base_text, store, canon)
    return offered, excluded


def tcard_html(o):
    attrs = (f' data-base="{esc_attr(o["base"])}"'
             f' data-parts="{esc_attr(",".join(o["parts"]))}"')
    return (f'<div class="tcard2" data-t="{o["name"]}" '
            f'style="--tc:{o["tc"]}"{attrs}>'
            f'<span class="mini-gem {o["gem"]}" style="--tone:{o["tc"]}">'
            f'{o["svg"]}</span>'
            f'<div style="flex:1;min-width:0">'
            f'<b class="tbrand">{o["brand"]}</b>'
            f'<span class="tnut">{o["nut"]}</span>'
            f'<div class="tdetail">{o["detail"]}</div></div>'
            f'<button class="tview" type="button">VIEW</button></div>')


def verify_templates(page, offered):
    """The step-5 acceptance equation on the generated bytes: each grid
    carries exactly the offered cards, in order, each annotated with its
    registry base and its censused parts."""
    names = re.findall(r'<div class="tcard2" data-t="([^"]+)"', page)
    expect = [o["name"] for o in offered]
    need(names == expect * 2,
         f"template grids do not carry the offered shelf twice in order: "
         f"{names} vs {expect} x2")
    for o in offered:
        frag = (f'data-t="{o["name"]}" style="--tc:{o["tc"]}" '
                f'data-base="{o["base"]}" '
                f'data-parts="{",".join(o["parts"])}"')
        need(page.count(frag) == 2,
             f"{o['name']}: annotated card header not found in both grids")


# --------------------------------------------------------------------------
# Step 6: the "Check against the contract" door
# --------------------------------------------------------------------------

DOOR_CSS = """#contract-door{max-width:1060px;margin:26px auto 34px;padding:20px 22px;background:#0a0a0e;border:2px solid #ffffff;border-radius:16px;color:#ffffff;font-size:16px}
#contract-door .cd-intro{opacity:.85;line-height:1.5;margin:10px 0 14px}
#contract-door .cd-lab{display:block;margin:12px 0 6px;font-weight:700}
#contract-door .cd-row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
#contract-door .cd-field{flex:1;min-width:240px;background:#020203;color:#ffffff;border:2px solid #ffffff;border-radius:10px;padding:10px 12px;font-size:16px}
#contract-door textarea.cd-field{width:100%;box-sizing:border-box;flex:none}
#contract-door .cd-field:hover{border-color:#a06bff}
#contract-door .cd-field:focus{border-color:#a06bff;box-shadow:0 0 10px #a06bff;outline:none}
#contract-door .cd-btn{background:#0a0a0e;color:#ffffff;border:2px solid #ffffff;border-radius:999px;padding:10px 18px;font-size:16px;cursor:pointer}
#contract-door .cd-btn:hover{border-color:#a06bff;box-shadow:0 0 12px #a06bff}
#contract-door .cd-btn:focus{border-color:#a06bff;box-shadow:0 0 12px #a06bff;outline:none}
#contract-door .cd-msg{opacity:.85}
#contract-door .cd-check{border:1.5px solid #ffffff;border-radius:12px;padding:10px 14px;margin-top:10px}
#contract-door .cd-check.cd-fail{border-color:#ff5e6c}
#contract-door .cd-check.cd-pass{border-color:#2fe89e}
#contract-door .cd-off{opacity:.85;margin:4px 0 0}
#contract-door .cd-limits{opacity:.7;line-height:1.5;margin-top:16px}"""

DOOR_JS = r"""(function () {
"use strict";
var P = JSON.parse(document.getElementById("naya-contract-params").textContent);
var WALK = P.walk.order, WSET = {}, WIDX = {};
WALK.forEach(function (h, i) { WSET[h] = 1; WIDX[h] = i; });
var HEXRE = /#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b/g;
function normHex(t) { t = t.toLowerCase(); if (t.length === 4) { t = "#" + t[1] + t[1] + t[2] + t[2] + t[3] + t[3]; } return t; }
function hexesIn(v) { var out = [], m; HEXRE.lastIndex = 0; v = v || ""; while ((m = HEXRE.exec(v))) { out.push(normHex(m[0])); } return out; }
function parseDecls(body) { var d = {}, parts = String(body || "").split(";"), i, ix, prop; for (i = 0; i < parts.length; i++) { ix = parts[i].indexOf(":"); if (ix < 0) { continue; } prop = parts[i].slice(0, ix).trim().toLowerCase(); if (prop) { d[prop] = parts[i].slice(ix + 1).trim(); } } return d; }
function splitGroups(sel) { var groups = [], start = 0, depth = 0, quote = null, i, ch; for (i = 0; i < sel.length; i++) { ch = sel[i]; if (quote) { if (ch === quote) { quote = null; } continue; } if (ch === "'" || ch === '"') { quote = ch; } else if (ch === "[") { depth++; } else if (ch === "]") { depth--; } else if (ch === "," && depth === 0) { groups.push(sel.slice(start, i).trim()); start = i + 1; } } groups.push(sel.slice(start).trim()); return groups.filter(function (g) { return g; }); }
function splitParts(group) { var parts = [], start = 0, depth = 0, quote = null, i, ch; for (i = 0; i < group.length; i++) { ch = group[i]; if (quote) { if (ch === quote) { quote = null; } continue; } if (ch === "'" || ch === '"') { quote = ch; } else if (ch === "[") { depth++; } else if (ch === "]") { depth--; } else if (/\s/.test(ch) && depth === 0) { if (start < i) { parts.push(group.slice(start, i)); } start = i + 1; } } if (start < group.length) { parts.push(group.slice(start)); } return parts.filter(function (p) { return p; }); }
function cssTopBlocks(css) { var blocks = [], i = 0, n = css.length, start, j, k, q, depth;
  function skipWs(x) { while (x < n) { if (/\s/.test(css[x])) { x++; } else if (css.substr(x, 2) === "/*") { j = css.indexOf("*/", x + 2); x = j < 0 ? n : j + 2; } else { break; } } return x; }
  while (true) { i = skipWs(i); if (i >= n) { break; } start = i;
    while (i < n && css[i] !== "{" && css[i] !== ";") { if (css.substr(i, 2) === "/*") { j = css.indexOf("*/", i + 2); i = j < 0 ? n : j + 2; } else if (css[i] === '"' || css[i] === "'") { q = css[i]; i++; while (i < n && css[i] !== q) { i += css[i] === "\\" ? 2 : 1; } i++; } else { i++; } }
    if (i >= n) { break; } if (css[i] === ";") { i++; continue; }
    var selector = css.slice(start, i).trim(); depth = 0; j = i;
    while (j < n) { if (css.substr(j, 2) === "/*") { k = css.indexOf("*/", j + 2); j = k < 0 ? n : k + 2; continue; } if (css[j] === '"' || css[j] === "'") { q = css[j]; j++; while (j < n && css[j] !== q) { j += css[j] === "\\" ? 2 : 1; } j++; continue; } if (css[j] === "{") { depth++; } else if (css[j] === "}") { depth--; if (depth === 0) { break; } } j++; }
    blocks.push([selector, css.slice(start, j + 1)]); i = j + 1; }
  return blocks; }
function parseCssRules(cssText) { var rules = [];
  function walk(css, media) { cssTopBlocks(css).forEach(function (b) { var sel = b[0], text = b[1], low = sel.toLowerCase();
    if (low.indexOf("@media") === 0 || low.indexOf("@supports") === 0) { walk(text.slice(text.indexOf("{") + 1, text.lastIndexOf("}")), true); return; }
    if (low.charAt(0) === "@") { return; }
    var decls = parseDecls(text.slice(text.indexOf("{") + 1, text.lastIndexOf("}")));
    splitGroups(sel).forEach(function (g) { rules.push({ selector: g, decls: decls, media: media }); }); }); }
  walk(cssText || "", false); return rules; }
var STATE_RE = /:(hover|focus-visible|focus-within|focus|active)(?![\w-])/;
var STRIP_RE = /::[A-Za-z-]+(\([^()]*\))?|:(hover|focus-visible|focus-within|focus|active)(?![\w-])/g;
function baseSelector(sel) { var b = sel.replace(STRIP_RE, "").replace(/\s+/g, " ").trim(); return b || "*"; }
function hasState(sel) { return STATE_RE.test(sel); }
function parseSimple(text) { var s = { tag: null, id: null, classes: [], attrs: [] }, m = /^(?:\*|[A-Za-z][A-Za-z0-9_-]*)/.exec(text), pos = 0, tok, t;
  if (m) { var v = m[0].toLowerCase(); s.tag = v === "*" ? null : v; pos = m[0].length; }
  tok = /#([A-Za-z0-9_-]+)|\.([A-Za-z0-9_-]+)|\[([A-Za-z0-9_-]+)(?:\s*(\*=|~=|=)\s*(?:'([^']*)'|"([^"]*)"|([^\]]+)))?\]/g; tok.lastIndex = pos;
  while ((t = tok.exec(text))) { if (t.index !== pos) { throw new Error("bad selector " + text); } pos = tok.lastIndex;
    if (t[1]) { s.id = t[1]; } else if (t[2]) { s.classes.push(t[2]); } else { var val = t[5] !== undefined ? t[5] : (t[6] !== undefined ? t[6] : (t[7] !== undefined ? t[7].trim() : null)); s.attrs.push([t[3].toLowerCase(), t[4] || null, val]); } }
  if (pos !== text.length) { throw new Error("bad selector " + text); } return s; }
function matchesSimple(el, s) { if (!el || el.nodeType !== 1) { return false; }
  if (s.tag && el.tagName.toLowerCase() !== s.tag) { return false; }
  if (s.id && el.getAttribute("id") !== s.id) { return false; }
  var cls = (el.getAttribute("class") || "").split(/\s+/), i, a, act;
  for (i = 0; i < s.classes.length; i++) { if (cls.indexOf(s.classes[i]) < 0) { return false; } }
  for (i = 0; i < s.attrs.length; i++) { a = s.attrs[i]; if (!el.hasAttribute(a[0])) { return false; } if (a[1]) { act = el.getAttribute(a[0]) || ""; if (a[1] === "=" && act !== a[2]) { return false; } if (a[1] === "*=" && act.indexOf(a[2]) < 0) { return false; } if (a[1] === "~=" && act.split(/\s+/).indexOf(a[2]) < 0) { return false; } } }
  return true; }
function selectAll(doc, selector) { var out = [], seen = new Set();
  splitGroups(selector).forEach(function (group) { var parts = splitParts(group); if (!parts.length) { return; }
    var current = [doc];
    parts.forEach(function (part) { var simple; try { simple = parseSimple(part); } catch (e) { current = []; return; }
      var next = []; current.forEach(function (base) { var desc = base.querySelectorAll("*"), i; for (i = 0; i < desc.length; i++) { if (matchesSimple(desc[i], simple)) { next.push(desc[i]); } } }); current = next; });
    current.forEach(function (n) { if (!seen.has(n)) { seen.add(n); out.push(n); } }); });
  return out; }
function evidence(el) { var label = el.tagName.toLowerCase(), id = el.getAttribute("id"), cls = (el.getAttribute("class") || "").split(/\s+/).filter(Boolean), text;
  if (id) { label += "#" + id; } if (cls.length) { label += "." + cls.slice(0, 3).join("."); }
  text = (el.textContent || "").replace(/\s+/g, " ").trim(); if (text) { label += " text='" + text.slice(0, 90) + "'"; } return label; }
function makeCtx(doc, rules) { var rootVars = {}, matchCache = {};
  rules.forEach(function (r) { if (r.selector.trim() === ":root") { for (var k in r.decls) { if (k.indexOf("--") === 0) { rootVars[k] = r.decls[k]; } } } });
  function resolve(value) { var v = String(value), i, m, repl; for (i = 0; i < 3; i++) { m = /var\(\s*(--[\w-]+)\s*(?:,\s*([^)]*))?\)/.exec(v); if (!m) { break; } repl = rootVars[m[1]] !== undefined ? rootVars[m[1]] : (m[2] || ""); v = v.slice(0, m.index) + repl + v.slice(m.index + m[0].length); } return v; }
  function matched(base) { if (!(base in matchCache)) { var s = new Set(); try { selectAll(doc, base).forEach(function (n) { s.add(n); }); } catch (e) {} matchCache[base] = s; } return matchCache[base]; }
  function inlineDecls(el) { return parseDecls(el.getAttribute("style") || ""); }
  function carrierValue(el, carriers) { var inline = inlineDecls(el), i, c, hx, r, decls, has;
    for (i = 0; i < carriers.length; i++) { c = carriers[i]; if (c in inline) { hx = hexesIn(resolve(inline[c])); if (hx.length) { return [c, hx[0]]; } } }
    for (r = 0; r < rules.length; r++) { decls = rules[r].decls; has = false; for (i = 0; i < carriers.length; i++) { if (carriers[i] in decls) { has = true; } } if (!has) { continue; } if (!matched(baseSelector(rules[r].selector)).has(el)) { continue; }
      for (i = 0; i < carriers.length; i++) { c = carriers[i]; if (c in decls) { hx = hexesIn(resolve(decls[c])); if (hx.length) { return [c, hx[0]]; } } } }
    return [null, null]; }
  function inBoard(el) { var cur = el; while (cur && cur.nodeType === 1) { if (cur.getAttribute(P.board_context_attr) === P.board_context_value) { return true; } var cls = (cur.getAttribute("class") || "").split(/\s+/); for (var i = 0; i < P.board_context_classes.length; i++) { if (cls.indexOf(P.board_context_classes[i]) >= 0) { return true; } } cur = cur.parentElement; } return false; }
  return { resolve: resolve, matched: matched, inlineDecls: inlineDecls, carrierValue: carrierValue, inBoard: inBoard, rules: rules }; }
function result(id, item, name, offenders, observed) { return { id: id, section10_item: item, name: name, status: offenders.length ? "FAIL" : "PASS", offenders: offenders, observed: observed }; }
function allParents(doc) { var list = [doc], els = doc.querySelectorAll("*"), i; for (i = 0; i < els.length; i++) { list.push(els[i]); } return list; }
function childrenOf(node) { return Array.prototype.slice.call(node.children || []); }
function checkWalk(ctx, doc) { var offenders = [], groups = 0, boardOnly = {}, marker = P.chip_class_marker;
  P.board_mapping_only_hexes.forEach(function (h) { boardOnly[h] = 1; });
  function stepOk(a, b) { var ia = WIDX[a], ib = WIDX[b]; if (P.walk.wraps) { return ((ib - ia) % WALK.length + WALK.length) % WALK.length === 1; } return ib === ia + 1; }
  function expectedNext(a) { var i = WIDX[a], j = P.walk.wraps ? (i + 1) % WALK.length : i + 1; return j < WALK.length ? WALK[j] : "(end of walk)"; }
  allParents(doc).forEach(function (parent) { if (parent.nodeType === 1 && ["script", "style", "title"].indexOf(parent.tagName.toLowerCase()) >= 0) { return; }
    var kids = childrenOf(parent); if (kids.length < 2) { return; }
    [[P.sequence_carriers, true], [P.member_carriers, false]].forEach(function (pair) { var carriers = pair[0], strict = pair[1], seq = [];
      kids.forEach(function (kid) { var cls = (kid.getAttribute("class") || "").split(/\s+/), isChip = false, i; for (i = 0; i < cls.length; i++) { if (cls[i].indexOf(marker) >= 0) { isChip = true; } } if (isChip) { return; }
        var cv = ctx.carrierValue(kid, carriers); if (!cv[0]) { return; } if (boardOnly[cv[1]] && ctx.inBoard(kid)) { return; } seq.push([kid, cv[0], cv[1]]); });
      if (seq.length < 2) { return; } groups++;
      var label = strict ? "section" : "member";
      seq.forEach(function (e) { if (!WSET[e[2]]) { offenders.push(evidence(e[0]) + ": " + label + " carrier " + e[1] + " = " + e[2] + " is not a spectrum-walk color (non-walk hues live only in SmartNote board sections)"); } });
      var runs = []; seq.forEach(function (e) { if (!WSET[e[2]]) { return; } if (strict && runs.length && runs[runs.length - 1][1] === e[2]) { offenders.push(evidence(e[0]) + ": section color " + e[2] + " repeats the previous section -- the walk never wears the same color twice in a row"); } if (!runs.length || runs[runs.length - 1][1] !== e[2]) { runs.push([e[0], e[2]]); } });
      for (var i = 0; i + 1 < runs.length; i++) { if (!stepOk(runs[i][1], runs[i + 1][1])) { offenders.push(evidence(runs[i + 1][0]) + ": walk breaks " + runs[i][1] + " -> " + runs[i + 1][1] + "; the next color after " + runs[i][1] + " is " + expectedNext(runs[i][1])); } } }); });
  return result("DL-WALK", 8, "Spectrum walk sequence", offenders, { groups_checked: groups }); }
var RIM_PROPS = ["border", "border-color", "border-top", "border-right", "border-bottom", "border-left", "border-top-color", "border-right-color", "border-bottom-color", "border-left-color", "box-shadow", "outline", "outline-color"];
var IGNITION_PROPS = RIM_PROPS.concat(["color", "background", "background-color", "transform", "filter"]);
function isNeutralLight(h) { var r = parseInt(h.slice(1, 3), 16), g = parseInt(h.slice(3, 5), 16), b = parseInt(h.slice(5, 7), 16); return Math.max(r, g, b) - Math.min(r, g, b) <= 24 && Math.min(r, g, b) >= 192; }
function interactiveish(ctx, base, ignitionBases) { if (ignitionBases.has(base)) { return true; } var parts = splitParts(base); if (!parts.length) { return false; } var simple; try { simple = parseSimple(parts[parts.length - 1]); } catch (e) { return false; }
  if (simple.tag && P.interactive_tags.indexOf(simple.tag) >= 0) { return true; }
  return simple.classes.some(function (cls) { return P.interactive_class_fragments.some(function (f) { return cls.indexOf(f) >= 0; }); }); }
function checkRest(ctx) { var offenders = [], ignitionBases = new Set(), examined = 0;
  ctx.rules.forEach(function (r) { if (hasState(r.selector)) { ignitionBases.add(baseSelector(r.selector)); } });
  ctx.rules.forEach(function (r) { if (hasState(r.selector)) { return; } var base = baseSelector(r.selector);
    if (P.rest_exceptions.some(function (x) { return base.indexOf(x) >= 0; })) { return; }
    if (!interactiveish(ctx, base, ignitionBases)) { return; }
    var rim = {}; RIM_PROPS.forEach(function (k) { if (k in r.decls) { rim[k] = r.decls[k]; } });
    if (!Object.keys(rim).length) { return; } examined++;
    Object.keys(rim).forEach(function (prop) { hexesIn(ctx.resolve(rim[prop])).forEach(function (h) {
      if (WSET[h]) { offenders.push(r.selector + ": " + prop + " wears spectrum color " + h + " at rest -- elements sit white at rest and ignite on hover/focus"); }
      else if (prop !== "box-shadow" && !isNeutralLight(h)) { offenders.push(r.selector + ": " + prop + " rest rim is " + h + ", not white light (idle state = white border/glow)"); } }); }); });
  return result("DL-REST", 10, "Rest-state rims (white at rest)", offenders, { rest_rules_examined: examined }); }
function fontSizePx(value) { var m = /(\d+(?:\.\d+)?)(px|rem|em|pt|%)/.exec(value); if (!m) { return [null, null]; } var num = parseFloat(m[1]), unit = m[2];
  if (unit === "px") { return [num, null]; } if (unit === "rem") { return [num * 16, null]; } if (unit === "pt") { return [num * 4 / 3, null]; } return [null, unit]; }
function checkType(ctx, doc) { var floor = P.type_floor_px, offenders = [], skipped = [];
  function judge(where, value) { var r = fontSizePx(value); if (r[0] !== null) { if (r[0] < floor) { offenders.push(where + ": font-size " + value.trim() + " = " + r[0] + "px is below the twin's type floor (" + floor + "px)"); } } else if (r[1]) { skipped.push(where + ": " + value.trim() + " (relative unit)"); } }
  ctx.rules.forEach(function (r) { ["font-size", "font"].forEach(function (prop) { if (prop in r.decls) { judge(r.selector, r.decls[prop]); } }); });
  var els = doc.querySelectorAll("*"), i; for (i = 0; i < els.length; i++) { var inline = ctx.inlineDecls(els[i]); ["font-size", "font"].forEach(function (prop) { if (prop in inline) { judge("inline " + evidence(els[i]), inline[prop]); } }); }
  return result("DL-TYPE", 17, "Type floor", offenders, { floor_px: floor, relative_units_not_determinable: skipped.slice(0, 10), relative_units_count: skipped.length }); }
function checkDead(ctx, doc) { var offenders = [], ignition = [];
  ctx.rules.forEach(function (r) { if (hasState(r.selector) && IGNITION_PROPS.some(function (k) { return k in r.decls; })) { ignition.push(baseSelector(r.selector)); } });
  var tags = {}, sigs = {}; P.interactive_tags.forEach(function (t) { tags[t] = 1; });
  var els = doc.querySelectorAll("*"), i;
  for (i = 0; i < els.length; i++) { var el = els[i], tag = el.tagName.toLowerCase();
    if (tag === "script" || tag === "style") { continue; }
    var interactive = ((tags[tag] && tag !== "a") || (tag === "a" && el.hasAttribute("href")) || el.getAttribute("role") === "button" || el.hasAttribute("onclick"));
    if (!interactive) { continue; }
    if (tag === "input" && el.getAttribute("type") === "hidden") { continue; }
    if (el.hasAttribute("disabled")) { continue; }
    var classes = (el.getAttribute("class") || "").split(/\s+/).filter(Boolean).sort(), sig = tag + (classes.length ? "." + classes.join(".") : "");
    if (!sigs[sig]) { sigs[sig] = { count: 0, nodes: [], evidence: evidence(el) }; }
    sigs[sig].count++; sigs[sig].nodes.push(el); }
  var dead = 0;
  Object.keys(sigs).sort().forEach(function (sig) { var entry = sigs[sig], alive = false;
    ignition.forEach(function (base) { var m = ctx.matched(base); if (entry.nodes.some(function (n) { return m.has(n); })) { alive = true; } });
    if (!alive && entry.nodes.some(function (n) { return n.hasAttribute("onmouseover") || n.hasAttribute("onfocus"); })) { alive = true; }
    if (!alive) { dead++; offenders.push(sig + " x" + entry.count + " (e.g. " + entry.evidence + "): no :hover/:focus ignition rule sets border, glow, color, background, outline, transform or filter -- the element cannot light up"); } });
  return result("DL-DEAD", 22, "Dead boards (no ignition)", offenders, { interactive_signatures: Object.keys(sigs).length, dead_signatures: dead }); }
function checkChips(ctx, doc) { var offenders = [], groups = 0, marker = P.chip_class_marker, carriers = P.sequence_carriers.concat(P.member_carriers);
  allParents(doc).forEach(function (parent) { var chips = childrenOf(parent).filter(function (c) { return (c.getAttribute("class") || "").split(/\s+/).some(function (cls) { return cls.indexOf(marker) >= 0; }); });
    if (chips.length < 2) { return; } groups++;
    var seen = {};
    chips.forEach(function (chip) { var cv = ctx.carrierValue(chip, carriers), hexv = cv[1];
      if (!hexv) { var inline = ctx.inlineDecls(chip); ["border-color", "color"].forEach(function (prop) { if (!hexv && prop in inline) { var hx = hexesIn(ctx.resolve(inline[prop])); if (hx.length) { hexv = hx[0]; } } }); }
      if (!hexv) { offenders.push(evidence(chip) + ": chip carries no spectrum color (contents chips are colored by the walk)"); }
      else if (!WSET[hexv]) { offenders.push(evidence(chip) + ": chip color " + hexv + " is not a spectrum-walk color"); }
      else { (seen[hexv] = seen[hexv] || []).push(chip); } });
    Object.keys(seen).forEach(function (h) { if (seen[h].length > 1) { offenders.push(evidence(parent) + ": " + seen[h].length + " contents chips share " + h + " -- a same-color cluster; chips carry distinct spectrum colors"); } }); });
  return result("DL-CHIPS", 8, "Contents chips (distinct colors)", offenders, { chip_groups_checked: groups }); }
function runChecks(html) { var doc = new DOMParser().parseFromString(html, "text/html");
  var styleText = Array.prototype.map.call(doc.querySelectorAll("style"), function (s) { return s.textContent; }).join("\n");
  var rules = parseCssRules(styleText), ctx = makeCtx(doc, rules);
  return [checkWalk(ctx, doc), checkRest(ctx), checkType(ctx, doc), checkDead(ctx, doc), checkChips(ctx, doc)]; }
function el(tag, cls, text) { var n = document.createElement(tag); if (cls) { n.className = cls; } if (text !== undefined) { n.textContent = text; } return n; }
function render(results, sourceLabel) { var box = document.getElementById("cd-results"); box.textContent = "";
  var failed = results.filter(function (r) { return r.status !== "PASS"; }).length;
  var head = el("p", null, (failed ? "FAIL — " + failed + " of " + results.length + " mechanical checks failed" : "PASS — all " + results.length + " mechanical checks pass") + " · " + sourceLabel + " · rules: " + P.source + (P.contract_version ? " v" + P.contract_version : ""));
  head.style.fontWeight = "700"; box.appendChild(head);
  results.forEach(function (r) { var card = el("div", "cd-check " + (r.status === "PASS" ? "cd-pass" : "cd-fail"));
    card.appendChild(el("div", null, (r.status === "PASS" ? "✓ " : "✗ ") + r.id + " — " + r.name + " (§10." + r.section10_item + ")"));
    r.offenders.slice(0, 8).forEach(function (o) { card.appendChild(el("p", "cd-off", o)); });
    if (r.offenders.length > 8) { card.appendChild(el("p", "cd-off", "… and " + (r.offenders.length - 8) + " more")); }
    box.appendChild(card); }); }
function msg(text) { document.getElementById("cd-msg").textContent = text; }
document.getElementById("cd-cannot").textContent = P.not_mechanically_checkable.map(function (e) { return "§10." + e.item + " " + e.name; }).join(" · ");
document.getElementById("cd-run").addEventListener("click", function () { var src = document.getElementById("cd-src").value;
  if (!src.trim()) { msg("Paste a page source first."); return; }
  try { render(runChecks(src), "pasted source, " + src.length + " bytes"); msg(""); } catch (e) { msg("The check itself failed: " + e.message); } });
document.getElementById("cd-fetch").addEventListener("click", function () { var url = document.getElementById("cd-url").value.trim();
  if (!url) { msg("Enter a page URL first."); return; }
  msg("Fetching…");
  fetch(url).then(function (r) { if (!r.ok) { throw new Error("HTTP " + r.status); } return r.text(); }).then(function (text) { try { render(runChecks(text), url + ", " + text.length + " bytes"); msg(""); } catch (e) { msg("The check itself failed: " + e.message); } })
  .catch(function (e) { msg("Could not fetch " + url + " (" + e.message + "). Browsers block many cross-origin reads (CORS) — paste the page source instead; the same checks run on pasted bytes."); }); });
})();"""


def load_design_params(twin_path):
    """The check parameters for the door, from the machine twin, extracted
    by the checker's own design_params() -- the generator never re-derives
    a rule value. A twin that cannot supply parameters fails the build
    loud (the door would otherwise ship stale rules)."""
    raw = read(twin_path, "machine twin")
    twin = json.loads(raw.decode("utf-8"))
    spec = importlib.util.spec_from_file_location(
        "check_standard_features", ENGINE / "check_standard_features.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        return module.design_params(twin)
    except ValueError as e:
        raise GenError(f"machine twin cannot supply check parameters: {e}")


def door_html(params):
    """The door region: ONE contiguous block (style + section + params +
    logic). Removing exactly these bytes from the generated page restores
    the step-5 page. Chrome colors are the page's own dominant tokens
    (near-black ground, white text/rims, purple signature); every RULE
    value -- the walk, the type floor, the carrier lists -- arrives via
    the embedded params, never via this markup."""
    params_json = json.dumps(params, indent=1, sort_keys=True)
    return ('<style data-generated="contract-door-css">\n' + DOOR_CSS +
            '\n</style>\n'
            '<section id="contract-door" data-generated="contract-door">\n'
            '  <div class="railhead"><span class="sec-dot"></span>'
            '<span class="pmodel">Check against the contract</span>'
            '<span style="font-size:12px;opacity:.5">the gate, on the '
            'page</span></div>\n'
            '  <p class="cd-intro">Paste or fetch any page and the '
            'mechanical items of the \u00a710 Same-Language Check answer '
            'here, on the same rule data the build gate reads from the '
            'machine twin. Verdicts name the offenders; nothing here is a '
            'rubber stamp.</p>\n'
            '  <label class="cd-lab" for="cd-url">Page URL</label>\n'
            '  <div class="cd-row"><input class="cd-field" id="cd-url" '
            'type="url" placeholder="https://your-page.example/">'
            '<button class="cd-btn" id="cd-fetch" type="button">Fetch '
            '&amp; check</button></div>\n'
            '  <label class="cd-lab" for="cd-src">\u2026or paste the page '
            'source</label>\n'
            '  <textarea class="cd-field" id="cd-src" rows="7" '
            'placeholder="&lt;!doctype html&gt; \u2026"></textarea>\n'
            '  <div class="cd-row"><button class="cd-btn" id="cd-run" '
            'type="button">Check pasted source</button>'
            '<span class="cd-msg" id="cd-msg" role="status"></span></div>\n'
            '  <div id="cd-results" aria-live="polite"></div>\n'
            '  <p class="cd-limits">This door runs the checks that are '
            'mechanical \u2014 decidable from page bytes (inline and '
            '&lt;style&gt; CSS; external stylesheets are not in the '
            'bytes). The rest of \u00a710 needs eyes on the rendered page '
            'and is named, not skipped: <span id="cd-cannot"></span>. A '
            'fetch can also be blocked by the other site\u2019s CORS '
            'policy \u2014 paste the source instead; the same checks run '
            'on pasted bytes.</p>\n'
            '</section>\n'
            '<script type="application/json" id="naya-contract-params">'
            + params_json + '</script>\n'
            '<script data-generated="contract-door-js">\n' + DOOR_JS +
            '\n</script>\n')


def verify_door(page, params):
    need(page.count('data-generated="contract-door"') == 1,
         "generated page must carry exactly one contract door")
    need(page.count('id="naya-contract-params"') == 1,
         "generated page must carry exactly one door params block")
    m = re.search(r'<script type="application/json" '
                  r'id="naya-contract-params">(.*?)</script>', page, re.S)
    need(m is not None, "door params block not found on the generated page")
    need(json.loads(m.group(1)) == params,
         "door params on the page != the twin's extracted parameters")


# --------------------------------------------------------------------------
# Generation
# --------------------------------------------------------------------------

def card_html(pid, store, pres, pills):
    e = store[pid]
    al = e["ai_label"]
    ai = (f' data-ai-purpose="{esc_attr(al["purpose"])}"'
          f' data-ai-use="{esc_attr(al["use_when"])}"'
          f' data-ai-laws="{esc_attr(", ".join(al["laws"]))}"')
    name = esc_attr(e["name"])
    nd = "</div>" * net_divs(e["html"])
    if pres["dialect"] == "board":
        return (f'<div class="pcard" style="--sc:{pres["sc"]}" data-cat="{pres["cat"]}" '
                f'data-model="{pid}" data-name="{name}"{ai}>\n'
                f'      <div class="pstage"><div class="zoom">\n'
                f'        {e["html"]}{nd}\n'
                f'      </div></div>\n'
                f'      <div class="pmodel">{pid}</div>\n'
                f'      <div class="pname">{e["name"]}</div>\n'
                f'      <div class="pdesc">{pres["desc"]}</div>\n'
                f'      <div class="pfoot">\n'
                f'        <div class="psizes">\n{pills["pills_board"]}</div>\n'
                f'        <div class="prow"><button class="btn-select elev-1" type="button">Select</button>'
                f'<button class="btn-notes carve-1" type="button">Notes</button></div>\n'
                f'      </div>\n'
                f'    </div>')
    wide = f' data-wide="{pres["wide"]}"' if pres.get("wide") else ""
    return (f'<div class="pcard" style="--sc:{pres["sc"]}" data-cat="{pres["cat"]}" '
            f'data-model="{pid}"{wide} data-name="{name}"{ai}>\n'
            f'  <div class="pstage carve-1"><div class="zoom">{e["html"]}{nd}</div></div>\n'
            f'  <div><div class="pmodel">{pid}</div><div class="pname">{e["name"]}</div>\n'
            f'  <div style="font-size:12px;opacity:.6">{pres["desc"]}</div></div>\n'
            f'  <div class="psizes">{pills["pills_compact"]}</div>\n'
            f'  <div class="prow"><button class="btn-select elev-1" type="button">Select</button>'
            f'<button class="btn-notes carve-1" type="button">Notes</button></div>\n'
            f'</div>')


def railblock_html(rail, store, presentations, pills):
    cards = "\n".join(card_html(pid, store, presentations[pid], pills)
                      for pid in rail["pieces"])
    return (f'<div class="railblock" style="--sec:{rail["sec"]}">'
            f'<div class="railhead"><span class="sec-dot"></span>'
            f'<span class="pmodel">{rail["label"]}</span>'
            f'<span style="font-size:12px;opacity:.5">scroll sideways</span></div>'
            f'<div class="rail">{cards}</div></div>')


def resolve_presentations(pmap, canon):
    """Final per-piece presentation + final rail order, or fail loud."""
    pres = dict(pmap.get("pieces", {}))
    overrides = pmap.get("overrides", {})
    for pid, ov in overrides.items():
        need(pid not in pres, f"override {pid} duplicates a harvested entry")
        pres[pid] = {k: ov[k] for k in ("rail", "sc", "desc", "dialect", "cat")}
    missing = sorted(canon - set(pres))
    need(not missing,
         "canonical pieces with NO presentation entry (addition rule: a part "
         f"lands whole -- rail, color, descriptor -- or not at all): {missing}")
    rails = []
    placed = []
    for r in pmap["rails"]:
        ids = [pid for pid in r["pieces"] if pid in canon]
        placed += ids
        rails.append({"label": r["label"], "sec": r["sec"], "pieces": ids})
    for nr in pmap.get("new_rails", []):
        ids = [pid for pid, ov in overrides.items()
               if ov.get("rail") == nr["label"] and pid in canon]
        need(ids, f"new rail {nr['label']} has no override pieces")
        entry = {"label": nr["label"], "sec": nr["sec"], "pieces": sorted(ids)}
        at = next(i for i, r in enumerate(rails) if r["label"] == nr["after"])
        rails.insert(at + 1, entry)
        placed += ids
    # override pieces joining EXISTING rails ride at the rail's end, id order
    by_rail = {r["label"]: r for r in rails}
    for pid, ov in sorted(overrides.items()):
        if pid in canon and pid not in placed:
            by_rail[ov["rail"]]["pieces"].append(pid)
            placed.append(pid)
    need(sorted(placed) == sorted(canon),
         f"rail placement != canonical set: placed {len(placed)}, "
         f"canon {len(canon)}, diff {sorted(set(canon) ^ set(placed))}")
    need(len(placed) == len(set(placed)), "a piece is placed on two rails")
    return pres, rails


def css_blocks(css):
    """Split a stylesheet into top-level blocks (selector text, full text),
    skipping comments and strings while matching braces."""
    blocks, i, n = [], 0, len(css)
    while i < n:
        while i < n:
            if css[i].isspace():
                i += 1
            elif css.startswith("/*", i):
                j = css.find("*/", i + 2)
                i = n if j < 0 else j + 2
            else:
                break
        if i >= n:
            break
        start = i
        while i < n and css[i] not in "{;":
            if css.startswith("/*", i):
                j = css.find("*/", i + 2)
                i = n if j < 0 else j + 2
            elif css[i] in "\"'":
                q = css[i]
                i += 1
                while i < n and css[i] != q:
                    i += 2 if css[i] == "\\" else 1
                i += 1
            else:
                i += 1
        if i >= n:
            break
        if css[i] == ";":
            i += 1
            continue
        selector = css[start:i].strip()
        depth, j = 0, i
        while j < n:
            if css.startswith("/*", j):
                k = css.find("*/", j + 2)
                j = n if k < 0 else k + 2
                continue
            if css[j] in "\"'":
                q = css[j]
                j += 1
                while j < n and css[j] != q:
                    j += 2 if css[j] == "\\" else 1
                j += 1
                continue
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        blocks.append((selector, css[start:j + 1]))
        i = j + 1
    return blocks


def class_defined(text, cls):
    return re.search(r"\." + re.escape(cls) + r"(?![\w-])", text) is not None


def piece_css(store, canon, factory_css, shell_text):
    """The store's own CSS for classes canonical pieces use that the shell
    page does not define -- derived from factory.css in file order, @media
    recursed, referenced @keyframes and shell-missing :root variables
    carried along. Returns (css_body, sorted class list)."""
    needed = set()
    for pid in canon:
        for attr in re.findall(r'class="([^"]+)"', store[pid]["html"]):
            for cls in attr.split():
                if not class_defined(shell_text, cls) and class_defined(factory_css, cls):
                    needed.add(cls)
    if not needed:
        return "", []
    keyframe_names, var_names = set(), set()

    def keep_from(blocks):
        out = []
        for selector, text in blocks:
            low = selector.lower()
            if low.startswith(("@media", "@supports")):
                inner = css_blocks(text[text.index("{") + 1:text.rindex("}")])
                inner_kept = keep_from(inner)
                if inner_kept:
                    head = text[:text.index("{") + 1]
                    out.append(head + "\n" + "\n".join(inner_kept) + "\n}")
                continue
            if low.startswith("@"):
                continue
            if any(class_defined(selector, cls) for cls in needed):
                out.append(text)
                keyframe_names.update(
                    re.findall(r"animation(?:-name)?\s*:\s*([\w-]+)", text))
                var_names.update(re.findall(r"var\(\s*(--[\w-]+)", text))
        return out

    kept = keep_from(css_blocks(factory_css))
    extras = []
    root_vars = [v for v in sorted(var_names)
                 if not re.search(re.escape(v) + r"\s*:", shell_text)]
    if root_vars:
        decls = set()
        for selector, text in css_blocks(factory_css):
            if selector.strip() == ":root":
                for v in root_vars:
                    m = re.search(re.escape(v) + r"\s*:\s*([^;]+);", text)
                    if m:
                        decls.add("  %s: %s;" % (v, m.group(1).strip()))
        if decls:
            extras.append(":root {\n" + "\n".join(sorted(decls)) + "\n}")
    for selector, text in css_blocks(factory_css):
        m = re.match(r"@keyframes\s+([\w-]+)", selector)
        if m and m.group(1) in keyframe_names:
            extras.append(text)
    body = "\n".join(extras + kept)
    missing = [c for c in sorted(needed) if not class_defined(body, c)]
    need(not missing,
         "factory.css extraction missed classes: %s" % ", ".join(missing))
    return body, sorted(needed)


STYLE_OPEN = '<style data-generated="factory-piece-css">'


def build_page(shell_text, store, canon, pmap, factory_css, twin,
               design=None):
    pres, rails = resolve_presentations(pmap, canon)
    _, first_rb, s4end = split_step4(shell_text)
    region = "\n".join(railblock_html(r, store, pres, pmap["templates"])
                       for r in rails)
    offered, _excluded = twin
    tcards = "\n".join(tcard_html(o) for o in offered)
    # Every generated region is located on the ORIGINAL shell, then all
    # replacements are applied last-to-first so no region can shift another:
    # the parts shelf keeps step 4's exact span and bytes, and each template
    # grid's content is swapped for the registry-generated cards.
    spans = [(first_rb, s4end, region + "\n")]
    for a, b in template_grid_regions(shell_text):
        spans.append((a, b, tcards))
    page = shell_text
    for a, b, text in sorted(spans, key=lambda s: s[0], reverse=True):
        page = page[:a] + text + page[b:]
    css_body, css_classes = piece_css(store, canon, factory_css, shell_text)
    if css_body:
        need(page.count("</head>") == 1, "shell must carry exactly one </head>")
        style = (STYLE_OPEN + "\n/* Carried from the canon's factory.css: the "
                 "store's own rules for the classes below -- canonical pieces "
                 "use them, the shell page defines none of them. Generated; "
                 "do not hand-edit. Classes: " + ", ".join(css_classes) +
                 " */\n" + css_body + "\n</style>\n")
        page = page.replace("</head>", style + "</head>", 1)
    verify_page(page, store, canon, pres, css_classes)
    verify_templates(page, offered)
    if design is not None:
        need(page.count("</body>") == 1,
             "shell must carry exactly one </body> to seat the door")
        page = page.replace("</body>", door_html(design) + "</body>", 1)
        verify_door(page, design)
    return page


def verify_page(page, store, canon, pres, css_classes=()):
    """The acceptance equation + per-card fidelity, on the generated bytes."""
    ids = re.findall(r'<div class="pcard"[^>]*data-model="(NAYA-[A-Z]+-\d+)"', page)
    need(len(ids) == len(canon),
         f"card count {len(ids)} != canonical {len(canon)}")
    need(set(ids) == canon,
         f"card set != canonical set: {sorted(set(ids) ^ canon)}")
    need(len(ids) == len(set(ids)), "duplicate card on the generated page")
    for pid in canon:
        need(store[pid]["html"] in page,
             f"{pid}: store html not present verbatim on the generated page")
        al = store[pid]["ai_label"]
        need(f'data-ai-purpose="{esc_attr(al["purpose"])}"' in page,
             f"{pid}: ai_label not carried through")
    if css_classes:
        need(page.count(STYLE_OPEN) == 1,
             "generated piece-css style block missing or duplicated")
        block = page.split(STYLE_OPEN, 1)[1].split("</style>", 1)[0]
        for cls in css_classes:
            need(class_defined(block, cls),
                 f"piece-css block carries no rule for .{cls}")
    return len(ids)


# --------------------------------------------------------------------------

def read(path, what):
    try:
        return pathlib.Path(path).read_bytes()
    except OSError as e:
        print(f"generate-factory-page: cannot read {what} {path}: {e}",
              file=sys.stderr)
        raise SystemExit(2)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--shell", type=pathlib.Path, default=DEFAULT_SHELL)
    ap.add_argument("--store", type=pathlib.Path, default=DEFAULT_STORE)
    ap.add_argument("--index", type=pathlib.Path, default=DEFAULT_INDEX)
    ap.add_argument("--map", type=pathlib.Path, default=DEFAULT_MAP)
    ap.add_argument("--out", type=pathlib.Path, default=DEFAULT_OUT)
    ap.add_argument("--css", type=pathlib.Path, default=CANON / "factory.css")
    ap.add_argument("--registry", type=pathlib.Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--twin", type=pathlib.Path, default=DEFAULT_TWIN,
                    help="machine twin the contract door's check parameters "
                         "are extracted from")
    ap.add_argument("--check", action="store_true",
                    help="exit 0 iff --out is byte-identical to a fresh generation")
    ap.add_argument("--harvest", action="store_true",
                    help="rebuild the presentation map from the shell")
    args = ap.parse_args(argv)

    shell_bytes = read(args.shell, "shell")
    shell_text = shell_bytes.decode("utf-8")
    shell_sha = hashlib.sha256(shell_bytes).hexdigest()

    if args.harvest:
        h = harvest(shell_text)
        ht = harvest_templates(shell_text)
        old = {}
        if args.map.exists():
            old = json.loads(args.map.read_text(encoding="utf-8"))
        pmap = {
            "kind": "factory-page-presentation",
            "authority": ("Presentation harvested from the live page's own "
                          "bytes (engine/factory-page-shell.html). Regenerate "
                          "with --harvest; never hand-edit the harvested "
                          "fields. `overrides` is the only hand-kept section: "
                          "canonical pieces the current page does not show, "
                          "each with its reason."),
            "shell_sha256": shell_sha,
            "shell_bytes": len(shell_bytes),
            "rails": h["rails"],
            "pieces": h["pieces"],
            "skipped_unparsed_cards": h["skipped_unparsed"],
            "templates": h["templates"],
            "overrides": old.get("overrides", {}),
            "new_rails": old.get("new_rails", []),
            "template_order": ht["template_order"],
            "template_cards": ht["template_cards"],
            "template_overrides": old.get("template_overrides", {}),
        }
        args.map.write_text(json.dumps(pmap, indent=1, ensure_ascii=False) + "\n",
                            encoding="utf-8")
        print(f"generate-factory-page: harvested {len(h['pieces'])} presentations, "
              f"{len(h['rails'])} rails, {len(ht['template_cards'])} template "
              f"cards from shell sha256 {shell_sha[:12]}... -> {args.map}")
        return 0

    try:
        store, canon = load_canon(args.store, args.index)
        pmap = json.loads(read(args.map, "presentation map").decode("utf-8"))
        need(pmap.get("shell_sha256") == shell_sha,
             "shell sha256 != the map's harvested shell "
             f"({shell_sha[:12]}... vs {str(pmap.get('shell_sha256'))[:12]}...) -- "
             "the shell changed; re-run --harvest and review the presentation")
        reg = load_registry(args.registry)
        twin = resolve_template_shelf(reg, pmap, store, canon,
                                      args.registry.resolve().parent)
        factory_css = read(args.css, "factory css").decode("utf-8")
        design = load_design_params(args.twin)
        page = build_page(shell_text, store, canon, pmap, factory_css, twin,
                          design=design)
    except GenError as e:
        print(f"generate-factory-page: GENERATION FAILED: {e}", file=sys.stderr)
        return 2

    offered, excluded = twin
    for name, key in excluded:
        print(f"generate-factory-page: shelf excludes {name} (registry key "
              f"{key}: in the registry's missing table -- no base, no card)")
    counts = (f"{len(canon)} canonical == {len(canon)} store == "
              f"{len(canon)} cards; {len(offered)} registry == "
              f"{len(offered)} bases == {len(offered)} template cards "
              "x2 grids; contract door seated (check params from "
              f"{args.twin.name})")
    data = page.encode("utf-8")
    if args.check:
        if not args.out.exists():
            print(f"CHECK FAIL: generated page missing at {args.out}")
            return 1
        if args.out.read_bytes() == data:
            print(f"CHECK PASS: {args.out.name} is byte-identical to a fresh "
                  f"generation ({counts})")
            return 0
        print(f"CHECK FAIL: {args.out.name} differs from a fresh generation -- "
              "regenerate it, never hand-edit it")
        return 1

    args.out.write_bytes(data)
    print(f"generate-factory-page: wrote {args.out} ({len(data)} bytes): "
          f"{counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
