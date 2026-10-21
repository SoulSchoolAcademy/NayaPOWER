# Two Unclaimed IV Rounds Escalate to a Capacity Finding — Never a Third Blind Re-Route

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01759-two-unclaimed-rounds-capacity-finding
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

PR #2835's IV assignment went unclaimed twice on 2026-10-21: first-available round (60 min, zero sign-ins), then a named round to Naya Judge (60 min, unclaimed). The temptation was a third blind re-route — re-rolling the same exhausted pool. L593 [F2] was promoted instead: an IV tag unclaimed through two routing rounds escalates as a capacity finding, never a third blind re-route. The main seat posted the lane-capacity finding (board 6313071517) and opened a capacity-declaration call (clock 11:00Z) — seats declare what they can actually cover, on the venue, with a claim-by time. Routing runs on declared capacity, not on hope.

## 🩷 HUMAN NOTE

Shawn — tonight a PR waited for a reviewer through two full assignment rounds and nobody picked it up. The easy move would have been to re-route a third time and hope. Instead the rule fired: two unclaimed rounds means the pool is empty, and re-routing blind just hides that fact. So we named it — a capacity finding — and asked every seat to declare, in the open, what they can actually cover and by when. No third blind roll. If the lanes are full, the honest answer is a verdict, not another roulette spin.

## 🟣 CHILD NOTE

Imagine you're picking teams and nobody raises their hand — twice. Spinning the bottle a third time and hoping someone picks differently doesn't work, because the same people are standing there. The smarter move: ask out loud, "who actually has time to play?" and let people raise their hands honestly. That's the rule: after two rounds with no takers, stop re-rolling and ask people to declare what they can do.

## 🔵 GRANDMA NOTE

Like calling a tradesman twice with no answer — you don't call a third time and hope; you admit the tradesman is busy and ask around the neighborhood for who's actually available. Today's finding was exactly that: two silent rounds on a review assignment proved the pool was dry. The declaration call is the neighborhood round — everybody says what they can take on and when. Honesty about capacity beats blind re-dialing, every time.

## 🟠 NAYA NOTE

Lane discipline: keep an unclaimed-round count per IV tag. Round 1 unclaimed → re-route once (first-available → named is the canonical two). Round 2 unclaimed → the router is BARRED from a third blind re-route. The move is a lane-capacity finding posted on the venue (6313071517 for #2835) naming both rounds, their clocks, and the assignment state — followed by a capacity-declaration call with a named clock (11:00Z for #2835): any seat holding scorecard capacity declares the PR it can cover and a claim-by time. If the clock expires empty, the finding stands as capacity-empty evidence and routing returns to the main seat with evidence — not with another blind re-route (director sign-out 6313449753 modeled this: no director re-route, no third blind re-route). Blind re-routes re-sample the same exhausted pool and mask the real signal (nobody has capacity today); a capacity finding routes on truth.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1759",
  "title": "Two unclaimed IV rounds escalate to a capacity finding — never a third blind re-route",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "applies_when": [
    ["iv", "routing"],
    ["review", "capacity"],
    ["dispatcher", "assignment"],
    ["coordination", "unclaimed"]
  ],
  "enforcement": "The router keeps an unclaimed-round count per IV tag in shared-state; at two unclaimed rounds it is barred from a third blind re-route and must post a lane-capacity finding with a capacity-declaration call (named clock). The director tick verifies the count before any re-route fires. The named check is the 'two-round capacity gate': a re-route is valid only when unclaimed_rounds < 2.",
  "evidence": {
    "l593_promotion": "#2793 comment 6313423154 (2026-10-21): L593 [F2] PROMOTED — an IV tag unclaimed through two routing rounds escalates as a capacity finding, never a third blind re-route",
    "capacity_finding": "#2793 comment 6313071517 (2026-10-21): LANE-CAPACITY FINDING for PR #2835 — two unclaimed IV rounds (first-available 60 min + named-Judge 60 min); capacity declaration call opened, clock 11:00Z",
    "director_signout": "#2793 comment 6313449753 (2026-10-21, 10:12Z): #2835 named-Judge IV clock EXPIRED @09:45Z UNCLAIMED → L593 stands; NO director re-route (no third blind re-route); expires empty → capacity-empty evidence, routing to main seat"
  },
  "decision_change": "When an IV assignment goes unclaimed through two routing rounds, the router's next move is a capacity finding + declaration call, not another re-route. This changes merge-queue routing: stalled PRs get a capacity verdict on the venue, never an endless blind re-route loop.",
  "falsifier": "If a third blind re-route ever lands a claim that two rounds could not — with the same pool and no new capacity entering — the rule's premise fails. The law is falsified by a successful third blind re-route, not by a capacity declaration that succeeds (that is the law working).",
  "mechanism": "Blind re-routes re-sample the same exhausted capacity pool, so repeated rounds decay to noise and mask the real signal (nobody has capacity today). A capacity finding makes hidden capacity visible — seats declare what they can actually cover — which routes on truth instead of hope. The information gain of a declaration call is nonzero; the information gain of a third blind re-route is approximately zero.",
  "related": ["SN-1756 (same #2835-era adjudication discipline: void claims get names, capacity gets names too)", "L587 re-route rule (the two-round routing discipline L593 completes)"]
}
```
