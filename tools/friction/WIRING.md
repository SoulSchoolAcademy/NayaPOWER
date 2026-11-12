# WIRING.md — tools/friction production integration contract

**Status: SHIPS DARK.** This package is pure repo code (stdlib only, no
database, no network). Nothing in production calls it. The points profile
it consumes (`points-profile-v1`) is itself PROPOSAL V1 — not ratified,
not wired (profile invariant 10: until ratified and wired, it issues
nothing). Friction activates only when every step below lands; until then
this document is the contract the wiring lane builds against, so nobody
has to guess.

## 1. The read path (where the stream comes from)

`balance.project()` consumes CONTRIBUTION_VALUE entries in the profile's
§7 dashboard-contract shape, attached to rows of the **existing**
`public.nayanet_smart_ledger` (no second ledger). A production reader —
a SQL view or a scheduled export job — must emit, per posting:

`entry_id · actor_id · action_class · occurred_at · posting_state ·
points · reversal_of · ledger_ref`

Two reader requirements, both load-bearing:

- **Reversals must be emitted as their own rows** (negative points,
  `reversal_of` set), exactly as the profile posts them. The production
  closure sync upserts by `(owner, source_table, source_id)` (census
  §7), so the reader reads the receipt layer, not a materialized balance —
  a reader that emits only current-state rows will silently drop
  reversals and overstate balances.
- **PENDING rows may be included or not** — the projection ignores them
  either way. Include them: the dashboard breakdown shows PENDING state,
  and the velocity watcher counts all actions, verified or not.

Feed shape to this package: JSONL, one entry per line, into `cli.py`
(batch) or the module APIs (`balance.project`, `friction.evaluate`,
`watchers.run_watchers`) for an in-process consumer.

## 2. Where tier checks gate (enforcement points)

Friction *decides*; surfaces *enforce*, server-side, in the write path —
the model is the v7 authorized-send pattern
(`nayanet_send_smart_mail_authorized`: authenticated identity check plus
an authority-grant check inside the write, never in the UI). A surface
about to perform an action:

1. resolves the actor's tier from the projection (or a cached
   `tier_state(actor)` refreshed on each new FINAL posting for that
   actor — the projection is a pure function, so caching is safe at any
   staleness the surface tolerates, and the refresh rule must be stated
   per surface);
2. applies the tier's limits data (`friction.TIERS`): `rate_multiplier`
   against the surface's own rate limit, `extra_verification_required`
   and `held_for_review` for sensitive actions, and at T3 the
   `permitted_action_classes` allowlist.

Wire in this order (highest harm first):

| # | Call site | Sensitive action gated |
|---|-----------|------------------------|
| 1 | Smart Mail send (v7 path) | send: T1 extra verification · T2 held for review · T3 not a repairing class → blocked |
| 2 | Ambassador link issuance | issue: same ladder |
| 3 | Space / page publishing | publish: same ladder |
| 4 | Match → connect initiation | connect: same ladder |

Client-side checks are decoration only; if the write path does not check,
the tier does not exist (SN-1855 question 3, asked at build time).

## 3. Friction events go back on the ledger

Every transition `friction.evaluate` emits is a decision about a citizen
and must itself be on the record (SN-1855: the friction decision is not an
off-ledger action). The wiring writer posts each transition back as a
ledger entry with `action_class = "friction_transition"`, using the same
writer pattern as census cure 4 (`nayanet_sync_ledger_source`), carrying
`from_tier / to_tier / balance / entry_id (the triggering posting)`.

Safety property, already in the code: `balance.py` never counts
`friction_transition` entries as postings, so replaying the full stream
(including written-back decisions) cannot double-apply a transition —
this is pinned by `test_emitted_events_replay_neutrally`.

## 4. Watchers runtime

`watchers.run_watchers` runs over a rolling export (suggested: the last
30 days of entries, hourly, as a job in the pattern of the existing
system watchers). Alerts are data. The job's only job is delivery:
post the alert set to the board (and, once mail is fitted, Smart Mail to
the watch seat). Alerts trigger **no** automatic action beyond the tier
table — friction keys off balance alone, so an alert can never punish
anyone; it is evidence for verification and for the pattern half of the
security watch (SN-1855 standing order 4).

Coverage caveat: the watchers see only what reaches the ledger. Until
census cure 4 lands (ledger writers for mail, clicks, PI items, matches,
ambassador issuance), velocity in particular watches the note/execution
core only. State that coverage limit wherever alert output is shown.

## 5. What rides the production gate (GT-039 class)

Repo-side (done or buildable now): this package + tests; the reader view
definition; the writer for friction events; the watcher job script.

Production-gated (Shawn's tap / admin hand, same class as GT-039):
- applying any migration that creates the reader view or the
  friction-event writer against production;
- RLS / RPC / Edge Function changes that make a surface consult tier
  state inside its write path (§2 call sites);
- turning any of it on. Activation additionally requires the points
  profile itself to be ratified — friction enforces the profile's
  balance, and an unratified balance is not a basis for consequences.

## 6. Config discipline

Tier floors (`friction.TIER_FLOORS`) and watcher thresholds
(`watchers.WATCHER_CONFIG`) are versioned config at the top of their
modules (`friction-profile-v1`, `watchers-v1`). Changing them is a
profile change: new version id, stated rationale, the recalibration
discipline of the points profile (0025 §13) — never a silent edit,
never a per-surface fork of the numbers. The system flows like water;
the config is how it flows, on the record.
