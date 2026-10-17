#!/usr/bin/env python3
"""Tests for spectrum_readout.py — including negative controls.

If this tool cannot be broken by these cases, it was not tested.
"""
import json
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from spectrum_readout import parse_comment, aggregate


def comment(body, cid=1, created="2026-10-15T07:00:00Z", login="SoulSchoolAcademy"):
    return {"id": cid, "body": body, "created_at": created,
            "user": {"login": login}}


class TestParse(unittest.TestCase):
    def test_standard_signout_line(self):
        p = parse_comment(comment("Self-score 8.5/10. Spectrum +7. Drift: none."))
        self.assertEqual(p["score"], 7)
        self.assertIsNone(p["excluded"])

    def test_negative_rung(self):
        p = parse_comment(comment("Spectrum -4 and holding."))
        self.assertEqual(p["score"], -4)

    def test_colon_form(self):
        p = parse_comment(comment("Spectrum: +3"))
        self.assertEqual(p["score"], 3)

    def test_no_spectrum_excluded(self):
        p = parse_comment(comment("Self-score 8.5/10. Drift: none."))
        self.assertIsNone(p["score"])
        self.assertEqual(p["excluded"], "no_spectrum_line")

    def test_self_score_alone_not_mistaken(self):
        # "score 8/10" must never parse as a spectrum score
        p = parse_comment(comment("Verdict: done | score 8/10"))
        self.assertIsNone(p["score"])
        self.assertEqual(p["excluded"], "no_spectrum_line")

    def test_malformed_word_excluded(self):
        p = parse_comment(comment("Spectrum nine, roughly."))
        self.assertIsNone(p["score"])
        self.assertEqual(p["excluded"], "no_spectrum_line")

    def test_out_of_range_excluded_not_clamped(self):
        p = parse_comment(comment("Spectrum +15, off the charts."))
        self.assertIsNone(p["score"])
        self.assertEqual(p["excluded"], "out_of_range")

    def test_last_match_wins_correction(self):
        p = parse_comment(comment(
            "CORRECTION: Was Spectrum +7. Is Spectrum (corrected): +6."))
        self.assertEqual(p["score"], 6)

    def test_seat_and_lane_extraction(self):
        p = parse_comment(comment(
            "**Seat:** Naya Resolve Narzan · **Lane:** build\nSpectrum +7"))
        self.assertEqual(p["seat"], "Naya Resolve Narzan")
        self.assertEqual(p["lane"], "build")

    def test_missing_user_dict(self):
        p = parse_comment({"id": 9, "body": "Spectrum +1", "created_at": None})
        self.assertEqual(p["score"], 1)
        self.assertIsNone(p["author"])

    def test_who_marker_seat(self):
        p = parse_comment(comment(
            "# VERIFY SIGN-OUT\n\n**WHO:** Naya Resolve Narzan · lane verify\nSpectrum +7"))
        self.assertEqual(p["seat"], "Naya Resolve Narzan")
        self.assertEqual(p["lane"], "verify")

    def test_wave_header_seat(self):
        p = parse_comment(comment(
            "**[Naya Mechanic] sign-out — WAVE 173 (INFRA)\nSpectrum +8"))
        self.assertEqual(p["seat"], "Naya Mechanic")

    def test_bracket_header_seat_and_lane(self):
        p = parse_comment(comment(
            "# PULSE — [Naya Resolve · BUILD] night-shift-build\nSpectrum +7"))
        self.assertEqual(p["seat"], "Naya Resolve")
        self.assertEqual(p["lane"], "build")

    def test_lane_wire_bracket(self):
        p = parse_comment(comment(
            "[Naya Electrician] WAVE-173 sign-out [LANE WIRE]\nSpectrum +7"))
        self.assertEqual(p["seat"], "Naya Electrician")
        self.assertEqual(p["lane"], "wire")

    def test_seat_marker_beats_who(self):
        p = parse_comment(comment(
            "**Seat:** Naya Resolve Narzan · **Lane:** build\n**WHO:** Someone Else\nSpectrum +7"))
        self.assertEqual(p["seat"], "Naya Resolve Narzan")


