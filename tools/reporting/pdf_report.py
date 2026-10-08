#!/usr/bin/env python3
"""PDF renderer for Team Naya nine-team intelligence reports.

Takes the same structured ReportData as the markdown renderer
(report_generator.py) and produces a professional, print-ready PDF
matching the morning-report quality bar:

  header (title + timestamp + one-line headline)
  key metrics bar (scannable at a glance)
  highlight boxes (4-5 callouts in a visual grid)
  numbered sections:
    1. Scorecard (team table)
    2. What got done (by team)
    3. Where we're winning (bulleted, evidenced)
    4. Where we're missing (numbered, concrete)
    5. Decisions needed (what / means / options / recommendation)
    6. Single priority for next period
  footer (timestamp, evidence basis, window)

Tone: direct, evidence-backed, honest about misses, no fluff.

Programmatic use:
    from pdf_report import build_pdf
    build_pdf(data, report_type="hourly", output_path="/tmp/report.pdf")

CLI:
    python3 pdf_report.py --type hourly --out /tmp/report.pdf
    (collects live data via ReportGenerator with default fetchers)

All external data comes from the supplied ReportData — the renderer
never invents numbers. Empty sections render honestly ("none recorded").
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

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
from reportlab.lib.units import inch, mm  # noqa: E402
from reportlab.platypus import (  # noqa: E402
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------------------------
# Palette — professional, print-safe
# ---------------------------------------------------------------------------
NAVY = HexColor("#1a2b4a")
BLUE = HexColor("#2563eb")
DARK = HexColor("#111827")
GRAY = HexColor("#6b7280")
LIGHT_BG = HexColor("#f3f4f6")
BORDER = HexColor("#d1d5db")
GREEN = HexColor("#15803d")
GREEN_BG = HexColor("#dcfce7")
AMBER = HexColor("#b45309")
AMBER_BG = HexColor("#fef3c7")
RED = HexColor("#b91c1c")
RED_BG = HexColor("#fee2e2")
WHITE = HexColor("#ffffff")

PAGE_W, PAGE_H = A4
MARGIN = 0.6 * inch

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------


def _styles() -> dict[str, ParagraphStyle]:
    base = ParagraphStyle("base", fontName="Helvetica", fontSize=9.5,
                          leading=13.5, textColor=DARK)
    return {
        "base": base,
        "title": ParagraphStyle("title", parent=base, fontName="Helvetica-Bold",
                                fontSize=20, leading=24, textColor=NAVY),
        "subtitle": ParagraphStyle("subtitle", parent=base, fontSize=11,
                                   leading=14, textColor=GRAY),
        "headline": ParagraphStyle("headline", parent=base,
                                   fontName="Helvetica-Oblique", fontSize=10,
                                   leading=14, textColor=NAVY),
        "h1": ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold",
                             fontSize=13, leading=16, textColor=NAVY,
                             spaceBefore=10, spaceAfter=6),
        "h2": ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold",
                             fontSize=10.5, leading=14, textColor=NAVY,
                             spaceBefore=8, spaceAfter=4),
        "body": base,
        "bullet": ParagraphStyle("bullet", parent=base, leftIndent=14,
                                 firstLineIndent=0, spaceAfter=3),
        "small": ParagraphStyle("small", parent=base, fontSize=8,
                                leading=11, textColor=GRAY),
        "box_title": ParagraphStyle("box_title", parent=base,
                                    fontName="Helvetica-Bold", fontSize=9,
                                    leading=12, textColor=NAVY),
        "box_body": ParagraphStyle("box_body", parent=base, fontSize=8.5,
                                   leading=11.5, textColor=DARK),
        "cell": ParagraphStyle("cell", parent=base, fontSize=8.5,
                               leading=11.5),
        "cell_bold": ParagraphStyle("cell_bold", parent=base,
                                    fontName="Helvetica-Bold", fontSize=8.5,
                                    leading=11.5),
        "cell_head": ParagraphStyle("cell_head", parent=base,
                                    fontName="Helvetica-Bold", fontSize=8.5,
                                    leading=11.5, textColor=WHITE),
    }


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def _esc(text: str) -> str:
    """Escape for reportlab Paragraph markup."""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))


def _short(text: str, limit: int = 160) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[:limit].rstrip() + "…"


def _score_color(score: float) -> HexColor:
    if score >= 9.0:
        return GREEN
    if score >= 7.0:
        return AMBER
    return RED


def _score_bg(score: float) -> HexColor:
    if score >= 9.0:
        return GREEN_BG
    if score >= 7.0:
        return AMBER_BG
    return RED_BG



def _hx(color) -> str:
    """Hex string with # prefix for reportlab <font color> markup."""
    return "#" + color.hexval()[2:]

