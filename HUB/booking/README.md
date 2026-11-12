# HUB/booking — the Booking block (Best-of-Best element #17)

"Your booking link lives on your app; someone picks a time, both sides
get reminded, and the booking lands on the person's timeline."

## Pieces

| File | What it is |
|---|---|
| `booking-core.mjs` | Pure logic: page/window validation, the slot rules, reminder planning, Smart Mail row shaping, plug-in states. Unit-tested (`tests/booking_block.test.mjs`). |
| `booking-store.mjs` | REST transport. Public reads only via the migration's RPCs (anon key); owner operations and reminder writes require a session and refuse visibly without one. |
| `index.html` | The booking page: one decision per step — day → time → who → confirm. Reads `?book=<slug>`; wired by `window.NayaBookingConfig { supabaseUrl, anonKey, getAccessToken }`. Without config it shows an honest not-wired state and invents nothing. |

Data: `supabase/migrations/20261022210000_booking_v1.sql`
(`booking_pages`, `booking_availability`, `bookings`, the slot guard,
the public RPCs, and the timeline view extension). Contract:
`docs/booking-block.md`.

## The six features (map Part 5, row 17)

- **availability** — owner windows (weekday + local range + timezone), set once.
- **booking link** — the page's slug, Smart Links name grammar, owner-scoped.
  The public surface is this page (`?book=<slug>`); the `nayanet.live/<name>`
  redirect worker is element #3's and ships gated — this block never
  depends on it.
- **conversational intake** — the flow is one decision per step, built
  conversational-ready; the conversational engine itself is the sibling
  intake build (map step 12), not this block.
- **reminders** — at booking time the module writes one Smart Mail thread
  per booking with reminders for BOTH sides (owner at once + a day
  ahead; visitor a day ahead). No external email exists or is claimed.
  Without a session the write defers and the result says so.
- **timeline write** — the migration extends `person_timeline_events`
  with a bookings branch in the one event shape, keyed by the read
  model's own resolution rule.
- **calendar sync** — NOT built. Element #21's first plug-in source.
  `booking_pages.calendar_sync_state` ships `'not_connected'` and the
  page prints exactly that.

## Gates

- The migration registers PENDING in the production ledger and applies
  only at the human gate, like every Phase-0 migration.
- Until it applies, the page's RPCs do not exist and the page shows its
  honest unavailable state — by design, not by accident.
