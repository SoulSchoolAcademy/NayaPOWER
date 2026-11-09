# PayPal Can Do Almost All of It — the Feasibility Verdicts

SN-2402 · PRICING / PAYPAL

**Created:** 2026-11-08 23:51Z

**Source:** PayPal feasibility research seat (393b0c4f, RESEARCH ONLY, completed 23:50:59Z), against Shawn's exact rules from SN-2400 (23:46Z). Source: PayPal's own current docs, read 23:49–23:51Z. Presented to Shawn in chat the same pass. Verdict per rule, with citations in the seat's report.

## Hook

PayPal can do almost all of it — but not quite as described. Three pieces are native, three are not.

## Nutshell

**Yes, native — no work needed:** (1) Nine days free, charge day ten — PayPal subscriptions have a trial cycle built in, 9 days at $0, then the regular charge; Max Yearly is already proven this way in Shawn's own account. (2) Cancel forward — cancelling stops future charges and does not refund the period already paid; exactly his rule. (3) Switch levels from the next period — PayPal's revise does that, new price next cycle, no proration; but the subscriber must log into PayPal and approve the change every single time (not a silent one-click switch in Settings), and all nine plans must sit under one product in his PayPal account for the switch to work at all — that second one still needs checking. **No, not native:** (4) Per-day adjustment — PayPal says plainly proration isn't automatically supported; next-period switching is the clean path, per-day is manual work we would have to build, with our own math. (5) Automatic 50% the second money lands — there is no PayPal switch that splits a payment at capture; chained payments are retired, and the marketplace split doesn't fit subscriptions (settles once a day to a bank, not instantly). The way it actually works: payment lands, PayPal tells our system, our code sends the 50% through PayPal's Payouts service — usually minutes, sometimes up to 24 hours, 32 cents a payout in CAD; needs PayPal's approval first, and only pays out of money actually sitting in the balance. (6) No refunds as an absolute — our policy can be strict, but it binds us, not PayPal or the banks: a buyer can still open a PayPal dispute or a card chargeback and get money forced back, plus a $20 fee. Honest wording: we never refund voluntarily — nine days free is the guarantee, and our only fix for our own mistakes is a free period, never cash. PayPal or a bank can still force one, and we can't switch that off. **The one that could bite early:** brand-new PayPal accounts have money held for up to 21 days (7 if we mark the order complete). While that hold is on, the money isn't in the balance to pay the 50% out of — so the very first payouts can lag behind the payment until that history is built, no matter how fast our code is.

## Human

The research seat's verdict, in its words: PayPal can do almost all of it, but not quite as you described it. The trial, the cancel-forward, and the next-period switch are native. The per-day adjustment, the instant automatic 50%, and the absolute no-refunds are not — they need our own code, our own wording, or both. And the early risk is not the code at all: it is the new-seller hold, up to 21 days, which can keep the very first payouts waiting even when everything else works.

## Child

Imagine a vending machine that can do most of what you ask: it can wait nine days before taking your coins, it can stop taking coins when you say stop, and it can change what it sells next month. But it cannot split one coin in half the second it drops in — a helper has to come and hand half over afterwards — and it cannot promise nobody will ever shake the machine and get coins back. And when the machine is brand new, the shopkeeper holds its coins for three weeks first.

## Grandma

PayPal will do most of it for you, dear — the nine free days, the stopping when you cancel, the changing levels next month — all built in. But three things it will not do on its own: it will not slice a payment in two the moment it lands — our own hands have to send the half over, which takes minutes, sometimes a day; it will not stop a bank from forcing money back if a buyer complains, no matter how strict our promise; and when the account is brand new, it holds the money for up to three weeks before we can pay anyone out of it. So the promise stays honest, dear: we never give money back ourselves — the nine days are the guarantee.

## Naya

The feasibility check draws the honest line between our law and PayPal's machinery. Our law (SN-2400) stands as written — trial, cancel-forward, next-period switch, recurring 50%, no refunds — and PayPal's native shape supports the first three exactly. The other three are where the system must be built or the copy must be honest: the 50% needs a webhook + Payouts job we build (minutes, not instant; approval needed; balance-funded); per-day adjustment is manual math, so next-period is the clean path; and no-refunds is our promise, not PayPal's — disputes and chargebacks can still force money back, so the board copy must say "we never refund voluntarily," never "no refund is possible." The new-seller hold is the earliest real risk to "pay immediately": the first payouts can lag up to 21 days until the account's history is built.

## What it means

- **Trial (9 days free, charge day 10): POSSIBLE AS-IS** — trial cycle $0 × 9 days, then regular; Max Yearly already proven in his account. Other eight plans' trials not individually seen.
- **Level switch next period: POSSIBLE AS-IS via revise** — BUT subscriber must re-consent in PayPal each switch, and all nine plans must share one Catalog Product (unchecked).
- **Per-day / mid-period adjustment: NOT POSSIBLE natively** — proration isn't automatically supported; manual only.
- **Cancel forward: POSSIBLE AS-IS on money** — cancel stops future charges, no auto-refund; keeping access until period end is OUR system logic, not PayPal's; buyer can also cancel inside PayPal without touching our Settings.
- **Automatic 50% payout on receipt: NOT POSSIBLE natively** — no split at capture, Adaptive retired, Commerce Platform partner fees don't fit subscriptions (daily bank settlement, not instant). POSSIBLE WITH webhook → our code → Payouts API (minutes, usually up to 24h; $0.32 CAD per payout; needs Payouts approval; funded from PayPal balance only).
- **Strict no refunds: NOT POSSIBLE as an absolute** — our policy binds us, not PayPal/card networks; buyer disputes (180d INR / 30d SNAD) and card chargebacks can force money back + $20 fees. Honest wording: we never refund voluntarily; PayPal/bank can still force one; our only fix for our own mistakes is a free period.
- **Limits:** new-seller holds up to 21 days (7 if order marked complete) are the real threat to instant payouts — payouts need available balance. Per-payout cap $20k.

## Why it matters

It keeps the hired-boards copy honest: every claim on the boards must survive PayPal's actual machinery, and three of Shawn's rules need our own build or careful wording rather than a PayPal switch. It also names the exact build owed (webhook → Payouts job) and the exact early risk (21-day holds) before anyone promises "the moment we're paid" as instant. The verdicts do not change his law — they change how the law is built and worded.

## What changes now

- **Three decisions owed to Shawn:** (a) 50% of gross charged or net after PayPal's 3.49% fee? (b) Are all nine plans under one Catalog Product? (c) Keep the Nov 6 daily payout cap ladder + fraud clawback, or does tonight's pay-immediately replace them (SN-2403)?
- The hired-boards replacement copy must carry the honest wording: "we never refund voluntarily" — never "no refund is possible"; "usually minutes" for the 50% — never "instant" as a PayPal guarantee.
- Build owed (not started): webhook → our code → Payouts API for the automatic 50%; Payouts approval to seek; balance-funded only.
- The per-day adjustment is manual-only — next-period switching is the clean path; the "if the math works and PayPal allows it" clause in SN-2400 now has its answer on the PayPal side: it doesn't, natively.