def _delta_str(sp: ScorePoint, previous: dict) -> str:
    prev = previous.get(sp.area)
    if prev is None or prev == sp.score:
        return "—"
    d = sp.score - prev
    return f"{d:+.1f}"


# ---------------------------------------------------------------------------
# Executive content — computed from data, never invented
# ---------------------------------------------------------------------------

def _headline(data: ReportData, sections: list[TeamSection]) -> str:
    """One line capturing the period's story."""
    bits: list[str] = []
    # Biggest score movement.
    moves: list[tuple[float, str, float, float]] = []
    for sp in data.scores:
        prev = data.previous_scores.get(sp.area)
        if prev is not None and prev != sp.score:
            moves.append((abs(sp.score - prev), sp.area, prev, sp.score))
    moves.sort(reverse=True)
    if moves:
        _, area, prev, now = moves[0]
        bits.append(f"{area} {prev:.1f}→{now:.1f}")
    # Count of achievements.
    n_ach = sum(len(s.achievements) for s in sections)
    if n_ach:
        bits.append(f"{n_ach} achievements landed")
    # Top blocker.
    all_holes: list[Item] = []
    for s in sections:
        all_holes.extend(s.holes)
    all_holes.sort(key=lambda i: -i.priority)
    if all_holes:
        bits.append("top blocker: " + _short(all_holes[0].text, 90))
    # Teams at/above the 9.0 floor.
    at_floor = sum(1 for sp in data.scores if sp.score >= 9.0)
    if at_floor:
        bits.append(f"{at_floor} area{'s' if at_floor != 1 else ''} at 9.0+")
    return " · ".join(bits) if bits else "steady period — no score movement recorded"


def _top_wins(sections: list[TeamSection], limit: int = 6) -> list[tuple[str, Item]]:
    wins: list[tuple[str, Item]] = []
    for s in sections:
        for a in s.achievements[:3]:
            wins.append((s.name, a))
    return wins[:limit]


