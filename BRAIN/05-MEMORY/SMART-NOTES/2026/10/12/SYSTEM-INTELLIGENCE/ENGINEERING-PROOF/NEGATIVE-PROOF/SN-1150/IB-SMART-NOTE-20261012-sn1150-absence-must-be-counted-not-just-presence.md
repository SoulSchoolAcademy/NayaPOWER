# INTELLIGENT BLOCK — SN-1150
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured date: 2026-10-12
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Absence must be counted, not just presence. A check regime that only examines marked cases can never catch omission — a dispatcher that forgets to emit leaves a brief indistinguishable from a hand-embedded one. The spec's teeth cover forged presence, not absent presence. So the battery must sample the zero-marker cases against the source-of-record too: one zero-marker brief per wave against the dispatch log.

## HUMAN NOTE
Lane 1's t0570 second-seat review of the provenance-marker spec found the residual hole nobody's battery could see: the spot-check samples one marker per dispatch wave — it never examines zero-marker briefs. Marker omission is invisible to the battery AND to the named mitigation. A dispatcher that arm-runs and forgets (or declines) to emit leaves a brief indistinguishable from a hand-embedded one; the only record of the omission is the "N/A with reason" line in the dispatch log, which nothing battery-checks. This is the same failure shape as the t0558 Sage "13 vs 12" class: what you don't count doesn't get checked. The amendments close it structurally: A1 pins the `fired` vocabulary (referenced conventions become owned lists), A2 adds an explicit field-status table (judged vs audit-only), A3 cross-checks tick == brief tick — and the mitigation extends the wave spot-check to one zero-marker brief per wave sampled against the dispatch log's `retrieval:` line. The general rule: whenever a check regime samples successes, ask what the un-sampled class is hiding, and sample it too.

## CHILD NOTE
Imagine the teacher only checks the homework of kids who raised their hands. The kids who forgot their homework just don't raise their hands — and the teacher never notices. If you want to know who forgot, you have to check the quiet kids too.

## GRANDMA NOTE
Counting the jars on the shelf tells you nothing about the jars that never got shelved. If you only ever count what's there, you'll never notice what's missing. Check the empty spots too.

## NAYA NOTE
When I design or review a check, I list the sampled class AND the un-sampled class, and I ask: what failure hides in the un-sampled class that this battery could never see? If omission is possible, I add an explicit zero-case sample against the source-of-record (the dispatch log, the registry, the primary source — never the check's own output). Presence checks prove presence; only absence sampling proves coverage.

## MACHINE NOTE
{
  "sn": "SN-1150",
  "lesson_id": "candidate-64",
  "rule": "OMISSION_POSSIBLE -> check regime MUST include zero-case sampling against source-of-record; presence-only sampling is an incomplete coverage proof",
  "forbidden": ["spot-checking only marked/present cases when omission is a live failure mode", "trusting a 'clean' sample that never examines the zero-marker class"],
  "cousins": ["SN-1079 absence-takes-two-witnesses (epistemology: an absence claim needs two agreeing reads)", "SN-1148 sweeps-reread-primary-sources (never inherit a registry count)", "SN-1145 t0558 what-you-dont-count-doesnt-get-checked family"],
  "evidence": {
    "lane_receipt": "hidden_files/twelve-lane-receipts/t0570-lane1.md",
    "residual_hole": "Marker omission is invisible to the battery AND to the named mitigation. The spec's teeth cover forged presence, not absent presence.",
    "mitigation": "sample one zero-marker brief per wave against the dispatch log; amendments A1 (pin fired vocabulary), A2 (field-status table judged vs audit-only), A3 (tick == brief tick cross-check)",
    "learning_events": "hidden_files/learning-events-2026-10-12-20.md"
  },
  "admission": {"durable": true, "new": true, "signal": true, "evidence_backed": true}
}
