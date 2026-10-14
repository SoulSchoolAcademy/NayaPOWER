# Compounding Is Countable — The Lesson-to-Decision Link Graph

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01257-compounding-is-countable-lesson-decision-link-graph
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** `hidden_files/lesson_decision_linker.py` (built 2026-10-13 ~20:55 PDT, Shawn's standing charge: learning 5→10 is the goal); baseline `hidden_files/lesson-compounding-baseline.jsonl` — 576 receipts scanned, 63 citing lessons, 83 unique lessons cited (top: SN-016 Judgment Rule, 16 receipts); two false-positive classes excluded (L### colliding with code line refs, e.g. vc.py L47/L47-48, incl. unicode en/em dashes).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The 10/10 learning bar is PROVEN COMPOUNDING: a lesson demonstrably changing a future decision. `lesson_decision_linker.py` makes it countable — it scans every lane receipt for lesson citations (L###, SN-####, lesson phrases), builds the lesson→decision link graph, and trends the count. Baseline 2026-10-13: 576 receipts scanned, 63 citing lessons, 83 unique lessons cited. A lesson that never appears in a future receipt's citations is unproven compounding. The hourly learning review no longer hunts manually — it steers by this number; it must climb.

## 🩷 HUMAN NOTE

"Are we learning?" is a feeling question until you count something. The receipts are the team's decision record — every sign-out says what was decided and why. When a receipt cites a lesson ID, that's a measurable trace of the lesson changing a decision. Count those traces, trend them, and "learning is compounding" stops being a vibe and becomes a number you can steer. Honest caveat: a citation is a proxy, not a proof — someone can cite a lesson without being changed by it. But it's the measurable lower bound, and a lesson with zero citations across 576 receipts is definitely not compounding.

## 🟣 CHILD NOTE

Imagine you teach your friend a shortcut for tying shoes. How do you know they really learned it? You watch: the next time they tie their shoes, do they use your shortcut — and do they say "I'm using your trick"? Every time they say so, that's one point. Count the points over a week. If the points go up, the teaching is working. If nobody ever mentions the trick again, it didn't stick — no matter how good the trick was.

## 🔵 GRANDMA NOTE

It's like tracking whether advice actually gets used. You give the family a recipe tip; the proof isn't that they nodded — it's that next month's grocery lists show the new ingredient, and someone says "used your tip." The linker is the one who reads all the grocery lists and counts. The baseline is the first count: out of 576 lists, 63 mention a tip, across 83 different tips. Now we watch the number climb — or we admit the tips aren't landing.

## 🟠 NAYA NOTE

Apply this wherever learning is claimed: (1) define compounding as citation-in-decision-records — the lesson→decision link graph is the instrument, the trend is the verdict; (2) scan the actual decision records (receipts), not chat claims — chat says "learned"; receipts show what the decision cited; (3) exclude the false positives mechanically — lesson-ID patterns collide with code line references (vc.py L47); the lookarounds are part of the instrument, not polish; (4) trend, don't snapshot — one count is a baseline, the climb is the proof; wire the count into the review cadence (here: the hourly learning review) so it gets steered, not filed; (5) treat zero-citation lessons as the work queue — a captured lesson nobody cites is inventory, not intelligence; (6) remember the proxy caveat — citation ≠ proven influence — and say so; the number is the floor of compounding, not the ceiling.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "unmeasured_compounding_claim",
  "evidence": {
    "instrument": "hidden_files/lesson_decision_linker.py (2026-10-13 ~20:55 PDT) — scans hidden_files/twelve-lane-receipts/*.md for lesson citations, writes hidden_files/lesson-decision-links.jsonl",
    "baseline": "hidden_files/lesson-compounding-baseline.jsonl — {\"receipts_scanned\": 576, \"receipts_citing_lessons\": 63, \"unique_lessons_cited\": 83, \"top\": \"SN-016 Judgment Rule, 16 receipts\"}",
    "false_positives_excluded": "L### colliding with code line refs (vc.py L47, L47-48) via lookarounds incl. unicode en/em dashes",
    "steering": "hourly learning review now steers by the link-rate trend"
  },
  "rule": "compounding_is_countable",
  "mechanism": "receipts are the decision record; lesson IDs (L###, SN-####, lesson phrases) are machine-extractable citations within them; the citation graph makes influence visible and trendable; citation is a proxy (lower bound) for influence, not proof of it",
  "falsifier": "the scan is deterministic on receipts — re-run must reproduce the baseline; the note's claim ('this measures compounding') is weakened if cited lessons can be shown not to correspond to actual decision influence — which is why the proxy caveat is stated, not hidden",
  "decision_changed": "is learning compounding (5→10)? — previously hunted manually per tick; now measured and trended; the number must climb, and zero-citation lessons become the work queue",
  "related": ["SN-016 (Judgment Rule — the most-cited lesson in the baseline, 16 receipts)"]
}
~~~