def _top_misses(sections: list[TeamSection],
                unassigned: dict,
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
    """Items that read as decisions needed — keyword scan, honest when empty."""
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


def _single_priority(sections: list[TeamSection],
                     unassigned: dict) -> str:
    misses = _top_misses(sections, unassigned, limit=1)
    if misses:
        team, item = misses[0]
        return f"[{team}] {_short(item.text, 200)}"
    # Fall back to the first team's action plan.
    for s in sections:
        plan = action_plan_text(s)
        if "No recorded actions" not in plan:
            return f"[{s.name}] {_short(plan, 200)}"
    return "No recorded priority this window."


# ---------------------------------------------------------------------------
# Flowable builders
# ---------------------------------------------------------------------------

def _metrics_bar(st: dict, data: ReportData) -> Table:
    """Key metrics strip: PRs, board, Supabase, window."""
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
        sb_txt = ", ".join(f"{k}={v}" for k, v in counts.items()) or "no rows"

    cells = [
        [Paragraph("<b>PRs updated</b><br/>%d (%d merged)" % (len(prs), merged),
                   st["box_body"]),
         Paragraph("<b>Open PRs</b><br/>%d" % open_prs, st["box_body"]),
         Paragraph("<b>#1354 comments</b><br/>%s" % comments, st["box_body"]),
         Paragraph("<b>learning_evidence</b><br/>%s" % _esc(sb_txt),
                   st["box_body"]),
         Paragraph("<b>Window</b><br/>%s" %
                   _esc(data.since.strftime("%m-%d %H:%M UTC")),
                   st["box_body"])],
    ]
    t = Table(cells, colWidths=[1.35 * inch] * 5)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def _highlight_boxes(st: dict, data: ReportData,
                     sections: list[TeamSection]) -> Table:
    """4-5 visual callout boxes."""
    boxes: list[tuple[str, str, HexColor]] = []

    # 1 — biggest score movement.
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
        color = GREEN if d > 0 else RED
        boxes.append((
            "BIGGEST MOVE",
            f"{_esc(area)} {prev:.1f} → <b>{now:.1f}</b> ({status})",
            color,
        ))

    # 2 — top blocker.
    misses = _top_misses(sections, {}, limit=1)
    if misses:
        team, item = misses[0]
        boxes.append((
            "TOP BLOCKER",
            f"[{_esc(team)}] {_esc(_short(item.text, 110))}",
            RED,
        ))

    # 3 — throughput.
    n_ach = sum(len(s.achievements) for s in sections)
    boxes.append((
        "THROUGHPUT",
        f"<b>{n_ach}</b> achievements recorded this window",
        BLUE,
    ))

    # 4 — floor count.
    at_floor = [sp for sp in data.scores if sp.score >= 9.0]
    boxes.append((
        "AT 9.0+ FLOOR",
        f"<b>{len(at_floor)}</b> of {len(data.scores)} "
        f"area{'s' if len(data.scores) != 1 else ''}"
        + (": " + ", ".join(_esc(sp.area) for sp in at_floor[:3])
           if at_floor else ""),
        GREEN if at_floor else GRAY,
    ))

    # 5 — authoritative anchor.
    auth = [sp for sp in data.scores if sp.status == "authoritative"]
    if auth:
        sp = auth[0]
        boxes.append((
            "AUTHORITATIVE",
            f"{_esc(sp.area)} <b>{sp.score:.1f}</b> (verified, not a claim)",
            NAVY,
        ))

    boxes = boxes[:5]
    n = len(boxes)
    width = (PAGE_W - 2 * MARGIN) / n
    row = []
    for title, body, color in boxes:
        inner = [
            [Paragraph(f'<font color="{_hx(color)}"><b>{title}</b></font>',
                       st["box_title"])],
            [Paragraph(body, st["box_body"])],
        ]
        cell = Table(inner, colWidths=[width - 12])
        cell.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LINEBELOW", (0, 0), (-1, 0), 2, color),
        ]))
        row.append(cell)
    t = Table([row], colWidths=[width] * n)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def _scorecard_table(st: dict, data: ReportData) -> Table:
    """Team × score dashboard."""
    header = [
        Paragraph("<b>Team</b>", st["cell_head"]),
        Paragraph("<b>Manager</b>", st["cell_head"]),
        Paragraph("<b>Area</b>", st["cell_head"]),
        Paragraph("<b>Score</b>", st["cell_head"]),
        Paragraph("<b>Status</b>", st["cell_head"]),
        Paragraph("<b>Δ</b>", st["cell_head"]),
    ]
    rows = [header]
    for sp in data.scores:
        # Find owning team for the area.
        team = next(
            (t for t in _team_lookup() if sp.area in t["areas"]),
            None,
        )
        team_name = team["name"] if team else "—"
        manager = team["manager"] if team else "—"
        tag = "authoritative" if sp.status == "authoritative" else "claim"
        delta = _delta_str(sp, data.previous_scores)
        color = _score_color(sp.score)
        rows.append([
            Paragraph(_esc(team_name), st["cell"]),
            Paragraph(_esc(manager), st["cell"]),
            Paragraph(_esc(sp.area), st["cell"]),
            Paragraph(
                f'<font color="{_hx(color)}"><b>{sp.score:.1f}</b></font>',
                st["cell"]),
            Paragraph(_esc(tag), st["cell"]),
            Paragraph(_esc(delta), st["cell"]),
        ])

    avail = PAGE_W - 2 * MARGIN
    widths = [1.55 * inch, 0.85 * inch, 1.6 * inch,
              0.65 * inch, 0.95 * inch, 0.5 * inch]
    # Scale to fit.
    scale = avail / sum(widths)
    widths = [w * scale for w in widths]
    t = Table(rows, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ]
    t.setStyle(TableStyle(style))
    return t


_team_cache: list[dict] | None = None


def _team_lookup() -> list[dict]:
    global _team_cache
    if _team_cache is None:
        from report_generator import TEAM_STRUCTURE
        _team_cache = TEAM_STRUCTURE
    return _team_cache


