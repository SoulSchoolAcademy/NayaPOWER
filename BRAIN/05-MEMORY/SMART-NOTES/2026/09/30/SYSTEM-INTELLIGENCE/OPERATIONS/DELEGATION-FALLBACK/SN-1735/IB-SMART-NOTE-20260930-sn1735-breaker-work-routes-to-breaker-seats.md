# Breaker Work Routes to Breaker Seats, Not Reviewer Seats

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1735-breaker-work-routes-to-breaker-seats
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When the director needed a fourth owner for the EMIT 5-vector adversarial battery, three review/law seats (Coda-1, Epsilon, Delta) went silently past their acceptance deadlines — and the seat that worked, Zeta, was chosen for demonstrated breaker behavior: premise-verification first, a re-fire watch discharged with evidence, a 9/10 gap-close packet. Route adversarial work to seats with adversarial receipts, not to seats whose posture is judgment.

## 🩷 HUMAN NOTE

Hey Shawn — quick discovery: when we needed someone to deliberately break the emit gate (find real holes), three reviewer seats quietly didn't pick it up. The one who got the job, Zeta, had already shown the breaker habit on another job — check the facts first, close the watch with proof, route by name. Lesson I'm filing: don't assign attack-work to judges; assign it to people who've shown they attack well. Same as real life — you don't hand the red pen to the proofreader and ask them to punch holes in the wall. That's what I decided and why: pick the seat whose receipts prove the posture the task needs.

## 🟣 CHILD NOTE

If you need someone to find the cracks in a wall, don't pick the person who grades walls — pick the person who has already found cracks. We learned this because three graders stayed silent and one crack-finder raised her hand.

## 🔵 GRANDMA NOTE

When a job needs someone to test whether something can be broken, you give it to the person who has already proven they test things hard — not to the people whose job is usually to approve. Three of the usual approvers quietly passed on the job; the tester got it done.

## 🟠 NAYA NOTE

For any breaker-class task (adversarial battery, red-team probe, falsification pass, sabotage battery), the dispatcher's owner-selection MUST cite at least one breaker-behavior receipt for the named seat (a gap-close packet with premise-verification plus a discharged watch, or a falsifier HIT on its own work). Review/law seats are not the default fallback for breaker work. If a named seat misses its acceptance deadline, the decline path fires and the next owner is selected by the same posture rule — never by "who's free."

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn1735-breaker-work-routes-to-breaker-seats",
  "title": "Breaker work routes to breaker seats, not reviewer seats",
  "lesson": "Owner selection for adversarial (breaker-class) tasks must match seat posture to task posture: three review/law seats went silently past acceptance deadlines for the EMIT 5-vector battery, while the selected fourth owner (Zeta) carried demonstrated breaker-behavior receipts (premise-verification first, re-fire watch discharged with evidence, 9/10 gap-close packet). Seat posture (reviewer = judge finished work; breaker = attack premises first) predicts acceptance better than availability.",
  "applies_when": [["dispatch", "owner-selection"], ["task", "breaker"]],
  "enforcement": "Dispatcher brief carries an OWNER-POSTURE CHECK for breaker-class tasks: the named seat must cite >=1 breaker-behavior receipt (gap-close packet with premise-verification + discharged watch, or falsifier HIT on own work). The director pass audits owner-selection decisions against this rule each tick and re-routes any breaker task assigned without the citation.",
  "evidence": ["shared-state.json:director_decision_emit_battery_fourth_owner_20261020 (2026-10-20T16:47:30Z)", "#2793 comment 6295785075 (Verity dispatcher: decline path fired - Delta silent past 16:00Z; third silence: Coda-1 13:00Z, Epsilon 13:45Z)", "#2793 comment 6293036880 (Zeta #2755 gap-close packet 9/10: premise-verification first, re-fire-watch discharged with evidence)"],
  "decision_change": "The next owner-selection for any adversarial task (red-team, sabotage battery, falsification pass): pick seats with demonstrated breaker-behavior receipts instead of review/law seats by default.",
  "falsifiability": "Zeta accepts the battery and delivers the first break receipt by the 17:15Z deadline -> corroborated. Zeta also goes silent or declines -> falsified: the selection rule fails and the real blocker is scope/incentive, not seat posture.",
  "mechanism": "Seat posture shapes behavior: reviewer/law seats optimize for verdict correctness on finished work (saying no is their product); breaker tasks require adversarial premise-first behavior (attack the premise before naming anything). Assigning attack-work to judge-seats creates a posture mismatch that resolves as silent decline.",
  "captured_date": "2026-10-20",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/OPERATIONS/DELEGATION-FALLBACK"
}
```
