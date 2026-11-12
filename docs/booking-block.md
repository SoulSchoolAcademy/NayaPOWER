# The Booking block — contract (Best-of-Best element #17)

Migration: `supabase/migrations/20261022210000_booking_v1.sql`
Module: `HUB/booking/` (`booking-core.mjs`, `booking-store.mjs`, `index.html`)
Tests: `tests/booking_block.test.mjs`, `tests/test_booking_contract.py`

## Objects

**booking_pages** — a named booking page. `slug` follows the Smart Links
name grammar (`^[a-z0-9][a-z0-9-]{1,62}$`, globally unique,
case-insensitive). `duration_minutes` is the one booking length the page
offers. `calendar_sync_state` is the element-#21 placeholder and ships
`'not_connected'`; nothing in this block performs or claims a sync.

**booking_availability** — the owner's windows: `weekday` (0 = Sunday,
the Postgres `extract(dow)` convention), `start_time`/`end_time` local
to `timezone`, per page. Set once; read publicly only through the RPC.

**bookings** — one row per booking. `owner_alias`/`owner_id` are filled
from the page by trigger, never trusted from the payload. Visitor email
is hash-only (`visitor_email_hash`, the invites pattern) and may be
null. `cancel_token` is the visitor's whole cancellation credential.

## The slot rules (enforced twice, identically)

1. **Trigger** (`bookings_guard_slot`, on insert and on time/status
   updates): a confirmed booking must fit inside ONE availability
   window on ONE local day (window's timezone) — else
   `booking_outside_availability` — and must not overlap another
   confirmed booking on the page — else `booking_slot_taken`.
2. **Partial unique index** (`bookings_one_confirmed_per_slot` on
   `(page_id, starts_at) where status = 'confirmed'`): the race-proof
   backstop for identical starts.

Cancelled rows are invisible to both guards: **cancelling frees the
slot**. Cancellation is the `cancel_booking(id, cancel_token)` RPC —
a wrong token flips nothing and reports `false`.

## Who may see what

- **Owner** (authenticated, `owner_id = auth.uid()`): full control of
  their pages, windows, and bookings.
- **Visitor** (anon): exactly the RPCs — `get_booking_page` (public
  shape), `get_booking_windows` (the offering), `get_booked_starts`
  (taken TIME RANGES only — never a name, a note, or a detail) — plus
  one guarded INSERT into `bookings` on an active page. There is no
  anon SELECT on any of the three tables: availability reads expose
  windows, never other bookings' details.

## Reminders (Smart Mail store, no external email)

At booking time `booking-store.writeReminders` shapes one
`smart_mail_threads` row (`thread_key = 'booking-<id>'`, in the page
owner's inbox) and one `smart_mail_messages` row per planned reminder:
owner new-booking at once, owner reminder a day ahead, visitor
reminder a day ahead. Only evidenced Smart Mail columns are used. The
write needs the owner's session; without one the booking result
carries `reminders: 'deferred_no_session'` — deferred is reported,
never faked.

## Timeline contract

The migration replaces `person_timeline_events` (from
`20261022203000_person_timeline_v1`, whose branches are reproduced
verbatim) adding one branch: confirmed bookings as `event_kind =
'booking'`, `event_at = created_at`, `source_table = 'bookings'`,
`source_id = booking id`, keyed by
`resolve_person_key(owner_alias, visitor_name, visitor_email_hash)` —
the read model's own rule, so a booking lands on the visitor's
timeline as the same person their mail and invites resolve to. The
migration fails loud (`BOOKING_TIMELINE_DEPENDENCY_MISSING`) if the
read model has not applied first.
