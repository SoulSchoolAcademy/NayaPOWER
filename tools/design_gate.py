#!/usr/bin/env python3
"""NayaNET design gate — code is law, machine-forced.

Usage:
    python3 tools/design_gate.py <page.html> [--manifest smart-blocks/manifest.json]
    python3 tools/design_gate.py <page.html> --require-activation --receipt=<receipt.json>

Enforces the STRUCTURAL design laws from DESIGN-LAWS.md as a hard gate.
Exit 0 = pass. Exit 1 = fail, with each violation named specifically.
Eye-enforced laws (craft, copy, motion meaning) remain Shawn's verdict —
this gate catches what a machine can prove.

With --require-activation, the gate also rejects deliverables with no, stale,
or mismatched activation citation (Naya 3's Gap 2, PR #1974). The citation
marker <!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> --> must match the sha256
of the exact receipt bytes, and the receipt must be fresh (<4h). Deep
verification against live GitHub state is Naya 3's checker in CI.

Structural checks:
  1. SELF-CONTAINED — no external stylesheet/script references (all inlined).
  2. BLACK ROOT — html/body background is deep black.
  3. NO LIGHT SURFACES — no white/light background declarations.
  4. DARK COLOR-SCHEME — meta or CSS declares dark.
  5. NO FREESTYLE COMPONENTS — every Naya-prefixed class exists in the manifest.
  6. LIGHT TEXT — body text color is light.
  7. MOBILE VIEWPORT — the viewport meta declares width=device-width
     (mobile is the primary canvas).

Normalization architecture (durable law, validator 2026-10-09): every
parser is only as strong as the narrowest input channel it doesn't read.
So there is ONE scanned CSS stream — <style> blocks AND inline style
attributes concatenated — punctuation is stripped before every color
lookup, and cascade winners are judged (inline beats stylesheet,
!important beats normal, later beats earlier), never first declarations.

Encoding normalization (extended law, validator 2026-10-09 round 3):
every parser is only as strong as the narrowest ENCODING it doesn't
decode. Browsers decode HTML entities in style ATTRIBUTE values (but
never inside <style> blocks — raw text elements), strip CSS /* */
comments, and decode CSS \\XX escapes before color lookup. The gate's
normalization layer does exactly the same, in the same order:
unescape (attributes only) -> strip comments -> decode escapes.
Fail direction is fail-closed: an encoding the layer cannot resolve
leaves the value unjudgeable, and unjudgeable is not-dark.

Fail direction: black-root judging is fail-CLOSED (an unjudgeable color
cannot be verified dark); light-surface judging is fail-OPEN on images
only (a url() cannot be judged without fetching — honest, not a hole).

Alpha judgment: alpha is composited over the black ground. A 5% white
sheen over black is visually black (passes); a 90% white overlay is
visually white (fails). The gate enforces the rendered result on Shawn's
black canvas, not raw channel values.
"""
from __future__ import annotations

