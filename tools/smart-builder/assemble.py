#!/usr/bin/env python3
"""
Smart Builder ASSEMBLER (Team Nitro, seat BUILD/Nu; functions: WIRE/Omega).

Contract data + library version in, finished HTML out.
Deterministic: same inputs -> same bytes, every time. Stdlib only.

Usage:
    python3 assemble.py --contract page.contract.json --registry registry.json \
        --functions-registry FUNCTIONS-REGISTRY.json \
        --out page.html [--tokens tokens.css]

Exit codes:
    0  assembled OK
    1  usage / structural error (bad JSON, missing required blocks)
    2  GAP: a referenced piece (or the nav/footer slot) has no registry entry,
       or a contract function id has no functions-registry entry.
       The assembler NEVER improvises a piece or a function.

Determinism contract:
    - section order is exactly contract order (json preserves document order)
    - function order is contract 'functions' order, then 'functions_default' order
    - no timestamps, no randomness, no environment reads
    - the only JSON serializations use sort_keys=True
    - no set/dict iteration that can vary run to run (registry lookup only)
"""
import argparse
import html
import json
import re
import sys

GAP_EXIT = 2

SELECTOR_RE = re.compile(r"^\[([A-Za-z0-9_-]+)=['\"]([^'\"]*)['\"]\]$")


def fail_gap(message):
    sys.stderr.write(message + "\n")
    sys.exit(GAP_EXIT)


def fail_error(message):
    sys.stderr.write("ERROR: " + message + "\n")
    sys.exit(1)


def load_json(path, label):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        fail_error("%s not found: %s" % (label, path))
    except json.JSONDecodeError as exc:
        fail_error("%s is not valid JSON (%s): %s" % (label, exc, path))


def render_body(text):
    """Plain-text body -> <p> paragraphs. Escaped, deterministic."""
    paras = [p.strip() for p in str(text).split("\n\n")]
    out = []
    for p in paras:
        if not p:
            continue
        escaped = html.escape(p, quote=False).replace("\n", "<br>")
        out.append("<p>%s</p>" % escaped)
    return "".join(out)


def stamp_piece(nid, fragment):
    """Stamp a registry fragment with its naya_id for traceability.

    Injects data-naya-piece="<naya_id>" into the fragment's first tag,
    deterministically. The verifier requires this stamp on every inserted
    piece; unstamped markup fails the gate.
    """
    return re.sub(r'<([a-zA-Z][a-zA-Z0-9-]*)',
                  r'<\1 data-naya-piece="%s"' % html.escape(nid, quote=True),
                  fragment, count=1)


def parse_selector(selector):
    """Parse a simple [attr='value'] selector. Returns (attr, value) or None."""
    m = SELECTOR_RE.match(selector.strip())
    if not m:
        return None
    return m.group(1), m.group(2)


def selector_present(markup, selector):
    """True if the [attr='value'] selector matches an element in the markup."""
    parsed = parse_selector(selector)
    if parsed is None:
        return False
    attr, value = parsed
    pat = re.compile(r'%s\s*=\s*["\']%s["\']' % (re.escape(attr), re.escape(value)))
    return pat.search(markup) is not None


def build_head(page, token_css, pwa):
    lines = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        '<meta name="theme-color" content="#0b0b12">',
        '<meta name="mobile-web-app-capable" content="yes">',
        '<meta name="apple-mobile-web-app-capable" content="yes">',
        '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">',
        "<title>%s</title>" % html.escape(str(page.get("title", "")), quote=True),
        '<link rel="manifest" href="manifest.webmanifest">',
        "<!-- PWA note: manifest.webmanifest and the app icon are produced by the",
        "     deploy step (intake icon choice), never invented here. The assembler",
        "     only guarantees the link and the mobile-first meta are present. -->",
        "<style>",
        token_css,
        "</style>",
        "</head>",
    ]
    return lines


