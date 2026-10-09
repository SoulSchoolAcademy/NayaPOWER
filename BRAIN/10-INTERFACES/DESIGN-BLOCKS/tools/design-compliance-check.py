#!/usr/bin/env python3
"""
Naya Design Compliance Checker
==============================
Machine enforcement for "code is law" — scores a built HTML page against the
official Naya Design Smart Blocks library.

The law (from naya-design-catalog.json):
    "If a block exists for the job, use it. Custom CSS for a solved job is a violation."

What this checks (graded 0-10 compliance score):
  1. BLOCK USAGE — which official block selectors appear in the HTML
  2. CUSTOM CSS — <style> rules and inline styles that duplicate official blocks
  3. SCORE — explainable, every deduction named

What this does NOT do (see Naya 5's tools/design_gate.py for the binary gate):
  - It does not FAIL/PASS on structural law (black root, light surfaces, etc.)
  - It GRADES usage: how much of this page is built from official blocks,
    and exactly which custom CSS reinvents a solved job.

Usage:
    python3 tools/design-compliance-check.py <page.html> --receipt <receipt.json> [--catalog PATH] [--json]

STEP 0 — ACTIVATION PRE-GATE (Gap-2 integration):
    The checker REFUSES to score without a valid, current activation receipt.
    No receipt = no score. Not a low score — a refusal. Activation first.

Exit codes: 0 = PASS (score >= 7), 1 = FAIL (score < 7), 2 = usage/tool error,
            3 = ACTIVATION REFUSED (no/invalid/stale activation receipt).
"""

import json
import re
import sys
import os
from html.parser import HTMLParser
from collections import defaultdict

# Activation pre-gate (STEP 0 — runs before any scoring)
try:
    from activation_pregate import gate_or_refuse, ActivationRefused
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from activation_pregate import gate_or_refuse, ActivationRefused

# ---------------------------------------------------------------------------
# Catalog loading
# ---------------------------------------------------------------------------

DEFAULT_CATALOG = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "BRAIN", "10-INTERFACES", "DESIGN-BLOCKS", "naya-design-catalog.json",
)

# Fallback: repo-root relative (when run from a worktree checkout)
FALLBACK_CATALOGS = [
    "BRAIN/10-INTERFACES/DESIGN-BLOCKS/naya-design-catalog.json",
    "../BRAIN/10-INTERFACES/DESIGN-BLOCKS/naya-design-catalog.json",
]


def load_catalog(path=None):
    candidates = []
    if path:
        candidates.append(path)
    candidates.append(DEFAULT_CATALOG)
    candidates.extend(FALLBACK_CATALOGS)
    for c in candidates:
        c = os.path.abspath(c)
        if os.path.exists(c):
            with open(c, encoding="utf-8") as f:
                return json.load(f), c
    raise FileNotFoundError(
        "naya-design-catalog.json not found. Tried: " + ", ".join(candidates)
    )


# ---------------------------------------------------------------------------
# HTML parsing — collect classes used, <style> CSS, inline styles
# ---------------------------------------------------------------------------

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.classes_used = defaultdict(int)   # class name -> count
        self.style_blocks = []                  # raw CSS text
        self.inline_styles = []                 # style="" values
        self._in_style = False
        self._style_buf = []
        self.tag_count = 0
        self.has_doctype = False

    def handle_decl(self, decl):
        if decl.lower().startswith("doctype"):
            self.has_doctype = True

    def handle_starttag(self, tag, attrs):
        self.tag_count += 1
        ad = dict(attrs)
        if tag == "style":
            self._in_style = True
            self._style_buf = []
            return
        cls = ad.get("class", "")
        for c in cls.split():
            self.classes_used[c] += 1
        st = ad.get("style", "")
        if st.strip():
            self.inline_styles.append(st.strip())

    def handle_endtag(self, tag):
        if tag == "style" and self._in_style:
            self._in_style = False
            self.style_blocks.append("".join(self._style_buf))

    def handle_data(self, data):
        if self._in_style:
            self._style_buf.append(data)