import hashlib
import html as _ihtml
import json
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def read_page(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# CLASS 1 — quote-tolerant attribute parsing (validator round 2 lineage,
# restored in round 4: the repairs3 fork silently lost it, reopening the
# unquoted-attribute rows).
# One tokenizer for every tag scan (rel, href, src, name, content, style).
# Handles double-quoted, single-quoted, and unquoted values per the HTML
# spec (an unquoted value ends at whitespace or `>`). Duplicate attributes:
# the FIRST wins (HTML spec — the parser drops later duplicates), so
# `<div style="background:white" style="background:black">` is judged on
# the white the browser actually applies.
# ---------------------------------------------------------------------------
_ATTR_RE = re.compile(r"""
    (?P<name>[^\s"'`>/=]+)
    (?:\s*=\s*
        (?:"(?P<dq>[^"]*)"
         |'(?P<sq>[^']*)'
         |(?P<uq>[^\s"'`>]+))
    )?""", re.X)


def _parse_attrs(tag: str) -> dict[str, str | None]:
    """Parse a tag's attributes, tolerating every quote form. First wins."""
    attrs: dict[str, str | None] = {}
    inner = re.sub(r"^<\s*/?\s*[a-zA-Z][a-zA-Z0-9]*", "", tag)
    inner = inner.rsplit(">", 1)[0]
    for m in _ATTR_RE.finditer(inner):
        name = m.group("name").lower()
        if name in attrs:
            continue  # duplicate attribute: first wins (HTML spec)
        val = m.group("dq")
        if val is None:
            val = m.group("sq")
        if val is None:
            val = m.group("uq")
        attrs[name] = val
    return attrs


def _tag_open_end(html: str, i: int) -> int | None:
    """Index just past the `>` that closes the tag whose `<name` opener
    ends at i. Quoted attribute values are respected — a `>` inside
    quotes does not end the tag — so `<body title="x>y"
    style="color:#111">` scans to its TRUE end. Returns None when the
    tag is unterminated (fail closed: no extent, no attributes read)."""
    n = len(html)
    while i < n:
        ch = html[i]
        if ch in "\"'":
            quote = ch
            i += 1
            while i < n and html[i] != quote:
                i += 1
            i += 1  # past the closing quote (or past EOF)
        elif ch == ">":
            return i + 1
        else:
            i += 1
    return None


class _TagMatch:
    """Minimal re.Match stand-in for the quote-aware tag scanners.

    `_find_tags` / `_all_tags` historically returned re.finditer matches
    and every caller reads only m.group(0) (group(1) is the tag name on
    _all_tags). The old `[^>]*>` regexes could not express "respect
    quotes", so the scanners below find the tag's TRUE extent instead."""
    __slots__ = ("_text", "_name")

    def __init__(self, text: str, name: str | None):
        self._text = text
        self._name = name

    def group(self, n: int = 0) -> str | None:
        if n == 0:
            return self._text
        if n == 1:
            return self._name
        raise IndexError(f"no such group: {n}")


def _iter_tag_matches(html: str, name_pat: str):
    """Yield a _TagMatch per opening tag whose name matches name_pat,
    each carrying the tag's TRUE extent (Port A, validator round 5,
    C1). Unterminated tags are skipped — fail closed."""
    for m in re.finditer(r"<(%s)\b" % name_pat, html, re.I):
        end = _tag_open_end(html, m.end())
        if end is None:
            continue
        yield _TagMatch(html[m.start():end], m.group(1))


def _tag_extent(html: str, tag: str) -> str | None:
    """Raw text of the first <tag ...> opening tag, with the tag's TRUE
    extent: quoted attribute values are respected, so a `>` inside quotes
    does not end the tag early.

    (Ported from the repairs5 line: validator round 5, C1. R4's
    `<%s\\b[^>]*>` prefix could not cross a `>` inside a quoted
    attribute value — `<body title="x>y" style="color:#111">` made the
    cascade path judge the stylesheet while the browser rendered the
    inline style.) Returns None when there is no <tag or the tag is
    unterminated — fail closed, no style extracted."""
    for tm in _iter_tag_matches(html, re.escape(tag)):
        return tm.group(0)
    return None


def _find_tags(html: str, name: str):
    return _iter_tag_matches(html, re.escape(name))


_style_close_re = re.compile(r"</style>", re.I)


def _style_blocks(html: str):
    """Raw text of every <style>...</style> block (Port A, C1).

    The opener is scanned with its TRUE extent via _tag_open_end — a `>`
    inside a quoted attribute value does not end the tag, so
    `<style title="a>b">` is one tag whose content starts after the real
    `>`. Content is captured to the first `</style>` (case-insensitive),
    exactly as the old `<style[^>]*>(.*?)</style>` regex captured it.
    Name matching is the old regex's `<style` prefix (no `\\b`), so
    `<stylefoo>` behaves exactly as before — the only inputs whose
    treatment changes are openers with a quoted `>`.

    Why it exists: the naive opener regex ended the tag at a quoted `>`,
    leaving a stray `"` in the captured text; _normalize_css_block's
    string neutralizer then read it as an unterminated string and
    swallowed the payload — the whole CSS channel went blind while the
    browser applied the stylesheet (`<style title="a>b">` with hostile
    CSS passed the gate).

    Fail closed: unterminated openers and unclosed blocks yield nothing."""
    for m in re.finditer(r"<style", html, re.I):
        open_end = _tag_open_end(html, m.end())
        if open_end is None:
            continue
        close = _style_close_re.search(html, open_end)
        if close is None:
            continue
        yield html[open_end:close.start()]


def _all_tags(html: str):
    return _iter_tag_matches(html, r"[a-zA-Z][a-zA-Z0-9]*")


def _strip_inert_html(html: str) -> str:
    """Remove markup the browser never renders: HTML comments and
    <template> contents. A <style> or <script src> inside a comment is
    inert — judging/flagging it is an over-block (validator round 4,
    hole 8). The activation marker is itself a comment: run_gate passes
    RAW html to check_activation, stripped html to everything else."""
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    html = re.sub(r"<template\b[^>]*>.*?</template\s*>", "", html,
                  flags=re.S | re.I)
    return html


def _skip_css_string(text: str, i: int) -> int:
    """Index just past the string literal starting at text[i] (a quote).
    Escape-aware; an unterminated string consumes to end of input."""
    n = len(text)
    q = text[i]
    i += 1
    while i < n:
        c = text[i]
        if c == "\\" and i + 1 < n:
            i += 2
            continue
        i += 1
        if c == q:
            break
    return i


def _neutralize_css_strings(text: str) -> str:
    """Replace CSS string literal CONTENTS with the empty string, keeping
    the quotes. Strings are never colors and never declarations — but an
    unbalanced `}` or `;` inside one breaks the rule-iterator's brace
    pairing: `style="content:'}';background:white"` smuggled the white
    into selector-position text, unjudged (validator round 4, hole 2).
    Neutralizing first makes the `*[inline]{...}` wrapper injection-proof
    at the class level. Escape-aware so `\\"` can't end the literal early;
    an unterminated string consumes to end of input (fail-closed)."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch in "\"'":
            out.append(ch)
            i = _skip_css_string(text, i)
            out.append(ch)
        else:
            out.append(ch)
            i += 1
    return "".join(out)


# --- encoding normalization (validator round 3, 2026-10-09) ---
# Browsers decode three encodings before a color is ever judged:
#   1. HTML entities in style ATTRIBUTE values (&#119; -> w). Never inside
#      <style> blocks — those are raw text elements, entities stay raw.
#   2. CSS /* */ comments (stripped). An unclosed comment swallows the rest
#      of the input per CSS Syntax — the gate drops it too (fail-closed).
#   3. CSS \XX escapes (\69<space> -> i, \<newline> -> line continuation).
# The gate normalizes in browser order: unescape (attributes only),
# then strip comments, then decode escapes.

_CSS_ESCAPE_RE = re.compile(
    r"\\([0-9a-fA-F]{1,6})[ \t\n\r\f]?|\\(\r\n|[\n\r\f])|\\(.)", re.S)


def _decode_css_escapes(text: str) -> str:
    """Decode CSS escape sequences the way a browser's CSS parser does.

    \\<1-6 hex digits> + one optional whitespace (consumed) -> the code
    point; \\<newline> -> line continuation (removed); \\<any other char>
    -> that char. Invalid code points become U+FFFD, never a crash."""
    def repl(m: re.Match) -> str:
        if m.group(1) is not None:
            code = int(m.group(1), 16)
            if code == 0 or code > 0x10FFFF or 0xD800 <= code <= 0xDFFF:
                return "\uFFFD"
            return chr(code)
        if m.group(2) is not None:
            return ""  # line continuation
        return m.group(3)
    return _CSS_ESCAPE_RE.sub(repl, text)


def _read_css_ident(text: str, i: int) -> tuple[str, int]:
    """Read a CSS ident starting at text[i], decoding \\ escapes the way
    the browser's tokenizer does ("consume a name"). Returns
    (decoded_name, end_index). A backslash-newline is NOT a valid escape,
    so the ident ends there — exactly like the browser.

    (Ported from the repairs5 line: validator round 5, S3. Needed by
    _match_url_opener so an escape-forged opener like \\75rl( is
    recognized as the url token the browser sees.)"""
    n = len(text)
    name: list[str] = []
    j = i
    while j < n:
        c = text[j]
        if c == "\\":
            if j + 1 >= n or text[j + 1] in "\r\n\f":
                break  # not a valid escape: the ident ends here
            k = j + 1
            hex_digits: list[str] = []
            while k < n and len(hex_digits) < 6 and \
                    text[k] in "0123456789abcdefABCDEF":
                hex_digits.append(text[k])
                k += 1
            if hex_digits:
                if k < n and text[k] in " \t\n\r\f":
                    k += 1  # one whitespace consumed after a hex escape
                code = int("".join(hex_digits), 16)
                if code == 0 or code > 0x10FFFF or 0xD800 <= code <= 0xDFFF:
                    code = 0xFFFD
                name.append(chr(code))
                j = k
            else:
                name.append(text[k])
                j = k + 1
        elif c.isalnum() or c in "-_" or ord(c) >= 0x80:
            name.append(c)
            j += 1
        else:
            break
    return "".join(name), j


def _match_url_opener(text: str, i: int) -> int:
    """If a CSS url( token opener starts at text[i], return the index just
    past the '('. Otherwise return -1.

    (Ported from the repairs5 line: validator round 5, S3.) Per CSS
    Syntax ("consume an ident-like token"), the browser creates a url
    token when the ident-like token's name is an ASCII case-insensitive
    match for "url" and the next code point is '('. Ident consumption
    decodes \\ escapes — so \\75rl( is a url token to the browser, and
    /* inside it is literal. This matcher reads the ident with the same
    escape decoding, so the gate's map matches the browser's territory
    exactly.

    What must NOT match (browser agrees):
      - `url (` with a space: a FUNCTION token — its contents ARE
        comment-scanned, so the stripper must treat them normally.
      - `xurl(` / `-url(`: different idents (preceding-char guard).
      - an escape that starts before i (backslash-parity guard): the
        ident started earlier, e.g. the `\\` in `a\\75rl(`.
      - a literal backslash immediately before i: `\\\\75rl(` decodes to
        ident `\\75rl` (literal backslash in the name), a function token.
    """
    n = len(text)
    if i > 0:
        # Backslash parity: an odd run means text[i] is inside an escape
        # that started before i — the ident started earlier.
        bs = 0
        j = i - 1
        while j >= 0 and text[j] == "\\":
            bs += 1
            j -= 1
        if bs % 2 == 1:
            return -1
        prev = text[i - 1]
        if prev.isalnum() or prev in "-_\\" or ord(prev) >= 0x80:
            return -1
    # Only 'u'/'U'/backslash can begin an ident that decodes to "url".
    if text[i] not in "uU\\":
        return -1
    name, j = _read_css_ident(text, i)
    if name.lower() == "url" and j < n and text[j] == "(":
        return j + 1
    return -1


def _strip_css_comments(text: str) -> str:
    """Strip CSS /* */ comments from the scanned stream — STRING-AWARE
    and URL-AWARE.

    CSS tokenizes strings BEFORE comments: `content:"/*"` is a STRING
    token, not a comment opener, so the browser never swallows the tail.
    Likewise, per CSS Syntax, `/*` is literal inside an unquoted url()
    token — comment recognition only happens at the top token level — so
    `.e{background:url(data:text/plain,/*);background:linen}` renders
    linen while a naive stripper goes blind after the `/*`.

    Validator law (round 4, 2026-10-09): every regex that strips CSS
    comments without understanding CSS strings hands the attacker a
    blindfold to place over the gate. Extended (round 5, ported from the
    repairs5 line): the same holds for url() tokens — the stripper must
    know where strings AND urls begin and end before judging what the
    text means.

    An unclosed comment consumes the rest of the input (CSS Syntax) —
    the tail is dropped, the gate judges less, and _is_dark fails closed
    on whatever remains unjudgeable. An unterminated string likewise
    consumes to end of input (nothing after it can reopen a comment).
    An unterminated url() consumes to the next ) or end of input —
    same fail-closed direction. CDO/CDC (<!-- -->) are not comments and
    are untouched. Escapes are decoded AFTER comment stripping
    (tokenization order), so an escape sequence can never forge a comment
    opener or a string delimiter."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch in "\"'":
            # Copy the string token verbatim — escapes ride along.
            quote = ch
            out.append(ch)
            i += 1
            while i < n:
                c = text[i]
                out.append(c)
                if c == "\\" and i + 1 < n:
                    out.append(text[i + 1])
                    i += 2
                    continue
                i += 1
                if c == quote:
                    break
        elif ch in "uU\\":
            k = _match_url_opener(text, i)
            if k == -1:
                out.append(ch)
                i += 1
            else:
                # A url( token: consume to the matching ) verbatim.
                # Strings inside are still respected; a \-escape never
                # terminates (a decoded ) is part of the url's value).
                out.append(text[i:k])
                i = k
                while i < n:
                    c = text[i]
                    if c in "\"'":
                        quote = c
                        out.append(c)
                        i += 1
                        while i < n:
                            d = text[i]
                            out.append(d)
                            if d == "\\" and i + 1 < n:
                                out.append(text[i + 1])
                                i += 2
                                continue
                            i += 1
                            if d == quote:
                                break
                    elif c == "\\" and i + 1 < n:
                        out.append(c)
                        out.append(text[i + 1])
                        i += 2
                    elif c == ")":
                        out.append(c)
                        i += 1
                        break
                    else:
                        out.append(c)
                        i += 1
        elif ch == "/" and i + 1 < n and text[i + 1] == "*":
            # Real comment (outside a string and outside url()): skip to
            # its closer.
            end = text.find("*/", i + 2)
            if end == -1:
                break  # unclosed comment swallows the tail
            i = end + 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def _normalize_css_block(text: str) -> str:
    """Normalize a <style> block's content: NO html.unescape — browsers do
    not decode entities in raw text elements. Comments stripped FIRST
    (string-aware: a `"` inside a comment is not a string delimiter —
    neutralizing before stripping misread it and swallowed real rules),
    then strings neutralized (hole 2: brace-in-string rule-iterator
    injection), then CSS escapes decoded."""
    return _decode_css_escapes(
        _neutralize_css_strings(_strip_css_comments(text)))


def _normalize_style_attr(text: str) -> str:
    """Normalize an extracted style="" attribute value: the HTML parser
    decodes entities in attribute values before CSS sees them, so
    html.unescape() runs first, then comments are stripped (string-aware),
    then strings are neutralized (hole 2), then the CSS pipeline
    (escapes). Strip-before-neutralize: a `"` inside a comment must not
    be misread as a string delimiter.

    Structural hardening (hole 2, escape variants): after decoding, any
    remaining `{`/`}` is a raw brace outside any string — malformed CSS
    or an escape-smuggled brace (`\\7d`). In a declaration list a brace
    can only ever separate declarations, so it becomes `;`: the
    `*[inline]{...}` wrapper can no longer be broken out of, and every
    declaration in the attribute is judged. (The <style>-block channel
    keeps structural braces; escape-smuggled braces there are a known
    residual — see the round-4 report.)"""
    norm = _decode_css_escapes(
        _neutralize_css_strings(
            _strip_css_comments(_ihtml.unescape(text))))
    return norm.replace("{", ";").replace("}", ";")


def inline_css(html: str) -> str:
    """The single scanned CSS stream: <style> blocks AND inline style
    attributes, concatenated.

    Durable law (validator, 2026-10-09): every parser is only as strong as
    the narrowest input channel it doesn't read. Inline styles were an
    unread channel — every color check missed them. Each inline style
    attribute is wrapped as a `*[inline]` rule so the rule-iterating checks
    judge it like any other rule.

    Encoding law (validator round 3): <style> blocks are normalized as
    raw text (no entity decoding); inline attribute values are
    entity-decoded first. Both then go through comment stripping and CSS
    escape decoding, in browser order.

    Quoting law (validator round 4): HTML does not require quotes —
    `<div style=background:white>` is applied by the browser. Style
    attributes are read through the _parse_attrs tokenizer (one tokenizer
    for every tag scan), so double-quoted, single-quoted, and unquoted
    forms are all judged exactly once. A trailing `/` on an unquoted
    value is self-closing syntax, never CSS — stripped fail-closed.
    """
    parts = [_normalize_css_block(p) for p in _style_blocks(html)]
    for m in _all_tags(html):
        tag = m.group(0)
        style = _parse_attrs(tag).get("style")
        if style is None:
            continue
        if not re.search(r"\bstyle\s*=\s*[\"']", tag, re.I):
            style = style.rstrip("/")  # self-closing `/`, never CSS
        style = style.strip()
        if style:
            parts.append(f"*[inline]{{{_normalize_style_attr(style)}}}")
    return "\n".join(parts)


def _inline_style_of(html: str, tag: str) -> str | None:
    """The normalized style="" attribute of the first <tag>, for cascade
    judging (inline styles beat stylesheet rules). Read through
    _parse_attrs (every quote form; duplicate attributes: first wins per
    HTML spec). Normalized through the same encoding layer as inline_css
    so cascade winners are judged on what the browser actually sees."""
    for m in _find_tags(html, tag):
        raw = m.group(0)
        style = _parse_attrs(raw).get("style")
        if style is None:
            continue
        if not re.search(r"\bstyle\s*=\s*[\"']", raw, re.I):
            style = style.rstrip("/")  # self-closing `/`, never CSS
        style = style.strip()
        return _normalize_style_attr(style) if style else None
    return None


def _split_top_level(value: str) -> list[str]:
    """Split on commas at paren depth 0 (layers, not gradient stops)."""
    parts, depth, cur = [], 0, []
    for ch in value:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def _strip_punct(s: str) -> str:
    """Strip trailing punctuation/whitespace before every color lookup.
    (Validator hole 2: "white)" never matched the named-color table.)"""
    return s.strip().strip(";,")


_GRADIENT_HINT_RE = re.compile(
    r"^(to\s+[a-z\s]+|\d+(\.\d+)?(deg|turn|rad|grad)|circle|ellipse"
    r"|closest-side|closest-corner|farthest-side|farthest-corner"
    r"|at\s+.+)$",
    re.I,
)


def _gradient_stops(value: str) -> list[str]:
    """Paren-aware color stops of a gradient(), direction/position hints
    removed, trailing punctuation stripped. Fail-closed callers treat an
    empty/unparseable result as not-dark."""
    m = re.search(r"[a-z-]*gradient\s*\(", value, re.I)
    if not m:
        return []
    depth, start, stops = 0, m.end(), []
    for j in range(m.end() - 1, len(value)):
        ch = value[j]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                stops.append(value[start:j])
                break
        elif ch == "," and depth == 1:
            stops.append(value[start:j])
            start = j + 1
    cleaned = []
    for s in stops:
        t = _strip_punct(s)
        if _GRADIENT_HINT_RE.match(t):
            continue
        t = re.sub(r"(\s+\d+(\.\d+)?%)+$", "", t).strip()
        if t:
            cleaned.append(t)
    return cleaned


def _first_color_token(layer: str) -> str | None:
    """First color-parseable token of a background shorthand layer.
    Tries the whole value first (functional notations contain spaces:
    hsl(0, 0%, 100%) must not be split), then falls back to whitespace
    token scanning for multi-token shorthands (snow url(x.png)).
    url(...) is skipped (an image cannot be judged without fetching);
    a layer with no color token is unjudgeable, not light."""
    t = _strip_punct(layer)
    if _luminance_of(t) is not None:
        return t
    v = re.sub(r"url\(\s*[^)]*\s*\)", " ", layer, flags=re.I)
    v = re.sub(r"var\(\s*--[^)]*\)", " ", v)
    for tok in re.split(r"\s+", v):
        t = _strip_punct(tok)
        if not t or t.lower() in ("none", "transparent", "inherit",
                                  "initial"):
            continue
        if _luminance_of(t) is not None:
            return t
    return None


# ---------------------------------------------------------------------------
# CSS-syntax at-rule parsing — ADOPTED from the compliance lane
# (naya5/compliance-import-class-fix @ a0caf183, 2026-10-09; 24/24
# adversarial + 29/29 tests green there). Reused here rather than building
# a second implementation, per the cross-lane note: at-rules are consumed
# as at-rules and RECORDED at the delivery boundary, never merged into
# selectors; escapes are decoded before at-keyword matching
# (`@\\69 mport` registers); comments between the keyword and the URL are
# consumed as comments (`@import/**/url(x)` registers); an @import inside
# a comment or string does NOT (no over-block); the parser is total (no
# exceptions on any input). The gate needs only the at_rules half:
# an external @import is a SELF-CONTAINED violation (fail-closed).
# ---------------------------------------------------------------------------
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




def _css_sources(html: str) -> list[str]:
    """Every CSS source with browser-order decoding, for REFERENCE scans
    (@import, url()): <style> blocks raw (raw-text elements: no entity
    decoding), inline style= attributes entity-decoded. The _CSSParser
    handles comments/strings/escapes itself, so these sources bypass the
    color-normalization pipeline (which is built for color judging, not
    reference extraction)."""
    sources = list(_style_blocks(html))
    for m in _all_tags(html):
        style = _parse_attrs(m.group(0)).get("style")
        if style:
            sources.append(_ihtml.unescape(style))
    return sources


def _is_inline_ref(url: str) -> bool:
    """data: URLs and #fragments are inline by definition; empty refs are
    nothing. Everything else (https:// or relative) leaves the single
    file — the sandbox renders it broken."""
    u = url.strip().lower()
    return not u or u.startswith("data:") or u.startswith("#")


def _import_prelude_url(prelude: str) -> str | None:
    """Extract the stylesheet URL from an @import prelude.

    The prelude arrives with comments already excluded and the at-keyword
    already identified. Forms: url("u"), url('u'), url(u), "u", 'u', u —
    each optionally followed by media queries. Escapes in the URL are
    decoded before the inline-reference check (`url(\\64 ata:...)` is a
    data: URL, not an external reference)."""
    p = css_unescape(prelude.strip())
    if not p:
        return None
    if p[:4].lower() == "url(":
        # paren-aware inner; media queries after the close paren ignored
        i, depth, start, n = 4, 0, 4, len(p)
        while i < n:
            c = p[i]
            if c in "\"'":
                i = _skip_css_string(p, i)
                continue
            if c == "(":
                depth += 1
            elif c == ")":
                if depth == 0:
                    break
                depth -= 1
            i += 1
        inner = p[start:i].strip()
    elif p[0] in "\"'":
        end = p.find(p[0], 1)
        inner = p[1:end] if end != -1 else p[1:]
    else:
        inner = re.split(r"[\s;]", p, maxsplit=1)[0]
    inner = inner.strip()
    if len(inner) >= 2 and inner[0] == inner[-1] and inner[0] in "\"'":
        inner = inner[1:-1]
    return inner.strip() or None


def _import_urls(css_text: str) -> list[str]:
    """Stylesheet targets of @import at-rules in one CSS source."""
    urls = []
    for name, prelude in parse_stylesheet(css_text)[1]:
        if name != "import":
            continue
        url = _import_prelude_url(prelude)
        if url:
            urls.append(url)
    return urls


def _iter_url_targets(css_text: str) -> list[str]:
    """Every url(...) target in a CSS source, string/comment aware.

    `content:"url(evil)"` is a string, not a reference (no flag);
    `/* url(evil) */` is a comment (no flag). `url (` with a space is
    not the url function per CSS (no flag — matches browsers). Total:
    never raises."""
    out = []
    i, n = 0, len(css_text)
    while i < n:
        c = css_text[i]
        if c in "\"'":
            i = _skip_css_string(css_text, i)
            continue
        if c == "/" and i + 1 < n and css_text[i + 1] == "*":
            end = css_text.find("*/", i + 2)
            i = n if end == -1 else end + 2
            continue
        if css_text[i:i + 4].lower() == "url(":
            j, depth, start = i + 4, 0, i + 4
            while j < n:
                d = css_text[j]
                if d in "\"'":
                    j = _skip_css_string(css_text, j)
                    continue
                if d == "(":
                    depth += 1
                elif d == ")":
                    if depth == 0:
                        break
                    depth -= 1
                j += 1
            inner = css_text[start:j].strip()
            if (len(inner) >= 2 and inner[0] == inner[-1]
                    and inner[0] in "\"'"):
                inner = inner[1:-1].strip()
            inner = css_unescape(inner)
            if inner:
                out.append(inner)
            i = j + 1
            continue
        i += 1
    return out


def check_self_contained(html: str) -> list[str]:
    """SELF-CONTAINED — every external-reference vector, every quote form.

    <link rel=stylesheet href> and <script src> go through the
    quote-tolerant _parse_attrs tokenizer (unquoted, single-quoted,
    whitespace and case variants are the same class, not new holes).
    @import goes through the CSS-syntax _CSSParser (at-rules as at-rules).
    url() references anywhere in CSS are external-resource vectors too
    (C2c verdict, round 4): detection is certain — no fetching needed —
    so an external url() fails closed; only judging image CONTENT stays
    fail-open-honest. data: URLs and #fragments are inline by definition."""
    v: list[str] = []
    for m in _find_tags(html, "link"):
        attrs = _parse_attrs(m.group(0))
        rel = attrs.get("rel") or ""
        href = attrs.get("href")
        if ("stylesheet" in rel.lower().split() and href
                and not _is_inline_ref(href)):
            v.append(
                f"SELF-CONTAINED: external stylesheet reference: {href}")
    for m in _find_tags(html, "script"):
        src = _parse_attrs(m.group(0)).get("src")
        if src and not _is_inline_ref(src):
            v.append(f"SELF-CONTAINED: external script reference: {src}")
    import_seen: set[str] = set()
    for css in _css_sources(html):
        for url in _import_urls(css):
            if not _is_inline_ref(url) and url not in import_seen:
                import_seen.add(url)
                v.append(
                    "SELF-CONTAINED: external stylesheet via @import: "
                    f"{url}")
        for url in _iter_url_targets(css):
            if not _is_inline_ref(url) and url not in import_seen:
                v.append(
                    f"SELF-CONTAINED: external resource via url(): {url}")
    return v
def _root_vars(css: str) -> dict[str, str]:
    """Parse :root { --name: value } custom properties."""
    vars: dict[str, str] = {}
    for m in re.finditer(r":root\s*\{([^}]*)\}", css, re.I):
        for vm in re.finditer(r"--([a-zA-Z0-9_-]+)\s*:\s*([^;}]+);?", m.group(1)):
            vars[vm.group(1)] = vm.group(2).strip()
    return vars


def _inline_vars(html: str) -> dict[str, str]:
    """Custom properties defined in inline style= attributes (element
    scope). The browser resolves var() at the ELEMENT, not just :root:
    `style="--wash:white"` + `background:var(--wash)` renders white even
    though :root never defines --wash (validator round 4, hole 3).
    Merged OVER :root by _merged_vars — a deliberate fail-closed
    over-approximation: an element-scoped light var anywhere means some
    element can paint light, and the gate cannot prove otherwise."""
    vars: dict[str, str] = {}
    for m in _all_tags(html):
        style = _parse_attrs(m.group(0)).get("style")
        if not style:
            continue
        norm = _normalize_style_attr(style)
        for vm in re.finditer(r"--([a-zA-Z0-9_-]+)\s*:\s*([^;}]+);?", norm):
            vars[vm.group(1)] = vm.group(2).strip()
    return vars


def _merged_vars(html: str, css: str) -> dict[str, str]:
    """:root custom properties, overlaid with element-scoped (inline)
    definitions. Inline wins on conflict: it is the more specific scope,
    and the fail-closed direction for hole 3."""
    merged = _root_vars(css)
    merged.update(_inline_vars(html))
    return merged


def _split_var_inner(inner: str) -> tuple[str | None, str | None]:
    """Split a var() inner into (name, fallback). The fallback is
    everything after the first top-level comma (`var(--x, rgb(1,2,3))`
    keeps the whole function as fallback). Returns (None, None) when the
    inner is not a custom-property reference."""
    i, n = 0, len(inner)
    while i < n and inner[i] in " \t\n\r\f":
        i += 1
    if inner[i:i + 2] != "--":
        return None, None
    i += 2
    start = i
    while i < n and (inner[i].isalnum() or inner[i] in "-_"):
        i += 1
    name = inner[start:i]
    j = i
    while j < n and inner[j] in " \t\n\r\f":
        j += 1
    if j < n and inner[j] == ",":
        return name, inner[j + 1:].strip()
    return name, None


def _resolve_vars(color: str, vars: dict[str, str], depth: int = 0) -> str:
    """Resolve var() references per CSS semantics, fail-safe.

    - `var(--x)` with --x defined -> the definition (recursively;
      chains like --b:var(--a) resolve).
    - `var(--x, <fallback>)` with --x undefined -> the FALLBACK
      (recursively) — the browser uses it, so the gate must judge it
      (validator round 4, hole 5: `var(--missing, white)` renders white).
    - `var(--x)` undefined with no fallback -> left as-is (unjudgeable:
      black-root judging stays fail-closed via _is_dark; surfaces stay
      fail-open-honest per the documented boundary — an undefined var
      with no fallback computes to unset/transparent, not a surface).
    Depth-capped (5): cyclic vars become unjudgeable, never hang."""
    if depth > 5:
        return color
    out: list[str] = []
    i, n = 0, len(color)
    while i < n:
        m = re.match(r"var\(\s*", color[i:], re.I)
        if not m:
            out.append(color[i])
            i += 1
            continue
        # paren-aware: find the matching close paren (strings skipped)
        j = i + m.end()
        d, k = 1, j
        while k < n and d > 0:
            c = color[k]
            if c in "\"'":
                k = _skip_css_string(color, k)
                continue
            if c == "(":
                d += 1
            elif c == ")":
                d -= 1
            k += 1
        if d != 0:
            out.append(color[i:j])  # unbalanced: not a call; verbatim
            i = j
            continue
        name, fallback = _split_var_inner(color[j:k - 1])
        if name and name in vars:
            out.append(_resolve_vars(vars[name], vars, depth + 1))
        elif fallback is not None:
            out.append(_resolve_vars(fallback, vars, depth + 1))
        else:
            out.append(color[i:k])  # unresolvable: leave as-is
        i = k
    return "".join(out)


# CSS named colors -> (r, g, b). Full table so heuristic checks cannot be
# evaded by spelling a light surface as a name (e.g. "snow", "yellow").
_NAMED_COLORS = {
    "aliceblue": (240, 248, 255), "antiquewhite": (250, 235, 215), "aqua": (0, 255, 255),
    "aquamarine": (127, 255, 212), "azure": (240, 255, 255), "beige": (245, 245, 220),
    "bisque": (255, 228, 196), "black": (0, 0, 0), "blanchedalmond": (255, 235, 205),
    "blue": (0, 0, 255), "blueviolet": (138, 43, 226), "brown": (165, 42, 42),
    "burlywood": (222, 184, 135), "cadetblue": (95, 158, 160), "chartreuse": (127, 255, 0),
    "chocolate": (210, 105, 30), "coral": (255, 127, 80), "cornflowerblue": (100, 149, 237),
    "cornsilk": (255, 248, 220), "crimson": (220, 20, 60), "cyan": (0, 255, 255),
    "darkblue": (0, 0, 139), "darkcyan": (0, 139, 139), "darkgoldenrod": (184, 134, 11),
    "darkgray": (169, 169, 169), "darkgrey": (169, 169, 169), "darkgreen": (0, 100, 0),
    "darkkhaki": (189, 183, 107), "darkmagenta": (139, 0, 139), "darkolivegreen": (85, 107, 47),
    "darkorange": (255, 140, 0), "darkorchid": (153, 50, 204), "darkred": (139, 0, 0),
    "darksalmon": (233, 150, 122), "darkseagreen": (143, 188, 143), "darkslateblue": (72, 61, 139),
    "darkslategray": (47, 79, 79), "darkslategrey": (47, 79, 79), "darkturquoise": (0, 206, 209),
    "darkviolet": (148, 0, 211), "deeppink": (255, 20, 147), "deepskyblue": (0, 191, 255),
    "dimgray": (105, 105, 105), "dimgrey": (105, 105, 105), "dodgerblue": (30, 144, 255),
    "firebrick": (178, 34, 34), "floralwhite": (255, 250, 240), "forestgreen": (34, 139, 34),
    "fuchsia": (255, 0, 255), "gainsboro": (220, 220, 220), "ghostwhite": (248, 248, 255),
    "gold": (255, 215, 0), "goldenrod": (218, 165, 32), "gray": (128, 128, 128),
    "grey": (128, 128, 128), "green": (0, 128, 0), "greenyellow": (173, 255, 47),
    "honeydew": (240, 255, 240), "hotpink": (255, 105, 180), "indianred": (205, 92, 92),
    "indigo": (75, 0, 130), "ivory": (255, 255, 240), "khaki": (240, 230, 140),
    "lavender": (230, 230, 250), "lavenderblush": (255, 240, 245), "lawngreen": (124, 252, 0),
    "lemonchiffon": (255, 250, 205), "lightblue": (173, 216, 230), "lightcoral": (240, 128, 128),
    "lightcyan": (224, 255, 255), "lightgoldenrodyellow": (250, 250, 210), "lightgray": (211, 211, 211),
    "lightgrey": (211, 211, 211), "lightgreen": (144, 238, 144), "lightpink": (255, 182, 193),
    "lightsalmon": (255, 160, 122), "lightseagreen": (32, 178, 170), "lightskyblue": (135, 206, 250),
    "lightslategray": (119, 136, 153), "lightslategrey": (119, 136, 153), "lightsteelblue": (176, 196, 222),
    "lightyellow": (255, 255, 224), "lime": (0, 255, 0), "limegreen": (50, 205, 50),
    "linen": (250, 240, 230), "magenta": (255, 0, 255), "maroon": (128, 0, 0),
    "mediumaquamarine": (102, 205, 170), "mediumblue": (0, 0, 205), "mediumorchid": (186, 85, 211),
    "mediumpurple": (147, 112, 219), "mediumseagreen": (60, 179, 113), "mediumslateblue": (123, 104, 238),
    "mediumspringgreen": (0, 250, 154), "mediumturquoise": (72, 209, 204), "mediumvioletred": (199, 21, 133),
    "midnightblue": (25, 25, 112), "mintcream": (245, 255, 250), "mistyrose": (255, 228, 225),
    "moccasin": (255, 228, 181), "navajowhite": (255, 222, 173), "navy": (0, 0, 128),
    "oldlace": (253, 245, 230), "olive": (128, 128, 0), "olivedrab": (107, 142, 35),
    "orange": (255, 165, 0), "orangered": (255, 69, 0), "orchid": (218, 112, 214),
    "palegoldenrod": (238, 232, 170), "palegreen": (152, 251, 152), "paleturquoise": (175, 238, 238),
    "palevioletred": (219, 112, 147), "papayawhip": (255, 239, 213), "peachpuff": (255, 218, 185),
    "peru": (205, 133, 63), "pink": (255, 192, 203), "plum": (221, 160, 221),
    "powderblue": (176, 224, 230), "purple": (128, 0, 128), "rebeccapurple": (102, 51, 153),
    "red": (255, 0, 0), "rosybrown": (188, 143, 143), "royalblue": (65, 105, 225),
    "saddlebrown": (139, 69, 19), "salmon": (250, 128, 114), "sandybrown": (244, 164, 96),
    "seagreen": (46, 139, 87), "seashell": (255, 245, 238), "sienna": (160, 82, 45),
    "silver": (192, 192, 192), "skyblue": (135, 206, 235), "slateblue": (106, 90, 205),
    "slategray": (112, 128, 144), "slategrey": (112, 128, 144), "snow": (255, 250, 250),
    "springgreen": (0, 255, 127), "steelblue": (70, 130, 180), "tan": (210, 180, 140),
    "teal": (0, 128, 128), "thistle": (216, 191, 216), "tomato": (255, 99, 71),
    "turquoise": (64, 224, 208), "violet": (238, 130, 238), "wheat": (245, 222, 179),
    "white": (255, 255, 255), "whitesmoke": (245, 245, 245), "yellow": (255, 255, 0),
    "yellowgreen": (154, 205, 50),
}


def _rgba_of(color: str) -> tuple[float, float, float, float] | None:
    """Parse a CSS color to (r, g, b, a) in 0..1, or None if unparseable."""
    c = re.sub(r";+$", "", color.strip().lower())
    if c == "transparent":
        return (0.0, 0.0, 0.0, 0.0)
    if c in _NAMED_COLORS:
        r, g, b = _NAMED_COLORS[c]
        return (r / 255, g / 255, b / 255, 1.0)
    m = re.fullmatch(r"#([0-9a-f]{3,4}|[0-9a-f]{6}|[0-9a-f]{8})", c)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h)
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255,
                int(h[4:6], 16) / 255, a)
    m = re.fullmatch(
        r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*"
        r"(?:,\s*([\d.]+))?\s*\)", c)
    if m:
        a = float(m.group(4)) if m.group(4) is not None else 1.0
        return (int(m.group(1)) / 255, int(m.group(2)) / 255,
                int(m.group(3)) / 255, max(0.0, min(1.0, a)))
    m = re.fullmatch(
        r"hsla?\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*"
        r"(?:,\s*([\d.]+))?\s*\)", c)
    if m:
        h, s, l = (float(m.group(1)) / 360.0, float(m.group(2)) / 100.0,
                   float(m.group(3)) / 100.0)
        if s == 0:
            r = g = b = l
        else:
            def hue2rgb(p: float, q: float, t: float) -> float:
                t %= 1.0
                if t < 1 / 6:
                    return p + (q - p) * 6 * t
                if t < 1 / 2:
                    return q
                if t < 2 / 3:
                    return p + (q - p) * (2 / 3 - t) * 6
                return p
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r, g, b = (hue2rgb(p, q, h + 1 / 3), hue2rgb(p, q, h),
                       hue2rgb(p, q, h - 1 / 3))
        a = float(m.group(4)) if m.group(4) is not None else 1.0
        return (r, g, b, max(0.0, min(1.0, a)))
    return None


def _luminance_of(color: str) -> float | None:
    """Relative luminance 0..1 of the color as rendered on the gate's black
    ground (alpha composited over black), or None if unparseable.

    Design judgment (validator hole 6): the gate enforces the rendered
    result on Shawn's black canvas, not raw channel values. A 5% white
    sheen over black is visually black (passes); a 90% white overlay is
    visually white (fails)."""
    rgba = _rgba_of(color)
    if rgba is None:
        return None
    r, g, b, a = rgba
    r, g, b = r * a, g * a, b * a  # composite over black
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 1.0


def _is_dark(color: str, vars: dict[str, str] | None = None) -> bool:
    """True only if the value is provably dark. Fail-closed everywhere:
    any light stop, any unparseable stop, any unjudgeable token -> False.

    Gradients are judged by ALL stops: a white-to-black gradient IS a light
    surface at its white end. (The old "first stop only" rule let
    linear-gradient(white, black) walk through.)"""
    color = _resolve_vars(color, vars or {})
    c = color.strip().lower()
    if c in ("transparent", "none", "initial", "inherit"):
        return True  # not a light surface
    if "gradient" in c:
        stops = _gradient_stops(c)
        if not stops:
            return False  # fail closed: no parseable stops
        for s in stops:
            lum = _luminance_of(_strip_punct(s))
            if lum is None:
                return False  # fail closed: unparseable stop
            if lum >= 0.35:
                return False  # any light stop -> not dark
        return True
    tok = _first_color_token(c)
    if tok is None:
        return False  # fail closed: cannot verify dark
    lum = _luminance_of(tok)
    if lum is None:
        return False
    return lum < 0.35


def _surface_is_light(value: str) -> bool:
    """True if any layer/stop/token of a background value is provably light.
    Unparseable layers (images) are unjudgeable, not light — fail-open here
    is honest: the gate cannot fetch images. (Black-root judging stays
    fail-closed via _is_dark.)"""
    c = value.strip()
    if not c:
        return False
    for layer in _split_top_level(c):
        layer = layer.strip()
        if not layer:
            continue
        if "gradient" in layer.lower():
            for s in _gradient_stops(layer):
                lum = _luminance_of(_strip_punct(s))
                if lum is not None and lum >= 0.6:
                    return True
        else:
            tok = _first_color_token(layer)
            if tok is None:
                continue
            lum = _luminance_of(tok)
            if lum is not None and lum >= 0.6:
                return True
    return False


_BG_PAT = re.compile(
    r"background(?:-color)?\s*:\s*([^;!{}]+)(\s*!important)?", re.I)
_COLOR_PAT = re.compile(
    r"(?<![a-z-])color\s*:\s*([^;!{}]+)(\s*!important)?", re.I)


def _selector_targets(selector: str, tag: str) -> bool:
    """Does a CSS selector target <tag> (bare, classed, or descendant)?"""
    for part in selector.split(","):
        p = part.strip().lower()
        if re.fullmatch(r"%s(\.[a-z0-9_-]+)*" % tag, p):
            return True
        if re.search(r"(^|[\s>+~])%s(\.[a-z0-9_-]+)?$" % tag, p):
            return True
    return False


def _prop_declarations(css: str, pat: re.Pattern, html: str,
                       tag: str) -> tuple[list[tuple[int, int, str]], bool]:
    """Collect (rank, order, value) for a property on <tag>.

    Cascade ranks: stylesheet normal 1, inline normal 2,
    stylesheet !important 3, inline !important 4. The winner is
    max(rank, order) — inline beats stylesheet, !important beats normal,
    later beats earlier. Durable law: judge the cascade winner, not the
    first declaration.
    Returns (declarations, any_rule_targeted_tag)."""
    decls: list[tuple[int, int, str]] = []
    order = 0
    any_rule = False
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        selector = m.group(1).strip()
        if selector.startswith("@"):
            continue
        if not _selector_targets(selector, tag):
            continue
        any_rule = True
        for pm in pat.finditer(m.group(2)):
            rank = 3 if pm.group(2) else 1
            decls.append((rank, order, pm.group(1).strip()))
            order += 1
    inl = _inline_style_of(html, tag)
    if inl:
        any_rule = True
        for pm in pat.finditer(inl):
            rank = 4 if pm.group(2) else 2
            decls.append((rank, order, pm.group(1).strip()))
            order += 1
    return decls, any_rule


def check_black_root(html: str, css: str) -> list[str]:
    v = []
    vars = _merged_vars(html, css)
    for sel in ("html", "body"):
        decls, any_rule = _prop_declarations(css, _BG_PAT, html, sel)
        if not decls:
            v.append(f"BLACK ROOT: no background declared for `{sel}` "
                     f"(browser default white leaks through)")
        else:
            winner = max(decls, key=lambda d: (d[0], d[1]))[2]
            if not _is_dark(winner, vars):
                v.append(f"BLACK ROOT: `{sel}` background is not deep black: "
                         f"{winner}")
    return v


def _split_shadow_tokens(s: str) -> list[str]:
    """Whitespace-split a box-shadow layer, keeping functions
    (rgba(...)) together — paren-aware."""
    parts, depth, cur = [], 0, []
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch.isspace() and depth == 0:
            if cur:
                parts.append("".join(cur))
                cur = []
        else:
            cur.append(ch)
    if cur:
        parts.append("".join(cur))
    return parts


def _inset_shadow_is_light(value: str, vars: dict[str, str]) -> bool:
    """True when an `inset` box-shadow layer paints light.

    An inset shadow fills the box interior — `inset 0 0 0 9999px white`
    IS a white surface with no background-* involved (validator round 4,
    hole 6). Outset (drop) shadows are glow craft, not surfaces —
    deliberately not judged. Each comma layer judged alone."""
    for layer in _split_top_level(value.strip()):
        toks = _split_shadow_tokens(_resolve_vars(layer.strip(), vars))
        if not any(t.lower() == "inset" for t in toks):
            continue
        for t in toks:
            t = _strip_punct(t)
            if t.lower() == "inset":
                continue
            lum = _luminance_of(t)
            if lum is not None and lum >= 0.6:
                return True
    return False


def check_no_light_surfaces(css: str, html: str = "") -> list[str]:
    v = []
    vars = _merged_vars(html, css)
    for m in re.finditer(
        r"([^{}]+)\{([^{}]*)\}", css
    ):
        selector, body = m.group(1).strip(), m.group(2)
        if selector.startswith("@"):
            continue
        # pseudo-element detail craft (specular dots, facet highlights)
        # are not surfaces — skip them
        if ":before" in selector or ":after" in selector:
            continue
        for bm in re.finditer(
            r"background(?:-color)?\s*:\s*([^;{}]+);?", body, re.I
        ):
            val = _resolve_vars(bm.group(1).strip(), vars)
            # Light surfaces are surfaces: any opaque background with high
            # luminance fails, however it is spelled (hex, name, hsl).
            # Every layer of multi-backgrounds is judged; every stop of a
            # gradient is judged.
            if _surface_is_light(val):
                v.append(f"NO LIGHT SURFACES: `{selector}` has light "
                         f"background: {bm.group(1).strip()}")
        for sm in re.finditer(r"box-shadow\s*:\s*([^;{}]+);?", body, re.I):
            if _inset_shadow_is_light(sm.group(1), vars):
                v.append(f"NO LIGHT SURFACES: `{selector}` has light "
                         f"inset box-shadow paint: {sm.group(1).strip()}")
    return v


def check_dark_scheme(html: str, css: str) -> list[str]:
    """The color-scheme declaration, read through _parse_attrs: lawful
    `<meta name=color-scheme content=dark>` (unquoted) MUST pass — the old
    quote-requiring regex wrongly rejected it (validator round 4, row 4
    over-block). Attribute order and case don't matter either."""
    for m in _find_tags(html, "meta"):
        attrs = _parse_attrs(m.group(0))
        if ((attrs.get("name") or "").lower() == "color-scheme"
                and (attrs.get("content") or "").lower() == "dark"):
            return []
    if re.search(r"color-scheme\s*:\s*dark", css, re.I):
        return []
    return ["DARK COLOR-SCHEME: no dark color-scheme declared "
            "(native controls/chrome render light)"]


def _manifest_classes(manifest_path: Path) -> set[str]:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    known: set[str] = set()
    manifest_dir = manifest_path.parent
    # every class defined in the canonical CSS files is canonical
    css_files = list(manifest_dir.glob("*.css"))
    css_files += list(manifest_dir.glob("*/*.css"))
    for cssf in css_files:
        css = cssf.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"\.([a-zA-Z0-9_-]+)", css):
            cls = m.group(1)
            if cls.startswith(_NAYA_PREFIXES):
                known.add(cls)
    for b in data.get("blocks", []):
        for c in b.get("css_classes", []):
            for part in re.split(r"[/,]", c):
                # all class names in the selector, not just the first
                # (handles `table.naya-table[x]` -> naya-table)
                known.update(re.findall(r"\.([a-zA-Z0-9_-]+)", part))
        # every class used inside the block's own snippet is canonical too
        html_file = b.get("html_file", "")
        if html_file:
            cat = b.get("category_id", "")
            snippet = manifest_dir / cat / Path(html_file).name
            if snippet.exists():
                shtml = snippet.read_text(encoding="utf-8", errors="replace")
                for m in re.finditer(r'class=["\']([^"\']+)["\']', shtml):
                    known.update(m.group(1).split())
    # structural page root — not a component
    known.add("naya-page")
    return known


