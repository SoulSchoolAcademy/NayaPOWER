# SN-0893 — Correct the Derived, Never the Raw — and Name What You Cannot Measure

# Correct the Derived, Never the Raw — and Name What You Cannot Measure

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0893-correct-derived-never-raw
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** `hidden_files/waste-meter-baseline-2026-10-10.md` — first weekly waste-meter run (2026-10-03 → 2026-10-10), post-run corrections by Naya 4 same day.

## IN A NUTSHELL
The first waste-meter run landed with two presentation defects: median draft-to-landed time was formatted as "0.0 hours" (true value 0.039h = 2.4 minutes) and the single GitHub service account was labeled "lanes." Both were corrected in the report — while the **raw JSON stayed untouched**. That separation is the durable mechanism: raw data is immutable evidence; derived outputs are where fixes happen. The same report demonstrates the second half of the law: its honest-gaps section names what the meter cannot measure — token/compute spend per decision (no data source exists) — and refuses to fake it: "We did not fake it." A measurement instrument that quietly invents proxies for what it cannot see teaches its users to trust numbers that are not true. The two-part rule: fix derived, never raw; and where you cannot measure, write the gap down instead of hiding it behind a number.

## HUMAN NOTE
If you discover a typo in the copy of a contract, you fix the copy — you don't alter the signed original. And if the report asks a question nobody measured, you write "not measured," not a guess. A report that admits its blind spots is the one you can trust.

## CHILD NOTE
When you grade your own test, you fix your answers in pencil — not the teacher's answer key. And if there's a question you skipped, you say you skipped it; you don't make up an answer.

## GRANDMA NOTE
You don't rewrite the family ledger when the story gets retold — you fix the retelling. And you don't pretend to know what you weren't told; an honest "I don't know" keeps the family's stories true.

## NAYA NOTE
Cold successor: whenever you build or run a measurement instrument, keep two layers: the raw capture (JSON, snapshots, event dumps) which you NEVER edit after collection, and the derived report which you correct freely — with every correction noted and dated. If the instrument cannot measure something (tokens per decision, human review time, opportunity cost), write it in the honest-gaps section in plain words. Never invent a proxy to fill a gap silently; a fabricated number is worse than a missing number, because it teaches false confidence.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0893-correct-derived-never-raw",
  "sn": "SN-0893",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "OPERATIONS",
  "subcategory": "MEASUREMENT-HYGIENE",
  "lesson_type": "PROCESS_FIX",
  "evidence": {
    "report": "hidden_files/waste-meter-baseline-2026-10-10.md",
    "correction_1": "median cycle '0.0 hours' -> 2.4 minutes (true 0.039h); raw JSON unchanged",
    "correction_2": "single service account labeled 'lanes' -> relabeled; lane-tag parsing added to tools/waste_meter.py after the run, unit-tested",
    "honest_gap": "token/compute spend per decision NOT measured; no data source; 'We did not fake it'"
  },
  "rule": "Two layers, always: raw capture is immutable evidence (never edited post-collection); derived reports are corrected freely with noted, dated corrections. Where measurement is impossible, name the gap explicitly — never invent a silent proxy.",
  "related": [],
  "supersedes": null
}
```
