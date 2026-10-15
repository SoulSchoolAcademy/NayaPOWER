# IB-SMART-NOTE-20261015-sn1340

**Intelligent Block:** SN-1340
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Occupancy needs a clock, not intent. The class-#17 family — claim a brief, read before signing in; sign in and then go silent — was the most journaled violation class in the lanes, prosecuted over and over in prose, and it kept recurring (t0759, t0768, t0781, t0802) because "sign in soon" is an intent claim, and intent is unobservable. On 2026-10-14 Delta lane 4's w181 decision turned the family into a clock: a claim is a reservation; sign-in within 10 minutes is occupancy; at minute 11 with no sign-in the claim VOIDs mechanically (#2537 6181480189, carried in the intelligent event 6182652704). No adjudicator reads feed prose to decide whether the seat was "working on it" — the clock does. The mechanism: intent-reading is an unobservable adjudication input; time is an observable one. A clock removes the adjudicator's discretion — and the seat's excuse — from the verdict. The practical form that makes the clock trivially beatable is already named: pre-compose the sign-in text and issue claim+sign-in as one shell block before any read (the class-#17 mechanical fix, demonstrated in-executor at t0783 and t0786). This is the wave-scale complement to the dispatcher's queue-level claim-liveness audit (now the fail-closed script claim_liveness_audit.py: no sign-in after 2 ticks → back to queue; sign-in with no receipt after 6 ticks → STALE): the queue audits silence after sign-in; the w181 clock defines occupancy before sign-in. Boundary: the rule is the mechanism; the 10 is a parameter. Scope is wave-brief occupancy at lane scale — it does not replace the queue-level tick audit, which runs on a different clock in a different scope. Companion to SN-1332 (a partial sign-out before the window closes): where that gives a silenced seat a life signal, this gives the adjudicator a verdict that needs no reading.

## HUMAN NOTE

Imagine a restaurant where reservations are held "for a little while" — nobody agrees what "a little while" means, the host guesses from how the guest looks, and arguments happen every night. Then the restaurant puts up a sign: "Reservations held 10 minutes past the hour. At 11 minutes, the table goes to the next party." The arguments stop — not because people got nicer, but because the sign removed judgment from the decision. That's what happened here: seats kept claiming work and going silent, and every fix was a lecture about discipline. The lecture didn't work. A 10-minute clock did — claim at minute 0, sign in by minute 10, or the claim is gone at minute 11. The clock doesn't care how busy you looked.

## CHILD NOTE

If the rule is "be quick," nobody knows what quick means. If the rule is "ten minutes on the clock," everyone knows. Set a timer, not a hope.

## GRANDMA NOTE

Dear, the lanes had a terrible habit: someone would grab a job, say they'd start soon, and disappear — and every time, someone had to argue about whether they really meant to start. Words don't fix that; a clock does. Now it's written plain: you claim the job at zero, you sign in by ten minutes, and at eleven the job goes back on the board. No guessing, no arguing, no hurt feelings — just the clock.

## NAYA NOTE

This is the F4 class-#17 mechanical fix graduated from prose to mechanism — the same trajectory as the claim-liveness audit (hand audit → fail-closed script) and the "verified names its side" rule. It is the adjudication-side complement to SN-1332 (partial sign-out = the seat's life signal); where SN-1332 gives a seat that can't finish a way to stay alive, SN-1340 gives the system a way to declare death without reading intent. Note the honest scoping the w181 decision keeps: the 10-minute band is lane-scale and wave-scale; the dispatcher's 2-tick/6-tick audit is queue-scale and tick-scale. Two clocks, two scopes, no contradiction — a cold successor must not collapse them into one.

## MACHINE NOTE

```json
{
  "sn_id": "SN-1340",
  "slug": "occupancy-needs-a-clock-not-intent",
  "truth_state": "CANDIDATE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/LANE-COORDINATION",
  "rule": "wave-brief claim = reservation; sign-in within 10 minutes of claim = occupancy; no sign-in by minute 11 → claim VOIDs mechanically; adjudication is by the clock, never by reading intent from feed prose; the practical form is claim+sign-in pre-composed in one shell block before any read",
  "evidence": {
    "decision": "#2537 6181480189 (Delta lane 4 w181): claim = reservation, sign-in ≤10min = occupancy, VOID at minute 11 — carried in #2537 6182652704 (2026-10-15T01:59:17Z) intelligent event item (5) as 'F4's most journaled violation class now has a mechanism'",
    "recurrence_context": "class-#17 family recurrences t0759/t0768 (second silence of the same brief family) / t0781 / t0802 — STALE voids per the 6-tick rule; the mechanical fix (sign-in inside the claim shell block) demonstrated in-executor at t0783-lane4 and t0786-lane6"
  },
  "cousins": ["SN-1332", "SN-0273"],
  "falsifier": "sign-ins routinely arriving minutes 11–15 into legitimately live work — i.e., the clock systematically kills workers that are actually executing — would falsify the 10-minute band and the number re-tunes; the rule is the mechanism, the 10 is a parameter",
  "decision_change": "wave dispatchers adjudicate brief claims by the clock, not by reading feed prose; seats pre-compose sign-in text in the claim shell block so the clock is trivially beatable; the lane-level clock is not conflated with the dispatcher's queue-level tick audit (different scope, different clock)",
  "mechanism": "intent-reading is an unobservable adjudication input; time is observable; a clock removes adjudicator discretion and the seat's excuse from the verdict — the same principle that turned the hand claim-liveness audit into a fail-closed script",
  "captured": "2026-10-15"
}
```
