# IB-SMART-NOTE — SN-1275 — Probe Past the Author's Boundary

Intelligent Block: IB-SMART-NOTE-20261014-sn1275-probe-past-the-authors-boundary
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-14
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
A verification battery that only replays the author's own RED cases confirms the fix and misses the hole: residual defects live one rung past the author's calibrated edge. Every independent scorecard battery must include at least one probe the author's own battery never wrote. A verdict is a measurement, not a story.

## HUMAN NOTE
The independent scorecard on PR #2566 (t0730-lane3) ran the author's full green battery — then deliberately probed one rung past the author's stated boundary and found a real residual hole (row B: repo-domain unrelated thread passes) that the author's battery couldn't see by construction. Instead of burying it under the green battery, the seat named the residual hole inside the MERGE-READY verdict: the verdict reports the measurement, not the narrative the author wrote. Root cause of the blind spot: a battery built by the author replays the author's own RED cases, so it inherits the author's calibration — confirmation can't see past its own edge. The remedy is structural: every scorecard battery now includes at least one probe the author's own battery never wrote. Evidence: hidden_files/twelve-lane-receipts/t0730-lane3.md, learning-events-2026-10-14-01.md (candidate 251).

## CHILD NOTE
Imagine you built a fort and your friend checks if it's strong — but your friend only tests the doors you told them about. The hole will be in the wall you never mentioned. A real checker always looks one place past where you said "we're done."

## GRANDMA NOTE
Honey, when someone checks another person's work, they shouldn't only look where they were told to look. The mistake is always hiding just past the edge of where the builder stopped checking.

## NAYA NOTE
Independent-verification doctrine: a battery that only replays the author's stated RED cases is a replay, not a probe. The independent seat's battery = author's battery PLUS at least one probe the author's own battery never wrote — aimed one rung past the author's calibrated edge. The verdict names residual holes inside the verdict (measurement, not story); a named residual inside a MERGE-READY verdict is honesty, not failure. This is the adversarial-battery family: the hole survives exactly because the author's battery was never pointed at it.

## MACHINE NOTE
{
  "smart_note_id": "SN-1275",
  "intelligent_block_id": "IB-SMART-NOTE-20261014-sn1275-probe-past-the-authors-boundary",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "category": "SYSTEM-INTELLIGENCE",
  "subcategory": "ENGINEERING-PROOF/INDEPENDENT-VERIFICATION",
  "captured": "2026-10-14",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "independent_battery = author_battery + at_least_one_probe_beyond_author_edge",
  "verdict_shape": "residual_holes_named_inside_verdict",
  "falsifier": "if residual defects reliably fell inside the author's calibrated edge, the one-rung-past probe would add nothing; t0730-lane3 falsifies that (row B found past the edge)",
  "evidence": ["hidden_files/twelve-lane-receipts/t0730-lane3.md", "learning-events-2026-10-14-01.md (candidate 251)"]
}
