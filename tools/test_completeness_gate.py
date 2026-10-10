#!/usr/bin/env python3
"""Tests for the Completeness Gate (Gate 3 of 7).

Fixture-tree tests: they prove the predicate logic against synthetic notes.
Real proof is the gate run against the live SMART-NOTES tree (see the
adversarial section below — the 8 genuinely incomplete notes on main).

Adversarial cases covered:
  - note missing the AI (NAYA NOTE) form            -> FAIL
  - note missing the human form                     -> FAIL
  - note missing / unparseable machine JSON         -> FAIL
  - note stranded outside the canonical tree        -> FAIL
  - note under a malformed date partition           -> FAIL
  - note with no identifiable owner                 -> flagged, not failed
  - evidence-corpus copy (allowlisted)              -> not stranded
  - code-form gap                                   -> warning only
  - SN dir / filename id mismatch                   -> warning only
  - --strict promotes warnings to failures
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import completeness_gate as cg  # noqa: E402

PROSE = "Substantive prose carrying the note's meaning for its audience. "


def good_note(sn="SN-0901", provenance="relayed by Naya 2",
              machine_json='{"sn": "SN-0901", "truth_state": "CANDIDATE"}'):
    return f"""# Fixture Note {sn}

**Smart Note:** {sn}
**Truth state:** CANDIDATE
**Provenance:** {provenance}

## IN A NUTSHELL

{PROSE * 3}

## HUMAN NOTE

{PROSE * 4}

## CHILD NOTE

{PROSE * 2}

## GRANDMA NOTE

{PROSE * 2}

## NAYA NOTE

{PROSE * 4}

## MACHINE NOTE