# ---------------------------------------------------------------------------
# CSS parsing (lightweight — no external deps; CSS Syntax semantics)
# ---------------------------------------------------------------------------
#
# CLASS-LEVEL RULE: at-rules are parsed as at-rules, never as selector text.
# The old implementation (RULE_RE over "anything before a {", then skipping
# selectors starting with "@") let an at-rule prelude MERGE into the next
# rule's selector — so `@import url(...); .x{...}` dropped `.x` entirely
# (grader-blindness / score inflation). Encoding variants of the same class
# (CSS-escaped at-keywords like `@\69 mport`, comments inside preludes,
# braces inside strings, unterminated comments) broke the string checks too.
#
# This parser tokenizes with browser-equivalent semantics instead:
#   - comments are consumed (unterminated `/*` runs to EOF, like browsers),
#   - strings swallow braces/semicolons/comments inside quotes,
#   - `@keyword prelude;` and `@keyword prelude { ... }` are consumed as
#     at-rules and RECORDED (never merged into a selector),
#   - rules nested in at-rule blocks (e.g. @media) are extracted deliberately,
#   - CSS escapes in at-keywords and selectors are decoded before matching.
# Fail-closed: the parser is total — any input tokenizes without exceptions;
# incomplete constructs are dropped exactly where browsers drop them.

CLASS_RE = re.compile(r"\.([a-zA-Z_][\w-]*)")

_HEX = set("0123456789abcdefABCDEF")


def css_unescape(s):
    """Decode CSS escape sequences (CSS Syntax 3, section 4.3.7)."""
    out = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        i += 1
        if i >= n:
            out.append("\\")
            break
        c2 = s[i]
        if c2 in "\r\n\f":
            # escaped newline: line continuation, contributes nothing
            if c2 == "\r" and i + 1 < n and s[i + 1] == "\n":
                i += 2
            else:
                i += 1
            continue
        if c2 in _HEX:
            j = i
            while j < n and j - i < 6 and s[j] in _HEX:
                j += 1
            code = int(s[i:j], 16)
            if code == 0 or code > 0x10FFFF or 0xD800 <= code <= 0xDFFF:
                code = 0xFFFD
            out.append(chr(code))
            i = j
            # one whitespace char after a hex escape is part of the escape
            if i < n and s[i] in " \t\n\f":
                i += 1
            elif i + 1 < n and s[i] == "\r" and s[i + 1] == "\n":
                i += 2
            continue
        out.append(c2)
        i += 1
    return "".join(out)


# At-rules whose blocks contain style rules (safe to recurse into).
# All other at-rule blocks (@keyframes, @font-face, @page, ...) hold
# non-rule content and are recorded but not descended into.
_RULE_CONTAINER_AT_RULES = frozenset({
    "media", "supports", "container", "layer", "scope", "starting-style",
})


