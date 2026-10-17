#!/usr/bin/env python3
"""Automatic scorecard gate for the Smart Builder pipeline.

Team Nitro, seat LAW/Xi. Rendered page in, verdict out.
9+ ships, below 9 returns the why-not-10 list. No human approval.
Exit codes fail closed:
    0 = SHIP   (score >= 9.0)
    1 = REWORK (score < 9.0, why_not_10 non-empty)
    2 = input error (missing file, bad JSON) -- never score what we can't read.
Stdlib only.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser

SHIP_THRESHOLD = 9.0


# ---------------------------------------------------------------------------
# Page parsing
# ---------------------------------------------------------------------------
class PageParser(HTMLParser):
    """Collects the elements the gate inspects: buttons, anchors, inputs,
    ids, data-naya-piece markers, data-naya-fn script stamps, inline CSS,
    and script text."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.buttons = []      # {attrs, line, in_form}
        self.anchors = []      # {attrs, line}
        self.inputs = []       # {attrs, line, wrapped_in_label}
        self.ids = {}          # id -> tag
        self.pieces = []       # {value, tag, line} for data-naya-piece
        self.fn_scripts = []   # {naya_id, line} for <script data-naya-fn>
        self.styles = []       # css text from <style> blocks
        self.style_attrs = []  # inline style attribute values
        self.scripts = []      # script text
        self.label_fors = []   # label for="..." values
        self._form_depth = 0
        self._label_depth = 0
        self._in_style = False
        self._in_script = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        line = self.getpos()[0]
        if tag == "form":
            self._form_depth += 1
        if tag == "label":
            self._label_depth += 1
            if attrs.get("for"):
                self.label_fors.append(attrs["for"])
        if tag == "button":
            self.buttons.append({"attrs": attrs, "line": line,
                                 "in_form": self._form_depth > 0})
        elif tag == "a":
            self.anchors.append({"attrs": attrs, "line": line})
        elif tag == "input":
            self.inputs.append({"attrs": attrs, "line": line,
                                "wrapped_in_label": self._label_depth > 0})
        if attrs.get("id"):
            self.ids.setdefault(attrs["id"], tag)
        if "data-naya-piece" in attrs:
            self.pieces.append({"value": attrs.get("data-naya-piece") or "",
                                "tag": tag, "line": line})
        if tag == "script" and attrs.get("data-naya-fn"):
            self.fn_scripts.append({"naya_id": attrs["data-naya-fn"],
                                    "line": line})
        if attrs.get("style"):
            self.style_attrs.append(attrs["style"])
        if tag == "style":
            self._in_style = True
        if tag == "script":
            self._in_script = True

    def handle_endtag(self, tag):
        if tag == "form" and self._form_depth > 0:
            self._form_depth -= 1
        if tag == "label" and self._label_depth > 0:
            self._label_depth -= 1
        if tag == "style":
            self._in_style = False
        if tag == "script":
            self._in_script = False

    def handle_data(self, data):
        if self._in_style:
            self.styles.append(data)
        if self._in_script:
            self.scripts.append(data)

    def css_blob(self):
        return "\n".join(self.styles + self.style_attrs)

    def scripts_blob(self):
        return "\n".join(self.scripts)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def describe(tag, attrs, line):
    bits = ["<%s" % tag]
    for key in ("id", "class", "href", "data-naya-piece"):
        if attrs.get(key):
            bits.append('%s="%s"' % (key, attrs[key]))
    return " ".join(bits) + "> (line %d)" % line


def classes_of(attrs):
    return set((attrs.get("class") or "").split())


SELECTOR_RE = re.compile(r"^\[([A-Za-z0-9_-]+)=['\"]([^'\"]*)['\"]\]$")


def parse_selector(selector):
    m = SELECTOR_RE.match(selector.strip())
    return (m.group(1), m.group(2)) if m else None


def selector_present(html_text, selector):
    parsed = parse_selector(selector)
    if parsed is None:
        return False
    attr, value = parsed
    pat = re.compile(r'%s\s*=\s*["\']%s["\']' % (re.escape(attr), re.escape(value)))
    return pat.search(html_text) is not None


