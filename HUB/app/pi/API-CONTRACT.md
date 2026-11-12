# PI face data contract — what the face fetches, exactly (Nitro → Power, 2026-10-26, face v3)

The face (HUB/app/pi/index.html, branch face-v2-shared-20261026) fetches ONE URL,
same-origin, fresh on every load and on Refresh:

    GET /pi/api/items   (Cache-Control: no-store)

Today that URL returns the Hub home HTML (SPA-masked) — the endpoint does not
exist live yet. That is Power's blocker A11/B1, and this file is everything
Power needs to build it: the exact shape the face already renders from.

## 1. Rows projection (the core — A11/B1)

The face renders rows, not aggregates alone. Serve item rows as:

    {
      "items": [
        {
          "item_key": "director-one-ultimate-app-consolidation-20261026",
          "title": "One ultimate app, not three copies",
          "state": "in_progress",
          "owner_seat": "naya-power",
          "next_action": "Wire the publisher to one true source.",
          "area": "projects"
        }
      ]
    }

Field meanings, plainly:
- item_key — the stable key (work_items.item_key / project_intel_items key). Rows are
  matched by this key only; never by title.
- title — the item's plain-words title, never empty.
- state — one of: waiting, in_progress, verifying, done_proven, blocked,
  needs_shawn. These six are the only states the face counts.
- owner_seat — the owning seat, or null when no owner is named. Null renders as
  ownerless (honest), never as a guessed owner.
- next_action — the next step in plain words, or "" when none is named.
- area — the area the item belongs to (one of the twelve rooms' keys, or
  "uncategorized" when unplaced). Per-area counts and percents come from this
  field alone — that is B4, and it waits on the one-pass application, not on
  a new count typed anywhere.

States the face already counts from aggregates (keep them, in the same response):
real {done_proven, total, queued, in_progress, verifying, needs_shawn, blocked},
rows {done_proven, total}, main_bucket {done_proven, total, needs_shawn}.
Aggregates must be COMPUTED from the rows in the same response, never typed.

## 2. Lists the face already renders (keep their shapes)

- master_todo: [{name, why, unblocks, source}] — priority order, computed from
  the record (B2: never hand-kept).
- named_blockers: [{name, why, owner}] — the weakest point and the
  top-priorities-with-owners come from here (A9/B2). Owner null renders dark.
- movement: [{text, item, from, to, actor, time}] — text is what renders today;
  item / from / to / actor / time are the distinct fields B3 asks for. Serve
  all six; the face renders text now and the distinct fields when its
  movement strip is next touched (no fake fields in the meantime).
- rooms: [{key, name, accent, why, seat, gates, workstreams[]}] — twelve rooms.
  accent is the room's spectrum colour key (purple/blue/green/shown/orange/red/
  magenta/teal/indigo/lime). Seat is proposed, never confirmed, until a seat
  confirms it.
- owners: {ownerless_real} — count of real jobs with no owner named.
- ledger: {tail_seq} — the ledger tail sequence, or null when frozen/unknown.

## 3. Human / seat / machine tongues (B5)

Per entry, serve three tongues where they exist, and omit them where they do
not (omission renders dark, never guessed):
- human: plain-words sentence.
- ai: the seat-view method sentence (how the number was derived).
- machine: identifiers and links (item_key, source rows, proof links).
The face's seat view today renders its method paragraph from the aggregate
method text; per-item tongues behind the item door are the v4 step (A2/C9).

## 4. Parts register (B17/B18)

The register lives beside this contract: HUB/app/pi/parts-register.json.
It lists every face part with owner, last touch, movement, and percent.
Percent is "not measured yet" wherever no probe evidence rows exist — the
honest form, never a guessed score. Power serves it at /pi/api/parts when
the endpoint lands; until then the face renders its absence dark with the
reason (which is what v2/v3 already do).

## 5. What the face does NOT need

- No per-page percent until areas are applied (B4) — the face will not show
  one, and no seat should type one.
- No notes write path in this contract — notes today live on the device only
  (C5). Notes writing to the record, against the object, is a separate build
  with its own privacy proof; it is not smuggled into this endpoint.
- No permission change is requested here. The endpoint serves the same record
  the face already reads; privacy gating (owner vs outsider vs member
  negative tests) stays a separate, Shawn-gated decision.

## 6. Done means

The endpoint is done when a cold reader, from outside the builder's box,
fetches /pi/api/items and gets rows (not HTML, not aggregates alone), the
face renders those rows, and Resolve re-checks the face at the new commit
and scores it. Until then, every claim about rows stays "not yet" in plain
words.

