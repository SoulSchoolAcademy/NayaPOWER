# Hired — Payout-Ladder Strip (F23, hired half)
**Filed:** 2026-11-07 (fix2). **Source:** harvested VERBATIM from the hired companion page `~/workspace/verify-pricing-v6/youre-hired-round7-work.html` lines 487, 496–500 (the payout ladder: "$100 → $200 → $300 → $400 → $500 → $1,000 a day" + "Month 1 you can be paid up to $100 a day. Then it grows — $200, $300, $400, $500, up to $1,000 a day at the top. The longer you're with us, and the more you do, the higher it goes. Amounts over $500 in a day pay the following day."). The companion page itself was NOT touched in fix1 or fix2 — it is the harvest source only.
**Where it goes:** the hired slide, below the job card — a `.hired-ladder` strip ("THE PAYOUT LADDER — PAID THE MOMENT WE'RE PAID", the six rungs with gold ◆ separators, the month-1 sentence). Gold lives on the ◆ separators, not in colored text (L5).

## Why it exists
The hired slide's bottom third was empty black at the locked stop (F23). The card already filled the width; the void beneath it needed the ladder — the one piece of hired content that was on the companion page and not yet on the pricing page. It closes the void (bottom void now 119px, 11%) and it is the payout ladder the job card's "50% / Same-day / Day 10" terms point at.

## Verification
Self-check `r7f2x-selfcheck.py` (run 2): ladder 11,583–11,760 (offset 782–959), hired slide scrollH 1,078 = fits at 1920; at 390 scrollH 1,946 (internal scroll). Screenshot viewed by eye: `r7f2x-1920-hired.png` (ladder clean under the card). 0 errors.
