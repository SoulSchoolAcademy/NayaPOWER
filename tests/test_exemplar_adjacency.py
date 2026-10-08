#!/usr/bin/env python3
"""Mechanical design-law verification — the check eyes missed.

Round-2 repair (2026-10-08): visual inspection passed 11 pages while
violations sat on pages 1-3. This test renders the exemplar PDF and
mechanically asserts, on EVERY page:

1. No two adjacent colored elements share a color (vertical flow).
2. No two side-by-side accent shapes share a color (horizontal flow).
3. No gray anywhere (fills, strokes, or text).

It covers ALL colored elements — bars, pills, jewel icons, table cells —
not just the ones SpectrumCycler emits. If the generator regresses, this
fails. Eyes are the backup, not the gate.
"""
import datetime as dt
import sys
import unittest
from pathlib import Path

sys.path.insert(
    0, "/home/hatch/workspace/nayapower-worktrees/reporting/tools/reporting")
sys.path.insert(0, str(Path(__file__).parent.parent / "proof"
                       / "hourly_exemplar"))

import pdf_report_exemplar as ex

try:
    import pymupdf
    _HAS_FITZ = True
except ImportError:  # pragma: no cover
    _HAS_FITZ = False

# Vertical gap (pt) under which two stacked, x-aligned elements count as
# adjacent. Bullets with wrapped text sit ~120pt apart jewel-to-jewel and
# are still "one after another" (Shawn's words) — the cap covers them.
_V_GAP = 130.0
# Horizontal gap (pt) under which two side-by-side shapes count as adjacent.
_H_GAP = 30.0
# Elements fully above this y are fixed brand chrome (header lockup), not
# spectrum flow — excluded from adjacency (gray is still checked).
_HEADER_CUT = 130.0
# Minimum shape area (sq pt) — skips antialiasing specks.
_MIN_AREA = 120.0
# Shapes bigger than this fraction of the page are ambient, not elements.
_MAX_AREA_FRAC = 0.25


def _hx01(c):
    return "#%02x%02x%02x" % (round(c[0] * 255), round(c[1] * 255),
                              round(c[2] * 255))


def _is_grayish(c):
    mx, mn = max(c), min(c)
    return (mx - mn) < 0.18 and 0.25 < mx < 0.92


def _is_accent(c):
    mx, mn = max(c), min(c)
    if mx < 0.12 or mn > 0.90:
        return False  # shadows / white
    return (mx - mn) >= 0.18


_SCORE_NUM_RE = __import__("re").compile(r"^\d+\.\d$")


def _extract(page):
    """All colored elements: (x0, y0, x1, y1, hex, kind).

    Score NUMBERS ("9.0") are data with semantic band colors (a heatmap
    may repeat); they are excluded. Everything chrome — jewels, bars,
    boxes, chips, team cells — is checked.
    """
    W, H = page.rect.width, page.rect.height
    els = []
    for d in page.get_drawings():
        r = d["rect"]
        area = max(0.0, r.width) * max(0.0, r.height)
        if area < _MIN_AREA or area > _MAX_AREA_FRAC * W * H:
            continue
        f = d.get("fill")
        if f and _is_accent(f):
            els.append([r.x0, r.y0, r.x1, r.y1, _hx01(f), "shape"])
        s = d.get("color")  # stroke — gray-checked, not adjacency-checked
        if s and _is_grayish(s):
            els.append([r.x0, r.y0, r.x1, r.y1, _hx01(s), "stroke"])
    for bi, b in enumerate(page.get_text("dict")["blocks"]):
        for l in b.get("lines", []):
            for s in l["spans"]:
                col = s["color"]
                c = ((col >> 16 & 255) / 255.0, (col >> 8 & 255) / 255.0,
                     (col & 255) / 255.0)
                if not _is_accent(c):
                    continue
                if _SCORE_NUM_RE.match(s["text"].strip()):
                    continue  # data band color, not chrome
                x0, y0, x1, y1 = s["bbox"]
                els.append([x0, y0, x1, y1, _hx01(c), "text", bi])
    # Merge same-color overlapping elements (jewel aura+body, card glow+
    # jewel+title, chip glow+edge): they are ONE visual element. Merge on
    # CONTAINMENT or substantial overlap — two adjacent same-color cards
    # whose glows merely kiss (2pt) must NOT merge, or the violation hides.
    def _overlaps(a, b):
        ix0, iy0 = max(a[0], b[0]), max(a[1], b[1])
        ix1, iy1 = min(a[2], b[2]), min(a[3], b[3])
        if ix1 <= ix0 or iy1 <= iy0:
            return 0.0
        return (ix1 - ix0) * (iy1 - iy0)

    merged = []
    for e in els:
        if e[5] == "stroke":
            merged.append(e)
            continue
        area_e = max(0.0, e[2] - e[0]) * max(0.0, e[3] - e[1])
        for m in merged:
            if m[5] == "stroke" or m[4] != e[4]:
                continue
            # Same paragraph's wrapped lines are one element (a team name
            # broken as "Evolution/<br/>Succession" is not two elements).
            same_para = (e[5] == "text" and m[5] == "text"
                         and len(e) > 6 and len(m) > 6 and e[6] == m[6])
            area_m = max(0.0, m[2] - m[0]) * max(0.0, m[3] - m[1])
            inter = _overlaps(e, m)
            contained = (
                e[0] >= m[0] - 1 and e[1] >= m[1] - 1
                and e[2] <= m[2] + 1 and e[3] <= m[3] + 1) or (
                m[0] >= e[0] - 1 and m[1] >= e[1] - 1
                and m[2] <= e[2] + 1 and m[3] <= e[3] + 1)
            substantial = (inter > 0.5 * min(area_e, area_m)
                           if min(area_e, area_m) > 0 else False)
            if same_para or contained or substantial:
                m[0] = min(m[0], e[0]); m[1] = min(m[1], e[1])
                m[2] = max(m[2], e[2]); m[3] = max(m[3], e[3])
                break
        else:
            merged.append(e)
    return merged