_NAYA_PREFIXES = ("naya-", "board", "orb-", "lv-", "torb", "gem-")


def check_no_freestyle(html: str, known: set[str]) -> list[str]:
    """Every non-canonical naya-* class must come from the manifest.

    The browser HTML-decodes class attribute values before matching, so
    `class="&#110;aya-evil"` IS class `naya-evil`. The check decodes
    entities first (validator round 4, H3) — a leading entity used to
    evade the raw-text prefix match. Unquoted class attributes are read
    too (same quoting law as inline styles: `<div class=naya-foo>` is
    applied by the browser)."""
    v = []
    used: set[str] = set()
    for m in re.finditer(r'class=["\']([^"\']+)["\']', html, re.I):
        for cls in _ihtml.unescape(m.group(1)).split():
            used.add(cls)
    for m in re.finditer(r"\bclass\s*=\s*([^\"'\s>][^>\s]*)", html, re.I):
        for cls in _ihtml.unescape(m.group(1)).split():
            used.add(cls)
    for cls in sorted(used):
        if cls.startswith(_NAYA_PREFIXES) and cls not in known:
            # allow BEM/state suffixes of known bases
            base = re.match(r"([a-zA-Z0-9_-]+?)(--|__|-sm|-xs|-lg|$)", cls)
            base_name = cls.split("--")[0].split("__")[0]
            if base_name not in known and cls not in known:
                v.append(f"NO FREESTYLE: class `.{cls}` is not in the "
                         f"manifest — use a canonical block or file the gap")
    return v


