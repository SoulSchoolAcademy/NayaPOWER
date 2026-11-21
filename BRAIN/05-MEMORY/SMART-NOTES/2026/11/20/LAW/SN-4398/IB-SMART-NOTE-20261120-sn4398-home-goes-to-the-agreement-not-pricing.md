# SN-4398 — Home Goes to the Agreement, Not Pricing

**Category:** LAW — where Home takes a citizen; 2026-11-20 ~18:50 MST

*Paired Naya Note: NN-20261120-home-goes-to-the-agreement-not-pricing — the verbatim record of the revised routing.*

**Filed:** SN-4398 — Intelligence Loop run 438, 2026-11-20. Home routing revised on call dfe2008f, recorded in the daily log 2026-11-20. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

Home takes a member straight into the Hub, auto logged in — and a non-member to the collective agreement, not to pricing.

## The Lesson

Home (top icons on the Naya app): a member clicks it and goes straight back into the Hub, auto logged in. Not a member — the collective agreement page (nayanet.app/agreement), and they go through that. This SUPERSEDES his 2026-11-14 rule (member → Hub, non-member → pricing page). The member half is unchanged; the non-member destination is now the agreement, not pricing. The One List item home-membership-routing was already queued from Nov 14 — update it to the agreement destination. The hard part stands: the system has to know whether they are a member. Not built yet; queued as its own piece behind the AI Score / Academy icon fixes (coordinator abc3e850, running). No Home href was found in the staged Dashboard file (no data-right="home", no ">Home<") — the Home control lives elsewhere (Hub plus-menu has a Home item); the routing piece must find its real home first.

## Why It Matters

The agreement is the front door — it is the governance for all our pages, available in system settings and on all our pages. A non-member meets what we stand for before they meet a price. Pricing first asks them to pay before they know what they are joining; the agreement first shows them what they are joining, and the join follows. The routing only works if the system knows membership — that check is the piece that has to be built, and it is queued, not assumed.

## How to Use It

When routing a citizen, ask membership first, then destination: member → Hub, auto logged in; non-member → the agreement. Never send a non-member to pricing as the first step. When a rule is superseded, name the old rule, the date it was set, and what changed — the old destination must not survive in a queued item or a stale brief.

## His Order, As Recorded

> "Home (top icons on the Naya app): member clicks it → straight back into the Hub, auto logged in. Not a member → the collective agreement page (nayanet.app/agreement), and they go through that."

## Owed from This Dictation

- One List item home-membership-routing: update the non-member destination from pricing to the agreement.
- The membership check itself (does the system know they are a member?) — queued behind the AI Score / Academy icon fixes, coordinator abc3e850.
- The routing piece must find the real Home control first (Hub plus-menu has a Home item; staged Dashboard has no Home href).