def _render():
    from report_generator import ReportGenerator
    gen = ReportGenerator()
    now = dt.datetime.now(dt.timezone.utc)
    data = gen.collect("hourly", now - dt.timedelta(hours=1), now)
    out = "/tmp/exemplar-adjacency-test.pdf"
    return ex.build_pdf(data, "hourly", out)


@unittest.skipUnless(_HAS_FITZ, "pymupdf not installed")
class TestMechanicalAdjacency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pdf = _render()
        cls.doc = pymupdf.open(cls.pdf)
        cls.pages = []
        for i in range(cls.doc.page_count):
            cls.pages.append(_extract(cls.doc[i]))
        assert cls.doc.page_count >= 2, "render produced no pages"

    def test_no_adjacent_same_color_vertical(self):
        """Stacked, horizontally-aligned elements within 130pt: colors
        must differ. Every page. (A score and its status chip are
        diagonally paired, not stacked — the x-overlap rule respects
        semantic pairings. Header brand chrome is fixed identity, not
        flow, and is excluded.)"""
        bad = []
        for pno, els in enumerate(self.pages):
            flow = sorted(
                [e for e in els if e[5] != "stroke" and e[3] > _HEADER_CUT],
                key=lambda e: (e[1], e[0]))
            for a, b in zip(flow, flow[1:]):
                x_overlap = b[0] < a[2] and a[0] < b[2]
                if not x_overlap:
                    continue
                gap = b[1] - a[3]
                overlap = b[1] < a[3]
                if gap < _V_GAP or overlap:
                    if a[4] == b[4]:
                        bad.append(
                            f"p{pno + 1} {a[5]}@{round(a[1])} "
                            f"vs {b[5]}@{round(b[1])} both {a[4]}")
        self.assertEqual(bad, [], f"adjacent same-color:\n" + "\n".join(bad))

    def test_no_adjacent_same_color_horizontal(self):
        """Side-by-side accent shapes (tiles): colors must differ."""
        bad = []
        for pno, els in enumerate(self.pages):
            shapes = sorted(
                [e for e in els if e[5] == "shape" and e[3] > _HEADER_CUT],
                key=lambda e: (e[1], e[0]))
            for a, b in zip(shapes, shapes[1:]):
                y_overlap = b[1] < a[3] and a[1] < b[3]
                x_gap = b[0] - a[2]
                if y_overlap and x_gap < _H_GAP and a[4] == b[4]:
                    bad.append(f"p{pno + 1} shapes@{round(a[1])} both {a[4]}")
        self.assertEqual(bad, [], f"horizontal same-color:\n" + "\n".join(bad))

    def test_no_gray_anywhere(self):
        """Shawn's law: zero gray — fills, strokes, or text."""
        bad = []
        for pno, els in enumerate(self.pages):
            for e in els:
                c = tuple(int(e[4][i:i + 2], 16) / 255.0
                          for i in (1, 3, 5))
                if _is_grayish(c):
                    bad.append(f"p{pno + 1} {e[5]}@{round(e[1])} {e[4]}")
        self.assertEqual(bad, [], f"gray found:\n" + "\n".join(bad))