def check_light_text(html: str, css: str) -> list[str]:
    """Body text must be light. Judges the cascade winner — the last
    declaration wins (inline styles beat stylesheet rules, !important beats
    normal) — not the first declaration. (Validator hole 5: a later dark
    override, including inside @media, used to walk through.)"""
    decls, any_rule = _prop_declarations(css, _COLOR_PAT, html, "body")
    if not any_rule:
        return ["LIGHT TEXT: no body rule found"]
    if not decls:
        return ["LIGHT TEXT: body has no text color declared"]
    col = max(decls, key=lambda d: (d[0], d[1]))[2]
    # light text = NOT dark
    if _is_dark(col, _merged_vars(html, css)):
        return [f"LIGHT TEXT: body text color is dark: {col}"]
    return []


def check_viewport(html: str) -> list[str]:
    """Viewport meta through _parse_attrs (same quoting class as
    color-scheme: an unquoted `<meta name=viewport ...>` is applied by
    the browser and must be judged). First viewport meta wins."""
    for m in _find_tags(html, "meta"):
        attrs = _parse_attrs(m.group(0))
        if (attrs.get("name") or "").lower() != "viewport":
            continue
        content = (attrs.get("content") or "").replace(" ", "")
        if "width=device-width" in content:
            return []
        return ["MOBILE VIEWPORT: viewport meta does not declare "
                "width=device-width"]
    return ["MOBILE VIEWPORT: no viewport meta tag "
            "(mobile is the primary canvas)"]


