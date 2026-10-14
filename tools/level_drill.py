#!/usr/bin/env python3
"""LEGACY INSTRUMENT — SEALED BY SUCCESSOR (Lane 9, t0765).

This file used to carry the full level-drill answer material. It no longer
carries anything: a blind subject who reaches it gets a loud refusal, never
the material. Importing it fails closed on purpose.

Where things live now (blind protocol):
- scenarios: tools/level_drill_scenarios.py (no answers, machine-proven by
  tools/verify_drill_blindness.py)
- sealed answers: tools/level_drill_key.py (protocol-named, subjects stay out)
- scoring: tools/level_drill_grade.py (external grader, scorer seat only)

Pre-fix content is preserved in git history at commit cde0c63dd for audit.
Amend-by-duplication record: t0765-lane9 receipt names the diff; nothing here
was silently rewritten.
"""
raise RuntimeError(
    "tools/level_drill.py is a sealed legacy instrument: it carries no "
    "answer material and refuses to run. Use "
    "tools/level_drill_scenarios.py (scenarios), tools/level_drill_grade.py "
    "(scoring), and tools/verify_drill_blindness.py (blindness proof). "
    "Subjects never touch the sealed file."
)