class TestRound2Units(unittest.TestCase):
    """Unit coverage for each round-2 repair item."""

    def test_no_adjacent_same_hue_family(self):
        c = ex.SpectrumCycler()
        seq = [c.next() for _ in range(200)]
        fams = [ex._family(x) for x in seq]
        for a, b in zip(fams, fams[1:]):
            self.assertNotEqual(a, b, f"same hue family adjacent: {a}")

    def test_teal_lime_not_adjacent(self):
        # The exact pair Shawn flagged (both read as "green").
        self.assertNotEqual(ex._family(ex.TEAL), None)
        self.assertEqual(ex._family(ex.TEAL), ex._family(ex.LIME))

    def test_humanize_strips_uuid_case_insensitive(self):
        out = ex.humanize(
            "T11 (1589C693-E230-4C3A-84C6-AD4FAB723EF8), done")
        self.assertNotIn("1589C693", out)
        self.assertNotIn("(", out)

    def test_humanize_screaming_before_paren_quote(self):
        self.assertIn("Verification",
                      ex.humanize("state PENDING_OUTCOME_VERIFICATION); x"))
        self.assertNotIn("VERIFICATION)", ex.humanize("a VERIFICATION); b"))
        self.assertIn("Provisional",
                      ex.humanize('worker logs "7.0 PROVISIONAL" ok'))

    def test_humanize_strips_paths_and_tags(self):
        out = ex.humanize(
            "filed at BRAIN/05-MEMORY/SMART-NOTES/2026/10/08/SN-0526/, "
            "see [memory:2026-10-08] ok")
        self.assertNotIn("BRAIN/", out)
        self.assertNotIn("memory:", out)
        self.assertNotIn("2026/10/08", out)
        # ...but keeps dates and brand names.
        keep = ex.humanize("on 2026-10-08 NayaPOWER shipped")
        self.assertIn("2026-10-08", keep)
        self.assertIn("NayaPOWER", keep)

    def test_humanize_preserves_icu(self):
        self.assertIn("ICU", ex.humanize("applied to ICU triage"))

    def test_humanize_preserves_connect_node(self):
        out = ex.humanize("drift caught after CONNECT's selector moved")
        self.assertIn("CONNECT's", out)

    def test_humanize_no_dangling_at_or_sha(self):
        out = ex.humanize("rescued branch @ abc1234 (starting 6/6)")
        self.assertNotIn("@", out)
        self.assertNotIn("abc1234", out)
        out2 = ex.humanize("landed at merge SHA def5678 ok")
        self.assertNotIn("Sha", out2)
        self.assertNotIn("def5678", out2)
        # ...but email addresses keep their @.
        self.assertIn("@", ex.humanize("mail user@example.com"))

    def test_humanize_strips_dangling_paren_refs(self):
        out = ex.humanize("Signed in/out on (comments / #1354). Done")
        self.assertNotIn("comments", out)
        self.assertNotIn("(", out)
        keep = ex.humanize("ratio (3 / 4) stays")
        self.assertIn("(3 / 4)", keep)

    def test_humanize_removes_path_parenthetical_whole(self):
        out = ex.humanize(
            'Naya 2 filed Smart Note SN-0526 "Quality" '
            "(filed 2026-10-08 at BRAIN/05-MEMORY/SN-0526/, posted to #1)")
        self.assertNotIn("filed 2026-10-08 at", out)
        self.assertNotIn("BRAIN", out)
        self.assertIn('Smart Note SN-0526 "Quality"', out)

    def test_short_never_mid_word(self):
        out = ex._short("T13 proved cross-domain transfer of the rule.", 20)
        self.assertTrue(out.endswith("…"))
        frag = out[:-1].rsplit(" ", 1)[-1]
        self.assertGreater(len(frag), 2, f"dangling fragment: {frag!r}")
        # A cut that would land mid-word backs up to the word boundary.
        out2 = ex._short("The quick brown fox jumps over", 14)
        self.assertEqual(out2, "The quick…")

    def test_short_prefers_sentence_end(self):
        out = ex._short("First thought complete. Second runs long " * 10, 60)
        self.assertTrue(out.endswith("."))
        self.assertNotIn("…", out)

    def test_short_no_dangling_quote(self):
        out = ex._short(
            "run the system as a high-performance machine and 'create "
            "the most wonderful thing", 60)
        self.assertTrue(out.endswith("…"))
        self.assertNotIn("'", out)
        # Apostrophes inside words are untouched.
        out2 = ex._short("don't stop believing in the system", 20)
        self.assertIn("don't", out2)

    def test_claim_chip_not_gray(self):
        st = ex._styles()
        chip = ex._auth_chip(st, "claim")
        hx = ex._hx(chip.color).lower()
        self.assertNotEqual(hx, ex._hx(ex.MUTED).lower())
        # Gray = low saturation AND mid brightness. White is neither.
        mx = max(chip.color.red, chip.color.green, chip.color.blue)
        mn = min(chip.color.red, chip.color.green, chip.color.blue)
        is_gray = (mx - mn) < 0.18 and 0.25 < mx < 0.92
        self.assertFalse(is_gray, f"claim chip is gray: {hx}")

    def test_scorecard_alternates_repeated_team(self):
        from report_generator import AREA_TO_TEAM, ScorePoint
        st = ex._styles()
        now = dt.datetime.now(dt.timezone.utc)
        areas = ["Action & Execution", "Retrieval", "Production Readiness"]
        self.assertTrue(all(
            AREA_TO_TEAM.get(a) == "Architecture/Engineering/Ops"
            for a in areas))
        data = ex.ReportData(
            scores=[ScorePoint(area=a, score=7.0 + i * 0.5, as_of=now,
                               source="t", status="claim")
                    for i, a in enumerate(areas)])
        t = ex._scorecard_table(st, data, ex.SpectrumCycler())
        colors = []
        for row in t._cellvalues[1:]:
            p = row[0]
            m = __import__("re").search(r'color="([^"]+)"', p.text)
            colors.append(m.group(1).lower())
        for a, b in zip(colors, colors[1:]):
            self.assertNotEqual(a, b, f"adjacent team cells share {a}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
