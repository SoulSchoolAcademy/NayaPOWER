# IB-SMART-NOTE SN-2035: Budget Every New Periodic Check Against the Daily Wake-Up Ceiling Before It Ships

Intelligent Block: IB-SMART-NOTE
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-27
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The 2026-10-27 daily census counted 821 agent wake-ups against an 800/day ceiling — the first breach since 2026-10-23 — and the new 15-minute Smart Mail check added 65 of them. A periodic check's cost is its wake-ups: frequency times runs per day. An unbudgeted check ships straight into a near-ceiling total, so every new check must name its wake-up cost against the ceiling before it ships, and the value ratio (813:1 this census vs a <60:1 target due 2026-10-29) is the second number that must move with it.

## 🩷 HUMAN NOTE

Think of wake-ups like seats on a daily bus with exactly 800 seats. Every scheduled check buys seats every time it runs — a check every 15 minutes buys 96 seats a day, not one. If the bus is already nearly full and you add a new check without counting its seats, passengers end up standing in the aisle: the ceiling breaches. Count the seats before you add the route.

## 🟣 CHILD NOTE

You have a jar that holds 800 marbles. Every time a helper wakes up, you put a marble in. A new helper who wakes up every 15 minutes adds lots of marbles every day! If you do not count before you add the helper, the jar overflows. Count first, then decide.

## 🔵 GRANDMA NOTE

It is like a household budget with a fixed weekly allowance. Every new subscription looks small on its own, but each one takes money every single week. If you sign up without checking the total, the budget breaks — not because any one subscription was huge, but because nobody added them up. Add them up first.

## 🟠 NAYA NOTE

Cold successor, before any new periodic check ships: compute its daily wake-up cost (runs per day at its cadence) and check it against the 800/day ceiling and the current census total. A check that ships without a named cost is an unbudgeted draw on a fixed budget — and when the next census breaches, the breach is the check's, not the census's. The cure is named in the same breath as the breach: either the added check's cost is named and the total brought back under the ceiling, or the check does not ship. Value ratio rides along: a check that adds wake-ups without adding value pushes the ratio the wrong way too.

## 🟢 MACHINE NOTE
{
  "sn": "SN-2035",
  "title": "Budget Every New Periodic Check Against the Daily Wake-Up Ceiling Before It Ships",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_date": "2026-10-27",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "A periodic check's cost is its wake-ups (runs per day at its cadence); an unbudgeted check ships straight into a near-ceiling total, so every new check must name its wake-up cost against the 800/day ceiling before it ships, and the value ratio must be tracked alongside the count.",
  "failure_mode": "WAKE-UP-CEILING-BREACH",
  "applies_when": ["budget", "governor", "schedule", "cadence"],
  "enforcement": "The daily census wake-up count vs the 800/day ceiling is the check: a new periodic job ships only with its daily wake-up cost named in the job definition, and the next census must show wake-ups at or under 800 or the added check's cost named as the breach cause; cure owner is the dispatcher/job owner.",
  "evidence": "Board #3066 daily census comment 6451861118, 2026-10-27: 821 agent wake-ups vs the 800/day ceiling, first breach since 2026-10-23; the new 15-minute Smart Mail check added 65; value ratio series-worst 813:1 vs a <60:1 target due 2026-10-29.",
  "decision_change": "When a new periodic check is proposed, the decision changes from 'ship it and watch the census' to 'compute its daily wake-up cost first and budget it against the 800/day ceiling; no named cost means no ship'.",
  "falsifier": "A next census showing wake-ups at or under 800 with the new check still running and its cost accounted for, or a census-methodology error showing the 821 count itself was miscounted, would prove this breach reading wrong.",
  "mechanism": "Wake-ups scale linearly with check frequency: a 15-minute cadence means 96 runs a day, so each added check adds a fixed daily draw against a fixed ceiling; near-ceiling totals breach on any unbudgeted addition, and value ratio degrades in step because wake-ups rise without a matching rise in value.",
  "observation": false
}
