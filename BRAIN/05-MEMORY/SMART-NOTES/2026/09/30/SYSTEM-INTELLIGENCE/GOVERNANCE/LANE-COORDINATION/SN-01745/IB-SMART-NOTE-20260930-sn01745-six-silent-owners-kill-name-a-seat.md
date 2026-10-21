# Six Silent Owners Kill the Name-a-Seat Hypothesis: Assign Adversarial Work by Demonstrated Behavior, Not by Availability List

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01745-six-silent-owners-kill-name-a-seat
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-20 the director named, one after another, six owners for the EMIT-battery breaker packet (an identical 5-vector red battery against the hardened emit gate): Coda-1 (accept by 13:00Z), Epsilon (13:45Z), Delta (16:00Z), Zeta (17:15Z), GPT-6 (accept 19:15Z, full battery 20:00Z), Naya Resolve (accept 22:45Z). All six went silent — no acceptance receipt, no decline PULSE, no break receipts. Three rounds of the same hypothesis (name the next available seat from the roster, set a hard deadline) burned six owners and ~10 hours with zero receipts. Per the three-try circuit breaker, the sixth silence forced a HYPOTHESIS CHANGE: the broken leg was not any owner — it was the selection mechanism itself. Review/law seats would not take adversarial breaker work regardless of roster position; breaker work demands a temperament (coldness at acceptance, premise-verification first, refusal to touch builder artifacts), and only evidence of that behavior predicts acceptance. The reframe: select on demonstrated breaker behavior (Resolve's #2755 gap-close packet — premise-verification first, re-fire-watch discharged with evidence, scored 9/10 — plus awake-and-posting evidence), and when even the behavior-selected owner stays silent, stop naming: the battery returns to the OPEN QUEUE (no seventh owner; the reframe is the last naming attempt, the next pass audits rather than names). The sixth-owner decision's own decline path carried this out: Resolve missed the 22:45Z acceptance → battery OPEN QUEUE.

## 🩷 HUMAN NOTE

Shawn — imagine hiring for a demolition job and going down the phone list: six calls, six no-answers. After the third no-answer you stop calling names off the list — the list isn't the problem, the job is: demolition needs people who have already swung a hammer. Same here: breaking the emit gate needs seats that have already broken things, with the receipts to prove it. So the rule now: for adversarial work, pick by proof of past breaking, not by whose name is next on the roster — and if the proven seat doesn't pick up, the job goes back in the queue instead of a seventh cold call. The decline path is the machinery that makes "no seventh name" a decision instead of a shrug.

## 🟣 CHILD NOTE

A soccer coach needs a penalty-shootout kicker. She doesn't point at whoever's next on the clipboard — she picks the kid who has scored penalties before. And if that kid isn't at practice today, she doesn't point at the next name anyway; she leaves the slot open and figures out the next move. Picking blind names wasted six slots today; picking by what the kid already did is the whole trick.

## 🔵 GRANDMA NOTE

Like hiring a handyman: you don't call down the yellow pages — you call the one who fixed your sink last time, because you saw the sink get fixed. And if he's busy, you don't hire a stranger sight unseen just to keep moving; you put the job on the list and wait for the right hands. Six strangers were offered the job today and none picked up the phone. The lesson: the phone list was never the tool — the memory of who fixed what was.

## 🟠 NAYA NOTE

Apply to any dispatcher or watch that assigns adversarial work (breaker batteries, falsification packets, adversarial IV, red-team re-derivation, cold breaker re-fire watches): (1) keep a decline ledger — every owner naming records the accept-by deadline and the decline path; (2) count consecutive silent owners (no acceptance receipt, no decline PULSE by deadline); (3) at three consecutive silences the circuit breaker fires: no fourth name on the availability hypothesis — the dispatcher must first write a HYPOTHESIS CHANGE (what I tried / why it failed / what I'm trying instead / why it's different at the ROOT) and reframe selection onto demonstrated behavior evidence (prior break receipts on the same defect class + a coldness STOP honored at acceptance); (4) when the behavior-selected owner also goes silent, the packet returns to the OPEN QUEUE — no seventh naming; the reframe is the last naming attempt and the next pass audits rather than names; (5) never select breaker owners from availability rotation alone — the roster lists who is present, only the evidence lists who is proven. This is the selection-side sibling of the three-try circuit breaker (AGENTS.md): that law stops the worker from trying the same wall a fourth time; this law stops the dispatcher from naming at the same wall a fourth time. And per L569, audit the leg, not the lane — the naming mechanism was the broken leg, so changing owners inside the same mechanism was new paint on the same wall.

## 🟢 MACHINE NOTE

```json
{
  "slug": "six-silent-owners-kill-name-a-seat",
  "sn": "SN-1745",
  "title": "Six Silent Owners Kill the Name-a-Seat Hypothesis: Assign Adversarial Work by Demonstrated Behavior, Not by Availability List",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-20",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["dispatcher", "battery-owner", "breaker-work", "circuit-breaker", "owner-assignment", "adversarial-iv"],
  "enforcement": "The dispatcher keeps a per-battery decline ledger: every owner naming records accept-by deadline + decline path. At three consecutive silent owners (no acceptance receipt, no decline PULSE by deadline), the circuit breaker fires: the dispatcher may not name a fourth owner on the availability hypothesis — it must first write a HYPOTHESIS CHANGE note and reframe selection onto demonstrated behavior evidence (prior break receipts on the same defect class + coldness STOP honored at acceptance). When the behavior-selected owner also goes silent, the battery returns to the OPEN QUEUE (no seventh naming). Any battery carrying four or more consecutive availability-hypothesis namings with no HYPOTHESIS CHANGE note is a tripwire violation: the breaker never fired.",
  "evidence": {
    "sixth-owner-decision": "shared-state.json director_decision_emit_battery_sixth_owner_20261020 (2026-10-20T22:08:00Z): six silent owners — Coda-1 (accept 13:00Z), Epsilon (13:45Z), Delta (16:00Z), Zeta (17:15Z), GPT-6 (accept 19:15Z / battery 20:00Z), Naya Resolve (accept 22:45Z); HYPOTHESIS CHANGE with falsifier; naming a battery owner explicitly ruled not a protected gate",
    "owner-sequence": "shared-state.json director_decision_emit_battery_fourth_owner_20261020 (16:47Z) + director_decision_emit_battery_fifth_owner_20261020 (18:44Z): the same name-a-seat + hard-deadline hypothesis named Zeta, then GPT-6, each with accept-by deadlines; both silent — five named silences before the reframe",
    "open-queue-outcome": "director_tick_20261020_1608 (2026-10-20T23:08Z, shared-state.json): Resolve missed the 22:45Z acceptance (no receipt, no PULSE) -> battery OPEN QUEUE per the sixth-owner decision's decline path; 'no seventh owner — the reframe is the last naming attempt'",
    "mechanism-precedent": "AGENTS.md THE THREE-TRY CIRCUIT BREAKER: 'Three rounds is the budget for one hypothesis. After three, you think differently or you stop.' L569: 'audit the leg, not the lane — the naming mechanism was the broken leg'"
  },
  "decision_changed": "How the dispatcher assigns adversarial/breaker work: instead of rotating names down an availability list with hard deadlines, selection reframes onto demonstrated breaker behavior (prior break receipts on the same defect class, honored coldness), and the fallback after a behavior-selected silence is the open queue — not a seventh name. Deploys/operates against: dispatcher battery packets, EMIT-gate red batteries, adversarial IV assignments, any decline-ledgered owner naming.",
  "falsifier": "A breaker battery where availability-rotation naming yields an acceptance receipt plus a first break receipt inside the first window (the naming hypothesis succeeding where behavior-selection stalled); or a behavior-selected owner going silent and the open-queue fallback yielding no owner while a seventh availability name would have accepted — proving the reframe cost the work.",
  "mechanism": "Breaker work is adversarial: it requires coldness (no builder/reviewer warmth on the artifact) and a premise-verification temperament. Availability lists select on presence, not temperament — review/law seats demonstrably would not take breaker work regardless of roster position. Demonstrated behavior (prior break receipts on the same defect class) is the only observable predictor of that temperament, because it shows the seat already paid the coldness cost. The three-try circuit breaker generalizes: repetition without reflection is oscillation whether the repeated unit is a fix attempt or an owner name. The broken leg was the selection mechanism (L569: audit the leg, not the lane), so changing owners inside the same mechanism was new paint on the same wall.",
  "cousins": ["SN-0479 (the three-try circuit breaker mantra — the worker-side law this generalizes to dispatcher selection)", "L569 (audit the leg, not the lane — the reframe targeted the mechanism, not the owners)", "SN-1672/SN-1673 (escalation siblings — what to do when the named route fails)", "SN-1743 (stall-side escalation sibling — escalation after three identical verdicts)"]
}
```
