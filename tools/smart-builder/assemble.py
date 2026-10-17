#!/usr/bin/env python3
"""
Smart Builder ASSEMBLER (Team Nitro, seat BUILD/Nu).

Contract data + library version in, finished HTML out.
Deterministic: same inputs -> same bytes, every time. Stdlib only.

Usage:
    python3 assemble.py --contract page.contract.json --registry registry.json \
        --out page.html [--tokens tokens.css]

Exit codes:
    0  assembled OK
    1  usage / structural error (bad JSON, missing required blocks)
    2  GAP: a referenced piece (or the nav/footer slot) has no registry entry.
       The assembler NEVER improvises a piece.

Determinism contract:
    - section order is exactly contract order (json preserves document order)
    - no timestamps, no randomness, no environment reads
    - the only JSON serialization is the page config with sort_keys=True
    - no set/dict iteration that can vary run to run (registry lookup only)
"""
import argparse
import html
import json
import re
import sys

GAP_EXIT = 2


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


def main():
    ap = argparse.ArgumentParser(
        description="Smart Builder assembler: page contract + piece registry -> HTML."
    )
    ap.add_argument("--contract", required=True, help="page-contract JSON file")
    ap.add_argument("--registry", required=True, help="piece registry JSON file")
    ap.add_argument("--out", required=True, help="output HTML file")
    ap.add_argument("--tokens", default=None, help="optional CSS file with design tokens to inline")
    args = ap.parse_args()

    contract = load_json(args.contract, "contract")
    registry = load_json(args.registry, "registry")

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

    # 3. Token CSS: inlined from --tokens, else a placeholder comment.
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

    # All scripts live BELOW the markup: wiring may only target DOM that exists.
    page_config = {
        "contract_version": contract.get("contract_version"),
        "library_version": library_version,
        "page_slug": page.get("slug"),
        "functions_default": contract.get("functions_default", []),
        "sections": [s.get("section_id") for s in sections],
    }
    out_lines.append("<script>")
    out_lines.append(
        "window.NAYA_PAGE=" + json.dumps(page_config, sort_keys=True, separators=(",", ":")) + ";"
    )
    out_lines.append("</script>")
    out_lines.append("</body>")
    out_lines.append("</html>")

    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out_lines) + "\n")

    sys.stdout.write("assembled: %s (contract %s, library %s, %d sections)\n" % (
        args.out, contract.get("contract_version"), library_version, len(sections)
    ))


if __name__ == "__main__":
    main()
