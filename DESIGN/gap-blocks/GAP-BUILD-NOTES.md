# GAP-BUILD-NOTES.md — calendar + checkout block families

Built 2026-10-16 by Team Nitro BUILD seat (Nu), two block builders, on Shawn's "Do it!"
Outputs: `calendar-blocks.md` + `checkout-blocks.md` (specs), `gap-blocks-index.json`
(10 NEW entries, CAL-001…CAL-005 + PAY-001…PAY-005 — merge fragment for BLOCK-INDEX.json).

## Design decisions

### Shared
- **Black ground, white-lit edges, no flat, no dead** — every block rests on #050507 with 1.5px+ visible edges; every interactive element lifts and ignites on hover. Zero yellow anywhere (verified by grep).
- **Chrome vs themed color:** chrome (buttons, chevrons, pickers, retry) ignites purple; themed elements (event pills, spines, cards, totals) ignite their own spectrum color. Color rests dark, ignites on touch.
- **Serif voice** (Georgia) for headers, totals, and the paid-amount hologram.

### Calendar family
- **Spectrum mapping fixed by meaning:** magenta = celebrations, purple = deep work, blue = meetings, green = health, gold = decisions/deadlines; 6th/7th types continue the wheel (orange, red), never restart it. Pills and dots walk the order within a day cell — never adjacent duplicates.
- **Today:** gold 2px edge + gold glow + slow 4s breathe. Today outranks selected, always. Gold's second use (the agenda now-line) is the same meaning — "attention, earned" — not a reuse.
- **Honest uncertainty:** tentative events get a dashed edge; the picker carries a timezone-honesty footnote; the agenda never invents events. Empty state: "Nothing scheduled — the day is yours." — emptiness gets dignity.
- **CAL-005 day-cell state system** exists so CAL-001 and CAL-003 can never drift: seven states with a written precedence order.

### Checkout family
- **Privacy boundary (spec, not guidance):** card data lives ONLY in input fields bound for the payment backend. The blocks NEVER render a card number back as text, NEVER log card fields anywhere, and the display layer shows at most last-4 + brand. A build that echoes a PAN violates the block.
- **Error tone:** red = urgency, not alarm — 45%-strength edge breathing on a 6s calm loop. Load-bearing sentence is "no money moved," rendered only when the backend confirms it; on unknown charge state the panel says so and offers "Check status" instead of "Try again." Never blames: "That number looks short," never "Invalid input."
- **Confirmation restraint:** exactly one ignition on a confirmed processor response, then a slow breathe. No confetti. Truth-state discipline: receipt-email is ✓ only on mailer confirmation, ? while claimed; never claims success before the processor answers (Law 75).

## What's still missing for a shippable scheduling app
Interface: week-view grid, drag-to-reschedule, recurring-event editor (named as future CAL-006+ — not promised by these specs).
Backend (not blocks' job, but the app can't ship without): timezone resolution, reminders/notifications, calendar sync (Google/Apple), attendee invites + RSVP handling.

## What's still missing for a shippable commerce app
Interface: order tracking/shipment (fulfillment family, not checkout), saved-address block (identity family).
Backend: payment processor integration (Stripe or equivalent), tax/shipping calculation, refunds, inventory.
Deliberately not specced: 3-D Secure / challenge-flow interstitial (processor-owned surface); the processing spinner (a transient Pay-button disabled state in PAY-002 — a spinner that outlives the attempt is a lie).

## HIGH gaps still open (build order per BLOCK-GAPS.md)
1. Comment thread + reactions
2. Chat bubbles + conversation list
3. Onboarding stepper
4. Notification center (toast + status pill exist as parts)
5. General error state block
6. Form validation states (partially covered by PAY-002) + file upload
7. Auth companions — signup, password reset, SSO buttons

## What's next
1. Sibling coordinator adopts CATALOG-EXTENSION.md into DESIGN/BLOCKS.md via lane PR.
2. This `gap-blocks-index.json` merges into BLOCK-INDEX.json (181 → 191 entries) at adoption time.
3. HIGH gaps get built in the order above — comment thread first.
4. The two CRITICAL holes are now closed: no scheduling or commerce app is blocked on missing parts.