class TestScorerRound2(unittest.TestCase):
    """Regression tests for the scorer's round-1 findings (blockers 1-4, polish 5-12)."""

    def test_fenced_example_not_counted(self):
        p = parse_comment(comment("Format:\n```\nSpectrum +9\n```\nDrift: none."))
        self.assertIsNone(p["score"])
        self.assertEqual(p["excluded"], "no_spectrum_line")

    def test_fenced_real_score_still_counts(self):
        p = parse_comment(comment("```\ncode\n```\nSpectrum +7. Drift: none."))
        self.assertEqual(p["score"], 7)

    def test_quoted_score_not_attributed(self):
        p = parse_comment(comment("> Naya 4: Spectrum +8\n\nAgree."))
        self.assertIsNone(p["score"])

    def test_own_score_beats_quoted(self):
        p = parse_comment(comment("Spectrum +7\n> quoted: Spectrum +8"))
        self.assertEqual(p["score"], 7)

    def test_unicode_minus(self):
        p = parse_comment(comment("Spectrum \u22127. Drift: none."))
        self.assertEqual(p["score"], -7)
        p = parse_comment(comment("Spectrum \u20137. Drift: none."))
        self.assertEqual(p["score"], -7)
        p = parse_comment(comment("Spectrum \u20147. Drift: none."))
        self.assertEqual(p["score"], -7)


class TestScorerRound3(unittest.TestCase):
    """Regression tests for the round-2 findings (B1, B2, P1-P5)."""

    def test_unclosed_fence_quarantines_example(self):
        p = parse_comment(comment(
            "My score: Spectrum +7. Drift: none.\n```\nExample: Spectrum +9"))
        self.assertEqual(p["score"], 7)

    def test_double_fence_second_unclosed(self):
        # a ``` b ``` c ``` d — the " c " segment is outside both fences and
        # must survive (pins the deviation from the scorer's [:-1] formula).
        p = parse_comment(comment(
            "```\ncode\n```\nSpectrum +6.\n```\nExample: Spectrum +9"))
        self.assertEqual(p["score"], 6)

    def test_inline_code_not_counted(self):
        p = parse_comment(comment(
            "My score: Spectrum +6.\nFormat like `Spectrum +7` above."))
        self.assertEqual(p["score"], 6)

    def test_inline_code_only_excluded(self):
        p = parse_comment(comment("See `Spectrum +7` for the format."))
        self.assertIsNone(p["score"])

    def test_parenthesized_score(self):
        p = parse_comment(comment("Spectrum (+7) today."))
        self.assertEqual(p["score"], 7)

    def test_range_not_first_number(self):
        p = parse_comment(comment("Spectrum 7-8, hard to say."))
        self.assertIsNone(p["score"])

    def test_negative_with_trailing_dash_phrase(self):
        p = parse_comment(comment("Spectrum -4 - drift was the theme."))
        self.assertEqual(p["score"], -4)

    def test_empty_render_no_nones(self):
        from spectrum_readout import render_human
        data = aggregate([])
        out = render_human(data, {"issue": "file", "pages_read": [0, 0],
                                  "total_comments": 0})
        self.assertIn("n/a", out)
        self.assertNotIn("None", out)

    def test_singular_comment_label(self):
        from spectrum_readout import render_human
        data = aggregate([parse_comment(comment("Spectrum +7", cid=1))])
        out = render_human(data, {"issue": "file", "pages_read": [0, 0],
                                  "total_comments": 1})
        self.assertIn("1 comment)", out)
        self.assertNotIn("1 comments", out)


