# 0031 — NEVER AGAIN: THE RESERVOIR LAWS (AI tongue)

Canonical design for preventing accumulation-without-completion in the NayaPOWER brain. Companion to 0030 (production standard); 0031 governs creation rights, reservoir surveillance, and escalation. Source event: 2026-10-20/21 reservoir night (662 open PRs → census → close wave 472 → purpose ledger: KEEP 60 / CLOSED 25 / PROVE-48h 105 → 165 open).

## L1 — Purpose card (pre-creation gate)
No PR / Smart Note / report artifact / build item is created without a purpose card in its body or filing record:
- `does`: one line — what the artifact does.
- `solves`: the CURRENT problem it solves (must name a live problem from the standing set or a dated, evidenced new one).
- `for`: who benefits (named human, lane, or system function).
- `finish_by`: a date.
- `success_measure`: the observable result that proves it worked.
Missing card = creation refused by lane discipline; reviewers reject cardless PRs at triage. (Mechanical enforcement candidate: PR-template + gate check for the five fields; until wired, the rule binds by protocol and triage review.)

## L2 — Creation budget (earned)
Per lane per rolling 7 days: `opens_allowed = finishes + 2`, where finishes = merges + purposeful closes (closes carrying a purpose-verdict reason). A lane at budget creates nothing until it finishes something. Exceptions only: correctives to live breakage, Shawn-directed items, Smart Note projections from spoken captures — each logged as an exception with its authorizer.

## L3 — Reservoir surveillance + ownership
- Metric: live open-PR count, sampled every 30 min by the director pass; printed nightly with trend (0030 print fields).
- Owner: the main seat, by name. The owner answers for the count.
- Bands: GREEN <50 · AMBER 50–100 (creation limited to repairs + Shawn-directed) · RED >100 (all lanes drain-only; creation freeze total except breakage correctives).
- Trend rule: 3 consecutive daily rises ⇒ owner executes a drain action within 24h and reports to Shawn AFTER acting (fix first, report solved).
- Current state at filing: 165 open = RED band. Freeze already in force (directive 6304093518 §1); lifts lane-by-lane only under 100 total AND lane WIP ≤5.

## L4 — Escalation ladder (Shawn's formulation, binding)
1. Find a problem → fix it → report to Shawn solved, with proof.
2. Cannot fix, or purpose unknown → ask the other seats (board, that day).
3. Team has no answer → remove the item (close/delete per its class; reversible closes preferred).
4. Shawn is asked ONLY at genuine human gates (authority, security, credentials, money, irreversible, constitutional).
Silence about a known problem is a protocol violation independent of the problem's size. Reporting a number without acting on what it means is classified as silence.

## L5 — Finish-first / WIP
Max 5 open items per lane (0030 §4 restated as a creation precondition). A lane with any item past its `finish_by` date starts nothing new until that item is finished, re-dated with cause, or closed.

## L6 — Quality loop
Purpose-valid items scoring <9 iterate: scorecard → named gaps → fix → re-score. Resting state below 9 is prohibited; an item that cannot reach 9 after two honest iterations returns to L1 (purpose re-test) and usually closes.

## L7 — Whole-before-part check (the wisdom clause, operational form)
Before creating or expanding anything, the actor states (in the purpose card's `solves` line or the run's sign-in): the current whole-system snapshot relevant to the action (reservoir count band, the standing problem list) and why the action improves the WHOLE, not only the actor's lane. Lane-local benefit with system-level cost (accumulation, duplication, ceremony) fails this check.

## Enforcement + falsifiers
- Nightly print includes: open count + band, per-lane opens/finishes vs budget, cardless creations detected (target 0), items past finish_by (target 0).
- Falsifier for the regime: any week closing with open count higher than it opened while all lanes report compliance ⇒ the laws are theater; escalate to Shawn with the evidence.
- This filing travels by PR through the full merge bar. No direct writes.