class _CSSParser:
    """Recursive-descent CSS parser. parse() -> (rules, at_rules)."""

    def __init__(self, text):
        self.t = text
        self.n = len(text)

    # -- low-level consumers ------------------------------------------------
    def skip_ws_comments(self, i):
        t = self.t
        while i < self.n:
            c = t[i]
            if c in " \t\n\r\f":
                i += 1
            elif c == "/" and i + 1 < self.n and t[i + 1] == "*":
                end = t.find("*/", i + 2)
                # unterminated comment runs to EOF — browser semantics
                i = self.n if end == -1 else end + 2
            else:
                break
        return i

    def consume_string(self, i):
        """self.t[i] is a quote. Returns index just past the string."""
        t = self.t
        q = t[i]
        i += 1
        while i < self.n:
            c = t[i]
            if c == "\\":
                i += 2
                continue
            if c == q:
                return i + 1
            if c in "\n\r\f":
                return i  # bad string: bail at the newline
            i += 1
        return i  # unterminated string runs to EOF

    def consume_ident(self, i):
        """Consume a CSS ident (escapes allowed). Returns (raw_text, i)."""
        t = self.t
        start = i
        if i < self.n and t[i] == "-":
            i += 1
        while i < self.n:
            c = t[i]
            if c.isalnum() or c in "-_":
                i += 1
            elif (c == "\\" and i + 1 < self.n
                    and t[i + 1] not in "\n\r\f"):
                i += 2
                if t[i - 1] in _HEX:
                    k = i
                    while k < self.n and k - i < 5 and t[k] in _HEX:
                        k += 1
                    i = k
                    if i < self.n and t[i] in " \t\n\f":
                        i += 1
                    elif (i + 1 < self.n and t[i] == "\r"
                            and t[i + 1] == "\n"):
                        i += 2
            else:
                break
        return t[start:i], i

    def consume_prelude(self, i):
        """Consume until `;`, `{`, `}` or EOF. Returns (text, i, terminator).

        Comments are semantically nothing and are excluded from the text.
        """
        t = self.t
        parts = []
        start = i
        while i < self.n:
            c = t[i]
            if c in "\"'":
                i = self.consume_string(i)
                continue
            if c == "/" and i + 1 < self.n and t[i + 1] == "*":
                parts.append(t[start:i])
                i = self.skip_ws_comments(i)  # comments vanish (semantically)
                start = i
                continue
            if c in ";{}":
                parts.append(t[start:i])
                return "".join(parts), i + 1 if c == ";" else i, c
            i += 1
        parts.append(t[start:i])
        return "".join(parts), i, None

    def consume_block(self, i):
        """self.t[i] == '{'. Returns (inner_text, i_after_closing_brace)."""
        t = self.t
        assert t[i] == "{"
        start = i
        depth = 0
        while i < self.n:
            c = t[i]
            if c in "\"'":
                i = self.consume_string(i)
                continue
            if c == "/" and i + 1 < self.n and t[i + 1] == "*":
                i = self.skip_ws_comments(i)
                continue
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return t[start + 1:i], i + 1
            i += 1
        return t[start + 1:], self.n  # unterminated block runs to EOF

    # -- grammar ------------------------------------------------------------
    def parse_into(self, rules, at_rules):
        i = self.skip_ws_comments(0)
        t = self.t
        while i < self.n:
            c = t[i]
            if c == "}":
                i = self.skip_ws_comments(i + 1)  # stray close: skip
                continue
            if c == "@":
                j = self.skip_ws_comments(i + 1)  # comments may sit between
                raw, j = self.consume_ident(j)    # '@' and the keyword
                if not raw:
                    i = self.skip_ws_comments(i + 1)  # lone '@': skip
                    continue
                name = css_unescape(raw).lower()
                prelude, i, term = self.consume_prelude(j)
                prelude = prelude.strip()
                if term == ";":
                    at_rules.append((name, prelude))
                elif term == "{":
                    inner, i = self.consume_block(i)
                    at_rules.append((name, prelude))
                    # rules nested in grouping at-rules are real rules:
                    # extract deliberately, never merge, never swallow
                    if name in _RULE_CONTAINER_AT_RULES:
                        _CSSParser(inner).parse_into(rules, at_rules)
                else:
                    # EOF or stray '}': record the at-rule, drop the rest
                    at_rules.append((name, prelude))
                    if term == "}":
                        pass  # leave '}' for the main loop to skip
                i = self.skip_ws_comments(i)
                continue
            prelude, i, term = self.consume_prelude(i)
            if term == "{":
                inner, i = self.consume_block(i)
                sel = css_unescape(prelude).strip()
                decl = inner.strip()
                if sel and decl:
                    rules.append((sel, decl))
            # `;`, `}`, EOF: prelude without a block is not a rule — drop
            i = self.skip_ws_comments(i)


def parse_stylesheet(css_text):
    """Parse CSS into (rules, at_rules).

    rules:    [(selector_text, declarations_text)] — escapes decoded.
    at_rules: [(name, prelude)] — name lowercased, escapes decoded;
              recorded at the delivery boundary instead of silently swallowed.
    """
    rules, at_rules = [], []
    _CSSParser(css_text).parse_into(rules, at_rules)
    return rules, at_rules


def extract_rules(css_text):
    """Yield (selector_text, declarations_text) for each rule."""
    rules, _ = parse_stylesheet(css_text)
    for sel, decl in rules:
        yield sel, decl


def classes_in_selector(selector):
    return set(CLASS_RE.findall(selector))


# ---------------------------------------------------------------------------
# Job inference — guess what a custom class is FOR, to match against blocks
# ---------------------------------------------------------------------------
# Maps lowercase name fragments -> canonical job keywords that appear in the
# catalog's tags/job/when_to_use fields.

