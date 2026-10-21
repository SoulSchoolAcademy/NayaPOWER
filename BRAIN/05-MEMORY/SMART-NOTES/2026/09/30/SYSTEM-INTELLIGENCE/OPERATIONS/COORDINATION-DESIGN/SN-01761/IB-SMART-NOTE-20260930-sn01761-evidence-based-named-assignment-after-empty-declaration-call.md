# When the Capacity Declaration Call Closes Empty, Route by Demonstrated Evidence — and Name the Hardening Clock

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01761-evidence-based-named-assignment-after-empty-declaration-call
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

L593 (SN-1759) says: two unclaimed IV rounds escalate to a capacity finding — never a third blind re-route. On 2026-10-21 PR #2835 hit the L593 ladder's second step: the 11:00Z declaration call closed with zero seat declarations, so the capacity finding stood as evidence that the scorecard lane is capacity-empty *as a blind market*. The main seat did not blind re-route. It made an evidence-based named assignment to the VERIFY lane — the one lane with three byte-proven 9.5 IVs in-window (#2831 CURE VERIFIED 9.5, #2839 115/115 re-run 9.5, #2841 9.5) — with a claim-by clock of 12:00Z. If the clock expires unclaimed, the finding hardens to "scorecard lane empty today": the scorecard leg pauses until a lane shows evidence of capacity. The lesson: after a finding stands, route on demonstrated in-window evidence, never on availability lists; always name the clock at which the finding hardens.

## 🩷 HUMAN NOTE

Hey Shawn — guess what: the declaration call closed with nobody showing up. So instead of routing #2835's scorecard to another blind guess, I looked at the actual evidence: the VERIFY lane delivered three byte-proven 9.5 independent reviews in-window this morning — #2831's registry cure, #2839's re-run, #2841's fail-closed verdicts. That's the seat that showed it can do the work. So the assignment goes there, with a clock: claim by noon. If they can't claim it either, then the finding gets even sharper — the scorecard lane is genuinely empty today, and we pause that leg until someone shows they have capacity. The point: we pick who showed up in the evidence, not who might be free. And every assignment carries the exact moment it expires into a harder finding. That's the second step of the L593 ladder, and why.

## 🟣 CHILD NOTE

If you need someone to fix your bike and you ask the whole neighborhood and nobody answers, you don't shout again — you look at who actually fixed bikes this week and ask them directly, with a deadline. If they can't either, you stop asking and admit nobody can fix bikes today. That is what happened here: nobody answered the call, so we asked the team that already proved it today, and we wrote down the time when "nobody can" becomes official.

## 🔵 GRANDMA NOTE

We asked everyone who might be available to review an important change, and nobody volunteered. Instead of guessing who *might* be free, we looked at who *actually did* the same kind of careful review work this morning — three of them, all excellent — and asked that team directly, giving them a clear deadline. If they can't take it either, then we will honestly say the review lane is empty for today and stop pretending otherwise. We choose by what people have proven, not by what we hope.

## 🟠 NAYA NOTE

For every Naya on an IV-routing leg: when an L593 capacity finding stands and the declaration call closes with zero declarations, do NOT fire another blind re-route and do NOT poll availability lists. Instead: (1) scan the current window for byte-proven evidence of the required behavior (scorecard-grade independent reviews with own evidence artifacts, on-time); (2) name the assignment to the seat/lane that demonstrated it, with a claim-by clock; (3) name the hardening outcome in the assignment itself: clock expiry without a claim hardens the finding to "lane empty today" and the leg PAUSES until a lane shows evidence of capacity. The merge path resumes the moment a lane shows up with evidence. An evidence-free re-route after a standing capacity finding is void — it is exactly the third blind re-route SN-1759 forbids, wearing a different name.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn01761-evidence-based-named-assignment-after-empty-declaration-call",
  "title": "When the capacity declaration call closes empty, route by demonstrated evidence — and name the hardening clock",
  "lesson": "L593 (SN-1759: two unclaimed IV rounds escalate to a capacity finding, never a third blind re-route) has a second step. When the declaration call closes with zero declarations, the capacity finding stands as evidence that the lane is capacity-empty as a blind market. The main seat then assigns by demonstrated in-window evidence of the required behavior — not by availability lists — with a named claim-by clock, and names the hardening: clock expiry unclaimed hardens the finding to 'lane empty today' and the leg pauses until a lane shows evidence of capacity. 2026-10-21: PR #2835 L593 second step — 11:00Z declaration call closed with zero declarations -> evidence-based named assignment to the VERIFY lane (three byte-proven 9.5 IVs in-window: #2831 CURE VERIFIED 9.5 6310156804, #2839 115/115 re-run CURE VERIFIED 9.5 6312255918, #2841 IV 9.5 6313317039), claim-by 12:00Z; expiry unclaimed -> finding hardens, scorecard leg pauses until evidence of capacity appears.",
  "applies_when": [["coordination", "iv-routing"], ["capacity", "finding"]],
  "enforcement": "Any IV tag past the declaration-call-empty stage must carry an evidence citation (byte-proven in-window demonstrations of the required behavior) and a named hardening clock (claim-by time; expiry unclaimed hardens the finding to 'lane empty today' and pauses the leg). An assignment without an evidence citation is void — it is a third blind re-route in disguise, which SN-1759 already forbids.",
  "evidence": ["#2793 comment 6314403976 (2026-10-21T11:06:01Z, main seat): '[IV ASSIGNMENT — PR #2835] Evidence-based named assignment: VERIFY lane, clock to 12:00Z' — 'the L593 ladder's second step: the declaration call (11:00Z) closed with zero seat declarations'; cites the three in-window 9.5 IVs", "live-plan.md DIRECTOR TICK 2026-10-21 04:08 PDT (11:08Z): #2835 L593 SECOND STEP — 11:00Z declaration call closed with zero seat declarations; main seat issued evidence-based named assignment to VERIFY lane (claim-by 12:00Z; evidence = three byte-proven 9.5 IVs in-window on #2831/#2839/#2841); 12:00Z expires unclaimed -> finding hardens to 'scorecard lane empty today,' scorecard leg pauses until a lane shows evidence of capacity", "precedent: SN-1759 (L593 [F2] — two unclaimed IV rounds escalate to a capacity finding, never a third blind re-route)"],
  "decision_change": "A main seat facing a standing capacity finding and an empty declaration call: instead of re-routing to 'first available' or named-but-evidence-free seats (the availability-list reflex), it assigns on demonstrated in-window evidence with a hardening clock. A cold successor inheriting this would otherwise burn another routing round on seats that already demonstrated silence.",
  "falsifiability": "Falsified if a seat with NO in-window evidence claims and delivers the #2835 scorecard before VERIFY's 12:00Z clock — then availability beat evidence and the selection criterion was wrong. Corroborated the other way: VERIFY misses 12:00Z -> the finding hardens and the leg pauses, proving the hardening clock was load-bearing.",
  "mechanism": "Selecting on demonstrated behavior (the L569 reframe: audit the leg, not the lane — pick the seat that already showed the required temperament in-window) rather than on stated availability. Availability lists name who might act; in-window evidence names who already acted. After two silent rounds, the base rate of a third blind route succeeding is measured at zero — the mechanism switches from polling capacity to recognizing it.",
  "captured_date": "2026-10-21",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/OPERATIONS/COORDINATION-DESIGN"
}
```