## 7. Staleness escalation (pi-stalled-work-surfacing-20261026, implements SN-1874)

Status: CONTRACT, Power 2026-11-11. The rule below is the wire for the
Finish-It law (SN-1874): unfinished work surfaces itself; it is never
left silent. Face render of this section is Nitro's lane; the worker
serving it is Power's.

### 7.1 The rule — computed at read time, never by a background writer

An item is STALLED when ALL hold: state in (`in_progress`, `verifying`)
AND no state change for 48 hours AND no note for 48 hours. Last activity
= GREATEST(state_changed_at, last note entries[-1].at), falling back to
updated_at then created_at when either is null. days_stalled = (now -
last activity) in days, one decimal. This follows the write-door plan
§2.4: the stall clock is a derivation from timestamps already in the
record — no poller, no background writer, no auto-assign, no catch-up
writes, ever. The write door (S1) is the clock's source: every state
move stamps state_changed_at and every note carries its `at`.

Canonical derivation (any seat can re-run it live against work_items,
project a554e536-66a6-4808-8c36-988f13d9f394):

    SELECT item_key, title, state, owner_seat,
      TO_CHAR(GREATEST(COALESCE(state_changed_at, updated_at, created_at),
        COALESCE(((notes->'entries'->-1)->>'at')::timestamptz,
        COALESCE(state_changed_at, updated_at, created_at))),
        'YYYY-MM-DD HH24:MI') AS last_activity_utc,
      ROUND(EXTRACT(EPOCH FROM (NOW() - GREATEST(
        COALESCE(state_changed_at, updated_at, created_at),
        COALESCE(((notes->'entries'->-1)->>'at')::timestamptz,
        COALESCE(state_changed_at, updated_at, created_at)))))/86400, 1)
        AS days_stalled
    FROM work_items
    WHERE project_id = 'a554e536-66a6-4808-8c36-988f13d9f394'
      AND state IN ('in_progress', 'verifying')
      AND COALESCE(state_changed_at, updated_at, created_at)
        < NOW() - INTERVAL '48 hours'
      AND COALESCE(((notes->'entries'->-1)->>'at')::timestamptz,
        COALESCE(state_changed_at, updated_at, created_at))
        < NOW() - INTERVAL '48 hours'
    ORDER BY days_stalled DESC;

First live run of this derivation, 2026-11-11 ~10:40 PST: 107 stalled
of 130 in flight (81 in_progress, 26 verifying); oldest 17.5 days
(14q-pi-hub-10star, owner naya-power); 18 ownerless. needs_shawn: 6
items waiting 6.0–18.9 days. Full list in the weekly sweep post, board
#3066 (same pass). The clock is proven maintained: state_changed_at
differs from updated_at on 279 rows — it is not a copy of updated_at.

### 7.2 What the worker serves (extends §1 rows projection)

Per row, in addition to §1: `state_changed_at` (UTC ISO or null),
`last_note_at` (UTC ISO or null), `days_stalled` (number, or null when
the item is not in_progress/verifying), `stalled` (boolean). Top level,
in the same response, computed from the same rows: `stalled` (stalled
rows only, days_stalled desc) and `needs_shawn` (needs_shawn rows with
`days_waiting`). Aggregates stay computed from the rows, never typed.
owner_seat null renders ownerless, never a guessed owner. area_key is
not yet in the record (area schema packet not applied) — area-card
surfacing waits on the area application (B4); the needs-attention rail
does NOT wait.

### 7.3 What the face renders (Nitro)

- A needs-attention rail above the area tabs: stalled rows, each with
  title (link to the item), owner, days-stalled. Ownerless rows show
  ownerless, honestly.
- Each area card carries its stalled count + oldest days-stalled once
  areas are applied; until then the rail carries the whole list.
- needs_shawn items re-present on the director's rhythm with a prepared
  packet and a named tap (c2) — a packet that sits unmentioned is the
  same failure in a nicer folder (SN-1874 law 4).

### 7.4 Until the face carries it natively

A weekly unfinished-work sweep posts the stalled list to board #3066
(detail §3 of the item). First sweep: 2026-11-11 (this contract's
landing pass). First citizen: build-ambassador-system — queued, owner
naya-power, state unchanged since 2026-10-24, last note 2026-10-26,
finish line in hub area 7 (Memberships + Ambassador + Money) per board
6407818112. Its state must never again be discoverable only by the
director asking.

### 7.5 Done means

A deliberately stalled test item visibly escalates in the hub within
one cycle (rail + area card), and the ambassador item's state is
visible without asking. Until the rail renders live, this section is
contract, not proof — the sweep post is the working interim, labelled
as such, never claimed as the face.
