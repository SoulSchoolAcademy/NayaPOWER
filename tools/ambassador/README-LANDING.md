# Affiliate system — landing package (Nitro, interface end)
## What this is
The ambassador system embedded in the existing system, by addition, not a new system.
Dashboard stays the dashboard. My Smart Link stays. This adds, beside it:
- ambassador row (link, clicks, signups, sales, Wednesday share, display-only until payout terms confirmed in the open)
- plus-button share (Facebook, text, email, copy) + Ask Naya post prompt
- leaderboard (alias only, honest empty state)
- improved graphs: one derivation feeding wall header, Reports, mix, Today, 14-day trend, streak, plus ambassador series — four renderings cannot drift
- Welcome end slide, verbatim, rendered from the completion response
- Checkout page, new (the one page that did not exist), test mode until merchant keys land
- Issuer fix: encodeURIComponent(alias) in the walk worker JOINING block

## Files
- dashboard_embed.html + dashboard_embed.js — place beside My Smart Link
- leaderboard.py + graphs.py — derivations, tests in test_affiliate_build.py (5/5)
- welcome_end_slide.html — final slide, from /api/welcome/complete ambassador_link
- checkout.html + checkout_config.json — pricing configurable, status PENDING_OPEN_CONFIRMATION
- issuer_fix.js — the encoding fix, idempotent by primary key

## What is NOT in this build, on purpose
- No real payment taken. Stripe/PayPal connect through Shawn's secure tap only.
- No payout run. Wednesday share is display-only until payout terms + pricing are confirmed in the open (board or repo).
- No privacy claim for mail. RLS repair + re-proof still required before any such claim.
- No live deploy by this package. Landing to nayanet.live is Nitro's worker step + Shawn's deploy greenlight + a different seat's live scorecard at the final head.