def extract_page_config(scripts):
    """Pull the window.NAYA_PAGE JSON object out of the page scripts."""
    m = re.search(r"window\.NAYA_PAGE\s*=\s*(\{.*?\});", scripts, re.DOTALL)
    if not m:
        return {}
    try:
        return json.loads(m.group(1))
    except (json.JSONDecodeError, ValueError):
        return {}


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------
class Scorecard:
    def __init__(self):
        self.why_not_10 = []
        self.deduction_by_check = {"design_laws": 0.0,
                                   "click_everything": 0.0,
                                   "contract_traceability": 0.0,
                                   "functions": 0.0}

    def deduct(self, check, amount, rule, element, detail):
        self.why_not_10.append({"rule": rule, "element": element,
                                "detail": detail, "deduction": amount})
        self.deduction_by_check[check] += amount

    def score(self):
        total = sum(self.deduction_by_check.values())
        return max(0.0, round(10.0 - total, 2))


def _input_error(message):
    """Print an error scorecard and exit 2. Never score what we can't read."""
    print(json.dumps({"score": None, "verdict": "ERROR",
                      "error": message, "why_not_10": []}, indent=2))
    sys.exit(2)


def load_json(path, kind):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        _input_error("%s file not found: %s" % (kind, path))
    except json.JSONDecodeError as exc:
        _input_error("%s is not valid JSON (%s): %s" % (kind, exc, path))
    except OSError as exc:
        _input_error("cannot read %s file %s: %s" % (kind, path, exc))


def normalize_registry(raw):
    """Registry maps naya_id -> piece dict (accepts dict or list form)."""
    pieces = raw.get("pieces", {}) if isinstance(raw, dict) else {}
    if isinstance(pieces, list):
        norm = {}
        for piece in pieces:
            if isinstance(piece, dict) and piece.get("naya_id"):
                norm[piece["naya_id"]] = piece
        return norm
    return pieces if isinstance(pieces, dict) else {}


def normalize_functions_registry(raw):
    """Functions registry maps naya_id -> function dict (list form)."""
    funcs = raw.get("functions", []) if isinstance(raw, dict) else []
    norm = {}
    for fn in funcs:
        if isinstance(fn, dict) and fn.get("naya_id"):
            norm[fn["naya_id"]] = fn
    return norm


def normalize_contract(raw):
    """Contract carries sections: [{section_id, pieces:[...]}]."""
    sections = raw.get("sections", []) if isinstance(raw, dict) else []
    return [s for s in sections if isinstance(s, dict)]