def load_functions_registry(path):
    raw = load_json(path, "functions registry")
    if not isinstance(raw, dict) or "functions" not in raw:
        fail_error("functions registry must be an object with 'functions'")
    by_id = {}
    alias_to_id = {}
    for entry in raw["functions"]:
        if not isinstance(entry, dict):
            fail_error("functions registry entry is not an object")
        nid = entry.get("naya_id")
        if not nid:
            fail_error("functions registry entry is missing naya_id")
        if nid in by_id:
            fail_error("functions registry has duplicate naya_id: %s" % nid)
        for key in ("wiring_js", "requires_dom", "activation", "human_label", "status"):
            if key not in entry:
                fail_error("functions registry entry %s is missing '%s'" % (nid, key))
        if not isinstance(entry["requires_dom"], list):
            fail_error("functions registry entry %s: requires_dom must be a list" % nid)
        by_id[nid] = entry
        for alias in entry.get("aliases", []) or []:
            alias_to_id.setdefault(str(alias), nid)
    return by_id, alias_to_id


def resolve_function(fid, by_id, alias_to_id, where):
    """Resolve a contract function id (canonical or alias) to its entry."""
    if fid in by_id:
        return by_id[fid]
    if fid in alias_to_id:
        return by_id[alias_to_id[fid]]
    fail_gap("GAP: %s references unknown function id '%s' (no functions-registry entry)" % (where, fid))


