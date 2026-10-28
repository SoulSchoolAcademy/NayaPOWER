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