def _team_section_flowables(st: dict, i: int, sec: TeamSection,
                            data: ReportData) -> list:
    """One team's section: scores, achievements, holes, plan, priorities."""
    out: list = []
    # Header line with score chips.
    chips: list[str] = []
    for sp in sec.scores:
        color = _score_color(sp.score)
        tag = "AUTH" if sp.status == "authoritative" else "claim"
        delta = _delta_str(sp, data.previous_scores)
        chips.append(
            f'<font color="{_hx(color)}"><b>{sp.score:.1f}</b></font>'
            f' <font size=7 color="#6b7280">{_esc(sp.area)} · {tag} · Δ{delta}</font>'
        )
    chip_txt = " &nbsp;&nbsp; ".join(chips) if chips else \
        '<font size=8 color="#6b7280">cross-cutting — no direct area score</font>'
    out.append(Paragraph(
        f"<b>Team {i}: {_esc(sec.name)}</b>"
        f' <font size=8 color="#6b7280">({_esc(sec.manager)} · feed {sec.feed})</font>',
        st["h2"]))
    out.append(Paragraph(chip_txt, st["body"]))
    out.append(Spacer(1, 4))

    # Achievements.
    out.append(Paragraph("<b>Done this period</b>", st["cell_bold"]))
    done = sec.achievements[:5]
    if done:
        for a in done:
            out.append(Paragraph(
                f"- {_esc(_short(a.text, 200))}"
                f' <font size=7 color="#6b7280">[{_esc(a.source)}]</font>',
                st["bullet"]))
    else:
        out.append(Paragraph(
            '<font color="#6b7280">Nothing recorded this window.</font>',
            st["bullet"]))

    # Holes.
    holes = sorted(sec.holes, key=lambda x: -x.priority)[:3]
    if holes:
        out.append(Paragraph("<b>Holes</b>", st["cell_bold"]))
        for j, h in enumerate(holes, 1):
            out.append(Paragraph(
                f"{j}. {_esc(_short(h.text, 200))}"
                f' <font size=7 color="#6b7280">[{_esc(h.source)}]</font>',
                st["bullet"]))

    # Action plan.
    plan = action_plan_text(sec).replace("_", "")
    out.append(Paragraph(
        f"<b>Plan to 10:</b> {_esc(_short(plan, 260))}", st["bullet"]))

    # Priorities.
    if sec.priorities:
        out.append(Paragraph("<b>Next</b>", st["cell_bold"]))
        for p in sec.priorities[:3]:
            out.append(Paragraph(
                f"→ {_esc(_short(p.text, 200))}", st["bullet"]))

    out.append(HRFlowable(width="100%", thickness=0.5, color=BORDER,
                          spaceAfter=4, spaceBefore=6))
    return out


# ---------------------------------------------------------------------------
# Page template — header + footer
# ---------------------------------------------------------------------------