JOB_HINTS = [
    (("btn", "button"), ["button"]),
    (("card",), ["card"]),
    (("modal", "dialog", "popup"), ["modal", "dialog", "overlay"]),
    (("toast", "snackbar"), ["toast", "notification"]),
    (("tab",), ["tab"]),
    (("nav", "navbar", "menu"), ["nav", "navigation", "menu"]),
    (("hero",), ["hero"]),
    (("badge", "pill", "chip", "tag"), ["badge", "pill", "chip"]),
    (("input", "field", "textarea", "select"), ["input", "field", "form"]),
    (("toggle", "switch"), ["toggle", "switch"]),
    (("slider", "carousel"), ["carousel", "slider"]),
    (("avatar",), ["avatar"]),
    (("tooltip",), ["tooltip"]),
    (("accordion", "collapse"), ["accordion"]),
    (("dropdown", "select-menu"), ["dropdown", "select"]),
    (("progress", "meter", "bar"), ["progress"]),
    (("spinner", "loader", "skeleton", "shimmer"), ["loading", "skeleton", "spinner"]),
    (("table",), ["table", "data"]),
    (("chart", "graph"), ["chart", "graph"]),
    (("feed", "stream", "timeline"), ["feed", "stream", "activity"]),
    (("chat", "message", "bubble"), ["chat", "message"]),
    (("drawer", "sidebar", "panel"), ["drawer", "panel"]),
    (("fab",), ["fab", "button"]),
    (("breadcrumb",), ["breadcrumb"]),
    (("pagination", "pager"), ["pagination"]),
    (("stepper", "wizard", "steps"), ["stepper", "wizard"]),
    (("rating", "stars"), ["rating"]),
    (("search",), ["search"]),
    (("header", "topbar"), ["header", "chrome"]),
    (("footer",), ["footer"]),
    (("jewel", "orb", "gem"), ["jewel", "orb"]),
    (("quote", "testimonial"), ["quote", "testimonial"]),
    (("price", "pricing", "plan"), ["pricing"]),
    (("banner", "alert"), ["banner", "alert"]),
    (("empty", "placeholder"), ["empty"]),
]


def infer_jobs(class_name):
    """Return a set of job keywords inferred from a custom class name."""
    name = class_name.lower()
    jobs = set()
    for fragments, keywords in JOB_HINTS:
        if any(f in name for f in fragments):
            jobs.update(keywords)
    return jobs


def block_covers_job(block, job_keywords):
    """True if the block's tags/job/when_to_use mention any of the keywords."""
    text = " ".join([
        block.get("job", ""),
        block.get("when_to_use", ""),
        " ".join(block.get("tags", [])),
        block.get("name", ""),
    ]).lower()
    return any(kw in text for kw in job_keywords)


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------

def normalize_selector(sel):
    """' .answer .jewel ' -> 'answer'; '.naya-btn.primary' -> 'naya-btn'."""
    sel = sel.strip().lstrip(".")
    # take first class token before any combinator/pseudo/extra class
    m = re.match(r"([a-zA-Z_][\w-]*)", sel)
    return m.group(1) if m else sel


