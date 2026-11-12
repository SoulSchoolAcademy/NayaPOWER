# PayPal Doesn't Know They Switched

SN-2361 · SYSTEM

**Created:** 2026-11-08 20:53Z
**Source:** Shawn's backend question, answered plainly in chat 2026-11-08 20:36Z (main chat seq 161263–161267). The answer given, in substance: when they pick a plan, that block is a Smart Link to ONE PayPal plan — PayPal sees a brand-new subscription and nothing more; PayPal does NOT know they switched (new subscription not linked to the old; old keeps charging unless cancelled). WE know via the Smart Link click (which plan chosen) + the return from PayPal — we do NOT see the payment itself, only click + return. Closers are later builds: PayPal webhooks (payment-proven, catches changes made inside PayPal, old subscription ending when new starts) + the Settings "change your level" button re-opening the chooser.

> His question, in substance: when someone changes their level, what does PayPal know — and what do we know? The answer: PayPal knows nothing about the switch. We know the click and the return. The payment itself, we never see.

## Hook

A switch is not a switch — not to PayPal. Tap Max while you're on Power and PayPal sees a brand-new subscription, unrelated to the old one, and the old one keeps charging until somebody cancels it. We see the click and the return. The payment itself, we never see.

## Nutshell

**HIS QUESTION 20:36Z:** when they pick a plan in the chooser, what happens on the backend — what does PayPal know, what do we know? **ANSWER GIVEN, plainly:** each block is a Smart Link to ONE PayPal plan. PayPal sees a brand-new subscription and nothing more. PayPal does NOT know they switched — the new subscription isn't linked to the old one, and the old one keeps charging unless it's cancelled. So someone going Power → Max by tapping the Max block ends up with TWO live subscriptions unless the old one is cancelled. **WHAT WE KNOW:** the Smart Link click (which plan was chosen) + the return from PayPal (they came back). **WHAT WE DON'T KNOW:** the payment itself — only click + return, never payment-proven. **CLOSERS, LATER BUILDS:** PayPal webhooks — payment-proven, catches changes made inside PayPal, old subscription ending when new starts — plus the Settings "change your level" button re-opening the chooser. **RELATED:** SN-2339 (PayPal IS the Billing System) — the plan picked IS the charge, we build only the chooser; this note is the sharp edge of that law — the chooser's simplicity has a cost, and the cost is switch-blindness. **STATUS:** the answer was given in chat 20:36Z; the webhooks + Settings change-level button are later builds, not dispatched.

## Human

The nine-block chooser is beautifully simple — one button, one template, nine cubes, tap one and you're in PayPal — and the simplicity hides a seam. PayPal's subscription model has no "switch plan" inside a single subscription: each PayPal plan link starts a NEW subscription. So the person who joined on Power and later taps Max has not switched. They have subscribed twice. The old Power subscription keeps charging, month after month, until somebody cancels it — and PayPal will never tell us, because as far as PayPal is concerned there are simply two customers who happen to be the same human. That is a real risk to a real person: double-charged, and the second charge looks like our fault even though it happened inside PayPal's rules. What we can see is narrower than it feels: the Smart Link click tells us which plan they chose, and the PayPal auto-return tells us they came back — but the dashboard must mark it "returned from PayPal," never payment-proven (the 2026-11-05 payments ruling). The honest boundary is the product: we see the intention and the return, not the money. The closers exist and are named — webhooks make the payment visible and catch changes made inside PayPal, including the old subscription ending when the new one starts, and the Settings "change your level" button gives the person one place to change instead of nine places to re-subscribe. They are later builds, deliberately, so the landing ships first — but they are owed, and this note is the receipt for that debt.

## Child

Imagine you have a ticket to ride the little train every month, and then you decide you want the big train instead. You buy a ticket for the big train — but nobody takes away your little-train ticket! So now you are paying for two trains, and nobody tells you. The people who sell the tickets don't know you switched trains — they just see a new person buying a big-train ticket. We can see which ticket you picked and that you came back, but we can't see the money itself. Later we will build a special bell that rings whenever money really moves, so we always know — and a button in Settings that lets you change trains properly, in one place.

## Grandma

Dear, he asked a very good question: when someone changes from one plan to another, what does the payment system actually know? And the honest answer is: it doesn't know they changed at all. Each plan is a brand-new subscription in PayPal's eyes, so the old one keeps charging until someone cancels it — a person could end up paying twice without realising. We can see which plan they tapped and that they came back from PayPal, but we never see the payment itself — we only ever see the click and the return. So the page must never claim a payment is proven when it isn't. The proper fixes are coming later: a webhook that tells us when money really moves and when an old subscription ends, and one button in Settings to change your level in a single place. For now the landing ships with the truth told plainly, and this note is the record of what is owed.

## Naya

I never call a switch a switch — to PayPal it is a brand-new subscription, unlinked to the old, and the old keeps charging until cancelled. I never mark a sale payment-proven on a click and a return — the dashboard says "returned from PayPal" and nothing more, because the payment itself is invisible to us. I never hide the double-subscription risk — a person going Power → Max by tapping Max ends up with two live subscriptions, and that fact is told to him plainly, not buried. And I never let a later build stay unnamed — webhooks (payment-proven, catching changes inside PayPal) and the Settings "change your level" button are the closers, owed and named here.

## What it means

1. **A switch is a new subscription, not a switch:** PayPal sees a brand-new subscription; the old one is unlinked and keeps charging unless cancelled.
2. **Double-subscription risk is real:** Power → Max by tapping Max = two live subscriptions until the old is cancelled.
3. **We see click + return only:** the Smart Link click (which plan) + the PayPal auto-return — never the payment itself.
4. **"Returned from PayPal," never payment-proven:** the dashboard marks the return, not a payment (2026-11-05 payments ruling).
5. **Closers are later builds, named and owed:** PayPal webhooks (payment-proven, catches in-PayPal changes, old ends when new starts) + Settings "change your level" button re-opening the chooser.
6. **Related law:** SN-2339 — PayPal IS the billing system, we build only the chooser; this note is its sharp edge.

## Why it matters

SN-2339 made the architecture simple: no billing system to build. This note makes the simplicity honest: the thing we didn't build is the thing that would have known about the switch. Simplicity has a price, and the price here is paid by the citizen — double-charged, silently — unless the closers are built. Naming the debt in the same pass as the answer is the difference between a system that knows its own seam and a system that discovers it from an angry citizen. The webhook is not a feature to schedule someday; it is the proof that a sale happened, and a billing system that cannot prove a sale is a billing system in name only. Until it lands, every presentation of the chooser carries the honest boundary with it: click + return, never payment-proven.