class TestScorerRound4(unittest.TestCase):
    """Regression tests for the round-3 polish items (1-4)."""

    def test_spaced_range_excluded(self):
        p = parse_comment(comment("Spectrum 7 - 8, hard to say."))
        self.assertIsNone(p["score"])

    def test_negative_minus_dash_phrase_still_counts(self):
        p = parse_comment(comment("Spectrum -4 - drift was the theme."))
        self.assertEqual(p["score"], -4)

    def test_escaped_fence_not_a_fence(self):
        # GitHub renders \``` literally — the score after it must survive.
        p = parse_comment(comment("Use \\``` to show fences.\nSpectrum +7."))
        self.assertEqual(p["score"], 7)

    def test_unbalanced_open_paren_rejected(self):
        p = parse_comment(comment("Spectrum (7 of them were great."))
        self.assertIsNone(p["score"])

    def test_unbalanced_close_paren_counts(self):
        # Documented leniency: trailing ")" alone does not void the score.
        p = parse_comment(comment("Spectrum 7) today."))
        self.assertEqual(p["score"], 7)

    def test_balanced_parens_count(self):
        p = parse_comment(comment("Spectrum ( +7 ) today."))
        self.assertEqual(p["score"], 7)

    def test_three_digit_is_out_of_range(self):
        p = parse_comment(comment("Spectrum 123?!"))
        self.assertIsNone(p["score"])
        self.assertEqual(p["excluded"], "out_of_range")

    def test_three_word_seat(self):
        p = parse_comment(comment("**Seat:** Naya Alpha Beta Gamma\nSpectrum +7"))
        self.assertEqual(p["seat"], "Naya Alpha Beta Gamma")

    def test_lane_trailing_prose_truncated(self):
        p = parse_comment(comment("**Seat:** Naya Alpha\n**Lane:** build stuff here\nSpectrum +7"))
        self.assertEqual(p["lane"], "build")

    def test_ratio_not_counted(self):
        p = parse_comment(comment("Spectrum 8/10 today."))
        self.assertIsNone(p["score"])

    def test_decimal_not_counted(self):
        p = parse_comment(comment("Spectrum 8.5 roughly."))
        self.assertIsNone(p["score"])

    def test_sentence_period_still_counts(self):
        # The scorer's literal (?![./\d]) would have broken this canonical form.
        p = parse_comment(comment("Self-score 8.5/10. Spectrum +7. Drift: none."))
        self.assertEqual(p["score"], 7)

    def test_hyphenated_prose_not_counted(self):
        p = parse_comment(comment("sub-spectrum +7 chatter"))
        self.assertIsNone(p["score"])

    def test_json_has_audit_trail(self):
        r = self._run_cli_offline(
            [comment("**Seat:** Naya Alpha\nSpectrum +8", cid=1),
             comment("Spectrum +15", cid=2)])
        data = json.loads(r.stdout)
        parsed = data["readout"]["parsed"]
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["score"], 8)
        self.assertEqual(parsed[1]["excluded"], "out_of_range")

    def test_nondict_payload_clean_refusal(self):
        r = self._run_cli_offline([{"id": 1}, "junk"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("refusing", r.stderr + r.stdout)

    def test_window_scoped_to_scored(self):
        a = comment("no spectrum", cid=1, created="2026-10-15T00:00:00Z")
        b = comment("Spectrum +7", cid=2, created="2026-10-15T06:00:00Z")
        data = aggregate([parse_comment(x) for x in (a, b)])
        self.assertEqual(data["window_oldest"], "2026-10-15T06:00:00Z")
        self.assertEqual(data["window_scope"], "scored comments")

    def _run_cli_offline(self, payload):
        script = __file__.rsplit("/", 1)[0] + "/spectrum_readout.py"
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(payload, f)
            path = f.name
        return subprocess.run(
            [sys.executable, script, "--comments-file", path, "--json"],
            capture_output=True, text=True)


class TestAggregate(unittest.TestCase):
    def test_distribution_and_mean(self):
        parsed = [parse_comment(comment(f"Spectrum {s}", cid=i))
                  for i, s in enumerate([7, 7, -4, 0])]
        data = aggregate(parsed)
        self.assertEqual(data["distribution"], {-4: 1, 0: 1, 7: 2})
        self.assertEqual(data["comments_scored"], 4)
        self.assertEqual(data["mean"], 2.5)
        self.assertEqual(data["min"], -4)
        self.assertEqual(data["max"], 7)

    def test_unscored_never_zero_filled(self):
        parsed = [parse_comment(comment("no spectrum here", cid=1))]
        data = aggregate(parsed)
        self.assertEqual(data["comments_scored"], 0)
        self.assertIsNone(data["mean"])
        self.assertEqual(data["distribution"], {})

    def test_by_seat(self):
        a = comment("**Seat:** Naya Alpha\nSpectrum +8", cid=1)
        b = comment("**Seat:** Naya Alpha\nSpectrum +6", cid=2)
        c = comment("**Seat:** Naya Beta\nSpectrum -2", cid=3)
        data = aggregate([parse_comment(x) for x in (a, b, c)])
        self.assertEqual(data["by_seat"]["Naya Alpha"], {"n": 2, "mean": 7.0})
        self.assertEqual(data["by_seat"]["Naya Beta"], {"n": 1, "mean": -2.0})


class TestCLI(unittest.TestCase):
    def _run_cli(self, payload):
        script = __file__.rsplit("/", 1)[0] + "/spectrum_readout.py"
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(payload, f)
            path = f.name
        return subprocess.run(
            [sys.executable, script, "--comments-file", path, "--json"],
            capture_output=True, text=True)

    def test_offline_mode_json(self):
        payload = [comment("**Seat:** Naya Alpha\nSpectrum +8", cid=1),
                   comment("no spectrum", cid=2)]
        r = self._run_cli(payload)
        self.assertEqual(r.returncode, 0, r.stderr)
        data = json.loads(r.stdout)
        self.assertEqual(data["readout"]["comments_scored"], 1)
        self.assertEqual(data["readout"]["distribution"], {"8": 1})

    def test_nonlist_payload_refuses(self):
        r = self._run_cli({"not": "a list"})
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