def main():
    ap = argparse.ArgumentParser(
        description="Smart Builder assembler: page contract + piece registry + functions registry -> HTML."
    )
    ap.add_argument("--contract", required=True, help="page-contract JSON file")
    ap.add_argument("--registry", required=True, help="piece registry JSON file")
    ap.add_argument("--functions-registry", required=True,
                    help="functions registry JSON file (wiring units)")
    ap.add_argument("--out", required=True, help="output HTML file")
    ap.add_argument("--tokens", default=None, help="optional CSS file with design tokens to inline")
    args = ap.parse_args()

    contract = load_json(args.contract, "contract")
    registry = load_json(args.registry, "registry")
    fn_by_id, fn_aliases = load_functions_registry(args.functions_registry)

    if not isinstance(contract, dict) or "page" not in contract or "sections" not in contract:
        fail_error("contract must be an object with 'page' and 'sections'")
    if not isinstance(registry, dict) or "pieces" not in registry:
        fail_error("registry must be an object with 'pieces'")

    page = contract["page"]
    sections = contract["sections"]
    library_version = registry.get("library_version", "0.0.0")

    pieces = {}
    piece_order = []
    for entry in registry["pieces"]:
        nid = entry.get("naya_id")
        if nid is None:
            fail_error("registry piece is missing naya_id")
        pieces[nid] = entry
        piece_order.append(nid)

    # 1. FAIL CLOSED: every referenced naya_id must exist, checked in contract order.
    for section in sections:
        sid = section.get("section_id", "?")
        for nid in section.get("pieces", []):
            if nid not in pieces:
                fail_gap("GAP: section %s references unknown piece %s" % (sid, nid))

    # 2. nav = first nav-category piece; footer = first footer-category piece.
    nav_piece = None
    footer_piece = None
    for nid in piece_order:
        cat = pieces[nid].get("category")
        if nav_piece is None and cat == "nav":
            nav_piece = pieces[nid]
        if footer_piece is None and cat == "footer":
            footer_piece = pieces[nid]
    if nav_piece is None:
        fail_gap("GAP: registry has no nav-category piece")
    if footer_piece is None:
        fail_gap("GAP: registry has no footer-category piece")

    # 3. FUNCTIONS: contract 'functions' (explicit) + 'functions_default',
    #    deduplicated in order. Aliases resolve; unknown ids fail closed (exit 2).
    explicit = contract.get("functions") or []
    defaults = contract.get("functions_default") or []
    if not isinstance(explicit, list) or not isinstance(defaults, list):
        fail_error("contract 'functions' and 'functions_default' must be arrays")
    activated = []
    for fid in list(explicit) + list(defaults):
        entry = resolve_function(str(fid), fn_by_id, fn_aliases, "contract")
        if entry["naya_id"] not in [e["naya_id"] for e in activated]:
            activated.append(entry)

    # 4. Token CSS: inlined from --tokens, else a placeholder comment.
    if args.tokens:
        try:
            with open(args.tokens, "r", encoding="utf-8") as fh:
                token_css = fh.read().rstrip("\n")
        except FileNotFoundError:
            fail_error("tokens file not found: %s" % args.tokens)
    else:
        token_css = "/* TOKENS PLACEHOLDER: pass --tokens <file> to inline design tokens */"

    out_lines = build_head(page, token_css, contract.get("pwa", {}))

    out_lines.append(
        '<body data-page-slug="%s" data-contract-version="%s" data-library-version="%s">'
        % (
            html.escape(str(page.get("slug", "")), quote=True),
            html.escape(str(contract.get("contract_version", "")), quote=True),
            html.escape(str(library_version), quote=True),
        )
    )

    out_lines.append('<nav data-piece="%s">' % html.escape(nav_piece["naya_id"], quote=True))
    out_lines.append(stamp_piece(nav_piece["naya_id"], nav_piece["html"]))
    out_lines.append("</nav>")

    for section in sections:
        sid = section.get("section_id", "")
        heading = section.get("heading", "")
        body = section.get("body", "")
        function = section.get("function", "")
        out_lines.append(
            '<section id="%s" class="naya-section" data-function="%s">'
            % (html.escape(str(sid), quote=True), html.escape(str(function), quote=True))
        )
        out_lines.append("<h2>%s</h2>" % html.escape(str(heading), quote=False))
        out_lines.append(render_body(body))
        for nid in section.get("pieces", []):
            out_lines.append(stamp_piece(nid, pieces[nid]["html"]))
        out_lines.append("</section>")

    out_lines.append('<footer data-piece="%s">' % html.escape(footer_piece["naya_id"], quote=True))
    out_lines.append(stamp_piece(footer_piece["naya_id"], footer_piece["html"]))
    out_lines.append("</footer>")

    # 5. FUNCTION MOUNT POINTS: for each activated function, every requires_dom
    #    selector must match an element in the page. Missing mounts get a
    #    deterministic placeholder slot injected here (before the scripts).
    markup = "\n".join(out_lines)
    for entry in activated:
        for selector in entry["requires_dom"]:
            parsed = parse_selector(selector)
            if parsed is None:
                fail_error("functions registry entry %s has an unparseable "
                           "requires_dom selector: %s" % (entry["naya_id"], selector))
            if selector_present(markup, selector):
                continue
            attr, value = parsed
            mount_name = value
            out_lines.append(
                '<section class="naya-fn-slot" id="fn-slot-%s" %s="%s" '
                'data-naya-fn-slot="%s" aria-label="%s">'
                % (
                    html.escape(mount_name, quote=True),
                    html.escape(attr, quote=True),
                    html.escape(value, quote=True),
                    html.escape(entry["naya_id"], quote=True),
                    html.escape(str(entry.get("human_label", entry["naya_id"])), quote=True),
                )
            )
            out_lines.append(
                '<p class="fn-slot-note">%s mounts here.</p>'
                % html.escape(str(entry.get("human_label", entry["naya_id"])), quote=False)
            )
            out_lines.append("</section>")
            markup = "\n".join(out_lines)

    # 6. All scripts live BELOW the markup: wiring may only target DOM that exists.
    #    First the page config, then one stamped script per activated function.
    page_config = {
        "contract_version": contract.get("contract_version"),
        "library_version": library_version,
        "page_slug": page.get("slug"),
        "functions": [e["naya_id"] for e in activated],
        "functions_default": contract.get("functions_default", []),
        "sections": [s.get("section_id") for s in sections],
    }
    out_lines.append("<script>")
    out_lines.append(
        "window.NAYA_PAGE=" + json.dumps(page_config, sort_keys=True, separators=(",", ":")) + ";"
    )
    out_lines.append("</script>")
    for entry in activated:
        out_lines.append('<script data-naya-fn="%s">' % html.escape(entry["naya_id"], quote=True))
        out_lines.append(entry["wiring_js"].rstrip("\n"))
        out_lines.append("</script>")
    out_lines.append("</body>")
    out_lines.append("</html>")

    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out_lines) + "\n")

    sys.stdout.write("assembled: %s (contract %s, library %s, %d sections, %d functions: %s)\n" % (
        args.out, contract.get("contract_version"), library_version, len(sections),
        len(activated), ", ".join(e["naya_id"] for e in activated) or "none"
    ))


if __name__ == "__main__":
    main()