def run_checks(page, contract, registry, html_text, fn_registry):
    card = Scorecard()

    button_piece_classes = set()
    for piece in registry.values():
        if isinstance(piece, dict) and piece.get("category") == "button":
            for cls in piece.get("css_classes", []) or []:
                button_piece_classes.add(cls.lstrip("."))

    css = page.css_blob()
    scripts = page.scripts_blob()

    # -- Check 1: design laws (0.5 per sub-rule, max 2.0) --------------------
    # 1a: every <button> carries .naya-btn or a registry button-piece class.
    for btn in page.buttons:
        cls = classes_of(btn["attrs"])
        if "naya-btn" not in cls and cls.isdisjoint(button_piece_classes):
            card.deduct("design_laws", 0.5, "1a",
                        describe("button", btn["attrs"], btn["line"]),
                        "button lacks .naya-btn or a registry button-piece class")

    # 1b: interactive elements have hover/ignite styling (:hover in page CSS).
    if ":hover" not in css:
        card.deduct("design_laws", 0.5, "1b", "page",
                    "no :hover styling found in page CSS")

    # 1c: reduced-motion media query present.
    if "prefers-reduced-motion" not in css:
        card.deduct("design_laws", 0.5, "1c", "page",
                    "no prefers-reduced-motion media query found")

    # 1d: touch targets -- buttons/inputs declare min-height >= 44px
    #     or carry the ignite class.
    heights = [float(m) for m in
               re.findall(r"min-height\s*:\s*(\d+(?:\.\d+)?)\s*px", css)]
    if not any(h >= 44 for h in heights):
        targets = ([{"tag": "button", "attrs": b["attrs"], "line": b["line"]}
                    for b in page.buttons] +
                   [{"tag": "input", "attrs": i["attrs"], "line": i["line"]}
                    for i in page.inputs])
        for t in targets:
            cls = classes_of(t["attrs"])
            if not any("ignite" in c.lower() for c in cls):
                card.deduct("design_laws", 0.5, "1d",
                            describe(t["tag"], t["attrs"], t["line"]),
                            "touch target has no min-height >= 44px "
                            "and no ignite class")

    # Cap check 1 at 2.0 (four 0.5 sub-rules) and drop entries past the cap.
    capped = []
    running = 0.0
    for entry in card.why_not_10:
        if not entry["rule"].startswith("1"):
            capped.append(entry)
            continue
        if running + 0.5 <= 2.0 + 1e-9:
            running += 0.5
            capped.append(entry)
    card.why_not_10 = capped
    card.deduction_by_check["design_laws"] = round(running, 2)

    # -- Check 2: click-everything function check (1.0/violation, max 3.0) ---
    def wired(btn):
        attrs = btn["attrs"]
        if attrs.get("onclick"):
            return True
        btype = (attrs.get("type") or "").lower()
        # HTML default button type is submit; only counts inside a form.
        if btn["in_form"] and btype in ("", "submit"):
            return True
        if "addEventListener" not in scripts:
            return False
        bid = attrs.get("id", "")
        pats = []
        if bid:
            pats += ["getElementById('%s')" % bid,
                     'getElementById("%s")' % bid, "#%s" % bid]
        for c in classes_of(attrs):
            pats.append(".%s" % c)
        pats += ["querySelector('button')", 'querySelector("button")',
                 "getElementsByTagName('button'",
                 'getElementsByTagName("button"']
        return any(p in scripts for p in pats)

    violations = []
    for btn in page.buttons:
        if not wired(btn):
            violations.append(("2a", describe("button", btn["attrs"], btn["line"]),
                               "button has no onclick, no addEventListener wiring, "
                               "and is not type=submit inside a form"))
    for anc in page.anchors:
        href = (anc["attrs"].get("href") or "").strip()
        if href in ("", "#"):
            violations.append(("2b", describe("a", anc["attrs"], anc["line"]),
                               "dead link: href is empty or '#'"))
    for inp in page.inputs:
        attrs = inp["attrs"]
        labeled = (bool((attrs.get("aria-label") or "").strip())
                   or bool(attrs.get("aria-labelledby"))
                   or inp["wrapped_in_label"]
                   or attrs.get("id") in page.label_fors)
        if not labeled:
            violations.append(("2c", describe("input", attrs, inp["line"]),
                               "input has no associated <label> or aria-label"))
    for rule, element, detail in violations[:3]:
        card.deduct("click_everything", 1.0, rule, element, detail)

    # -- Check 3: contract traceability (1.0/violation, max 3.0) -------------
    tviol = []
    for section in contract:
        sid = section.get("section_id", "")
        if sid and sid not in page.ids:
            tviol.append(("3a", "contract section '%s'" % sid,
                          "section_id '%s' has no matching id in the HTML" % sid))
        for nid in section.get("pieces", []) or section.get("naya_ids", []) or []:
            if nid not in registry:
                tviol.append(("3b", "contract naya_id '%s'" % nid,
                              "naya_id '%s' referenced by the contract is not "
                              "in the registry" % nid))
    for marker in page.pieces:
        if not marker["value"] or marker["value"] not in registry:
            tviol.append(("3c",
                          describe(marker["tag"],
                                   {"data-naya-piece": marker["value"]},
                                   marker["line"]),
                          "data-naya-piece marker '%s' does not resolve to the "
                          "registry -- unstamped/invented markup"
                          % marker["value"]))
    for rule, element, detail in tviol[:3]:
        card.deduct("contract_traceability", 1.0, rule, element, detail)

    # -- Check 4: activated functions (1.0/violation, max 3.0) ---------------
    # Activated function ids come from window.NAYA_PAGE (assembler-written).
    # 4a: wiring script with the data-naya-fn stamp must be present.
    # 4b: every requires_dom selector must match an element in the HTML.
    #     (Checked against the DOM-visible markup only -- script bodies are
    #     stripped, since wiring units quote their own mount selectors.)
    # 4c: activation config must be valid (known id, field 'functions',
    #     default_on boolean, status READY).
    fviol = []
    page_config = extract_page_config(scripts)
    activated = page_config.get("functions") or []
    dom_text = re.sub(r"<script\b[^>]*>.*?</script>", "", html_text,
                      flags=re.DOTALL | re.IGNORECASE)
    stamped = {s["naya_id"] for s in page.fn_scripts}
    for fid in activated:
        if fid not in stamped:
            fviol.append(("4a", "function '%s'" % fid,
                          "activated function has no <script data-naya-fn=\"%s\"> "
                          "wiring unit in the page" % fid))
            continue
        if fn_registry:
            fn = fn_registry.get(fid)
            if fn is None:
                fviol.append(("4c", "function '%s'" % fid,
                              "activated function is not in the functions registry"))
                continue
            act = fn.get("activation") or {}
            if act.get("field") != "functions" or not isinstance(act.get("default_on"), bool):
                fviol.append(("4c", "function '%s'" % fid,
                              "activation config invalid: field must be 'functions' "
                              "and default_on a boolean"))
            elif fn.get("status") != "READY":
                fviol.append(("4c", "function '%s'" % fid,
                              "function status is '%s', not READY -- cannot be activated"
                              % fn.get("status")))
            for selector in fn.get("requires_dom") or []:
                if parse_selector(selector) is None:
                    fviol.append(("4b", "function '%s'" % fid,
                                  "requires_dom selector '%s' is not a simple "
                                  "[attr='value'] selector" % selector))
                elif not selector_present(dom_text, selector):
                    fviol.append(("4b", "function '%s'" % fid,
                                  "requires_dom selector '%s' matches no element "
                                  "in the HTML" % selector))
    for rule, element, detail in fviol[:3]:
        card.deduct("functions", 1.0, rule, element, detail)

    return card


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Automatic scorecard gate: rendered page in, verdict out.")
    ap.add_argument("--html", required=True, help="rendered page to verify")
    ap.add_argument("--contract", required=True,
                    help="page contract JSON (sections + pieces)")
    ap.add_argument("--registry", required=True,
                    help="piece registry JSON (naya_id -> piece)")
    ap.add_argument("--functions-registry", default=None,
                    help="functions registry JSON (naya_id -> function); "
                         "without it, only the wiring-stamp check (4a) runs")
    args = ap.parse_args(argv)

    try:
        with open(args.html, "r", encoding="utf-8") as fh:
            html_text = fh.read()
    except FileNotFoundError:
        _input_error("HTML file not found: %s" % args.html)
    except OSError as exc:
        _input_error("cannot read HTML file %s: %s" % (args.html, exc))

    contract = normalize_contract(load_json(args.contract, "contract"))
    registry = normalize_registry(load_json(args.registry, "registry"))
    fn_registry = (normalize_functions_registry(
        load_json(args.functions_registry, "functions registry"))
        if args.functions_registry else {})

    page = PageParser()
    try:
        page.feed(html_text)
        page.close()
    except Exception as exc:  # fail closed on unparseable input
        _input_error("cannot parse HTML %s: %s" % (args.html, exc))

    card = run_checks(page, contract, registry, html_text, fn_registry)
    score = card.score()
    verdict = "SHIP" if score >= SHIP_THRESHOLD else "REWORK"

    result = {
        "score": score,
        "verdict": verdict,
        "threshold": SHIP_THRESHOLD,
        "why_not_10": card.why_not_10,
        "deductions": {k: round(v, 2)
                       for k, v in card.deduction_by_check.items()},
        "counts": {
            "buttons": len(page.buttons),
            "anchors": len(page.anchors),
            "inputs": len(page.inputs),
            "sections": len(contract),
            "piece_markers": len(page.pieces),
            "function_scripts": len(page.fn_scripts),
        },
    }
    print(json.dumps(result, indent=2))
    sys.exit(0 if score >= SHIP_THRESHOLD else 1)


if __name__ == "__main__":
    main()
