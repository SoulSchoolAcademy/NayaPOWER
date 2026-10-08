#!/usr/bin/env python3
"""Repair verification — Shawn's 2026-10-08 review of the design exemplar.

Every test maps to a specific failure he named. If any fail, the exemplar
is not ready. Honest scoring only.
"""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(
    0, "/home/hatch/workspace/nayapower-worktrees/reporting/tools/reporting")
sys.path.insert(0, str(Path(__file__).parent.parent / "proof"
                       / "hourly_exemplar"))

import pdf_report_exemplar as ex


class TestSpectrumFlow(unittest.TestCase):
    """Shawn: 'no bullet point one after another that is the same color.'"""

    def test_no_adjacent_repeat_100_draws(self):
        c = ex.SpectrumCycler()
        seq = [c.next() for _ in range(100)]
        for a, b in zip(seq, seq[1:]):
            self.assertFalse(ex._same_color(a, b),
                             f"adjacent repeat: {ex._hx(a)}")

    def test_no_adjacent_repeat_with_exclude(self):
        c = ex.SpectrumCycler()
        for _ in range(50):
            got = c.next(exclude=ex.RED)
            self.assertFalse(ex._same_color(got, ex.RED))

    def test_muddy_neighbors_rejected(self):
        # Shawn: orange score next to yellow/gold header is muddy.
        self.assertLess(ex._color_distance(ex.GOLD, ex.YELLOW),
                        ex._MIN_ADJACENT_DISTANCE)
        self.assertLess(ex._color_distance(ex.GOLD, ex.GOLD),
                        ex._MIN_ADJACENT_DISTANCE)
        # Sanity: clearly different colors pass.
        self.assertGreaterEqual(ex._color_distance(ex.GOLD, ex.BLUE),
                                ex._MIN_ADJACENT_DISTANCE)

    def test_distant_or_ink_falls_back(self):
        self.assertTrue(ex._same_color(
            ex._distant_or_ink(ex.GOLD, ex.YELLOW), ex.INK))
        self.assertTrue(ex._same_color(
            ex._distant_or_ink(ex.GOLD, ex.BLUE), ex.GOLD))

    def test_cycler_never_muddy_200_draws(self):
        c = ex.SpectrumCycler()
        seq = [c.next() for _ in range(200)]
        for a, b in zip(seq, seq[1:]):
            self.assertGreaterEqual(
                ex._color_distance(a, b), ex._MIN_ADJACENT_DISTANCE,
                f"muddy pair: {ex._hx(a)} vs {ex._hx(b)}")


class TestTypography(unittest.TestCase):
    """Shawn: 24 headlines, 18 body, 14 small. No gray text. Ever."""

    def test_styles_only_24_18_14(self):
        st = ex._styles()
        allowed = {24, 18, 14}
        for name, ps in st.items():
            self.assertIn(ps.fontSize, allowed,
                          f"style {name}: {ps.fontSize}px not in 24/18/14")

    def test_no_gray_in_styles(self):
        st = ex._styles()
        muted_hx = ex._hx(ex.MUTED).lower()
        for name, ps in st.items():
            tc = "#" + ps.textColor.hexval()[2:]
            self.assertNotEqual(
                tc.lower(), muted_hx,
                f"style {name} uses gray/muted text")

    def test_no_muted_reference_in_source(self):
        src = Path(ex.__file__).read_text()
        # MUTED may exist as a constant, but must never be assigned to
        # a text color. Find textColor=MUTED and setFillColor(MUTED).
        for pat in (r"textColor\s*=\s*MUTED",
                    r"setFillColor\s*\(\s*MUTED\s*\)"):
            hits = re.findall(pat, src)
            self.assertEqual(hits, [], f"gray text found via {pat}: {hits}")

    def test_header_footer_fonts_legal(self):
        src = Path(ex.__file__).read_text()
        # Canvas font sizes in _header_footer must be 24/18/14.
        hf = src.split("def _header_footer")[1].split("\ndef ")[0]
        sizes = [int(s) for s in re.findall(r"setFont\(\"Helvetica[^\"]*\",\s*(\d+)\)", hf)]
        for s in sizes:
            self.assertIn(s, (24, 18, 14), f"header/footer font {s}px illegal")


class TestReadability(unittest.TestCase):
    """Shawn: 'write for a human child first.' No PR numbers in body."""

    def test_pr_numbers_stripped(self):
        clean, prs = ex.strip_pr_refs("Fix landed in PR-1795 and #1809")
        self.assertNotIn("1795", clean)
        self.assertNotIn("1809", clean)
        self.assertEqual(sorted(prs), ["1795", "1809"])

    def test_humanize_kills_jargon(self):
        out = ex.humanize("Production readiness 3/10, red until PR-1795 merges")
        self.assertNotIn("PR-1795", out)
        self.assertNotIn("readiness", out.lower().replace(
            "how ready we are to launch", ""))
        self.assertIn("how ready we are to launch", out)
        # "red" as status becomes "blocked"
        self.assertNotRegex(out, r"\bred\b")

    def test_humanize_no_orphan_pr_verbs(self):
        out = ex.humanize("waiting on PR-1234 merges")
        self.assertNotIn("1234", out)

    def test_area_plain_is_human(self):
        s = ex._area_plain("Production Readiness", 3.0, "claim")
        self.assertIn("early stages", s)
        self.assertNotIn("PR", s)
        self.assertRegex(s, r"\d\.\d out of 10")

    def test_score_plain_bands(self):
        self.assertIn("excellent", ex._score_plain(9.5))
        self.assertIn("good progress", ex._score_plain(8.0))
        self.assertIn("halfway", ex._score_plain(5.5))
        self.assertIn("early stages", ex._score_plain(3.0))
        self.assertIn("just getting started", ex._score_plain(1.0))


class TestButtonSafety(unittest.TestCase):
    """Shawn: text overlapping buttons is an instant fail."""

    def test_button_truncates_long_text(self):
        st = ex._styles()
        long_text = "x" * 500
        btn = ex.ButtonBar(long_text, st)
        self.assertLessEqual(len(btn.text), 121)  # 120 + ellipsis
        self.assertTrue(btn.text.endswith("…"))

    def test_button_empty_safe(self):
        st = ex._styles()
        btn = ex.ButtonBar("", st)
        self.assertEqual(btn.text, "—")


class TestNoDuplication(unittest.TestCase):
    """Shawn: 'you have it twice' — wins/misses duplicated team sections."""

    def test_wins_misses_sections_gone(self):
        src = Path(ex.__file__).read_text()
        self.assertNotIn("_wins_misses_decisions", src)
        self.assertNotIn("Where we're winning", src)
        self.assertNotIn("Where we're missing", src)

    def test_decisions_section_present(self):
        src = Path(ex.__file__).read_text()
        self.assertIn("Decisions needed", src)


class TestLogo(unittest.TestCase):
    """Shawn: 'it's not even our logo' — use the real brand mark."""

    def test_logo_file_exists(self):
        self.assertTrue(Path(ex._LOGO_PATH).exists(),
                        f"logo missing at {ex._LOGO_PATH}")

    def test_header_uses_logo(self):
        src = Path(ex.__file__).read_text()
        hf = src.split("def _header_footer")[1].split("\ndef ")[0]
        self.assertIn("drawImage", hf)
        self.assertIn("_LOGO_PATH", hf)


if __name__ == "__main__":
    unittest.main(verbosity=2)