def analyze(page_html, catalog):
    blocks = catalog["blocks"]

    # Index: class name -> block ids that claim it
    class_to_blocks = defaultdict(list)
    for b in blocks:
        for sel in b.get("selectors", []):
            cls = normalize_selector(sel)
            if cls:
                class_to_blocks[cls].append(b["id"])

    parser = PageParser()
    parser.feed(page_html)

    used_classes = set(parser.classes_used.keys())

    # --- 1. Block usage ---
    blocks_used = {}
    for cls in used_classes:
        for bid in class_to_blocks.get(cls, []):
            blocks_used.setdefault(bid, set()).add(cls)

    block_index = {b["id"]: b for b in blocks}
    categories_used = sorted({block_index[bid]["category"] for bid in blocks_used})

    # --- 2. Custom CSS ---
    # A "custom class" = appears in the page's own <style> but is not an
    # official block selector class.
    official_classes = set(class_to_blocks.keys())
    custom_rules = []  # (selector, declarations, classes)
    # Delivery boundary: every <style> block is parsed with full at-rule
    # semantics. At-rules (esp. @import) are RECORDED, never silently
    # swallowed — absence of the class in the report is the cheapest exploit.
    at_rules_seen = []  # (name, prelude), deduplicated, in order
    for css in parser.style_blocks:
        rules, at_rules = parse_stylesheet(css)
        for name, prelude in at_rules:
            if (name, prelude) not in at_rules_seen:
                at_rules_seen.append((name, prelude))
        for sel, decl in rules:
            sel_classes = classes_in_selector(sel)
            # skip rules that only target official classes or elements
            custom_in_rule = sel_classes - official_classes
            if custom_in_rule and decl.strip():
                custom_rules.append((sel, decl, custom_in_rule))

    # Also: classes used in HTML but defined nowhere (neither official nor
    # in <style>) — likely utility/framework classes; note but don't penalize.
    defined_custom = set()
    for _, _, cc in custom_rules:
        defined_custom |= cc
    undefined_classes = {
        c for c in used_classes
        if c not in official_classes and c not in defined_custom
    }

    # --- 3. Duplication flags: custom class whose inferred job is covered ---
    flags = []
    for sel, decl, sel_classes in custom_rules:
        for cls in sel_classes:
            jobs = infer_jobs(cls)
            if not jobs:
                continue
            covering = [
                b["id"] for b in blocks
                if b["id"] not in blocks_used and block_covers_job(b, jobs)
            ]
            # Only flag when the page does NOT already use a covering block
            # (using both = worst: reinvented AND ignored the official one)
            if covering:
                # Heuristic strength: how "component-like" is the rule?
                decl_l = decl.lower()
                component_signals = sum([
                    "border-radius" in decl_l,
                    "box-shadow" in decl_l,
                    "background" in decl_l,
                    "padding" in decl_l,
                    "display" in decl_l,
                    ":hover" in sel,
                ])
                flags.append({
                    "custom_class": cls,
                    "selector": sel,
                    "inferred_job": sorted(jobs),
                    "use_instead": covering[:3],
                    "component_signals": component_signals,
                })

    # Deduplicate flags by custom class (keep strongest)
    best = {}
    for f in flags:
        c = f["custom_class"]
        if c not in best or f["component_signals"] > best[c]["component_signals"]:
            best[c] = f
    flags = sorted(best.values(),
                   key=lambda f: -f["component_signals"])

    # --- 4. Scoring (0-10, explainable) ---
    deductions = []
    score = 10.0

    # 4a. Custom components duplicating official blocks: -1.5 each (cap -6)
    dup_penalty = min(6.0, 1.5 * len(flags))
    if dup_penalty:
        deductions.append({
            "points": -dup_penalty,
            "reason": f"{len(flags)} custom component(s) duplicate official blocks",
            "detail": [f".{f['custom_class']} -> use {', '.join(f['use_instead'])}"
                       for f in flags],
        })
        score -= dup_penalty

    # 4b. Custom CSS volume vs block usage (reinvention ratio)
    n_custom_rules = len(custom_rules)
    n_blocks = len(blocks_used)
    if n_custom_rules > 0 and n_blocks == 0:
        deductions.append({
            "points": -3.0,
            "reason": "page defines custom component CSS but uses zero official blocks",
            "detail": [f"{n_custom_rules} custom rule(s), 0 blocks"],
        })
        score -= 3.0
    elif n_custom_rules > 3 * max(n_blocks, 1) and n_blocks > 0:
        deductions.append({
            "points": -1.0,
            "reason": "custom CSS volume dwarfs block usage",
            "detail": [f"{n_custom_rules} custom rules vs {n_blocks} blocks used"],
        })
        score -= 1.0

    # 4c. Inline styles doing component work (each distinct heavy one -0.5, cap -2)
    heavy_inline = [s for s in parser.inline_styles
                    if len(s) > 60 and any(k in s.lower() for k in
                                           ("border-radius", "box-shadow", "background"))]
    inline_penalty = min(2.0, 0.5 * len(heavy_inline))
    if inline_penalty:
        deductions.append({
            "points": -inline_penalty,
            "reason": f"{len(heavy_inline)} heavy inline style(s) doing component work",
            "detail": heavy_inline[:3],
        })
        score -= inline_penalty

    # 4d. External @import: rules the grader cannot see (fail closed on the
    # whole class — an @import of a custom stylesheet is custom CSS whose
    # duplication status is UNKNOWN, not "clean"). One bounded deduction.
    imports = [p for n, p in at_rules_seen if n == "import"]
    if imports:
        deductions.append({
            "points": -1.0,
            "reason": (f"{len(imports)} external stylesheet(s) via @import — "
                       "their rules are outside the grader's view; "
                       "duplication unverifiable"),
            "detail": [f"@import {p}" for p in imports[:5]],
        })
        score -= 1.0

    score = max(0.0, round(score, 1))
    verdict = "PASS" if score >= 7 else "FAIL"

    return {
        "score": score,
        "verdict": verdict,
        "blocks_used": [
            {"id": bid,
             "category": block_index[bid]["category"],
             "name": block_index[bid]["name"],
             "matched_classes": sorted(blocks_used[bid])}
            for bid in sorted(blocks_used)
        ],
        "categories_used": categories_used,
        "num_blocks_used": len(blocks_used),
        "custom_rules": [
            {"selector": sel, "classes": sorted(cc)}
            for sel, _, cc in custom_rules
        ],
        "num_custom_rules": n_custom_rules,
        "duplication_flags": flags,
        "deductions": deductions,
        "at_rules": [
            {"name": n, "prelude": p} for n, p in at_rules_seen
        ],
        "num_at_rules": len(at_rules_seen),
        "notes": sorted(undefined_classes)[:20],
        "stats": {
            "total_classes_in_html": len(used_classes),
            "official_classes_matched": len(used_classes & official_classes),
            "tags_in_page": parser.tag_count,
        },
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def human_summary(result, page_name):
    L = []
    L.append(f"Naya Design compliance: {page_name}")
    L.append(f"Score: {result['score']}/10 — {result['verdict']}")
    L.append("")
    L.append(f"Official blocks used: {result['num_blocks_used']} "
             f"({', '.join(result['categories_used']) or 'none'})")
    for b in result["blocks_used"]:
        L.append(f"  ✓ {b['id']} [{b['category']}] — {b['name']}")
    L.append("")
    L.append(f"Custom CSS rules: {result['num_custom_rules']}")
    if result["duplication_flags"]:
        L.append("Duplication flags (custom CSS reinventing official blocks):")
        for f in result["duplication_flags"]:
            L.append(f"  ✗ .{f['custom_class']} (job: {', '.join(f['inferred_job'])}) "
                     f"-> use: {', '.join(f['use_instead'])}")
    else:
        L.append("Duplication flags: none")
    L.append("")
    if result.get("at_rules"):
        L.append("At-rules seen (parsed, not merged into selectors):")
        for a in result["at_rules"]:
            L.append(f"  @ {a['name']} {a['prelude']}".rstrip())
        L.append("")
    if result["deductions"]:
        L.append("Deductions:")
        for d in result["deductions"]:
            L.append(f"  {d['points']:+g} — {d['reason']}")
    else:
        L.append("Deductions: none — clean.")
    if result["verdict"] == "FAIL":
        L.append("")
        L.append("Verdict: FAIL — rebuild from official blocks before delivery.")
        L.append("Law: if a block exists for the job, use it. "
                 "Custom CSS for a solved job is a violation.")
    else:
        L.append("")
        L.append("Verdict: PASS — Naya Design compliant.")
    return "\n".join(L)


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__.strip().split("\n\n")[0])
        print("Usage: python3 tools/design-compliance-check.py <page.html> --receipt <receipt.json> [--json] [--catalog PATH]")
        print("")
        print("STEP 0 — ACTIVATION PRE-GATE: --receipt is REQUIRED.")
        print("Without a valid, current activation receipt the checker REFUSES")
        print("to score (exit 3). Activation first.")
        return 2
    page_path = argv[1]
    as_json = "--json" in argv
    catalog_path = None
    receipt_path = None
    if "--catalog" in argv:
        i = argv.index("--catalog")
        if i + 1 < len(argv):
            catalog_path = argv[i + 1]
    if "--receipt" in argv:
        i = argv.index("--receipt")
        if i + 1 < len(argv):
            receipt_path = argv[i + 1]

    # --- STEP 0: ACTIVATION PRE-GATE (runs before anything else) ---
    if not receipt_path:
        print("ACTIVATION REFUSED: no --receipt provided.", file=sys.stderr)
        print("The checker does not score work from an unactivated Naya.", file=sys.stderr)
        print("Activate first, then re-run with --receipt <receipt.json>.", file=sys.stderr)
        return 3

    try:
        catalog, used_catalog = load_catalog(catalog_path)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    try:
        with open(page_path, encoding="utf-8") as f:
            html = f.read()
    except OSError as e:
        print(f"ERROR: cannot read {page_path}: {e}", file=sys.stderr)
        return 2

    # Verify activation against independently-fetched trusted state.
    # Any failure -> REFUSE (exit 3), never a score.
    try:
        receipt_digest = gate_or_refuse(receipt_path, html)
    except ActivationRefused as e:
        print(f"ACTIVATION REFUSED: {', '.join(e.violations)}", file=sys.stderr)
        print("The checker does not score work without valid activation.", file=sys.stderr)
        return 3

    result = analyze(html, catalog)
    result["page"] = page_path
    result["catalog"] = used_catalog
    result["catalog_blocks"] = catalog["total_blocks"]
    result["activation_receipt_sha256"] = receipt_digest
    result["activation"] = "VERIFIED"

    if as_json:
        print(json.dumps(result, indent=2))
    else:
        print(human_summary(result, page_path))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
