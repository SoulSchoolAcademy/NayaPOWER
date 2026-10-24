# The Ambassador System V1 — "You're hired. Here's your link."
**Naya Power (engine end) · 2026-10-24 · Shawn's design, stated in chat and built the same night.**

## The idea in one paragraph
The moment a citizen joins, they are an ambassador. **Their alias IS their affiliate link** — `nayanet.live/joinus?ref=<alias>` (the join door that already exists, carrying their name). The system tracks it end to end: clicks on the link, signups it causes, sales it earns. Everything surfaces in their dashboard, beside their Smart Link, with one-click Easy Share. No application, no waiting, no separate program to join later.

## What exists tonight (built, live in the database)
- `public.ambassador_links` — one row per citizen alias: the link, issued-at, status. **9 links issued** for every citizen on record (certificate registry + seat aliases): shawn, shawnv, shawnvibert, joseph, nitro, naya-power, naya4, welcomeright1, welcomeright2.
- `public.ambassador_events` — the ledger every number derives from: kind ∈ click / signup / sale / refund, alias, visitor_key, subject_ref (order or signup), amount_cents, currency, source (stripe / paypal / groovesell). Empty tonight — honestly: events begin when the click wiring lands; no history is invented.
- Dashboard derivations are queries, not new machinery: clicks = count(click), signups = count(signup), earned = sum(sale) − sum(refund), per alias.

## The attribution chain (how a click becomes credit)
1. **Click** — the citizen shares their link anywhere. The join door reads `?ref=<alias>`, logs a click event with a visitor_key (first-party cookie), and keeps the ref attached to the visit.
2. **Signup** — when that visitor activates, a signup event binds visitor_key → the new citizen. The ambassador sees "your link brought a citizen" before any money exists.
3. **Sale** — checkout carries the attribution: the order is stamped with the ambassador's alias (Stripe: `client_reference_id` / metadata; PayPal: `custom_id`). The payment provider then tells our server the sale completed — **a webhook**, a signed server-to-server message:
   - Stripe: `checkout.session.completed` / `payment_intent.succeeded` → read the alias from the metadata → write a sale event with amount + order id.
   - PayPal: `PAYMENT.CAPTURE.COMPLETED` (IPN/webhooks) → read `custom_id` → same sale event. PayPal checkout also supports **card payment without a PayPal account** (guest checkout), so buyers are never forced into an account.
   - Signature verification on every webhook; an unverified message writes nothing. Refunds arrive the same way and write a refund event — credit reverses in the open, in the same ledger.
   This is the whole "sales part": one endpoint, one lookup, one ledger write. Standard, well-trodden code — not the hard part of this system.

## Easy Share (the growth surface)
The link's home is the dashboard, beside the Smart Link, with the ambassador shortcut (tonight's placements). Share actions ride the same row: **Invite by email** (pre-made invite emails in the growth kit, their link auto-embedded), **share to socials** (their link attached to their posts), **copy link**. Sharing is one tap from the number that motivates it — the clicks count sits next to the share button on purpose.

## What is NOT code (the two human doors)
- **Merchant accounts** — Stripe/PayPal accounts and their keys are Shawn's business credentials: connected by him through the secure flow, never handled in chat. Money movement and payouts stay human-gated, always.
- **The click wiring on the live door** — the joinus redirector adding the click log + ref persistence is site-lane work (same family as the Smart Link route wiring, citizen finding F2). The registry and ledger are ready to receive it.

## Relationship to the GrooveSell ambassador
Unchanged tonight: the Human Maximus Codex ambassador link (getpaid.takeyourpowerback.xyz) credits through GrooveSell for GrooveSell products. The native system covers NayaNET/NayaPOWER's own offers as our checkout carries them. A citizen can hold both; the dashboard shows each in its place.
