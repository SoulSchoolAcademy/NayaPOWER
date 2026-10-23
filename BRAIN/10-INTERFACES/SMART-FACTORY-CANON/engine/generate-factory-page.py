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

The acceptance equation is enforced mechanically on every run:

  count(canonical in index) == count(canonical in store) ==
  count(piece cards in the generated page)

and every card carries its store piece's real html verbatim plus its dual
labels (human name + descriptor on the face; ai_label in the card's data
attributes, machine-readable where the piece stands).

Usage:
  generate-factory-page.py [--shell P] [--store P] [--index P] [--map P]
                           [--out P]        # regenerate the page
  generate-factory-page.py --check ...    # exit 0 iff --out is byte-identical
                                          # to a fresh generation
  generate-factory-page.py --harvest ...  # rebuild the presentation map from
                                          # the shell (preserves `overrides`)

Defaults resolve from this file's location (canon/engine/), so the script
works from any checkout. Output is deterministic: no timestamps -- same
inputs in, same bytes out. Deploying the generated page is step 8 and is
NOT this script's business: --out is a preview artifact.
"""
import argparse, hashlib, json, pathlib, re, sys

ENGINE = pathlib.Path(__file__).resolve().parent
CANON = ENGINE.parent
DEFAULT_SHELL = ENGINE / "factory-page-shell.html"
DEFAULT_MAP = ENGINE / "factory-page-presentation.json"
DEFAULT_STORE = CANON / "pieces.json"
DEFAULT_INDEX = CANON / "CANONICAL-PIECE-INDEX.json"
DEFAULT_OUT = CANON / "factory-page.generated.html"
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


def build_page(shell_text, store, canon, pmap, factory_css):
    pres, rails = resolve_presentations(pmap, canon)
    _, first_rb, s4end = split_step4(shell_text)
    region = "\n".join(railblock_html(r, store, pres, pmap["templates"])
                       for r in rails)
    page = shell_text[:first_rb] + region + "\n" + shell_text[s4end:]
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
        }
        args.map.write_text(json.dumps(pmap, indent=1, ensure_ascii=False) + "\n",
                            encoding="utf-8")
        print(f"generate-factory-page: harvested {len(h['pieces'])} presentations, "
              f"{len(h['rails'])} rails from shell sha256 {shell_sha[:12]}... "
              f"-> {args.map}")
        return 0

    try:
        store, canon = load_canon(args.store, args.index)
        pmap = json.loads(read(args.map, "presentation map").decode("utf-8"))
        need(pmap.get("shell_sha256") == shell_sha,
             "shell sha256 != the map's harvested shell "
             f"({shell_sha[:12]}... vs {str(pmap.get('shell_sha256'))[:12]}...) -- "
             "the shell changed; re-run --harvest and review the presentation")
        factory_css = read(args.css, "factory css").decode("utf-8")
        page = build_page(shell_text, store, canon, pmap, factory_css)
    except GenError as e:
        print(f"generate-factory-page: GENERATION FAILED: {e}", file=sys.stderr)
        return 2

    data = page.encode("utf-8")
    if args.check:
        if not args.out.exists():
            print(f"CHECK FAIL: generated page missing at {args.out}")
            return 1
        if args.out.read_bytes() == data:
            print(f"CHECK PASS: {args.out.name} is byte-identical to a fresh "
                  f"generation ({len(canon)} canonical == {len(canon)} store == "
                  f"{len(canon)} cards)")
            return 0
        print(f"CHECK FAIL: {args.out.name} differs from a fresh generation -- "
              "regenerate it, never hand-edit it")
        return 1

    args.out.write_bytes(data)
    print(f"generate-factory-page: wrote {args.out} ({len(data)} bytes): "
          f"{len(canon)} canonical == {len(canon)} store == {len(canon)} cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
