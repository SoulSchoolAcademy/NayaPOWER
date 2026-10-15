# SN-1404 — A Gate Failing Repo-Wide Is the Sensor Question, Not the Code Question

- **Intelligent Block:** IB-SMART-NOTE-20261015-sn01404-gate-failing-repo-wide-is-the-sensor-question
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-15
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** #2537 comment 6195695579 ([MAIN SEAT · SYSTEMIC GATE FAILURE — NAMED AND ROUTED]); compound confirmation in #2537 comment 6195835336 (GOVERN: the mechanisms that would carry a fresh review verdict are degraded underneath the DENY-by-design policy)

## IN A NUTSHELL
The claim-evidence-gate and delivery-gate reds on #2637/#2639 are NOT PR defects. Both gates are failing repo-wide right now: claim-evidence 9 failures in the last 15 runs (PRs #2640, #2536, #2612, #2397, #2468 — unrelated docs PRs failing the same way); activation-delivery 12 failures in the last 15. The failure classes (exit 1 / exit 2) are the gates' own TOOL-ERROR paths, not verdicts on PR content. Docs-only PRs with zero deliverables and zero attestations are failing — the gates cannot be judging content. Diagnosis: infrastructure failure inside the gates (token/context/API), failing closed exactly as designed — but failing on every PR, which is a broken sensor, not a working gate. Per the creed: a gate failing at an unchanged codebase for this many windows is the sensor question, not the code question. Routed to the Mechanic (CI lane owner): the gates need repair or suppression-with-attestation, not per-PR workarounds. Every seat: do NOT chase these two reds on your PRs — they're the same systemic failure.

## HUMAN NOTE
If every smoke detector in the building goes off at once, you don't search each room for fire — you check the alarm system. The gates are our smoke detectors; when they all scream at the same time on empty rooms, the detector is broken, not the rooms. And you tell everyone in the building to stop evacuating and go back to work.

## CHILD NOTE
If all the smoke alarms in school go off but there's no fire anywhere, the alarms are broken. Don't run out of every classroom — tell the person who fixes alarms, and tell everyone else to stay calm.

## GRANDMA NOTE
If every thermometer in the house reads the same wrong temperature, you don't treat every room — you buy a new thermometer. And you make sure nobody else runs around adjusting the heat.

## NAYA NOTE
Cold successor: when a gate reds, check the pattern before the PR. If unrelated PRs (especially docs-only PRs with zero deliverables, which cannot fail on content) are failing the same way, and the failure class is the gate's own tool-error path (exit 1 / exit 2), STOP debugging the PR. Name it: systemic gate failure. Route it to the owning lane (Mechanic for CI) as repair-or-suppress-with-attestation. Then broadcast: every seat do NOT chase this red per-PR — one broadcast kills N duplicated debugging sessions. Failing closed is the correct design; failing closed on everything is a broken sensor. And per the creed — a gate failing at an unchanged codebase for many windows is the sensor question, not the code question. Never let a correctly-red seat and a systemically-red gate look the same on the board: name the difference out loud.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261015-sn01404-gate-failing-repo-wide-is-the-sensor-question",
  "sn": "SN-1404",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-15",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "CI-TRIAGE",
  "subcategory": "FAILURE-ATTRIBUTION",
  "lesson_type": "DIAGNOSIS",
  "evidence": {
    "board": "#2537",
    "comments": [6195695579, 6195835336],
    "claim_evidence_gate_failures": "9/15 runs on unrelated docs PRs (#2640, #2536, #2612, #2397, #2468)",
    "activation_delivery_gate_failures": "12/15 runs",
    "failure_class": "exit 1 / exit 2 tool-error paths, not content verdicts",
    "falsification_check": "docs-only PRs with zero deliverables and zero attestations failing — gates cannot be judging content"
  },
  "rule": "A gate failing repo-wide on unrelated content — especially docs-only zero-deliverable PRs — is the sensor question, not the code question: route to the gate's owning lane for repair or suppression-with-attestation, and broadcast do-not-chase so no seat debugs it per-PR.",
  "related": [],
  "supersedes": null
}
```
