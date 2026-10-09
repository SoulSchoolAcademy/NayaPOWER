#!/usr/bin/env python3
"""Hourly report PDF — EXEMPLAR EDITION (Design Contract V1 reference standard).

Rebuild of the Team Naya intelligence-report PDF generator to the exemplar
standard harvested from the nine smart-app reference pages (Phase-1 reads).
Same data layer as the production generator (imports ReportData etc. from
the reporting worktree) — the reporting worktree is NOT modified, so the
hourly cron is untouched.

Exemplar standard (see EXEMPLAR-STANDARD.md for the harvest + law citations):
  Field      --bg:#0B0D12 obsidian, --ink:#F5F7FB, --muted:#AAB2BF (secondary only)
  Spectrum   canonical tokens only; Reports-room accent indigo #6675ff
  Type       24/18/14; body 18px minimum everywhere (D9 closed)
  Jewel      Code-exact faceted diamond clip-path as signature bullets + brand mark
  Elevation  L1 cards #12151D with the depth formula (theme glow + inset top
             light + deep drop shadow) and 1.5pt visible white edge light
  Buttons    black-heart #050505 pill, white text + mark, 1.5pt white edge,
             purple glow (DC-072/073; ground truth: start.html .btn)
  Chips      pill, uppercase micro-type, per-state color (ledger status chips)
  Teams      Shawn's nine team colors for team-coded elements (his direct spec)
  Truth      counts from real data or absent; claim vs AUTH labeled

CLI:
    python3 pdf_report_exemplar.py --type hourly --hours 1 --out /tmp/out.pdf
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

# Data layer: the reporting worktree's generator (read-only import).
sys.path.insert(0, "/home/hatch/workspace/nayapower-worktrees/reporting/tools/reporting")

from report_generator import (  # noqa: E402
    Item,
    ReportData,
    ReportGenerator,
    ScorePoint,
    TeamSection,
    action_plan_text,
    group_by_team,
)

from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import inch  # noqa: E402
from reportlab.platypus import (  # noqa: E402
    Flowable,
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------------------------
# Canonical tokens (naya-design-contract-v1.machine.json — tokens object)
# ---------------------------------------------------------------------------
BG = HexColor("#0B0D12")          # --bg: room default obsidian
BG_RAISE = HexColor("#12151D")    # --bg-raise: L1 boards
BG_CARD = HexColor("#171B25")     # --bg-card: popovers/topmost
EDGE = HexColor("#252B39")        # --edge
INK = HexColor("#F5F7FB")         # --ink: primary text, always
MUTED = HexColor("#AAB2BF")       # --muted: secondary text ONLY
WHITE = HexColor("#FFFFFF")
BTN_BLACK = HexColor("#050505")   # --btn-black

PURPLE = HexColor("#9d75ff")      # --purple: chrome/glow, never solid fill
INDIGO = HexColor("#6675ff")      # --indigo: THIS report's room accent (Reports)
BLUE = HexColor("#55b9ee")
TEAL = HexColor("#40d3bb")
EMERALD = HexColor("#55e39a")      # green pinned; AUTH/verified/pass
LIME = HexColor("#b8ee57")
YELLOW = HexColor("#f1d75a")       # spectrum yellow (not amber)
GOLD = HexColor("#e8b64c")        # contract gold — 7.0-8.99 band
ORANGE = HexColor("#ff9a5a")
RICH_ORANGE = HexColor("#ff7a3d")
RED = HexColor("#ff5a6e")         # contract red: alarm only
MAGENTA = HexColor("#d86cff")

# Shawn's nine team colors — his direct spec 2026-10-08 (contract CD-14:
# recorded as PENDING INPUT, never invented; his word pinned them).
TEAM_COLORS: dict[str, HexColor] = {
    "Learning": HexColor("#FF00FF"),
    "Brain/Memory": HexColor("#800080"),
    "Law/Governance": HexColor("#4B0082"),
    "Architecture/Engineering/Ops": HexColor("#228B22"),
    "Evolution/Succession": HexColor("#FFFF00"),
    "Interfaces/Hub": HexColor("#FFD700"),
    "Knowledge/Intelligence": HexColor("#FFA500"),
    "Proving/Verifying": HexColor("#FF0000"),
    "Innovation": HexColor("#C0C0C0"),
}

PAGE_W, PAGE_H = A4


# ---------------------------------------------------------------------------
# Spectrum flow — Shawn's hard law: NO TWO ADJACENT ELEMENTS SHARE A COLOR.
# Colors exist to break visual flow and signal "new point". Adjacent colors
# must also be perceptually distant (no muddy neighbors like gold-vs-yellow).
# ---------------------------------------------------------------------------

_SPECTRUM_FLOW = [MAGENTA, PURPLE, BLUE, TEAL, EMERALD,
                  LIME, YELLOW, GOLD, ORANGE, RED]

# Minimum perceptual distance between adjacent colors. Tuned so that
# gold-vs-yellow and gold-vs-gold FAIL, gold-vs-blue PASSES.
_MIN_ADJACENT_DISTANCE = 0.30

# Hue families — the distance check alone lets TEAL sit next to LIME and
# both read as "green" (Shawn: "two adjacent green bullet bars"). Adjacent
# elements must ALSO change hue family, not just pass the distance math.
_COLOR_FAMILY = {
    "#d86cff": "violet", "#9d75ff": "violet",
    "#55b9ee": "blue",
    "#40d3bb": "green", "#55e39a": "green", "#b8ee57": "green",
    "#f1d75a": "yellow", "#e8b64c": "yellow",
    "#ff9a5a": "orange",
    "#ff5a6e": "red",
}


def _family(color: HexColor) -> str | None:
    return _COLOR_FAMILY.get(_hx(color).lower())


def _color_distance(c1: HexColor, c2: HexColor) -> float:
    """Redmean-weighted RGB perceptual distance, 0.0 (identical) to ~1.7."""
    r1, g1, b1 = c1.red, c1.green, c1.blue
    r2, g2, b2 = c2.red, c2.green, c2.blue
    rm = (r1 + r2) / 2.0
    dr, dg, db = r1 - r2, g1 - g2, b1 - b2
    return (((2 + rm) * dr * dr + 4 * dg * dg
             + (3 - rm) * db * db) ** 0.5) / 3.0


def _same_color(c1: HexColor, c2: HexColor) -> bool:
    return _hx(c1).lower() == _hx(c2).lower()


class SpectrumCycler:
    """Yields spectrum colors in flow order. Hard guarantees:
    - never returns the same color twice in a row
    - never returns two adjacent colors from the same hue family
      (TEAL-then-LIME both read as "green" — the distance math alone
      does not catch it; Shawn's eye does)
    - always keeps minimum perceptual distance from the previous color
    - falls back to INK (white) rather than violating any rule
    """

    def __init__(self) -> None:
        self._idx = 0
        self._last: HexColor | None = None

    def next(self, exclude: HexColor | None = None) -> HexColor:
        for _ in range(len(_SPECTRUM_FLOW) * 3):
            cand = _SPECTRUM_FLOW[self._idx % len(_SPECTRUM_FLOW)]
            self._idx += 1
            if self._last is not None and _same_color(cand, self._last):
                continue
            if exclude is not None and _same_color(cand, exclude):
                continue
            if (self._last is not None
                    and _family(cand) is not None
                    and _family(cand) == _family(self._last)):
                continue
            if (self._last is not None
                    and _color_distance(cand, self._last)
                    < _MIN_ADJACENT_DISTANCE):
                continue
            self._last = cand
            return cand
        self._last = INK  # white never violates; always a safe fallback
        return INK

    def reset(self) -> None:
        self._last = None


def _distant_or_ink(candidate: HexColor, neighbor: HexColor) -> HexColor:
    """Return candidate unless it's too close to neighbor — then INK.

    Used where a score color would sit next to a team color (e.g. GOLD
    score beside a gold/yellow team header = muddy, unreadable).
    """
    if _color_distance(candidate, neighbor) < _MIN_ADJACENT_DISTANCE:
        return INK
    return candidate
MARGIN = 0.55 * inch
SHADOW = HexColor("#000000")

# Exact Code jewel clip-path as fractional points (x%, y% with y=0 at TOP):
# polygon(50% 0%, 86% 28%, 74% 82%, 50% 100%, 26% 82%, 14% 28%)
JEWEL_PTS = [(0.50, 0.00), (0.86, 0.28), (0.74, 0.82),
             (0.50, 1.00), (0.26, 0.82), (0.14, 0.28)]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _esc(text: str) -> str:
    return (str(text).replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;"))


def _short(text: str, limit: int = 160) -> str:
    """Truncate to a COMPLETE thought. Never mid-word, never mid-sentence
    if a sentence boundary fits.

    - Prefer a sentence end (". ", "! ", "? ") inside the window: the
      bullet then reads as a finished thought, no ellipsis needed.
    - Else cut at the last word boundary and add "…" to signal more.
    - A dangling 1–2 character fragment ("T13 C…") is never shipped:
      back up to the previous word.
    """
    text = re.sub(r"\s+", " ", str(text)).strip()
    if len(text) <= limit:
        return text
    window = text[:limit]
    for sep in (". ", "! ", "? ", "; "):
        idx = window.rfind(sep)
        if idx > limit * 0.35:
            return _fix_dangling_quote(window[:idx + 1].rstrip())
    idx = window.rfind(" ")
    if idx > 0:
        frag = window[idx + 1:]
        if len(frag) <= 2 and idx > limit * 0.3:
            # Fragment too short to mean anything — back up one more word.
            prev = window[:idx].rfind(" ")
            if prev > limit * 0.3:
                idx = prev
        out = window[:idx].rstrip() + "…"
    else:
        out = window.rstrip() + "…"
    return _fix_dangling_quote(out)


def _fix_dangling_quote(s: str) -> str:
    """A truncation that strands an opening quote ("…and 'create the
    most…") or a dangling conjunction ("…creation, and…") reads broken.
    Cut the dangling fragment instead."""
    if not s.endswith("…"):
        return s
    # Dangling conjunction first: "…, and…" → "…".
    s = re.sub(r",?\s+(and|or|but)\u2026$", "\u2026", s)
    for i in range(len(s) - 2, -1, -1):
        if s[i] in "'\"":
            # Apostrophe inside a word ("don't") is not an opener.
            prev = s[i - 1] if i > 0 else " "
            if prev.isalnum():
                continue
            rest = s[i + 1:-1]
            if s[i] not in rest:
                cut = s[:i].rstrip()
                cut = re.sub(r",?\s+and\s*$", "", cut)
                cut = re.sub(r"[,;:]\s*$", "", cut)
                return cut + "…"
            break
    return s


def _hx(color) -> str:
    return "#" + color.hexval()[2:]


def _team_hx(team_name: str) -> str:
    return _hx(TEAM_COLORS.get(team_name, INK))


def _score_color(score: float) -> HexColor:
    if score >= 9.0:
        return EMERALD
    if score >= 7.0:
        return GOLD
    return RED


def _delta_str(sp: ScorePoint, previous: dict) -> str:
    prev = previous.get(sp.area)
    if prev is None or prev == sp.score:
        return "—"
    return f"{sp.score - prev:+.1f}"


# ---------------------------------------------------------------------------
# Human-first language — Shawn's law: "write for a human child first."
# Plain meaning comes FIRST (18px). Technicals are evidence, linked, second.
# PR/issue numbers NEVER appear in body text — they become evidence links.
# ---------------------------------------------------------------------------

_PR_RE = re.compile(r"\bPR[-\s]?(\d+)\b|(?<!\w)#(\d{3,})\b")


def strip_pr_refs(text: str) -> tuple[str, list[str]]:
    """Remove PR/issue numbers from body text. Returns (clean, [numbers])."""
    found: list[str] = []
    def _grab(m: re.Match) -> str:
        num = m.group(1) or m.group(2)
        if num not in found:
            found.append(num)
        return ""
    clean = _PR_RE.sub(_grab, text)
    clean = re.sub(r"\s{2,}", " ", clean).strip()
    clean = re.sub(r"\s+([,.])", r"\1", clean)
    return clean, found


# Jargon → plain human meaning. Ordered longest-first so multi-word
# phrases match before their parts.
_JARGON: list[tuple[str, str]] = [
    ("production readiness", "how ready we are to launch"),
    ("production parity", "whether what's live matches what's built"),
    ("fail-closed", "safely said no"),
    ("fail closed", "safely said no"),
    ("cold retrieve", "finding it fresh, with no memory to lean on"),
    ("cold retrieval", "finding it fresh, with no memory to lean on"),
    ("cold successor", "a fresh teammate with no prior context"),
    ("cold-start", "starting from zero"),
    ("successor reuse", "a future teammate using what we learned"),
    ("learning lineage", "the trail from experience to lesson"),
    ("scorecard receipt", "a graded report card"),
    ("independent verification", "checked by someone else"),
    ("merge-ready", "ready to be approved and added"),
    ("merged", "approved and added"),
    ("merges", "gets approved"),
    ("merge", "approve and add"),
    ("tip", "the latest version"),
    ("CI", "automated checks"),
    ("governance", "the rules"),
    ("ratified", "officially approved"),
    ("candidate", "being considered"),
    ("promotion", "moving up"),
    ("promoted", "moved up"),
    ("rebase", "refresh"),
    ("rebased", "refreshed"),
    ("red", "blocked"),
    ("green", "working"),
    ("worktree", "workspace"),
    ("submodule", "part"),
    ("regression", "something that broke again"),
    ("falsifier", "a test designed to catch mistakes"),
    ("harness", "test setup"),
    ("preregistration", "a public promise of what we'll test"),
    ("replication", "repeat test"),
    ("delta", "change"),
    ("throughput", "how much got done"),
    ("stale", "out of date"),
    ("drift", "slowly going off course"),
    ("quarantine", "set aside safely"),
    ("parity verdict", "match check"),
    ("handshake", "confirmation"),
    ("provenance", "where it came from"),
    ("ingestion", "taking in"),
    ("distillation", "boiling down to the essence"),
    ("compound", "build on itself"),
    ("compounding", "building on itself"),
    ("rows", "items"),
    ("row", "item"),
    ("shebang", "starter line"),
    ("subprocess", "background task"),
    ("bash", "command line"),
    ("script", "tool"),
    ("binary", "program"),
    ("invoke", "run"),
    ("wrapper", "helper"),
    ("401", "connection problem"),
    ("403", "permission problem"),
    ("sb-api", "database tool"),
    ("prod", "live"),
    ("lane", "team"),
    ("authd", "login"),
    ("surrogate", "temporary"),
    ("PR", "fix"),
]


_UUID_RE = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    re.IGNORECASE)
# File paths are evidence, never body text: UPPERCASE/segmented paths.
# Dir segments may start with a digit ("05-MEMORY"); every segment must
# still contain an uppercase letter so dates ("2026/10/08") and brand
# camelCase ("NayaPOWER/x") never match.
_PATH_RE = re.compile(
    r"\b(?:[A-Z0-9][A-Z0-9_-]*/)+(?:[A-Z0-9_.-]*[A-Z][A-Z0-9_.-]*)/?")
# Source tags are database-speak: [memory:...], [source:...], etc.
_TAG_RE = re.compile(r"\[(?:memory|source|src|ref|tag):[^\]]*\]",
                     re.IGNORECASE)
# SCREAMING_CASE / SCREAMING database-speak. The lookahead must include
# every punctuation a token can touch: ")" '"' "=" "/" ";" ":" "!" "?"
# "'" ("VERIFICATION)" and '"PROVISIONAL"' both slipped through before).
_SCREAM_RE = re.compile(r"\b([A-Z]{3,})(?=[\s.,;:!?\"')\]/}=']|$)")
# Proper names and acronyms that must NEVER be lowercased: CONNECT is
# one of the nine Master Nodes (a proper noun); ICU is an acronym.
_PRESERVE_WORDS = {"API", "URL", "UUID", "SQL", "ICU", "CONNECT"}


def humanize(text: str) -> str:
    """Translate technical report language into plain human meaning.

    PR numbers are stripped here too (they become evidence links).
    Output reads for a smart 12-year-old, not an engineer.
    """
    text, _ = strip_pr_refs(text)
    # A parenthetical that exists only to carry a file path is pure
    # metadata ("(filed 2026-10-08 at BRAIN/.../SN-0526/, posted to …)"):
    # remove it WHOLE, before the path strip leaves "at," dangling.
    text = re.sub(r"\([^()]{0,160}?" + _PATH_RE.pattern
                  + r"[^()]{0,160}?\)", "", text)
    # File paths are evidence, never reading flow: remove whole FIRST,
    # while underscores are still intact (paths may contain them).
    text = _PATH_RE.sub("", text)
    # Source tags ([memory:...]) are database-speak: remove.
    text = _TAG_RE.sub("", text)
    # UUIDs are never human reading: remove (case-insensitive).
    text = _UUID_RE.sub("", text)
    # snake_case and SCREAMING_CASE are database-speak: normalize.
    text = re.sub(r"_", " ", text)
    text = re.sub(r"\b([A-Z]{2,})([A-Z][a-z])", r"\1 \2", text)
    # Backticks are engineer noise: remove.
    text = text.replace("`", "")
    # Commit SHAs are engineer noise: remove. A "SHA <hex>" label goes
    # with its hash ("at merge SHA abc123" must not leave "at merge Sha").
    text = re.sub(r"\bSHA\s+[0-9a-f]{7,40}\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\b[0-9a-f]{7,40}\b", "", text)
    # A dangling "@" left by SHA stripping ("branch @ (…") goes too —
    # but "user@example.com" keeps its @.
    text = re.sub(r"\s+@(?=\s*[\s(.,;])", "", text)
    # Residue left by stripping: empty or punctuation-only parens,
    # parens left with a dangling "word /" ("(comments / )" after the
    # reference was stripped), dangling commas, doubled spaces.
    text = re.sub(r"\(\s*[/,;:]?\s*\)", "", text)
    text = re.sub(r"\[\s*[/,;:]?\s*\]", "", text)
    text = re.sub(r"\([^()]*?/\s*\)", "", text)
    text = re.sub(r"\[[^[\]]*?/\s*\]", "", text)
    text = re.sub(r"\s+,", ",", text)
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"\(\s*,", "(", text)
    text = re.sub(r",\s*\)", ")", text)
    # SCREAMING_CASE database-speak: bring down to normal case.
    # (Common acronyms are preserved.)
    text = _SCREAM_RE.sub(
        lambda m: (m.group(1) if m.group(1) in _PRESERVE_WORDS
                   else m.group(1).capitalize()), text)
    # Markdown markers leak from source text: strip.
    text = text.replace("**", "")
    out = f" {text} "
    for jargon, plain in _JARGON:
        out = re.sub(r"\b" + re.escape(jargon) + r"\b", plain, out,
                     flags=re.IGNORECASE)
    out = re.sub(r"\s{2,}", " ", out).strip()
    # Clean up doubled words the substitution can create ("the the").
    out = re.sub(r"\b(\w+) \1\b", r"\1", out, flags=re.IGNORECASE)
    # Tidy sentence ends left ragged by stripping ("word .", "word ,").
    out = re.sub(r"\s+([.,;:!?])", r"\1", out)
    return out


def _score_plain(score: float) -> str:
    """What a score MEANS to a human, first — before the number."""
    if score >= 9.0:
        return "excellent — verified working"
    if score >= 7.0:
        return "good progress, still improving"
    if score >= 5.0:
        return "about halfway there"
    if score >= 3.0:
        return "early stages"
    return "just getting started"


def _area_plain(area: str, score: float, status: str) -> str:
    """One human sentence for an area score. No jargon, no PR numbers."""
    meaning = _score_plain(score)
    verified = ("independently checked" if status == "authoritative"
                else "our own assessment so far")
    return (f"{area}: {meaning} ({score:.1f} out of 10, "
            f"{verified}).")


# ---------------------------------------------------------------------------
# Styles — 24/18/14; body 18px minimum; hierarchy by SIZE, never color
# ---------------------------------------------------------------------------

def _styles() -> dict[str, ParagraphStyle]:
    base = ParagraphStyle("base", fontName="Helvetica", fontSize=18,
                          leading=24, textColor=INK)
    return {
        "base": base,
        "title": ParagraphStyle("title", parent=base,
                                fontName="Helvetica-Bold",
                                fontSize=24, leading=29, textColor=INK),
        "kicker": ParagraphStyle("kicker", parent=base,
                                 fontName="Helvetica-Bold",
                                 fontSize=14, leading=18, textColor=INK),
        "h1": ParagraphStyle("h1", parent=base,
                             fontName="Helvetica-Bold",
                             fontSize=24, leading=29, textColor=INK,
                             spaceBefore=16, spaceAfter=8),
        "h2": ParagraphStyle("h2", parent=base,
                             fontName="Helvetica-Bold",
                             fontSize=18, leading=23, textColor=INK,
                             spaceBefore=10, spaceAfter=6),
        "body": base,
        # Shawn's law: ZERO gray text anywhere. Secondary text is 14px
        # white, never muted — muted (#AAB2BF) is unreadable on dark.
        "detail": ParagraphStyle("detail", parent=base,
                                 fontSize=14, leading=19, textColor=INK),
        "detail_white": ParagraphStyle("detail_white", parent=base,
                                       fontSize=14, leading=19,
                                       textColor=INK),
        # Bullets: color changes signal "new point" — paired with real
        # breathing room (Shawn's law: separation is spacing + color).
        "bullet": ParagraphStyle("bullet", parent=base, leftIndent=6,
                                 spaceBefore=7, spaceAfter=9),
        "chip": ParagraphStyle("chip", parent=base,
                               fontName="Helvetica-Bold",
                               fontSize=14, leading=18, textColor=INK,
                               alignment=1),
        "cell": ParagraphStyle("cell", parent=base, fontSize=18,
                               leading=23, textColor=INK),
        "cell_bold": ParagraphStyle("cell_bold", parent=base,
                                    fontName="Helvetica-Bold", fontSize=18,
                                    leading=23, textColor=INK),
        "cell_head": ParagraphStyle("cell_head", parent=base,
                                    fontName="Helvetica-Bold", fontSize=14,
                                    leading=18, textColor=INK),
        "btn": ParagraphStyle("btn", parent=base,
                              fontName="Helvetica-Bold",
                              fontSize=18, leading=22, textColor=WHITE,
                              alignment=1),
    }


# ---------------------------------------------------------------------------
# Custom flowables — jewel, elevation, button, chip
# ---------------------------------------------------------------------------

class JewelMark(Flowable):
    """Code-exact faceted diamond: theme aura + white-hot core + white edge.

    DC-070. clip-path polygon(50% 0%, 86% 28%, 74% 82%, 50% 100%,
    26% 82%, 14% 28%).
    """

    def __init__(self, size: float, color: HexColor, aura: bool = True):
        super().__init__()
        self.size = size
        self.color = color
        self.aura = aura

    def wrap(self, aW, aH):
        return self.size, self.size

    def _poly(self, canv, cx, cy, scale):
        pts = []
        for fx, fy in JEWEL_PTS:
            # CSS y=0 is TOP; canvas y=0 is BOTTOM.
            pts.append((cx + (fx - 0.5) * self.size * scale,
                        cy + (0.5 - fy) * self.size * scale))
        p = canv.beginPath()
        p.moveTo(*pts[0])
        for pt in pts[1:]:
            p.lineTo(*pt)
        p.close()
        return p

    def draw(self):
        c = self.canv
        cx, cy = self.size / 2, self.size / 2
        c.saveState()
        if self.aura:
            c.setFillColor(self.color)
            c.setFillAlpha(0.30)
            c.setStrokeColor(self.color)
            c.setStrokeAlpha(0.30)
            c.setLineWidth(1.2)
            c.drawPath(self._poly(c, cx, cy, 1.35), stroke=1, fill=1)
        # Body: the jewel color.
        c.setFillColor(self.color)
        c.setFillAlpha(1)
        c.setStrokeColor(WHITE)
        c.setStrokeAlpha(0.95)
        c.setLineWidth(1.1)
        c.drawPath(self._poly(c, cx, cy, 1.0), stroke=1, fill=1)
        # White-hot core (small diamond at the crown).
        c.setFillColor(WHITE)
        c.setFillAlpha(0.95)
        c.drawPath(self._poly(c, cx, cy + self.size * 0.12, 0.38),
                   stroke=0, fill=1)
        c.restoreState()


class GlowCard(Flowable):
    """L1 elevation card — the depth formula (DC-065).

    Outer glow in the theme color + inset 0 1px #fff6 top light +
    deep drop shadow 0 18px 42px rgba(0,0,0,.73), 1.5pt white edge light
    visible at rest (A-LAW-05, briefing governs per X-1).
    """

    def __init__(self, content, accent: HexColor,
                 pad: float = 12, radius: float = 13):
        super().__init__()
        self.content = content
        self.accent = accent
        self.pad = pad
        self.radius = radius
        self._w = self._h = 0.0

    def wrap(self, aW, aH):
        inner_w = aW - 2 * self.pad
        _w, _h = self.content.wrap(inner_w, aH)
        self._w = aW
        self._h = _h + 2 * self.pad
        return self._w, self._h

    def draw(self):
        c = self.canv
        w, h, r, p = self._w, self._h, self.radius, self.pad
        c.saveState()
        # 1. Deep drop shadow (CD-8: L1 0 18px 42px rgba(0,0,0,.73)).
        c.setFillColor(SHADOW)
        c.setFillAlpha(0.73)
        c.roundRect(3, -7, w - 3, h, r, stroke=0, fill=1)
        # 2. Outer glow in the theme color.
        c.setFillColor(self.accent)
        c.setFillAlpha(0.16)
        c.roundRect(-5, -5, w + 10, h + 10, r + 5, stroke=0, fill=1)
        # 3. Panel.
        c.setFillColor(BG_RAISE)
        c.setFillAlpha(1)
        c.roundRect(0, 0, w, h, r, stroke=0, fill=1)
        # 4. White edge light 1.5pt, visible at rest.
        c.setStrokeColor(WHITE)
        c.setStrokeAlpha(0.9)
        c.setLineWidth(1.5)
        c.roundRect(0.75, 0.75, w - 1.5, h - 1.5, r - 1, stroke=1, fill=0)
        # 5. Inset top light: inset 0 1px #fff6.
        c.setStrokeColor(WHITE)
        c.setStrokeAlpha(0.38)
        c.setLineWidth(1)
        c.line(r, h - 2.5, w - r, h - 2.5)
        c.restoreState()
        self.content.drawOn(c, p, p)


class ButtonBar(Flowable):
    """Button-law bar (DC-072/073): black heart, white voice, visible skin.

    background #050505 · color #fff ALWAYS · 1.5pt white edge light at rest ·
    pill 999px · purple glow. Text always white with a mark — never colored.
    """

    def __init__(self, text: str, st: dict, glow: HexColor = PURPLE,
                 pad_v: float = 13):
        super().__init__()
        self.st = st
        self.glow = glow
        self.pad_v = pad_v
        self._w = self._h = 0.0
        # HARD LAW: text NEVER overlaps the button or anything else.
        # Measure at render width; truncate with ellipsis rather than
        # overflow. A clipped button is an instant design fail.
        self.text = self._fit_text(text, st["btn"])

    @staticmethod
    def _fit_text(text: str, style, max_width: float = 7.0 * inch,
                  limit: int = 120) -> str:
        from reportlab.pdfbase.pdfmetrics import stringWidth
        text = re.sub(r"\s+", " ", str(text)).strip()
        if len(text) > limit:
            text = text[:limit].rstrip() + "…"
        # Shrink until it fits the button's inner width — backing up to
        # word boundaries, never cutting mid-word.
        while text and stringWidth(text, style.fontName,
                                   style.fontSize) > max_width - 60:
            cut = text[:-2].rstrip("…").rstrip()
            sp = cut.rfind(" ")
            text = (cut[:sp] if sp > 10 else cut[:-1]).rstrip() + "…"
        return text or "—"

    def _make_para(self):
        return Paragraph("◆&nbsp;&nbsp;" + _esc(self.text), self.st["btn"])

    def wrap(self, aW, aH):
        self._para = self._make_para()
        _w, _h = self._para.wrap(aW - 44, aH)
        self._w = aW
        self._h = _h + 2 * self.pad_v
        return self._w, self._h

    def draw(self):
        c = self.canv
        w, h = self._w, self._h
        r = h / 2
        c.saveState()
        # Purple glow at rest (chrome ignites purple).
        c.setFillColor(self.glow)
        c.setFillAlpha(0.28)
        c.roundRect(-6, -6, w + 12, h + 12, r + 6, stroke=0, fill=1)
        # Deep shadow.
        c.setFillColor(SHADOW)
        c.setFillAlpha(0.73)
        c.roundRect(2, -6, w - 2, h, r, stroke=0, fill=1)
        # Black heart.
        c.setFillColor(BTN_BLACK)
        c.setFillAlpha(1)
        c.roundRect(0, 0, w, h, r, stroke=0, fill=1)
        # White edge light 1.5pt, visible at rest.
        c.setStrokeColor(WHITE)
        c.setStrokeAlpha(0.95)
        c.setLineWidth(1.5)
        c.roundRect(0.75, 0.75, w - 1.5, h - 1.5, r - 1, stroke=1, fill=0)
        # Inset top light.
        c.setStrokeColor(WHITE)
        c.setStrokeAlpha(0.32)
        c.setLineWidth(1)
        c.line(r, h - 3, w - r, h - 3)
        c.restoreState()
        self._para.drawOn(c, 22, self.pad_v)


class Chip(Flowable):
    """Pill chip — uppercase micro-type, per-state color (DC-077).

    Ledger status-chip pattern: colored edge + white text. The quiet
    (claim) variant uses a dimmed WHITE edge — never gray.
    """

    def __init__(self, text: str, color: HexColor, st: dict,
                 edge_alpha: float = 0.95, glow_alpha: float = 0.22):
        super().__init__()
        self.text = text.upper()
        self.color = color
        self.st = st
        self.edge_alpha = edge_alpha
        self.glow_alpha = glow_alpha
        self._w = self._h = 0.0
        self._para = Paragraph(_esc(self.text), st["chip"])

    def wrap(self, aW, aH):
        _w, _h = self._para.wrap(aW, aH)
        self._w = min(_w + 26, aW)
        self._h = _h + 12
        return self._w, self._h

    def draw(self):
        c = self.canv
        w, h = self._w, self._h
        r = h / 2
        c.saveState()
        c.setFillColor(BTN_BLACK)
        c.setFillAlpha(1)
        c.roundRect(0, 0, w, h, r, stroke=0, fill=1)
        c.setStrokeColor(self.color)
        c.setStrokeAlpha(self.edge_alpha)
        c.setLineWidth(1.5)
        c.roundRect(0.75, 0.75, w - 1.5, h - 1.5, r - 1, stroke=1, fill=0)
        c.setFillColor(self.color)
        c.setFillAlpha(self.glow_alpha)
        c.roundRect(0, 0, w, h, r, stroke=0, fill=1)
        c.restoreState()
        self._para.drawOn(c, 13, 6)


# ---------------------------------------------------------------------------
# Composite builders
# ---------------------------------------------------------------------------

def _jewel_bullet(st: dict, color: HexColor, text: str,
                  size: float = 20) -> Table:
    """Jewel-bullet row: precision diamond + 18px white text (reports.html)."""
    body = Paragraph(text, st["bullet"])
    t = Table([[JewelMark(size, color), body]],
              colWidths=[size + 10, None])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    return t

# ---------------------------------------------------------------------------
# Executive content — computed from data, never invented (truth law DC-091)
# ---------------------------------------------------------------------------

def _headline(data: ReportData, sections: list[TeamSection]) -> str:
    bits: list[str] = []
    moves: list[tuple[float, str, float, float]] = []
    for sp in data.scores:
        prev = data.previous_scores.get(sp.area)
        if prev is not None and prev != sp.score:
            moves.append((abs(sp.score - prev), sp.area, prev, sp.score))
    moves.sort(reverse=True)
    if moves:
        _, area, prev, now = moves[0]
        bits.append(f"{area} {prev:.1f}→{now:.1f}")
    n_ach = sum(len(s.achievements) for s in sections)
    if n_ach:
        bits.append(f"{n_ach} achievements landed")
    all_holes: list[Item] = []
    for s in sections:
        all_holes.extend(s.holes)
    all_holes.sort(key=lambda i: -i.priority)
    if all_holes:
        bits.append("top blocker: " + _short(all_holes[0].text, 90))
    at_floor = sum(1 for sp in data.scores if sp.score >= 9.0)
    if at_floor:
        bits.append(f"{at_floor} area{'s' if at_floor != 1 else ''} at 9.0+")
    return " · ".join(bits) if bits else "steady period — no score movement recorded"


def _top_wins(sections: list[TeamSection], limit: int = 6
              ) -> list[tuple[str, Item]]:
    wins: list[tuple[str, Item]] = []
    for s in sections:
        for a in s.achievements[:3]:
            wins.append((s.name, a))
    return wins[:limit]


def _top_misses(sections: list[TeamSection], unassigned: dict,
                limit: int = 6) -> list[tuple[str, Item]]:
    misses: list[tuple[str, Item]] = []
    for s in sections:
        for h in sorted(s.holes, key=lambda i: -i.priority)[:2]:
            misses.append((s.name, h))
    for h in unassigned.get("holes", [])[:2]:
        misses.append(("Cross-team", h))
    misses.sort(key=lambda t: -t[1].priority)
    return misses[:limit]


_DECISION_RE = re.compile(
    r"\b(needs?\b|awaiting|gate\b|decision|shawn'?s word|ratif\w*|"
    r"merge\b.*\bneeds\b|only he can|protected gate)",
    re.IGNORECASE,
)


def _decisions(sections: list[TeamSection],
               unassigned: dict) -> list[tuple[str, Item]]:
    found: list[tuple[str, Item]] = []
    seen: set[str] = set()
    for s in sections:
        for it in list(s.holes) + list(s.priorities):
            if _DECISION_RE.search(it.text) and it.text not in seen:
                seen.add(it.text)
                found.append((s.name, it))
    for it in unassigned.get("holes", []) + unassigned.get("priorities", []):
        if _DECISION_RE.search(it.text) and it.text not in seen:
            seen.add(it.text)
            found.append(("Cross-team", it))
    return found[:5]


def _single_priority(sections: list[TeamSection], unassigned: dict) -> str:
    misses = _top_misses(sections, unassigned, limit=1)
    if misses:
        team, item = misses[0]
        return f"[{team}] {_short(item.text, 200)}"
    for s in sections:
        plan = action_plan_text(s)
        if "No recorded actions" not in plan:
            return f"[{s.name}] {_short(plan, 200)}"
    return "No recorded priority this window."


# ---------------------------------------------------------------------------
# Section builders — exemplar styling
# ---------------------------------------------------------------------------

def _metrics_bar(st: dict, data: ReportData,
                 cycler: SpectrumCycler) -> Table:
    """Metrics strip — five L1 glow-cards, spectrum-cycled accents.

    Ground truth: reports.html weekStrip dayTiles, one tile per day each in
    its own spectrum color. Accents cycle with no adjacent repeats.
    """
    gh = data.github_snapshot
    sb = data.supabase_snapshot
    prs = gh.get("prs", []) if not gh.get("error") else []
    merged = sum(1 for p in prs if p.get("merged"))
    open_prs = sum(1 for p in prs if not p.get("merged"))
    comments = len(gh.get("comments", [])) if not gh.get("error") else "n/a"
    if sb.get("error"):
        sb_txt = "unavailable"
    else:
        counts = sb.get("counts", {})
        # "CANDIDATE=36" is database-speak: say "36 being considered".
        parts = []
        for k, v in counts.items():
            label = humanize(k).lower().strip() or "items"
            parts.append(f"{v} {label}")
        sb_txt = ", ".join(parts) or "no rows"

    metrics = [
        ("PRs touched", f"{len(prs)} · {merged} approved and added"),
        ("Open PRs", f"{open_prs}"),
        ("Team feed", f"{comments} messages"),
        ("Evidence", _short(sb_txt, 40)),
        ("Window", data.since.strftime("%m-%d %H:%M")),
    ]
    width = (PAGE_W - 2 * MARGIN) / 5
    row = []
    for label, value in metrics:
        accent = cycler.next()
        inner = [
            Paragraph(f"<b>{_esc(humanize(label))}</b>", st["detail_white"]),
            Paragraph(_esc(humanize(_short(value, 48))), st["detail_white"]),
        ]
        inner_t = Table([[inner[0]], [inner[1]]], colWidths=[width - 24])
        inner_t.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ]))
        row.append(GlowCard(inner_t, accent, pad=8))
    t = Table([row], colWidths=[width] * 5)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def _highlight_boxes(st: dict, data: ReportData,
                     sections: list[TeamSection],
                     cycler: SpectrumCycler) -> Table:
    """Callout cards — jewel-bullet titles, L1 elevation (DC-070 + DC-065).

    Colors cycle the spectrum: no two adjacent boxes share a color or sit
    in muddy proximity (Shawn's hard law). Semantic colors (red = alarm)
    yield to the alternation law — the TITLE text already signals urgency.
    """
    boxes: list[tuple[str, str]] = []

    moves: list[tuple[float, str, float, float, str]] = []
    for sp in data.scores:
        prev = data.previous_scores.get(sp.area)
        if prev is not None and prev != sp.score:
            moves.append((abs(sp.score - prev), sp.area, prev, sp.score,
                          sp.status))
    moves.sort(reverse=True)
    if moves:
        _, area, prev, now, status = moves[0]
        d = now - prev
        direction = "up" if d > 0 else "down"
        boxes.append((
            "BIGGEST MOVE",
            f"{_esc(humanize(area))} {prev:.1f} → <b>{now:.1f}</b> "
            f"({direction}, {_esc(status)})",
        ))

    misses = _top_misses(sections, {}, limit=1)
    if misses:
        team, item = misses[0]
        clean, _ = strip_pr_refs(item.text)
        boxes.append((
            "TOP BLOCKER",
            f"[{_esc(humanize(team))}] {_esc(humanize(_short(clean, 110)))}",
        ))

    n_ach = sum(len(s.achievements) for s in sections)
    boxes.append((
        "THROUGHPUT",
        f"<b>{n_ach}</b> achievements recorded this window",
    ))

    at_floor = [sp for sp in data.scores if sp.score >= 9.0]
    boxes.append((
        "AT 9.0+ FLOOR",
        f"<b>{len(at_floor)}</b> of {len(data.scores)} "
        f"area{'s' if len(data.scores) != 1 else ''} verified excellent"
        + (": " + ", ".join(_esc(humanize(sp.area)) for sp in at_floor[:3])
           if at_floor else ""),
    ))

    auth = [sp for sp in data.scores if sp.status == "authoritative"]
    if auth:
        sp = auth[0]
        boxes.append((
            "AUTHORITATIVE",
            f"{_esc(humanize(sp.area))} <b>{sp.score:.1f}</b> "
            f"({_score_plain(sp.score)})",
        ))

    boxes = boxes[:5]
    # Full-width callout strips: jewel + colored title + 18px body.
    out: list = []
    avail = PAGE_W - 2 * MARGIN
    for title, body in boxes:
        color = cycler.next()
        text = (f'<font color="{_hx(color)}"><b>{_esc(title)}</b></font>'
                f" &nbsp;{body}")
        inner = Table(
            [[JewelMark(26, color), Paragraph(text, st["body"])]],
            colWidths=[36, avail - 36 - 28])
        inner.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 2),
            ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        out.append(GlowCard(inner, color, pad=10))
        out.append(Spacer(1, 8))
    return out


def _auth_chip(st: dict, status: str) -> Chip:
    """Truth dialect (BF-006): AUTH = emerald (verified — the number survived
    contact with reality); claim = PURPLE (self-reported, awaiting its stamp —
    shown honestly, never hidden). State is color; color is state."""
    if status == "authoritative":
        return Chip("AUTH", EMERALD, st)
    return Chip("claim", PURPLE, st, edge_alpha=0.55, glow_alpha=0.08)


def _scorecard_table(st: dict, data: ReportData) -> Table:
    """Team × score dashboard — L1 card, 1.5pt white edge, team colors.

    BF-001/BF-009 (seat synthesis): a color MUST mean the same thing every
    time. Each team owns ONE fixed identity hue — the color IS the name.
    No positional alternation: two adjacent Architecture rows are both green
    because green MEANS Architecture. Separation between areas comes from
    dividers, not color rotation. (DC-041 amendment: identity first,
    flow-order second.)
    """
    from report_generator import AREA_TO_TEAM

    header = [
        Paragraph("<b>Team</b>", st["cell_head"]),
        Paragraph("<b>Area</b>", st["cell_head"]),
        Paragraph("<b>Score</b>", st["cell_head"]),
        Paragraph("<b>Status</b>", st["cell_head"]),
        Paragraph("<b>Δ</b>", st["cell_head"]),
    ]
    rows = [header]
    table_style_cmds = []
    prev_team: str | None = None
    for i, sp in enumerate(data.scores):
        team_name = AREA_TO_TEAM.get(sp.area, "—")
        # Identity color — pinned, never rotated (BF-009).
        team_color = TEAM_COLORS.get(team_name, INK)
        # Team boundary: stronger divider when the team changes (BF-009
        # grouping cue — areas under one team read as a family).
        if prev_team is not None and team_name != prev_team:
            table_style_cmds.append(
                ("LINEABOVE", (0, i + 1), (-1, i + 1), 1.0, EDGE))
        prev_team = team_name
        # Score color keeps perceptual distance from the DISPLAYED team
        # color: a GOLD score beside a gold team header is muddy.
        color = _distant_or_ink(_score_color(sp.score), team_color)
        thx = _hx(team_color)
        # Break ONLY at slashes — never mid-word (the old report's
        # "Engine/ering" wraps were a readability failure).
        team_cell = _esc(team_name).replace("/", "/<br/>")
        rows.append([
            Paragraph(f'<font color="{thx}"><b>{team_cell}</b></font>',
                      st["cell"]),
            Paragraph(_esc(sp.area), st["cell"]),
            Paragraph(f'<font color="{_hx(color)}">'
                      f"<b>{sp.score:.1f}</b></font>", st["cell"]),
            _auth_chip(st, sp.status),
            Paragraph(_esc(_delta_str(sp, data.previous_scores)),
                      st["cell"]),
        ])

    avail = PAGE_W - 2 * MARGIN
    widths = [2.35 * inch, 1.65 * inch, 0.70 * inch,
              1.00 * inch, 0.60 * inch]
    scale = avail / sum(widths)
    widths = [w * scale for w in widths]
    # A long scorecard is a BOARD (DC-077), not a card: it must flow across
    # pages, so it renders as a splittable table with the 1.5pt white edge
    # light applied directly (A-LAW-05).
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BG_CARD),
        ("BACKGROUND", (0, 1), (-1, -1), BG_RAISE),
        ("BOX", (0, 0), (-1, -1), 1.5, WHITE),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, WHITE),
        ("LINEBELOW", (0, 1), (-1, -2), 0.75, EDGE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ] + table_style_cmds))
    return t

def _team_section_flowables(st: dict, i: int, sec: TeamSection,
                            data: ReportData,
                            cycler: SpectrumCycler,
                            evidence: list[str]) -> list:
    """One team's section — human first, always.

    - 24px team-colored header (Shawn's spec)
    - Plain-language status line FIRST (18px): what a human needs to know
    - Bullets cycle the spectrum: NEVER two adjacent the same color,
      always perceptually distant (Shawn's hard law)
    - Every bullet humanized; PR numbers stripped to evidence links
    - Score colors keep distance from the team header color (no muddy
      gold-on-gold); fall back to white when too close
    """
    out: list = []
    thx = _team_hx(sec.name)
    team_color = TEAM_COLORS.get(sec.name, INK)

    out.append(Paragraph(
        f'<font color="{thx}"><b>Team {i}: {_esc(sec.name)}</b></font>',
        st["h1"]))
    # Human status line FIRST: what does this team's hour MEAN?
    out.append(Paragraph(_esc(_team_human_status(sec)), st["body"]))
    out.append(Spacer(1, 6))

    chips: list[str] = []
    for sp in sec.scores:
        # Score color must stay readable next to the team header:
        # too close (gold score + gold team) → white instead.
        scolor = _distant_or_ink(_score_color(sp.score), team_color)
        tag = "AUTH" if sp.status == "authoritative" else "claim"
        delta = _delta_str(sp, data.previous_scores)
        chips.append(
            f'<font color="{_hx(scolor)}"><b>{sp.score:.1f}</b></font>'
            f" {_esc(humanize(sp.area))} · {tag} · Δ{delta}"
        )
    chip_txt = " &nbsp;&nbsp; ".join(chips) if chips else \
        "cross-cutting — no direct area score"
    out.append(Paragraph(chip_txt, st["body"]))
    out.append(Spacer(1, 6))
    # Plain-English score meanings, one line each.
    for sp in sec.scores:
        out.append(Paragraph(
            f"• {_esc(_area_plain(sp.area, sp.score, sp.status))}",
            st["detail_white"]))
    out.append(Spacer(1, 6))

    out.append(Paragraph("<b>The work that landed.</b>", st["h2"]))
    done = sec.achievements[:5]
    if done:
        for a in done:
            clean, prs = strip_pr_refs(a.text)
            evidence.extend(prs)
            out.append(_jewel_bullet(
                st, cycler.next(exclude=team_color),
                _esc(humanize(_short(clean, 200)))))
    else:
        out.append(Paragraph("Nothing recorded this window.", st["body"]))

    holes = sorted(sec.holes, key=lambda x: -x.priority)[:3]
    if holes:
        out.append(Paragraph("<b>What needs attention</b>", st["h2"]))
        for j, h in enumerate(holes, 1):
            clean, prs = strip_pr_refs(h.text)
            evidence.extend(prs)
            # Holes are the alarm's business — but STILL cycle: never
            # two reds in a row (Shawn's law beats the alarm convention;
            # the "What needs attention" header already signals urgency).
            out.append(_jewel_bullet(
                st, cycler.next(),
                f"<b>{j}.</b> {_esc(humanize(_short(clean, 200)))}"))

    out.append(Paragraph("<b>The road to 10.</b>", st["h2"]))
    plan = action_plan_text(sec).replace("_", "")
    plan_clean, plan_prs = strip_pr_refs(plan)
    evidence.extend(plan_prs)
    out.append(Paragraph(_esc(humanize(_short(plan_clean, 260))),
                         st["body"]))

    if sec.priorities:
        out.append(Paragraph("<b>Next</b>", st["h2"]))
        for p in sec.priorities[:3]:
            clean, prs = strip_pr_refs(p.text)
            evidence.extend(prs)
            out.append(_jewel_bullet(
                st, cycler.next(exclude=team_color),
                _esc(humanize(_short(clean, 200)))))

    out.append(HRFlowable(width="100%", thickness=1.5, color=EDGE,
                          spaceAfter=6, spaceBefore=10))
    return out


def _team_human_status(sec: TeamSection) -> str:
    """One plain sentence: what does this team's period MEAN to a human?"""
    def _n(n: int, singular: str, plural: str | None = None) -> str:
        w = singular if n == 1 else (plural or singular + "s")
        return f"{n} {w}"
    bits: list[str] = []
    n_done = len(sec.achievements)
    n_holes = len(sec.holes)
    if n_done and not n_holes:
        bits.append(f"a strong period — {_n(n_done, 'thing')} got done, "
                    "nothing blocked")
    elif n_done and n_holes:
        bits.append(f"moving forward — {_n(n_done, 'thing')} done, "
                    f"{_n(n_holes, 'blocker')} needing attention")
    elif n_holes:
        bits.append(f"a tough period — {_n(n_holes, 'blocker')}, "
                    "working through them")
    else:
        bits.append("a quiet period — nothing major recorded")
    best = None
    if sec.scores:
        best = max(sec.scores, key=lambda s: s.score)
        bits.append(f"strongest area: {humanize(best.area)} "
                    f"({_score_plain(best.score)})")
    return f"The {sec.name} team had " + ", ".join(bits) + "."


def _decisions_only(st: dict, sections: list[TeamSection],
                    unassigned: dict, cycler: SpectrumCycler,
                    evidence: list[str]) -> list:
    """Decisions needed — the ONLY cross-team list. Wins and misses were
    removed: they duplicated the team sections (Shawn: "you have it twice").
    Every bullet cycles the spectrum; PR numbers become evidence."""
    out: list = []
    out.append(Paragraph("3 · Decisions needed", st["h1"]))
    out.append(Paragraph(
        "Only items genuinely needing a human call appear here — "
        "everything else lives in its team section above.", st["body"]))
    decisions = _decisions(sections, unassigned)
    if decisions:
        for j, (team, item) in enumerate(decisions, 1):
            clean, prs = strip_pr_refs(item.text)
            evidence.extend(prs)
            out.append(_jewel_bullet(
                st, cycler.next(),
                f"<b>{j} · [{_esc(humanize(team))}]</b> "
                f"{_esc(humanize(_short(clean, 240)))}"))
            out.append(Paragraph(
                "Our suggestion: pick the option that helps the most; "
                "only bring it to Shawn if it's something only he can "
                "approve.", st["detail_white"]))
    else:
        out.append(Paragraph("None recorded this window — "
                             "the math is deciding.", st["body"]))
    return out


# ---------------------------------------------------------------------------
# Page template — obsidian field, jewel brand, ambient glow
# ---------------------------------------------------------------------------

# Actual Naya brand mark (harvested from reports.html NAYA_LOGO).
_LOGO_PATH = str(Path(__file__).parent / "naya-logo.png")


def _header_footer(canvas, doc, kind: str, stamp: str):
    canvas.saveState()
    # FIELD: sovereign darkness, the room default (DC-020).
    canvas.setFillColor(BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # Ambient: low-opacity jewel light, never distracting (CD-2 ≤ 0.25).
    canvas.setFillColor(INDIGO)
    canvas.setFillAlpha(0.055)
    canvas.ellipse(PAGE_W * 0.55, PAGE_H * 0.62,
                   PAGE_W * 1.15, PAGE_H * 1.05, stroke=0, fill=1)
    canvas.setFillColor(PURPLE)
    canvas.setFillAlpha(0.045)
    canvas.ellipse(-PAGE_W * 0.25, -PAGE_H * 0.30,
                   PAGE_W * 0.55, PAGE_H * 0.45, stroke=0, fill=1)
    canvas.setFillAlpha(1)

    # Brand lockup, top-left always (DC-061): THE ACTUAL NAYA LOGO +
    # wordmark. Never a placeholder diamond.
    # Type scale is strict 24/18/14 — no 15px, 11px, 10px anywhere.
    try:
        canvas.drawImage(_LOGO_PATH, MARGIN, PAGE_H - 0.78 * inch,
                         width=0.52 * inch, height=0.52 * inch,
                         mask="auto", preserveAspectRatio=True)
    except Exception:
        jewel = JewelMark(30, INDIGO)  # last-resort fallback only
        jewel.canv = canvas
        jewel.drawOn(canvas, MARGIN, PAGE_H - 0.72 * inch)

    canvas.setFont("Helvetica-Bold", 18)
    canvas.setFillColor(INK)
    canvas.drawString(MARGIN + 44, PAGE_H - 0.50 * inch, "NAYA")
    canvas.setFont("Helvetica", 14)
    canvas.setFillColor(INK)  # white, never gray
    canvas.drawString(MARGIN + 44, PAGE_H - 0.70 * inch,
                      "TEAM INTELLIGENCE")

    # Header rule — visible edge.
    canvas.setStrokeColor(WHITE)
    canvas.setStrokeAlpha(0.35)
    canvas.setLineWidth(1.5)
    canvas.line(MARGIN, PAGE_H - 0.85 * inch,
                PAGE_W - MARGIN, PAGE_H - 0.85 * inch)
    canvas.setStrokeAlpha(1)

    # Right: stamp only (kind already rides the title-block chip).
    canvas.setFont("Helvetica", 14)
    canvas.setFillColor(INK)  # white, never gray
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.60 * inch, stamp)

    # Footer.
    canvas.setStrokeColor(WHITE)
    canvas.setStrokeAlpha(0.25)
    canvas.setLineWidth(1)
    canvas.line(MARGIN, 0.62 * inch, PAGE_W - MARGIN, 0.62 * inch)
    canvas.setStrokeAlpha(1)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.setFillColor(INK)
    canvas.drawString(MARGIN, 0.44 * inch, "PROVE THAT THE BRAIN LEARNS")
    canvas.setFont("Helvetica", 14)
    canvas.setFillColor(INK)  # white, never gray
    canvas.drawRightString(PAGE_W - MARGIN, 0.44 * inch,
                           f"{stamp} · Page {doc.page}")
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def _evidence_section(st: dict, evidence: list[str]) -> list:
    """Evidence links — every PR/issue number stripped from body text lands
    here as a clickable reference. Shawn's law: technicals are evidence,
    linked, never in the reading flow."""
    out: list = []
    seen: list[str] = []
    for num in evidence:
        if num not in seen:
            seen.append(num)
    if not seen:
        return out
    out.append(Paragraph("Evidence", st["h1"]))
    out.append(Paragraph(
        "Every technical reference from this report, linked. "
        "The story above is written for humans; this is the proof "
        "underneath it.", st["body"]))
    for num in seen[:12]:
        url = ("https://github.com/SoulSchoolAcademy/NayaPOWER/pull/"
               + num)
        out.append(Paragraph(
            f'• <link href="{url}">Pull request #{num}</link>',
            st["detail_white"]))
    if len(seen) > 12:
        out.append(Paragraph(
            f"• …and {len(seen) - 12} more on the team feed #1354.",
            st["detail_white"]))
    out.append(Spacer(1, 8))
    return out


def build_pdf(data: ReportData, report_type: str, output_path: str) -> str:
    """Render ReportData to the exemplar-standard dark PDF."""
    st = _styles()
    stamp = data.generated_at.strftime("%Y-%m-%d %H:%M UTC")
    kind = (data.window_label or report_type).upper()
    cycler = SpectrumCycler()  # ONE cycler for the whole doc: the spectrum
    evidence: list[str] = []   # flows unbroken, no color ever repeats nearby.

    story: list = []
    sections, unassigned = group_by_team(data)

    # ---- Title block: chip kicker + 24px headline + 18px story ----
    kind_chip = Chip(kind, INDIGO, st)
    stamp_line = Paragraph(
        f"{_esc(stamp)} · window since "
        f"{_esc(data.since.strftime('%Y-%m-%d %H:%M UTC'))}", st["detail"])
    story.append(Spacer(1, 0.1 * inch))
    row = Table([[Chip(kind, INDIGO, st), stamp_line]],
                colWidths=[1.7 * inch, PAGE_W - 2 * MARGIN - 1.7 * inch])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(row)
    story.append(Spacer(1, 8))
    story.append(Paragraph("Intelligence Report", st["title"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(_esc(humanize(_headline(data, sections))),
                           st["body"]))
    story.append(Spacer(1, 10))

    # ---- Metrics bar ----
    story.append(_metrics_bar(st, data, cycler))
    story.append(Spacer(1, 10))

    # ---- Highlight boxes ----
    story.extend(_highlight_boxes(st, data, sections, cycler))
    story.append(Spacer(1, 4))

    # ---- 1 · Scorecard (W-001: the headline argues) ----
    story.append(Paragraph("Scores move on evidence, never optimism.",
                           st["h1"]))
    story.append(Paragraph(
        "<b>AUTH</b> means checked by someone else — it survived contact "
        "with reality. <b>claim</b> means our own assessment so far.",
        st["detail_white"]))
    story.append(Spacer(1, 6))
    story.append(_scorecard_table(st, data))
    story.append(Spacer(1, 4))

    # ---- 2 · What got done (W-001: the headline argues) ----
    story.append(Paragraph("What the teams got done.", st["h1"]))
    for i, sec in enumerate(sections, 1):
        story.extend(_team_section_flowables(st, i, sec, data, cycler,
                                             evidence))

    # ---- 3 · Decisions needed (wins/misses removed: they duplicated
    # the team sections above) ----
    story.extend(_decisions_only(st, sections, unassigned, cycler,
                                 evidence))

    # ---- 4 · Single priority — the button-law bar (DC-072/073) ----
    story.append(Paragraph("4 · Single priority for next period", st["h1"]))
    prio = _single_priority(sections, unassigned)
    prio_clean, prio_prs = strip_pr_refs(prio)
    evidence.extend(prio_prs)
    story.append(ButtonBar(humanize(prio_clean), st))
    story.append(Spacer(1, 6))

    # ---- Cross-team signals ----
    story.append(Paragraph("Cross-team signals", st["h1"]))
    shown = False
    for label, items in (("Needs attention", unassigned.get("holes", [])),
                         ("Achievements", unassigned.get("achievements", [])),
                         ("Intelligence", unassigned.get("intelligence", []))):
        items = items[:3]
        if not items:
            continue
        shown = True
        story.append(Paragraph(f"<b>{_esc(humanize(label))}</b>", st["h2"]))
        for it in items:
            clean, prs = strip_pr_refs(it.text)
            evidence.extend(prs)
            out_text = _esc(humanize(_short(clean, 220)))
            story.append(_jewel_bullet(st, cycler.next(), out_text))
    if not shown:
        story.append(Paragraph("All items attributed to teams.", st["body"]))

    # ---- Evidence — PR/issue links, never in body text ----
    story.extend(_evidence_section(st, evidence))

    # ---- Evidence basis — truth, stated (DC-091) ----
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=EDGE,
                            spaceAfter=8, spaceBefore=8))
    story.append(Paragraph(
        f"Window: since {_esc(data.since.strftime('%Y-%m-%d %H:%M UTC'))}. "
        f"Generated {_esc(stamp)}. Built from: worker run logs, daily "
        "memory log, the team feed, and the project database (read-only). "
        "Scores labeled claim vs AUTH; a claim becomes authoritative only "
        "when someone else checks it.",
        st["detail_white"]))

    def _page(canv, doc):
        _header_footer(canv, doc, kind, stamp)

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.0 * inch, bottomMargin=0.85 * inch,
        title=f"Team Naya Intelligence Report — {kind} {stamp} (exemplar)",
        author="Naya 5",
    )
    doc.build(story, onFirstPage=_page, onLaterPages=_page)
    return output_path


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Team Naya PDF intelligence report — exemplar edition")
    ap.add_argument("--type", default="hourly",
                    choices=["hourly", "morning", "nightly"])
    ap.add_argument("--out", default="/tmp/naya-report-exemplar.pdf")
    ap.add_argument("--hours", type=float, default=1.0,
                    help="lookback window in hours")
    args = ap.parse_args()

    now = dt.datetime.now(dt.timezone.utc)
    since = now - dt.timedelta(hours=args.hours)
    gen = ReportGenerator()
    data = gen.collect(args.type, since, now)
    path = build_pdf(data, args.type, args.out)
    print(path)


if __name__ == "__main__":
    main()
