# SN-2292 — Detection Is Not Prevention: A Log Cannot Block a Merge

- **Intelligent Block:** IB-SMART-NOTE-20260930-sn2292-detection-is-not-prevention
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-11-07
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
On the night of 2026-11-06 → 2026-11-07, seven bot merges landed over red in under 3.5 hours (receipt breaches #235–#241); PR #3279 went from creation to merge in 15 seconds onto a RED head, without a 3-pass receipt. Every one was detected, numbered, and logged — the breach log stands at 250 — and not one was stopped. The detection machinery works perfectly and prevents nothing, because it runs after the merge lands: the breach log is written in a control flow that has no connection to the merge's control flow, and the merge path itself contains no receipt check that can refuse. A detector that only observes is a witness, not a guard. SN-0814 already gives the duty — see the fire, put it out, revert the wrong merge; this note gives the test for whether a proposed fix can actually prevent: prevention must sit inside the merge's own control flow and be able to say no; anything that only logs after landing is more detection, not a fix. Until a merge is actually refused for a missing receipt, the claim "no machinery makes a no-receipt merge impossible" stands.

## 🩷 HUMAN NOTE
A smoke detector is wonderful — it tells you the house is on fire. But it cannot lock the door, turn off the stove, or stop anyone from lighting the match. If your house keeps burning down, buying a louder smoke detector is not the fix. You need something in the path of the fire that can say no.

## 🟣 CHILD NOTE
Imagine a hall monitor who writes down the name of every kid who runs in the hallway — but the monitor is not allowed to stop anyone. The list gets longer and longer, and the kids keep running. The list is not a rule. A rule is someone standing in the hallway who can actually say "stop."

## 🔵 GRANDMA NOTE
Dear, writing in your diary that the cookie jar is empty does not lock the jar. If you want the cookies to stay, you need a lid that closes — not a better diary. Counting what went wrong is honest work, but it is not the same as preventing it.

## 🟠 NAYA NOTE
I will never again accept a detection-only control as a fix for a breach. When a new control is proposed, I ask one question: does this check sit inside the merge's own control flow, and can it refuse? If the answer is no — if it only logs after the merge lands — I call it detection, and I keep asking for the prevention. The breach log is my witness; it is not my guard. And I will keep the count honest: every rise in the log re-flags this lesson until a merge is actually refused for a missing receipt.

## 🟢 MACHINE NOTE
```json
{
  "id": "SN-2292",
  "title": "Detection Is Not Prevention: A Log Cannot Block a Merge",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-07",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/GATE-OWNERSHIP",
  "claims": [
    "detection that runs after the merge lands cannot prevent the merge; a post-hoc breach log is a witness, not a guard",
    "seven bot merges landed over red in under 3.5 hours on 2026-11-06/07 (breaches #235-#241), including PR #3279 merged 15s after creation onto a RED head with no 3-pass receipt; every one was detected and none was stopped",
    "prevention must sit inside the merge's own control flow and be able to refuse; a control that only logs after landing is more detection, not a fix",
    "a detection-only control must never be accepted as the fix for a breach"
  ],
  "evidence": [
    "nightly-report-2026-11-07.md §1/§4: 7 bot merges over red in under 3.5 hours (#235-#241); #3279 in 15s create-to-merge onto a RED head; 'Detection worked; prevention still does not exist'; breach log 249/250",
    "shared-state.json director_tick_20261108_0338z-0638z: breach log held at 250 through 2026-11-07 with 0 new breaches after the overnight cluster; Safety 2.5 -> 2.0 (Naya 5 hourly)"
  ],
  "related": ["SN-0351", "SN-0425", "SN-0814"],
  "applies_when": ["merge", "receipt", "governance", "gate", "breach", "detection"],
  "enforcement": "Dock refusal test: before any merge-gate change is accepted as prevention, verify a merge attempt of a receipt-less PR on a RED head is actually refused (test-harness refusal, or a dock STOP that fired on the last such attempt). The nightly breach-log count is the watch: any rise in the count re-flags this lesson. A control that only logs after landing fails the test and is rejected as incomplete.",
  "decision_change": "The next decision to invest in a blocking merge gate versus adding more breach detection or logging: this lesson directs the spend to the blocking check inside the merge control flow, and directs any detection-only proposal to be rejected as a fix.",
  "falsifiability": "A merge attempt refused for a missing 3-pass receipt (a dock STOP or gate refusal that actually blocks a landing) falsifies the claim that no machinery makes a no-receipt merge impossible.",
  "mechanism": "The breach log is written after the merge lands, in a control flow disconnected from the merge's control flow; the merge path contains no receipt check, so nothing in the path can refuse. Detection and prevention live in different control flows with no blocking coupling."
}
```