def _header_footer(canvas, doc, report_type: str, stamp: str):
    canvas.saveState()
    # Header rule.
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, PAGE_H - 0.45 * inch,
                PAGE_W - MARGIN, PAGE_H - 0.45 * inch)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GRAY)
    canvas.drawString(MARGIN, PAGE_H - 0.38 * inch,
                      "TEAM NAYA INTELLIGENCE REPORT")
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.38 * inch,
                          f"{report_type.upper()} · {stamp}")
    # Footer.
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(GRAY)
    canvas.drawString(MARGIN, 0.45 * inch,
                      "PROVE THAT THE BRAIN LEARNS")
    canvas.drawCentredString(PAGE_W / 2, 0.45 * inch,
                             f"Generated {stamp}")
    canvas.drawRightString(PAGE_W - MARGIN, 0.45 * inch,
                           f"Page {doc.page}")
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def build_pdf(data: ReportData, report_type: str, output_path: str) -> str:
    """Render ReportData to a professional PDF. Returns the output path."""
    st = _styles()
    stamp = data.generated_at.strftime("%Y-%m-%d %H:%M UTC")
    kind = (data.window_label or report_type).upper()

    story: list = []

    # ---- Title block ----
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Team Naya Intelligence Report", st["title"]))
    story.append(Paragraph(
        f"{kind} · {stamp}", st["subtitle"]))
    story.append(Spacer(1, 6))

    sections, unassigned = group_by_team(data)
    story.append(Paragraph(_esc(_headline(data, sections)), st["headline"]))
    story.append(Spacer(1, 10))

    # ---- Metrics bar ----
    story.append(_metrics_bar(st, data))
    story.append(Spacer(1, 8))

    # ---- Highlight boxes ----
    story.append(_highlight_boxes(st, data, sections))
    story.append(Spacer(1, 6))

    # ---- 1 · Scorecard ----
    story.append(Paragraph("1 · Scorecard", st["h1"]))
    story.append(Paragraph(
        "Scores move on evidence, never optimism. "
        "<b>AUTH</b> = independently verified; <b>claim</b> = self-reported, "
        "awaiting a stamp.", st["small"]))
    story.append(Spacer(1, 4))
    story.append(_scorecard_table(st, data))

    # ---- 2 · What got done (by team) ----
    story.append(Paragraph("2 · What got done — by team", st["h1"]))
    for i, sec in enumerate(sections, 1):
        story.extend(_team_section_flowables(st, i, sec, data))

    # ---- 3 · Where we're winning ----
    story.append(Paragraph("3 · Where we're winning", st["h1"]))
    wins = _top_wins(sections)
    if wins:
        for team, item in wins:
            story.append(Paragraph(
                f"- <b>[{_esc(team)}]</b> {_esc(_short(item.text, 220))}"
                f' <font size=7 color="#6b7280">[{_esc(item.source)}]</font>',
                st["bullet"]))
    else:
        story.append(Paragraph(
            '<font color="#6b7280">No achievements recorded this window.</font>',
            st["body"]))

    # ---- 4 · Where we're missing ----
    story.append(Paragraph("4 · Where we're missing the mark", st["h1"]))
    misses = _top_misses(sections, unassigned)
    if misses:
        for j, (team, item) in enumerate(misses, 1):
            story.append(Paragraph(
                f"<b>MISS {j} — [{_esc(team)}]</b> "
                f"{_esc(_short(item.text, 240))}"
                f' <font size=7 color="#6b7280">[{_esc(item.source)}]</font>',
                st["bullet"]))
    else:
        story.append(Paragraph(
            '<font color="#6b7280">No holes recorded this window.</font>',
            st["body"]))

    # ---- 5 · Decisions needed ----
    story.append(Paragraph("5 · Decisions needed", st["h1"]))
    decisions = _decisions(sections, unassigned)
    if decisions:
        for j, (team, item) in enumerate(decisions, 1):
            story.append(Paragraph(
                f"<b>{j} · [{_esc(team)}]</b> {_esc(_short(item.text, 240))}",
                st["bullet"]))
            story.append(Paragraph(
                '<font size=8 color="#6b7280">Recommendation: resolve via '
                "the Value Calculus; escalate to Shawn only if it crosses "
                "a protected gate.</font>",
                st["bullet"]))
    else:
        story.append(Paragraph(
            '<font color="#6b7280">None recorded this window — '
            "the math is deciding.</font>",
            st["body"]))

    # ---- 6 · Single priority ----
    story.append(Paragraph("6 · Single priority for next period", st["h1"]))
    story.append(Paragraph(
        f"<b>{_esc(_single_priority(sections, unassigned))}</b>",
        st["body"]))

    # ---- Cross-team signals ----
    story.append(Paragraph("Cross-team signals", st["h1"]))
    shown = False
    for label, items in (("Holes", unassigned.get("holes", [])),
                         ("Achievements", unassigned.get("achievements", [])),
                         ("Intelligence", unassigned.get("intelligence", []))):
        items = items[:3]
        if not items:
            continue
        shown = True
        story.append(Paragraph(f"<b>{label}</b>", st["cell_bold"]))
        for it in items:
            story.append(Paragraph(
                f"- {_esc(_short(it.text, 220))}"
                f' <font size=7 color="#6b7280">[{_esc(it.source)}]</font>',
                st["bullet"]))
    if not shown:
        story.append(Paragraph(
            '<font color="#6b7280">All items attributed to teams.</font>',
            st["body"]))

    # ---- Evidence basis ----
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
    since_s = data.since.strftime("%Y-%m-%d %H:%M UTC")
    story.append(Paragraph(
        f'<font size=7 color="#6b7280">Window: since {since_s}. '
        f"Generated {stamp}. Evidence basis: worker run logs, daily memory "
        "log, GitHub (#1354 + PRs), Supabase learning_evidence (read-only). "
        "All items carry their source. Scores labeled claim vs authoritative; "
        "a claim becomes authoritative only on independent verification."
        "</font>",
        st["small"]))

    def _page(canv, doc):
        _header_footer(canv, doc, kind, stamp)

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=0.65 * inch, bottomMargin=0.65 * inch,
        title=f"Team Naya Intelligence Report — {kind} {stamp}",
        author="Naya 5",
    )
    doc.build(story, onFirstPage=_page, onLaterPages=_page)
    return output_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Team Naya PDF intelligence report")
    ap.add_argument("--type", default="hourly",
                    choices=["hourly", "morning", "nightly"])
    ap.add_argument("--out", default="/tmp/naya-report.pdf")
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