RECEIPT_MARKER_RE = re.compile(
    r"<!--\s*NAYA-ACTIVATION-RECEIPT-SHA256:([a-fA-F0-9]{64})\s*-->")
RECEIPT_TTL = timedelta(hours=4)


def _normalize_repo(ref: str) -> str:
    """Normalize a repository reference to owner/repo for comparison."""
    s = str(ref or "").strip().lower()
    s = re.sub(r"^(https?://github\.com/|git@github\.com:)", "", s)
    s = re.sub(r"\.git$", "", s).rstrip("/")
    return s


def _detect_repo() -> str:
    """Best-effort expected repository from git remote.origin.url."""
    try:
        out = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True, text=True, timeout=10,
            cwd=REPO_ROOT).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        out = ""
    return _normalize_repo(out)


def check_activation(html: str, receipt_path: Path | None,
                     expected_repo: str | None = None) -> list[str]:
    """Activation citation check (Naya 3's Gap 2 — PR #1974 integration).

    With --require-activation, a deliverable FAILS unless it carries a
    current activation citation. This is the gate layer: structural
    presence/format/freshness. Deep verification of the receipt against
    live GitHub state is Naya 3's checker (tools/qa/) running in CI —
    the gate cannot fetch live state, and must not trust builder-supplied
    state as live.
    """
    v = []
    m = RECEIPT_MARKER_RE.search(html)
    if not m:
        return ["ACTIVATION: no activation citation marker in deliverable "
                "(<!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> -->). "
                "Unactivated work doesn't ship."]
    marker_sha = m.group(1).lower()
    if receipt_path is None:
        return ["ACTIVATION: citation marker present but no --receipt given; "
                "cannot verify freshness or integrity."]
    try:
        raw = receipt_path.read_bytes()
        receipt = json.loads(raw)
    except (OSError, ValueError) as e:
        return [f"ACTIVATION: cannot read receipt {receipt_path}: {e}"]
    if not isinstance(receipt, dict):
        # Round-2 had a dict guard; the fork lost it and a JSON array /
        # string / null / number receipt crashed with AttributeError.
        # A receipt that is not an object is not a receipt: fail closed,
        # never crash (validator round 4, hole 7).
        return ["ACTIVATION: receipt is not a JSON object "
                f"(got {type(receipt).__name__}) — failing closed"]
    if receipt.get("schema") != "naya.activation.receipt.v2":
        v.append("ACTIVATION: receipt schema is not naya.activation.receipt.v2")
    if receipt.get("status") != "ACTIVATED":
        v.append("ACTIVATION: receipt status is not ACTIVATED")
    for field in ("session_id", "naya_identity", "human_authority",
                  "repository", "job", "proof_plan"):
        if not receipt.get(field):
            v.append(f"ACTIVATION: receipt missing {field}")
    if not receipt.get("gates"):
        v.append("ACTIVATION: receipt names no governing gates")
    main_sha = receipt.get("main_sha", "")
    if not re.fullmatch(r"[a-fA-F0-9]{40}", str(main_sha)):
        v.append("ACTIVATION: receipt main_sha is not a 40-hex SHA")
    # Repository binding: the receipt must name THIS repository. A receipt
    # minted for another repo is a wrong-repository activation - fail.
    want = _normalize_repo(expected_repo) if expected_repo else _detect_repo()
    got = _normalize_repo(receipt.get("repository", ""))
    if not want:
        v.append("ACTIVATION: cannot determine the gated repository "
                 "(no --expected-repo and no git remote) - refusing to bind")
    elif got != want:
        v.append(f"ACTIVATION: receipt is for repository '{got}', not the "
                 f"gated repository '{want}' (wrong-repository activation)")
    # Integrity: the marker must be the sha256 of the exact receipt bytes.
    digest = hashlib.sha256(raw).hexdigest()
    if digest != marker_sha:
        v.append("ACTIVATION: citation marker does not match receipt bytes "
                 "(stale or forged citation)")
    # Freshness: 4h TTL, no future activations.
    try:
        activated = datetime.fromisoformat(
            str(receipt.get("activated_at", "")).replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        if activated > now + timedelta(minutes=2):
            v.append("ACTIVATION: receipt activated_at is in the future")
        elif now - activated > RECEIPT_TTL:
            v.append("ACTIVATION: receipt expired (>4h old) — re-activate")
    except ValueError:
        v.append("ACTIVATION: receipt activated_at is not a valid timestamp")
    return v


def run_gate(page: Path, manifest: Path,
             require_activation: bool = False,
             receipt_path: Path | None = None,
             expected_repo: str | None = None) -> list[str]:
    html = read_page(page)
    # Inert markup (HTML comments, <template> contents) is never rendered:
    # strip it before every check so inert vectors can't over-block
    # (validator round 4, hole 8). The activation citation IS a comment,
    # so check_activation always sees the raw html.
    clean = _strip_inert_html(html)
    css = inline_css(clean)
    violations: list[str] = []
    violations += check_self_contained(clean)
    violations += check_black_root(clean, css)
    violations += check_no_light_surfaces(css, clean)
    violations += check_dark_scheme(clean, css)
    violations += check_viewport(clean)
    if manifest.exists():
        violations += check_no_freestyle(clean, _manifest_classes(manifest))
    else:
        violations.append(f"NO FREESTYLE: manifest not found at {manifest} "
                          f"— cannot verify components")
    violations += check_light_text(clean, css)
    if require_activation:
        violations += check_activation(html, receipt_path, expected_repo)
    return violations


def self_test() -> int:
    """Red-green: a violating page must fail, a lawful page must pass."""
    bad = """<!DOCTYPE html><html><head><link rel="stylesheet" href="x.css">
<style>body{background:#fff;color:#111}</style></head>
<body><div class="naya-frobnicate">hi</div></body></html>"""
    good = """<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<style>html{background:#050507}body{background:#050507;color:#f8f7fb}
.naya-btn{color:#fff}</style></head>
<body><button class="naya-btn">Go</button></body></html>"""
    import tempfile
    mf = REPO_ROOT / "smart-blocks" / "manifest.json"
    with tempfile.TemporaryDirectory() as d:
        pb, pg = Path(d) / "bad.html", Path(d) / "good.html"
        pb.write_text(bad)
        pg.write_text(good)
        bad_v = run_gate(pb, mf)
        good_v = run_gate(pg, mf)
        # --- activation scenarios (Naya 3 Gap 2) ---
        now = datetime.now(timezone.utc)
        receipt = {
            "schema": "naya.activation.receipt.v2",
            "status": "ACTIVATED",
            "session_id": "selftest-1",
            "naya_identity": "Naya 5",
            "human_authority": "Shawn",
            "repository": "SoulSchoolAcademy/NayaPOWER",
            "job": "self-test",
            "gates": ["Usefulness Gate"],
            "proof_plan": "self-test",
            "main_sha": "a" * 40,
            "activated_at": now.isoformat(),
        }
        rp = Path(d) / "receipt.json"
        rp.write_bytes(json.dumps(receipt).encode())
        digest = hashlib.sha256(rp.read_bytes()).hexdigest()
        marked = good.replace("</body>",
                              f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{digest} --></body>")
        pm = Path(d) / "marked.html"
        pm.write_text(marked)
        noact_v = run_gate(pg, mf, require_activation=True,
                           receipt_path=rp)          # no marker -> fail
        okact_v = run_gate(pm, mf, require_activation=True,
                           receipt_path=rp)          # valid -> pass
        forged = marked.replace(digest, "0" * 64)
        pf = Path(d) / "forged.html"
        pf.write_text(forged)
        forged_v = run_gate(pf, mf, require_activation=True,
                            receipt_path=rp)         # mismatch -> fail
        old = dict(receipt,
                   activated_at=(now - timedelta(hours=5)).isoformat())
        rp_old = Path(d) / "receipt_old.json"
        rp_old.write_bytes(json.dumps(old).encode())
        d_old = hashlib.sha256(rp_old.read_bytes()).hexdigest()
        pm_old = Path(d) / "marked_old.html"
        pm_old.write_text(good.replace(
            "</body>",
            f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d_old} --></body>"))
        expired_v = run_gate(pm_old, mf, require_activation=True,
                             receipt_path=rp_old)    # expired -> fail
        # wrong-repository receipt -> fail (Naya 1's adversarial case)
        wrong = dict(receipt, repository="SomeoneElse/OtherRepo")
        rp_wrong = Path(d) / "receipt_wrong.json"
        rp_wrong.write_bytes(json.dumps(wrong).encode())
        d_wrong = hashlib.sha256(rp_wrong.read_bytes()).hexdigest()
        pm_wrong = Path(d) / "marked_wrong.html"
        pm_wrong.write_text(good.replace(
            "</body>",
            f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d_wrong} --></body>"))
        wrongrepo_v = run_gate(
            pm_wrong, mf, require_activation=True, receipt_path=rp_wrong,
            expected_repo="SoulSchoolAcademy/NayaPOWER")  # wrong repo -> fail
    ok = True
    if not bad_v:
        print("SELF-TEST FAIL: violating page passed the gate")
        ok = False
    else:
        print(f"SELF-TEST: violating page failed with {len(bad_v)} violations (good)")
        for viol in bad_v:
            print("   -", viol)
    if good_v:
        print("SELF-TEST FAIL: lawful page failed the gate:")
        for viol in good_v:
            print("   -", viol)
        ok = False
    else:
        print("SELF-TEST: lawful page passed (good)")
    # --- parser blind-spot regressions (Pair D scorer, 2026-10-09) ---
    # Every heuristic parser had an evasion; each now has a pinned repro.
    blind_spots = [
        ("named light color", "body{background:yellow}", False),
        ("hsl white", "body{background:hsl(0,0%,100%)}", False),
        ("hsl black", "body{background:hsl(0,0%,0%)}", True),
        ("named snow surface", "div{background:snow}", "light"),
        ("script src whitespace", '<script src ="https://e/x.js"></script>', "ext"),
        ("link rel whitespace", '<link rel = "stylesheet" href="x.css">', "ext"),
    ]
    for name, frag, want in blind_spots:
        if want == "light":
            got = check_no_light_surfaces(frag)
            bad = not got
        elif want == "ext":
            got = check_self_contained(frag)
            bad = not got
        else:
            got = _is_dark(frag.split(":", 1)[1].rstrip("}"))
            bad = (got != want)
        if bad:
            print(f"SELF-TEST FAIL: blind-spot '{name}' regressed")
            ok = False
        else:
            print(f"SELF-TEST: blind-spot '{name}' held (good)")
    for name, vv, want_fail in [
            ("no-marker+required", noact_v, True),
            ("valid receipt", okact_v, False),
            ("forged marker", forged_v, True),
            ("expired receipt", expired_v, True),
            ("wrong-repository receipt", wrongrepo_v, True)]:
        has_act = any(x.startswith("ACTIVATION") for x in vv)
        if want_fail and not has_act:
            print(f"SELF-TEST FAIL: activation case '{name}' did not fail")
            ok = False
        elif not want_fail and vv:
            print(f"SELF-TEST FAIL: activation case '{name}' failed: {vv}")
            ok = False
        else:
            print(f"SELF-TEST: activation case '{name}' "
                  f"{'failed as required' if want_fail else 'passed'} (good)")
    # --- second-wave blind-spot regressions (validator, 2026-10-09) ---
    # The first red-team found holes INSIDE the parsers; these were at the
    # BOUNDARIES between parsers: stylesheet vs inline attribute, first stop
    # vs named stop, first layer vs second layer, first declaration vs
    # cascade winner. Durable law: one scanned stream, punctuation stripped
    # before every lookup, cascade winners judged.
    def _rule(decl: str) -> str:
        return "x{%s}" % decl

    wave2 = [
        # (name, fragment, check-kind, must_flag_violation)
        ("inline style light bg",
         '<div style="background:linen">x</div>', "surface_html", True),
        ("inline style light bg-color",
         '<div style="background-color: yellow">x</div>', "surface_html",
         True),
        ("inline style dark bg passes",
         '<div style="background:#0a0a0f">x</div>', "surface_html", False),
        ("inline body bg beats dark stylesheet",
         '<style>body{background:#050507}</style>'
         '<body style="background:#ffffff">x</body>', "rooth_html", True),
        ("inline body dark bg passes",
         '<html style="background:#000"></html>'
         '<body style="background:#050507">x</body>', "rooth_html", False),
        ("gradient named light stop",
         "linear-gradient(white, black)", "notdark", True),
        ("gradient all dark stops",
         "linear-gradient(#0a0a0f, #15151f)", "notdark", False),
        ("gradient uppercase fn",
         "LINEAR-GRADIENT(white, black)", "notdark", True),
        ("gradient rgba heavy stop",
         "linear-gradient(rgba(255,255,255,0.9), black)", "notdark", True),
        ("gradient transparent stop passes",
         "linear-gradient(rgba(0,0,0,0.9), transparent)", "notdark", False),
        ("background shorthand snow+url",
         _rule("background:snow url(x.png)"), "surface", True),
        ("background shorthand url+snow",
         _rule("background:url(x.png) snow"), "surface", True),
        ("background image only: unjudgeable",
         _rule("background:url(x.png)"), "surface", False),
        ("multi-layer second light",
         _rule("background:#050507,#ffffff"), "surface", True),
        ("multi-layer all dark",
         _rule("background:#050507,#0a0a0f"), "surface", False),
        ("text cascade: later dark wins",
         "body{color:#f8f7fb}body{color:#222}", "text", True),
        ("text cascade: later light wins",
         "body{color:#222}body{color:#f8f7fb}", "text", False),
        ("text inline beats stylesheet",
         '<style>body{color:#f8f7fb}</style>'
         '<body style="color:#111">x</body>', "texthtml", True),
        ("text important beats inline",
         '<style>body{color:#f8f7fb !important}</style>'
         '<body style="color:#111">x</body>', "texthtml", False),
        ("text dark inside media",
         "@media(max-width:1px){body{color:#333}}", "text", True),
        ("alpha hairline sheen passes",
         "rgba(255,255,255,0.05)", "notdark", False),
        ("alpha heavy overlay fails",
         _rule("background:rgba(255,255,255,0.9)"), "surface", True),
        ("hex8 translucent white passes",
         "#ffffff0d", "notdark", False),
    ]
    for name, frag, kind, must_flag in wave2:
        if kind == "surface":
            flagged = bool(check_no_light_surfaces(frag))
        elif kind == "surface_html":
            flagged = bool(check_no_light_surfaces(inline_css(frag)))
        elif kind == "notdark":
            # _is_dark True == dark == no violation
            flagged = not _is_dark(frag)
        elif kind == "rooth_html":
            flagged = bool(check_black_root(frag, inline_css(frag)))
        elif kind == "text":
            flagged = bool(check_light_text("", frag))
        elif kind == "texthtml":
            flagged = bool(check_light_text(frag, inline_css(frag)))
        if flagged != must_flag:
            print(f"SELF-TEST FAIL: wave-2 blind-spot '{name}' regressed "
                  f"(flagged={flagged}, want={must_flag})")
            ok = False
        else:
            print(f"SELF-TEST: wave-2 blind-spot '{name}' held (good)")
    # --- encoding bypass regressions (validator round 3, 2026-10-09) ---
    # Durable law: every parser is only as strong as the narrowest
    # ENCODING it doesn't decode. Browsers decode HTML entities in style
    # attribute values (but NOT inside <style> blocks), strip CSS /* */
    # comments, and decode CSS \XX escapes. Each has a pinned repro.
    enc = [
        # (name, fragment, check-kind, must_flag_violation)
        ("entity inline bg",
         '<div style="background:&#119;hite">x</div>', "surface_html", True),
        ("entity hex inline bg",
         '<div style="background:&#x77;hite">x</div>', "surface_html", True),
        ("entity inline bg-color",
         '<div style="background-color:&#121;ellow">x</div>',
         "surface_html", True),
        ("entity in property name",
         '<div style="&#98;ackground:white">x</div>', "surface_html", True),
        ("entity text color cascade",
         '<style>body{color:#f5f5f5}</style>'
         '<body style="color:&#35;111">x</body>', "texthtml", True),
        ("entity body bg cascade",
         '<style>body{background:#050507}</style>'
         '<body style="background:&#35;ffffff">x</body>', "rooth_html", True),
        ("entity double-encoded stays raw",
         '<div style="background:&amp;#119;hite">x</div>',
         "surface_html", False),
        ("entity in style block NOT decoded",
         "<style>div{background:&#119;hite}</style>",
         "surface_html", False),
        ("css escape inline bg",
         '<div style="background:wh\\69te">x</div>', "surface_html", True),
        ("css escape block bg",
         "<style>div{background:wh\\69te}</style>", "surface_html", True),
        ("css escape hex consumes space",
         "<style>div{background:wh\\49 te}</style>", "surface_html", True),
        ("css escape line continuation",
         "<style>div{background:bl\\\nack}</style>", "surface_html", False),
        ("css escape dark stays dark",
         "<style>div{background:bl\\61ck}</style>", "surface_html", False),
        ("css escape uppercase hex",
         "<style>div{background:WH\\49TE}</style>", "surface_html", True),
        ("css comment inline bg",
         '<div style="background:/*x*/white">x</div>', "surface_html", True),
        ("css comment block bg",
         "<style>div{background:/*x*/white}</style>", "surface_html", True),
        ("css comment splits property",
         "<style>div{back/*x*/ground:white}</style>", "surface_html", True),
        ("css comment in text color",
         "<style>body{color:/*x*/#111}</style>", "texthtml", True),
        ("css comment dark passes",
         "<style>div{background:/*ok*/#050507}</style>",
         "surface_html", False),
    ]
    for name, frag, kind, must_flag in enc:
        if kind == "surface_html":
            flagged = bool(check_no_light_surfaces(inline_css(frag)))
        elif kind == "rooth_html":
            flagged = bool(check_black_root(frag, inline_css(frag)))
        elif kind == "texthtml":
            flagged = bool(check_light_text(frag, inline_css(frag)))
        if flagged != must_flag:
            print(f"SELF-TEST FAIL: encoding blind-spot '{name}' regressed "
                  f"(flagged={flagged}, want={must_flag})")
            ok = False
        else:
            print(f"SELF-TEST: encoding blind-spot '{name}' held (good)")
    # --- string/quote regression pins (validator round 4, 2026-10-09) ---
    # Durable law: every regex that strips CSS comments without
    # understanding CSS strings hands the attacker a blindfold to place
    # over the gate. Tokenizer awareness: respect strings before
    # stripping comments; read unquoted attribute values (HTML doesn't
    # require quotes); decode entities in class values before the
    # NO-FREESTYLE prefix match.
    w4known = {"naya-btn"}
    w4 = [
        # (name, fragment, check-kind, must_flag_violation)
        ("string comment-blinding block",
         '<style>.x::before{content:"/*"}.card{background:white}</style>',
         "surface_html", True),
        ("string comment-blinding inline",
         '<div style="content:\'/*\';background:white">x</div>',
         "surface_html", True),
        ("string comment-blinding url",
         '<style>.a{background:url("/*") #fff}</style>',
         "surface_html", True),
        ("string with real comment dark passes",
         '<style>.a{content:"/* ok */";background:#050507}</style>',
         "surface_html", False),
        ("comment still stripped outside strings",
         '<style>div{background:/*x*/white}</style>',
         "surface_html", True),
        ("unclosed comment still swallows tail",
         '<style>div{background:#050507/*</style>',
         "surface_html", False),
        ("unquoted style bg",
         '<div style=background:white>x</div>', "surface_html", True),
        ("unquoted style bg-color",
         '<div style=background-color:yellow>x</div>', "surface_html", True),
        ("unquoted style dark passes",
         '<div style=background:#050507>x</div>', "surface_html", False),
        ("unquoted style spaces around equals",
         '<div style = background:white>x</div>', "surface_html", True),
        ("quoted style not double-counted",
         '<div style="background:#050507">x</div>', "surface_html", False),
        ("unquoted body bg cascade",
         '<style>body{background:#050507}</style>'
         '<body style=background:#ffffff>x</body>', "rooth_html", True),
        ("unquoted body text cascade",
         '<style>body{color:#f5f5f5}</style>'
         '<body style=color:#111>x</body>', "texthtml", True),
        ("entity-encoded freestyle class",
         '<div class="&#110;aya-evil">x</div>', "freestyle", True),
        ("mid-string entity freestyle class",
         '<div class="naya-&#101;vil">x</div>', "freestyle", True),
        ("unquoted freestyle class",
         '<div class=naya-evil>x</div>', "freestyle", True),
        ("lawful canonical class passes",
         '<div class="naya-btn">x</div>', "freestyle", False),
        ("plain non-naya class passes",
         '<div class="container">x</div>', "freestyle", False),
        ("self-closing unquoted style",
         '<div style=background:white/>x</div>', "surface_html", True),
        ("uppercase CLASS attribute",
         '<div CLASS="naya-evil">x</div>', "freestyle", True),
    ]
    for name, frag, kind, must_flag in w4:
        if kind == "surface_html":
            flagged = bool(check_no_light_surfaces(inline_css(frag)))
        elif kind == "rooth_html":
            flagged = bool(check_black_root(frag, inline_css(frag)))
        elif kind == "texthtml":
            flagged = bool(check_light_text(frag, inline_css(frag)))
        elif kind == "freestyle":
            flagged = bool(check_no_freestyle(frag, w4known))
        if flagged != must_flag:
            print(f"SELF-TEST FAIL: wave-4 blind-spot '{name}' regressed "
                  f"(flagged={flagged}, want={must_flag})")
            ok = False
        else:
            print(f"SELF-TEST: wave-4 blind-spot '{name}' held (good)")
    # --- url/tag regression pins (validator round 5, 2026-10-09; ported
    # from the repairs5 line) ---
    # Durable law: every check that scans code text must know where
    # strings begin and end, where url() tokens begin and end, and where
    # a tag's attributes truly end. Tokenizer-awareness is a three-front
    # requirement: strings, urls, tags.
    w5 = [
        # (name, fragment, check-kind, must_flag_violation)
        # S3: /* inside unquoted url() is literal per CSS Syntax — the
        # stripper must not go blind after it.
        ("unquoted url comment-blinding",
         "<style>.e{background:url(data:text/plain,/*);background:linen}</style>",
         "surface_html", True),
        ("unquoted url blinding in style attr",
         '<div style="background:url(data:x,/*);background:white">x</div>',
         "surface_html", True),
        ("url with space is a function token",
         "<style>.e{background:url (x);background:/*c*/white}</style>",
         "surface_html", True),
        ("escape-forged url opener",
         "<style>.e{background:\\75rl(data:text/plain,/*);background:linen}</style>",
         "surface_html", True),
        ("xurl( is not a url token",
         "<style>.e{background:xurl(data:x,/*);background:#050507}</style>",
         "surface_html", False),
        ("comment after closed url still stripped",
         '<style>.e{background:url("x");background:/*c*/white}</style>',
         "surface_html", True),
        ("lawful data url passes",
         "<style>.e{background:url(data:image/png;base64,AAA);background:#050507}</style>",
         "surface_html", False),
        # C1: a > inside a quoted attribute before style must not blind
        # the cascade path — the tag's true extent is what matters.
        ("gt in quoted attr before style",
         '<style>body{color:#f5f5f5}</style>'
         '<body title="x>y" style="color:#111111">x</body>',
         "texthtml", True),
        ("gt in single-quoted attr before style",
         "<style>body{color:#f5f5f5}</style>"
         "<body title='a>b' style='color:#111111'>x</body>",
         "texthtml", True),
        ("style before quoted gt still flags",
         '<style>body{color:#f5f5f5}</style>'
         '<body style="color:#111111" title="x>y">x</body>',
         "texthtml", True),
        ("lawful quoted attr without style passes",
         '<style>body{color:#f5f5f5;background:#050507}</style>'
         '<body title="x>y">x</body>',
         "texthtml", False),
    ]
    for name, frag, kind, must_flag in w5:
        if kind == "surface_html":
            flagged = bool(check_no_light_surfaces(inline_css(frag)))
        elif kind == "rooth_html":
            flagged = bool(check_black_root(frag, inline_css(frag)))
        elif kind == "texthtml":
            flagged = bool(check_light_text(frag, inline_css(frag)))
        elif kind == "freestyle":
            flagged = bool(check_no_freestyle(frag, w4known))
        if flagged != must_flag:
            print(f"SELF-TEST FAIL: wave-5 blind-spot '{name}' regressed "
                  f"(flagged={flagged}, want={must_flag})")
            ok = False
        else:
            print(f"SELF-TEST: wave-5 blind-spot '{name}' held (good)")
    # --- round-4 pins (validator re-validator verdict, 2026-10-09) ---
    # The repairs3 fork lost round-2's tokenizer and @import scanning
    # (branch-base gap); the re-validator found 8 more holes. Each has a
    # pinned repro below. New check-kinds: selfcontained_html (raw html
    # fragment -> check_self_contained), darkscheme_iso / viewport_iso
    # (isolated page carrying ONLY the meta under test — the scaffold's
    # own quoted meta would otherwise mask the over-block), act_obj
    # (non-object receipt JSON -> ACTIVATION violation, never a crash).
    def _iso_page(head_inner: str, scheme: bool = True) -> str:
        # scheme=False: the page carries ONLY the meta under test, so the
        # scaffold's own lawful meta cannot mask an over-block (row 4).
        return ('<!DOCTYPE html><html><head>'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                + ('<meta name="color-scheme" content="dark">' if scheme else '')
                + head_inner +
                '<style>html{background:#050507}'
                'body{background:#050507;color:#f8f7fb}</style>'
                '</head><body>x</body></html>')

    w5 = [
        # (name, fragment, check-kind, must_flag_violation)
        # rows 1/2 — unquoted external references (tokenizer class)
        ("unquoted link rel", '<link rel=stylesheet href="x.css">',
         "selfcontained_html", True),
        ("single-quoted link rel",
         "<link rel='stylesheet' href='x.css'>",
         "selfcontained_html", True),
        ("unquoted link reversed attrs",
         '<link href=x.css rel=stylesheet>', "selfcontained_html", True),
        ("unquoted script src", '<script src=evil.js></script>',
         "selfcontained_html", True),
        ("uppercase unquoted script", '<SCRIPT SRC=HTTPS://E/X.JS></SCRIPT>',
         "selfcontained_html", True),
        ("quoted script still caught",
         '<script src="https://e/x.js"></script>',
         "selfcontained_html", True),
        ("data-uri script passes",
         '<script src="data:text/javascript,1"></script>',
         "selfcontained_html", False),
        # row 4 — lawful unquoted meta must PASS (over-block removal)
        ("unquoted color-scheme meta passes",
         '<meta name=color-scheme content=dark>', "darkscheme_iso", False),
        ("unquoted meta attr order passes",
         '<meta content=dark name=color-scheme>', "darkscheme_iso", False),
        ("missing color-scheme still fails",
         '', "darkscheme_iso", True),
        ("unquoted viewport meta passes",
         '<meta name=viewport content="width=device-width, initial-scale=1">',
         "viewport_iso", False),
        # row 6 — @import at class level (adopted _CSSParser)
        ("at-import url()", '<style>@import url("https://e/x.css");</style>',
         "selfcontained_html", True),
        ("at-import bare string", '<style>@import "https://e/y.css";</style>',
         "selfcontained_html", True),
        ("at-import escaped keyword",
         '<style>@\\69 mport url("https://e/z.css");</style>',
         "selfcontained_html", True),
        ("at-import comment-split prelude",
         '<style>@import/**/url("https://e/w.css");</style>',
         "selfcontained_html", True),
        ("at-import inside comment passes",
         '<style>/* @import url("https://e/q.css"); */</style>',
         "selfcontained_html", False),
        ("at-import data uri passes",
         '<style>@import url("data:text/css,body{}");</style>',
         "selfcontained_html", False),
        # C2c — external url() references fail closed (detection is
        # certain); judging image CONTENT stays fail-open-honest
        ("external bg url() flagged",
         '<style>div{background:url(https://e/t.png)}</style>',
         "selfcontained_html", True),
        ("relative bg url() flagged",
         '<style>div{background:url(tex.png)}</style>',
         "selfcontained_html", True),
        ("data-uri bg url() passes",
         '<style>div{background:url(data:image/png;base64,AAA)}</style>',
         "selfcontained_html", False),
        ("fragment bg url() passes",
         '<style>div{background:url(#grad)}</style>',
         "selfcontained_html", False),
        ("url() inside string passes",
         '<style>div{content:"url(https://e/notreal)"}</style>',
         "selfcontained_html", False),
        # hole 2 — brace-in-attribute rule-iterator injection
        ("brace-in-string attr injection",
         '<div style="content:\'}\';background:white">x</div>',
         "surface_html", True),
        ("escape-formed brace attr injection",
         '<div style="content:\\7d ;background:white">x</div>',
         "surface_html", True),
        ("lawful content string passes",
         '<div style="content:\'hi\';background:#050507">x</div>',
         "surface_html", False),
        # hole 3 — element-scoped custom properties
        ("element-scoped var white",
         '<style>div{background:var(--wash)}</style>'
         '<div style="--wash:white">x</div>', "surface_both", True),
        ("element-scoped var dark passes",
         '<style>div{background:var(--wash)}</style>'
         '<div style="--wash:#050507">x</div>', "surface_both", False),
        # hole 5 — var() fallback per CSS
        ("var fallback white",
         '<style>div{background:var(--missing, white)}</style>',
         "surface_html", True),
        ("var fallback dark passes",
         '<style>div{background:var(--missing, #050507)}</style>',
         "surface_html", False),
        ("var defined beats light fallback",
         '<style>:root{--x:#050507}div{background:var(--x, white)}</style>',
         "surface_html", False),
        # hole 6 — inset box-shadow paints the box
        ("inset shadow white",
         '<div style="box-shadow:inset 0 0 0 9999px white">x</div>',
         "surface_html", True),
        ("inset shadow dark passes",
         '<div style="box-shadow:inset 0 0 0 9999px #050507">x</div>',
         "surface_html", False),
        ("outset glow shadow passes",
         '<div style="box-shadow:0 0 40px rgba(255,255,255,.5)">x</div>',
         "surface_html", False),
        # hole 8 — inert markup + duplicate style=
        # (inert stripping lives in run_gate, so these two run end-to-end)
        ("style in html comment passes",
         '<!-- <style>div{background:white}</style> -->'
         '<div style="background:#050507">x</div>', "run_gate_pass", False),
        ("style in template passes",
         '<template><style>div{background:white}</style></template>'
         '<div style="background:#050507">x</div>', "run_gate_pass", False),
        ("duplicate style= first wins",
         '<div style="background:white" style="background:#050507">x</div>',
         "surface_html", True),
        ("quoted style not double counted",
         '<div style="background:#050507" style="background:white">x</div>',
         "surface_html", False),
    ]
    for name, frag, kind, must_flag in w5:
        if kind == "surface_html":
            flagged = bool(check_no_light_surfaces(inline_css(frag)))
        elif kind == "surface_both":
            flagged = bool(check_no_light_surfaces(inline_css(frag), frag))
        elif kind == "selfcontained_html":
            flagged = bool(check_self_contained(frag))
        elif kind == "darkscheme_iso":
            page = _iso_page(frag, scheme=False)
            flagged = bool(check_dark_scheme(page, inline_css(page)))
        elif kind == "viewport_iso":
            flagged = bool(check_viewport(_iso_page(frag)))
        elif kind == "run_gate_pass":
            # end-to-end through run_gate (inert-HTML stripping lives
            # there, not in the unit helpers)
            with tempfile.TemporaryDirectory() as _td:
                _pp = Path(_td) / "pin.html"
                _pp.write_text(_iso_page(frag))
                flagged = bool(run_gate(_pp, mf))
        if flagged != must_flag:
            print(f"SELF-TEST FAIL: wave-5 blind-spot '{name}' regressed "
                  f"(flagged={flagged}, want={must_flag})")
            ok = False
        else:
            print(f"SELF-TEST: wave-5 blind-spot '{name}' held (good)")
    # hole 7 — non-object receipts fail closed, never crash
    import tempfile as _tf
    with _tf.TemporaryDirectory() as _d:
        for _rname, _payload in [
                ("array receipt", "[1,2,3]"),
                ("string receipt", '"hello"'),
                ("null receipt", "null"),
                ("number receipt", "42")]:
            _rp = Path(_d) / "receipt.json"
            _rp.write_text(_payload)
            try:
                _vv = check_activation("<html></html>", _rp,
                                       expected_repo="SoulSchoolAcademy/NayaPOWER")
                _crashed = None
            except Exception as _e:  # noqa: BLE001 — the crash IS the bug
                _vv, _crashed = [], f"{type(_e).__name__}: {_e}"
            _clean = (_crashed is None
                      and any(str(x).startswith("ACTIVATION") for x in _vv))
            if not _clean:
                print(f"SELF-TEST FAIL: wave-5 '{_rname}' "
                      f"{'crashed: ' + _crashed if _crashed else 'no ACTIVATION violation'}")
                ok = False
            else:
                print(f"SELF-TEST: wave-5 '{_rname}' failed clean (good)")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    args = [a for a in argv if not a.startswith("--")]
    flags = {a for a in argv if a.startswith("--")}
    if not args:
        print(__doc__)
        return 2
    page = Path(args[0])
    manifest = Path(args[1]) if len(args) > 1 else (
        REPO_ROOT / "smart-blocks" / "manifest.json"
    )
    require_activation = "--require-activation" in flags
    receipt_path = None
    expected_repo = None
    for a in argv:
        if a.startswith("--receipt="):
            receipt_path = Path(a.split("=", 1)[1])
        elif a.startswith("--expected-repo="):
            expected_repo = a.split("=", 1)[1]
    if not page.exists():
        print(f"design_gate: no such file: {page}")
        return 2
    violations = run_gate(page, manifest,
                          require_activation=require_activation,
                          receipt_path=receipt_path,
                          expected_repo=expected_repo)
    if violations:
        print(f"DESIGN GATE: FAIL — {len(violations)} violation(s) in {page}:")
        for viol in violations:
            print(f"  ✕ {viol}")
        return 1
    print(f"DESIGN GATE: PASS — {page}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
