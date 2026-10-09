#!/usr/bin/env python3
"""PDF renderer — NayaNET instrument edition (2026-10-09).

Rebuilt after Shawn's verdict on the old output: template stamped nine
times, stale recycled content, score soup, zero design. "Garbage."

Design laws (WHAT-I-LEARNED.md):
  - Deep black ground (#050507). White text, 99%. Hierarchy by SIZE
    (24/18/14), never color.
  - Serif voice headlines (Times). One clear line, not a label.
  - Thin lines, generous black space. No boxes around everything.
  - Spectrum accents used sparingly — one per element. This report's
    single accent is indigo #6675ff (the Reports-room accent).
  - Every number carries provenance. A claim is labeled claim.

Structure mirrors the markdown report exactly:
  kicker · voice headline · What moved · Scoreboard · Needs from Shawn
  · Evidence. Quiet hours render one honest line.

Programmatic use:
    from pdf_report import build_pdf
    build_pdf(data, report_type="hourly", output_path="/tmp/report.pdf")

CLI:
    python3 pdf_report.py --type hourly --out /tmp/report.pdf

All external data comes from the supplied ReportData — the renderer
never invents numbers.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from report_generator import (  # noqa: E402
    ReportData,
    ReportGenerator,
    ScorePoint,
    _headline_text,
    _what_moved,
)

from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import inch  # noqa: E402
from reportlab.platypus import (  # noqa: E402
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------------------------
# Palette — black is the suit. One accent, used sparingly.
# ---------------------------------------------------------------------------
BLACK = HexColor("#050507")
WHITE = HexColor("#ffffff")
INDIGO = HexColor("#6675ff")      # the single accent: Δ movements, hairline
HAIRLINE = HexColor("#26262e")    # thin lines, barely there

PAGE_W, PAGE_H = A4
MARGIN = 0.75 * inch


# ---------------------------------------------------------------------------
# Styles — 24 / 18 / 14. Serif voice. All white.
# ---------------------------------------------------------------------------

def _styles() -> dict[str, ParagraphStyle]:
    base = ParagraphStyle("base", fontName="Helvetica", fontSize=14,
                          leading=20, textColor=WHITE)
    return {
        "base": base,
        # Kicker: small caps line above the headline.
        "kicker": ParagraphStyle("kicker", parent=base,
                                 fontName="Helvetica-Bold", fontSize=11,
                                 leading=14, textColor=WHITE,
                                 spaceAfter=8),
        # Voice headline: serif, the one line that matters.
        "voice": ParagraphStyle("voice", parent=base,
                                fontName="Times-Bold", fontSize=24,
                                leading=29, textColor=WHITE,
                                spaceAfter=4),
        # Section headers: 18px white bold.
        "h2": ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold",
                             fontSize=18, leading=23, textColor=WHITE,
                             spaceBefore=20, spaceAfter=8),
        "body": base,
        "bullet": ParagraphStyle("bullet", parent=base, leftIndent=20,
                                 firstLineIndent=0, spaceAfter=8,
                                 bulletIndent=6),
        "small": ParagraphStyle("small", parent=base, fontSize=14,
                                leading=20, textColor=WHITE),
        "cell": ParagraphStyle("cell", parent=base, fontSize=14,
                               leading=19, textColor=WHITE),
        "cell_bold": ParagraphStyle("cell_bold", parent=base,
                                    fontName="Helvetica-Bold", fontSize=14,
                                    leading=19, textColor=WHITE),
        "cell_head": ParagraphStyle("cell_head", parent=base,
                                    fontName="Helvetica-Bold", fontSize=14,
                                    leading=19, textColor=WHITE),
    }


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def _esc(text: str) -> str:
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))


def _short(text: str, limit: int = 200) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[:limit].rstrip() + "…"


def _md_src_to_plain(text: str) -> str:
    """`_(src: x)_` markdown -> ` [x]` plain for PDF text."""
    return re.sub(r"_\s*\(src:\s*([^)]+)\)\s*_", r" [\1]", text)


def _md_src_strip(text: str) -> str:
    """Remove the `_(src: x)_` source tag entirely (for headlines)."""
    return re.sub(r"\s*_\s*\(src:\s*[^)]+\)\s*_\s*", " ", text).strip()


def _hx(color) -> str:
    return "#" + color.hexval()[2:]


def _delta_cell(sp: ScorePoint, previous: dict, st: dict) -> Paragraph:
    prev = previous.get(sp.area)
    if prev is None or prev == sp.score:
        return Paragraph("—", st["cell"])
    d = sp.score - prev
    return Paragraph(
        f'<font color="{_hx(INDIGO)}"><b>{d:+.1f}</b></font>', st["cell"])


def _delta_header(st: dict) -> Paragraph:
    # Δ is not renderable in reportlab's base-14 fonts: ± (WinAnsi-safe)
    # carries the same meaning in a column of signed movements.
    return Paragraph("<b>±</b>", st["cell_head"])


# ---------------------------------------------------------------------------
# Flowable builders
# ---------------------------------------------------------------------------

def _provenance_cell(sp, st):
    """As-of + source: a score without provenance is a lie with
    formatting. Truncated to fit the column."""
    asof = sp.as_of.strftime("%m-%d %H:%M")
    src = sp.source if len(sp.source) <= 26 else sp.source[:23].rstrip() + "\u2026"
    return Paragraph(f"{asof}<br/><font size=7>{_esc(src)}</font>",
                     st["cell"])


def _scoreboard_table(st: dict, data: ReportData) -> Table:
    """Minimal scoreboard: hairlines only, no boxes, no fills."""
    header = [
        Paragraph("<b>Area</b>", st["cell_head"]),
        Paragraph("<b>Score</b>", st["cell_head"]),
        Paragraph("<b>Status</b>", st["cell_head"]),
        Paragraph("<b>As of / source</b>", st["cell_head"]),
        _delta_header(st),
    ]
    rows = [header]
    for sp in data.scores:
        rows.append([
            Paragraph(_esc(sp.area), st["cell"]),
            Paragraph(f"<b>{sp.score:.1f}</b>", st["cell_bold"]),
            Paragraph(_esc(sp.status), st["cell"]),
            _provenance_cell(sp, st),
            _delta_cell(sp, data.previous_scores, st),
        ])
    if len(rows) == 1:
        rows.append([Paragraph("<i>No scores recorded yet.</i>", st["cell"]),
                     Paragraph("", st["cell"]),
                     Paragraph("", st["cell"]),
                     Paragraph("", st["cell"]),
                     Paragraph("", st["cell"])])

    avail = PAGE_W - 2 * MARGIN
    widths = [2.0 * inch, 0.7 * inch, 1.1 * inch, 1.9 * inch, 0.6 * inch]
    scale = avail / sum(widths)
    widths = [w * scale for w in widths]
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, 0), 2),
        ("LEFTPADDING", (0, 1), (-1, -1), 2),
        ("LINEBELOW", (0, 0), (-1, 0), 1, WHITE),
        ("LINEBELOW", (0, 1), (-1, -2), 0.4, HAIRLINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


# ---------------------------------------------------------------------------
# Page template — black ground, quiet header + footer
# ---------------------------------------------------------------------------

def _page_template(kind: str, stamp: str):
    def _draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BLACK)
        canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.setFillColor(WHITE)
        canvas.drawString(MARGIN, PAGE_H - 0.5 * inch,
                          "TEAM NAYA INTELLIGENCE")
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.5 * inch,
                               f"{kind} · {stamp}")
        canvas.setStrokeColor(HAIRLINE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, PAGE_H - 0.62 * inch,
                    PAGE_W - MARGIN, PAGE_H - 0.62 * inch)
        canvas.setFont("Helvetica", 9)
        canvas.drawString(MARGIN, 0.5 * inch, "PROVE THAT THE BRAIN LEARNS")
        canvas.drawRightString(PAGE_W - MARGIN, 0.5 * inch,
                               f"Page {doc.page}")
        canvas.restoreState()
    return _draw


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def build_pdf(data: ReportData, report_type: str, output_path: str) -> str:
    """Render ReportData as a NayaNET instrument. Returns output path."""
    st = _styles()
    stamp = data.generated_at.strftime("%a %Y-%m-%d %H:%M UTC")
    kind = (data.window_label or report_type).upper()
    moved = _what_moved(data)

    story: list = []
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(f"{kind} — {stamp}", st["kicker"]))
    story.append(Paragraph(_esc(_headline_text(data, moved)), st["voice"]))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=0.5, color=INDIGO,
                            spaceAfter=12, spaceBefore=6))

    # What moved.
    story.append(Paragraph("What moved", st["h2"]))
    if moved:
        for m in moved:
            story.append(Paragraph(
                "·&nbsp;&nbsp;" + _esc(_md_src_to_plain(_short(m, 220))),
                st["bullet"]))
    else:
        story.append(Paragraph("Quiet hour — no window activity.",
                               st["body"]))

    # Scoreboard.
    story.append(Paragraph("Scoreboard", st["h2"]))
    story.append(_scoreboard_table(st, data))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Scores move on evidence, never optimism. "
        "A claim becomes authoritative only on independent verification.",
        st["small"]))

    # Needs from Shawn.
    story.append(Paragraph("Needs from Shawn", st["h2"]))
    needs = sorted(data.holes, key=lambda i: -i.priority)[:3]
    if needs:
        for h in needs:
            story.append(Paragraph(
                "·&nbsp;&nbsp;" + _esc(_short(h.text, 220))
                + f" [{_esc(h.source)}]",
                st["bullet"]))
    else:
        story.append(Paragraph("None this hour.", st["body"]))

    # Evidence.
    story.append(Paragraph("Evidence", st["h2"]))
    gh = data.github_snapshot or {}
    sb = data.supabase_snapshot or {}
    if gh.get("error"):
        story.append(Paragraph(f"GitHub: unavailable ({_esc(gh['error'])})",
                               st["body"]))
    else:
        prs = gh.get("prs", [])
        merged = [p for p in prs if p.get("merged")]
        updated = [p for p in prs if not p.get("merged")]
        bits = ([f"#{p['number']} merged" for p in merged[:4]]
                + [f"#{p['number']} updated" for p in updated[:3]])
        story.append(Paragraph(
            "PRs: " + (_esc(", ".join(bits)) if bits else "no PR activity")
            + f" ({len(merged)} merged, {len(updated)} updated).",
            st["body"]))
        n_comments = len(gh.get("comments", []))
        if n_comments:
            story.append(Paragraph(
                f"#1354: {n_comments} comments this window.", st["body"]))
    if sb.get("error"):
        story.append(Paragraph(f"Supabase: unavailable ({_esc(sb['error'])})",
                               st["body"]))
    else:
        counts = sb.get("counts", {})
        story.append(Paragraph(
            "Supabase: " + (_esc(", ".join(f"{k}={v}"
                                          for k, v in counts.items()))
                            or "no rows") + ".",
            st["body"]))

    # Footer rule + window line.
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HAIRLINE,
                            spaceAfter=8, spaceBefore=4))
    since_s = data.since.strftime("%H:%M UTC")
    gen_s = data.generated_at.strftime("%H:%M UTC")
    story.append(Paragraph(
        f"Window {since_s} → {gen_s}. All items carry their source. "
        f"Evidence basis: worker run logs, daily memory log, GitHub "
        f"(#1354 + PRs), Supabase learning_evidence (read-only).",
        st["small"]))

    draw = _page_template(kind, stamp)
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=0.8 * inch, bottomMargin=0.7 * inch,
        title=f"Team Naya Intelligence — {kind} {stamp}",
        author="Naya 5",
    )
    doc.build(story, onFirstPage=draw, onLaterPages=draw)
    return output_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Team Naya PDF intelligence report")
    ap.add_argument("--type", default="hourly",
                    choices=["hourly", "morning", "nightly"])
    ap.add_argument("--out", default="/tmp/naya-report.pdf")
    ap.add_argument("--hours", type=float, default=1.0,
                    help="lookback window in hours (ignored when --since given)")
    ap.add_argument("--since", default=None,
                    help="window start as ISO timestamp; when given, the PDF "
                         "covers exactly the same window as the markdown")
    args = ap.parse_args()

    now = dt.datetime.now(dt.timezone.utc)
    if args.since:
        since = dt.datetime.fromisoformat(args.since)
        if since.tzinfo is None:
            since = since.replace(tzinfo=dt.timezone.utc)
    else:
        since = now - dt.timedelta(hours=args.hours)
    gen = ReportGenerator()
    data = gen.collect(args.type, since, now)
    path = build_pdf(data, args.type, args.out)
    print(path)


if __name__ == "__main__":
    main()