{machine_json}
"""


def drop_section(text, section):
    """Remove a `## ... SECTION` block (header through next header)."""
    import re
    return re.sub(
        r"^#+\s*[^\w\n]*" + section + r"\b.*?(?=^#+\s|\Z)",
        "",
        text,
        flags=re.M | re.S,
    )


class FixtureRepo:
    """A fake repo root with a canonical SMART-NOTES tree."""

    def __init__(self, base: Path):
        self.root = base
        self.notes = base / "BRAIN" / "05-MEMORY" / "SMART-NOTES"

    def note(self, sn, rel_dir="2026/10/10/SYSTEM-INTELLIGENCE/TEST",
             body=None, fname=None, subdir=None):
        d = self.notes / rel_dir / (subdir or sn.replace("-", "-"))
        d.mkdir(parents=True, exist_ok=True)
        name = fname or f"IB-SMART-NOTE-20261010-{sn.lower().replace('-', '')}-fixture.md"
        p = d / name
        p.write_text(body if body is not None else good_note(sn), encoding="utf-8")
        return p

    def tool_ref(self, sn, fname="consumer.py"):
        t = self.root / "tools"
        t.mkdir(exist_ok=True)
        (t / fname).write_text(f"# consumes {sn}\nX = '{sn}'\n", encoding="utf-8")


class CompletenessGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.fx = FixtureRepo(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def gate(self, **kw):
        return cg.run(Path(self.tmp.name), **kw)

    # ---- happy path -----------------------------------------------------
    def test_good_note_passes(self):
        self.fx.note("SN-0901")
        self.fx.tool_ref("SN-0901")
        rep = self.gate()
        self.assertEqual(rep["notes_checked"], 1)
        self.assertEqual(rep["failures"], 0, rep["notes"])
        self.assertEqual(rep["warnings"], 0, rep["notes"])
        n = rep["notes"][0]
        self.assertTrue(all(n["forms"].values()))
        self.assertEqual(n["owner"]["id"], "Naya 2")

    def test_main_exit_zero_on_pass(self):
        self.fx.note("SN-0901")
        self.fx.tool_ref("SN-0901")
        self.assertEqual(
            cg.main(["--root", self.tmp.name]), 0)

    # ---- four-form failures ----------------------------------------------
    def test_missing_ai_form_fails(self):
        self.fx.note("SN-0902", body=drop_section(good_note("SN-0902"), "NAYA NOTE"))
        rep = self.gate()
        self.assertEqual(rep["failures"], 1)
        self.assertIn("AI form", rep["notes"][0]["failures"][0])
        self.assertEqual(cg.main(["--root", self.tmp.name]), 1)

    def test_missing_human_form_fails(self):
        self.fx.note("SN-0903", body=drop_section(good_note("SN-0903"), "HUMAN NOTE"))
        rep = self.gate()
        self.assertEqual(rep["failures"], 1)
        self.assertIn("human form", rep["notes"][0]["failures"][0].lower())

    def test_missing_machine_section_fails(self):
        self.fx.note("SN-0904", body=drop_section(good_note("SN-0904"), "MACHINE NOTE"))
        rep = self.gate()
        self.assertEqual(rep["failures"], 1)
        self.assertIn("machine form", rep["notes"][0]["failures"][0].lower())

    def test_machine_note_unparseable_json_fails(self):
        body = good_note("SN-0905", machine_json='{"sn": "SN-0905", broken,,,')
        self.fx.note("SN-0905", body=body)
        rep = self.gate()
        self.assertEqual(rep["failures"], 1)
        self.assertIn("unparseable", rep["notes"][0]["failures"][0])

    def test_machine_note_without_payload_fails(self):
        body = good_note("SN-0905", machine_json="just prose, no JSON object here")
        self.fx.note("SN-0906", body=body)
        rep = self.gate()
        self.assertEqual(rep["failures"], 1)
        self.assertIn("no JSON payload", rep["notes"][0]["failures"][0])

    def test_thin_prose_fails_human_form(self):
        body = good_note("SN-0907").replace(PROSE * 4, "short. ")
        self.fx.note("SN-0907", body=body)
        rep = self.gate()
        self.assertGreaterEqual(rep["failures"], 1)
        self.assertTrue(any("substantive" in f for f in rep["notes"][0]["failures"]))

    def test_emoji_section_headers_accepted(self):
        body = (good_note("SN-0908")
                .replace("## HUMAN NOTE", "## \U0001fa77 HUMAN NOTE")
                .replace("## NAYA NOTE", "## \U0001f916 NAYA NOTE")
                .replace("## MACHINE NOTE", "## \u2699\ufe0f MACHINE NOTE"))
        self.fx.note("SN-0908", body=body)
        self.fx.tool_ref("SN-0908")
        rep = self.gate()
        self.assertEqual(rep["failures"], 0, rep["notes"])

    # ---- placement ---------------------------------------------------------
    def test_stranded_note_fails(self):
        stray = self.fx.root / "BRAIN" / "05-MEMORY" / "stray"
        stray.mkdir(parents=True)
        (stray / "IB-SMART-NOTE-20261010-sn0910-stray.md").write_text(
            good_note("SN-0910"), encoding="utf-8")
        rep = self.gate()
        self.assertEqual(rep["failures"], 1)
        self.assertIn("stranded", rep["notes"][0]["failures"][0])

    def test_malformed_date_partition_fails(self):
        self.fx.note("SN-0911", rel_dir="2026/13/40/SYSTEM-INTELLIGENCE/TEST")
        rep = self.gate()
        self.assertEqual(rep["failures"], 1)
        self.assertIn("date partition", rep["notes"][0]["failures"][0])

    def test_allowlisted_evidence_copy_not_stranded(self):
        corp = self.fx.root / "evidence" / "corpus"
        corp.mkdir(parents=True)
        (corp / "IB-SMART-NOTE-20261010-sn0912-copy.md").write_text(
            good_note("SN-0912"), encoding="utf-8")
        rep = self.gate()
        self.assertEqual(rep["notes_checked"], 1)
        self.assertFalse(any("stranded" in f for f in rep["notes"][0]["failures"]),
                         rep["notes"])

    def test_sn_dir_filename_mismatch_warns(self):
        self.fx.note("SN-0913", subdir="SN-0913",
                     fname="IB-SMART-NOTE-20261010-sn9999-other.md")
        rep = self.gate()
        self.assertEqual(rep["failures"], 0)
        self.assertTrue(any("mismatch" in w for w in rep["notes"][0]["warnings"]),
                        rep["notes"])

    # ---- owner: flagged, never blocking --------------------------------------
    def test_unowned_note_flagged_not_failed(self):
        body = good_note("SN-0914", provenance="source unknown")
        self.fx.note("SN-0914", body=body)
        self.fx.tool_ref("SN-0914")
        rep = self.gate()
        self.assertEqual(rep["failures"], 0)
        self.assertEqual(rep["notes"][0]["owner"], None)
        self.assertTrue(any("unowned" in w for w in rep["notes"][0]["warnings"]))
        self.assertEqual(cg.main(["--root", self.tmp.name]), 0)

    def test_explicit_owner_field_accepted(self):
        body = good_note("SN-0915").replace(
            "**Provenance:** relayed by Naya 2", "**Owner:** Naya 4")
        self.fx.note("SN-0915", body=body)
        rep = self.gate()
        self.assertEqual(rep["notes"][0]["owner"]["id"], "Naya 4")
        self.assertEqual(rep["notes"][0]["owner"]["evidence"], "explicit Owner field")

    def test_strict_promotes_owner_warning_to_failure(self):
        body = good_note("SN-0916", provenance="source unknown")
        self.fx.note("SN-0916", body=body)
        self.fx.tool_ref("SN-0916")
        self.assertEqual(cg.main(["--root", self.tmp.name, "--strict"]), 1)

    # ---- code form: warning only ---------------------------------------------
    def test_code_form_gap_is_warning_only(self):
        self.fx.note("SN-0917")  # no tools/ reference
        rep = self.gate()
        self.assertEqual(rep["failures"], 0)
        self.assertFalse(rep["notes"][0]["forms"]["code"])
        self.assertTrue(any("code form" in w for w in rep["notes"][0]["warnings"]))

    def test_code_form_present_when_referenced(self):
        self.fx.note("SN-0918")
        self.fx.tool_ref("SN-0918")
        rep = self.gate()
        self.assertTrue(rep["notes"][0]["forms"]["code"])
        self.assertFalse(any("code form" in w for w in rep["notes"][0]["warnings"]))

    # ---- units ---------------------------------------------------------------
    def test_extract_note_id(self):
        p = Path("BRAIN/05-MEMORY/SMART-NOTES/2026/10/04/x/SN-0282/"
                 "IB-SMART-NOTE-20261004-sn0282-do-it-now-doctrine.md")
        self.assertEqual(cg.extract_note_id(p), "SN0282")
        p2 = Path("x/SN-NET-POWER-MAGIC-001/IB-SMART-NOTE-20261005-NET-POWER-MAGIC-001.md")
        self.assertEqual(cg.extract_note_id(p2), "SNNETPOWERMAGIC001")

    def test_is_note_file(self):
        self.assertTrue(cg.is_note_file(Path("IB-SMART-NOTE-20261010-sn1-x.md")))
        self.assertTrue(cg.is_note_file(Path("SMART-NOTE-20261010-sn-1.json".replace(".json", ".md"))))
        self.assertFalse(cg.is_note_file(Path("random-doc.md")))
        self.assertFalse(cg.is_note_file(Path("IB-SMART-NOTE-x.json")))

    def test_json_output(self):
        self.fx.note("SN-0919")
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cg.main(["--root", self.tmp.name, "--json"])
        doc = json.loads(buf.getvalue())
        self.assertEqual(doc["notes_checked"], 1)
        self.assertEqual(rc, 0)

    def test_changed_only_detects_new_note(self):
        root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "t@t"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=root, check=True)
        (root / "base.txt").write_text("base")
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=root, check=True)
        subprocess.run(["git", "update-ref", "refs/remotes/origin/main", "HEAD"],
                       cwd=root, check=True)
        p = self.fx.note("SN-0920", body=drop_section(good_note("SN-0920"), "NAYA NOTE"))
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "note"], cwd=root, check=True)
        found = cg.changed_note_files(root)
        self.assertEqual([f.name for f in found], [p.name])
        rep = cg.run(root, found)
        self.assertEqual(rep["failures"], 1)  # missing AI form blocks


if __name__ == "__main__":
    unittest.main()
